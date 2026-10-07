"""العمودُ الثالث: انقسامُه خبرٌ جديد، وحصّتُه ليست خبرًا — ومقاماتُ تدرّجه غائبة.

**ما يُقاس ههنا**: أرقامُ التقرير تُعاد، ويُشتَقّ منها ما يلزم. ولا مدوّنةَ
تُقرَأ ولا شجرةَ تُفتَح.

`THE_THIRD_SHARE_IS_DERIVED_AND_THE_SPLIT_IS_NOT`: الأعمدةُ الثلاثةُ تجمع إلى
مئة، فدرجاتُ حرّيّتها **اثنتان لا ثلاث**. وحصّةُ الإسناديّة ١٠٠ ناقصَ
الأخرَيين، ونشرُها شاهدًا ثالثًا عدٌّ للشيء مرّتين. **وانقسامُها الداخليُّ
درجةٌ ثالثةٌ حقًّا**: جدولٌ آخرُ بمقامٍ آخرَ لا يُشتَقّ من الحصص. فالتمييزُ
بينهما صوابٌ، وهو الذي يجعل الفصلَ خبرًا.

`TWO_NULLS_AGREE_ON_THE_SPLIT_WITHIN_TWO_AND_A_TENTH_PERCENT`: والانقسامُ
٢٦٫٤٤٪ مقابل ٨٨٫٥٦٪ — فارقُ **٦٢٫١** نقطة. و`z` على صفريٍّ تبديليٍّ حافظٍ
للهوامش **+٢١٫٧**، وعلى نسبتين مجمّعتين **+٢١٫٢٦**؛ والفرقُ بينهما **٢٫٠٣٪**.
فمقياسان مختلفان يتّفقان في حدود جزءٍ من خمسين، وذلك تصديقٌ لا تعارض. (وكتبتُ
أوّلًا «في حدود اثنين بالمئة»، فردَّه الحسابُ بثلاثة أجزاءٍ من مئة الجزء.)

`BOTH_PUBLISHED_P_VALUES_ARE_FLOORS_AND_ONE_IS_NAMED_AS_SUCH`: و٠٫٠٠٠٥ =
١/٢٠٠١ سُمّيت أرضَ تصميمها بحقّ. و٠٫٠٣٢٨ = **٢/٦١** وهي أرضُ الستّين ذاتَ
طرفين، وسُمّيت «تجريبيّة». والاثنتان أرضان: لا تُخرِج التجربةُ أصغرَ منهما
مهما بلغ الفارق. فيُقالان أرضَين معًا، وإلّا قُرِئت إحداهما قياسًا.

`ONLY_THE_UNPREDICTED_POINT_IS_PROVABLY_ATTESTED`: والتدرّجُ أربعُ نسبٍ بلا
مقامات. ويقيّدها المجموعُ المنشورُ (٣٠٢ من ٣٤١ = ٨٨٫٥٦٪) بمعادلةٍ واحدة:

    ٠٫٠٩٢ · نصيبُ اسم الفاعل  +  ٠٫٣٧١ · نصيبُ المصدر  =  ٠٫١١٤٤

فيلزم منها أنّ **نصيبَ المصدر بين ٨٫٠٪ و٣٠٫٨٪** — أي بين ٢٧ و١٠٥ وقوعًا،
**ولا يمكن أن يكون صفرًا**. وأمّا اسمُ المفعول واسمُ الفاعل فحدُّهما الأدنى
**صفر**: لا يمنع المجموعُ أن يقوم «١٠٠٫٠٪» على وقوعاتٍ تُعَدّ بالأصابع.

فالنقطةُ الوحيدةُ التي **يضمن الحسابُ شهودَها** هي **المصدر** — وهي بعينها
النقطةُ التي لم يتنبّأ بها. وذلك لا يُثبِت التدرّجَ ولا ينقضه؛ يقول إنّ
طرفَيه غيرُ مضمونَي الشهادة حتّى تُنشَر مقاماتُهما.
"""

from __future__ import annotations

import math
from fractions import Fraction

from algebra.evaluation import ClusteredSample
from algebra.reconciliation import Partition, rounds_to
from algebra.results import Placement, Vacancy

SHARES: dict[str, tuple[float, float, float]] = {
    # (إضافيّة، تقييديّة، إسناديّة)
    "جنس": (44.9, 27.7, 27.4),
    "مشتقّ": (16.6, 45.2, 38.2),
}

