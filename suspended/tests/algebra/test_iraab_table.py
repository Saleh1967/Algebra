"""ضبطُ العلامة الإعرابيّة: جدولٌ تامٌّ، وامتناعان مُعلَنان، وقسمةٌ ثلاثيّة.

**ما يُبنى ههنا**: العلامةُ الإعرابيّةُ دالّةٌ **تامّةٌ** على حاصل ضربِ
«نوعِ المعرَب × الحالةِ الإعرابيّة». وتمامُها شرطُ إنشاءٍ لا دعوى: خليّةٌ
منسيّةٌ تُسقِط الجدولَ، وخليّةٌ لا تقع في اللغة **تُعلَن ممتنعةً** — وإعلانُ
الامتناع دعوًى قابلةٌ للنقض («لا جزمَ في الأسماء، ولا جرَّ في الأفعال»).

ثمّ يُستخرَج ما لا يُرى بالسرد: **أيُّ أنواعِ المعرَب لا تفرّق بينها العلامةُ
أصلًا**، و**أيُّ حالةٍ يقوم عليها الفرقُ وحدَها**. وذلك حكمٌ على النظام لا
على الجدول.

والقسمةُ الثلاثيّةُ (اسمٌ · فعلٌ · حرف) مبنيّةٌ على العلامات لا على معجم:
مربّعٌ ٢×٢ خليّتُه الرابعةُ **ممتنعةٌ مُعلَنة** — «لا تجتمع للكلمة علامةُ
اسمٍ وعلامةُ فعل». والحرفُ معرَّفٌ **سلبًا**: ما لا يقبل هذه ولا تلك.
"""

from __future__ import annotations

import pytest

from algebra.assignment import Assignment, AssignmentError

CASES = ("رفع", "نصب", "جرّ", "جزم")

NOUN_KINDS = (
    "الاسمُ المفرد",
    "جمعُ التكسير",
    "جمعُ المؤنّث السالم",
    "جمعُ المذكّر السالم",
    "المثنّى",
    "الأسماءُ الخمسة",
    "الممنوعُ من الصرف",
    "الاسمُ المقصور",
    "الاسمُ المنقوص",
)
VERB_KINDS = (
    "المضارعُ الصحيحُ الآخر",
    "المضارعُ المعتلُّ بالواو أو الياء",
    "المضارعُ المعتلُّ بالألف",
    "الأفعالُ الخمسة",
)
KINDS = NOUN_KINDS + VERB_KINDS

# لا جزمَ في الأسماء، ولا جرَّ في الأفعال — دعويان تُعلَنان لا ثغرتان تُنسَيان
FORBIDDEN = tuple((kind, "جزم") for kind in NOUN_KINDS) + tuple(
    (kind, "جرّ") for kind in VERB_KINDS
)

MARKS = {
    "الاسمُ المفرد": ("ضمّة", "فتحة", "كسرة"),
    "جمعُ التكسير": ("ضمّة", "فتحة", "كسرة"),
    "جمعُ المؤنّث السالم": ("ضمّة", "كسرة", "كسرة"),
    "جمعُ المذكّر السالم": ("واو", "ياء", "ياء"),
    "المثنّى": ("ألف", "ياء", "ياء"),
    "الأسماءُ الخمسة": ("واو", "ألف", "ياء"),
    "الممنوعُ من الصرف": ("ضمّة", "فتحة", "فتحة"),
    "الاسمُ المقصور": ("ضمّةٌ مقدّرة", "فتحةٌ مقدّرة", "كسرةٌ مقدّرة"),
    "الاسمُ المنقوص": ("ضمّةٌ مقدّرة", "فتحة", "كسرةٌ مقدّرة"),
}
VERB_MARKS = {
    "المضارعُ الصحيحُ الآخر": ("ضمّة", "فتحة", "سكون"),
    "المضارعُ المعتلُّ بالواو أو الياء": (
        "ضمّةٌ مقدّرة",
        "فتحة",
        "حذفُ حرف العلّة",
    ),
    "المضارعُ المعتلُّ بالألف": (
        "ضمّةٌ مقدّرة",
        "فتحةٌ مقدّرة",
        "حذفُ حرف العلّة",
    ),
    "الأفعالُ الخمسة": ("ثبوتُ النون", "حذفُ النون", "حذفُ النون"),
}

