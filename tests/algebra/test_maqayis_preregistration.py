"""تسجيلٌ مختومٌ قبل النظر: أربعةُ شروطٍ على مقاييس ابن فارس.

**حالُ هذا الملفّ**: لا رقمَ مقيسٌ فيه. يحمل **الأوراكلَ مُعلَنًا** و**أربعةَ
شروطٍ بحدودٍ عدديّة** و**بصمتَها**، ويُودَع **قبل** أن يُفتَح الملفُّ. فإن
جاء القياسُ بعدُ فحُكمُه عليه، ولا تُبدَّل الحدودُ لتوافقَه — وتبديلُها
يُعرَف بتغيُّر البصمة.

`THE_ORDER_OF_THE_TWO_COMMITS_IS_THE_EVIDENCE`: لا يُصدَّق تسجيلٌ سابقٌ لأنّه
يقول عن نفسه ذلك، بل لأنّ التزامَه في التاريخ **قبل** التزامِ القياس. فهذا
الملفُّ يُدفَع وحدَه، والأرقامُ في التزامٍ آخَر بعدَه.

والمقياسُ في الشرطين ٣ و٤ **فائضُ** المعلومة المتبادلة فوق صفريٍّ تبديليّ، لا
الخام: فالخامُ موجبٌ حتى على بياناتٍ مستقلّةٍ تمامًا (وذلك مفحوصٌ في
`test_signified`). واعتباطيّةُ العلامة هي الصفريُّ، لا النتيجة.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.attainability import (
    Attainability,
    bonferroni_threshold,
    read_attainability,
)
from algebra.signified import (
    SIGNIFIED_NAMED_RESIDUALS,
    Direction,
    Oracle,
    Prediction,
    SignifiedError,
    Verdict,
    seal,
)

MAQAYIS = Oracle(
    name="مقاييسُ اللغة لابن فارس",
    source="maqayis_by_root_csv_999.csv في شجرة Alghanem",
    extraction=(
        "حقلُ semantic_axes نصًّا، وaxes_count عددًا، وroot_full وroot_type "
        "كما وردت؛ بلا تنقيحٍ ولا توحيدِ إملاء"
    ),
)

REPLICATES = 2_000
SEED = 20_260_923
FAMILY = 4

PREDICTIONS = (
    Prediction(
        identifier="ق-ج١ سلامةُ الحقل",
        statistic="نصيبُ الصفوف التي عددُ محاورها المسرودة يخالف axes_count",
        threshold=Fraction(5, 100),
        direction=Direction.AT_MOST,
        falsifies="كلُّ ما يقوم على semantic_axes، فيصير حكمُ ما بعده VOID",
    ),
    Prediction(
        identifier="ق-ج٢ التلوّث",
        statistic="نصيبُ الأزواج التي يحوي نصُّ محورها حروفَ جذرها بترتيبها",
        threshold=Fraction(20, 100),
        direction=Direction.AT_MOST,
        falsifies="استقلالَ المدلول عن الصورة، فيصير كلُّ ارتباطٍ دائريًّا",
    ),
    Prediction(
        identifier="ق-ج٣ نوعُ الجذر",
        statistic="فائضُ I(نوعُ الجذر ؛ المحور) فوق الصفريّ التبديليّ، بالبتّات",
        threshold=Fraction(1, 100),
        direction=Direction.AT_LEAST,
        falsifies="«بنيةُ الجذر تقيّد مدلولَه» عند هذه الدقّة",
    ),
    Prediction(
        identifier="ق-ج٤ الفاء",
        statistic="فائضُ I(الحرفُ الأوّل ؛ المحور) فوق الصفريّ التبديليّ، بالبتّات",
        threshold=Fraction(1, 100),
        direction=Direction.AT_LEAST,
        falsifies="«الرمزيّةُ الصوتيّة في فاء الجذر» عند هذه الدقّة",
    ),
)

SEAL = "780d948acd88124b5d66734c4bf0712f827b0bd648d97d6aa872301c20ee716a"


def test_the_seal_is_fixed_before_any_measurement() -> None:
    """البصمةُ مثبَّتةٌ: شرطٌ يُبدَّل بعد النظر يُعرَف بتغيُّرها."""

    assert seal(MAQAYIS, PREDICTIONS) == SEAL
    assert len(PREDICTIONS) == FAMILY


def test_every_prediction_names_a_threshold_a_direction_and_a_casualty() -> None:
    """كلُّ شرطٍ يحمل حدًّا عدديًّا واتّجاهًا وما يسقط بسقوطه — ولا استثناء."""

    for prediction in PREDICTIONS:
        assert prediction.threshold > 0
        assert prediction.direction in Direction
        assert prediction.falsifies.strip()
        assert prediction.identifier.startswith("ق-ج")


def test_a_prediction_that_names_no_casualty_is_refused() -> None:
    """شرطٌ لا يُسمّي ما ينقضه غيرُ قابلٍ للنقض، فيُرَدّ في الإنشاء."""

    with pytest.raises(SignifiedError):
        Prediction(
            identifier="ق-ج٥",
            statistic="أيُّ مقياس",
            threshold=Fraction(1, 2),
            direction=Direction.AT_LEAST,
            falsifies="   ",
        )


def test_the_threshold_is_attainable_with_the_declared_replicates() -> None:
    """حدُّ بونفيروني على أربعةٍ يُبلَغ بـ٢٬٠٠٠ تبديلٍ، وفيه سعةٌ لا حدُّ سكّين."""

    threshold = bonferroni_threshold(Fraction(5, 100), FAMILY)
    assert threshold == Fraction(125, 10_000)
    reading = read_attainability(threshold, REPLICATES)
    assert reading.standing is Attainability.ROOMY
    assert reading.outcomes == 25
    assert reading.floor < threshold


def test_no_verdict_is_recorded_in_this_commit() -> None:
    """لا حكمَ ههنا: الأحكامُ ثلاثةٌ مغلقة، وتُسجَّل في التزامٍ لاحقٍ بأرقامه."""

    assert set(Verdict) == {Verdict.MET, Verdict.FALSIFIED, Verdict.VOID}
    # والسلامةُ تحجُب ما بعدها: شرطٌ يسقط أساسُه يُحكَم عليه VOID لا FALSIFIED
    assert PREDICTIONS[2].verdict(Fraction(0), void=True) is Verdict.VOID
    assert PREDICTIONS[2].verdict(Fraction(0)) is Verdict.FALSIFIED
    assert PREDICTIONS[0].verdict(Fraction(1, 100)) is Verdict.MET


def test_the_named_residuals_are_five_and_distinct() -> None:
    """البواقي المُسمّاةُ خمسٌ، ولا تكرارَ فيها."""

    assert len(SIGNIFIED_NAMED_RESIDUALS) == 5
    assert len(set(SIGNIFIED_NAMED_RESIDUALS)) == 5
