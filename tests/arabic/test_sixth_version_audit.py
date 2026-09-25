"""النسخةُ ٦: **الخاناتُ أربعٌ والأسرُ أكثر** — والثلاثيُّ المتطابقُ يصمد.

**لا مرفقَ ورد**؛ والمقيسُ هو المنقول، **وشواهدُه من بايتات المدوّنة**.

`A_STRUCK_LAW_LEFT_VISIBLE_IS_THE_BEST_MOVE_IN_THE_SERIES`: ويُقرّ أوّلًا:
شطبُ F13 **مُعلَّمًا لا ممحوًّا** («سجلُّ العطل جزءٌ من الوثيقة») هو أقوى
حركةٍ منهجيّةٍ وردت في هذه السلسلة. الممحوُّ لا يُحاسَب، والمعلَّمُ يُحاسَب
— وهو ما يجعل النصَّ قابلًا للتاريخ كما يُقرأ سجلُّ الالتزامات.

`AND_THE_TRIPLE_IS_CONFIRMED_ON_LEXICALLY_IDENTICAL_MATERIAL`: وأقوى ما في
النسخة يأتي من خارجها: ثلاثُ خاناتٍ تتحقّق في المدوّنة على **مادّةٍ لفظيّةٍ
واحدة** — «**واللهُ غفورٌ رحيمٌ**» (١٣)، «**وكان اللهُ غفورًا رحيمًا**» (٩)،
«**إنّ اللهَ غفورٌ رحيمٌ**» (٢٠). حاملٌ واحدٌ وحالةٌ واحدةٌ وثلاثةُ نواسخ
وثلاثُ خانات، ٤٢ شاهدًا — **مقارنةٌ مضبوطةُ المادّة**، وهي أمتنُ دليلٍ نالته
الأطروحة.

`BUT_THE_FOURTH_CELL_BREAKS_THE_FRAME`: والخانةُ الرابعةُ **لا تُملأ بهذه
المادّة**: «ظننتُ اللهَ غفورًا» ليست من الباب. فالثلاثُ الأولى نواسخُ تدخل
على **جملةٍ اسميّة**، والرابعةُ **فعلٌ متعدٍّ إلى مفعولين** — عمليّتان لا
عمليّةٌ واحدة، والجدولُ يضمّهما تحت «انقل إلى النصب» بلا إعلان.

`AND_A_DOUBLE_ACCUSATIVE_NEED_CARRY_NO_NISBA`: و«ظنّ تحمل النسبةَ كلَّها
اعتقادًا، ولهذا مفعولان» تفسيرٌ **لا يميّز**: «**وآتينا داوودَ زبورًا**»
منصوبان **ولا نسبةَ بينهما**. فالنصبُ المزدوجُ خاصّيةُ **تعدٍّ**، والاعتقادُ
تفسيرٌ زائدٌ يعطي ما يعطيه المنافسُ الأبسط.

`THE_CELL_OF_KAD_IS_NOT_OBSERVABLE_ON_THE_SURFACE`: و«كاد» تُوضَع في خانة
{حالة} بعبارة «**أو في محلّ نصب**» — وهذا مفتاحُ العطل: «**يكادُ البرقُ
يخطفُ أبصارهم**» علامتاه **رفعٌ ورفع**. فعلى المرصود وحدَه تقع كادُ في خانة
«لا ناسخ»، ونقلُها يحتاج **موضعًا مقدَّرًا بلا علامة**. فالجدولُ يخلط صفوفًا
مقيسةً بصفٍّ مفترض — عطلُ الوحدات في صورته الخامسة.

`FOUR_IS_PRESERVED_BY_SUBSTITUTION_NOT_BY_DERIVATION`: و«٤» في هذا الجدول
**ليست ٤ في Q7**: هناك أربعةُ نواسخَ (كان، كاد، إنّ، ظنّ)، وهنا **كادُ
مضمومةٌ إلى كان** و«**لا ناسخ**» مضافٌ صفًّا — تغييران يُبقيان المجموعَ ٤.
وهي بعينها بنيةُ «٦٥ بخطأين يتقاصّان»: رقمٌ يثبت لأنّ تعديلين تعادلا. و«لا
ناسخ» **ليست أسرةً من النواسخ** أصلًا.

`AND_THE_POWER_SET_BOUNDS_THE_CELLS_IT_DOES_NOT_COUNT_THE_FAMILIES`: و٢²
تعطي **حدًّا أعلى للخانات**، لا عددًا للأسر ولا برهانًا على امتلائها.
والأسرُ أكثرُ من أربع، ومن المدوّنة: «**ما هذا بشرًا**» — ما الحجازيّةُ
أسرةٌ خامسةٌ تسكن خانةَ كان؛ و«**لا ريبَ فيه**» — لا النافيةُ للجنس أسرةٌ
سادسةٌ **لا خانةَ لها**: اسمُها **مبنيٌّ على الفتح لا منصوب**، وقيمةٌ ثالثةٌ
خارج {رفع، نصب}. فحصرُ القيم في اثنتين **فرضٌ صامتٌ خامس** — في الوثيقة
التي تُعلن حراستَها من الرابع.

`AND_THE_RESTATED_BALANCE_IS_AN_IDENTITY`: و«الناسخُ يأخذ من حريّة المواضع
**بقدر ما ينصب**» لا ناقضَ لها: «الحرّ» مُعرَّفٌ بأنّه «غيرُ المنصوب».
فالعبارةُ «عددُ المنصوبات = عددُ المنصوبات» — و«٤ = ٤» في صورتها الثانية.
"""

