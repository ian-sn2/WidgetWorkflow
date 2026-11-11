#!/usr/bin/env python3
"""Tests for check_arithmetic.py. Prints one line per case and "N failing" last (what ci_check.py reads)."""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_arithmetic import check, page_text  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
failing = 0


def case(name, html, wrong, checked=None):
    """wrong: how many calculations must be reported wrong; checked: how many must be found at all"""
    global failing
    ok_list, bad = check(page_text(html))
    ok = len(bad) == wrong and (checked is None or len(ok_list) + len(bad) == checked)
    failing += not ok
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f"  (found {len(ok_list) + len(bad)}, wrong {len(bad)})"))


# right answers pass, including rounding to the places shown and a chain of steps
case("a plain sum", "<p>μ = 2 + 2 + 4 + 5 + 2 = 15 weeks</p>", 0, 1)
case("a chain with brackets and 4(2)", "<p>t = [1 + 4(2) + 3] ÷ 6 = 12 ÷ 6 = 2</p>", 0, 2)
case("rounded to the places shown", r"<p>\[z = \frac{16 - 15}{1.76} = \frac{1}{1.76} = \mathbf{0.57}\]</p>", 0, 2)
case("products of brackets", "<p>x = (2.33)(1.76) + (15) = 4.10 + 15 = <strong>19.10</strong></p>", 0, 2)
case("a square root", r"<p>\(= \sqrt{3.11} = \) <strong>1.76 weeks</strong></p>", 0, 1)
case("a squared fraction in sup", "<p>v = [(9−1) ÷ 6]<sup>2</sup> = (4 ÷ 3)<sup>2</sup> = 1.78</p>", 0, 2)
case("thousands separators and dollars", "<p>Total Cost = $0 + $28,000 + $2,600 = $30,600</p>", 0, 1)
case("a percentage", r"<p>\(\%\Delta Q = \frac{12 - 8}{10} = 40\%\)</p>", 0, 1)
case("a rounded input carried through", r"<p>\(DWL = \frac{1}{2} \times 200 \times 266.67 = 26{,}666.67\)</p>", 0, 1)
case("a calculation over several lines",
     "<p>Total Cost = 100(0)+700(40)</p>\n\n<p>Total Cost = $0+$28,000</p><p>Total Cost = $28,000</p>", 0, 2)
case("labels in brackets are not factors", "<p>3 (B) + 4 (D) + 5 (G) + 2 (H) = 14 weeks</p>", 0, 1)

# wrong answers are caught
case("a sum off by one", "<p>μ = 2 + 2 + 4 + 5 + 2 = 14 weeks</p>", 1)
case("rounded the wrong way", r"<p>\[z = \frac{1}{1.76} = 0.58\]</p>", 1)
case("a wrong final step in a chain", "<p>x = (2.33)(1.76) + 15 = 4.10 + 15 = 19.20</p>", 1)
case("a wrong middle step in a chain", "<p>t = [1 + 4(2) + 3] ÷ 6 = 14 ÷ 6 = 2</p>", 1)   # 14 ÷ 6 rounds to 2, so only the first step is wrong
case("a wrong total over several lines",
     "<p>Total Cost = 100(0)+700(40)</p><p>Total Cost = $28,500</p>", 1)

# words and variables are not arithmetic
case("variables are skipped", "<p>Slack = LS − ES</p><p>z = (x − μ)/σ</p>", 0, 0)
case("dates and ranges are skipped", "<p>Tuesday, 4/14/26. Plans run 3–18 months.</p>", 0, 0)
case("widget data in scripts is skipped", '<script type="application/json">{"cap": "2 + 2 = 5"}</script>', 0, 0)

# a real page: the aggregate planning chapter as built, and the same page with its total changed
src = ROOT / "chapters/MAN4504/Exam3-AggregatePlanning/source/MAN4504-263-Exam3-AggregatePlanning-FULL.html"
if src.exists():
    page = src.read_text(encoding="utf-8")
    case("the aggregate planning chapter is right", page, 0)
    assert page.count("$105,700") == 1
    case("its total changed to $105,770 is caught", page.replace("$105,700", "$105,770"), 1)

print(f"{failing} failing")
sys.exit(1 if failing else 0)
