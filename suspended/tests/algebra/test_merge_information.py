"""`Δ` يُحسَب ولا يُقدَّر — والحدُّ المنشورُ `2δ²/ln2` **ليس حدًّا أدنى**.

**المادّةُ مبنيّةٌ باليد**، فالفحصُ فحصُ جبرٍ لا فحصُ لغة.

`THE_CHAIN_RULE_GIVES_DELTA_EXACTLY`: الكتلةُ دالّةٌ في الحالة، فـ
`I(Y;X) = I(Y;B) + I(Y;X|B)` هُويّةٌ لا تقريب. فـ`Δ = I(Y;X) − I(Y;B)`
يُحسَب من الجداول نفسِها التي يُحسَب منها `δ`، ولا حاجةَ إلى تقدير.

`THE_PUBLISHED_PINSKER_FORM_LOSES_TWO_FACTORS`: ومن قدّره بـ`2δ²/ln2` خسر
عاملين: (١) بنسكر يقيس البُعدَ عن **الخليط**، ومتباينةُ المثلّث لا تضمن
إلّا `δ/2` لأحد الليفين — فعاملُ أربعة؛ (٢) و`Δ` متوسّطٌ **موزونٌ** بوزن
الليف — فعامل `1/w`. فالمنشورُ أوسعُ من المضمون بـ`4/w`، والصحيحُ
`Δ ≥ w·δ²/(2 ln2)`.

`AND_A_LOWER_BOUND_THAT_EXCEEDS_ITS_QUANTITY_IS_FALSE`: وليس ذلك تراخيًا
في حدٍّ صحيح: المقيسُ على مدوّنتنا `Δ = 1.1533` بتًّا لطبقة الرسم،
و«الحدُّ» المنشورُ **٢٫٨٣٨١** — أي **فوقها**. بل يجاوز `I` للذرّة كلِّها
(١٫٦٩٩٤)، وهي سقفُ القناة. فالصيغةُ المنشورةُ **تُكذَّب عدديًّا**، لا
تُوصَف بالخشونة.
"""

from __future__ import annotations

import math

from algebra.markov_layers import (
    Layer,
    lumpability,
    merge_information,
    mutual_information,
    project_census,
)

LN2 = math.log(2)

# كتلةٌ واحدة {a,b} وليفان متباعدان، وكتلةٌ ثانية {c} مرجعًا
CENSUS = {
    ("a", "c"): 90,
    ("a", "a"): 10,
    ("b", "c"): 10,
    ("b", "a"): 90,
    ("c", "c"): 50,
    ("c", "a"): 50,
}
LAYER = Layer(name="كتلتان", projection={"a": "A", "b": "A", "c": "C"})


def test_the_chain_rule_identity_holds_exactly() -> None:
    """`I(Y;X) = I(Y;B) + Δ` — تُفحَص عدديًّا على مادّةٍ مبنيّة."""

    with_target = {
        (first, LAYER.of(second)): number for (first, second), number in CENSUS.items()
    }
    whole = mutual_information(with_target)
    blocked = mutual_information(project_census(CENSUS, LAYER))
    assert abs(whole - (blocked + merge_information(CENSUS, LAYER))) < 1e-12


def test_the_published_bound_exceeds_the_quantity_it_claims_to_bound() -> None:
    """`2δ²/ln2` يخرج فوق `Δ` — فهو ليس حدًّا أدنى بحال."""

    delta = float(lumpability(CENSUS, LAYER).defect)
    published = 2 * delta**2 / LN2
    measured = merge_information(CENSUS, LAYER)
    assert delta > 0 and measured > 0
    assert published > measured  # وهذا وحدَه يُسقِط الصيغة


def test_the_corrected_bound_is_a_bound() -> None:
    """`Δ ≥ w·δ²/(2 ln2)` — بوزن أصغر ليفٍ في الكتلة، ويصدق."""

    delta = float(lumpability(CENSUS, LAYER).defect)
    masses = {"a": 100, "b": 100}
    weight = min(masses.values()) / sum(masses.values())
    corrected = weight * delta**2 / (2 * LN2)
    assert corrected <= merge_information(CENSUS, LAYER)
    assert corrected < 2 * delta**2 / LN2


def test_a_lumpable_layer_has_zero_merge_information() -> None:
    """التكتيلُ الشديدُ صفرُ خلل **وصفرُ** `Δ` — والمسبارُ يوافق الشرط."""

    census = {
        ("a", "a"): 25,
        ("a", "b"): 25,
        ("a", "c"): 50,
        ("b", "a"): 10,
        ("b", "b"): 40,
        ("b", "c"): 50,
        ("c", "c"): 40,
        ("c", "a"): 60,
    }
    layer = Layer(name="مكتَّلة", projection={"a": "A", "b": "A", "c": "C"})
    reading = lumpability(census, layer)
    assert reading.defect == 0 and reading.is_strong
    assert abs(merge_information(census, layer)) < 1e-12
