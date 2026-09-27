"""خاصّيةُ الاختيار الجشع في قرارات أداة الإعراب، والحَكَمُ QAC — تشغيلُ ختم `9390b473…`.

كلُّ تعريفٍ هنا نصُّ الاستخراج في الختم. والمرشَّحاتُ في ج٣ تُولَّد بمنطق `analyse`
المودَعة نفسِه، ويُتحقَّق أنّ أوّلَها بعد الترتيب هو ما تعيده `analyse`.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
PERSON = {
    "1S": "ي",
    "1P": "نا",
    "2MS": "ك",
    "2FS": "ك",
    "2D": "كما",
    "2MP": "كم",
    "2FP": "كن",
    "3MS": "ه",
    "3FS": "ها",
    "3D": "هما",
    "3MP": "هم",
    "3FP": "هن",
}
FORM_VF = {
    "I": {1},
    "II": {2},
    "III": {3},
    "IV": {4},
    "V": {5},
    "VI": {6},
    "VII": {7},
    "VIII": {8},
    "X": {10},
    "I/IV": {1, 4},
}
FATHA = "َ"
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


JARR = _load("run_jarr_zero")
JAZM = _load("run_jazm_zero")
QACRUN = _load("run_valency_qac")
PEELER, GOVERNED = JAZM.PEELER, JAZM.GOVERNED


def _noun(word: list) -> tuple[str, str | None, bool] | None:
    """(الحالة، صورةُ الضمير اللاحق، فيها DET) لكلمةٍ اسمٍ ذاتِ حالةٍ بلا فعل."""

    if any(pos == "V" for pos, _ in word):
        return None
    for i, (pos, feats) in enumerate(word):
        case = next((c for c in ("NOM", "ACC", "GEN") if c in feats), None)
        if pos == "N" and case is not None:
            suffix = None
            for p, f in word[i + 1 :]:
                if p == "N" and "PRON" in f and "SUFF" in f:
                    suffix = next((PERSON[x] for x in f if x in PERSON), None)
            det = any(p == "P" and f[0] == "DET" for p, f in word)
            return (case, suffix, det)
    return None


def _prefix(word: list) -> bool:
    pos, feats = word[0]
    return pos == "P" and "PREF" in feats and ("LEM:و" in feats or "LEM:ف" in feats)


def _jarr(token: str) -> bool:
    return GOVERNED.kind(*PEELER.peel(token), PEELER.STRUCTURE) == "جر"


def candidates(scope: dict, token: str) -> list[dict]:
    """مرشَّحاتُ analyse المودَعة مرتّبةً، بمنطقها نفسه."""

    render, parse_suffix, letters = (
        scope["render"],
        scope["parse_suffix"],
        scope["letters"],
    )
    table, corpus = scope["T"], scope["corpus"]
    r = render(token)
    cands = [r]
    for p in ("وa", "فa"):
        if r.startswith(p):
            cands.append(r[len(p) :])
    more = []
    for c in cands:
        for p in ("لa", "لi", "سa"):
            if c.startswith(p):
                more.append(c[len(p) :])
    cands += more
    found = []
    for c in cands:
        for t in table:
            form, voice, tense, rx = t[:4]
            weak = t[4] if len(t) > 4 else None
            mm = re.match(rx, c)
            if not mm:
                continue
            g = list(mm.groups())
            suffix = g[-1]
            before = c[: len(c) - len(suffix)]
            rv = before[-1] if before and before[-1] in "0aiu" else None
            ok, _ = parse_suffix(suffix, rv)
            if not ok:
                continue
            del weak
            found.append((len(letters(suffix)), len(c), form, tense))
    rest = corpus.is_mudari(token)
    mud = rest is not None and rest[0][0][0] in "يتن"
    found.sort(key=lambda x: ((x[3] == "مضارع") != mud, x[1], x[3] == "أمر", -x[0]))
    return [{"form": f, "tense": t} for _, _, f, t in found]


def census(text: str, qac_path: Path) -> dict[str, object]:
    scope = QACRUN.instrument(text)
    qac = QACRUN.read_qac(qac_path)
    order = sorted(qac)
    lines = text.split("\n")
    hits: dict[str, list[int]] = {
        k: [0, 0] for k in ("ج١", "ج٢", "ج٣", "ج٤", "ج٥", "ب١")
    }
    misses: dict[str, Counter[str]] = {k: Counter() for k in hits}
    aligned: dict[int, tuple[list[tuple[str, int]], dict]] = {}
    for number, (line, key) in enumerate(zip(lines, order, strict=True), start=1):
        flat: list[tuple[str, int]] = []
        for index, part in enumerate(line.split("<sel>")):
            flat.extend((token, index) for token in part.split())
        if len(flat) == max(qac[key]):
            aligned[number] = (flat, qac[key])

    def mark(name: str, good: bool, token: str) -> None:
        hits[name][1] += 1
        hits[name][0] += good
        if not good:
            misses[name][token] += 1

    for flat, words in aligned.values():
        for i, (token, seg) in enumerate(flat):
            word = words[i + 1]
            kept = JAZM.units(token)
            noun = _noun(word)
            letters = JAZM.skeleton(kept)
            if noun is not None:
                greedy = next(
                    (
                        p
                        for p in JARR.PRONOUNS
                        if letters.endswith(p) and len(letters) >= len(p) + 2
                    ),
                    None,
                )
                if greedy is not None:
                    mark("ج١", noun[1] == greedy, token)
            if len(kept) >= 3 and kept[0][0][0] in "وف" and kept[0][0][1] == FATHA:
                mark("ج٢", _prefix(word), token)
            if not _jarr(token) or i + 1 >= len(flat) or flat[i + 1][1] != seg:
                continue
            second, third = flat[i + 1], flat[i + 2] if i + 2 < len(flat) else None
            after = _noun(words[i + 2])
            if after is not None:
                mark("ج٤", after[0] == "GEN", second[0])
            if third is None or third[1] != seg:
                continue
            last = _noun(words[i + 3])
            if last is None:
                continue
            if JAZM.raw(third[0]).startswith("وال"):
                mark("ج٥", last[0] == "GEN", third[0])
            tanween = any(e.get("تنوين") for e in PEELER.peel(second[0])[1])
            if (
                after is not None
                and after[0] == "GEN"
                and not after[2]
                and after[1] is None
            ):
                if not tanween:
                    mark("ب١", last[0] == "GEN", third[0])

    exchange_ok = 0
    for number, w, token, chosen in scope["TOKENS"]:
        if number not in aligned:
            continue
        verb = QACRUN._verb(aligned[number][1][w])
        if verb is None or not verb[0]:
            continue
        options = candidates(scope, token)
        assert options and options[0]["form"] == chosen["form"], token
        forms = {one["form"] for one in options}
        if len(forms) < 2 or not any(verb[0] in FORM_VF[f] for f in forms):
            continue
        good = verb[0] in FORM_VF[chosen["form"]]
        mark("ج٣", good, token)
        exchange_ok += good
    return {"hits": hits, "misses": misses, "aligned": len(aligned)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--qac", type=Path, required=True)
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"), given.qac)
    hits, misses = found["hits"], found["misses"]
    assert isinstance(hits, dict) and isinstance(misses, dict)
    print("الآياتُ المتطابقة:", found["aligned"])
    for name, (good, total) in hits.items():
        share = Fraction(good, total) if total else Fraction(0)
        print(f"{name}: {good}/{total} = {float(share):.4f}")
        print("   أكثرُ الخطأ:", misses[name].most_common(12))
    return 0


if __name__ == "__main__":
    sys.exit(main())
