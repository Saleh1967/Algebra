"""قرارُ الضمير بموانع الرسم ومعجم الجذوع، والحَكَمُ QAC — تشغيلُ ختم `b904a9f9…`.

المجتمعُ والصوابُ والترتيبُ والمعجمُ كما في `run_online_lexicon`. والاختيارُ نصُّ الختم.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
VOWELS = ("َ", "ُ", "ِ")
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ONLINE = _load("run_online_lexicon")
GREEDY, JAZM, JARR, QACRUN = ONLINE.GREEDY, ONLINE.JAZM, ONLINE.JARR, ONLINE.QACRUN
ENDINGS = ("", *JARR.PRONOUNS)


def barred(token: str) -> bool:
    """موانعُ الرسم: تاءٌ مربوطة، أو «ال»، أو تنوين."""

    kept = JAZM.units(token)
    if JAZM.raw(token).endswith("ة"):
        return True
    if JAZM._after_al(token, kept) is not None:
        return True
    return any(e.get("تنوين") for e in JAZM.PEELER.peel(token)[1])


def choose(token: str, lexicon: set[str]) -> str | None:
    if barred(token):
        return None
    kept = [(u, e) for u, e in JAZM.units(token) if e.get("شدّة") != "نعم"]
    letters = "".join(u[0] for u, _ in kept)
    for one in JARR.PRONOUNS:
        stem = letters[: len(letters) - len(one)]
        if not letters.endswith(one) or len(stem) < 2:
            continue
        (letter, state), extra = kept[len(kept) - len(one) - 1]
        voiced = state in VOWELS or (letter in "اوي" and extra.get("سكون") == "عارٍ")
        if not voiced:
            continue
        if sum(1 for e in ENDINGS if stem + e in lexicon) >= 2:
            return one
    return None


def census(text: str, qac_path: Path) -> dict[str, object]:
    qac = QACRUN.read_qac(qac_path)
    order = sorted(qac)
    lines = text.split("\n")
    offline = {
        JAZM.skeleton(JAZM.units(t))
        for line in lines
        for t in line.replace("<sel>", " ").split()
    }
    seen: set[str] = set()
    rows: list[tuple[bool, bool]] = []
    marbuta_errors = 0
    misses: Counter[str] = Counter()
    for line, key in zip(lines, order, strict=True):
        tokens = line.replace("<sel>", " ").split()
        words = qac[key]
        aligned = len(tokens) == max(words)
        for i, token in enumerate(tokens):
            letters = JAZM.skeleton(JAZM.units(token))
            if aligned:
                noun = GREEDY._noun(words[i + 1])
                candidate = any(
                    letters.endswith(p) and len(letters) >= len(p) + 2
                    for p in JARR.PRONOUNS
                )
                if noun is not None and candidate:
                    off = choose(token, offline) == noun[1]
                    on = choose(token, seen) == noun[1]
                    rows.append((on, off))
                    if not off:
                        misses[token] += 1
                        marbuta_errors += JAZM.raw(token).endswith("ة")
            seen.add(letters)
    on = sum(a for a, _ in rows)
    off = sum(b for _, b in rows)
    return {
        "n": len(rows),
        "online": on,
        "offline": off,
        "ratio": Fraction(on, off),
        "marbuta_errors": marbuta_errors,
        "misses": misses,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--qac", type=Path, required=True)
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"), given.qac)
    n, on, off = found["n"], found["online"], found["offline"]
    assert isinstance(n, int) and isinstance(on, int) and isinstance(off, int)
    print(f"ح١ الكامل: {off}/{n} = {off / n:.4f} | الفوريّ: {on}/{n} = {on / n:.4f}")
    ratio = found["ratio"]
    assert isinstance(ratio, Fraction)
    print(
        f"ح٢ النسبة: {float(ratio):.4f} | ح٣ أخطاءُ المربوطة: {found['marbuta_errors']}"
    )
    print("أكثرُ خطأ الكامل:", found["misses"].most_common(20))  # type: ignore[attr-defined]
    return 0


if __name__ == "__main__":
    sys.exit(main())
