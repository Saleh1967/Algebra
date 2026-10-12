"""الشاهدُ المستقلّ (ADR ٣): `formal/Harf` لا يستورد نواةَ الغانم، والجسرُ وحدَه يقرأ الطرفين.

١. كلُّ `import` في `formal/Harf.lean` و`formal/Harf/*.lean` من `Harf.*` وحدَه.
٢. الطفرة `MUTANT_HARF_IMPORTS_A116`: ملفٌّ في `Harf/` يستورد `A116.Hadd` يُلتقط.
٣. الجسرُ يستورد الطرفين، والاعتمادُ على الغانم مثبَّتٌ بنقطةٍ بعينها في `lakefile.toml`.
٤. `Audit.lean` يذكر مبرهنتي التكافؤ والطفرة بأسمائها.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "formal"
IMPORT = re.compile(r"^import\s+(\S+)", re.M)


def foreign_imports(files: list[Path]) -> list[tuple[str, str]]:
    out = []
    for f in files:
        for m in IMPORT.finditer(f.read_text(encoding="utf-8")):
            if not (m.group(1) == "Harf" or m.group(1).startswith("Harf.")):
                out.append((f.name, m.group(1)))
    return out


def harf_files() -> list[Path]:
    return [FORMAL / "Harf.lean", *sorted((FORMAL / "Harf").glob("*.lean"))]


def test_harf_imports_only_harf() -> None:
    files = harf_files()
    assert len(files) == 9
    assert foreign_imports(files) == []


def test_mutant_import_is_caught(tmp_path: Path) -> None:
    planted = tmp_path / "Planted.lean"
    planted.write_text("import Harf.Khana\nimport A116.Hadd\n", encoding="utf-8")
    assert foreign_imports([planted]) == [("Planted.lean", "A116.Hadd")]


def test_bridge_reads_both_and_pin_is_fixed() -> None:
    bridge = (FORMAL / "HarfBridge" / "Takafu.lean").read_text(encoding="utf-8")
    imports = IMPORT.findall(bridge)
    assert "Harf" in imports and "A116.Hadd" in imports
    lake = (FORMAL / "lakefile.toml").read_text(encoding="utf-8")
    assert re.search(r'rev = "[0-9a-f]{40}"', lake)
    assert 'subDir = "formal/a116"' in lake


def test_audit_names_the_equivalences() -> None:
    audit = (FORMAL / "Audit.lean").read_text(encoding="utf-8")
    for t in ("HarfBridge.wasl_eq_strictB", "HarfBridge.waqf_eq_strictPauseB",
              "HarfBridge.mutant_refuted", "HarfBridge.proj_bijective",
              "Harf.factor_through_mahw", "Harf.licence_not_through_mahw",
              "HarfBridge.line_eq_strictLineB", "HarfBridge.lineWaqf_eq_strictLinePauseB",
              "HarfBridge.join_eq_strictJoinB", "HarfBridge.joinWaqf_eq_strictJoinPauseB",
              "HarfBridge.line_mutant_refuted", "HarfBridge.binB_eq_strict", "Harf.binB_eq",
              "HarfBridge.line_eq_pairwise", "HarfBridge.pairwise_needs_vowel_start",
              "HarfBridge.empty_word_smuggles_straddle", "HarfBridge.lineN_eq_strictLineN",
              "Harf.line_eq_pairs", "Harf.lineB_erase_empty",
              "Harf.dep_eq", "Harf.rawOK_needed", "Harf.freeFirst_needed",
              "HarfBridge.deposit_eq_line", "HarfBridge.deposit_needs_raw",
              "HarfBridge.deposit_needs_free", "Harf.dep_eq_waqf", "Harf.line_mix",
              "HarfBridge.deposit_eq_line_pause", "HarfBridge.deposit_needs_raw_pause",
              "Harf.dep_sync", "Harf.dep_shape_waqf", "HarfBridge.deposit_eq_line_shape",
              "HarfBridge.deposit_eq_line_shape_wasl", "HarfBridge.deposit_needs_vowel_after_madd",
              "HarfBridge.segment_eq_line", "HarfBridge.segment_eq_line_wasl"):
        assert f"#print axioms {t}\n" in audit, t
