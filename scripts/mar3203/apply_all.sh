#!/bin/bash
# Apply every chapter map to its three editions. MAR_WORK holds src/ (Exams 2-4),
# src1/ (Exam 1), maps/ and deliver/. Pass chapter keys to limit the run.
set -u
S=${MAR_WORK:?set MAR_WORK}
D="$S/deliver/f - MAR3203 UCF Widgets"; mkdir -p "$D"
REPO=$(cd "$(dirname "$0")/../.." && pwd)
declare -A SRC=(
  [Exam1-OperationsProductivity]="src1/01 - MAR3203 UCF Exam 1 OperationsProductivity - DONE|Exam 1/01 - MAR3203 UCF Exam 1 OperationsProductivity"
  [Exam1-Forecasting]="src1/02 - MAR3203 UCF Exam 1 Forecasting - DONE|Exam 1/02 - MAR3203 UCF Exam 1 Forecasting"
  [Exam1-InventoryMgmt]="src1/03 - MAR3203 UCF Exam 1 Inventorymanagement - DONE|Exam 1/03 - MAR3203 UCF Exam 1 Inventorymanagement"
  [Exam1-ZTableSupplement]="src1/04 - MAR3203 UCF Exam 1 ZTableSupplement - DONE|Exam 1/04 - MAR3203 UCF Exam 1 ZTableSupplement"
  [Exam2-ProjectMgmt]="src/Exam 2 - DONE/01 - MAR3203 UCF Exam 2 ProjectManagement - DONE|Exam 2/01 - MAR3203 UCF Exam 2 ProjectManagement"
  [Exam2-Processes]="src/Exam 2 - DONE/02 - MAR3203 UCF Exam 2 Processes - DONE|Exam 2/02 - MAR3203 UCF Exam 2 Processes"
  [Exam2-CapacityMgmt]="src/Exam 2 - DONE/03 - MAR3203 UCF Exam 2 CapacityManagement - DONE|Exam 2/03 - MAR3203 UCF Exam 2 CapacityManagement"
  [Exam3-JITLeanOps]="src/Exam 3 - DONE/1 - MAR3203 UCF Exam 3 JITLeanOperations - DONE|Exam 3/1 - MAR3203 UCF Exam 3 JITLeanOperations"
  [Exam3-QualityMgmt]="src/Exam 3 - DONE/2 - MAR3203 UCF Exam 3 QualityManagement - DONE|Exam 3/2 - MAR3203 UCF Exam 3 QualityManagement"
  [Exam3-SPC]="src/Exam 3 - DONE/3 - MAR3203 UCF Exam 3 SPC - DONE|Exam 3/3 - MAR3203 UCF Exam 3 SPC"
  [Exam4-SupplyChainMgmt]="src/Exam 4 - DONE/01 - MAR3203 UCF Exam 4 SupplyChainManagement - DONE|Exam 4/01 - MAR3203 UCF Exam 4 SupplyChainManagement"
  [Exam4-SupplyChainAnalytics]="src/Exam 4 - DONE/02 - MAR3203 UCF Exam 4 SupplyChainAnalytics - DONE|Exam 4/02 - MAR3203 UCF Exam 4 SupplyChainAnalytics"
)
keys=("$@"); [ ${#keys[@]} -eq 0 ] && keys=("${!SRC[@]}")
for k in "${keys[@]}"; do
  IFS='|' read -r src out <<< "${SRC[$k]}"
  mkdir -p "$D/$out"
  for ed in Full Balanced Concise; do
    f=$(ls "$S/$src"/*-$ed.html 2>/dev/null | head -1); [ -z "$f" ] && { echo "!! no $ed file for $k"; continue; }
    map="$S/maps/$k.json"; flags="--toc"
    if [ "$ed" = Concise ]; then map="$S/maps/$k-Concise.json"; flags="--toc --anchors"; fi
    [ -f "$map" ] || map="$S/maps/$k.json"
    echo "== $k $ed"
    python3 "$REPO/scripts/apply_widgets.py" "$f" "$map" "$D/$out/$(basename "$f")" $flags 2>&1 | grep -v '^UCF' | grep -v '^\s*$'
  done
done