CELLS = tuple(
    (kind, case, mark)
    for kind, marks in MARKS.items()
    for case, mark in zip(("رفع", "نصب", "جرّ"), marks, strict=True)
) + tuple(
    (kind, case, mark)
    for kind, marks in VERB_MARKS.items()
    for case, mark in zip(("رفع", "نصب", "جزم"), marks, strict=True)
)

IRAAB = Assignment(rows=KINDS, columns=CASES, cells=CELLS, forbidden=FORBIDDEN)


def test_the_table_is_total_over_the_grid_it_declares() -> None:
    """١٣ نوعًا × ٤ حالاتٍ = ٥٢ خليّة: ٣٩ مملوءةٌ و١٣ ممتنعةٌ مُعلَنة."""

    assert len(KINDS) == 13
    assert len(CASES) == 4
    assert IRAAB.filled == 39
    assert IRAAB.forbidden_count == 13
    assert IRAAB.covers_the_grid()
    assert IRAAB.filled + IRAAB.forbidden_count == 13 * 4 == 52


def test_the_two_bans_are_claims_and_are_enforced_on_every_row() -> None:
    """«لا جزمَ في الأسماء» و«لا جرَّ في الأفعال» — على كلّ صفٍّ بلا استثناء."""

    for kind in NOUN_KINDS:
        with pytest.raises(AssignmentError):
            IRAAB.value_at(kind, "جزم")
        assert IRAAB.value_at(kind, "جرّ")
    for kind in VERB_KINDS:
        with pytest.raises(AssignmentError):
            IRAAB.value_at(kind, "جرّ")
        assert IRAAB.value_at(kind, "جزم")
    assert len(FORBIDDEN) == len(NOUN_KINDS) + len(VERB_KINDS) == 13


def test_the_original_marks_are_four_and_the_rest_are_substitutes() -> None:
    """الأصليّةُ أربعٌ، والجدولُ يحمل ثلاثَ عشرةَ علامةً متمايزة."""

    original = {"ضمّة", "فتحة", "كسرة", "سكون"}
    assert original < set(IRAAB.distinct_values)
    assert len(IRAAB.distinct_values) == 13
    substitutes = set(IRAAB.distinct_values) - original
    assert {"واو", "ألف", "ياء"} <= substitutes
    assert {"ثبوتُ النون", "حذفُ النون", "حذفُ حرف العلّة"} <= substitutes


def test_the_mark_alone_does_not_separate_the_singular_from_the_broken_plural() -> None:
    """المفردُ وجمعُ التكسير **توقيعُهما واحد** — والجدولُ يُخرِجها زمرةً.

    وذلك حكمٌ على النظام: «جمعُ التكسير يُعرَب إعرابَ المفرد» ليس قاعدةً
    تُضاف، بل هو **أنّ العلامةَ لا تفرّق بينهما أصلًا**. ولا زمرةَ أخرى في
    الجدول كلِّه.
    """

    groups = IRAAB.indistinguishable_rows()
    assert groups == (("الاسمُ المفرد", "جمعُ التكسير"),)
    assert IRAAB.separating_columns("الاسمُ المفرد", "جمعُ التكسير") == ()


def test_four_pairs_differ_in_exactly_one_case_and_it_is_named() -> None:
    """أربعةُ فروقٍ يقوم كلٌّ منها على **حالةٍ واحدة** — وتُسمّى بالحساب."""

    assert IRAAB.separating_columns("الاسمُ المفرد", "جمعُ المؤنّث السالم") == ("نصب",)
    assert IRAAB.separating_columns("الاسمُ المفرد", "الممنوعُ من الصرف") == ("جرّ",)
    assert IRAAB.separating_columns("جمعُ المذكّر السالم", "المثنّى") == ("رفع",)
    assert IRAAB.separating_columns(
        "المضارعُ المعتلُّ بالواو أو الياء", "المضارعُ المعتلُّ بالألف"
    ) == ("نصب",)


