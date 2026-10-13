"""بوّابةُ المدلول وحده (ADR ٩): الاستقلالُ عن نواة الغانم، والجدولُ مرآةً، والشواهدُ بأسمائها.

١. كلُّ `import` في `formal/Madlul.lean` و`formal/Madlul/*.lean` من `Madlul.*` وحدَه؛ والطفرة
   `MUTANT_MADLUL_IMPORTS_A116` تُلتقط.
٢. `formal/madlul.csv` (يطبعه `lake exe madlul-table`، ويطابَق في CI) هو `src/madlul.py` على المودَع الصغير
   نفسِه؛ وصفوفٌ مكتوبةٌ باليد من نصّ القسمة، لا من الشيفرة.
٣. ثلاثُ طفرات: `MUTANT_MUHMAL_FROM_ABSENCE` (الغيابُ إهمال)، `MUTANT_ONE_WORD_MURAKKAB` (لفظٌ واحدٌ
   مركّب)، `MUTANT_EXIT_REVERSES` (المخرجُ يعكس الألفاظ) — كلٌّ يخالف الجدول.
٤. لكلّ قسمٍ ولكلّ نوعٍ من المعنى شاهدٌ في `formal/Madlul/Shawahid.lean`، وAudit يذكر المبرهنات بأسمائها.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Callable, Hashable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "formal"
sys.path.insert(0, str(ROOT / "src"))

import madlul as M  # noqa: E402

IMPORT = re.compile(r"^import\s+(\S+)", re.M)
TABLE = FORMAL / "madlul.csv"


def _foreign(files: list[Path]) -> list[tuple[str, str]]:
    out = []
    for f in files:
        for m in IMPORT.finditer(f.read_text(encoding="utf-8")):
            if not (m.group(1) == "Madlul" or m.group(1).startswith("Madlul.")):
                out.append((f.name, m.group(1)))
    return out


def test_madlul_imports_only_madlul(tmp_path: Path) -> None:
    files = [FORMAL / "Madlul.lean", *sorted((FORMAL / "Madlul").glob("*.lean"))]
    assert len(files) == 2
    assert _foreign(files) == []
    planted = tmp_path / "Planted.lean"  # MUTANT_MADLUL_IMPORTS_A116
    planted.write_text("import Madlul.Shawahid\nimport A116.Wad\n", encoding="utf-8")
    assert _foreign([planted]) == [("Planted.lean", "A116.Wad")]


# المودَعُ الصغير كما في `formal/MadlulMain.lean` (d0)
NAW0 = {0: ("jins", 20), 1: ("damir", 21)}
ISTI0 = {(0,): ("mustamal", 10), (1,): ("muhmal", 11), (0, 1): ("mustamal", 12),
         (1, 1): ("muhmal", 13), (0, 1, 2): ("muhmal", 14)}


def _d0(isti: Callable[[tuple[Hashable, ...]], tuple[str, Hashable] | None] | None = None) -> M.Mawda:
    return M.Mawda(naw=NAW0.get, isti=isti or ISTI0.get)


def _lists(k: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = [()]
    for _ in range(k):
        out = [ls + (x,) for ls in out for x in (0, 1, 2)]
    return out


def _refs() -> list[M.Ref]:
    return [("N", n) for n in (0, 1, 2)] + [("L", ls) for k in range(4) for ls in _lists(k)]


def _row(d: M.Mawda, ref: M.Ref, exit_ref: Callable[[M.Madlul], M.Ref] = M.exit_ref) -> str:
    tag, x = ref
    rs = f"N:{x}" if tag == "N" else "L:" + " ".join(map(str, x))  # type: ignore[call-overload]
    o = M.enter(d, ref)
    if isinstance(o, M.Rafd):
        return f"{rs}\trafd:{o.name}\t-\t-"
    if o.kind == "maana":
        out = f"maana:{o.ref}:{o.sub}:{o.witness}"
    elif o.kind == "mufrad":
        out = f"mufrad:{o.ref}:{o.sub}:{o.witness}"
    else:
        out = "murakkab:" + " ".join(map(str, o.ref)) + f":{o.sub}:{o.witness}"  # type: ignore[call-overload]
    back = "back" if exit_ref(o) == (tag, x if tag == "N" else tuple(x)) else "LOST"  # type: ignore[arg-type]
    return f"{rs}\t{out}\t{M.qism(o)}\t{back}"


def _table() -> list[str]:
    return TABLE.read_text(encoding="utf-8").splitlines()


def test_table_is_the_mirror() -> None:
    rows = _table()
    assert len(rows) == 3 + 1 + 3 + 9 + 27
    assert rows == [_row(_d0(), r) for r in _refs()]


def test_rows_by_hand() -> None:
    rows = {r.split("\t")[0]: r.split("\t")[1:] for r in _table()}
    assert rows["N:0"] == ["maana:0:jins:20", "maana", "back"]
    assert rows["N:2"] == ["rafd:MAANA_WITHOUT_WITNESS", "-", "-"]
    assert rows["L:"] == ["rafd:EMPTY_LAFZ_REF", "-", "-"]
    assert rows["L:1"] == ["mufrad:1:muhmal:11", "mufradMuhmal", "back"]
    # لا شاهدَ لـ«2»: يُرفض ولا يُحكم بإهماله
    assert rows["L:2"] == ["rafd:ISTI_WITHOUT_WITNESS", "-", "-"]
    assert rows["L:1 1"] == ["murakkab:1 1:muhmal:13", "murakkabMuhmal", "back"]
    assert rows["L:0 1 2"] == ["murakkab:0 1 2:muhmal:14", "murakkabMuhmal", "back"]
    assert all(r.endswith("\tback") or r.endswith("\t-") for r in _table())
    assert not any("LOST" in r for r in _table())


def test_mutants_are_caught() -> None:
    table = _table()

    def absent_is_muhmal(ls: tuple[Hashable, ...]) -> tuple[str, Hashable] | None:
        return ISTI0.get(ls) or ("muhmal", 0)  # type: ignore[arg-type]

    assert [_row(_d0(absent_is_muhmal), r) for r in _refs()] != table  # MUTANT_MUHMAL_FROM_ABSENCE

    old = M.enter

    def one_word_murakkab(d: M.Mawda, ref: M.Ref) -> M.Madlul | M.Rafd:
        o = old(d, ref)
        if isinstance(o, M.Madlul) and o.kind == "mufrad":
            return M.Madlul("murakkab", (o.ref,), o.sub, o.witness)
        return o

    M.enter = one_word_murakkab  # type: ignore[assignment]  # MUTANT_ONE_WORD_MURAKKAB
    try:
        assert [_row(_d0(), r) for r in _refs()] != table
    finally:
        M.enter = old

    def reversed_exit(m: M.Madlul) -> M.Ref:
        tag, x = M.exit_ref(m)
        return (tag, tuple(reversed(x))) if tag == "L" else (tag, x)  # type: ignore[call-overload]

    assert [_row(_d0(), r, reversed_exit) for r in _refs()] != table  # MUTANT_EXIT_REVERSES


def test_every_kind_has_a_witness_line() -> None:
    text = (FORMAL / "Madlul" / "Shawahid.lean").read_text(encoding="utf-8")
    for key in (*M.QISM, *M.NAW, "taqsim"):
        assert re.search(rf'\("{key}", ⟨"shakhsiyya-3", 4\d\d, "', text), key
    # المهملُ بشاهدٍ موجِب من نصّه، لا من الغياب
    assert "ضه، وره، وبه، لم توضع لمعنى" in text and "غير موضوع، أي لم تضعه العرب" in text


def test_audit_names_the_theorems() -> None:
    audit = (FORMAL / "Audit.lean").read_text(encoding="utf-8")
    for t in ("exit_enter", "enter_exit", "enter_agrees", "absence_refused", "muhmal_needs_witness",
              "mufrad_iff_single", "maana_iff_node", "qism_mem_all", "all_nodup",
              "every_qism_witnessed", "every_naw_witnessed"):
        assert f"#print axioms Madlul.{t}" in audit, t
