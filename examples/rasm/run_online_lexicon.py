"""المعجمُ الفوريّ وغيرُ الفوريّ لقرار الضمير، والحَكَمُ QAC — تشغيلُ ختم `363ee517…`.

المجتمعُ مجتمعُ ج١ في `run_greedy_irab` بتعريفه. والمعجمُ هياكلُ ألفاظٍ تامّة: كلُّها
(غيرُ الفوريّ)، أو ما سبق الموضعَ بترتيب الأسطر ثم الألفاظ (الفوريّ).
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
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


GREEDY = _load("run_greedy_irab")
JAZM, JARR, QACRUN = GREEDY.JAZM, GREEDY.JARR, GREEDY.QACRUN


def choose(letters: str, lexicon: set[str]) -> str | None:
    for one in JARR.PRONOUNS:
        stem = letters[: len(letters) - len(one)]
        if letters.endswith(one) and len(stem) >= 2 and stem in lexicon:
            return one
    return None


def census(text: str, qac_path: Path) -> dict[str, object]:
    qac = QACRUN.read_qac(qac_path)
    order = sorted(qac)
    lines = text.split("\n")
    stream: list[str] = []
    for line in lines:
        stream.extend(
            JAZM.skeleton(JAZM.units(t)) for t in line.replace("<sel>", " ").split()
        )
    offline = set(stream)
    seen: set[str] = set()
    rows: list[tuple[bool, bool]] = []
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
                    truth = noun[1]
                    on = choose(letters, seen) == truth
                    off = choose(letters, offline) == truth
                    rows.append((on, off))
                    if not on:
                        misses[token] += 1
            seen.add(letters)
    n = len(rows)
    quarter = n // 4

    def ratio(part: list[tuple[bool, bool]]) -> Fraction:
        on = sum(a for a, _ in part)
        off = sum(b for _, b in part)
        return Fraction(on, off)

    return {
        "n": n,
        "online": sum(a for a, _ in rows),
        "offline": sum(b for _, b in rows),
        "ratio": ratio(rows),
        "first": ratio(rows[:quarter]),
        "last": ratio(rows[3 * quarter :]),
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
    print(f"ف١ غيرُ الفوريّ: {off}/{n} = {off / n:.4f} | الفوريّ: {on}/{n} = {on / n:.4f}")
    ratio, first, last = found["ratio"], found["first"], found["last"]
    assert isinstance(ratio, Fraction) and isinstance(first, Fraction)
    assert isinstance(last, Fraction)
    print(f"ف٢ النسبة: {float(ratio):.4f}")
    print(
        f"ف٣ الربع الأوّل {float(first):.4f} | الأخير {float(last):.4f} | "
        f"{float(last - first):.4f}"
    )
    print("أكثرُ خطأ الفوريّ:", found["misses"].most_common(15))  # type: ignore[attr-defined]
    return 0


if __name__ == "__main__":
    sys.exit(main())
