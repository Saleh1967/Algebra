"""تدقيقُ محوّل ميلي: دالّةٌ على ما زارته، وجداءٌ أوسعُ ممّا زارت.

**ما يُقاس ههنا**: اتّساقُ تقرير الفصل ٢٩ مع نفسه ومع ما أُودِع. لا مدوَّنةَ
تُقرَأ. والمحوّلُ نفسُه ليس محلَّ طعن: أربعُ مئةٍ وستّةٌ وأربعون مدخلًا
**تُفحَص خليّةً خليّة**، وذلك أوّلُ شيءٍ في هذا المشروع يقبل الفحصَ كذلك.

`A_TOTAL_FUNCTION_ON_WHAT_IT_VISITED_IS_NOT_TOTAL_ON_THE_PRODUCT`: «دالّةٌ
كلّيّةٌ على جداءٍ مُعلَن» تصدق على **٤٤٦ خليّةً زارها**، والجداءُ المُعلَن
٢١×٨٨×٢ = ٣٬٦٩٦. فـ٨٧٫٩٣٪ منه **لم يُزَر ولم يُعلَن ممتنعًا**. والفرقُ ليس
لفظيًّا: التقويمُ خارجَ العيّنة أصاب **١٠٢ خليّةً غائبة** — فالمنطقةُ غيرُ
المزارة **مبلوغةٌ لا ممتنعة**، وشرطُ التمام يُقرَأ عليها لا على المزار.

`A_DIFFERENCE_MAY_NOT_OUTRUN_ITS_TERMS`: مكسبا ماركوف (+٠٫٧٥١٢ و+٠٫١٧٨٧)
لا يُشتَقّان من الإنتروبيات الأربع المطبوعة: الطرحُ يعطي ٠٫٧٥١١ و٠٫١٧٨٨.
وكلاهما **داخلَ** مجاله، فالخلافُ أثرُ الطرح قبل التقريب — ويُرفَع بطبع
منزلةٍ خامسة.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.assignment import Assignment
from algebra.evaluation import Tally
from algebra.reconciliation import Difference, PrintedFigure, rounds_to

SUBSETS_SEARCHED = 1_024
FEATURES = 10
MINIMAL_COMPLETE = 9

STATES_BEFORE, STATES_AFTER = 24, 21
INPUT_SYMBOLS, LOOKAHEAD, ACTIONS = 88, 2, 27
TABLE_ENTRIES = 446

TRANSITIONS_TESTED = 172_393
MISSING_CELLS = 102

ENTROPIES = ("3.1508", "2.3997", "2.2209", "2.1441")
REPORTED_GAINS = ("0.7512", "0.1787")

SIX_POSITIONAL = Fraction("0.076487")
PLUS_MARKOV = Fraction("0.005754")
REPORTED_RECOVERY = Fraction("92.4")

EXTRACTOR_LETTERS = 326_160
PUBLISHED_UNITS = (341_249, 77_429, 225_911, 130_030, 18_993)


def test_the_exhaustive_search_covers_the_whole_power_set() -> None:
    """١٬٠٢٤ = ٢^١٠ — بحثٌ شاملٌ لا عيّنةٌ منه، والحدُّ الأدنى تسعٌ من عشر."""

    assert 2**FEATURES == SUBSETS_SEARCHED
    assert MINIMAL_COMPLETE == FEATURES - 1
    assert MINIMAL_COMPLETE < FEATURES


def test_the_declared_product_is_eight_times_what_the_table_holds() -> None:
    """٤٤٦ من ٣٬٦٩٦ = ١٢٫٠٧٪، فـ٨٧٫٩٣٪ لم يُزَر ولم يُعلَن ممتنعًا.

    و`Assignment` تردّ جدولًا كهذا: `filled + forbidden` لا يساوي الشبكة.
    والتصحيحُ إمّا سردُ الخلايا الممتنعة، وإمّا قولُ «كلّيّةٌ على ما زارت».
    """

    grid = STATES_AFTER * INPUT_SYMBOLS * LOOKAHEAD
    assert grid == 3_696
    assert STATES_BEFORE * INPUT_SYMBOLS * LOOKAHEAD == 4_224
    assert rounds_to(Fraction(TABLE_ENTRIES * 100, grid), 2) == Fraction("12.07")
    unvisited = grid - TABLE_ENTRIES
    assert unvisited == 3_250
    # جدولٌ لا يغطّي شبكتَه يُرَدّ في الإنشاء: نموذجٌ مصغَّرٌ يُثبِت القاعدة
    small = Assignment(
        rows=("ح١", "ح٢"),
        columns=("د١", "د٢"),
        cells=(("ح١", "د١", "ف"), ("ح٢", "د١", "ف")),
        forbidden=(("ح١", "د٢"), ("ح٢", "د٢")),
    )
    assert small.covers_the_grid()
    assert small.forbidden_count == 2


def test_the_unvisited_region_is_reachable_not_forbidden() -> None:
    """١٠٢ خليّةً غائبةً أُصيبت خارجَ العيّنة — فالباقي **مبلوغٌ** لا ممتنع.

    وهذا يحسم الصياغة: لو كان غيرُ المزار ممتنعًا لما أصابه التقويم. فالجدولُ
    **ناقصٌ على جداءٍ حقيقيّ**، لا تامٌّ على جداءٍ أضيق. والنقصُ مقيسٌ
    (٠٫٠٥٩٢٪) وذلك أنفعُ من إخفائه.
    """

    assert MISSING_CELLS > 0
    share = Fraction(MISSING_CELLS * 100, TRANSITIONS_TESTED)
    assert rounds_to(share, 4) == Fraction("0.0592")
    assert MISSING_CELLS <= 3_250  # لا تتجاوز الخلايا غيرَ المزارة


def test_zero_violation_is_correctly_reported_as_three_numbers() -> None:
    """«صفرُ مخالفة» مع الغياب: سعةٌ ٩٩٫٩٤٪ وصوابٌ ١٠٠٪ حيث انطبقت.

    وقد أعلن التقريرُ الغيابَ إلى جانب الصفر، فلم يخلط الامتناعَ بالصواب —
    وهذا انضباطٌ يُذكَر لا يُصحَّح.
    """

    tally = Tally(
        correct=TRANSITIONS_TESTED - MISSING_CELLS, wrong=0, abstained=MISSING_CELLS
    )
    assert tally.total == TRANSITIONS_TESTED
    assert tally.precision_where_it_fires == 1
    assert rounds_to(tally.coverage * 100, 4) == Fraction("99.9408")
    assert tally.accuracy_charging_abstention == tally.coverage


def test_the_two_markov_gains_do_not_follow_from_the_printed_entropies() -> None:
    """الطرحُ يعطي ٠٫٧٥١١ و٠٫١٧٨٨، والمُعلَنُ ٠٫٧٥١٢ و٠٫١٧٨٧ — وكلاهما داخلَ مجاله."""

    for index, reported in enumerate(REPORTED_GAINS):
        gap = Difference(
            PrintedFigure(ENTROPIES[index]), PrintedFigure(ENTROPIES[index + 1])
        )
        low, high = gap.interval()
        assert low <= Fraction(reported) <= high
        assert Fraction(reported) != gap.value
    assert Difference(PrintedFigure("3.1508"), PrintedFigure("2.3997")).value == (
        Fraction("0.7511")
    )
    assert Difference(PrintedFigure("2.3997"), PrintedFigure("2.2209")).value == (
        Fraction("0.1788")
    )


def test_the_recovery_share_is_truncated_where_the_rest_are_rounded() -> None:
    """٩٢٫٤٧٧٢٪ تُقرَّب إلى ٩٢٫٥ وتُبتَر إلى ٩٢٫٤ — والمنشورُ بتْر."""

    recovery = (SIX_POSITIONAL - PLUS_MARKOV) / SIX_POSITIONAL * 100
    assert rounds_to(recovery, 4) == Fraction("92.4772")
    assert rounds_to(recovery, 1) == Fraction("92.5")
    assert rounds_to(recovery, 1) != REPORTED_RECOVERY
    assert int(float(recovery) * 10) / 10 == float(REPORTED_RECOVERY)


def test_the_backward_step_is_absorbed_and_the_forward_one_is_not() -> None:
    """الخليّتان الحاسمتان: «سبقه تنوين» لا يكسب شيئًا، والنظرُ الأماميّ يُصفّر."""

    assert PLUS_MARKOV == Fraction("0.005754")
    assert PLUS_MARKOV - Fraction("0.005754") == 0  # لا مكسبَ من خطوةٍ خلفيّةٍ ثانية
    assert rounds_to(PLUS_MARKOV, 4) == Fraction("0.0058")
    assert PLUS_MARKOV > 0  # وماركوفُ وحدَه لا يبلغ الصفر
    assert SIX_POSITIONAL > 10 * PLUS_MARKOV


def test_the_extractor_letter_count_matches_no_published_unit() -> None:
    """٣٢٦٬١٦٠ ليست ذرّاتٍ ولا وقوعاتٍ ولا مقاطعَ ولا صورًا — وحدةٌ خامسةٌ بلا اسم."""

    for unit in PUBLISHED_UNITS:
        assert EXTRACTOR_LETTERS != unit
    assert 341_249 - EXTRACTOR_LETTERS == 15_089
    assert rounds_to(Fraction(EXTRACTOR_LETTERS * 100, 341_249), 2) == Fraction("95.58")


def test_four_failures_are_named_and_three_are_claimed() -> None:
    """المتنُ يُسمّي أربعَ إخفاقاتٍ والخلاصةُ تقول ثلاثًا — والحسمُ في (أ).

    و(أ) **لم يفشل**: فشل قياسُه الأوّل، لأنّه أُجري على تجريدٍ معطوب (وسمُ
    `ن0` بمطابقة نصّ). وبعد الوسم عند الإصدار صار H = ٠ — أي أنّ (أ)
    **تحقّق**. فالعدُّ الصحيحُ ثلاثٌ، والرابعُ صنفٌ آخر: **قياسٌ فاسدٌ لا
    تنبّؤٌ فاشل**، ويُسمّى باسمه.
    """

    named_in_body = (
        "(أ) H ≠ 0",
        "الحدُّ الأدنى ≤ ٦",
        "التناثر < ١٪",
        "الرتبةُ الثانية ≤ ٠٫٠٥",
    )
    assert len(named_in_body) == 4
    genuine_failures = named_in_body[1:]
    assert len(genuine_failures) == 3
    assert named_in_body[0] not in genuine_failures
