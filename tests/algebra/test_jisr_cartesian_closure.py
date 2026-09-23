"""الإغلاقُ ديكارتيًّا: عشرُ طبقاتٍ × خمسةُ شروط، ولا خليّةَ تُترَك.

**القاعدة**: لا تُقفَل فجوةٌ برقعةٍ متفرّقة. تُقام الشبكةُ كاملةً — كلُّ طبقةٍ
في كلّ شرطٍ من **الحدّ الأدنى المكتمل** — ويُفرَض تمامُها شرطَ إنشاء
(`assignment.Assignment`). فخليّةٌ منسيّةٌ تُسقِط الشبكة، وخليّةٌ لا تُقوَّم
ههنا **تُعلَن ممتنعةً** ويُسمّى سببُها.

والشروطُ الخمسةُ منقولةٌ من «البناء الثاني» بنصّها:
    ش١ عدٌّ مباشرٌ أو قياسٌ محجوب — لا ملاءمةَ ولا استقراء
    ش٢ اسمٌ يطابق المقيس
    ش٣ صفريٌّ مكافئٌ يختلف في المدَّعى وحدَه — أو حصرٌ تامٌّ يُغني
    ش٤ الأوراكلُ منعدمٌ أو مُعلَنٌ والقولُ مقيَّدٌ به
    ش٥ ثابتٌ تحت اختيارات التمثيل

`A_COLUMN_MAY_FAIL_WHERE_NO_CELL_DOES`: أهمُّ ما يُخرِجه التعدادُ التامُّ
ليس خليّةً بل **عمودًا**: ش٥ مخرومٌ في **الطبقات التسع كلِّها**. فليست تسعَ
عللٍ متفرّقةً بل **علّةٌ واحدةٌ مشتركة**، ولا يُصلِحها تسعُ رقعٍ بل قرارٌ
واحد. وهذا ما يخفيه سردُ الرقع.

`A_PATCH_CLOSES_A_CELL_OR_IT_IS_NOT_A_PATCH`: كلُّ رقعةٍ تُنسَب إلى الخليّة
التي تقلبها؛ ورقعةٌ لا تُسمّي خليّتَها تحسينٌ لا إغلاق. والرقعُ التسعُ تُغلِق
**خمسَ خلايا**، ويبقى اثنتا عشرة — وذلك يُقال لا يُطوى.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.assignment import Assignment, AssignmentError

LAYERS = ("ط٠", "ط١", "ط٢", "ط٣", "ط٤", "ط٥", "ط٦", "ط٧", "ط٨", "ط٩")
CONDITIONS = ("ش١", "ش٢", "ش٣", "ش٤", "ش٥")
MET, BROKEN = "مستوفٍ", "مخروم"

# ط٤ طبقةٌ **مُحمَّلةٌ** لا منفَّذة (`CUR = pickle.load('jidh5.pkl')['cur']`)،
# فلا تُقوَّم في هذا الملفّ. والامتناعُ يُعلَن ولا يُترَك ثغرةً.
FORBIDDEN = tuple(("ط٤", condition) for condition in CONDITIONS)

GRID = {
    "ط٠": (MET, MET, MET, MET, BROKEN),
    "ط١": (MET, MET, MET, MET, BROKEN),
    "ط٢": (MET, BROKEN, BROKEN, MET, BROKEN),
    "ط٣": (BROKEN, MET, MET, MET, BROKEN),
    "ط٥": (BROKEN, MET, BROKEN, MET, BROKEN),
    "ط٦": (MET, MET, BROKEN, MET, BROKEN),
    "ط٧": (MET, MET, MET, MET, BROKEN),
    "ط٨": (MET, MET, BROKEN, MET, BROKEN),
    "ط٩": (MET, BROKEN, MET, MET, BROKEN),
}

TABLE = Assignment(
    rows=LAYERS,
    columns=CONDITIONS,
    cells=tuple(
        (layer, condition, verdict)
        for layer, verdicts in GRID.items()
        for condition, verdict in zip(CONDITIONS, verdicts, strict=True)
    ),
    forbidden=FORBIDDEN,
)

# كلُّ رقعةٍ تُنسَب إلى الخليّة التي تقلبها — ورقعةٌ بلا خليّةٍ تحسينٌ لا إغلاق
PATCHES = {
    ("ط٣", "ش١"): "ر١ — CLOSED تُبنى من TRAIN وحدَه، فيصير القياسُ محجوبًا",
    ("ط٥", "ش١"): "ر٢ — R تُبنى من TRAIN وتُقوَّم على TEST",
    ("ط٢", "ش٢"): "ر٣ — المقارنةُ بالمضمون لا بالطول، فيطابق الاسمُ المقيسَ",
    ("ط٩", "ش٢"): "ر٤ و ر٥ — الامتناعُ يُفصَل والمقامُ يُطبَع",
    ("ط٦", "ش٣"): "ر٦ — خطُّ الأساس على TEST لا على TRAIN",
}

# وما لا تُغلِقه الرقعُ التسع — أسرتان مُسمّاتان لا اثنتا عشرةَ علّة
OPEN_FAMILIES = {
    "بلا صفريٍّ مكافئ": (("ط٢", "ش٣"), ("ط٥", "ش٣"), ("ط٨", "ش٣")),
    "بلا ثباتٍ تحت التمثيل": tuple((layer, "ش٥") for layer in LAYERS if layer != "ط٤"),
}
# ورقعٌ لا تُغلِق خليّةً: متانةٌ وتحديدٌ، وتُسمّى كذلك ولا تُحسَب إغلاقًا
HYGIENE_PATCHES = ("ر٧ — ترتيبٌ مُعلَن", "ر٨ — حارسُ الخالية", "ر٩ — الموازنة")


def test_the_grid_is_total_and_nothing_was_forgotten() -> None:
    """عشرُ طبقاتٍ × خمسةُ شروطٍ = ٥٠ خليّة: ٤٥ مملوءةٌ و٥ ممتنعةٌ مُعلَنة."""

    assert len(LAYERS) * len(CONDITIONS) == 50
    assert TABLE.filled == 45
    assert TABLE.forbidden_count == 5
    assert TABLE.covers_the_grid()
    assert set(TABLE.distinct_values) == {MET, BROKEN}


def test_a_forgotten_cell_sinks_the_grid_at_construction() -> None:
    """إسقاطُ خليّةٍ واحدةٍ يُسقِط الشبكةَ — وهذا هو التعدادُ التامّ عاملًا."""

    short = tuple(
        (layer, condition, verdict)
        for layer, verdicts in GRID.items()
        for condition, verdict in zip(CONDITIONS, verdicts, strict=True)
        if (layer, condition) != ("ط٧", "ش٣")
    )
    with pytest.raises(AssignmentError) as raised:
        Assignment(rows=LAYERS, columns=CONDITIONS, cells=short, forbidden=FORBIDDEN)
    assert "ثغرات" in str(raised.value)


def test_the_fifth_condition_fails_in_every_single_layer() -> None:
    """ش٥ مخرومٌ في التسع كلِّها — علّةٌ واحدةٌ مشتركةٌ لا تسعُ عللٍ متفرّقة.

    وهذا ما لا يُرى في سردِ الرقع ويُرى في الشبكة: لا طبقةَ أُعيد قياسُها على
    أساسٍ ثانٍ، ولا على قسمةٍ أخرى غيرِ الفرديّة والزوجيّة. فالإصلاحُ قرارٌ
    واحدٌ في التصميم لا تسعُ رقعٍ في الشفرة.
    """

    fifth = [TABLE.value_at(layer, "ش٥") for layer in LAYERS if layer != "ط٤"]
    assert len(fifth) == 9
    assert set(fifth) == {BROKEN}
    fourth = [TABLE.value_at(layer, "ش٤") for layer in LAYERS if layer != "ط٤"]
    assert set(fourth) == {MET}  # والعمودُ المقابلُ سليمٌ في التسع


def test_the_grid_groups_the_layers_by_their_signature() -> None:
    """ثلاثُ طبقاتٍ توقيعُها واحد — وهي التي تستوفي ش١–ش٤ اليومَ."""

    groups = {frozenset(members) for members in TABLE.indistinguishable_rows()}
    assert frozenset({"ط٠", "ط١", "ط٧"}) in groups
    assert frozenset({"ط٦", "ط٨"}) in groups
    for layer in ("ط٠", "ط١", "ط٧"):
        assert TABLE.signature_of(layer)[:4] == (MET, MET, MET, MET)


def test_the_minimal_complete_is_three_of_nine_today() -> None:
    """بالشروط الأربعة القابلة للإغلاق اليومَ: ثلاثٌ تستوفي، وستٌّ لا.

    ولا طبقةَ تستوفي الخمسةَ، لأنّ ش٥ مخرومٌ في الكلّ. فالحدُّ الأدنى المكتملُ
    للجسر **خالٍ** ما دام ش٥ قائمًا، و**ثلاثٌ** إن عُزِل ش٥ دَينًا مشتركًا
    مُعلَنًا. والفرقُ بين العبارتين يُقال ولا يُطوى.
    """

    all_five = [
        layer
        for layer in LAYERS
        if layer != "ط٤" and set(TABLE.signature_of(layer)) == {MET}
    ]
    assert all_five == []
    first_four = [
        layer
        for layer in LAYERS
        if layer != "ط٤" and set(TABLE.signature_of(layer)[:4]) == {MET}
    ]
    assert first_four == ["ط٠", "ط١", "ط٧"]
    assert len(first_four) == 3
    assert Fraction(len(first_four), 9) == Fraction(1, 3)


def test_every_broken_cell_is_either_patched_or_in_a_named_family() -> None:
    """لا خليّةَ مخرومةٌ بلا رقعةٍ أو أسرةٍ مُسمّاة — وهذا شرطُ الإغلاق."""

    broken = {
        (layer, condition)
        for layer in LAYERS
        for condition in CONDITIONS
        if (layer, condition) not in set(FORBIDDEN)
        and TABLE.value_at(layer, condition) == BROKEN
    }
    assert len(broken) == 17
    covered = set(PATCHES) | {
        cell for cells in OPEN_FAMILIES.values() for cell in cells
    }
    assert broken <= covered
    assert not (broken - covered)


def test_the_nine_patches_close_five_cells_and_twelve_remain() -> None:
    """الرقعُ التسعُ تُغلِق **خمسًا**، وتبقى اثنتا عشرةَ في أسرتين مُسمّاتين."""

    assert len(PATCHES) == 5
    remaining = {cell for cells in OPEN_FAMILIES.values() for cell in cells}
    assert len(remaining) == 12
    assert len(PATCHES) + len(remaining) == 17
    assert not (set(PATCHES) & remaining)
    assert len(OPEN_FAMILIES["بلا صفريٍّ مكافئ"]) == 3
    assert len(OPEN_FAMILIES["بلا ثباتٍ تحت التمثيل"]) == 9
    assert len(HYGIENE_PATCHES) == 3  # ولا تُحسَب إغلاقًا


def test_the_grid_after_the_patches_moves_three_layers_into_the_minimum() -> None:
    """بعد الرقع الخمس المُغلِقة: تستوفي ش١–ش٤ **ستُّ** طبقاتٍ لا ثلاث."""

    patched = dict(GRID)
    for (layer, condition), _ in PATCHES.items():
        row = list(patched[layer])
        row[CONDITIONS.index(condition)] = MET
        patched[layer] = tuple(row)
    after = Assignment(
        rows=LAYERS,
        columns=CONDITIONS,
        cells=tuple(
            (layer, condition, verdict)
            for layer, verdicts in patched.items()
            for condition, verdict in zip(CONDITIONS, verdicts, strict=True)
        ),
        forbidden=FORBIDDEN,
    )
    first_four = [
        layer
        for layer in LAYERS
        if layer != "ط٤" and set(after.signature_of(layer)[:4]) == {MET}
    ]
    assert first_four == ["ط٠", "ط١", "ط٣", "ط٦", "ط٧", "ط٩"]
    assert len(first_four) == 6
    # وتبقى ط٢ وط٥ وط٨ خارجَه — كلُّها بسبب ش٣ وحدَه
    for layer in ("ط٢", "ط٥", "ط٨"):
        assert after.value_at(layer, "ش٣") == BROKEN
    assert [
        layer
        for layer in LAYERS
        if layer != "ط٤" and set(after.signature_of(layer)) == {MET}
    ] == []
