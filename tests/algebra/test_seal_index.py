"""الفهرسُ شهادةُ اتّساقٍ لا جدولَ نقل — ولا ختمَ في الشجرة خارجَه.

**ما يحرسه**: أنّ كلَّ بصمةٍ في `docs/فهرس-الأختام.md` **أُعيد حسابُها**
من شاهدها وشروطها، وأنّ **كلَّ ثابتٍ سداسيٍّ عشريٍّ من ٦٤ خانةً** مكتوبٍ
في `tests/` إمّا **مُشتقٌّ ومُفهرَس**، أو **مُعلَنٌ ههنا بسببه**.

**ولماذا**: ختمٌ يُكتَب ولا يُفهرَس **يسقط من الجرد صامتًا**، فتُقرَأ
الشجرةُ أقلَّ التزامًا ممّا هي، أو — وهو الأسوأ — **أكثرَ**.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
TOOL = REPOSITORY / "tools" / "write_seal_index.py"
INDEX = REPOSITORY / "docs" / "فهرس-الأختام.md"
TESTS = REPOSITORY / "tests"
HEX = re.compile(r"\b[0-9a-f]{64}\b")

EMPTY = hashlib.sha256(b"").hexdigest()
"""بصمةُ اللاشيء — تُحسَب ولا تُنقَل، فلا يُخطئ أحدٌ في التعرّف عليها."""

NOT_A_PREREGISTRATION = {
    "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a": (
        "بايتاتُ المدوّنة المُجمَّدة — سجلُّ مادّةٍ لا شرطَ فيه"
    ),
    "30c7e393eff12641e27802dbfc38c51e7171ed873bfd2f78dc889de2fad7a359": (
        "سجلُّ بايتاتٍ آخرُ — مادّةٌ لا شرطَ فيها"
    ),
    "46b4393fdb3a09208ecb96fbbac990a150e4374f82d7940c655430cd1b1611ae": (
        "بصمةُ مصدرٍ — مادّةٌ لا شرطَ فيها"
    ),
    "265a30b69b9f95e57f7884fd7b4946eb2a5374cdc20db07fb87238a5e5fe59de": (
        "بصمةُ QAC — مادّةٌ لا شرطَ فيها"
    ),
    "3fa9a1bee07abcb18b7c7038b9f70682c7f86d3cfe09c3201b78a081aa7a6fab": (
        "بصمةُ كتابٍ — مادّةٌ لا شرطَ فيها"
    ),
    "d435d63a4e49ea03a75344b050df01dd99d5bfb77335c807e2d6309f52174341": (
        "بصمةُ مُودَعٍ — مادّةٌ لا شرطَ فيها"
    ),
    "ca75f300ba9125e3cd45cbf1f43eb6482d2ae6cdf40d1876eeb5fbc76ee7278a": (
        "سجلُّ الانقلاب المُجمَّد — سجلُّ **نتيجةٍ مقيسة** لا تسجيلَ شرطٍ "
        "قبل النظر؛ حقولُه مُقابَلةٌ بالسجلّات في `tools/inversion_seal.py`"
    ),
    EMPTY: (
        "بصمةُ اللاشيء في خانة بصمة — **عطلٌ مُعلَنٌ لا إسناد**: "
        "`PROSE` في `test_schema_transition_preregistration` يحمل "
        "بصمةَ سلسلةٍ خالية مع حجمٍ ٢٣٦٬٩٩٤ كلمة، فالحجمُ مكتوبٌ "
        "والبايتاتُ لم تُبصَم قطّ"
    ),
}
"""ثوابتُ ليست أختامًا — ولكلٍّ سببٌ مكتوب، ولا يُزاد فيها بلا سبب."""


def _tool() -> object:
    spec = importlib.util.spec_from_file_location("write_seal_index", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_index_is_regenerated_and_never_typed() -> None:
    """المكتوبُ مطابقٌ لما تولّده الأداة — حرفًا بحرف."""

    assert _tool().render() == INDEX.read_text(encoding="utf-8")  # type: ignore[attr-defined]


def test_every_indexed_seal_is_recomputed_not_copied() -> None:
    """لا بصمةَ في الفهرس إلّا وقد أُعيد اشتقاقُها من شروطها."""

    rows = _tool().gather()  # type: ignore[attr-defined]
    assert rows, "لا ختمَ وُجِد — وهو عطلُ آلةٍ لا خلوُّ شجرة"
    written = INDEX.read_text(encoding="utf-8")
    for row in rows:
        assert f"`{row['digest'][:8]}…`" in written, row["digest"]
        assert row["count"] >= 1
        assert len(row["marks"]) == row["count"]


def test_no_seal_in_the_tree_falls_outside_the_index() -> None:
    """كلُّ ثابتٍ من ٦٤ خانةً في `tests/` إمّا مُفهرَسٌ أو مُعلَنٌ بسببه."""

    indexed = {row["digest"] for row in _tool().gather()}  # type: ignore[attr-defined]
    loose: dict[str, set[str]] = {}
    for path in sorted(TESTS.rglob("*.py")):
        for digest in HEX.findall(path.read_text(encoding="utf-8")):
            if digest in indexed or digest in NOT_A_PREREGISTRATION:
                continue
            loose.setdefault(digest, set()).add(str(path.relative_to(REPOSITORY)))
    assert not loose, {one: sorted(two) for one, two in loose.items()}


def test_the_exemptions_are_named_and_few() -> None:
    """المستثنى يُسمّى بسببه — ولا يُتوسَّع فيه."""

    assert len(NOT_A_PREREGISTRATION) <= 8
    for digest, why in NOT_A_PREREGISTRATION.items():
        assert len(digest) == 64 and HEX.fullmatch(digest)
        assert len(why) > 20 and "—" in why


def test_a_digest_of_nothing_is_never_silently_accepted_as_provenance() -> None:
    """بصمةُ اللاشيء في خانة بصمةٍ عطلٌ — ويُعلَن حيثما وقع.

    `e3b0c442…` هي `sha256(b"")`. فوجودُها في خانةٍ يُفترَض أنّها إسنادُ
    مادّةٍ يعني أنّ **البايتاتِ لم تُبصَم قطّ**، وأنّ الحقلَ مُلئ بلا قياس.
    ولا يُحذَف السجلُّ ولا تُعدَّل أرقامُه — **يُوسَم**، ويُمنَع الصامتُ منه.
    """

    assert EMPTY == ("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    assert EMPTY in NOT_A_PREREGISTRATION
    assert "عطلٌ مُعلَنٌ لا إسناد" in NOT_A_PREREGISTRATION[EMPTY]
    carriers = {
        str(path.relative_to(REPOSITORY))
        for path in sorted(TESTS.rglob("*.py"))
        if EMPTY in path.read_text(encoding="utf-8")
    }
    assert carriers == {
        "tests/algebra/test_schema_transition_preregistration.py",
        "tests/algebra/test_seal_index.py",
        "tests/arabic/test_schema_transition_run.py",
    }, sorted(carriers)


def test_every_exemption_is_witnessed_in_the_tree_not_typed() -> None:
    """المستثنى يجب أن **يوجد** فعلًا — فبصمةٌ تُكتَب بيدٍ لا تُصادَف.

    كتبتُ ذيلَ بصمةٍ من عرضٍ مقطوعٍ بدل نسخها، فخرجت بصمةٌ لا وجودَ لها.
    فالشرطُ: كلُّ مستثنًى **مشهودٌ في ملفٍّ آخر** من الشجرة، وإلّا فهو
    مُختلَق — **ولا يُستثنى ما لا يوجد**.
    """

    seen: set[str] = set()
    here = Path(__file__).resolve()
    for path in sorted(REPOSITORY.rglob("*")):
        if not path.is_file() or any(
            one in path.parts for one in (".git", "__pycache__")
        ):
            continue
        if path.suffix not in {".py", ".md", ".log", ".txt"} or path.resolve() == here:
            continue
        try:
            seen |= set(HEX.findall(path.read_text(encoding="utf-8")))
        except (UnicodeDecodeError, OSError):
            continue
    invented = sorted(one for one in NOT_A_PREREGISTRATION if one not in seen)
    assert not invented, invented
