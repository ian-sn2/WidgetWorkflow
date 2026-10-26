REE3043-263-Exam3-Homeownership.html

Source: the chapter file as sent (house head already current: `sn25-v6.css`, `studyguide/sn25-v2.js`). The only change is the figure; the `<!--SDG-ENGINE-->` placeholder went in after the house script and `embed_engine.py` filled it.

Figure → widget (1 of 1): the inline SVG "PV of Cost of Owning − PV of Cost of Renting" becomes one widget with four scenario buttons.
* Base case: the line crosses zero just past 4 years (the fitted line through the four stated values crosses at 4.6; the prose says "more than 4 years"). The four stated years are marked on the line and their values are in the caption: +$9,504, +$3,529, −$2,303, −$7,995. The line's heights are symbolic, as in the source, which prints only "$" and "0" on that axis.
* Rent of $1,600, 5% appreciation, Standard deduction: the three sensitivity cases from the prose, each a line through zero at its stated break-even year (about 3, 2 and 8). Nothing else about those lines is stated, so nothing else is drawn.
* The source's callout box ("This is the holding period at which…") is the lede; the two red braces (Owning Preferred, Renting Preferred) are kept, wrapped on two lines.

Decisions: the axes cross at the origin so the line runs through zero on the Q axis, which is how the source draws it. The checker's prose warning on the base caption is accepted: the four values restate the paragraph below, and the caption exists to put them on the figure.

Names: "Dr. Ling" appears throughout the chapter's prose as sent; nothing in the widget names anyone. For Ian to confirm before publication, as always.

Checks: `check_file.py` 0 widget FAIL (the two FAILs are the source's own prose: "In this lecture" and "deed recording fees" trip the source-word check); `render_widgets.py` four scenarios, no engine errors; `mobile_check.py` 0 problems at 390px.
