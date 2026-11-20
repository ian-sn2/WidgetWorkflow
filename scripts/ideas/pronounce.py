"""Hard words: look each one up, teach it to the voice, remember it.

A neural voice guesses at a word it has rarely met (a surname, "heterochrony", "allopolyploidy"), and guesses differently
from one paragraph to the next. So before a paragraph is recorded, every rare word in it is looked up and the voice is
told the dictionary's pronunciation instead of being left to guess (Ian, 2026-11-18: "for complex words I would suggest
looking it up").

Where a pronunciation comes from, first hit wins:
  1. narration/pronounce.json   entered by hand: names no dictionary has, and anything a dictionary gets wrong
  2. narration/learned.json     what an earlier build looked up, so a word is looked up once, ever, for every chapter
  3. the installed dictionary   (misaki's, built from Wiktionary: about 89,000 words, offline)
  4. en.wiktionary.org          asked once per build for all of a page's unknown words (prepare), answers kept in learned.json
  5. a prefix and a known word  prezygotic = pre + zygotic
A rare word none of them knows is listed in the listening report as not found, and is left to the voice.
(CMUdict was tried for surnames and dropped: its names are machine guesses. It had Gillooly and Eldredge stressed on
the wrong syllable, and a wrong pronunciation taught is worse than the voice's own guess.)

"Rare" is measured, not judged: under RARE on the wordfreq scale (about one use in two million words), five letters or
more. Without wordfreq installed only the two files are applied.

    python scripts/ideas/pronounce.py heterochrony cichlids "Van Valen"     what would be taught, and from where
"""
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).parent
BY_HAND = HERE / 'narration' / 'pronounce.json'
LEARNED = HERE / 'narration' / 'learned.json'
CACHE = pathlib.Path('~/.cache/narrate').expanduser()
RARE = 2.7
WIKI = 'https://en.wiktionary.org/w/api.php?action=query&prop=revisions&rvprop=content&rvslots=main&format=json&formatversion=2&titles='
VOWELS = 'aeiouæɑɒʌəɛɪɔʊɜɝɚ'
ONSETS = {'pɹ', 'bɹ', 'tɹ', 'dɹ', 'kɹ', 'ɡɹ', 'fɹ', 'θɹ', 'ʃɹ', 'pl', 'bl', 'kl', 'ɡl', 'fl', 'sl', 'sp', 'st', 'sk', 'sm', 'sn', 'sw', 'tw', 'dw', 'kw',
          'spɹ', 'stɹ', 'skɹ', 'spl', 'skw', 'pj', 'bj', 'kj', 'fj', 'mj', 'hj', 'vj'}
PREFIXES = {'pre': 'pɹi', 'post': 'poʊst', 'allo': 'ælə', 'auto': 'ɔtoʊ', 'proto': 'pɹoʊtoʊ', 'non': 'nɑn', 'sub': 'sʌb', 'co': 'koʊ', 'anti': 'ænti',
            'micro': 'maɪkɹoʊ', 'macro': 'mækɹoʊ', 'inter': 'ɪntɚ', 'intra': 'ɪntɹə', 'poly': 'pɑli', 'hetero': 'hɛtəɹoʊ', 'homo': 'hoʊmoʊ', 'neo': 'nioʊ'}
MISAKI = [('A', 'eɪ'), ('I', 'aɪ'), ('O', 'oʊ'), ('W', 'aʊ'), ('Y', 'ɔɪ'), ('ʤ', 'dʒ'), ('ʧ', 'tʃ'), ('ᵊ', 'ə'), ('ᵻ', 'ɪ'), ('ɜɹ', 'ɝ'), ('əɹ', 'ɚ'), ('ɾ', 't'), ('Q', 'oʊ')]
SPELL = [('tʃ', 'ch'), ('dʒ', 'j'), ('eɪ', 'ay'), ('aɪ', 'eye'), ('oʊ', 'oh'), ('aʊ', 'ow'), ('ɔɪ', 'oy'), ('æ', 'a'), ('ɑ', 'ah'), ('ɒ', 'ah'), ('ʌ', 'uh'),
         ('ə', 'uh'), ('ɛ', 'eh'), ('ɪ', 'ih'), ('i', 'ee'), ('ɔ', 'aw'), ('ʊ', 'uu'), ('u', 'oo'), ('ɝ', 'er'), ('ɚ', 'er'), ('ɜ', 'er'), ('θ', 'th'),
         ('ð', 'dh'), ('ʃ', 'sh'), ('ʒ', 'zh'), ('ŋ', 'ng'), ('j', 'y'), ('ɹ', 'r'), ('ɡ', 'g'), ('e', 'ay'), ('o', 'oh'), ('a', 'ah')]
