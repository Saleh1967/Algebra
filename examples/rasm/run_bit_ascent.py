"""من البتّات إلى الطبقات: صعودٌ حرٌّ وهبوطٌ مرصودٌ بالرسم — تشغيلُ ختم `149af813…`.

كلُّ تعريفٍ هنا نصُّ الاستخراج في الختم. والمتعلِّمُ جدولُ مفاتيح: لكلّ مفتاحٍ (بتّاتٌ قبل
الموضع وبعده) حصّةُ الحدّ في التعلّم، ويُتراجع إلى مفتاحٍ أقصر إن لم يُرَ.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
STATES = {"َ": (0, 0), "ُ": (0, 1), "ِ": (1, 0)}
SUKUN = (1, 1)
LEVELS = ("الوحدة", "المقطع", "الكلمة", "الوقف", "الآية")
ORDERS = ("الحرف أوّلًا", "الحال أوّلًا")
DIRECTIONS = ("صعود", "عكس")
LOOKAHEADS = (0, 1, 2, 7)
HISTORY = (21, 14, 7, 0)
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()


def _peeler() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "run_cv_peel", RASM / "run_cv_peel.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئ")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def stream(text: str) -> tuple[dict[str, list[int]], list[int], list[int]]:
    """(البتّاتُ بالترتيبين، وقناعُ الحدود بالطبقات لكلّ موضع، ورقمُ سطر كلّ بتّ).

    قناعُ الموضع t عددٌ بخمس بتّات: البتّةُ i مرفوعةٌ إن كان قبل t حدٌّ في الطبقة i.
    """

    peeler = _peeler()
    units: list[tuple[str, tuple[int, int]]] = []
    starts: list[tuple[bool, bool, bool, bool]] = []  # مقطع، كلمة، وقف، آية
    lines: list[int] = []
    letters: set[str] = set()
    for number, line in enumerate(text.split("\n"), start=1):
        for s_index, segment in enumerate(line.split("<sel>")):
            for w_index, token in enumerate(segment.split()):
                peeled, _ = peeler.peel(token)
                kept = [u for u in peeled if u[0] != peeler.STRUCTURE]
                for u_index, (letter, state) in enumerate(kept):
                    first_word = u_index == 0
                    units.append((letter, STATES.get(state, SUKUN)))
                    letters.add(letter)
                    starts.append(
                        (
                            first_word or state in STATES,
                            first_word,
                            first_word and w_index == 0,
                            first_word and w_index == 0 and s_index == 0,
                        )
                    )
                    lines.append(number)
    rank = {letter: i for i, letter in enumerate(sorted(letters))}
    assert len(rank) == 28
    letter_first: list[int] = []
    state_first: list[int] = []
    for letter, state in units:
        lb = [(rank[letter] >> (4 - i)) & 1 for i in range(5)]
        sb = list(state)
        letter_first.extend(lb + sb)
        state_first.extend(sb + lb)
    masks = [0] * (7 * len(units))
    for i, flags in enumerate(starts):
        if i == 0:
            continue
        mask = 1
        for level in range(4):
            if flags[level]:
                mask |= 1 << (level + 1)
        masks[7 * i] = mask
    line_of = [n for n in lines for _ in range(7)]
    return {ORDERS[0]: letter_first, ORDERS[1]: state_first}, masks, line_of


def _keys(bits: list[int], before: int, after: int, first: int, last: int) -> list[int]:
    """مفتاحُ كلّ t من first إلى last: البتّاتُ before قبلها وafter بعدها، عددًا صحيحًا."""

    width = before + after
    count = last - first + 1
    if width == 0:
        return [0] * count
    start = first - before
    mask = (1 << width) - 1
    key = 0
    for i in range(width):
        key = (key << 1) | bits[start + i]
    out = [key]
    for s in range(start + 1, start + count):
        key = ((key << 1) & mask) | bits[s + width - 1]
        out.append(key)
    return out


def evaluate(
    bits: list[int], masks: list[int], line_of: list[int], k: int
) -> list[Fraction]:
    length = len(bits)
    first, last = HISTORY[0], min(length - k, length - 1)
    positions = range(first, last + 1)
    train = [line_of[t] % 2 == 0 for t in positions]
    truth = [masks[t] for t in positions]
    predicted: list[int | None] = [None] * len(train)
    for before in HISTORY:
        keys = _keys(bits, before, k, first, last)
        table: dict[int, list[int]] = {}
        for i, key in enumerate(keys):
            if train[i]:
                row = table.get(key)
                if row is None:
                    row = table[key] = [0, 0, 0, 0, 0, 0]
                row[0] += 1
                m = truth[i]
                if m:
                    for level in range(5):
                        if m >> level & 1:
                            row[level + 1] += 1
        for i, key in enumerate(keys):
            if train[i] or predicted[i] is not None:
                continue
            row = table.get(key)
            if row is None:
                continue
            vote = 0
            for level in range(5):
                if row[level + 1] * 2 > row[0]:
                    vote |= 1 << level
            predicted[i] = vote
    counts = [[0, 0, 0] for _ in range(5)]  # tp, fp, fn
    for i in range(len(train)):
        if train[i]:
            continue
        guess = predicted[i] or 0
        real = truth[i]
        for level in range(5):
            g, r = guess >> level & 1, real >> level & 1
            if g and r:
                counts[level][0] += 1
            elif g:
                counts[level][1] += 1
            elif r:
                counts[level][2] += 1
    return [
        Fraction(2 * tp, 2 * tp + fp + fn) if tp + fp + fn else Fraction(1)
        for tp, fp, fn in counts
    ]


def census(text: str) -> dict[tuple[str, str, int], list[Fraction]]:
    bits, masks, line_of = stream(text)
    length = len(masks)
    table: dict[tuple[str, str, int], list[Fraction]] = {}
    for order in ORDERS:
        for direction in DIRECTIONS:
            b, m, lines = bits[order], masks, line_of
            if direction == DIRECTIONS[1]:
                b = b[::-1]
                m = [0] + [masks[length - t] for t in range(1, length)]
                lines = line_of[::-1]
            for k in LOOKAHEADS:
                table[(order, direction, k)] = evaluate(b, m, lines, k)
    return table


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    table = census(given.text.read_text(encoding="utf-8").rstrip("\n"))
    print("الترتيب | الاتّجاه | k | " + " | ".join(LEVELS))
    for (order, direction, k), row in table.items():
        print(
            f"{order} | {direction} | {k} | "
            + " | ".join(f"{float(x):.4f}" for x in row)
        )
    lf, sf = ORDERS
    print("ب١", f"{float(table[(lf, 'صعود', 1)][0]):.4f}")
    print("ب٢", f"{float(table[(sf, 'صعود', 2)][1]):.4f}")
    print("ب٣", f"{float(table[(lf, 'صعود', 2)][1]):.4f}")
    print("ب٤", f"{float(table[(sf, 'صعود', 1)][2]):.4f}")
    print("ب٥", f"{float(table[(sf, 'صعود', 7)][2] - table[(sf, 'صعود', 1)][2]):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
