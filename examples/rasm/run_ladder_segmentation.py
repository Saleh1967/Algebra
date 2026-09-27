"""الطبقةُ الأولى من السلّم: تقطيعُ الكلمة فوريًّا بالهندسة العكسيّة من QAC — ختم `1b3a639a…`.

كلُّ تعريفٍ هنا نصُّ الاستخراج في الختم.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
STRIP = re.compile("[ً-ٰٟۖ-ۭـ]")
HALF = Fraction(1, 2)
DEPTH = 6
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


JAZM = _load("run_jazm_zero")

Segment = tuple[str, str, list[str]]


def norm(form: str) -> str:
    return STRIP.sub("", form).replace("ٱ", "ا")


def read_qac(path: Path) -> dict[tuple[int, int], dict[int, list[Segment]]]:
    verses: dict[tuple[int, int], dict[int, list[Segment]]] = defaultdict(dict)
    for line in path.read_text(encoding="utf-8").split("\n"):
        if not line.strip():
            continue
        loc, form, pos, feat = line.split("\t")
        c, v, w, _s = (int(x) for x in loc.split(":"))
        verses[(c, v)].setdefault(w, []).append((form, pos, feat.split("|")))
    return verses


def _label(pos: str, feats: list[str]) -> str:
    if "PREF" in feats or "SUFF" in feats:
        tail = f":{feats[-1]}" if feats[0] == "PRON" else ""
        return f"{pos}:{feats[0]}{tail}"
    return pos


def analyse(
    word: list[Segment],
) -> tuple[tuple[str, ...], str, tuple[str, ...], str, tuple[str, ...], str]:
    """(التوقيع، P، وسومُ P، S، وسومُ S، قسمُ الجذع)."""

    signature = tuple(_label(pos, feats) for _f, pos, feats in word)
    pre = [(norm(f), _label(p, x)) for f, p, x in word if "PREF" in x]
    suf = [(norm(f), _label(p, x)) for f, p, x in word if "SUFF" in x]
    stem = next((p for _f, p, x in word if "PREF" not in x and "SUFF" not in x), "N")
    return (
        signature,
        "".join(f for f, _ in pre),
        tuple(lab for _, lab in pre),
        "".join(f for f, _ in suf),
        tuple(lab for _, lab in suf),
        stem,
    )


class Learner:
    def __init__(self) -> None:
        self.memory: dict[str, Counter[tuple[str, ...]]] = defaultdict(Counter)
        self.pstart: Counter[str] = Counter()
        self.sstart: Counter[str] = Counter()
        self.phits: Counter[str] = Counter()
        self.shits: Counter[str] = Counter()
        self.plabels: dict[str, Counter[tuple[str, ...]]] = defaultdict(Counter)
        self.slabels: dict[str, Counter[tuple[str, ...]]] = defaultdict(Counter)
        self.stems: dict[str, Counter[str]] = defaultdict(Counter)
        self.by_prefix: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)

    def learn(self, token: str, word: list[Segment]) -> None:
        signature, p, plab, s, slab, stem = analyse(word)
        raw = JAZM.raw(token)
        self.memory[JAZM.skeleton(JAZM.units(token))][signature] += 1
        for k in range(1, min(DEPTH, len(raw)) + 1):
            self.pstart[raw[:k]] += 1
            self.sstart[raw[-k:]] += 1
        if p:
            self.phits[p] += 1
            self.plabels[p][plab] += 1
        if s:
            self.shits[s] += 1
            self.slabels[s][slab] += 1
        self.stems[raw[len(p) : len(raw) - len(s)] if s else raw[len(p) :]][stem] += 1
        self.by_prefix[plab][stem] += 1

    def _rate(self, hits: Counter[str], start: Counter[str], key: str) -> Fraction:
        return Fraction(hits[key], start[key]) if start[key] else Fraction(0)

    def predict(self, token: str) -> tuple[tuple[str, ...], bool]:
        """(التوقيع المتنبَّأ، أكان الهيكلُ في الذاكرة)."""

        seen = self.memory.get(JAZM.skeleton(JAZM.units(token)))
        if seen:
            return seen.most_common(1)[0][0], True
        raw = JAZM.raw(token)
        pre = max(
            (
                p
                for p in self.phits
                if raw.startswith(p) and self._rate(self.phits, self.pstart, p) >= HALF
            ),
            key=len,
            default="",
        )
        suf = max(
            (
                s
                for s in self.shits
                if raw.endswith(s)
                and len(raw) - len(pre) - len(s) >= 2
                and self._rate(self.shits, self.sstart, s) >= HALF
            ),
            key=len,
            default="",
        )
        plab = self.plabels[pre].most_common(1)[0][0] if pre else ()
        slab = self.slabels[suf].most_common(1)[0][0] if suf else ()
        stem = raw[len(pre) : len(raw) - len(suf)] if suf else raw[len(pre) :]
        if self.stems.get(stem):
            pos = self.stems[stem].most_common(1)[0][0]
        elif self.by_prefix.get(plab):
            pos = self.by_prefix[plab].most_common(1)[0][0]
        else:
            pos = "N"
        return (*plab, pos, *slab), False


def census(text: str, qac_path: Path) -> dict[str, object]:
    qac = read_qac(qac_path)
    order = sorted(qac)
    items: list[tuple[str, list[Segment]]] = []
    for line, key in zip(text.split("\n"), order, strict=True):
        tokens = line.replace("<sel>", " ").split()
        words = qac[key]
        if len(tokens) == max(words):
            items.extend((t, words[i + 1]) for i, t in enumerate(tokens))
    full = Learner()
    for token, word in items:
        full.learn(token, word)
    online = Learner()
    rows: list[tuple[bool, bool, bool]] = []
    for token, word in items:
        truth = analyse(word)[0]
        guess, known = online.predict(token)
        off, _ = full.predict(token)
        rows.append((guess == truth, off == truth, known))
        online.learn(token, word)
    n = len(rows)
    quarter = n // 4
    unseen = [r for r in rows if not r[2]]

    def share(part: list[tuple[bool, bool, bool]], at: int = 0) -> Fraction:
        return Fraction(sum(r[at] for r in part), len(part))

    return {
        "n": n,
        "online": sum(r[0] for r in rows),
        "offline": sum(r[1] for r in rows),
        "first": share(rows[:quarter]),
        "last": share(rows[3 * quarter :]),
        "unseen": len(unseen),
        "unseen_right": sum(r[0] for r in unseen),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--qac", type=Path, required=True)
    given = parser.parse_args()
    f = census(given.text.read_text(encoding="utf-8").rstrip("\n"), given.qac)
    n, on, off = f["n"], f["online"], f["offline"]
    assert isinstance(n, int) and isinstance(on, int) and isinstance(off, int)
    print(f"س١ الفوريّ: {on}/{n} = {on / n:.4f} | غيرُ الفوريّ: {off}/{n} = {off / n:.4f}")
    print(f"س٢ النسبة: {on / off:.4f}")
    first, last = f["first"], f["last"]
    assert isinstance(first, Fraction) and isinstance(last, Fraction)
    print(
        f"س٣ الأوّل {float(first):.4f} الأخير {float(last):.4f} "
        f"الفرق {float(last - first):.4f}"
    )
    u, ur = f["unseen"], f["unseen_right"]
    assert isinstance(u, int) and isinstance(ur, int)
    print(f"س٤ ما لم يُرَ: {ur}/{u} = {ur / u:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