_files, _gold, _zipf, _asked = {}, None, None, 0.0


def _load(path):
    if path not in _files:
        _files[path] = {k.lower(): v for k, v in json.loads(path.read_text(encoding='utf8')).items() if not k.startswith('_')} if path.exists() else {}
    return _files[path]


def clean(ipa):
    """one spelling of IPA for every source: no slashes, no syllable dots, American r, no flap, no length marks"""
    ipa = re.sub(r'[/\[\].‿ː\s]', '', ipa)
    ipa = re.sub(r'\(([^)]*)\)', r'\1', ipa)              # an optional sound is said
    ipa = ipa.replace('g', 'ɡ').replace('ɾ', 't').replace('ɫ', 'l').replace('ɐ', 'ə').replace('ɘ', 'ə')
    ipa = re.sub(r'r', 'ɹ', ipa).replace('əɹ', 'ɚ').replace('ɜɹ', 'ɝ').replace('ɛɹ', 'ɛɹ')
    return ipa.replace('ɵ', 'oʊ').replace('ɨ', 'ɪ').replace('̩', '').replace('̯', '').replace('͡', '')


def from_misaki(ph):
    for a, b in MISAKI:
        ph = ph.replace(a, b)
    return clean(ph)


def to_misaki(ipa):
    """IPA -> the offline voice's own phoneme letters"""
    for a, b in MISAKI[:9]:
        ipa = ipa.replace(b, a)
    return ipa.replace('ɝ', 'ɜɹ').replace('ɚ', 'əɹ')


def syllables(ipa):
    """IPA -> [(stress, syllable)]. A stress mark counts for the syllable its next vowel is in, wherever it was written."""
    units, k = [], 0
    while k < len(ipa):
        two = ipa[k:k + 2]
        if two in ('eɪ', 'aɪ', 'oʊ', 'aʊ', 'ɔɪ', 'tʃ', 'dʒ'):
            units.append(two)
            k += 2
        else:
            units.append(ipa[k])
            k += 1
    sylls, onset, stress = [], [], ''
    for u in units:
        if u in 'ˈˌ':
            stress = u
        elif u[0] in VOWELS:
            if sylls and onset:                        # consonants between two vowels: the most that can start a syllable go to the second
                keep = len(onset)
                while keep > 1 and ''.join(onset[-keep:]) not in ONSETS:
                    keep -= 1
                if keep == 1 and onset[-1] == 'ŋ':
                    keep = 0
                sylls[-1][1] += ''.join(onset[:len(onset) - keep])
                onset = onset[len(onset) - keep:]
            sylls.append([stress, ''.join(onset) + u])
            onset, stress = [], ''
        else:
            onset.append(u)
    if sylls:
        sylls[-1][1] += ''.join(onset)
    return [(a, b) for a, b in sylls]


def respell(ipa):
    """a rough respelling a person can read without knowing IPA: gih-LOO-lee"""
    if ' ' in ipa.strip():
        return ' '.join(respell(part) for part in ipa.split())
    out = []
    for stress, syl in syllables(ipa):
        text, k = '', 0
        while k < len(syl):
            for a, b in SPELL:
                if syl.startswith(a, k):
                    text += b
                    k += len(a)
                    break
            else:
                text += syl[k]
                k += 1
        text = re.sub(r'(?<=.)eye', 'y', text)              # zy-GAH-tihk, not zeye-
        out.append(text.upper() if stress == 'ˈ' else text)
    return '-'.join(out)


