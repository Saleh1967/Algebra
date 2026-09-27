"""النموذجُ الرياضيّ المستقرَأ: اللفظ = قالبٌ ⊗ جذر — تشغيلُ ختم (يُثبَّت في اختبار التشغيل).

**النموذج**: كلُّ لفظٍ له جذرٌ في QAC يُكتب زوجًا (T, r): r حروفُ الجذر، وT وحداتُ اللفظ
(حرفٌ وحال) وقد أُبدلت وحداتُ الجذر فيها بخاناتٍ مرقّمة. فالبناءُ build(T, r) تعويضٌ
للخانات، والتقشيرُ peel(w) اختيارُ قالبٍ يطابق اللفظَ في غير الخانات، وقراءةُ الجذر من
الخانات. والبناءُ والتقشيرُ متعاكسان على المشهود بالإنشاء؛ **فالامتحانُ ليس المرآة، بل
التعميم**: يُستقرَأ النموذجُ من الآيات الزوجيّة، ويُمتحن على ألفاظ الفرديّة التي لم تُرَ.
"""

from __future__ import annotations

import argparse
import importlib.util
import random
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
FOLD = {"أ": "ا", "إ": "ا", "آ": "ا", "ء": "ا", "ؤ": "ا", "ئ": "ا", "ى": "ا", "ة": "ه"}
SLOT = "#"
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()

Unit = tuple[str, str]
Template = tuple[tuple[str, str], ...]


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


PEELER = _load("run_cv_peel")
QACRUN = _load("run_valency_qac")


def units(token: str) -> list[Unit]:
    peeled, _ = PEELER.peel(token)
    return [u for u in peeled if u[0] != PEELER.STRUCTURE]


def fold_root(root: str) -> str:
    return "".join(FOLD.get(c, c) for c in root)


def template(word: list[Unit], root: str) -> Template:
    """حروفُ الجذر تُطابَق بالترتيب من اليمين إلى اليسار: كلُّ حرفٍ أوّلُ وحدةٍ بعد سابقه."""

    slots: dict[int, int] = {}
    at = 0
    for index, letter in enumerate(root):
        for j in range(at, len(word)):
            if word[j][0] == letter:
                slots[j] = index
                at = j + 1
                break
    return tuple(
        ((SLOT, f"{slots[j]}{s}") if j in slots else (letter, s))
        for j, (letter, s) in enumerate(word)
    )


def build(t: Template, root: str) -> tuple[Unit, ...] | None:
    out = []
    for letter, state in t:
        if letter == SLOT:
            index = int(state[0])
            if index >= len(root):
                return None
            out.append((root[index], state[1:]))
        else:
            out.append((letter, state))
    return tuple(out)


def peel(
    word: tuple[Unit, ...], by_length: dict[int, Counter[Template]]
) -> tuple[Template, str] | None:
    """أكثرُ القوالب ورودًا مطابقةً للّفظ في غير الخانات، والجذرُ من الخانات."""

    best = None
    for t, count in by_length.get(len(word), Counter()).most_common():
        letters: dict[int, str] = {}
        ok = True
        for (tl, ts), (wl, ws) in zip(t, word, strict=True):
            if tl == SLOT:
                if ts[1:] != ws:
                    ok = False
                    break
                index = int(ts[0])
                if letters.get(index, wl) != wl:
                    ok = False
                    break
                letters[index] = wl
            elif (tl, ts) != (wl, ws):
                ok = False
                break
        if ok:
            best = (
                t,
                "".join(
                    letters.get(i, "?") for i in range(max(letters, default=-1) + 1)
                ),
            )
            break
    return best