GENUS_SUBJECT, GENUS_PREDICATE = 1_074, 386
DERIVED_SUBJECT, DERIVED_PREDICATE = 39, 302

GRADIENT = {
    "اسمُ مفعول": Fraction("1.000"),
    "اسمُ فاعل": Fraction("0.908"),
    "مصدر": Fraction("0.629"),
    "جنس": Fraction("0.264"),
}

SIXTY, TWO_THOUSAND = 60, 2_000


def test_the_three_columns_are_a_composition_with_two_degrees_of_freedom() -> None:
    """تجمع إلى مئة، فالثالثةُ مُشتَقّةٌ ونشرُها شاهدًا عدٌّ للشيء مرّتين."""

    for who, parts in SHARES.items():
        tenths = tuple(round(one * 10) for one in parts)
        assert Partition(parts=tenths, declared_total=1_000).residue == 0, who
        assert round(sum(parts), 1) == 100.0

    independent = len(next(iter(SHARES.values()))) - 1
    assert independent == 2


def test_the_internal_split_is_a_new_table_not_a_restatement() -> None:
    """٢٦٫٤٤٪ مقابل ٨٨٫٥٦٪ بمقامين آخرَين، لا يُشتقّان من الحصص."""

    genus_total = GENUS_SUBJECT + GENUS_PREDICATE
    derived_total = DERIVED_SUBJECT + DERIVED_PREDICATE
    assert (genus_total, derived_total) == (1_460, 341)

    genus_rate = Fraction(GENUS_PREDICATE, genus_total)
    derived_rate = Fraction(DERIVED_PREDICATE, derived_total)
    assert rounds_to(genus_rate * 100, 2) == Fraction("26.44")
    assert rounds_to(derived_rate * 100, 2) == Fraction("88.56")
    assert rounds_to((derived_rate - genus_rate) * 100, 1) == Fraction("62.1")

    # والمقامان لا يُستخرَجان من حصص الأعمدة، فهما معلومةٌ زائدة
    assert genus_total != SHARES["جنس"][2]
    assert derived_total != SHARES["مشتقّ"][2]


def test_two_different_nulls_agree_on_the_split() -> None:
    """+٢١٫٧ تبديليًّا و+٢١٫٢٦ بنسبتين مجمّعتين — تصديقٌ لا تعارض."""

    genus_total = GENUS_SUBJECT + GENUS_PREDICATE
    derived_total = DERIVED_SUBJECT + DERIVED_PREDICATE
    first = GENUS_PREDICATE / genus_total
    second = DERIVED_PREDICATE / derived_total

    pooled = (GENUS_PREDICATE + DERIVED_PREDICATE) / (genus_total + derived_total)
    spread = math.sqrt(pooled * (1 - pooled) * (1 / genus_total + 1 / derived_total))
    pooled_z = (second - first) / spread
    assert round(pooled_z, 2) == 21.26

    permutation_z = 21.7
    apart = abs(permutation_z - pooled_z) / permutation_z
    assert round(apart * 100, 2) == 2.03
    assert apart < Fraction(3, 100)


def test_both_published_p_values_are_design_floors() -> None:
    """٠٫٠٠٠٥ = ١/٢٠٠١، و٠٫٠٣٢٨ = ٢/٦١ — والثانيةُ سُمّيت «تجريبيّة»."""

    assert Fraction(1, TWO_THOUSAND + 1) == Fraction(1, 2_001)
    assert round(float(Fraction(1, 2_001)), 4) == 0.0005

    two_sided_floor = Fraction(2, SIXTY + 1)
    assert two_sided_floor == Fraction(2, 61)
    assert round(float(two_sided_floor), 4) == 0.0328

    # فالاثنتان أرضان، ولا تُخرِج التجربةُ أصغرَ منهما مهما بلغ الفارق
    assert Fraction(1, 2_001) < two_sided_floor


