"""Google Cloud Text-to-Speech (Chirp 3: HD voices) as the narrator.

    NARRATE_ENGINE=google python scripts/ideas/build_demos.py ...      record with Google instead of the offline voice
    python scripts/ideas/narrate.py voices                             list the Chirp 3: HD voices the key can use
    python scripts/ideas/narrate.py sample "Some text." out.mp3        one clip in the current voice, to compare by ear

Setup is in scripts/ideas/GOOGLE-VOICE-SETUP.md. The key is read from the GOOGLE_TTS_KEY environment variable and sent
in the X-Goog-Api-Key header; it is never written to a file or a page.

Two things keep this free:
  * every recorded paragraph is kept in ~/.cache/narrate, so rebuilding a study guide sends only the paragraphs
    whose script changed;
  * the characters sent are tallied per calendar month in ~/.cache/narrate/google-usage.json, and the build stops
    before the month's total passes GOOGLE_TTS_MONTHLY_LIMIT (default 900,000, under Google's 1,000,000 free).
"""
import base64
import datetime
import io
import json
import os
import pathlib
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

import numpy as np

API = 'https://texttospeech.googleapis.com/v1/'
DEFAULT_VOICE = 'en-US-Chirp3-HD-Aoede'
RATE = 24000
LIMIT = int(os.environ.get('GOOGLE_TTS_MONTHLY_LIMIT', '900000'))
USAGE = pathlib.Path(os.environ.get('NARRATE_CACHE', '~/.cache/narrate')).expanduser() / 'google-usage.json'
sent_this_run = 0


def _call(path, body=None):
    """one request to the API, retried when Google asks us to slow down"""
    # In a cloud session the key is attached to the request by the session itself, so a placeholder is sent here.
    headers = {'X-Goog-Api-Key': os.environ.get('GOOGLE_TTS_KEY', 'supplied-by-the-session'), 'Content-Type': 'application/json'}
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf8', 'replace')[:600]
            if e.code in (429, 500, 502, 503) and attempt < 4:
                time.sleep(2 ** attempt * 2)
                continue
            raise RuntimeError('Google Text-to-Speech refused the request (%d): %s' % (e.code, detail)) from None
    raise RuntimeError('Google Text-to-Speech did not answer')


def used(month=None):
    month = month or datetime.date.today().strftime('%Y-%m')
    try:
        return json.loads(USAGE.read_text()).get(month, 0)
    except (OSError, ValueError):
        return 0


def _tally(chars):
    global sent_this_run
    month = datetime.date.today().strftime('%Y-%m')
    try:
        data = json.loads(USAGE.read_text())
    except (OSError, ValueError):
        data = {}
    data[month] = data.get(month, 0) + chars
    USAGE.parent.mkdir(parents=True, exist_ok=True)
    USAGE.write_text(json.dumps(data, indent=1))
    sent_this_run += chars


def _samples(response):
    import soundfile
    samples, rate = soundfile.read(io.BytesIO(base64.b64decode(response['audioContent'])), dtype='float32')
    assert rate == RATE, 'Google returned %d Hz, expected %d' % (rate, RATE)
    return np.asarray(samples if samples.ndim == 1 else samples[:, 0], dtype=np.float32)


def _stretch(samples, speed):
    """change the pace without changing the pitch, for a voice that will not do it itself"""
    import soundfile
    with tempfile.TemporaryDirectory() as tmp:
        soundfile.write(tmp + '/a.wav', samples, RATE)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp + '/a.wav', '-af', 'atempo=%.3f' % speed, '-ar', str(RATE), tmp + '/b.wav'], check=True)
        out, _ = soundfile.read(tmp + '/b.wav', dtype='float32')
    return np.asarray(out, dtype=np.float32)


def synthesize(text, voice, speed=1.0):
    """text -> samples at RATE. Refuses to start a request that would take the month past the free allowance."""
    month_total = used()
    if month_total + len(text) > LIMIT:
        raise SystemExit('Google voice: %s characters already sent this month and this paragraph is %d more, which passes the limit of %s '
                         '(GOOGLE_TTS_MONTHLY_LIMIT). Nothing was sent. Wait for next month, raise the limit, or record with NARRATE_ENGINE=kokoro.'
                         % (format(month_total, ','), len(text), format(LIMIT, ',')))
    body = {'input': {'text': text}, 'voice': {'languageCode': '-'.join(voice.split('-')[:2]), 'name': voice},
            'audioConfig': {'audioEncoding': 'LINEAR16', 'sampleRateHertz': RATE}}
    if abs(speed - 1.0) > 0.001:
        body['audioConfig']['speakingRate'] = speed
    try:
        out = _samples(_call('text:synthesize', body))
    except RuntimeError as e:
        if 'speakingRate' not in body['audioConfig'] or '(400)' not in str(e):
            raise
        del body['audioConfig']['speakingRate']         # this voice does not take a pace: record at its own and stretch it here
        out = _stretch(_samples(_call('text:synthesize', body)), speed)
    _tally(len(text))
    return out


def voices(language='en-US'):
    listed = _call('voices?languageCode=' + language).get('voices', [])
    return sorted((v['name'], v.get('ssmlGender', '')) for v in listed if 'Chirp3-HD' in v['name'])


def summary():
    return 'Google voice: %s characters sent in this run, %s this month of a %s limit' % (format(sent_this_run, ','), format(used(), ','), format(LIMIT, ','))
