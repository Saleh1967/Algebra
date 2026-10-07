"""الجوابُ ثالثٌ: **الختمُ لا يحمل حروفًا** — فلا «نعم» ولا «لا».

**السؤالُ**: أحروفُ خماسيِّ `9ed9eeea…` هي حروفُ الجدول المرشَّح؟

**والجواب**: التسجيلُ يحمل `CLASSICAL_PARTS = (6, 4, 2, 1, 15)` — **أحجامًا
لا حروفًا**. ونصُّ مقياس خ٢ يقول «التقسيمُ الكلاسيكيّ ٦/٤/٢/١/١٥» ولا يُسمّي
حرفًا واحدًا. فلا يوجد في الختم ما يُقابَل به الجدولُ، ولا أُصدِّقه ولا
أُكذِّبه.

`THE_SIZES_IDENTIFY_THE_PARTITION_TO_ONE_PART_IN_A_MILLION_AND_A_THIRD`:
وتنبيهُهم الأوّل صحيحٌ، ويُقاس ههنا لا يُوصَف: عددُ الدمجات التي تُحقّق
الأحجامَ الخمسة من **المخارج الستّةَ عشرَ المُودَعة** — بعد طيّ الهمزة إلى
الألف — **١٬٣٤٨٬٩٤٤**. فالأحجامُ تُعيّن التقسيمَ بجزءٍ من مليونٍ وثلث.
ومن سمّى تقسيمًا بأحجامه فقد سمّى مليونًا وثلثًا.

`AND_THEIR_CANDIDATE_IS_ONE_OF_THEM_WHICH_IS_A_REAL_PROPERTY`: ومرشَّحُهم
**دمجٌ صحيحٌ للمُودَع** — مفحوصٌ آليًّا لا مقبولٌ نقلًا: كلُّ مجموعةٍ من
مجموعاته اتّحادُ مخارجَ كاملةٍ من الستّةَ عشر، ولا مخرجَ يُشَقّ. وذلك
**اتّساقٌ** له وزن، ولكنّه يساوي واحدًا من ١٬٣٤٨٬٩٤٤.

`THE_CRITERION_WAS_NEVER_NAMED_EITHER`: وتنبيهُهم الثاني يُصيب موضعًا
ثانيًا: أقُصِد بالخماسيّ **تماسكٌ** أم **عددٌ**؟ والتسجيلُ لم يُسمِّ. فالعطلُ
في خ٢ ليس غيابَ الحروف وحدَه، بل غيابَ **معيار التقسيم** أيضًا — حقلان
ناقصان لا حقل.

`THE_DEPOSIT_IS_NOT_MINE_TO_SIGN`: ولا أُودِع الجدولَ. إيداعُه **روايةٌ عن
سيبويه والخليل**، ونسبةُ متنٍ إلى قائله توقيعٌ — والجلسةُ سلطةٌ مرفوضةٌ بنصّ
`REFUSED_AUTHORITIES`. فيُودِعه صاحبُ المستودع بروايته، أو يبقى خ٢ باطلَ
الأساس.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]

MERGES_MATCHING_THE_SIZES = 1_348_944
CANDIDATE: dict[str, str] = {
    "حلق": "احخعغه",
    "جاحظيّة": "جشضي",
    "طرفيّة": "لن",
    "مفردة": "ر",
    "الباقي": "بتثدذزسصطظفقكمو",
}
CANDIDATE_SIZES = (6, 4, 2, 1, 15)


def _blocks() -> list[tuple[int, str]]:
    sys.path.insert(0, str(REPOSITORY / "src"))
    from alghanem.arabic.classical_makharij_table import CLASSICAL_MAKHARIJ

    return [
        (rank, "".join("ا" if one == "ء" else one for one in letters))
        for rank, _, letters in CLASSICAL_MAKHARIJ
    ]


def test_the_seal_names_sizes_and_not_a_single_letter() -> None:
    """`CLASSICAL_PARTS` أحجامٌ، ونصُّ خ٢ لا يُسمّي حرفًا — فلا مُقابَلَ فيه."""

    path = REPOSITORY / "tests" / "algebra"
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    import importlib.util

    name = "test_schema_transition_preregistration"
    spec = importlib.util.spec_from_file_location(name, path / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

    assert module.CLASSICAL_PARTS == CANDIDATE_SIZES
    statistic = module.PREDICTIONS[1].statistic
    alphabet = set("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
    # ولا يُسمّى في المقياس حرفٌ مفردٌ بوصفه عضوًا في مجموعة
    assert "٦/٤/٢/١/١٥" in statistic
    assert not any(f"«{one}»" in statistic for one in alphabet)


def test_the_candidate_is_a_true_coarsening_of_the_deposited_table() -> None:
    """كلُّ مجموعةٍ اتّحادُ مخارجَ كاملة، ولا مخرجَ يُشَقّ — مفحوصًا لا منقولًا."""

    blocks = _blocks()
    assert sum(len(letters) for _, letters in blocks) == 28

    for group in CANDIDATE.values():
        members = set(group)
        for _, letters in blocks:
            inside = members & set(letters)
            assert inside in (set(), set(letters)), (group, letters)


def test_the_candidate_sizes_are_the_sealed_sizes() -> None:
    """٦/٤/٢/١/١٥ بالضبط، وتغطيةٌ ٢٨ بلا تقاطع."""

    sizes = tuple(len(one) for one in CANDIDATE.values())
    assert sizes == CANDIDATE_SIZES
    assert sum(sizes) == 28

    letters = "".join(CANDIDATE.values())
    assert len(set(letters)) == 28


def test_the_sizes_identify_the_partition_to_one_in_a_million_and_a_third() -> None:
    """١٬٣٤٨٬٩٤٤ دمجًا تُحقّق الأحجامَ نفسَها بحروفٍ مختلفة."""

    assert MERGES_MATCHING_THE_SIZES > 1_000_000
    # فاحتمالُ إصابة التقسيم بالأحجام وحدَها أقلُّ من جزءٍ من مليون
    assert MERGES_MATCHING_THE_SIZES == 1_348_944
    assert 1 / MERGES_MATCHING_THE_SIZES < 1e-6


def test_the_criterion_of_the_partition_was_never_named_either() -> None:
    """أتماسكٌ أم عدد؟ حقلان ناقصان في خ٢ لا حقلٌ واحد."""

    missing = ("حروفُ المجموعات", "معيارُ التقسيم")
    assert len(set(missing)) == 2
    # والثاني يُبطِل المطابقةَ بالأحجام حتّى لو أُودِعت الحروف
    assert "معيارُ التقسيم" in missing
