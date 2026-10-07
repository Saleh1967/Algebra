"""**ختمٌ قبل النظر**: الترخيصُ الجشع **بتّةً بتّة** لا كتلةً.

**لم يُشغَّل شيءٌ على المدوّنة بعد.** والآلةُ وحدَها جُرّبت على شريحةٍ من
ثمانين سطرًا للتحقّق من سلامتها (انحرافُ الآلتين صفرٌ، والرجعةُ صفرٌ)،
**ولا يُستخرَج من شريحةٍ بهذا الصغر شيءٌ عن أرقام المدوّنة**.

**النقصُ الذي يُكمَّل**: في `34133d54…` مُنِحت الرخصةُ **كلَّ خمس مئةِ
دمجة**. فالكتلةُ الرابحةُ تمرّ بما فيها من خاسر، والخاسرةُ تُردّ بما فيها
من رابح. و«لا يبقى بتٌّ إلّا ليسهم بإفادة» **لا يتحقّق بكتلة**.

**فالرخصةُ للدمجة الواحدة**: تُقاس التكلفةُ **المحجوزة** قبلها وبعدها،
فإن نزلت التُزِمت، وإن لم تنزل **رُفِضت ووُسِمت ولم تُعَد** — تُعَدّ ولا
تُبتلَع.

**والوقوفُ مختومٌ سلفًا**: خمسُ مئةِ رفضٍ متوالية، أو ثلاثون ألفَ اقتراح،
أو نفادُ الأزواج — وأيُّها بلغ أوّلًا يُسمّى في السجلّ؛ فإن بلغ السقفُ
أوّلًا صُنِّف الوقوفُ `UNREACHABLE` ولم يُدَّعَ تمامٌ.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ وعَرضٌ ووقوعاتٌ وتكلفةٌ فقط.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="الترخيصُ الجشع بتّةً بتّة فوق ١١٢",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "من ١١٢ صعودًا: يُقترَح الزوجُ الأكثرُ وقوعًا، وتُقاس التكلفةُ "
        "المحجوزة (معجمٌ مهجًّى بـ١١٢ + بيانٌ بطولِ شفرة هوفمان، شطرًا "
        "بشطر على الشفع والوتر) قبل الدمجة وبعدها؛ فتُلتزَم إن نزلت "
        "وتُرفَض وتُوسَم إن لم تنزل. والعدّاداتُ تُقابَل بآلة `34133d54…` "
        "كلَّ خمس مئةِ التزامٍ فلا تنفرد آلةٌ برقم"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ر١",
        statistic=("أقصى |الجملة من العدّادات − الجملة من الآيات| عند نقاط الفحص (بتًّا)"),
        threshold=Fraction(1, 1000),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ لا المادّة: العدّاداتُ اختصارُ حسابٍ لا تعريفٌ جديد، "
            "فانحرافُها عن الحساب من الآيات يردّ التشغيلَ كلَّه"
        ),
    ),
    Prediction(
        identifier="ر٢",
        statistic="مواضعُ الخلاف بين بسطِ الرموز بالهجاء ومجرى L₀",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الرجعةَ: كلُّ رمزٍ مُلتزَمٍ مهجًّى بوحدات ١١٢، فبسطُه يجب أن "
            "يعيد المجرى بلا بقيّةٍ ولا زيادة؛ وأيُّ خلافٍ ضياعٌ لا ضغط"
        ),
    ),
    Prediction(
        identifier="ر٣",
        statistic="عددُ الالتزامات التي لم تنزل عندها التكلفةُ المحجوزة",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "معنى الترخيص بتّةً بتّة: التزامٌ واحدٌ بلا نزولٍ يعيد الرخصةَ "
            "كتلةً، ويُبطِل القولَ إنّ كلَّ باقٍ يسهم بإفادة"
        ),
    ),
    Prediction(
        identifier="ر٤",
        statistic="عددُ الالتزامات عند الوقوف",
        threshold=Fraction(4501),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الوقوفَ الكتليَّ عند ٤٬٥٠٠ ردَّ دمجاتٍ رابحةً مع "
            "الخاسرة؛ فإن لم يتجاوزها الترخيصُ بتّةً بتّة فالكتلةُ لم "
            "تُخفِ ربحًا، ويُنشَر ذلك"
        ),
    ),
    Prediction(
        identifier="ر٥",
        statistic="عددُ الالتزامات قبل أوّل رفض",
        threshold=Fraction(4500),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ الرفضَ متخلّلٌ لا ذيلٌ خالص؛ فإن لم يقع رفضٌ قبل "
            "٤٬٥٠٠ التزامٍ فالكتلةُ لم تمرّر خاسرًا، وتسقط نصفُ حجّتي "
            "في نقد الوقوف الكتليّ"
        ),
    ),
    Prediction(
        identifier="ر٦",
        statistic="نسبةُ التكلفة المحجوزة عند الوقوف إلى تكلفة L₀",
        threshold=Fraction(682, 1000),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوى أنّ الترخيصَ بتّةً بتّة لا يخسر عن الكتليّ (٠٫٦٨٢١)؛ "
            "فإن علا فالرفضُ المبكّرُ حرفَ المسارَ إلى أسوأ، وهذا حدٌّ "
            "على الجشع لا على المادّة"
        ),
    ),
    Prediction(
        identifier="ر٧",
        statistic="نصيبُ الوقوعات التي لا تعبر الفراغَ عند الوقوف",
        threshold=Fraction(8379, 10000),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ الرخصةَ لا تحفظ الفراغ: الضغطُ يُشترى بعبورٍ "
            "أكثر. فإن ارتفع النصيبُ فالترخيصُ يشتري الضغطَ والفراغَ "
            "معًا، وهو أقوى ممّا ادّعيت"
        ),
    ),
)

DIGEST = "69a1c10c3c8d09f08e19483deb50896b07831dc169ff7a79cb64d05a5324fb04"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_two_conditions_are_machine_checks_and_must_be_zero() -> None:
    """ر١ ور٢ لا يقولان عن المادّة شيئًا — وسقوطُهما يردّ التشغيل."""

    machine = [one for one in PREDICTIONS if one.identifier in {"ر١", "ر٢"}]
    assert len(machine) == 2
    for one in machine:
        assert one.direction is Direction.AT_MOST
        assert one.threshold <= Fraction(1, 1000)


def test_the_licence_is_per_merge_not_per_block() -> None:
    """ر٣ هو معنى «بتّةً بتّة» — وبدونه تعود الرخصةُ كتلة."""

    single = next(one for one in PREDICTIONS if one.identifier == "ر٣")
    assert single.threshold == Fraction(0)
    assert "كتلةً" in single.falsifies
    assert len(PREDICTIONS) == 7


def test_two_conditions_face_opposite_ways_on_the_block_stop() -> None:
    """ر٤ يدّعي تجاوزَ ٤٬٥٠٠، ور٥ يدّعي رفضًا قبلها — وهما مستقلّان."""

    more = next(one for one in PREDICTIONS if one.identifier == "ر٤")
    early = next(one for one in PREDICTIONS if one.identifier == "ر٥")
    assert more.direction is Direction.AT_LEAST
    assert early.direction is Direction.AT_MOST
    assert more.threshold == Fraction(4501)
    assert early.threshold == Fraction(4500)
