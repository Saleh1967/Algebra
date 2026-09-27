"""قرارُ الضمير بياء المثنّى والصيغة المعربة والتراجع، والحَكَمُ QAC — تشغيلُ ختم `8bf5fda5…`.

كلُّ تعريفٍ هنا نصُّ الاستخراج في الختم؛ والمجتمعُ والموانعُ من `run_paradigm_lexicon`.
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
FATHA = "َ"
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


PARADIGM = _load("run_paradigm_lexicon")
GREEDY, JAZM, JARR, QACRUN = (
    PARADIGM.GREEDY,
    PARADIGM.JAZM,
    PARADIGM.JARR,
    PARADIGM.QACRUN,
)
PRONOUNS = JARR.PRONOUNS


class Lexicon:
    """L وLv وR(p)، تُبنى بالإدراج."""

    def __init__(self) -> None:
        self.words: set[str] = set()
        self.declined: set[str] = set()
        self.num: Counter[str] = Counter()
        self.den: Counter[str] = Counter()

    def paradigm(self, stem: str) -> int:
        return (stem in self.declined) + sum(
            1 for e in PRONOUNS if stem + e in self.words
        )

    def rate(self, p: str) -> Fraction:
        return Fraction(self.num[p], self.den[p]) if self.den[p] else Fraction(0)

    def count(self, token: str) -> None:
        """يُحسب نموذجُ اللفظ بالمعجم كما هو الآن، ثم يُدرج."""

        if not PARADIGM.barred(token):
            for p, stem in _accepted(token):
                self.den[p] += 1
                self.num[p] += self.paradigm(stem) >= 2

    def insert(self, token: str) -> None:
        kept = JAZM.units(token)
        letters = JAZM.skeleton(kept)
        self.words.add(letters)
        if kept and kept[-1][0][1] in VOWELS:
            self.declined.add(letters)


def _accepted(token: str) -> list[tuple[str, str]]:
    kept = [(u, e) for u, e in JAZM.units(token) if e.get("شدّة") != "نعم"]
    letters = "".join(u[0] for u, _ in kept)
    found = []
    for p in PRONOUNS:
        stem = letters[: len(letters) - len(p)]
        if not letters.endswith(p) or len(stem) < 2:
            continue
        index = len(kept) - len(p) - 1
        (letter, state), extra = kept[index]
        ok = state in VOWELS
        ok = ok or (letter in "اوي" and extra.get("سكون") == "عارٍ")
        ok = ok or (
            letter == "ي"
            and extra.get("سكون") == "مكتوب"
            and index >= 1
            and kept[index - 1][0][1] == FATHA
        )
        if ok:
            found.append((p, stem))
    return found


def choose(token: str, lexicon: Lexicon) -> str | None:
    if PARADIGM.barred(token):
        return None
    accepted = _accepted(token)
    for p, stem in accepted:
        if lexicon.paradigm(stem) >= 2:
            return p
    for p, _stem in accepted:
        if lexicon.rate(p) >= Fraction(1, 2):
            return p
    return None


def census(text: str, qac_path: Path) -> dict[str, object]:
    qac = QACRUN.read_qac(qac_path)
    order = sorted(qac)
    lines = text.split("\n")
    stream = [t for line in lines for t in line.replace("<sel>", " ").split()]
    full = Lexicon()
    for token in stream:
        full.insert(token)
    for token in stream:
        full.count(token)
    online = Lexicon()
    rows: list[tuple[bool, bool]] = []
    phantom = 0
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
                    letters.endswith(p) and len(letters) >= len(p) + 2 for p in PRONOUNS
                )
                if noun is not None and candidate:
                    off_choice = choose(token, full)
                    off = off_choice == noun[1]
                    on = choose(token, online) == noun[1]
                    rows.append((on, off))
                    if not off:
                        misses[token] += 1
                        phantom += off_choice is not None and noun[1] is None
            online.count(token)
            online.insert(token)
    on_total = sum(a for a, _ in rows)
    off_total = sum(b for _, b in rows)
    return {
        "n": len(rows),
        "online": on_total,
        "offline": off_total,
        "ratio": Fraction(on_total, off_total),
        "phantom": phantom,
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
    print(f"ط١ الكامل: {off}/{n} = {off / n:.4f} | الفوريّ: {on}/{n} = {on / n:.4f}")
    ratio = found["ratio"]
    assert isinstance(ratio, Fraction)
    print(f"ط٢ النسبة: {float(ratio):.4f} | ط٣ ضمائرُ متوهَّمة: {found['phantom']}")
    print("أكثرُ خطأ الكامل:", found["misses"].most_common(20))  # type: ignore[attr-defined]
    return 0


if __name__ == "__main__":
    sys.exit(main())
