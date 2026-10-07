"""الوضعُ والنِّسَب: انفصالٌ مزدوجٌ يصمد، وتنبّؤٌ سقفُه أرضُ تصميمه.

**ما يُقاس ههنا**: أرقامُ التقرير تُعاد، ويُحسَب ما يلزم منها وما يَحُدُّها.
ولا مدوّنةَ تُقرَأ ولا شجرةَ تُفتَح.

`THE_UNMEASURABLE_HALF_IS_DECLARED_BEFORE_THE_NUMBER`: دعوى الكتاب أنّ
الموضوعَ له «المعاني الذهنيّة دون الخارجيّة» **غيرُ قابلةٍ للتكذيب على هذه
الركيزة**: المدوّنةُ تُسجّل الألفاظَ لا الأذهان. وأُعلِن ذلك **قبل** الرقم،
كما أُعلِن شرطُ الحروف في فصل التعريب. وهذا ثاني موضعٍ يُعلَن فيه شرطٌ عقيمًا
قبل قياسه، والإعلانُ المتقدّمُ هو ما يجعله حدًّا لا عذرًا.

`A_DOUBLE_DISSOCIATION_IS_NOT_A_DIFFERENCE`: والمقيسُ **انفصالٌ مزدوج**:
الجنسُ أعلى في الإضافيّة (٢٫٧٠×)، والمشتقُّ أعلى في التقييديّة (١٫٦٣×).
واتّجاهان متعاكسان لا يُفسَّران بأنّ أحدَ الصنفين أكثرُ نِسَبًا من الآخر —
وذلك ما يفصل الانفصالَ المزدوجَ عن فرقٍ في المقدار. وبإخراج `obj` يشتدّان
معًا (٣٫١٠× و٥٫١٣×) ولا ينقلب أحدُهما.

`THE_STRONGER_NUMBER_IS_THE_WEAKER_EVIDENCE`: ونصفا الانفصال ليسا سواءً في
الدلالة. «المشتقُّ في التقييديّة» **قريبٌ من التحليليّة**: التقييديّةُ
مُعرَّفةٌ بحوافَّ كالنعت، واسمُ الفاعل نعتٌ بالصورة. وقد أُخرِجت اللِّمَمُ
الموسومةُ `ADJ` لكسر دائريّةٍ مُعلَنة، وتبقى الأخرى. وأمّا «الجنسُ في
الإضافيّة» فليس فيه تحليليّةٌ ألبتّة: لا شيءَ في كون اللفظةِ جنسًا يستلزم
أن تُضاف إليها. **فالنصفُ الأضعفُ عددًا (٣٫١٠×) هو الأقوى شهادةً.**

`A_DESIGN_OF_SIXTY_REPLICATES_CANNOT_SPEAK_BELOW_ONE_IN_SIXTY_ONE`: وأدنى
`p` يبلغها تصميمٌ بستّين تكرارًا **١/٦١ = ٠٫٠١٦٤**. فقولُ «لم تبلغ عيّنةٌ
واحدةٌ من ستّين» لا يحمل أكثرَ من ذلك مهما عظُم الفارق. والفارقُ ٢٫٤٧ انحرافًا
يعطي تحت السويّة `p ≈ ٠٫٠٠٦٨` — **وهي دون أرضِ التصميم**، فلا تُنشَر منه.
ويُتوقَّع ٠٫٤١ تجاوزًا في الستّين، فصفرُ تجاوزاتٍ **هو الحالُ الأغلب** لا
حدثٌ نادر. فالوقفُ عند «ضعيف» صوابٌ، وهذا عددُه.

`A_CONTROL_CHOSEN_AFTER_THE_NUMBER_DOES_NOT_SEAL_A_PREDICTION`: والتنبّؤ
انقلب حكمُه بالضبط: خامًّا **كاذب** (١٠٫٢٩٪ للجنس مقابل ٦٫٣٨٪)، ومضبوطًا
**صادق** (٣٫٧٤٪ مقابل ٦٫٣٨٪). وإعلانُ الوجهين معًا هو الصواب؛ ولا يُرفَع
الحكمُ فوق «ضعيفٌ في الجهة المتنبَّأ بها» لأنّ الضبطَ **اختير بعد رؤية
الرقم**. ولو كان التصغيرُ مكتوبًا في التسجيل لكان الحكمُ حكمَ تنبّؤٍ مختوم.

`THE_NUMBER_SURVIVES_THE_READING_THAT_FELL`: وتأويلُ الفصل الستّين سقط
وقياسُه قائم: `+٠٫٢٥٨٩` بتّ لم يتحرّك. والساقطُ «الجنسُ اعتباطيٌّ والمشتقُّ
محسوب» — وهو خطأٌ على نصّ الكتاب، إذ اللغاتُ عنده كلُّها اصطلاحيّة. والقائمُ
تفسيرٌ **أقوى** لأنّه يتنبّأ بالاتّجاه لا يصفه: مضمونٌ ذهنيٌّ مركّبٌ (ذاتٌ
وصفةٌ ونسبة) صداه تركُّبٌ في الصورة الصوتيّة، ومضمونٌ بسيطٌ لا صدى له.
"""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from algebra.attainability import (
    AttainabilityError,
    permutation_floor,
)
from algebra.results import Placement, ResultsError, Vacancy