def _english(text):
    """a Wiktionary page's wikitext -> (ipa, recorded clip or None) for its English entry, or None"""
    if '==English==' not in text:
        return None
    english = re.split(r'\n==[^=]', text.split('==English==', 1)[1])[0]
    found = re.findall(r'\{\{IPA\|en\|([^}]*)\}\}', english)
    if not found:
        return None
    american = [f for f in found if re.search(r'a=[^|]*(GA|US|GenAm)', f)] or [f for f in found if not re.search(r'a=[^|]*(RP|UK|AU|NZ)', f)] or found
    ipa = next((p for p in american[0].split('|') if p.startswith(('/', '['))), None)
    if not ipa:
        return None
    clip = re.search(r'\{\{audio\|en\|([^|}]*(?:us|US)[^|}]*)', english) or re.search(r'\{\{audio\|en\|([^|}]*)', english)
    return clean(ipa), clip.group(1) if clip else None


def _wiktionary(words):
    """words -> {word: (ipa, clip)} for those Wiktionary has. One request for up to 50 words: asked a word at a time
    from a shared address, Wiktionary answers "too many requests". Raises ConnectionError if it cannot be asked."""
    out = {}
    for k in range(0, len(words), 25):
        group = words[k:k + 25]
        titles = '|'.join(dict.fromkeys(t for w in group for t in (w, w.capitalize())))
        req = urllib.request.Request(WIKI + urllib.parse.quote(titles), headers={'User-Agent': 'study-notes-builder/1.0'})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=40) as r:
                    data = json.loads(r.read())
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 3:        # asked to wait: wait as long as it says, once or twice
                    time.sleep(min(int(e.headers.get('retry-after') or 20), 60) + 2)
                    continue
                raise ConnectionError('Wiktionary answered %d' % e.code) from None
            except (urllib.error.URLError, ValueError, OSError) as e:
                raise ConnectionError('Wiktionary could not be reached (%s)' % type(e).__name__) from None
        for page in data.get('query', {}).get('pages', []):
            text = (page.get('revisions') or [{}])[0].get('slots', {}).get('main', {}).get('content', '')
            got = _english(text)
            if got:
                out.setdefault(page['title'].lower(), got)
        time.sleep(1.5)
    return out


def _dictionary(word):
    global _gold
    if _gold is None:
        try:
            import misaki
            _gold = json.loads((pathlib.Path(misaki.__file__).parent / 'data' / 'us_gold.json').read_text(encoding='utf8'))
        except (ImportError, OSError):
            _gold = {}
    hit = _gold.get(word) or _gold.get(word.capitalize())
    if hit:
        return from_misaki(hit if isinstance(hit, str) else hit.get('DEFAULT') or next(iter(hit.values()))), 'dictionary'
    return None


def _plural(ipa, ending):
    last = ipa[-1]
    if ending == 'ing':
        return ipa + 'ɪŋ'
    if ending == 'ed':
        return ipa + ('ɪd' if last in 'td' else 't' if last in 'pkfθsʃ' else 'd')
    return ipa + ('ɪz' if last in 'szʃʒ' else 's' if last in 'ptkfθ' else 'z')


def lookup(word, _depth=0):
    """a word -> {'ipa':..., 'from':..., 'clip':...} or None. Never touches the network: prepare() does that, once."""
    w = word.lower()
    for store in (_load(BY_HAND), _load(LEARNED)):
        if w in store:
            e = store[w]
            if isinstance(e, str):
                return {'ipa': from_misaki(e), 'from': 'entered by hand'}
            if e.get('ipa'):
                return dict(e)
            # an empty entry: Wiktionary was asked and has nothing. The rules below may still build it.
    hit = _dictionary(w)
    if hit:
        return {'ipa': hit[0], 'from': hit[1]}
    if _depth == 0:                                    # cichlids, finches, nectaries, hybridized, coevolving: the plain word, with its ending added
        for ending, back, kind in (('ies', 'y', 's'), ('ied', 'y', 'ed'), ('ing', '', 'ing'), ('ing', 'e', 'ing'), ('es', '', 's'), ('s', '', 's'),
                                   ('ed', '', 'ed'), ('ed', 'e', 'ed')):
            base = w[:-len(ending)] + back
            if w.endswith(ending) and len(base) >= 4:
                got = lookup(base, _depth=1)
                if got:
                    return {'ipa': _plural(got['ipa'], kind), 'from': got['from'] + ', as %s + %s' % (base, kind)}
    if _depth == 0:
        for pre, sound in PREFIXES.items():             # prezygotic: no dictionary has it, every dictionary has zygotic
            base = w[len(pre):].lstrip('-')
            if w.startswith(pre) and len(base) >= 5:
                got = lookup(base, _depth=1)
                if got:
                    return {'ipa': 'ˌ' + sound + got['ipa'], 'from': '%s- + %s (%s)' % (pre, base, got['from'])}
    return None


