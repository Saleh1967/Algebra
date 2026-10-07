"""فهرسُ السور — تشغيلُ ختم `eb26eef8…`.

**العلامةُ تُقرَأ من الشجرة لا تُكتَب ههنا**: هيكلُ البسملة الرباعيُّ
`HEAD` في `examples/rasm/run_basmala_lifted.py` — المادّةُ ٩: لا يدخل
قياسًا حرفٌ طبعناه.

**والقسمة**: سطرٌ تبتدئه الكلماتُ الأربعُ (بهياكلها) **رأسُ كتلة**، وما
بعده حتّى الرأس التالي كتلةٌ واحدة. **ولا يُرقَّم رأسٌ برقم سورة**: أنّ
السورَ ١١٤ **معلومٌ من خارجٍ لا مقيسٌ ههنا**، فالحدُّ الذي لا علامةَ له
**يُصنَّف `UNATTESTED` ولا يُخترَع له موضع**.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
LIFTED = REPOSITORY / "examples" / "rasm" / "run_basmala_lifted.py"
SURAHS_KNOWN_FROM_OUTSIDE = 114


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def bare(one: str) -> str:
    return "".join(c for c in one if unicodedata.category(c) != "Mn")


def heads_of(lines: list[str], head: list[str]) -> tuple[list[int], list[int]]:
    """(مواضعُ الرؤوس، مواضعُ الرؤوس القائمةِ بنفسها) — بالهياكل لا بالضبط."""

    starts: list[int] = []
    alone: list[int] = []
    for index, line in enumerate(lines):
        pieces = line.split()
        if (
            len(pieces) >= len(head)
            and [bare(one) for one in pieces[: len(head)]] == head
        ):
            starts.append(index)
            if len(pieces) == len(head):
                alone.append(index)
    return (starts, alone)


def elsewhere(lines: list[str], head: list[str]) -> list[int]:
    """أسطرٌ تحمل الكلماتِ الأربعَ متتالياتٍ **في غير موضع الابتداء**."""

    found: list[int] = []
    width = len(head)
    for index, line in enumerate(lines):
        pieces = [bare(one) for one in line.split()]
        for place in range(1, max(len(pieces) - width + 1, 1)):
            if pieces[place : place + width] == head:
                found.append(index)
                break
    return found


def blocks_of(starts: list[int], total: int) -> list[tuple[int, int]]:
    """(أوّلُ سطرٍ، طولٌ) لكلّ كتلة — ورأسُها منها."""

    edges = [*starts, total]
    return [(edges[one], edges[one + 1] - edges[one]) for one in range(len(starts))]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    lifted = _load(LIFTED, "run_basmala_lifted")
    head: list[str] = list(lifted.HEAD)  # type: ignore[attr-defined]
    lines = [
        one
        for one in given.text.read_text(encoding="utf-8").splitlines()
        if one.strip()
    ]

    print(f"— الأسطر: {len(lines)}")
    print(f"— العلامة: {len(head)} كلماتٍ بهياكلها، مقروءةً من run_basmala_lifted.HEAD")

    starts, alone = heads_of(lines, head)
    aside = elsewhere(lines, head)
    print(f"— رؤوسُ الكتل: {len(starts)}")
    print(f"  منها قائمةٌ بنفسها: {len(alone)} | وملحَقةٌ: {len(starts) - len(alone)}")
    print(f"  وأسطرٌ تحمل العلامةَ غيرَ مبتدأةٍ بها: {len(aside)}")
    if aside:
        print(
            "  ومواضعُها (أرقامُ أسطرٍ من واحد): "
            + ", ".join(str(one + 1) for one in aside)
        )
    if alone:
        print(f"  وموضعُ القائمةِ بنفسها: {', '.join(str(one + 1) for one in alone)}")

    if not starts or starts[0] != 0:
        print("  وأوّلُ سطرٍ ليس رأسًا — فالأسطرُ قبل أوّل رأسٍ خارجُ القسمة")

    table = blocks_of(starts, len(lines))
    covered = sum(length for _, length in table)
    outside = len(lines) - covered
    print()
    print("— الكتل")
    print(f"  عددُها: {len(table)}")
    print(f"  مجموعُ أطوالها: {covered} | وأسطرٌ خارجَ كتلةٍ: {outside}")
    lengths = [length for _, length in table]
    print(f"  أقصرُها: {min(lengths)} | أطولُها: {max(lengths)}")
    print(f"  كتلٌ طولُها صفرٌ: {sum(1 for one in lengths if one == 0)}")
    print(f"  كتلٌ طولُها ≤ ٥: {sum(1 for one in lengths if one <= 5)}")
    print(f"  كتلٌ طولُها ٣ بالضبط: {sum(1 for one in lengths if one == 3)}")

    print()
    print("— أطوالُ الكتل بترتيبها (أوّلُ سطرٍ من واحد ← طولٌ)")
    for start, length in table:
        print(f"  {start + 1} ← {length}")

    print()
    print("— الأطولُ خمسًا، والأقصرُ خمسًا")
    ranked = sorted(table, key=lambda one: (-one[1], one[0]))
    for start, length in ranked[:5]:
        print(f"  أطول: سطر {start + 1} ← {length}")
    for start, length in ranked[-5:]:
        print(f"  أقصر: سطر {start + 1} ← {length}")

    spread: Counter[int] = Counter(lengths)
    print()
    print("— توزيعُ الأطوال (طولٌ: كم كتلة)، للأطوال التي تكرّرت")
    for length, number in sorted(spread.items()):
        if number > 1:
            print(f"  {length}: {number}")

    print()
    print("— ما لا يحلُّه البايت")
    missing = SURAHS_KNOWN_FROM_OUTSIDE - len(table)
    print(f"  السورُ معلومةً من خارج: {SURAHS_KNOWN_FROM_OUTSIDE} — **لا مقيسةً ههنا**")
    print(f"  وحدودٌ حلَّها البايت: {len(table)}")
    print(f"  فحدودٌ لا علامةَ لها في البايتات: {missing} — UNATTESTED")
    print("  وحكمُها انعدامُ دليلٍ لا امتناعُ بلوغ: لا يُخترَع لها موضعٌ ولا تُصفَّر")
    print("  ولا يُرقَّم رأسٌ برقم سورة؛ والترقيمُ يحتاج جردًا مُودَعًا")
    return 0


if __name__ == "__main__":
    sys.exit(main())
