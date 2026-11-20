"""Tests for what the narrator is given to say. Run after changing narrate.py, pronounce.py, hear.py or narration/say.json:

    python scripts/ideas/test_narration.py

The first five cases are Ian's text-to-speech test sheet (2026-11-18): each "should say" item that is decided before the
voice is involved is checked here. What only an ear can judge (pacing, a science word's sound) is not.
"""
import sys

import hear
import narrate
import pronounce

FAILED = []


def check(name, got, *wanted, absent=()):
    for w in wanted:
        if w not in got:
            FAILED.append('%s: expected %r in %r' % (name, w, got))
    for w in absent:
        if w in got:
            FAILED.append('%s: did not expect %r in %r' % (name, w, got))


say = narrate.say
# 1. Roman numerals and subscripts
t = say('Trigeminal nerve (CN V) – It has three divisions—ophthalmic (V₁), maxillary (V₂), and mandibular (V₃)—that divide the face. '
        'CN VII covers the front two-thirds of the tongue, CN IX covers the back third, and CN X covers the epiglottis. The accessory nerves (CN XI).')
check('roman', t, 'CN 5', 'CN 7', 'CN 9', 'CN 10', 'CN 11', 'V 1', 'V 2', 'V 3', 'two-thirds', absent=('CN V', 'CN X', '₁', '—', '–'))
check('roman list', say('CN IX, X and XI; types I and II; phase III'), 'CN 9, 10 and 11', 'types 1 and 2', 'phase 3')
check('letters stay letters', say('vitamin D, plan X, Activity V and hepatitis C'), 'vitamin D', 'plan X', 'Activity V')
# 2. Greek letters and biology abbreviations
t = say('β-galactosidase transfers an acetyl group from acetyl-CoA. E. coli produce cyclic AMP (cAMP), a derivative of ATP, in the lac operon (CRP).')
check('greek', t, 'beta-galactosidase', 'acetyl co-A', 'E. coli', 'cyclic AMP (cyclic A M P)', 'ATP', 'lack operon', 'CRP', absent=('β', 'cAMP'))
check('sentences', ' | '.join(narrate.sentences('Dr. Gillooly said so. E. coli grows fast. See Fig. 3 here. Done.')),
      'Dr. Gillooly said so. | E. coli grows fast. | See Fig. 3 here. | Done.')
# 3. A formula with money and percentages
t = say('If the commission is 6%: Gross Price = Target Net Price ÷ (1 − Commission Rate) = $200,000 ÷ (1 − 0.06) = $212,766. As low as 1% to 1.5%. (FSBO) outside the MLS (CCIM).')
check('formula', t, '6 percent', 'Gross Price equals Target Net Price divided by (1 minus Commission Rate) equals two hundred thousand dollars divided by (1 minus point zero six) equals '
      'two hundred twelve thousand seven hundred sixty-six dollars',
      '1 percent to 1.5 percent', 'fizz-bo', 'MLS', 'CCIM', absent=('=', '÷', '%', '$', 'FSBO'))
# 4. Table rows
t = say('Truckload (TL): Average haul of 274 miles; capacity of 42,000–50,000 lb. (about 20–25 tons). Less-than-truckload (LTL). A 2016 figure was about $1.59 per mile, around $2.25 per mile.')
check('rows', t, 'TL', 'LTL', '274 miles', 'forty-two thousand to fifty thousand pounds (about 20 to 25 tons)', '2016', '$1.59 per mile', '$2.25 per mile', absent=('lb', '–'))
# 5. Long paragraph
t = say('Hypoglossal nerve (CN XII) – the visible part of the tongue—the portion you use for chewing—whereas CN IX and CN X handle the rest: if it veers off-center.')
check('long', t, 'CN 12', 'CN 9 and CN 10', 'tongue, the portion you use for chewing, whereas', 'rest: if', absent=('—',))
# tables and arithmetic, from the MAN4504 chapter
check('arithmetic', say('Total Cost = 100(0)+700(40)+50(52)'), 'equals 100 times 0 plus 700 times 40 plus 50 times 52')
check('money sum', say('Total Cost = $0+$28,000+$2,600'), '0 dollars plus twenty-eight thousand dollars plus two thousand six hundred dollars')
# a number with a thousands separator goes to the voice in words: in digits, "4,712 units" was said "four, seven twelve"
check('grouped', say('or 4,712 units, the remaining 1,488; 1,000,000 in all; 1,234.50; a 2016 figure; items 1,2 and 3'), 'four thousand seven hundred twelve units',
      'one thousand four hundred eighty-eight;', 'one million in all', 'one thousand two hundred thirty-four point five zero', 'a 2016 figure', '1,2 and 3')
check('signed', say('Monthly Inventory Change: +200, then −150'), 'plus 200', 'minus 150')
check('cell', say('Layoff Cost: $ 600; # of Workers = 10; Hiring / Layoffs; and/or'), '600 dollars', 'Number of Workers equals 10', 'Hiring or Layoffs', 'and/or')
# the listener's idea of "the same words"
for written, heard in (('1 minus point zero six equals 212,766 dollars', '1 minus .06 equals $212,766'), ('fifty plus one hundred fifty equals two hundred', '50 + 150 = 200'),
                       ('four thousand seven hundred twelve units and nine hundred and five', '4,712 units and 905'), ('the remaining one thousand four hundred eighty-eight', 'the remaining 1,488'), ('two weeks and 0.50', '2 weeks and 0.5'),
                       ('It costs 105,152 dollars', 'It costs $105,152.')):
    score, diffs = hear.compare(written, heard)
    if diffs:
        FAILED.append('listener: %r against %r reported %r' % (written, heard, diffs))
score, diffs = hear.compare('or four thousand seven hundred twelve units', 'or for 712 units')
if not any(hear.serious(d) for d in diffs):
    FAILED.append('listener: "for 712" passed as 4,712')
score, diffs = hear.compare('It finishes in week 12', 'It finishes in week 20')
if not any(hear.serious(d) for d in diffs):
    FAILED.append('listener: a wrong number was not reported')
if not hear.is_term(('gillooly', 'galloulli')):
    FAILED.append('listener: a misspelled name was not treated as a term')
# hard words
check('respell', pronounce.respell('ɡɪˈluli'), 'gih-LOO-lee')
check('respell two words', pronounce.respell('væn ˈveɪlən'), 'van VAY-luhn')
got = pronounce.lookup('gillooly')
check('by hand', got['ipa'] if got else '', 'ɡɪˈluli')
if pronounce._dictionary('cichlid'):                 # the installed dictionary is optional; these need it
    for word, ending in (('cichlids', 'dz'), ('hybridized', 'zd'), ('nectaries', 'iz'), ('coevolving', 'ɪŋ')):
        got = pronounce.lookup(word)
        if not got or not got['ipa'].endswith(ending):
            FAILED.append('ending: %s gave %r' % (word, got))
    got = pronounce.lookup('prezygotic')
    check('prefix', got['from'] if got else '', 'pre- + zygotic')
taught, unknown = pronounce.for_text('Leigh Van Valen and Dr. Gillooly\'s notes.')
check('phrases', ' '.join(p for p, _, _ in taught), 'Van Valen', 'Gillooly')

print('%d failing' % len(FAILED))
for f in FAILED:
    print('  FAIL', f)
sys.exit(1 if FAILED else 0)
