set -u
S=${QMB_WORK:?set QMB_WORK to the folder holding src/ (the unpacked zip), maps/ and deliver/}
D="$S/deliver/e - QMB3200 Widgets"; find "$D" -name "*.html" -delete 2>/dev/null; mkdir -p "$D"
for exam in 1 2; do for part in 1 2 3; do
  src="$S/src/e - QMB3200/Exam $exam - DONE/0$part - QMB3200 UCF Exam $exam Part $part - DONE"
  out="$D/Exam $exam/0$part - QMB3200 UCF Exam $exam Part $part"; mkdir -p "$out"
  for ed in Full Balanced Concise; do
    f="UCF QMB3200-262-Exam$exam-Part$part-$ed.html"
    flags="--toc"; sfx=""; [ "$ed" = Concise ] && { flags="--toc --anchors"; sfx="-Concise"; }
    echo "== Exam $exam Part $part $ed"
    python3 scripts/apply_widgets.py "$src/$f" "$S/maps/Part$part-Exam$exam$sfx.json" "$out/$f" $flags 2>&1 | tail -3
  done
done; done
