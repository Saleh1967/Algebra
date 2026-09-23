"""شجرةُ النتائج مفحوصةً في نفسها: الجداءُ يُتَمّ، والغيابُ يُصنَّف.

ولا رقمَ لغويًّا ههنا: محاورُ مُختلَقةٌ بأسماءٍ محايدة. والغرضُ أن تُفحَص
شروطُ الإنشاء نفسُها — أنّ الفرعَ الناقصَ يُسقِط البناءَ، وأنّ الامتناعَ بلا
ناقضٍ يُرَدّ، وأنّ النتيجةَ بلا بقيّةٍ لا تُودَع.
"""

from __future__ import annotations

import pytest

from algebra.results import (
    COMPLETENESS_CONDITIONS,
    FORBIDDEN,
    OPEN,
    SHELVED,
    STATES,
    Axis,
    Finding,
    Library,
    Placement,
    Product,
    ResultsError,
)

LEFT = Axis(name="المحورُ الأوّل", values=("أ", "ب"))
RIGHT = Axis(name="المحورُ الثاني", values=("س", "ص", "ع"))
GRID = Product(axes=(LEFT, RIGHT))


def _finding(label: str, unmet: tuple[str, ...] = ()) -> Finding:
    return Finding(
        statement=f"قولُ {label}",
        source=f"مصدرُ {label}",
        unit="عددُ الوقوعات",
        null="تبديلٌ يحفظ الهامشين ببذرةٍ معلَنة",
        oracle="لا أوراكل",
        invariance="ثابتٌ تحت تسمية الرموز",
        residue=f"ما لا يقوله {label}",
        unmet=unmet,
    )


def _shelf(first: str, second: str, label: str) -> Placement:
    return Placement(coordinate=(first, second), finding=_finding(label))


FULL = Library(
    name="مكتبةٌ للفحص",
    product=GRID,
    placements=tuple(
        _shelf(first, second, f"{first}{second}")
        for first in LEFT.values
        for second in RIGHT.values
    ),
)


# ------------------------------------------------------- المحورُ والجداء


def test_an_axis_refuses_emptiness_and_disjunction() -> None:
    """محورٌ بلا قيمٍ لا يُجدَأ، وقيمةٌ فيها «أو» قيمتان في خانةٍ واحدة."""

    with pytest.raises(ResultsError):
        Axis(name="فارغ", values=())
    with pytest.raises(ResultsError):
        Axis(name="مزدوج", values=("أ", "ب أو ج"))
    with pytest.raises(ResultsError):
        Axis(name="مكرَّر", values=("أ", "أ"))


def test_the_product_size_is_the_product_not_the_count_we_have() -> None:
    """حجمُ الجداء حاصلُ ضربِ المحاور، ونقاطُه مسرودةٌ بترتيبٍ ثابت."""

    assert GRID.size == 2 * 3 == 6
    assert GRID.depth == 2
    assert len(GRID.points()) == GRID.size
    assert GRID.points()[0] == ("أ", "س")
    assert GRID.points()[-1] == ("ب", "ع")
    assert GRID.index_of("المحورُ الثاني") == 1
    with pytest.raises(ResultsError):
        GRID.index_of("محورٌ لا وجودَ له")


# --------------------------------------------------------------- النتيجة


def test_a_result_without_its_conditions_is_refused() -> None:
    """المصدرُ والوحدةُ والصفريُّ والأوراكلُ والثباتُ شروطُ إيداعٍ لا زينة."""

    names = (
        "statement",
        "source",
        "unit",
        "null",
        "oracle",
        "invariance",
        "residue",
    )
    for blank in names:
        text = {name: ("   " if name == blank else "نصٌّ") for name in names}
        with pytest.raises(ResultsError):
            Finding(
                statement=text["statement"],
                source=text["source"],
                unit=text["unit"],
                null=text["null"],
                oracle=text["oracle"],
                invariance=text["invariance"],
                residue=text["residue"],
            )


def test_a_result_without_a_residue_has_not_been_read() -> None:
    """«لا شيء» ليست بقيّةً بل نفيُها، فتُرَدّ عند الإيداع."""

    with pytest.raises(ResultsError):
        Finding(
            statement="قول",
            source="مصدر",
            unit="وحدة",
            null="صفريّ",
            oracle="أوراكل",
            invariance="ثبات",
            residue="لا شيء",
        )