# (إضافيّة، تقييديّة) بالمئة، كما نُشِرت
FULL: dict[str, tuple[float, float]] = {"جنس": (44.9, 27.7), "مشتقّ": (16.6, 45.2)}
WITHOUT_OBJ: dict[str, tuple[float, float]] = {"جنس": (57.4, 7.6), "مشتقّ": (18.5, 39.0)}

RAW = {"جنس": 10.29, "مشتقّ": 6.38}
CONTROLLED = {"جنس_متوسّط": 3.74, "جنس_انحراف": 1.07, "مشتقّ": 6.38}
TRAINING_ROWS = {"جنس": 3_104, "مشتقّ": 436}
REPLICATES = 60
CHAPTER_SIXTY_BITS = Fraction("0.2589")


def test_the_mental_content_claim_is_declared_unfalsifiable_here() -> None:
    """«المعاني الذهنيّة دون الخارجيّة» لا وقوعَ يُسقِطها على ركيزةِ ألفاظ."""

    barren = Placement(
        coordinate=("الوضع", "المعاني الذهنيّة دون الخارجيّة"),
        forbidden_because=(
            "المدوّنةُ تُسجّل الألفاظَ لا الأذهان، فلا وقوعَ فيها يُتصوَّر "
            "يُسقِط دعوى أنّ الموضوعَ له المعنى الذهنيُّ لا الخارجيّ"
        ),
        refuted_by="ركيزةٌ تُسجّل حالَ الذهن عند النطق مع اللفظ",
    )
    assert barren.vacancy is Vacancy.IMPOSSIBLE

    with pytest.raises(ResultsError, match="بلا ناقضٍ"):
        Placement(
            coordinate=("الوضع", "المعاني الذهنيّة"),
            forbidden_because="لا وقوعَ يُسقِطها ههنا",
        )


def test_the_dissociation_is_double_and_survives_the_disputed_row() -> None:
    """اتّجاهان متعاكسان، ويشتدّان معًا بإخراج `obj` ولا ينقلب أحدُهما."""

    for table in (FULL, WITHOUT_OBJ):
        (genus_add, genus_mod) = table["جنس"]
        (derived_add, derived_mod) = table["مشتقّ"]
        assert genus_add > derived_add  # الجنسُ أعلى في الإضافيّة
        assert derived_mod > genus_mod  # والمشتقُّ أعلى في التقييديّة

    before = (FULL["جنس"][0] / FULL["مشتقّ"][0], FULL["مشتقّ"][1] / FULL["جنس"][1])
    after = (
        WITHOUT_OBJ["جنس"][0] / WITHOUT_OBJ["مشتقّ"][0],
        WITHOUT_OBJ["مشتقّ"][1] / WITHOUT_OBJ["جنس"][1],
    )
    assert [round(one, 2) for one in before] == [2.70, 1.63]
    assert [round(one, 2) for one in after] == [3.10, 5.13]
    assert all(later > earlier for earlier, later in zip(before, after, strict=True))


def test_the_two_halves_are_not_equal_in_what_they_can_show() -> None:
    """التقييديّةُ أقربُ إلى التحليليّة، والإضافيّةُ ليست منها في شيء.

    فالنصفُ الأقوى عددًا (٥٫١٣×) يقوم على تصنيفٍ يقترب من تعريف صنفه؛
    والنصفُ الأضعفُ (٣٫١٠×) لا يلزم من التعريف شيئًا، **فهو الشاهد**.
    """

    modification = WITHOUT_OBJ["مشتقّ"][1] / WITHOUT_OBJ["جنس"][1]
    annexation = WITHOUT_OBJ["جنس"][0] / WITHOUT_OBJ["مشتقّ"][0]
    assert modification > annexation
    assert round(modification, 2) == 5.13
    assert round(annexation, 2) == 3.10

    # وكسرُ الدائريّة المُعلَن أخرج `ADJ` وحدَها، وما بقي اسمُ فاعلٍ ومفعولٍ ومصدر
    removed_for_circularity = ("ADJ",)
    remaining = ("اسمُ فاعل", "اسمُ مفعول", "مصدر")
    assert len(removed_for_circularity) == 1
    assert len(remaining) == 3
    assert not set(removed_for_circularity) & set(remaining)


