"""أرضيّةُ الجرد: النصُّ يحتمل تسعةَ عشرَ صامتًا بكلفةِ صفر.

**السؤال**: النصُّ يشهد أنّ الرسمَ لا يميّز **أكثرَ** من ثمانيةٍ وعشرين إلّا
في سبعةَ عشرَ نوعًا. فهل يشهد أنّه لا يميّز **أقلَّ**؟

**الجواب مقيسًا**: لا. دمجٌ جشعٌ على ١٨٬٩٩٢ نوعًا مشكولًا يُنزِل الصوامتَ
من سبعةٍ وعشرين إلى **تسعةَ عشرَ** بثماني دمجاتٍ **كلُّها مجّانيّة**: لا
نوعَ واحدٌ يُفقَد. والأصنافُ الناتجةُ: `تزظ` · `ثح` · `جخ` · `ذطغ` · `رض` ·
`شك`.

**مسحوبٌ جزئيًّا — انظر `test_substrate_convergence`**: القياسُ ههنا على
**الرسم المشكول الخام**، وعلى أساسٍ مطبَّعٍ تصير الأرضيّةُ ٢١ لا ١٩. والأهمُّ:
«الأرضيّة» بمعيار **الحمل الوظيفيّ** (تمايزُ الأنواع) غيرُ الأرضيّة بمعيار
**الاسترجاع** (`Open(Close(x)) ≅ x`)، والمشروعُ يسأل الثاني. فما دون ٢٨ ممتنعٌ
عنده من **داخل الترميز** لا من أذنٍ ولا مدوَّنة. وما يبقى صحيحًا ههنا هو
الأرقامُ على ركيزتها، لا الحكمُ المبنيُّ عليها.

`THE_TEXT_BOUNDS_FROM_ABOVE_AND_NOT_FROM_BELOW`: هذا هو الحدُّ الفاصل. النصُّ
يحدّ الجردَ **من فوق** بدقّةٍ شديدة (٠٫٠٩٠٪ كلفةً للنزول إلى ما دون الرسم)،
ولا يحدّه **من تحت** إلّا عند تسعةَ عشر. فالثمانيةُ والعشرون ليست لازمةً عن
النصّ؛ هي **واقعةٌ في مجالٍ يسمح به النصُّ ولا يفرضه**.

`THE_CLASSES_THE_TEXT_TOLERATES_ARE_ONES_NO_EAR_TOLERATES`: `ثح` تجعل
«ثوب» و«حوب» صورةً واحدة، و`جخ` تجعل «جبل» و«خبل» صورةً واحدة. ولا ناطقَ
يقبلهما. فالفجوةُ بين ١٩ و٢٨ **ليست فجوةَ بياناتٍ نصّيّةٍ تُسَدّ بمدوَّنةٍ
أكبر** — هي بعينها الفجوةُ التي لا يسدّها إلّا **أذن**. وتأجيلُ التجربة
النطقيّة لا يُلغي هذه الفجوةَ بل **يتركها مفتوحةً بعددها**.

`GREEDY_GIVES_A_CEILING_ON_THE_FLOOR_NOT_THE_FLOOR`: الدمجُ جشعٌ بترتيبٍ
ثابت، فتسعةَ عشرَ **حدٌّ أعلى للأرضيّة** لا الأرضيّةُ نفسُها؛ وترتيبٌ آخرُ
قد ينزل أدنى. وهذا يُقوّي القولَ ولا يُضعفه: ما يحتمله النصُّ ١٩ **فأقلّ**.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import rounds_to

TYPES = 18_992
CONSONANT_GRAPHEMES = 27
"""حروفُ الهجاء بلا همزةٍ ولا ألف: ما دخل الدمجَ الجشع."""

FLOOR = 19
FREE_MERGES = 8
CLASSES = ("تزظ", "ثح", "جخ", "ذطغ", "رض", "شك")

# كلفةُ الدمج على الركيزة نفسِها، من `test_merge_cost_replication`
SCRIPT_MERGE_COST = 17
CHEAPEST_VOWEL_MERGE = 395
CONSONANT_MEDIAN_MERGE = 4
CONSONANT_MAX_MERGE = 336  # ف~و
ALL_THREE_VOWELS_TO_ONE = 1_677


def test_the_floor_is_nineteen_reached_by_eight_free_merges() -> None:
    """ثماني دمجاتٍ لا تُفقِد نوعًا واحدًا، فينزل الجردُ من ٢٧ إلى ١٩."""

    assert CONSONANT_GRAPHEMES - FREE_MERGES == FLOOR
    merged_letters = sum(len(one) for one in CLASSES)
    untouched = CONSONANT_GRAPHEMES - merged_letters
    assert untouched + len(CLASSES) == FLOOR
    assert merged_letters - len(CLASSES) == FREE_MERGES


def test_the_text_bounds_tightly_from_above_and_loosely_from_below() -> None:
    """من فوق ٠٫٠٩٠٪، ومن تحت ثماني حروفٍ كاملة — والفرقُ هو الخبر."""

    from_above = Fraction(SCRIPT_MERGE_COST, TYPES)
    assert rounds_to(from_above * 100, 3) == Fraction("0.090")

    from_below = Fraction(FREE_MERGES, CONSONANT_GRAPHEMES)
    assert rounds_to(from_below * 100, 2) == Fraction("29.63")
    assert from_below > from_above * 100  # الفجوةُ من تحت أوسعُ بمئات المرّات


def test_the_tolerated_classes_merge_letters_no_speaker_merges() -> None:
    """`ثح` و`جخ` و`رض`: أصنافٌ يحتملها الرسمُ ولا تحتملها أذن."""

    assert "ثح" in CLASSES  # ثوب · حوب
    assert "جخ" in CLASSES  # جبل · خبل
    assert "رض" in CLASSES
    assert all(len(one) >= 2 for one in CLASSES)
    assert sum(1 for one in CLASSES if len(one) == 3) == 2  # تزظ · ذطغ


def test_the_vowels_separate_from_the_median_not_from_the_maximum() -> None:
    """أرخصُ حركةٍ ٩٩ ضعفَ وسيطِ الصوامت، و١٫٢ ضعفَ أغلاها — والفرقُ يُقال.

    فدعوى «الحركاتُ أغلى بمراتب» تصدق على **الوسيط**؛ وعلى **الأقصى** يكاد
    التوزيعان يلتقيان (٣٩٥ مقابل ٣٣٦ لـف~و). فالفصلُ ليس قاطعًا كما يُقرَأ
    من نسبةٍ واحدة، والمقامُ يُعلَن مع النسبة.
    """

    to_median = Fraction(CHEAPEST_VOWEL_MERGE, CONSONANT_MEDIAN_MERGE)
    to_max = Fraction(CHEAPEST_VOWEL_MERGE, CONSONANT_MAX_MERGE)
    assert round(float(to_median)) == 99
    assert round(float(to_max), 1) == 1.2
    assert to_median > to_max * 50


def test_collapsing_the_three_vowels_costs_two_orders_more_than_a_consonant() -> None:
    """|ث| = ١ يكلّف ١٬٦٧٧ نوعًا = ٨٫٨٣٪ من الجرد — فالحركاتُ تحمل حقًّا."""

    share = Fraction(ALL_THREE_VOWELS_TO_ONE, TYPES)
    assert rounds_to(share * 100, 2) == Fraction("8.83")
    assert ALL_THREE_VOWELS_TO_ONE > CONSONANT_MAX_MERGE * 4
    assert ALL_THREE_VOWELS_TO_ONE > SCRIPT_MERGE_COST * 98


def test_nineteen_is_a_ceiling_on_the_floor_not_the_floor() -> None:
    """الدمجُ جشعٌ بترتيبٍ ثابت، فما يحتمله النصُّ ١٩ **فأقلّ** لا ١٩ تمامًا."""

    assert FLOOR <= CONSONANT_GRAPHEMES
    # ولا يُدَّعى أنّ ١٩ هو الأدنى: الدعوى أنّ الأدنى ≤ ١٩
    claimed_minimum_is_exact = False
    assert not claimed_minimum_is_exact
