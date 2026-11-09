MAR3023-Fall26-Chapter15-Full.html

Source: Ian's `MAR3023-Fall26-Chapter15-Full.html` (2026-10-21) plus its
ten PNGs on S3. Built with `scripts/apply_widgets.py --toc` from a map; the
engine (v2.60) is embedded after the house script, the head's
`content/sn25-v5.js` is swapped for the live `studyguide/sn25-v2.js`, and
nothing else in the file changed (apply_widgets proves it before writing).

## Images: 10 -> 5 widgets, 4 HTML figures, 0 kept

| # | image | what it is now |
|---|---|---|
| 01 | old-distribution-system | one HTML figure with 02: two inline-SVG panels side by side, "Old System" and "With Cross-Docking", drawn on the prose's numbers -- four manufacturers and three stores, twelve direct routes against four trucks in and three out (the picture shows three and three; rule 3, prose wins, and said so here). Receiving / Sorting / Shipping bands in the center as drawn. |
| 02 | cross-docking-system | folded into 01's figure (its tag is removed; the figure sits where 01 was, before the paragraph that counts the routes) |
| 03 | supply-chain-diagram | **widget**: a vertical chain Supplier -> Manufacturer -> Consumer, links named "Raw materials/parts" and "Finished products", four steps: the chain, then the Supplier network brace, the Marketing channel brace, and the Supply Chain brace over both |
| 04 | coverage-spectrum | HTML figure: one two-headed SVG arrow, teal to purple, Intensive / Selective / Exclusive above and Convenience / Prestige at the ends |
| 05 | direct-channel-flow | **widget**: a vertical chain Manufacturer -> Consumer, static, with a caption |
| 06 | indirect-channel-flow | **widget**: a vertical chain Manufacturer -> Wholesaler -> Retailer -> Consumer, static; no caption, because the paragraph under it says everything the caption said (check_file's prose rule) |
| 07 | wholesaler-types-matrix | HTML table: Possess & Hold Inventory? YES / NO across, Manufacturer-Owned? YES / NO down, the four kinds in the cells; opts out of the house table rules (`financial`) so it fits a phone |
| 08 | channel-conflict-diagram | HTML figure: the tree as drawn (Manufacturer, Wholesaler, two Retailers, two Consumers), the purple two-headed arrow between the retailers for horizontal conflict and the red one between the wholesaler and Retailer 2 for vertical; floats right at the width the image had |
| 09 | old-channel-view | **widget**: a horizontal chain Manufacturer -> Product -> Marketing Channel -> Out Product with plain arrows (the pipeline); no caption, the prose states it |
| 10 | new-channel-view | **widget**: the same chain with the chain motif and a + between its last links, ending "Out Product +"; no caption |

## Engine (v2.60)

Vertical chains (`flow.vertical`), brace spans with rows, plain-arrow
links, a link label `size`, and node names auto-fitted to their boxes. See
`docs/engine-reference.md`.

## Flagged, not changed

- `<u>` on the B, O, P, U, S and B, O, R, I, S letters in the omnichannel
  paragraph: the house format never underlines, but this is the source's
  own device for the acronyms. check_file FAILs on it; your call.
- check_file's "names its source ('recording')" is "a shared, decentralized
  digital ledger for recording and tracking transactions": a word, not a
  source. False positive.
- The franchising advantages/disadvantages table (nested lists in cells)
  scrolls a phone sideways by 185px at 390px and 256px at 320px; it is the
  source's table, untouched.
- The head links the font before `sn25-v6.css` (check_file WARN); left as
  sent.
- No `<!-- IMAGE POSITION -->` comments in the source, so none here.
- Named people: none.

## Checks

check_file: 2 FAIL (the two flagged above), 2 WARN (head order, no IMAGE
POSITION comments). render_widgets: 8 screenshots, no engine errors.
mobile_check 390 and 320: every widget fits with usable controls; the one
problem is the source table above.
