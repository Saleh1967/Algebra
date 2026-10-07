"""تدقيقُ المخطّط قبل القياس: تقسيمٌ تامٌّ يُفحَص، وتعارضٌ يُصنَّف لا يُدمَج.

**ما ههنا**: أوّلُ منتجات الهندسة العكسيّة ليس رقمًا بل فحصَ المخطّط الذي
ستُقاس عليه. ولا مدوّنةَ تُقرَأ: تُفحَص **بنيةُ الجداول** لا مضمونُها في نصّ.

`THE_CLASSICAL_SCHEME_IS_ALREADY_A_TOTAL_PARTITION`: وأحكامُ النون الساكنة
تقسيمٌ تامٌّ للأبجديّة بلا بقيّة: ٦ + ٤ + ٢ + ١ + ١٥ = ٢٨. فهي **قابلةٌ
للمقارنة كتقسيم** لا كأزواجٍ متفرّقة، وذلك يجعل «أتُستخرَج من العدّ؟» سؤالًا
له جوابٌ واحدٌ لا خمسة أجوبةٍ منفصلة. ومقارنةُ تقسيمٍ بتقسيمٍ غيرُ مقارنةِ
حرفٍ بحرف.

`A_LETTER_IN_TWO_GROUPS_IS_NOT_ALWAYS_A_CONTRADICTION`: وحرفٌ يظهر في
مجموعتين قد يكون تعارضًا، وقد يكون **محورين مدمجين في عمودٍ واحد**: تسميةٌ
بالمخرج التشريحيّ وتسميةٌ بالتصنيف المدرسيّ، جُمِعتا في حقلٍ واحدٍ بلا إعلان.
والعلاجُ مختلف: التعارضُ يُفصَل بندين ويُحسَم أحدُهما، والمحوران يُعلَن
محورُهما في كلّ صفّ فيزول الظاهرُ من غير حذفِ صفّ. والخلطُ بينهما يُسقِط
صفًّا صحيحًا باسم التناقض.

`A_CONTRADICTION_I_CANNOT_SEE_IS_UNRUN_NOT_CONFIRMED`: ومن التعارضات
المبلَّغة ما لا أملك ملفَّه فلا أُصدِّقه ولا أُكذِّبه — منزلتُه
`Vacancy.UNRUN`. وواحدٌ منها **لا يقوم بصيغته**: «الهاءُ حلقيّةٌ بلا حكمٍ
حلقيّ» — والهاءُ من حروف الإظهار الحلقيّ الستّة (ء هـ ع ح غ خ) في التقسيم
نفسِه الذي يُقاس عليه. فإن خلا منها جدولُ الملفّ فذلك **نقصٌ في الجدول**
يُصلَح، لا تعارضٌ في المخطّط يُسجَّل.
"""

from __future__ import annotations

from algebra.reconciliation import Partition
from algebra.results import Vacancy

ALPHABET = 28

# أحكامُ النون الساكنة: تقسيمٌ مُعلَنٌ للأبجديّة كلِّها
IZHAR = ("ء", "ه", "ع", "ح", "غ", "خ")
IDGHAM_WITH_GHUNNA = ("ي", "ن", "م", "و")
IDGHAM_WITHOUT = ("ل", "ر")
IQLAB = ("ب",)
HIDDEN = ALPHABET - (
    len(IZHAR) + len(IDGHAM_WITH_GHUNNA) + len(IDGHAM_WITHOUT) + len(IQLAB)
)

# (الموضعُ المبلَّغ، جنسُ العطل، أيمكن الفحصُ ههنا؟)
REPORTED: tuple[tuple[str, str, bool], ...] = (
    ("الظاءُ في اللثويّة والسنانيّة معًا", "محوران مدمجان", True),
    ("الهاءُ حلقيّةٌ بلا حكمٍ حلقيّ", "نقصٌ في جدولٍ لا تعارضٌ في مخطّط", True),
    ("صفاتُ الحروف بترتيبين", "ترتيبٌ لم يُعلَن", True),
)


def test_the_five_rulings_partition_the_alphabet_without_residue() -> None:
    """٦ + ٤ + ٢ + ١ + ١٥ = ٢٨ — تقسيمٌ تامٌّ يُقارَن كتقسيم."""

    parts = (
        len(IZHAR),
        len(IDGHAM_WITH_GHUNNA),
        len(IDGHAM_WITHOUT),
        len(IQLAB),
        HIDDEN,
    )
    assert parts == (6, 4, 2, 1, 15)
    assert Partition(parts=parts, declared_total=ALPHABET).residue == 0

    named = set(IZHAR) | set(IDGHAM_WITH_GHUNNA) | set(IDGHAM_WITHOUT) | set(IQLAB)
    assert len(named) == 13  # ولا حرفَ يُعَدّ في حكمين
    assert ALPHABET - len(named) == HIDDEN


def test_the_letter_said_to_lack_its_ruling_is_inside_the_ruling() -> None:
    """الهاءُ من الستّة؛ فالمبلَّغُ نقصُ جدولٍ لا تعارضُ مخطّط."""

    assert "ه" in IZHAR
    assert len(IZHAR) == 6

    reported = {name: kind for name, kind, _ in REPORTED}
    assert reported["الهاءُ حلقيّةٌ بلا حكمٍ حلقيّ"].startswith("نقصٌ في جدول")


def test_two_taxonomies_in_one_column_are_not_a_contradiction() -> None:
    """محوران مدمجان يُعلَن محورُهما، ولا يُحذَف صفٌّ صحيحٌ باسم التناقض."""

    kinds = {kind for _, kind, _ in REPORTED}
    assert "محوران مدمجان" in kinds
    assert len(REPORTED) == len(kinds) == 3  # ثلاثةُ مواضعَ وثلاثةُ أجناسٍ مختلفة

    remedy = {
        "محوران مدمجان": "يُعلَن المحورُ في كلّ صفّ",
        "ترتيبٌ لم يُعلَن": "يُعلَن الترتيبُ أو يُعَدّ مجموعةً لا متوالية",
        "نقصٌ في جدولٍ لا تعارضٌ في مخطّط": "يُكمَل الصفُّ الناقص",
    }
    assert set(remedy) == kinds
    assert "يُحذَف" not in " ".join(remedy.values())


def test_what_cannot_be_read_here_is_unrun_not_denied() -> None:
    """ما لا يُفتَح ملفُّه لا يُصدَّق ولا يُكذَّب: منزلتُه «لم يُجرَ»."""

    assert Vacancy.UNRUN.value == "فحصُها مُعيَّنٌ ولم يُجرَ"
    assert Vacancy.UNRUN is not Vacancy.REFUSED
    assert Vacancy.UNRUN is not Vacancy.UNATTESTED

    # والمفحوصُ ههنا بنيةُ المخطّط لا مضمونُ ملفٍّ بعينه
    checkable = [name for name, _, here in REPORTED if here]
    assert len(checkable) == 3
