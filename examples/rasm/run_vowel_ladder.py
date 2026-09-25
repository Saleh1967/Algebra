"""سلّمُ الضبط بشرط السياق — تشغيلُ ختم `9034199d…`.

**سلّمان**: سلّمُ الرسم `h^A_k = H(s_i | ℓ_{i−k}…ℓ_i)` — ما يضيفه الضبطُ
لقارئٍ يملك الحروفَ وحدَها؛ وسلّمُ الفكّ `h^B_k` يشترط على الحالات السابقة
أيضًا — ما يضيفه لقارئٍ يقرأ متتابعًا.

**القراراتُ المختومة**: مواضعُ الرسم بلا توسيعِ شدّة (المجرّدُ لا شدّةَ فيه)؛
والحروفُ مُطبَّعةٌ بـR2/R7؛ و**السياقُ داخلَ السطر ولا يعبره**؛ وأرضيّةُ قراءة
السياق **ثلاثون وقوعًا**؛ وما سقط سياقُه **يُستبعَد ويُعلَن نصيبُه**؛
و**تصحيحُ ميلر–مادو** على كلّ رتبة.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
AUDIT = REPOSITORY / "examples" / "rasm" / "run_encoding_audit.py"
CONTEXT_FLOOR = 30
ORDERS = (0, 1, 2, 3)
MARKUP = "<sel>"


def _audit() -> object:
    spec = importlib.util.spec_from_file_location("run_encoding_audit", AUDIT)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للمواصفة")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def lines_of_units(text: str) -> list[list[tuple[str, str]]]:
    """مواضعُ الرسم سطرًا سطرًا — فالسياقُ لا يعبر السطر."""

    audit = _audit()
    return [
        audit.rasm_units(line)  # type: ignore[attr-defined]
        for line in text.replace(MARKUP, " ").splitlines()
        if line.strip()
    ]


def contexts(
    lines: list[list[tuple[str, str]]], order: int, with_states: bool
) -> dict[tuple[str, ...], Counter[str]]:
    """توزيعُ الحالة لكلّ سياقٍ من الرتبة المطلوبة."""

    table: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    for units in lines:
        for index in range(order, len(units)):
            window = units[index - order : index + 1]
            key: list[str] = [letter for letter, _ in window]
            if with_states and order:
                key.extend(state for _, state in window[:-1])
            table[tuple(key)][units[index][1]] += 1
    return table


def ladder_step(
    table: dict[tuple[str, ...], Counter[str]],
) -> tuple[float, float, float]:
    """(h المصحَّحة، مقدارُ التصحيح، نصيبُ المقروء) على الأرضيّة المعلنة."""

    readable = {
        key: counts
        for key, counts in table.items()
        if sum(counts.values()) >= CONTEXT_FLOOR
    }
    everything = sum(sum(counts.values()) for counts in table.values())
    mass = sum(sum(counts.values()) for counts in readable.values())
    if not mass:
        return (float("nan"), float("nan"), 0.0)
    plugin = 0.0
    bias = 0.0
    for counts in readable.values():
        total = sum(counts.values())
        weight = total / mass
        plugin += weight * -math.fsum(
            (number / total) * math.log2(number / total) for number in counts.values()
        )
        bias += weight * (len(counts) - 1) / (2 * total * math.log(2))
    return (plugin + bias, bias, mass / everything)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    lines = lines_of_units(given.text.read_text(encoding="utf-8"))
    positions = sum(len(one) for one in lines)
    print(f"أسطر: {len(lines)} | مواضعُ الرسم: {positions}")
    print(f"أرضيّةُ السياق: {CONTEXT_FLOOR} وقوعًا")
    print()
    print("الرتبة |    h^A |  تصحيح | نصيبُ المقروء |    h^B |  تصحيح | نصيبُ المقروء")
    for order in ORDERS:
        rasm = ladder_step(contexts(lines, order, with_states=False))
        decode = ladder_step(contexts(lines, order, with_states=True))
        print(
            f"   {order}   | {rasm[0]:6.4f} | {rasm[1]:6.4f} | {rasm[2]:12.4f} "
            f"| {decode[0]:6.4f} | {decode[1]:6.4f} | {decode[2]:12.4f}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
