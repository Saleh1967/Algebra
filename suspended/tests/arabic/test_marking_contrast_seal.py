"""**ختمٌ قبل النظر**: ذراعان بعمقٍ واحد — تصحيحُ عزلٍ لم يكن عزلًا.

**لم يُشغَّل شيءٌ على المدوّنة بعد.** والآلةُ جُرّبت على شريحةٍ من ثمانين
سطرًا، **وفيها جاء ذراعُ الوسم الأبديّ أرخصَ بـ١٥٧ بتًّا** — ويُعلَن ذلك
ههنا، فما رأيتُه قبل الختم لا يُخفى. **ولا يُستخرَج من شريحةٍ بهذا الصغر
شيءٌ عن أرقام المدوّنة.**

**العطلُ الذي يُصلَح**: ختمُ `89b59b10…` نصَّ على «التغييرٌ واحدٌ لا غير»،
**وكان فيه متغيّران**: رفعُ الوسم **وحدُّ عمق البحث** (٢٤ في كلّ حال)،
بينما ذراعُ `69a1c10c…` لم يكن محدودَ العمق في الحال الواحدة. فالمقابلةُ
التي نُشِرت **ملتبسةٌ بمتغيّرين**، ولا يصحّ نسبُ الفرق إلى الوسم وحدَه.
وهذا خللٌ في تصميمي، مكتوبٌ في `docs/سجل-الأعطال.md`.

**فالذراعان ههنا في آلةٍ واحدةٍ وتشغيلٍ واحدٍ وعمقٍ واحد**، ولا يختلفان
إلّا في شيءٍ واحد: **أيبقى وسمُ المرفوض أم يُرفَع عند كلّ التزام**.

**وعمقُ البحث محدودٌ معلنٌ**: فما يُبلَغ **حدٌّ أدنى** لا أعلى، وصفرٌ ههنا
يُقرأ «لم يُبلَغ» لا «ممتنع».

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ وعَرضٌ ووقوعاتٌ وتكلفةٌ فقط.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

BY_BLOCK = 1_394_638
BY_LIFTED = 1_416_789
BY_LASTING_UNBOUNDED = 1_400_392
COMMITS_UNBOUNDED = 2_662

ORACLE = Oracle(
    name="ذراعا الوسم بعمقٍ واحد — الأبديُّ والمؤقّت",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "تشغيلٌ واحدٌ فيه ذراعان من نقطة الصفر نفسِها بآلة `69a1c10c…` "
        "وعمقِ بحثٍ واحدٍ (أعلى ٢٤ مقترَحًا متاحًا في كلّ حال) ووقوفٍ "
        "واحد (حالٌ لا يربح فيها واحدٌ منها)؛ والفرقُ الوحيد أنّ وسمَ "
        "المرفوض يبقى في ذراعٍ ويُرفَع عند كلّ التزامٍ في الآخر"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ع١",
        statistic="أقصى |الجملة من العدّادات − الجملة من الآيات| في الذراعين (بتًّا)",
        threshold=Fraction(1, 1000),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ لا المادّة: انحرافُ العدّادات يردّ الذراعين معًا",
    ),
    Prediction(
        identifier="ع٢",
        statistic="أكبرُ عددِ مواضعِ الخلاف بين بسطِ الرموز ومجرى L₀ في الذراعين",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الرجعةَ: أيُّ خلافٍ في أيّ ذراعٍ ضياعٌ لا ضغط",
    ),
    Prediction(
        identifier="ع٣",
        statistic="مجموعُ الالتزامات التي لم تنزل عندها التكلفةُ في الذراعين",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="أنّ الرخصةَ بقيت للدمجة الواحدة في الذراعين جميعًا",
    ),
    Prediction(
        identifier="ع٤",
        statistic="جملةُ ذراع المؤقّت − جملةُ ذراع الأبديّ (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ المصحَّحة أنّ الوسمَ الأبديَّ **لم يكن** سببَ الخسارة، "
            "وأنّ رفعَه لا ينفع بل يضرّ عند عمقٍ واحد. فإن جاء المؤقّتُ "
            "أرخصَ فدعوايَ الأولى — أنّ الوسمَ الأبديَّ يكلّف — تعود صحيحةً، "
            "ويكون الالتباسُ بالعمق هو الذي أخفاها"
        ),
    ),
    Prediction(
        identifier="ع٥",
        statistic="أدنى جملةٍ في الذراعين (بتًّا)",
        threshold=Fraction(BY_BLOCK + 1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى أنّ الترخيصَ بتّةً بتّة لا يبلغ الكتليَّ بأيّ وسم؛ فإن "
            "بلغه ذراعٌ فالخسارةُ من الوسم أو العمق لا من الترخيص، "
            "وتُعاد قراءةُ `69a1c10c…` كلِّها"
        ),
    ),
    Prediction(
        identifier="ع٦",
        statistic="عددُ التزامات ذراع الأبديّ",
        threshold=Fraction(COMMITS_UNBOUNDED - 1),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ حدَّ العمق يعضّ فعلًا: فإن بلغ ذراعُ الأبديِّ ٢٬٦٦٢ أو "
            "جاوزها فالعمقُ ٢٤ لم يكن قيدًا، ويسقط وجهُ الالتباس الذي "
            "أُصلِح ههنا — ويُنشَر ذلك"
        ),
    ),
    Prediction(
        identifier="ع٧",
        statistic="|جملةُ ذراع المؤقّت − جملةِ تشغيل `89b59b10…`| (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "إعادةَ الإنتاج: الذراعُ المؤقّتُ ههنا هو تشغيلُ `89b59b10…` "
            "بقاعدته نفسِها وعمقِه نفسِه، فاختلافُ بتٍّ واحدٍ عطلُ آلةٍ "
            "يردّ المقابلةَ كلَّها"
        ),
    ),
)

DIGEST = "2cd80c0f3b37c3dd23c466cd237a8594b0a5622ff915e8b3de16901d58846a50"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_two_arms_differ_in_exactly_one_thing_this_time() -> None:
    """وهو ما لم يتحقّق في `89b59b10…` — والعطلُ مُعلَنٌ في الوثيقة."""

    assert "الفرقُ الوحيد" in ORACLE.extraction
    assert "عمقِ بحثٍ واحدٍ" in ORACLE.extraction
    assert "متغيّران" in __doc__ and "خللٌ في تصميمي" in __doc__
    assert len(PREDICTIONS) == 7


def test_the_contrast_carries_a_reproduction_check() -> None:
    """ع٧: الذراعُ المؤقّتُ يجب أن يعيد رقمَ `89b59b10…` بتًّا بتًّا."""

    same = next(one for one in PREDICTIONS if one.identifier == "ع٧")
    assert same.threshold == Fraction(0)
    assert str(BY_LIFTED) == "1416789"


def test_the_crux_can_restore_my_first_claim_or_bury_it() -> None:
    """ع٤ يحتمل الوجهين، ومكتوبٌ ما يعنيه كلُّ وجه."""

    crux = next(one for one in PREDICTIONS if one.identifier == "ع٤")
    assert crux.direction is Direction.AT_LEAST
    assert "تعود صحيحةً" in crux.falsifies
    assert BY_LASTING_UNBOUNDED < BY_LIFTED  # وهو ما قِيس بعمقين مختلفين
