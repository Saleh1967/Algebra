"""الحروفُ المُضافة بين صورتين من ألفاظ المصحف — تشغيلُ ختم `113fc280…`.

الصورةُ سلسلةُ حروف اللفظ بلا حركات (الحرفُ المكتوب مرّة). والزوجُ صورتان
تخرج القصيرةُ منهما من الطويلة بحذف حرفٍ إلى ثلاثة، وتُؤخذ من مواضع الحذف
أصغرُها ترتيبًا. والتعريفاتُ كلُّها نصُّ الاستخراج في الختم.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
MARKUP = "<sel>"
ZAWAID = set("استلمونيه")
ATTACHED = set("بفك")
EXEMPT = set("طد")
SHORTEST = 3
MOST_ADDED = 3


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


def forms(text: str) -> tuple[set[str], Counter[str]]:
    """الصورُ المتميّزة، وعددُ كلّ حرفٍ في ألفاظ المصحف بتكرارها."""

    peeler = _peeler()
    found: set[str] = set()
    letters: Counter[str] = Counter()
    for line in text.split("\n"):
        for token in line.replace(MARKUP, " ").split():
            units, extras = peeler.peel(token)
            kept = "".join(
                letter
                for (letter, _), extra in zip(units, extras, strict=True)
                if letter != peeler.STRUCTURE
                and extra.get("تنوين") != "ذيل"
                and extra.get("شدّة") != "نعم"
            )
            if kept:
                found.add(kept)
                letters.update(kept)
    return (found, letters)


def pairs(found: set[str]) -> list[tuple[str, str, tuple[int, ...]]]:
    """(القصيرة، الطويلة، مواضع الإضافة في الطويلة) — لكلّ زوجٍ مرّة."""

    out: list[tuple[str, str, tuple[int, ...]]] = []
    for longer in found:
        seen: set[str] = set()
        for added in range(1, MOST_ADDED + 1):
            if len(longer) - added < SHORTEST:
                break
            for places in combinations(range(len(longer)), added):
                shorter = "".join(
                    one for i, one in enumerate(longer) if i not in places
                )
                if shorter in found and shorter not in seen:
                    seen.add(shorter)
                    out.append((shorter, longer, places))
    return out


def added_letters(
    found: list[tuple[str, str, tuple[int, ...]]],
) -> list[tuple[str, int, int, bool]]:
    """(الحرف، موضعه، طولُ الطويلة، أهو تكرير) لكلّ حرفٍ مُضاف."""

    out: list[tuple[str, int, int, bool]] = []
    for _, longer, places in found:
        for place in places:
            letter = longer[place]
            left = longer[place - 1] if place > 0 else ""
            right = longer[place + 1] if place + 1 < len(longer) else ""
            out.append((letter, place, len(longer), letter in (left, right)))
    return out


def edge(place: int, length: int) -> bool:
    return place <= 1 or place >= length - 3


def measures(text: str) -> dict[str, object]:
    found, letters = forms(text)
    matched = pairs(found)
    added = added_letters(matched)
    good = sum(
        1 for letter, _, _, repeated in added if letter in ZAWAID | ATTACHED or repeated
    )
    attached = [(p, n) for letter, p, n, _ in added if letter in ATTACHED]
    on_edge = sum(1 for p, n in attached if edge(p, n))
    plain = Counter(letter for letter, _, _, repeated in added if not repeated)
    total_plain = sum(plain.values())
    total_letters = sum(letters.values())
    rate = {
        letter: (plain[letter] / total_plain) / (letters[letter] / total_letters)
        for letter in letters
    }
    lowest_zawaid = min(rate[one] for one in ZAWAID)
    others = [one for one in rate if one not in ZAWAID | ATTACHED | EXEMPT]
    highest_other = max(rate[one] for one in others)
    return {
        "forms": len(found),
        "pairs": len(matched),
        "added": len(added),
        "good": good,
        "attached": len(attached),
        "on_edge": on_edge,
        "rate": rate,
        "lowest_zawaid": lowest_zawaid,
        "highest_other": highest_other,
        "matched": matched,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()
    m = measures(given.text.read_text(encoding="utf-8").rstrip("\n"))
    print(f"صور {m['forms']} | أزواج {m['pairs']} | حروف مُضافة {m['added']}")
    print(f"ز١: {m['good']}/{m['added']} = {m['good'] / m['added']:.4f}")
    print(f"ز٢: {m['on_edge']}/{m['attached']} = {m['on_edge'] / m['attached']:.4f}")
    gap = m["lowest_zawaid"] - m["highest_other"]
    print(
        f"ز٣: أدنى التسعة {m['lowest_zawaid']:.4f}"
        f" | أعلى غيرها {m['highest_other']:.4f} | الفرق {gap:.4f}"
    )
    for letter, value in sorted(m["rate"].items(), key=lambda item: -item[1]):
        print(f"  {letter} {value:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
