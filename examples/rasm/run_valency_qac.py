"""أداةُ التعدّي على محكّ QAC — تشغيلُ ختم `7f050383…`.

الأداةُ تُنفَّذ كما أُودعت (`deposits/valency_instrument.py.txt`)، وQAC يُعطى مسارُه
(`--qac`: quran-morphology.txt من mustafa0x/quran-morphology عند 8f38b39). وحيث احتمل
نصُّ الختم وجهين أُخذ بلفظه: في ت٢ «حرفُ الجرّ» مقطعٌ وسمُه P وأوّلُ خصائصه P؛ وفي ت٣
«أوّلُ مقاطعها P» وسمُ المقطع الأوّل P أيًّا كان (فيدخل فيه «ال» والعطف)، والكلمةُ
الأخيرةُ في الآية ليس بعدها شيءٌ فتُعَدّ.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

RASM = Path(__file__).resolve().parent
INSTRUMENT = RASM.parents[1] / "deposits" / "valency_instrument.py.txt"
INSTRUMENT_SHA = "4e0d868b871a3a40"
FORMS = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "X": 10,
}
LAZIM_ROOTS = (
    "سكن",
    "شعر",
    "طغي",
    "عجب",
    "عوذ",
    "موت",
    "فلح",
    "بخل",
    "شيأ",
    "جري",
    "توب",
    "سجد",
    "لبث",
)
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()

Segment = tuple[str, list[str]]


def instrument(text: str) -> dict[str, object]:
    body = INSTRUMENT.read_bytes()
    if not hashlib.sha256(body).hexdigest().startswith(INSTRUMENT_SHA):
        raise RuntimeError("الأداةُ غيرُ المودَعة")
    scope: dict[str, object] = {"TEXT": text, "RASM": str(RASM), "__name__": "valency"}
    exec(compile(body.decode("utf-8"), str(INSTRUMENT), "exec"), scope)  # noqa: S102
    return scope


def read_qac(path: Path) -> dict[tuple[int, int], dict[int, list[Segment]]]:
    verses: dict[tuple[int, int], dict[int, list[Segment]]] = defaultdict(dict)
    for line in path.read_text(encoding="utf-8").split("\n"):
        if not line.strip():
            continue
        loc, _, pos, feat = line.split("\t")
        c, v, w, _s = (int(x) for x in loc.split(":"))
        verses[(c, v)].setdefault(w, []).append((pos, feat.split("|")))
    return verses


def _verb(word: list[Segment]) -> tuple[int, bool, bool, str] | None:
    """(الوزن، مجهول؟، ضميرٌ مفعول؟، الجذر) لكلمةٍ فيها فعل."""

    for i, (pos, feats) in enumerate(word):
        if pos != "V":
            continue
        vf = next((int(f[3:]) for f in feats if f.startswith("VF:")), 0)
        root = next((f[5:] for f in feats if f.startswith("ROOT:")), "")
        obj = any(p == "N" and "PRON" in f and "SUFF" in f for p, f in word[i + 1 :])
        return (vf, "PASS" in feats, obj, root)
    return None


def census(text: str, qac_path: Path) -> dict[str, object]:
    scope = instrument(text)
    tokens = scope["TOKENS"]
    res = scope["res"]
    assert isinstance(tokens, list) and isinstance(res, dict)
    qac = read_qac(qac_path)
    order = sorted(qac)
    lines = text.split("\n")
    aligned: dict[int, dict[int, list[Segment]]] = {}
    for number, (line, key) in enumerate(zip(lines, order, strict=True), start=1):
        words = qac[key]
        if len(line.replace("<sel>", " ").split()) == max(words):
            aligned[number] = words
    mine = {(n, w): a for n, w, _t, a in tokens if n in aligned}

    counts: dict[str, list[int]] = {k: [0, 0] for k in ("ق١", "ق٢", "ق٣", "ق٤", "ق٥")}
    for (n, w), a in mine.items():
        verb = _verb(aligned[n][w])
        counts["ق٥"][1] += 1
        counts["ق٥"][0] += verb is not None
        if a["voice"] == "مفعول":
            counts["ق١"][1] += 1
            counts["ق١"][0] += verb is not None and verb[1]
        if verb is not None and a["form"] in FORMS:
            counts["ق٣"][1] += 1
            counts["ق٣"][0] += verb[0] == FORMS[a["form"]]
        if a["voice"] == "فاعل" and a["obj"] >= 1:
            counts["ق٤"][1] += 1
            counts["ق٤"][0] += verb is not None and verb[2]
    for n, words in aligned.items():
        for w, word in words.items():
            verb = _verb(word)
            if verb is not None and verb[1]:
                counts["ق٢"][1] += 1
                a = mine.get((n, w))
                counts["ق٢"][0] += a is not None and a["voice"] == "مفعول"

    by_root: dict[str, dict[int, list[tuple[bool, bool]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    passive_named: Counter[str] = Counter()
    for key in order:
        words = qac[key]
        for w in sorted(words):
            verb = _verb(words[w])
            if verb is None:
                continue
            vf, passive, obj, root = verb
            by_root[root][vf].append((passive, obj))
            if vf == 1 and passive and root in LAZIM_ROOTS:
                after = words.get(w + 1)
                if after is None or after[0][0] != "P":
                    passive_named[root] += 1
    eligible = [
        r
        for r, forms in by_root.items()
        if len(forms.get(1, [])) >= 3
        and not any(p or o for p, o in forms[1])
        and forms.get(4)
    ]
    shifted = [r for r in eligible if any(p or o for p, o in by_root[r][4])]

    after: dict[str, Counter[str]] = {"متعدٍّ": Counter(), "لازم": Counter()}
    for (n, w), a in mine.items():
        if a["voice"] != "فاعل" or a["tense"] == "أمر" or a["obj"] > 0:
            continue
        kind = res.get(f"{a['root']}|{a['form']}")
        if not isinstance(kind, str):
            continue
        group = (
            "متعدٍّ"
            if kind.startswith("متعدٍّ")
            else "لازم"
            if kind.startswith("لازم")
            else None
        )
        if group is None:
            continue
        for j in range(w + 1, w + 4):
            word = aligned[n].get(j)
            if word is None:
                break
            if any(p == "P" and f[0] == "P" for p, f in word) or any(
                p == "V" for p, _ in word
            ):
                break
            if any(p == "P" and f[0] == "DET" for p, f in word):
                case = next(
                    (
                        c
                        for p, f in word
                        if p == "N"
                        for c in ("NOM", "ACC", "GEN")
                        if c in f
                    ),
                    None,
                )
                if case is not None:
                    after[group][case] += 1
                    break
    share = {
        g: Fraction(c["ACC"], sum(c.values())) if sum(c.values()) else Fraction(0)
        for g, c in after.items()
    }
    return {
        "aligned": len(aligned),
        "counts": counts,
        "eligible": sorted(eligible),
        "shifted": sorted(shifted),
        "after": after,
        "gap": share["متعدٍّ"] - share["لازم"],
        "passive_named": passive_named,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--qac", type=Path, required=True)
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"), given.qac)
    print("الآياتُ المتطابقة:", found["aligned"])
    counts = found["counts"]
    assert isinstance(counts, dict)
    for name, (hit, total) in counts.items():
        print(f"{name}: {hit}/{total} = {hit / total:.4f}")
    eligible, shifted = found["eligible"], found["shifted"]
    assert isinstance(eligible, list) and isinstance(shifted, list)
    print(f"ت١: {len(shifted)}/{len(eligible)} = {len(shifted) / len(eligible):.4f}")
    print("  لم يتعدَّ:", sorted(set(eligible) - set(shifted)))
    print("ت٢:", {g: dict(c) for g, c in found["after"].items()}, float(found["gap"]))  # type: ignore[attr-defined, arg-type]
    print("ت٣:", dict(found["passive_named"]))  # type: ignore[call-overload]
    return 0


if __name__ == "__main__":
    sys.exit(main())