from __future__ import annotations

import re
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

MARKS = re.compile(r"[ً-ْٰـ]")

CELLS: dict[str, tuple[str, str]] = {
    "لا ناسخ": ("رفع", "رفع"),
    "كان/كاد": ("رفع", "نصب"),
    "إنّ": ("نصب", "رفع"),
    "ظنّ": ("نصب", "نصب"),
}
MATCHED_FRAME: dict[str, str] = {
    "لا ناسخ": "والله غفور رحيم",
    "كان/كاد": "وكان الله غفورا رحيما",
    "إنّ": "إن الله غفور رحيم",
}
Q7_FAMILIES = ("كان", "كاد", "إنّ", "ظنّ")
MORE_FAMILIES = ("ما الحجازية", "لا النافية للجنس")


def _bare() -> list[str]:
    return [
        MARKS.sub("", line) for line in CORPUS.read_text(encoding="utf-8").splitlines()
    ]


def _attested(needle: str) -> int:
    return sum(1 for line in _bare() if needle in line)


def test_the_four_cells_exhaust_the_pair_under_two_values_only() -> None:
    """٢² = ٤ حدٌّ أعلى مشروطٌ بقيمتين — وعددُ القيم هو الفرضُ الصامت."""

    assert len(CELLS) == 4 == 2**2
    assert set(CELLS.values()) == {
        (carrier, state) for carrier in ("رفع", "نصب") for state in ("رفع", "نصب")
    }
    # ولو دخلت قيمةٌ ثالثةٌ (البناء) لصارت الخاناتُ تسعًا
    assert 3**2 == 9 != len(CELLS)


def test_the_four_of_this_table_is_not_the_four_of_the_census() -> None:
    """كادُ ضُمّت وصفُّ «لا ناسخ» أُضيف — تعديلان يُبقيان المجموعَ أربعة."""

    assert len(Q7_FAMILIES) == 4
    merged = {"كان", "كاد"}
    assert merged <= set(Q7_FAMILIES)
    families_left = len(Q7_FAMILIES) - (len(merged) - 1)
    assert families_left == 3  # والرابعُ صفٌّ ليس أسرة
    assert families_left + 1 == len(CELLS)
    assert "لا ناسخ" in CELLS and "لا ناسخ" not in Q7_FAMILIES


def test_the_balance_as_restated_has_no_falsifier() -> None:
    """«يأخذ بقدر ما ينصب» — والحرُّ مُعرَّفٌ بغير المنصوب، فهي هويّة."""

    for positions in CELLS.values():
        accusatives = sum(1 for one in positions if one == "نصب")
        free = sum(1 for one in positions if one != "نصب")
        assert accusatives + free == 2  # يصدق في كلّ خانةٍ بلا استثناء
        assert accusatives == 2 - free


@requires_corpus
def test_three_cells_are_confirmed_on_one_lexical_frame() -> None:
    """حاملٌ واحدٌ وحالةٌ واحدةٌ وثلاثُ خانات — مقارنةٌ مضبوطةُ المادّة."""

    counts = {cell: _attested(text) for cell, text in MATCHED_FRAME.items()}
    assert counts == {"لا ناسخ": 13, "كان/كاد": 9, "إنّ": 20}
    assert sum(counts.values()) == 42
    assert all(number > 0 for number in counts.values())
    assert len(MATCHED_FRAME) == 3 < len(CELLS)  # والرابعةُ لا تُملأ بهذه المادّة


@requires_corpus
def test_the_fourth_cell_is_a_different_operation() -> None:
    """منصوبان بلا نسبة: «وآتينا داوودَ زبورًا» — فالتعدّي يكفي تفسيرًا."""

    assert _attested("ولا تحسبن الذين قتلوا في سبيل الله أمواتا") == 1
    assert _attested("وآتينا داوود زبورا") == 2  # مفعولان ولا نسبةَ بينهما
    assert _attested("وعلمناه صنعة لبوس") == 1
    assert CELLS["ظنّ"] == ("نصب", "نصب")


@requires_corpus
def test_the_cell_of_kad_has_no_surface_mark() -> None:
    """«يكادُ البرقُ يخطفُ» — رفعٌ ورفع، فموضعُها مقدَّرٌ لا مرصود."""

    assert _attested("يكاد البرق يخطف أبصارهم") == 1
    observed = ("رفع", "رفع")
    assert observed == CELLS["لا ناسخ"] != CELLS["كان/كاد"]


@requires_corpus
def test_more_families_are_attested_than_the_table_counts() -> None:
    """«ما هذا بشرًا» خامسةٌ تسكن خانةَ كان، و«لا ريبَ فيه» سادسةٌ بلا خانة."""

    assert _attested("ما هذا بشرا") == 1  # ما الحجازيّة: خانةُ كان
    assert _attested("لا ريب فيه") == 14  # ريبَ مبنيٌّ على الفتح
    assert len(MORE_FAMILIES) == 2
    assert len(Q7_FAMILIES) + len(MORE_FAMILIES) == 6 > len(CELLS)


def test_the_audited_document_did_not_arrive() -> None:
    """الوثيقةُ المُحالُ إليها ليست في هذه الحاوية."""

    assert not Path("/mnt/agents/output/hamil_hala_zaman_layers.md").exists()
