"""فُحِص المرشَّحُ بمعيار التماسك — فخرج **عكسَ المتوقَّع**: G5 تتماسك، وG1 لا.

**ما قِيس** (وصفٌ مُعلَنٌ خارجَ كلّ ختم): لكلّ مجموعةٍ من مجموعات المرشَّح
متوسّطُ تشابه صفوف الانتقال داخلَها، ومئينُه **بين مجموعاتٍ عشوائيّةٍ من
حجمها نفسِه** (ألفا سحبة). فالمقارنةُ مضبوطةٌ بالحجم، إذ متوسّطُ التشابه
يرتفع بصغر المجموعة.

`THE_CAGE_IS_THE_MOST_COHERENT_GROUP_NOT_THE_LEAST`: قيل إنّ G5 «تماسكُها
ضعيفٌ مقصودًا للعدد» — إذ تجمع ق ك مع ب م و. والمقيسُ خلافُ ذلك: مئينُها
**٠٫٩٩٤ داخلَ الكلمة، و٠٫٩٨٣ عابرًا، و٠٫٩٩٨ بالضبط**. أي أنّها أشدُّ تماسكًا
من نحو تسعٍ وتسعين من مئةِ مجموعةٍ عشوائيّةٍ بحجمها.

`AND_THE_THROAT_IS_THE_LEAST_COHERENT_GROUP`: وG1 — أوضحُ المجموعات هُويّةً
نطقيّةً — مئينُها **٠٫٠٦٤ و٠٫٠٠٤ و٠٫٠٠٦**. فحروفُ الحلق **أشدُّ تباعدًا في
فضاء التعاقب** من أكثر المجموعات العشوائيّة بحجمها. فلو كان المعيارُ
تماسكًا لكان الساقطُ G1 لا G5.

`WHAT_THIS_DOES_NOT_YET_SHOW`: وصفريُّ الحجم يضبط الحجمَ **ولا يضبط
التردّد**. وG5 مجموعةُ «الباقي» تغلب عليها حروفٌ متوسّطةُ الشيوع، وG1 فيها
الألفُ الحاملةُ للهمزة وهي من أشيع الرموز وأشذِّها توزيعًا. فقد يكون
المقيسُ **شيوعًا لا مخرجًا**. والحاسمُ صفريٌّ مطابقٌ في التردّد، ولم يُجرَ
بعد — فيُسجَّل مفتوحًا ولا يُفسَّر.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
CORPUS = REPOSITORY / "corpora" / "quran-simple-enhanced.txt"

pytestmark = pytest.mark.skipif(
    not CORPUS.is_file(),
    reason="بايتاتُ المدوّنة المُجمَّدة غيرُ مستقبَلةٍ في هذه الشجرة",
)

# (المجموعة، الحجم، أزواجُ القياس، مئينُها: داخلَ الكلمة · عابرًا · بالضبط)
MEASURED: tuple[tuple[str, int, int, Fraction, Fraction, Fraction], ...] = (
    ("G1 حلق", 6, 15, Fraction(64, 1000), Fraction(4, 1000), Fraction(6, 1000)),
    ("G2 جاحظيّة", 4, 6, Fraction(526, 1000), Fraction(419, 1000), Fraction(331, 1000)),
    ("G3 طرفيّة", 2, 1, Fraction(908, 1000), Fraction(900, 1000), Fraction(890, 1000)),
    (
        "G5 الباقي",
        15,
        105,
        Fraction(994, 1000),
        Fraction(983, 1000),
        Fraction(998, 1000),
    ),
)
DRAWS = 2_000


def test_the_group_called_a_cage_is_the_most_coherent_of_all() -> None:
    """G5 فوق ٠٫٩٨ في السياسات الثلاث — فليست قفصًا بلا تماسك."""

    name, _, _, within, across, dabt = MEASURED[3]
    assert name.startswith("G5")
    for value in (within, across, dabt):
        assert value > Fraction(98, 100)


def test_the_throat_group_is_the_least_coherent_of_all() -> None:
    """G1 دون ٠٫٠٧ في الثلاث، ودون ٠٫٠١ في اثنتين — أشدُّ تباعدًا لا تماسكًا."""

    name, _, _, within, across, dabt = MEASURED[0]
    assert name.startswith("G1")
    assert within < Fraction(7, 100)
    assert across < Fraction(1, 100) and dabt < Fraction(1, 100)

    # ولو كان المعيارُ تماسكًا لكان الساقطُ G1 لا G5
    assert MEASURED[0][3] < MEASURED[3][3]


def test_the_ordering_is_the_same_under_all_three_row_policies() -> None:
    """الترتيبُ نفسُه في السياسات الثلاث، فليس أثرَ سياسةٍ بعينها."""

    for column in (3, 4, 5):
        ordered = sorted(MEASURED, key=lambda row: row[column])
        assert ordered[0][0].startswith("G1")
        assert ordered[-1][0].startswith("G5")


def test_the_size_matched_null_controls_size_and_not_frequency() -> None:
    """الصفريُّ يضبط الحجمَ وحدَه؛ فالتردّدُ يبقى تفسيرًا مفتوحًا لا مردودًا."""

    assert DRAWS == 2_000
    sizes = {name: size for name, size, _, _, _, _ in MEASURED}
    assert sizes["G5 الباقي"] == 15 and sizes["G1 حلق"] == 6
    # وأزواجُ القياس تتبع الحجمَ لا التماسك، فتُطبَع معه
    for _, size, pairs, *_ in MEASURED:
        assert pairs == size * (size - 1) // 2

    open_control = "صفريٌّ مطابقٌ في التردّد — لم يُجرَ بعد"
    assert "لم يُجرَ" in open_control


def test_the_singleton_group_is_excluded_and_counted() -> None:
    """G4 حرفٌ واحد: لا تشابهَ داخلَها يُقاس، فتخرج معدودةً لا مطويّة."""

    assert len(MEASURED) == 4  # من خمسٍ، والخامسةُ مفردة
    assert all(size >= 2 for _, size, _, _, _, _ in MEASURED)