def test_the_aggregate_binds_the_infinitive_and_leaves_the_ends_free() -> None:
    """نصيبُ المصدر بين ٨٫٠٪ و٣٠٫٨٪ ولا يكون صفرًا؛ وطرفا التدرّج حدُّهما صفر."""

    aggregate = Fraction(DERIVED_PREDICATE, DERIVED_SUBJECT + DERIVED_PREDICATE)
    agent_weight = 1 - GRADIENT["اسمُ فاعل"]
    infinitive_weight = 1 - GRADIENT["مصدر"]
    residue = 1 - aggregate

    # القيدُ الوحيدُ الذي يفرضه المجموع على الأنصبة الثلاثة
    assert rounds_to(agent_weight, 3) == Fraction("0.092")
    assert rounds_to(infinitive_weight, 3) == Fraction("0.371")
    assert rounds_to(residue, 4) == Fraction("0.1144")

    def infinitive_at(agent: Fraction) -> Fraction:
        return (residue - agent_weight * agent) / infinitive_weight

    # طرفا المنطقة المُجدية يُحَلّان بالضبط لا بمسحِ شبكة
    at_no_agent = infinitive_at(Fraction(0))  # نصيبُ اسم الفاعل صفرًا
    no_patient_agent = (infinitive_weight - residue) / (
        infinitive_weight - agent_weight
    )
    at_no_patient = infinitive_at(no_patient_agent)

    assert rounds_to(at_no_agent * 100, 1) == Fraction("30.8")
    assert rounds_to(at_no_patient * 100, 1) == Fraction("8.0")
    assert at_no_patient > 0  # فالمصدرُ مشهودٌ بالضرورة
    assert 1 - Fraction(0) - at_no_agent > 0  # والحلّان مُجديان كلاهما
    assert 0 <= no_patient_agent <= 1

    total = DERIVED_SUBJECT + DERIVED_PREDICATE
    assert round(float(at_no_patient) * total) == 27
    assert round(float(at_no_agent) * total) == 105

    # وأمّا الطرفان فحدُّهما الأدنى **صفرٌ بالضبط**، وكلٌّ يُبلَغ بحلٍّ مُجدٍ
    assert 1 - no_patient_agent - at_no_patient == 0  # اسمُ المفعول صفرًا
    assert rounds_to(no_patient_agent * 100, 2) == Fraction("91.98")


def test_the_gradient_is_monotone_and_its_ends_are_unattested() -> None:
    """أربعُ نسبٍ متنازلة، ومقاماتُ ثلاثٍ منها غيرُ منشورة."""

    values = list(GRADIENT.values())
    assert values == sorted(values, reverse=True)
    assert GRADIENT["اسمُ مفعول"] == 1
    assert GRADIENT["مصدر"] < GRADIENT["اسمُ فاعل"]
    assert GRADIENT["جنس"] < GRADIENT["مصدر"]

    # والمصدرُ بين الوصف والجنس فعلًا، والمسافتان غيرُ متساويتين
    to_the_description = GRADIENT["اسمُ فاعل"] - GRADIENT["مصدر"]
    to_the_genus = GRADIENT["مصدر"] - GRADIENT["جنس"]
    assert rounds_to(to_the_description, 3) == Fraction("0.279")
    assert rounds_to(to_the_genus, 3) == Fraction("0.365")
    assert to_the_genus > to_the_description  # فهو إلى الوصف أقربُ منه إلى الجنس

    # ومقامُ الجنس وحدَه منشورٌ في هذا التدرّج
    published = ClusteredSample(observations=1_460, clusters=1_460)
    assert published.effective == 1_460


def test_the_annexation_column_is_not_yet_split_and_the_cell_says_so() -> None:
    """الإضافيّةُ لم تُقسَم داخليًّا: مضافٌ ومضافٌ إليه، وخانتُها مفتوحةٌ بفحص."""

    cell = Placement(
        coordinate=("الإضافيّة", "الانقسامُ الداخليّ"),
        open_test=(
            "يُعَدّ لكلّ قسمٍ نصيبُه من طرفَي الإضافة — مضافًا ومضافًا إليه — "
            "بمقامٍ منشورٍ لكلّ خانة، ثمّ يُقارَن بصفريٍّ حافظٍ للهوامش"
        ),
    )
    assert cell.vacancy is Vacancy.UNRUN
    assert cell.finding is None

    # وثلاثُ نِسَبٍ مُسمّاة، انقسمت منها واحدةٌ داخليًّا لا غير
    named = ("إسناديّة", "تقييديّة", "إضافيّة")
    split_so_far = ("إسناديّة",)
    assert len(named) == 3
    assert len(split_so_far) == 1
    assert set(split_so_far) < set(named)
