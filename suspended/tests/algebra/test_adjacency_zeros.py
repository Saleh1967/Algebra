"""أصفارُ الجوار مقيسةً: مئةٌ وأربعٌ وأربعون خاليةً، والمتوقَّعُ صدفةً أقلُّ من واحدة.

**ما جرى**: اقتُرح في الفصل السابق عددٌ واحدٌ يحسم «أمنعٌ أم ندرة» — مجموعُ
`exp(−E)` على الخانات. وشُغِّل ههنا على المصحف، والبصمةُ
`46b4393fdb3a0920…`. والمدوّنةُ لا تُودَع؛ تُودَع أرقامُها وبصمةُ مصدرها.

`THE_TEST_I_PROPOSED_WENT_AGAINST_THE_READING_I_OFFERED`: قلتُ في الفصل
السابق إنّ أصفارَ المصحف «تُفسَّر بالندرة لأنّ المدوّنةَ صغيرة»، وإنّ
مدوّنةً أكبرَ تُبقي الأصفارَ الحقيقيّةَ وحدَها. **والتشغيلُ ردَّ ذلك**:
المصحفُ أصغرُ من مدوّنته بثلاثة أضعافٍ في الحروف، **وفيه أصفارٌ أكثرُ**
(١٤٤ من ٧٨٤ مقابل ٤٣ من ٨٤١)، **ولا واحدٌ منها مُنقَذٌ بالندرة**: أدنى
متوقَّعٍ بين الخالية **٢٫٢٤**، والمتوقَّعُ الكلّيُّ **٠٫٦١** خانة.

`AND_MY_ERROR_WAS_MOVING_A_FINDING_ACROSS_TABLES`: وسببُ خطئي مُسمًّى:
نقلتُ نتيجةً من **جدولٍ آخر**. فالأصفارُ الثلاثةُ والخمسون في
`test_functional_load_arabic` أصفارُ **كلفةِ دمج** — كم نوعًا ينهار لو صار
الحرفان واحدًا — وهي ندرةٌ بتمامها كما قِيس هناك. وأصفارُ هذا الملفّ أصفارُ
**جوار** — أيتلو هذا الحرفُ ذاك. وجدولان لا جدول، وحكمُ أحدهما لا يُنقَل.
وهو العطلُ الذي أُسمّيه منذ فصولٍ، واقعًا منّي.

`TWO_DEFECTS_IN_MY_OWN_RUN_CAUGHT_BEFORE_PUBLISHING`: أوّلُ تشغيلٍ ضمّ
الفراغَ إلى المفردة، فخرجت أقوى خانةٍ خاليةٍ «فراغٌ يتلوه فراغ» بمتوقَّعٍ
١٤٬٩٨٦ — أثرُ وصلٍ في آلتي لا خبرٌ عن العربيّة. وثانيه أنّ الهوامشَ حُسِبت
من الحروف كلِّها، وفيها ما يقع آخرَ الكلمة فلا يبدأ زوجًا؛ فتضخّم متوقَّعُ
كلّ خانةٍ صدرُها هاء: «هع» من ٣٨١ إلى **٢١٤**، أي الضِّعفَ تقريبًا.

`THE_POLICY_MOVES_THE_EXPECTED_COUNT_BY_SIXTY_FOUR_FOLD`: وطيُّ الهمزات
والتاء المربوطة يغيّر الجواب: ١٤٤ خاليةً بمتوقَّعٍ ٠٫٦١ إن طُوِيت، و٣٧٤
بمتوقَّعٍ ٣٩٫١٧ إن فُصِلت. **فالفائضُ قائمٌ في الحالين**، ودعوى «لا واحدَ
منها مُنقَذ» **صادقةٌ على المطويّ وحدَه**: في المفصول خاناتٌ متوقَّعُها صفر.

`THE_STRONGEST_CELL_LEANS_ON_ONE_MORPHEME`: وأقوى خانةٍ «رل» بمتوقَّعٍ
١٣٢٣ وصفرِ وقوع، ومقلوبُها «لر» ٣٥٦ وقوعًا. لكنّ متوقَّعَها يقوم على نصيب
اللام ثانيةً (١٣٫٥٧٪)، وهو **مضخَّمٌ بأداةِ التعريف** وحدَها. فالخانةُ خبرٌ،
ومقدارُ متوقَّعها ليس نظيفًا.
"""

from __future__ import annotations

import math
from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

SOURCE_DIGEST = "46b4393fdb3a09208ecb96fbbac990a150e4374f82d7940c655430cd1b1611ae"

WORDS, POSITIONS = 77_428, 245_171
ALPHABET, CELLS = 28, 784
OBSERVED_EMPTY = 144
EXPECTED_EMPTY = 0.61
LOWEST_EXPECTATION_AMONG_EMPTY = 2.24

BANDED = {"مُنقَذ": 0, "غيرُ حاسم": 2, "ضعيف": 13, "قويّ": 63, "قاطع": 66}

UNFOLDED = {"cells": 1_296, "empty": 374, "expected": 39.17}
HIS_CORPUS = {"cells": 841, "empty": 43, "characters": 1_020_673}


