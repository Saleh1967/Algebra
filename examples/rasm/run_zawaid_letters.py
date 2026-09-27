"""حروفُ الزيادة ومجموعاتُ الوظيفة — تشغيلُ ختم `aaf77e3d…`.

ثلاثُ مجموعات بالحرف بعد الطيّ: ز «سألتمونيها»، وم الملتصقُ غيرُ الزائد (ب ف
ك)، وأ الأصليُّ وحده. والحرفُ المكتوب يُعَدّ مرّةً (يُطرَح شطرُ الشدّة الأوّل).
ويُطبَع مع الشروط وصفًا مصفوفةُ ماركوف بين المجموعات داخلَ اللفظ.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
MARKUP = "<sel>"
ZAWAID = set("استلمونيه")
ATTACHED = set("بفك")
LONG = 7
CEILING = 5
GROUPS = ("ز", "م", "أ")


def _peeler() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "run_cv_peel", RASM / "run_cv_peel.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def group(letter: str) -> str:
    if letter in ZAWAID:
        return "ز"
    if letter in ATTACHED:
        return "م"
    return "أ"


def letters(text: str) -> list[str]:
    """حروفُ كلّ لفظٍ بتكراره، مجموعاتٍ — لفظًا لفظًا."""

    peeler = _peeler()
    out: list[str] = []
    for line in text.split("\n"):
        for token in line.replace(MARKUP, " ").split():
            units, extras = peeler.peel(token)
            kept = [
                letter
                for (letter, _), extra in zip(units, extras, strict=True)
                if letter != peeler.STRUCTURE
                and extra.get("تنوين") != "ذيل"
                and extra.get("شدّة") != "نعم"
            ]
            if kept:
                out.append("".join(group(one) for one in kept))
    return out


def _at_most(n: int, p: float, k: int) -> float:
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k + 1))


def measures(words: list[str]) -> dict[str, float | int]:
    """الشروطُ الثلاثة وما تحتاجه."""

    total = Counter("".join(words))
    p = (total["م"] + total["أ"]) / sum(total.values())
    long_words = [one for one in words if len(one) >= LONG]
    under = sum(1 for one in long_words if one.count("م") + one.count("أ") <= CEILING)
    expected = sum(_at_most(len(one), p, CEILING) for one in long_words) / len(
        long_words
    )
    starts = [one for one in words if len(one) >= 2]
    radical_first = sum(1 for one in starts if one[0] == "أ")
    radical_share = total["أ"] / sum(total.values())
    return {
        "words": len(words),
        "letters": sum(total.values()),
        "p": p,
        "long": len(long_words),
        "under": under,
        "share": under / len(long_words),
        "expected": expected,
        "starts": len(starts),
        "radical_first": radical_first,
        "radical_share": radical_share,
        "first_share": radical_first / len(starts),
    }


def markov(words: list[str]) -> tuple[Counter[str], Counter[tuple[str, str]]]:
    """الحالُ الابتدائيّة والانتقالاتُ بين المجموعات داخلَ اللفظ."""

    first: Counter[str] = Counter(one[0] for one in words)
    moves: Counter[tuple[str, str]] = Counter()
    for one in words:
        moves.update(zip(one, one[1:]))
    return (first, moves)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    words = letters(given.text.read_text(encoding="utf-8").rstrip("\n"))
    m = measures(words)
    print(f"ألفاظ {m['words']} | حروف {m['letters']} | نسبة م وأ {m['p']:.4f}")
    print(f"س١: {m['under']}/{m['long']} = {m['share']:.4f}")
    gap = m["share"] - m["expected"]
    print(f"س٢: ذو الحدّين {m['expected']:.4f} | الزيادة {gap:.4f}")
    first_gap = m["radical_share"] - m["first_share"]
    print(
        f"س٣: أ في الحروف {m['radical_share']:.4f} | أوّلًا {m['first_share']:.4f}"
        f" | الفرق {first_gap:.4f}"
    )
    first, moves = markov(words)
    total = Counter("".join(words))
    print("\nالحالُ الابتدائيّة:", {g: round(first[g] / len(words), 4) for g in GROUPS})
    print("النسبُ في الحروف:", {g: round(total[g] / m["letters"], 4) for g in GROUPS})
    for g in GROUPS:
        out = sum(moves[(g, h)] for h in GROUPS)
        row = {h: round(moves[(g, h)] / out, 4) for h in GROUPS}
        print(f"من {g}: {row}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
