"""**ختمٌ قبل النظر**: البيانُ بهوفمان لا بالإنتروبيا — تصحيحُ خللٍ في المعادلة.

**لم يُشغَّل شيءٌ بعد.**

**الخللُ المُصحَّح**: في `620b63a2…` كان شطرُ البيان `إنتروبيا × عدد`.
**والإنتروبيا حدٌّ أدنى لا تبلغه شفرةٌ رمزًا رمزًا** — يبلغها التقسيمُ
اللانهائيّ لا الشفرةُ الصحيحةُ الطول. والجشعُ **المبرهَن** — هوفمان:
«ادمج أقلَّ رمزين احتمالًا، وكرّر» — يبلغ `H ≤ L < H + 1`.

**فالتكلفةُ المنشورةُ كانت دون المُحقَّق**، وقولي «الاختيارُ جشعٌ فالتكلفةُ
حدٌّ أعلى» **مقلوبُ الجهة في شطر البيان**: كان حدًّا **أدنى**. والحدُّ
الأعلى إنّما يصحّ على شطر **القسمة** (أيَّ زوجٍ يُدمَج)، لا على شطر
**الترميز** — وقد خلطتُهما في عبارةٍ واحدة.

**والتصحيح**: يُستبدَل البيانُ بـ**طولِ شفرة هوفمان الفعليّ**. فيصير
الشطران معًا:

- **القسمةُ**: جشعٌ **غيرُ مبرهَن** (الزوجُ الأكثرُ وقوعًا) ⟹ حدٌّ أعلى.
- **الترميزُ**: جشعٌ **مبرهَن** (هوفمان) ⟹ **أمثلُ رمزًا رمزًا**، لا حدَّ
  فوقه ولا تحته.

**والبوّابةُ تبقى**: بنيةٌ يُشتقّ فيها مقشورٌ من مقشورٍ يعود إليه **يسقط
عليها الجشعُ باسمها، وتُوسَم وتُعَدّ ولا تُبتلَع**.

**والبايتاتُ تصل مئةً بالمئة**: `rebuild(peel(x)) == x` يُعاد فحصُه — فلا
تشكيلةَ ولا همزةَ ولا شدّةَ ولا حرفَ تسقط، ولا يُعرَف لأيٍّ منها اسمٌ ولا
وظيفة. **بتّاتٌ عمياءُ فقط.**
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="الصعودُ المكتشَف ببيانٍ هوفمانيّ",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "كما في `620b63a2…` غيرَ أنّ شطرَ البيان يصير **طولَ شفرة هوفمان** "
        "لا الإنتروبيا: تُبنى الشفرةُ على نصف الآيات بالجشع المبرهَن (دمجُ "
        "أقلّ رمزين احتمالًا) وتُقاس أطوالُها على النصف الآخر ثمّ بالعكس؛ "
        "ورمزٌ لم يُرَ في السند يُعطى طولَ أطولِ شفرةٍ زائدًا واحدًا "
        "ويُعلَن نصيبُه؛ والمعجمُ كما هو يُهجّى بحروف الـ١١٢"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ل١",
        statistic="أدنى (طولُ هوفمان − الإنتروبيا) على نقاط الفحص (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "الآلةَ لا المادّة: مبرهنةُ شانون تمنع شفرةً دون إنتروبيا مصدرها، "
            "فنزولُ هوفمان تحتها عطلُ حسابٍ يردّ الجدولَ كلَّه"
        ),
    ),
    Prediction(
        identifier="ل٢",
        statistic="أقصى (طولُ هوفمان − الإنتروبيا) على نقاط الفحص (بت)",
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ أيضًا: هوفمان مبرهَنٌ دون H + 1، فتجاوزُه يعني أنّ "
            "المبنيَّ ليس شفرةَ هوفمان"
        ),
    ),
    Prediction(
        identifier="ل٣",
        statistic="تكلفةُ أفضل نقطةٍ بهوفمان مقسومةً على المنشورِ بالإنتروبيا",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "تشخيصي للخلل: إن نزلت التكلفةُ بهوفمان عن المنشور فالإنتروبيا "
            "لم تكن تُقلّل الكلفة، ويسقط سببُ إعادة الحساب من أصله"
        ),
    ),
    Prediction(
        identifier="ل٤",
        statistic="عددُ الدمجات عند أفضل نقطةٍ بهوفمان",
        threshold=Fraction(4_500),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ ثمنَ هوفمان يخفّ بنقصان عدد الرموز فيتأخّر الوقوف؛ "
            "فإن تقدّم الوقوفُ فالعكسُ هو الواقع ويُنشَر كذلك"
        ),
    ),
    Prediction(
        identifier="ل٥",
        statistic="عددُ البايتات التي لا تُستعاد مطابقةً من التقشير",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوى وصولِ البايتات مئةً بالمئة: بايتةٌ واحدةٌ تسقط تُبطِل "
            "البناءَ كلَّه، ولا يُنقِذها إعلان"
        ),
    ),
    Prediction(
        identifier="ل٦",
        statistic="أدنى (المحجوزة − الملحَقة) على نقاط الفحص (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies="اتّجاهَ الانتحال؛ وهو الدرسُ الذي سقطت به نتيجتي في `ca8fd2c`",
    ),
)

DIGEST = "34133d546ce5963e56ea80598806950951deb728527cf1506ea3b584640fc5d5"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_two_conditions_fence_huffman_between_its_proven_bounds() -> None:
    """ل١ ول٢ يحصران الطولَ في [H، H+1) — وهما شرطا آلةٍ لا مادّة."""

    low = next(one for one in PREDICTIONS if one.identifier == "ل١")
    high = next(one for one in PREDICTIONS if one.identifier == "ل٢")
    assert low.threshold == Fraction(0) and low.direction is Direction.AT_LEAST
    assert high.threshold == Fraction(1) and high.direction is Direction.AT_MOST


def test_the_split_of_greedy_into_two_halves_is_recorded() -> None:
    """القسمةُ جشعٌ غيرُ مبرهَن، والترميزُ جشعٌ مبرهَن — وقد خُلِطا قبلُ."""

    assert "مقلوبُ الجهة في شطر البيان" in __doc__
    assert "أمثلُ رمزًا رمزًا" in __doc__
    mine = next(one for one in PREDICTIONS if one.identifier == "ل٣")
    assert "تشخيصي للخلل" in mine.falsifies