def test_sixty_replicates_floor_the_claim_at_one_in_sixty_one() -> None:
    """أدنى `p` ممكنةٍ ٠٫٠١٦٤؛ وp السويّةِ ٠٫٠٠٦٨ **دونها**، فلا تُنشَر منه."""

    floor = permutation_floor(REPLICATES)
    assert floor == Fraction(1, 61)
    assert round(float(floor), 4) == 0.0164

    deviations = (CONTROLLED["مشتقّ"] - CONTROLLED["جنس_متوسّط"]) / CONTROLLED[
        "جنس_انحراف"
    ]
    assert round(deviations, 2) == 2.47

    normal_tail = 0.5 * math.erfc(deviations / math.sqrt(2))
    assert round(normal_tail, 4) == 0.0068
    assert normal_tail < float(floor)  # فالتصميمُ لا يبلغ ما يعِد به الحساب

    # وصفرُ تجاوزاتٍ هو الحالُ الأغلب: المتوقَّعُ ٠٫٤١ في الستّين
    assert round(REPLICATES * normal_tail, 2) == 0.41
    assert (1 - normal_tail) ** REPLICATES > 0.5

    with pytest.raises(AttainabilityError):
        permutation_floor(0)


def test_the_prediction_flips_with_the_control_and_the_control_came_after() -> None:
    """كاذبٌ خامًّا وصادقٌ مضبوطًا؛ والضبطُ بعد الرقم فلا يُختَم به حكم."""

    assert RAW["جنس"] > RAW["مشتقّ"]  # قبل الضبط: التنبّؤ ساقط
    assert CONTROLLED["جنس_متوسّط"] < CONTROLLED["مشتقّ"]  # وبعده: قائم

    ratio = Fraction(TRAINING_ROWS["جنس"], TRAINING_ROWS["مشتقّ"])
    assert round(float(ratio), 2) == 7.12
    assert round(math.sqrt(float(ratio)), 2) == 2.67

    # والوجهان مُعلَنان معًا، وذلك شرطُ قراءةِ أيِّهما
    published = (RAW["جنس"], CONTROLLED["جنس_متوسّط"])
    assert len(set(published)) == 2
    assert published[0] > published[1] * 2  # فالضبطُ حرّك الرقمَ أكثرَ من الضعف


def test_a_fallen_reading_does_not_take_its_measurement_with_it() -> None:
    """`+٠٫٢٥٨٩` لم يتحرّك، والساقطُ تأويلُه — وهما شيئان لا شيء."""

    assert CHAPTER_SIXTY_BITS == Fraction("0.2589")
    assert CHAPTER_SIXTY_BITS > 0

    withdrawn = "الجنسُ اعتباطيٌّ والمشتقُّ محسوب"
    standing = "مضمونُ المشتقّ مركّبٌ ومضمونُ الجنس بسيط"
    assert withdrawn != standing

    # والقائمُ أقوى لأنّه **يتنبّأ بالاتّجاه**: تركُّبُ المضمون ⇒ تركُّبُ الصورة
    assert "مركّب" in standing
    assert "اعتباط" in withdrawn
    # ولا يُقال «اعتباط» فارقًا، إذ اللغاتُ كلُّها اصطلاحيّةٌ على نصّ الكتاب
    assert "اصطلاح" not in withdrawn


def test_the_two_relations_do_not_exhaust_the_three_that_were_named() -> None:
    """ثلاثُ نِسَبٍ مُسمّاة، ومقيستان — والثالثةُ بقيّةٌ تُعَدّ ولا تُطوى."""

    named = ("إسناديّة", "تقييديّة", "إضافيّة")
    assert len(named) == 3

    for table in (FULL, WITHOUT_OBJ):
        for who, (annexation, modification) in table.items():
            remainder = 100 - annexation - modification
            assert remainder > 0, who  # فليست النسبتان قسمةً تامّة
            assert remainder < 50

    assert round(100 - sum(FULL["جنس"]), 1) == 27.4
    assert round(100 - sum(FULL["مشتقّ"]), 1) == 38.2
