"""**ختمٌ قبل النظر**: سلّمُ الضبط بشرط السياق — h_k على قناة الحالة.

**لم يُشغَّل شيءٌ بعد.** هذا الملفُّ يُودَع **قبل** كتابة القارئ وقبل أيّ
رقم، وترتيبُه مُثبَتٌ في سجلّ الالتزامات؛ فمن بدّل شرطًا بعد النظر عُرِف
بتغيُّر البصمة.

**السؤالُ**: Δضبط قِيس ١٫٩٥١٨ بتًّا للموضع **بلا سياق** (`dd8d366`)، ونُشِر
**حدًّا أعلى** لأنّ الشرطَ على السياق لا يزيد الإنتروبيا. فكم ينزل؟ وهل يبقى
للضبط خبرٌ بعد أن يُعطى القارئُ الرسمَ كلَّه؟

**سلّمان لا واحد**، لأنّهما سؤالان:

- **سلّمُ الرسم** `h^A_k = H(s_i | ℓ_{i−k}…ℓ_i)` — ما يضيفه الضبطُ لقارئٍ
  **يملك الحروفَ وحدَها**. وهذا هو Δضبط بمعناه الأوّل.
- **سلّمُ الفكّ** `h^B_k = H(s_i | ℓ_{i−k}…ℓ_i، s_{i−k}…s_{i−1})` — ما يضيفه
  لقارئٍ **يقرأ متتابعًا** فقد حلّ ما قبلَه.

**قراراتٌ تُختَم معها**: الوحداتُ مواضعُ الرسم (لا توسيعَ للشدّة، لأنّ
المجرّدَ لا شدّةَ فيه)؛ والحروفُ مُطبَّعةٌ بـR2/R7؛ و**السياقُ داخلَ السطر
ولا يعبره**؛ و**أرضيّةُ قراءة السياق ثلاثون وقوعًا**؛ وما سقط سياقُه
**يُستبعَد ويُعلَن نصيبُه** ولا يُصفَّر؛ و**تصحيحُ ميلر–مادو** يُطبَّق على كلّ
رتبة.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="سلّمُ الضبط بشرط السياق",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "على مواضع الرسم (حرفٌ مُطبَّعٌ بـR2/R7، وحالةٌ هي سلسلةُ علاماته بلا "
        "توسيعِ شدّة): h^A_k = H(s_i | ℓ_{i−k}…ℓ_i) وh^B_k = H(s_i | "
        "ℓ_{i−k}…ℓ_i، s_{i−k}…s_{i−1})؛ السياقُ داخلَ السطر لا يعبره؛ "
        "أرضيّةُ السياق ثلاثون وقوعًا؛ الساقطُ يُستبعَد ويُعلَن نصيبُه؛ "
        "وتصحيحُ ميلر–مادو على كلّ رتبة"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="س١",
        statistic="أدنى فرقٍ بين رتبتين متتاليتين في السلّمين (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "المقدِّرَ نفسَه لا المادّة: الشرطُ لا يزيد الإنتروبيا مبرهنةً، "
            "فصعودُ السلّم عطلُ آلةٍ يوجب ردَّ الأرقام كلِّها"
        ),
    ),
    Prediction(
        identifier="س٢",
        statistic="أقصى (h^B_k − h^A_k) على الرتب المقروءة (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "المقدِّرَ نفسَه: سلّمُ الفكّ يشترط على ما يشترط عليه سلّمُ الرسم "
            "وزيادةً، فلا يعلوه"
        ),
    ),
    Prediction(
        identifier="س٣",
        statistic="أدنى h على رتبةٍ مقروءة في السلّمين (بت)",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى أنّ الضبطَ خبرٌ جوهريٌّ لا زائدةٌ مستخرَجة: إن نزل عن بتٍّ "
            "واحدٍ فأكثرُ الضبط مُستخرَجٌ من الرسم وسياقِه، والدَّينُ الأوّلُ "
            "كان أصغرَ ممّا ظُنّ"
        ),
    ),
    Prediction(
        identifier="س٤",
        statistic="نصيبُ المواضع المقروءة عند الرتبة الثانية في سلّم الرسم",
        threshold=Fraction(1, 2),
        direction=Direction.AT_LEAST,
        falsifies="قراءةَ h₂ أصلًا، فتُوسَم الرتبةُ الثانيةُ UNREACHABLE",
    ),
    Prediction(
        identifier="س٥",
        statistic="تصحيحُ ميلر–مادو عند أعلى رتبةٍ مقروءة (بت)",
        threshold=Fraction(1, 5),
        direction=Direction.AT_MOST,
        falsifies=(
            "قراءةَ الهبوط بنيةً: إن بلغ الانحيازُ خُمسَ البتّ فالنزولُ أثرُ "
            "ندرةٍ كما كانت هضبةُ المدى البعيد"
        ),
    ),
)

DIGEST = "9034199d2b6f55968f0ef48e7ba81e09f7ea4f91331c95219ed4419de83c798d"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل — فتبديلُ شرطٍ يُغيّرها."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_every_condition_names_what_falls_with_it() -> None:
    """شرطٌ لا يُسمّي ما يسقط بسقوطه ليس شرطًا."""

    assert len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == 5
    for one in PREDICTIONS:
        assert one.falsifies.strip()
    at_least = [one for one in PREDICTIONS if one.direction is Direction.AT_LEAST]
    assert len(at_least) == 3


def test_two_conditions_test_the_machine_and_three_test_the_matter() -> None:
    """س١ وس٢ مبرهنتان — سقوطُهما يردّ الأرقام؛ والثلاثُ الباقيةُ عن المادّة."""

    machine = {"س١", "س٢"}
    matter = {"س٣", "س٤", "س٥"}
    assert machine | matter == {one.identifier for one in PREDICTIONS}
    assert not machine & matter
    risky = next(one for one in PREDICTIONS if one.identifier == "س٣")
    assert risky.threshold == Fraction(1)  # الشرطُ الوحيدُ المعرَّضُ حقًّا