def test_a_broken_condition_lowers_the_standing_and_is_named() -> None:
    """الخرمُ يُسمّى باسم الشرط، والحكمُ يهبط إلى «مبدئيّ» لا يُطوى."""

    sound = _finding("تامّ")
    assert sound.is_minimally_complete
    assert sound.standing == "مُوثَّق"

    lame = _finding("ناقص", unmet=(COMPLETENESS_CONDITIONS[4],))
    assert not lame.is_minimally_complete
    assert lame.standing == "مبدئيّ"
    assert len(lame.conditions()) == len(COMPLETENESS_CONDITIONS)
    assert dict(lame.conditions())[COMPLETENESS_CONDITIONS[4]] is False
    assert dict(lame.conditions())[COMPLETENESS_CONDITIONS[0]] is True

    with pytest.raises(ResultsError):
        _finding("مجهول", unmet=("ش٩ شرطٌ لا وجودَ له",))


# --------------------------------------------------------------- الخانة


def test_a_cell_carries_exactly_one_of_three() -> None:
    """نتيجةٌ أو امتناعٌ أو فتحٌ — واحدةٌ لا صفرٌ ولا اثنتان."""

    with pytest.raises(ResultsError):
        Placement(coordinate=("أ", "س"))
    with pytest.raises(ResultsError):
        Placement(
            coordinate=("أ", "س"),
            finding=_finding("واحد"),
            open_test="فحصٌ فاصل",
        )


def test_a_forbidden_cell_must_name_what_would_refute_it() -> None:
    """الامتناعُ دعوًى قابلةٌ للنقض؛ وبلا ناقضٍ هو إعفاءٌ من الملء."""

    with pytest.raises(ResultsError):
        Placement(coordinate=("أ", "س"), forbidden_because="لا يقع ههنا")
    standing = Placement(
        coordinate=("أ", "س"),
        forbidden_because="لا يقع ههنا",
        refuted_by="مثالٌ واحدٌ يقع",
    )
    assert standing.state == FORBIDDEN
    assert "ينقضه" in standing.text

    with pytest.raises(ResultsError):
        Placement(
            coordinate=("أ", "س"),
            finding=_finding("واحد"),
            refuted_by="ناقضٌ بلا امتناع",
        )


def test_an_open_cell_names_one_test_not_a_disjunction() -> None:
    """«فحصُ أ أو ب» امتناعٌ عن القسمة لا فحصٌ فاصل."""

    with pytest.raises(ResultsError):
        Placement(coordinate=("أ", "س"), open_test="عدُّ أ أو عدُّ ب")
    locus = Placement(coordinate=("أ", "س"), open_test="مرورٌ واحدٌ على المجتمع")
    assert locus.state == OPEN
    assert locus.path == "أ ← س"
    assert locus.summary(20).startswith(f"[{OPEN}]")


# -------------------------------------------------------------- المكتبة


def test_a_missing_branch_sinks_the_library() -> None:
    """الفرعُ الناقصُ ثغرةٌ تُرَدّ عند الإنشاء لا اختصارٌ يُحسَب ترتيبًا."""

    with pytest.raises(ResultsError) as raised:
        Library(
            name="ناقصة",
            product=GRID,
            placements=(_shelf("أ", "س", "واحد"),),
        )
    assert "5 من 6" in str(raised.value)


def test_a_cell_placed_twice_is_refused() -> None:
    """خانةٌ موضوعةٌ مرّتين ليست تأكيدًا بل تناقضًا محتملًا."""

    doubled = (*FULL.placements, _shelf("أ", "س", "ثانٍ"))
    with pytest.raises(ResultsError):
        Library(name="مزدوجة", product=GRID, placements=doubled)


def test_the_census_prints_every_state_including_zero() -> None:
    """الحالاتُ الثلاثُ تُعَدّ كلُّها، والصفرُ يُطبَع ولا يُحذَف."""

    census = FULL.census()
    assert set(census) == set(STATES)
    assert census[SHELVED] == 6
    assert census[FORBIDDEN] == 0
    assert census[OPEN] == 0
    assert FULL.covers_the_product()
    assert sum(census.values()) == GRID.size


