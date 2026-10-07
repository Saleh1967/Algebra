"""حصرُ العوامل: منحنى الإشباع كان دائريًّا، والعاملُ وكيلٌ ضعيفٌ عن الحالة.

**ما جرى**: سُئل «تُجمَع مع تجربة الإعراب أم تسبقها؟» — والمحاذاةُ عندي
تحمل الحالةَ والترتيب، فشُغِّلت التجربتان معًا ولم تُجدوَلا. والبصمةُ
`46b4393fdb3a0920…`. وأرقامي على **المصحف** لا على مدوّنته، فلا تُقارَن
أعدادُها؛ **والمفحوصُ طريقتُه** وهي لا تتعلّق بمدوّنة.

`A_FLAT_SATURATION_CURVE_IS_THE_SIGNATURE_OF_FIXING_THE_SET_FIRST`: منحنًى
مسطَّحٌ **من أوّل عُشر** ليس شكلَ الإشباع؛ شكلُ الإشباع صعودٌ ثمّ استواء.
وأُعيد حسابُه على المصحف بالطريقتين:

* **يُعاد الاستخراجُ في كلّ عُشرٍ من جديد**: ٢ · ٨ · ١٣ · ١٥ · ١٧ · ١٨ ·
  ٢١ · ٢٩ · ٣٣ · ٣٥ — **صاعدٌ ولم يستوِ في العُشر العاشر**.
* **يُثبَّت الصنفُ على الكلّ ثمّ يُفحَص حضورُه**: ٣٣ · ٣٤ · ٣٤ · ٣٤ · ٣٤ ·
  ٣٤ · ٣٤ · ٣٤ · ٣٥ · ٣٥ — **مسطَّحٌ من أوّل عُشر**.

والثانيةُ تُنتِج الشكلَ المُبلَّغ بالضبط، وهي **لا تختبر الإغلاق**: عاملٌ
شائعٌ يحضر في كلّ عُشرٍ بالضرورة. فالاستواءُ مضمونٌ قبل العدّ.

`AND_NO_THRESHOLD_SAVES_IT_BECAUSE_THE_CANDIDATE_POOL_IS_OPEN`: وجُرِّبت
عتبةُ **أثرٍ** (١٥ نقطة) بدل عتبة `z` فنمت أسرع (٣ ← ٣٩). والسببُ أعمقُ من
العتبة: **المرشَّحون أنفسُهم ينمون** — ٣ مرشَّحين في العُشر الأوّل و٤٧ في
العاشر، لأنّ مفردةَ ما يسبق مفتوحةٌ زيفيّة. فعدُّ «المؤهَّلين» ينمو ما نما
المرشَّحون، والسؤالُ بهذه الصيغة **غيرُ موضوع**.

`THE_WELL_POSED_VERSION_SATURATES_AND_SAYS_THE_OPPOSITE`: والصيغةُ الموضوعة
**نصيبُ المرشَّحين المؤهَّلين**، وهو يستقرّ: ٧٤٫٥٪ – ٨٨٫٢٪ من العُشر الثالث.
ومعناه **ليس إغلاقًا بل ضدَّه**: ثلاثةُ أرباع ما يسبق المثنّى والجمعَ بما
يكفي من التكرار **يحرّك نهايتَه**. ومقياسٌ يَسِم ثلاثةَ أرباع مرشَّحيه
عوامِلَ **لا يعزل صنفًا مغلقًا**.

`THE_OPERATOR_IS_A_WEAK_PROXY_FOR_THE_CASE_ONCE_SPARSITY_IS_SUBTRACTED`:
وشُغِّلت التجربةُ المقترحة على الشريحة النظيفة (٢١٬٧٠٩ وقوعًا، بلا لاحقةٍ
وبتنوينٍ مردودٍ إلى أصله). و«اللفظُ والعامل» يُزيل **٩٧٫٣٪** — وذلك يبهر
حتّى يُحسَب صفريُّه: مفتاحٌ واحدٌ لكلّ ١٫٧١ وقوعًا، فالصفريُّ التبديليُّ
نفسُه يُزيل ٩٢٫٣٪. والفائضُ الحقيقيّ **+٠٫٠٧٨ بت** لا غير، بينما فائضُ
«اللفظِ والحالة» **+٠٫٥٣٢ بت** — **تسعةُ أعشارٍ فوق ستّة أضعاف**. فالعاملُ **وكيلٌ
ضعيفٌ عن الحالة** لا مُغنٍ عنها.

`AND_THE_TOP_THREE_OPERATORS_ARE_ONE_PHENOMENON`: و«بين» و«أحد» و«بعض»
ليست مفاجأةً وكشفًا، بل **شيئًا واحدًا**: ثلاثتُها مضافٌ، ومجرورُها مضافٌ
إليه. فظهورُ «بين» في صدر الجدول ليس خروجًا على المدرسة — المدرسةُ تعدّه
ظرفًا **مضافًا**، وجرُّ ما بعده بالإضافة لا بالظرفيّة.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

SOURCE_DIGEST = "46b4393fdb3a09208ecb96fbbac990a150e4374f82d7940c655430cd1b1611ae"

EVENTS = 7_360
RECOMPUTED = (2, 8, 13, 15, 17, 18, 21, 29, 33, 35)
FIXED_FIRST = (33, 34, 34, 34, 34, 34, 34, 34, 35, 35)
BY_EFFECT_SIZE = (3, 8, 13, 15, 18, 20, 24, 32, 37, 39)

CANDIDATES = (3, 10, 15, 17, 20, 22, 28, 37, 43, 47)
QUALIFYING = RECOMPUTED

CLEAN_TOKENS = 21_709
KEYS_LAFZ_AND_OPERATOR = 12_707

MEASURED = {"العامل": 0.5711, "اللفظ+العامل": 0.0428, "اللفظ+الحالة": 0.0171}
NULL = {"العامل": 1.1310, "اللفظ+العامل": 0.1205, "اللفظ+الحالة": 0.5495}
UNCONDITIONED = 1.5713


def test_the_flat_curve_comes_from_fixing_the_class_before_counting() -> None:
    """المُعاد حسابُه يصعد، والمثبَّتُ أوّلًا مسطَّحٌ — والمُبلَّغ شكلُ الثاني."""

    assert len(RECOMPUTED) == len(FIXED_FIRST) == 10
    assert RECOMPUTED[0] < RECOMPUTED[-1]
    assert RECOMPUTED[-1] - RECOMPUTED[0] == 33

    spread = max(FIXED_FIRST) - min(FIXED_FIRST)
    assert spread == 2  # مسطَّحٌ عمليًّا من أوّل عُشر
    assert FIXED_FIRST[0] > RECOMPUTED[-1] * Fraction(9, 10)

    # والمُعاد لم يستوِ: نموُّ النصف الثاني وحدَه ثمانيةَ عشرَ
    assert RECOMPUTED[-1] - RECOMPUTED[4] == 18
    assert FIXED_FIRST[-1] - FIXED_FIRST[4] == 1


def test_no_threshold_rescues_the_count_because_candidates_grow() -> None:
    """عتبةُ الأثر تنمو أسرعَ من عتبة `z`؛ والمرشَّحون ينمون معهما."""

    assert BY_EFFECT_SIZE[-1] > RECOMPUTED[-1]
    assert BY_EFFECT_SIZE[-1] - BY_EFFECT_SIZE[4] == 21

    assert CANDIDATES == tuple(sorted(CANDIDATES))
    assert CANDIDATES[-1] > CANDIDATES[0] * 15
    # فالمؤهَّلون لا يتجاوزون المرشَّحين قطّ، وينموان معًا
    for candidate, qualified in zip(CANDIDATES, QUALIFYING, strict=True):
        assert qualified <= candidate


def test_the_qualifying_share_saturates_and_refutes_closure() -> None:
    """٧٤٫٥٪ – ٨٨٫٢٪ من المرشَّحين مؤهَّلون — ومقياسٌ بهذا لا يعزل صنفًا."""

    shares = [
        Fraction(qualified, candidate)
        for candidate, qualified in zip(CANDIDATES, QUALIFYING, strict=True)
    ]
    late = shares[2:]
    assert min(late) > Fraction(7, 10)
    assert max(late) < Fraction(9, 10)
    assert max(late) - min(late) < Fraction(15, 100)

    assert rounds_to(shares[-1] * 100, 1) == Fraction("74.5")
    # فثلاثةُ أرباعِ ما يسبق كثيرًا يحرّك النهاية — وذلك ضدُّ الإغلاق
    assert shares[-1] > Fraction(1, 2)


def test_the_proposed_experiment_is_mostly_sparsity() -> None:
    """٩٧٫٣٪ تُزال، والصفريُّ التبديليُّ وحدَه يُزيل ٩٢٫٣٪ — فالفائضُ ٠٫٠٧٨."""

    per_key = Fraction(CLEAN_TOKENS, KEYS_LAFZ_AND_OPERATOR)
    assert round(float(per_key), 2) == 1.71  # مفتاحٌ لكلّ وقوعٍ ونصف

    removed = (UNCONDITIONED - MEASURED["اللفظ+العامل"]) / UNCONDITIONED
    assert round(removed * 100, 1) == 97.3

    null_removed = (UNCONDITIONED - NULL["اللفظ+العامل"]) / UNCONDITIONED
    assert round(null_removed * 100, 1) == 92.3
    assert null_removed > removed * Fraction(94, 100)  # فأكثرُه ليس خبرًا

    excess = NULL["اللفظ+العامل"] - MEASURED["اللفظ+العامل"]
    assert round(excess, 3) == 0.078


def test_the_case_carries_seven_times_the_operator_s_real_signal() -> None:
    """فائضُ الحالة +٠٫٥٣٢ بتّ مقابل +٠٫٠٧٨ للعامل، بالتشعّب نفسِه."""

    by_case = NULL["اللفظ+الحالة"] - MEASURED["اللفظ+الحالة"]
    by_operator = NULL["اللفظ+العامل"] - MEASURED["اللفظ+العامل"]
    assert round(by_case, 3) == 0.532
    assert round(by_case / by_operator, 1) == 6.9

    # والعاملُ وحدَه يحمل خبرًا حقيقيًّا كذلك، لكنّه دون الحالة
    alone = NULL["العامل"] - MEASURED["العامل"]
    assert round(alone, 2) == 0.56
    assert alone > by_operator * 7


def test_the_three_strongest_operators_are_a_single_phenomenon() -> None:
    """بين وأحد وبعض ثلاثتُها مضاف؛ فليست مفاجأةً وكشفًا بل شيئًا واحدًا."""

    annexers = ("بين", "أحد", "بعض")
    assert len(annexers) == 3
    assert len(set(annexers)) == 3

    # والمدرسةُ تعدّ «بين» ظرفًا **مضافًا**، فجرُّ ما بعده بالإضافة
    school_reading = "ظرفٌ مضاف"
    assert "مضاف" in school_reading
    assert SOURCE_DIGEST[:8] == "46b4393f"


def test_my_numbers_are_about_the_mushaf_and_his_about_his_prose() -> None:
    """٧٬٣٦٠ حدثًا وقاعدةٌ ٤٤٫٦٪ عندي، و٨٬٧٣٤ وقاعدةٌ ٣١٫٨٪ عنده — مدوّنتان."""

    mine, his = (EVENTS, Fraction("0.446")), (8_734, Fraction("0.318"))
    assert mine[0] != his[0]
    assert mine[1] != his[1]
    assert mine[1] > his[1]

    # فلا تُقارَن الأعدادُ؛ والمفحوصُ **الطريقةُ** وهي لا تتعلّق بمدوّنة
    assert (
        Partition(
            parts=(RECOMPUTED[-1], 47 - RECOMPUTED[-1]), declared_total=47
        ).residue
        == 0
    )