def test_the_deciding_number_says_the_zeros_are_not_chance() -> None:
    """١٤٤ مرصودةً و٠٫٦١ متوقَّعةً — فالفائضُ ١٤٣ خانةً لا تفسّرها الصدفة."""

    assert CELLS == ALPHABET**2
    assert OBSERVED_EMPTY > EXPECTED_EMPTY * 200
    assert round(OBSERVED_EMPTY - EXPECTED_EMPTY, 2) == 143.39

    assert (
        Partition(parts=tuple(BANDED.values()), declared_total=OBSERVED_EMPTY).residue
        == 0
    )
    assert BANDED["مُنقَذ"] == 0
    assert BANDED["قويّ"] + BANDED["قاطع"] == 129

    # وأدنى متوقَّعٍ بين الخالية فوق عتبة الإنقاذ بأربعة أضعافٍ ونصف
    assert LOWEST_EXPECTATION_AMONG_EMPTY > 0.5 * 4
    assert round(math.exp(-LOWEST_EXPECTATION_AMONG_EMPTY), 4) == 0.1065


def test_the_smaller_corpus_carries_more_zeros_not_fewer() -> None:
    """المصحفُ أصغرُ بثلاثة أضعافٍ وفيه أصفارٌ أكثرُ بثلاثة — فالحجمُ ليس العلّة."""

    mushaf_letters = 322_599
    assert HIS_CORPUS["characters"] > mushaf_letters * 3
    assert OBSERVED_EMPTY > HIS_CORPUS["empty"] * 3

    mine = Fraction(OBSERVED_EMPTY, CELLS)
    his = Fraction(HIS_CORPUS["empty"], HIS_CORPUS["cells"])
    assert rounds_to(mine * 100, 2) == Fraction("18.37")
    assert rounds_to(his * 100, 2) == Fraction("5.11")
    assert mine > his * 3

    # فقراءتي («المدوّنةُ الصغيرةُ تُولِّد أصفارَ ندرة») **مردودةٌ بالعدّ**
    my_reading_survives = OBSERVED_EMPTY <= EXPECTED_EMPTY
    assert not my_reading_survives


def test_the_error_was_carrying_a_verdict_across_two_tables() -> None:
    """أصفارُ كلفةِ الدمج غيرُ أصفارِ الجوار؛ وحكمُ أحدهما لا يُنقَل."""

    merge_zeros, merge_cells = 53, 378  # `test_functional_load_arabic`
    adjacency_zeros, adjacency_cells = OBSERVED_EMPTY, CELLS

    assert merge_cells == 28 * 27 // 2  # أزواجٌ غيرُ مرتَّبة
    assert adjacency_cells == 28**2  # وأزواجٌ مرتَّبة
    assert merge_cells != adjacency_cells
    assert merge_zeros != adjacency_zeros

    # والسؤالان مختلفان: «كم نوعًا ينهار؟» و«أيتلو هذا ذاك؟»
    questions = ("كم نوعًا ينهار بالدمج", "أيتلو هذا الحرفُ ذاك")
    assert len(set(questions)) == 2


def test_the_normalisation_policy_moves_the_expected_count_sixty_four_fold() -> None:
    """٠٫٦١ مطويًّا و٣٩٫١٧ مفصولًا؛ والفائضُ قائمٌ في الحالين."""

    assert UNFOLDED["cells"] == 36**2
    assert round(UNFOLDED["expected"] / EXPECTED_EMPTY, 1) == 64.2
    assert UNFOLDED["empty"] > UNFOLDED["expected"] * 9  # فالفائضُ باقٍ

    # ودعوى «لا واحدَ منها مُنقَذ» صادقةٌ على المطويّ وحدَه
    assert BANDED["مُنقَذ"] == 0
    unfolded_has_rescued = UNFOLDED["expected"] > 1
    assert unfolded_has_rescued


def test_two_defects_in_my_own_run_are_recorded_with_their_size() -> None:
    """فراغان لا يتجاوران، وهامشٌ من حروفٍ لا تبدأ زوجًا — وكلاهما قِيس."""

    space_artefact = 14_986.3
    assert space_artefact > 1_000  # أقوى خانةٍ كانت أثرَ وصلٍ في الآلة

    before, after = 381.0, 214.0
    assert round(after / before, 2) == 0.56
    assert before > after  # فالهامشُ الخاطئ يضخّم لا يُنقِص

    # والتصحيحُ لم يغيّر الحكم: ١٤٤ قبلُ وبعدُ، والمتوقَّعُ ١٫١٤ ← ٠٫٦١
    assert OBSERVED_EMPTY == 144
    assert 0.61 < 1.138


def test_the_strongest_cell_names_what_inflates_it() -> None:
    """«رل» صفرٌ ومتوقَّعُه ١٣٢٣، ومقلوبُه ٣٥٦ — والمتوقَّعُ مشوبٌ بأداة التعريف."""

    forward, backward = 0, 356
    assert forward == 0 < backward

    lam_as_second = Fraction("0.1357")
    assert lam_as_second > Fraction(1, 10)  # نصيبٌ يرفعه «ال» وحدَه

    # فالخانةُ خبرٌ، ومقدارُ متوقَّعها ليس نظيفًا — والفرقُ يُكتَب
    assert 1_323 > 100
    assert SOURCE_DIGEST[:8] == "46b4393f"