def test_the_five_nouns_and_the_dual_meet_in_the_genitive_alone() -> None:
    """الأسماءُ الخمسةُ والمثنّى يفترقان في الرفع والنصب، **ويلتقيان في الجرّ**.

    وهذا ما أخرجه الحسابُ لا ما توقّعتُه: كلاهما يُجَرّ بالياء، فالياءُ علامةُ
    جرٍّ مشتركةٌ بين المثنّى وجمع المذكّر السالم والأسماء الخمسة — ثلاثةُ
    أنواعٍ تلتقي في حالةٍ وتفترق في غيرها.
    """

    assert IRAAB.separating_columns("الأسماءُ الخمسة", "المثنّى") == ("رفع", "نصب")
    assert IRAAB.value_at("الأسماءُ الخمسة", "جرّ") == "ياء"
    assert IRAAB.value_at("المثنّى", "جرّ") == "ياء"
    assert IRAAB.value_at("جمعُ المذكّر السالم", "جرّ") == "ياء"
    assert IRAAB.value_at("الأسماءُ الخمسة", "نصب") == "ألف"
    assert IRAAB.value_at("المثنّى", "نصب") == "ياء"


def test_the_table_separates_the_estimated_from_the_apparent() -> None:
    """المقصورُ والمنقوصُ يفترقان في النصب وحدَه: مقدّرةٌ مقابل ظاهرة."""

    assert IRAAB.separating_columns("الاسمُ المقصور", "الاسمُ المنقوص") == ("نصب",)
    assert IRAAB.value_at("الاسمُ المقصور", "نصب") == "فتحةٌ مقدّرة"
    assert IRAAB.value_at("الاسمُ المنقوص", "نصب") == "فتحة"


# ------------------------------------------------------------------ القسمة
NOUN_MARKS = ("الجرّ", "التنوين", "النداء", "أل", "الإسنادُ إليه")
VERB_SIGNS = (
    "قد",
    "السين",
    "سوف",
    "تاءُ التأنيث الساكنة",
    "ياءُ الفاعلة",
    "نونُ التوكيد",
)

PARTS = Assignment(
    rows=("يقبل علامةَ الاسم", "لا يقبلها"),
    columns=("يقبل علامةَ الفعل", "لا يقبلها"),
    cells=(
        ("لا يقبلها", "يقبل علامةَ الفعل", "فعل"),
        ("يقبل علامةَ الاسم", "لا يقبلها", "اسم"),
        ("لا يقبلها", "لا يقبلها", "حرف"),
    ),
    forbidden=(("يقبل علامةَ الاسم", "يقبل علامةَ الفعل"),),
)


def test_the_three_way_division_is_decided_by_marks_not_by_a_lexicon() -> None:
    """اسمٌ وفعلٌ وحرف: مربّعٌ ٢×٢، والحرفُ معرَّفٌ **سلبًا** لا بقائمة."""

    assert PARTS.covers_the_grid()
    assert PARTS.filled == 3
    assert set(PARTS.distinct_values) == {"اسم", "فعل", "حرف"}
    assert PARTS.value_at("لا يقبلها", "لا يقبلها") == "حرف"
    assert len(NOUN_MARKS) == 5
    assert len(VERB_SIGNS) == 6


def test_the_fourth_cell_is_a_falsifiable_claim_not_an_oversight() -> None:
    """«لا تجتمع علامةُ اسمٍ وعلامةُ فعل» ممتنعةٌ مُعلَنة، فتُنقَض إن وُجِدت."""

    with pytest.raises(AssignmentError):
        PARTS.value_at("يقبل علامةَ الاسم", "يقبل علامةَ الفعل")
    assert PARTS.forbidden_count == 1
    assert PARTS.separating_columns("يقبل علامةَ الاسم", "لا يقبلها") == (
        "يقبل علامةَ الفعل",
        "لا يقبلها",
    )