def remember(entries):
    data = json.loads(LEARNED.read_text(encoding='utf8')) if LEARNED.exists() else {
        '_how': 'Written by pronounce.py: what a build looked up, so each word is looked up once. An empty entry means it was asked for and not found. '
                'To correct one, put the word in pronounce.json, which wins.'}
    data.update(entries)
    LEARNED.write_text(json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=1) + '\n', encoding='utf8')
    _files.pop(LEARNED, None)


def fixed(word):
    """for the offline voice, which has the dictionary built in: only what was entered by hand or looked up online"""
    for store in (_load(BY_HAND), _load(LEARNED)):
        e = store.get(word.lower())
        if e:
            return e if isinstance(e, str) else to_misaki(e['ipa']) if e.get('ipa') else None
    return None


def prepare(text):
    """before a page is recorded: ask Wiktionary, in one go, for every rare word on it that nothing here knows yet.
    -> a line to print. A word asked for and not found is remembered as empty, so it is not asked for again."""
    ask = []
    for word in dict.fromkeys(w.lower() for w in re.findall(r'[A-Za-z]{5,}', text)):
        if is_rare(word) and word not in _load(BY_HAND) and word not in _load(LEARNED):
            got = lookup(word)
            if not got or '- + ' in got['from']:        # nothing knows it, or it was only built from a prefix: a real entry is better
                ask.append(word)
    if not ask:
        return ''
    try:
        found = _wiktionary(ask)
    except ConnectionError as e:
        return 'hard words: %d not looked up online (%s); the dictionary and the two files are still used' % (len(ask), e)
    remember({w: ({'ipa': found[w][0], 'from': 'Wiktionary', **({'clip': found[w][1]} if found[w][1] else {})} if w in found else {}) for w in ask})
    return 'hard words: asked Wiktionary for %d, it had %d' % (len(ask), len(found))


def is_rare(word):
    global _zipf
    if _zipf is None:
        try:
            from wordfreq import zipf_frequency
            _zipf = zipf_frequency
        except ImportError:
            _zipf = False
    return bool(_zipf) and len(word) >= 5 and _zipf(word.lower(), 'en') < RARE


def for_text(text):
    """the hard words in a passage -> ([(phrase exactly as it is written, ipa, entry)], [rare words nothing knows])"""
    taught, unknown, done = [], [], set()
    low = text.lower()
    for phrase, e in _load(BY_HAND).items():           # hand entries first: they can be two words ("van valen") and need not be rare
        m = re.search(r'(?<![a-z])' + re.escape(phrase) + r'(?![a-z])', low)
        if m:
            got = lookup(phrase)
            taught.append((text[m.start():m.end()], got['ipa'], got))
            done.update(phrase.split())
    for word in dict.fromkeys(re.findall(r"[A-Za-z]{5,}", text)):
        w = word.lower()
        if w in done or not is_rare(w) or word.isupper():
            continue
        done.add(w)
        got = lookup(w)
        if got:
            taught.append((word, got['ipa'], got))
        else:
            unknown.append(w)
    return taught, unknown


if __name__ == '__main__':
    print(prepare(' '.join(sys.argv[1:])) or 'nothing to look up online')
    for arg in sys.argv[1:]:
        got = lookup(arg)
        print(arg + ':', '%s  /%s/  from %s%s' % (respell(got['ipa']), got['ipa'], got['from'], '  clip: ' + got['clip'] if got.get('clip') else '')
              if got else 'no pronunciation found')