def observations(text: str, qac_path: Path) -> list[tuple[int, tuple[Unit, ...], str]]:
    """(رقمُ السطر، وحداتُ اللفظ، الجذرُ مطويًّا) لكلّ لفظٍ في آيةٍ متطابقةٍ له جذر."""

    qac = QACRUN.read_qac(qac_path)
    order = sorted(qac)
    out = []
    for number, (line, key) in enumerate(
        zip(text.split("\n"), order, strict=True), start=1
    ):
        tokens = line.replace("<sel>", " ").split()
        words = qac[key]
        if len(tokens) != max(words):
            continue
        for i, token in enumerate(tokens):
            root = next(
                (
                    f[5:]
                    for _p, feats in words[i + 1]
                    for f in feats
                    if f.startswith("ROOT:")
                ),
                None,
            )
            if root:
                out.append((number, tuple(units(token)), fold_root(root)))
    return out


def census(text: str, qac_path: Path) -> dict[str, object]:
    obs = observations(text, qac_path)
    even = [(w, r) for n, w, r in obs if n % 2 == 0]
    odd = [(w, r) for n, w, r in obs if n % 2 == 1]
    pairs_even = {(template(list(w), r), r) for w, r in even}
    templates_even = Counter(template(list(w), r) for w, r in even)
    roots_even = {r for _, r in even}
    forms_even = {w for w, _ in even}
    by_length: dict[int, Counter[Template]] = defaultdict(Counter)
    for t, c in templates_even.items():
        by_length[len(t)][t] = c

    novel = [(w, r) for w, r in odd if w not in forms_even]
    covered = [
        (w, r)
        for w, r in novel
        if template(list(w), r) in templates_even and r in roots_even
    ]
    right = 0
    for w, r in covered:
        found = peel(w, by_length)
        if found is not None:
            got = found[1]
            right += len(got) == len(r) and all(
                g in ("?", c) for g, c in zip(got, r, strict=True)
            )

    templates_of: dict[str, set[Template]] = defaultdict(set)
    roots_of: dict[Template, set[str]] = defaultdict(set)
    for t, r in pairs_even:
        templates_of[r].add(t)
        roots_of[t].add(r)
    generated: set[tuple[Template, str]] = set()
    for r, mine in templates_of.items():
        neighbours: Counter[str] = Counter()
        for t in mine:
            for other in roots_of[t]:
                if other != r:
                    neighbours[other] += 1
        for other, shared in neighbours.items():
            if shared >= 2:
                for t in templates_of[other] - mine:
                    generated.add((t, r))
    pairs_odd = {(template(list(w), r), r) for w, r in odd}
    hits = len(generated & pairs_odd)
    universe = sorted(templates_even, key=lambda t: (-templates_even[t], t))
    roots_sorted = sorted(roots_even)
    rng = random.Random(0)
    baseline: set[tuple[Template, str]] = set()
    while len(baseline) < len(generated):
        pair = (rng.choice(universe), rng.choice(roots_sorted))
        if pair not in pairs_even:
            baseline.add(pair)
    base_hits = len(baseline & pairs_odd)
    return {
        "observations": len(obs),
        "templates": len(templates_even),
        "roots": len(roots_even),
        "novel": len(novel),
        "covered": len(covered),
        "right": right,
        "generated": len(generated),
        "hits": hits,
        "base_hits": base_hits,
        "roundtrip": sum(build(template(list(w), r), r) == w for _n, w, r in obs),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--qac", type=Path, required=True)
    parser.add_argument("--sizes-only", action="store_true")
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"), given.qac)
    if given.sizes_only:
        for k in ("observations", "templates", "roots", "generated"):
            print(k, found[k])
        return 0
    for k, v in found.items():
        print(k, v)
    n1 = Fraction(found["covered"], found["novel"])  # type: ignore[arg-type]
    n2 = Fraction(found["right"], found["covered"])  # type: ignore[arg-type]
    p = Fraction(found["hits"], found["generated"])  # type: ignore[arg-type]
    b = Fraction(found["base_hits"], found["generated"])  # type: ignore[arg-type]
    print(
        f"ن١ {float(n1):.4f} | ن٢ {float(n2):.4f} | ن٣ {float(p):.6f} / {float(b):.6f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
