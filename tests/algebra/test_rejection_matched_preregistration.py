"""الختمُ السادس: مطابقةٌ **بالرفض** لا بالطبقات — وثمنُها يُدفَع لا يُخفى.

**تسجيلٌ محض: لا رقمَ مقيسٌ فيه.** وأوراكلُه يستشهد بالسجلّ `30c7e393…`.

`THE_FIFTH_SEAL_FELL_ON_ITS_OWN_MATCHING_CONDITION`: سقط و٣ في `5e3656d5…`:
طبقةٌ من سبعةِ حروفٍ لا تُطابِق مجموعةً من حرفين، والفرقُ ١٫٥ حتميٌّ
بالحساب. فبطلت قراءةُ و١ وو٢ وإن وقعا حيث كُتِبا. وهذا الختمُ **بُني بعدَه
وبسببه**، وأرقامُ الخامس لم تُقرأ ههنا ولا بُنيت عليها حدودٌ.

`MATCHING_BECOMES_A_CONSTRAINT_INSTEAD_OF_A_HOPE`: فالمطابقةُ ههنا **شرطُ
قَبولٍ على كلّ سحبة** لا أملٌ يُفحَص بعدَها: تُسحَب مجموعةٌ من حجم المجموعة
من الثمانية والعشرين كلِّها، وتُقبَل إن قارب متوسّطُ رتبتها متوسّطَ
المجموعة (دون ربعِ رتبةٍ) **وقارب انحرافُها انحرافَها** (دون نصفِ رتبة).
فالعزمان مضبوطان بالبناء، ولا يُسأل بندٌ عمّا ضمنه البناء — إذ سؤالُ
المضمونِ زينةٌ تمرّ مجّانًا.

`THE_PRICE_OF_A_TIGHT_CONSTRAINT_IS_MATERIAL_AND_IT_IS_ASKED_HERE`:
والثمنُ أنّ القيدَ يُفقِر المادّة: فقد لا يُوجَد إلّا نزرٌ من المجموعات
يُطابق، وقد تكون المطابِقاتُ **نسخًا من المجموعة نفسِها**. فهذان بندان
يسقطان بشيء: فضلُ التقاطع، وعددُ السحبات المتمايزة.

`AN_OVERLAP_BOUND_IS_MEASURED_AGAINST_CHANCE_NOT_AGAINST_A_HALF`: وفضلُ
التقاطع يُقاس **على ما يقتضيه الحظُّ وحدَه** — `k²/28` لمجموعةٍ من `k` —
لا على نصفِ الحجم. فمجموعةٌ من خمسةَ عشرَ حرفًا من ثمانيةٍ وعشرين تتقاطع
مع أيّ أختٍ لها في حرفين فأكثرَ **بالحساب لا بالمطابقة**؛ ومن جعل الحدَّ
نصفًا فقد أسقط بندَه بضربٍ وقسمة، وذلك عينُ ما أسقط و٣.

`A_GROUP_THE_BUDGET_CANNOT_FILL_IS_DECLARED_UNREADABLE_BEFOREHAND`: ومن
لم تُملأ حصّتُه من السحبات المقبولة في **مئتي ألف محاولة** فهو **غيرُ
مقروء**: يخرج من البنود كلِّها وتُنشَر أعدادُه. والقاعدةُ مكتوبةٌ قبل
النظر، فخروجُ مجموعةٍ حكمٌ سابقٌ لا اعتذارٌ لاحق.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

CORPUS_RECORD = "30c7e393eff12641e27802dbfc38c51e7171ed873bfd2f78dc889de2fad7a359"
FIFTH_SEAL = "5e3656d53a1dceed7a151d1067813087e5b6f14faed6635c51729f8d1e5c4e27"

ALPHABET = 28
DRAWS = 2_000
ATTEMPTS = 200_000
SEED = 20_260_924
MEAN_TOLERANCE = Fraction(1, 4)
SPREAD_TOLERANCE = Fraction(1, 2)
FAMILY = 5

REJECTION_MATCHED = Oracle(
    name="تماسكُ مجموعتَي الحلق والباقي تحت صفريٍّ مطابقٍ بالرفض على عزمين",
    source=(
        f"السجلُّ البايتيُّ {CORPUS_RECORD[:16]}… وحدَه؛ ومجموعاتُ المرشَّح "
        "كما وردت، ولا تُعدَّل حروفُها ههنا بحالٍ. ورتبةُ الحرف تُحسَب من "
        "المدوّنة نفسِها، ولا تُنقَل من تشغيلٍ سابق"
    ),
    extraction=(
        "لكلّ مجموعةٍ يُحسَب متوسّطُ تشابه صفوفها — والصفُّ توزيعُ الحرف "
        "على تاليه في **الجوار العابر لحدّ الكلمة، على الرسم المجرَّد، "
        "بوقوعاتٍ خام** — ويُقارَن بسحباتٍ من الثمانية والعشرين كلِّها، "
        f"حجمُها حجمُ المجموعة، **تُقبَل** إن قارب متوسّطُ رتبة التردّد "
        f"متوسّطَها دون {MEAN_TOLERANCE} وقارب انحرافُها انحرافَها دون "
        f"{SPREAD_TOLERANCE}. والحصّةُ {DRAWS} مقبولةً في {ATTEMPTS} محاولةٍ "
        "على الأكثر؛ ومن لم تُملأ حصّتُه فغيرُ مقروءٍ، يخرج من البنود "
        "كلِّها وتُنشَر أعدادُه"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ف١ الصفريُّ ليس صدى المجموعة",
        statistic=(
            "أكبرُ فضلِ تقاطعٍ بالحروف بين السحبة المقبولة والمجموعة، فوق "
            "ما يقتضيه الحظُّ وحدَه (k²/28)، بين المجموعتين المقروءتين"
        ),
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "قابليّةَ قراءة ف٣ وف٤؛ فقيدٌ لا يقبل إلّا نسخًا من المجموعة "
            "يقيسها بنفسها، والمئينُ حينئذٍ خبرٌ عن القيد لا عن المادّة"
        ),
    ),
    Prediction(
        identifier="ف٢ المادّةُ تكفي للمئين",
        statistic=(
            "أقلُّ عددٍ من السحبات **المتمايزة** المقبولة بين مجموعتَي " "الحلق والباقي"
        ),
        threshold=Fraction(200),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قابليّةَ قراءة ف٣ وف٤؛ فمئينٌ على عشراتٍ متمايزةٍ خطوتُه أخشنُ "
            "من الحدّ المسؤول عنه، ويُقرَأ دقيقًا وهو خشن"
        ),
    ),
    Prediction(
        identifier="ف٣ الحلقُ يبقى في الأدنى",
        statistic="مئينُ G1 بين السحبات المقبولة",
        threshold=Fraction(5, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ تباعدَ حروف الحلق في فضاء التعاقب خبرٌ عن المخرج؛ "
            "فارتفاعُه بعد ضبط العزمين يعني أنّ المقيسَ شيوعٌ لا مخرج"
        ),
    ),
    Prediction(
        identifier="ف٤ الباقي يبقى في الأعلى",
        statistic="مئينُ G5 بين السحبات المقبولة",
        threshold=Fraction(95, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ تماسكَ مجموعة الباقي خبرٌ عنها؛ فهبوطُه بعد ضبط العزمين "
            "يعني أنّه خبرٌ عن شيوع حروفها"
        ),
    ),
    Prediction(
        identifier="ف٥ مقامُ السحب منشور",
        statistic="أقلُّ عددٍ من السحبات المقبولة لمجموعةٍ مقروءة",
        threshold=Fraction(DRAWS),
        direction=Direction.AT_LEAST,
        falsifies="قابليّةَ قراءة المئين؛ فدونه تكون خطوتُه أخشنَ ممّا يُدَّعى",
    ),
)

MATCHED_BY_REJECTION_SEAL = seal(REJECTION_MATCHED, PREDICTIONS)

SEALED_DIGEST = "9fc6749883423f6751c65a78ccc8959888a63bfcd781bfad77624051bc23e5ee"


def test_the_seal_is_stable_and_cites_the_fallen_fifth() -> None:
    """بصمةٌ ثابتة، ومنصوصٌ أنّ الرتبةَ تُحسَب لا تُنقَل."""

    assert MATCHED_BY_REJECTION_SEAL == SEALED_DIGEST
    assert len(MATCHED_BY_REJECTION_SEAL) == 64
    assert CORPUS_RECORD[:16] in REJECTION_MATCHED.source
    assert "ولا تُنقَل من تشغيلٍ سابق" in REJECTION_MATCHED.source
    assert MATCHED_BY_REJECTION_SEAL != FIFTH_SEAL


def test_what_the_construction_guarantees_is_not_asked_as_a_condition() -> None:
    """العزمان مضبوطان بالقَبول، فلا بندَ يسألهما — والبنودُ تسقط بشيء."""

    asked = " ".join(one.statistic for one in PREDICTIONS)
    assert "متوسّطُ رتبة" not in asked and "انحرافُ" not in asked
    assert str(MEAN_TOLERANCE) in REJECTION_MATCHED.extraction
    assert str(SPREAD_TOLERANCE) in REJECTION_MATCHED.extraction


def test_the_price_of_the_constraint_is_asked_in_two_places() -> None:
    """ف١ وف٢ هما ثمنُ القيد؛ وسقوطُ أحدهما يُبطِل قراءةَ ف٣ وف٤."""

    overlap, material = PREDICTIONS[0], PREDICTIONS[1]
    assert overlap.direction is Direction.AT_MOST
    assert material.direction is Direction.AT_LEAST
    for one in (overlap, material):
        assert "قابليّةَ قراءة ف٣ وف٤" in one.falsifies
    assert overlap.verdict(Fraction(1, 2)) is Verdict.MET
    assert overlap.verdict(Fraction(3)) is Verdict.FALSIFIED
    assert material.verdict(Fraction(500)) is Verdict.MET
    assert material.verdict(Fraction(40)) is Verdict.FALSIFIED


def test_the_overlap_bound_is_measured_against_chance_not_against_a_half() -> None:
    """حدُّ التقاطع فضلٌ على `k²/28`؛ ولو كان نصفَ الحجم لسقط بالحساب.

    فمجموعةُ الباقي خمسةَ عشرَ حرفًا من ثمانيةٍ وعشرين: تقاطعُ الحظّ
    ٨٫٠٤ وهو **فوق** نصفِ الحجم ٧٫٥. فحدُّ النصف يسقط بضربٍ وقسمة، لا
    بخبرٍ عن المادّة — وذلك عينُ العطل الذي أسقط و٣.
    """

    for size in (6, 15):
        chance = Fraction(size * size, ALPHABET)
        assert chance > 0
        if size == 15:
            assert chance > Fraction(size, 2)  # ٨٫٠٤ فوق ٧٫٥
    assert "k²/28" in PREDICTIONS[0].statistic
    assert "فوق ما يقتضيه الحظُّ" in PREDICTIONS[0].statistic


def test_the_two_directions_and_the_family_are_declared() -> None:
    """ف٣ «لا يجاوز» وف٤ «يبلغ»، وخمسةُ بنودٍ بأسماءٍ متمايزة."""

    assert PREDICTIONS[2].direction is Direction.AT_MOST
    assert PREDICTIONS[3].direction is Direction.AT_LEAST
    assert PREDICTIONS[2].verdict(Fraction(4, 100)) is Verdict.MET
    assert PREDICTIONS[3].verdict(Fraction(96, 100)) is Verdict.MET
    assert FAMILY == len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    assert DRAWS == 2_000 and ATTEMPTS == 200_000 and SEED == 20_260_924