def test_a_whole_slab_open_is_an_axis_not_a_cell() -> None:
    """إن كان كلُّ ما تحت قيمةٍ مفتوحًا فالنقصُ في المحور لا في الخلايا."""

    placements = []
    for first in LEFT.values:
        for second in RIGHT.values:
            if second == "ع":
                placements.append(
                    Placement(coordinate=(first, second), open_test=f"فحصُ {first}")
                )
            else:
                placements.append(_shelf(first, second, f"{first}{second}"))
    library = Library(name="بعمودٍ مفتوح", product=GRID, placements=tuple(placements))

    assert library.slabs_entirely(OPEN) == (("المحورُ الثاني", "ع"),)
    assert library.census()[OPEN] == 2
    assert len(library.open_loci()) == 2
    with pytest.raises(ResultsError) as raised:
        library.assert_not_reportable_as_settled()
    assert "2 موضعًا مفتوحًا" in str(raised.value)


def test_two_values_with_one_signature_are_not_distinguished() -> None:
    """قيمتان تتّفق حالُهما على الباقي كلِّه لا يفرّق بينهما البناء."""

    placements = []
    for first in LEFT.values:
        for second in RIGHT.values:
            if second in {"س", "ص"}:
                placements.append(
                    Placement(
                        coordinate=(first, second), open_test=f"فحصُ {first}{second}"
                    )
                )
            else:
                placements.append(_shelf(first, second, f"{first}{second}"))
    library = Library(name="بتوقيعين", product=GRID, placements=tuple(placements))

    assert library.indistinguishable_values("المحورُ الثاني") == (("س", "ص"),)
    assert library.indistinguishable_values("المحورُ الأوّل") == (("أ", "ب"),)
    assert FULL.indistinguishable_values("المحورُ الأوّل") == (("أ", "ب"),)


def test_the_tree_shows_one_path_for_every_point() -> None:
    """الشجرةُ تُظهِر مسارًا لكلّ نقطةٍ من الجداء، لا لما عندنا وحدَه."""

    drawing = FULL.tree(width=24).splitlines()
    assert drawing[0] == "مكتبةٌ للفحص"
    leaves = [line for line in drawing if "·" in line]
    assert len(leaves) == GRID.size
    assert len(drawing) == 1 + len(LEFT.values) + GRID.size
    assert all(f"[{SHELVED}]" in leaf for leaf in leaves)
    assert len(FULL.paths()) == GRID.size


def test_the_library_reports_its_own_silence() -> None:
    """البقايا تُخرَج بطلبٍ كما تُخرَج النتائج، والمبدئيُّ يُفصَل عن المُوثَّق."""

    mixed = (
        _shelf("أ", "س", "واحد"),
        Placement(
            coordinate=("أ", "ص"),
            finding=_finding("ناقص", unmet=(COMPLETENESS_CONDITIONS[2],)),
        ),
        Placement(
            coordinate=("أ", "ع"),
            forbidden_because="لا يقع ههنا",
            refuted_by="مثالٌ واحدٌ يقع",
        ),
        _shelf("ب", "س", "اثنان"),
        _shelf("ب", "ص", "ثلاثة"),
        Placement(coordinate=("ب", "ع"), open_test="مرورٌ واحدٌ على المجتمع"),
    )
    library = Library(name="مختلطة", product=GRID, placements=mixed)

    assert library.census() == {SHELVED: 4, FORBIDDEN: 1, OPEN: 1}
    assert len(library.certified()) == 3
    assert len(library.provisional()) == 1
    assert library.broken_conditions()[COMPLETENESS_CONDITIONS[2]] == 1
    assert library.broken_conditions()[COMPLETENESS_CONDITIONS[0]] == 0
    assert len(library.residues()) == 4
    assert library.forbidden_claims() == (("أ ← ع", "لا يقع ههنا", "مثالٌ واحدٌ يقع"),)
    assert library.open_loci() == (("ب ← ع", "مرورٌ واحدٌ على المجتمع"),)
    assert library.slabs_entirely(SHELVED) == (
        ("المحورُ الثاني", "س"),
        ("المحورُ الثاني", "ص"),
    )
    assert library.slabs_entirely(OPEN) == ()
    assert library.state_at(("ب", "س")) == SHELVED
    assert len(library.slice_of("المحورُ الأوّل", "أ")) == 3
