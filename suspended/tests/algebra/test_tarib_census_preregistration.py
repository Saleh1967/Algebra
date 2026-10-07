"""تسجيلُ تعداد الدرجات مختومًا: سبعةُ بنودٍ كُتِبت قبل أن يُقرَأ رقمٌ واحد.

**ولماذا ختمٌ ثانٍ لا إضافةٌ إلى الأوّل**: التسجيلُ `3a7ccdc9…` **مغلق**،
وإضافةُ بندٍ إليه تُبدّل بصمتَه فتُبطِله — وذلك عينُ ما بُنِي ليمنعه. والبنودُ
السبعةُ ليست تعديلًا لشروطه أصلًا: هي **دعوًى أخرى بمقياسٍ آخرَ ومستوًى
آخر**، فتُختَم ختمًا ثانيًا وتُنشَر إلى جانبه لا بدله.

`THE_TWO_SEALS_ANSWER_TWO_DIFFERENT_QUESTIONS`: فالأوّلُ يسأل **داخلَ
المعرَّبات**: أيفترق المصوغُ عن غير المصوغ؟ وأرضيّتُه ١/١٠ لأنّ تبديل
الوسمين على خمسةٍ لا يعطي أكثرَ من عشرة تراتيب. وهذا الثاني يسأل **لكلّ
معرَّبٍ على حدة**: أدرجتُه شاذّةٌ بين أقرانه في الطول والتردّد؟ ومقامُه
مجموعةُ الضابط — مئاتٌ عند الترددات النادرة — فدقّتُه `1/|الضابط|`.

`THE_FINER_FLOOR_IS_REAL_AND_IT_IS_NOT_A_SUBSTITUTE`: والملاحظةُ صحيحةٌ
ويُعترَف بها بلا تحفّظ: مَن قاس الأرضيّةَ على تبديل الوسمين وحدَه لم يرَ
حجمَ الضابط. بل إنّ جمعَ المئينات الخمسة يعطي مستوًى أدقَّ من ١/١٠ بكثير:
لو وقع الخمسةُ كلُّهم دون المئين الخامس لكان احتمالُ ذلك صدفةً
`(1/20)^5 = 1/3,200,000`. **لكنّه لا يُغني عن الأوّل**: مطابقةُ الطول
والتردّد لا تُزيل أنّ الدخيلَ دخل، فالمقارنةُ بالأصيل تخلط الدخولَ
بالصياغة — وذلك هو السببُ المكتوبُ في التسجيل الأوّل لاختيار المقارنة داخلَ
المعرَّبات. فمستويان لا مستوًى، ويُنشَران معًا.

`THE_SCORES_ARE_A_DESCRIPTION_AND_THE_INFERENCE_LIVES_IN_THE_SEALS`: ودرجاتُ
التعداد تُحسَب **داخلَ العينة**، فهي وصفٌ لا استدلال. ومن قرأ منها استدلالًا
عاريًا فقد أخذ من النموذج ما لم يُسجَّل له مقام.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.attainability import label_permutation_floor, permutation_floor
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

CENSUS = Oracle(
    name="تعدادُ درجات الانتقال على المصحف، ومئينُ كلّ معرَّبٍ في ضابطه",
    source=(
        "عمودُ الرسم من المحاذاة ببصمته وإغلاقه (٧٧٬٤٢٩ صفًّا)، وقواعدُ "
        "التطبيع مُسمّاةٌ (همزاتٌ مدموجة، وصلٌ، إمالة) لا غيرُها"
    ),
    extraction=(
        "الدرجةُ مجموعُ `log2 P(اللاحق | السابق)` على ثنائيات اللفظ، "
        "والوحدةُ **بتٌّ للفظ**، والنموذجُ مقدَّرٌ **داخلَ العينة** فالدرجاتُ "
        "وصفٌ لا استدلال. ولكلّ معرَّبٍ مجموعةُ ضابطٍ من ألفاظ المصحف "
        "المطابقةِ له في الطول والتردّد، ويُنشَر موضعُه بينهم مئينًا"
    ),
)

FAMILY = 7
CONTROL_FLOOR = 100
ROWS = 77_429
REPLICATES = 2_000

PREDICTIONS = (
    Prediction(
        identifier="ج١ الوحدةُ والنموذجُ مُعلَنان قبل العدّ",
        statistic="عددُ الحقول المُعلَنة: الوحدةُ، وقواعدُ التطبيع، وموضعُ التقدير",
        threshold=Fraction(3),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قابليّةَ قراءة الدرجات أصلًا؛ فدرجةٌ بلا وحدةٍ ولا قواعدَ ولا "
            "موضعِ تقديرٍ رقمٌ لا يُقارَن بشيء"
        ),
    ),
    Prediction(
        identifier="ج٢ مجموعةُ الضابط تبلغ مئةً فأكثر",
        statistic="عددُ الألفاظ في أصغر مجموعةِ ضابطٍ من مجموعات المعرَّبات",
        threshold=Fraction(CONTROL_FLOOR),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دقّةَ المئين المدَّعاة؛ فدون مئةٍ تصير خطوةُ المئين أخشنَ من "
            "واحدٍ في المئة، ويُعلَن الرقمُ بخشونته لا بدقّةٍ مفترضة"
        ),
    ),
    Prediction(
        identifier="ج٣ التطابقُ الترديّ مزدوجٌ ويُنشَر بوجهيه",
        statistic="عددُ تشغيلات المطابقة المنشورة: تامٌّ (١↔١) ونطاقٌ (±١)",
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ النتيجةَ خبرٌ عن الظاهرة؛ فتشغيلةٌ واحدةٌ تُخفي حساسيّةَ "
            "الشاذّ التردّد ولا تُظهرها"
        ),
    ),
    Prediction(
        identifier="ج٤ الاتّجاهُ مكتوبٌ قبل العدد",
        statistic="عددُ الاتّجاهات المُعلَنة لقراءة المئين قبل رؤيته",
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قابليّةَ قراءة المئين؛ فمئينٌ عالٍ يعني أنّ الطولَ والندرةَ "
            "يكفيان، ومنخفضٌ بارزٌ يعني لافتًا — واتّجاهٌ يُختار بعد الرقم "
            "يقرأ كلَّ نتيجةٍ تأييدًا"
        ),
    ),
    Prediction(
        identifier="ج٥ إغلاقا التعداد",
        statistic="عددُ الإغلاقات المفحوصة: عددُ الصفوف، وبصمةُ إنتروبيا العمود",
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "سلامةَ العمود؛ فخللٌ في محوّلٍ خفيٍّ يمرّ بالعدّ وحدَه ولا يمرّ "
            "بإنتروبيا العمود مقابلةً بإنتروبيا المدوّنة"
        ),
    ),
    Prediction(
        identifier="ج٦ التعدادُ يُنشَر كاملًا لا وسيطًا",
        statistic="عددُ الدرجات المنشورة في ملفٍّ واحدٍ ببصمته",
        threshold=Fraction(ROWS),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قابليّةَ إعادة الحساب؛ فمن نشر قشرةَ التعداد دون نصِّه طلب " "التصديقَ لا الفحص"
        ),
    ),
    Prediction(
        identifier="ج٧ حدُّ الادّعاء مكتوبٌ في التسجيل",
        statistic="عددُ الأسئلة التي يجيب عنها التعدادُ من سؤالين مُسمَّيين",
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "لا شيءَ من النتيجة؛ وهو حدٌّ على القراءة: يجيب «أشاذّةٌ بين "
            "أقرانها؟» ولا يجيب «لماذا»، وطلبُ الماهيّة منه تجاوزٌ للسور"
        ),
    ),
)

CENSUS_SEAL = seal(CENSUS, PREDICTIONS)

SEALED_DIGEST = "6149704f0ceaa18e753fab50529ce3748d5701eb3d19984c47f5cc431eec7f98"

LOANS_IN_SCOPE = 5
TARIB_SEAL = "3a7ccdc9738738a5c482467313e2fd62acad31bd16a1e5be7c8d47737dbc322c"


def test_the_seal_is_stable_and_separate_from_the_first() -> None:
    """ختمٌ ثانٍ مستقلٌّ، ولم يُمَسّ الأوّلُ بحرف."""

    assert CENSUS_SEAL == SEALED_DIGEST
    assert len(CENSUS_SEAL) == 64
    assert CENSUS_SEAL == seal(CENSUS, PREDICTIONS)
    assert CENSUS_SEAL != TARIB_SEAL
    assert len(TARIB_SEAL) == 64  # والأوّلُ مذكورٌ ليُقابَل لا ليُعدَّل


def test_the_per_item_floor_is_finer_than_the_label_permutation_floor() -> None:
    """`1/|الضابط|` أدقُّ من ١/١٠؛ والملاحظةُ صحيحةٌ ويُعترَف بها بالحساب."""

    label_floor = label_permutation_floor(2, LOANS_IN_SCOPE)
    assert label_floor == Fraction(1, 10)

    per_item = Fraction(1, CONTROL_FLOOR)
    assert per_item < label_floor
    assert label_floor / per_item == 10

    # وجمعُ الخمسة يعطي مستوًى أدقَّ بكثيرٍ لو وقعوا كلُّهم دون المئين الخامس
    joint = Fraction(1, 20) ** LOANS_IN_SCOPE
    assert joint == Fraction(1, 3_200_000)
    assert joint < per_item

    # ومئينٌ واحدٌ شاذٌّ من خمسةٍ ليس خبرًا: احتمالُه صدفةً ٢٢٫٦٪
    at_least_one = 1 - Fraction(19, 20) ** LOANS_IN_SCOPE
    assert round(float(at_least_one), 3) == 0.226


def test_the_finer_floor_does_not_replace_the_sealed_contrast() -> None:
    """مطابقةُ الطول والتردّد لا تُزيل أنّ الدخيلَ دخل؛ فالمستويان يُنشَران معًا."""

    sealed_question = "أيفترق المصوغُ عن غير المصوغ داخلَ المعرَّبات؟"
    census_question = "أدرجةُ هذا المعرَّب شاذّةٌ بين أقرانه في الطول والتردّد؟"
    assert sealed_question != census_question

    confounded = "الدخولُ مشترَكٌ بين المعرَّب والأصيل، فمقارنتُهما تخلطه بالصياغة"
    assert "تخلطه بالصياغة" in confounded

    # وأرضيّةُ المبادلات المسجَّلةُ باقيةٌ كما هي، ولم تُمَسّ بهذا الختم
    assert permutation_floor(REPLICATES) == Fraction(1, 2_001)


def test_the_claim_limit_runs_the_other_way() -> None:
    """ج٧ اتّجاهُه «لا يجاوز»: سؤالٌ واحدٌ يُجاب، والثاني تجاوز."""

    limit = PREDICTIONS[6]
    assert limit.direction is Direction.AT_MOST
    assert limit.verdict(Fraction(1)) is Verdict.MET
    assert limit.verdict(Fraction(2)) is Verdict.FALSIFIED
    assert "ولا يجيب «لماذا»" in limit.falsifies


def test_the_family_is_seven_and_each_name_is_distinct() -> None:
    """سبعةُ بنودٍ مُعلَنةٌ قبل العدّ، ولا اسمَ يتكرّر."""

    assert FAMILY == len(PREDICTIONS) == 7
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    assert {one.identifier[:2] for one in PREDICTIONS} == {
        "ج١",
        "ج٢",
        "ج٣",
        "ج٤",
        "ج٥",
        "ج٦",
        "ج٧",
    }


def test_the_scores_are_declared_in_sample_and_therefore_descriptive() -> None:
    """النموذجُ داخلَ العينة مكتوبٌ في الأوراكل، فالدرجاتُ وصفٌ لا استدلال."""

    assert "داخلَ العينة" in CENSUS.extraction
    assert "وصفٌ لا استدلال" in CENSUS.extraction
    assert "بتٌّ للفظ" in CENSUS.extraction
