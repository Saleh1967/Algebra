"""الثنائيّ `src/entry.py::licensed` هو `Harf.binB` في Lean (ADR ٤)، على كلّ كلمةٍ من خانةٍ أو خانتين، وكلّ كلمةٍ من ثلاثٍ حواملُها من «ء ا ب ل».

الجدولُ `formal/binary.csv` مولَّدٌ بـ`lake exe harf-table` ومطابَقٌ في CI (`git diff --exit-code`)؛ و`entry.licensed`
كُتب قبله، فهو شاهدٌ لا مرآة. الطفرة `MUTANT_ADJACENT_SUKUN_ALLOWED` (ثنائيٌّ يقبل ساكنين متجاورين) تخالف الجدول.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import entry  # noqa: E402

TABLE = ROOT / "formal" / "binary.csv"


def _rows() -> list[tuple[list[str], bool]]:
    out = []
    for line in TABLE.read_text(encoding="utf-8").splitlines():
        word, val = line.rsplit(",", 1)
        out.append((word.split(" "), val == "true"))
    return out


def test_table_is_entry_licensed() -> None:
    rows = _rows()
    assert len(rows) == 116 + 116 * 116 + 16 ** 3
    for atoms, expected in rows:
        assert entry.licensed(entry.from_atoms(atoms)) == expected, atoms
    assert sum(1 for _, v in rows if v) == 87 + 87 * 116 + 12 * (4 * 12 + 12 * 16)


def test_mutant_is_caught() -> None:
    def mutant(cells: tuple[tuple[str, str], ...]) -> bool:  # MUTANT_ADJACENT_SUKUN_ALLOWED
        return not cells or cells[0][1] != "سكون"

    wrong = [a for a, v in _rows() if mutant(entry.from_atoms(a)) != v]
    assert ["بَ", "لْ", "بْ"] in wrong and ["بَ", "لْ"] not in wrong
