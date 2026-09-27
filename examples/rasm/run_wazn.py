"""بناءُ الأوزان: القالبُ = سابقةٌ ⊗ وزنٌ ⊗ لاحقة — تشغيلُ ختم (يُثبَّت في اختبار التشغيل).

سقط في ختم القالب ⊗ الجذر أنّ الجديدَ تركيبٌ لقالبٍ وجذرٍ مشهودَين، وكان
أكثرُ الساقط قالبًا جديدًا بجذرٍ مشهود: فالقالبُ الكاملُ ليس عاملًا أوّليًّا.
وههنا يُفكَّك، **والوزنُ أوّلًا** كما أمر صاحبُ المستودع.

**التعريف** (من الصرف): الوزنُ هيئةُ الجذع — حروفُه وحركاتُه وسكونُه **ما عدا
الآخر**، والآخرُ للإعراب. فاللفظ:

    w = P ⊗ W(r) ⊗ S

- P السابقة: وحداتُ مقاطع PREF في QAC (و ف ب ل ال …)، بحالها.
- W الوزن: وحداتُ الجذع، وقد صارت وحداتُ الجذر فيه خاناتٍ مرقّمةً تحمل حالَها،
  والمضعَّفُ خانةٌ واحدةٌ مكرَّرة، والحرفُ الأخيرُ بلا حال.
- S اللاحقة: حالُ الآخر (علامةُ الإعراب) ثمّ وحداتُ مقاطع SUFF (الضمائر).

**وحدودُ المقاطع من QAC** على المشهود وحدَه (الزوجيّ)؛ **والامتحانُ أعمى**: على
الفرديّ يُقشَّر اللفظُ بمخازن الزوجيّ وحدها، بلا حدودٍ من QAC.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter, defaultdict
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
SLOT = "#"
LAST = "*"
TAIL = "@"
SUN = "~"
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()

Unit = tuple[str, str]
Units = tuple[Unit, ...]
Wazn = tuple[tuple[str, str], ...]
Suffix = tuple[Units, Units]


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
TEMPLATE = _load("run_root_template")
LETTERS = set(PEELER.BASE28) | set(PEELER.FOLD)


def clusters(token: str) -> list[tuple[str, Units]]:
    """(الحرفُ مطويًّا، وحداتُه) لكلّ حرفٍ في اللفظ بعلاماته؛ وما ليس حرفًا يسقط."""

    out: list[tuple[str, Units]] = []
    i = 0
    while i < len(token):
        if token[i] not in LETTERS:
            i += 1
            continue
        j = i + 1
        while j < len(token) and token[j] not in LETTERS:
            j += 1
        chunk = token[i:j]
        units = tuple(u for u in PEELER.peel(chunk)[0] if u[0] != PEELER.STRUCTURE)
        out.append((PEELER.FOLD.get(token[i], token[i]), units))
        i = j
    return out


def skeleton(form: str) -> list[str]:
    """حروفُ مقطعٍ من QAC مطويّة؛ والألفُ المقصورةُ «؟» تطابق ا أو ي."""

    out = []
    for c in form:
        if c == "ٱ":
            out.append("ا")
        elif c == "ى":
            out.append("؟")
        elif c in LETTERS:
            out.append(PEELER.FOLD.get(c, c))
    return out


def _same(qac: list[str], rasm: list[str]) -> bool:
    return len(qac) == len(rasm) and all(
        q == r or (q == "؟" and r in ("ا", "ي")) for q, r in zip(qac, rasm, strict=True)
    )


def wazn(stem: Units, geminate: set[int], root: str) -> Wazn:
    """خاناتُ الجذر في الجذع، والشطرُ الثاني من المشدَّد خانةُ الأوّل إن كان خانة."""

    t = list(TEMPLATE.template(list(stem), root))
    for j in sorted(geminate):
        if t[j - 1][0] == SLOT and t[j][0] != SLOT:
            t[j] = (SLOT, t[j - 1][1][0] + stem[j][1])
    return tuple(t)


def _geminate(cl: list[tuple[str, Units]]) -> set[int]:
    """مواضعُ الشطر الثاني من كلّ مشدَّد: وحدتان في حرفٍ واحد، الأولى ساكنة."""

    out: set[int] = set()
    at = 0
    for _b, us in cl:
        if len(us) >= 2 and us[0][1] == PEELER.SUKUN and us[1][0] == us[0][0]:
            out.add(at + 1)
        at += len(us)
    return out


def factor(
    token: str, segments: list[tuple[str, str, list[str]]], root: str
) -> tuple[Units, Wazn, Suffix, Units] | None:
    """(P, W, S, وحداتُ اللفظ) أو لا شيء إن لم تتطابق حدودُ QAC مع الرسم."""

    cl = clusters(token)
    head = [c for form, tag, _f in segments if tag == "PREF" for c in skeleton(form)]
    tail = [c for form, tag, _f in segments if tag == "SUFF" for c in skeleton(form)]
    letters = [b for b, _u in cl]
    if len(head) + len(tail) >= len(letters):
        return None
    if not _same(head, letters[: len(head)]):
        return None
    if tail and not _same(tail, letters[len(letters) - len(tail) :]):
        return None
    pre = cl[: len(head)]
    stem = cl[len(head) : len(letters) - len(tail)]
    suf = cl[len(letters) - len(tail) :]
    assimilated: Units = ()
    det = any("DET" in f for _form, tag, f in segments if tag == "PREF")
    if det and len(stem[0][1]) >= 2 and 0 in {g - 1 for g in _geminate(stem[:1])}:
        assimilated = ((SUN, PEELER.SUKUN),)
        stem = [(stem[0][0], stem[0][1][1:]), *stem[1:]]
    stem_units = tuple(u for _b, us in stem for u in us)
    t = wazn(stem_units, _geminate(stem), root)
    last_len = len(stem[-1][1])
    core = t[: len(t) - last_len]
    last_letter, last_units = stem[-1][0], stem[-1][1]
    first_of_last = t[len(t) - last_len]
    mark = (first_of_last[1][0] if first_of_last[0] == SLOT else "") + LAST
    w = (*core, (first_of_last[0], mark))
    ending = tuple((TAIL if u[0] == last_letter else u[0], u[1]) for u in last_units)
    p = tuple(u for _b, us in pre for u in us) + assimilated
    s_units = tuple(u for _b, us in suf for u in us)
    whole = tuple(u for _b, us in cl for u in us)
    return (p, w, (ending, s_units), whole)


def build(p: Units, w: Wazn, s: Suffix, root: str) -> Units | None:
    """P ⊗ W(r) ⊗ S ⟼ وحداتُ اللفظ."""

    out: list[Unit] = list(p)
    last = ""
    sun = bool(out) and out[-1][0] == SUN
    for k, (letter, state) in enumerate(w):
        if letter == SLOT:
            index = int(state[0])
            if index >= len(root):
                return None
            letter, state = root[index], state[1:]
        if sun:
            out[-1] = (letter, out[-1][1])
            sun = False
        if k == len(w) - 1:
            last = letter
        else:
            out.append((letter, state))
    ending, s_units = s
    out.extend((last if a == TAIL else a, b) for a, b in ending)
    out.extend(s_units)
    return tuple(out)


def _fill(w: Wazn, middle: Units) -> str | None:
    """يطابق الوسطَ بالوزن (ما عدا الآخر وعلامته) ويقرأ الجذر؛ «?» للمجهول."""

    letters: dict[int, str] = {}
    for (tl, ts), (ml, ms) in zip(w[:-1], middle, strict=True):
        if tl == SLOT:
            if ts[1:] != ms:
                return None
            i = int(ts[0])
            if letters.get(i, ml) != ml:
                return None
            letters[i] = ml
        elif (tl, ts) != (ml, ms):
            return None
    return "".join(letters.get(i, "?") for i in range(max(letters, default=-1) + 1))


def _prefix(word: Units, p: Units) -> bool:
    if len(p) >= len(word):
        return False
    for k, (a, b) in enumerate(p):
        if a == SUN:
            if (word[k + 1][0], b) != word[k]:
                return False
        elif (a, b) != word[k]:
            return False
    return True


def blind_peel(
    word: Units,
    prefixes: Counter[Units],
    suffixes: Counter[Suffix],
    wazns: dict[int, Counter[Wazn]],
) -> str | None:
    """أعمى: كلُّ سابقةٍ ولاحقةٍ ووزنٍ من الزوجيّ يطابق، وأعلاها حاصلُ ضرب الورود."""

    best: tuple[int, str] | None = None
    for p, cp in prefixes.items():
        if not _prefix(word, p):
            continue
        for (ending, s_units), cs in suffixes.items():
            size = len(ending) + len(s_units)
            if len(p) + size + 1 > len(word):
                continue
            if s_units and word[len(word) - len(s_units) :] != s_units:
                continue
            e_at = len(word) - size
            last = word[e_at][0]
            e = tuple(
                (TAIL if a == last else a, b)
                for a, b in word[e_at : e_at + len(ending)]
            )
            if e != ending:
                continue
            middle = word[len(p) : e_at]
            for w, cw in wazns.get(len(middle) + 1, Counter()).items():
                if w[-1][0] != SLOT and w[-1][0] != last:
                    continue
                got = _fill(w, middle)
                if got is None:
                    continue
                if w[-1][0] == SLOT:
                    i = int(w[-1][1][0])
                    letters = list(got) + ["?"] * max(0, i + 1 - len(got))
                    if letters[i] not in ("?", last):
                        continue
                    letters[i] = last
                    got = "".join(letters)
                score = cp * cw * cs
                if best is None or score > best[0]:
                    best = (score, got)
    return None if best is None else best[1]


def observations(text: str, qac_path: Path) -> list[dict[str, object]]:
    qac = QACRUN.read_qac(qac_path)
    raw: dict[tuple[int, int, int], list[tuple[str, str, list[str]]]] = defaultdict(
        list
    )
    for line in qac_path.read_text(encoding="utf-8").split("\n"):
        if not line.strip():
            continue
        loc, form, pos, feat = line.split("\t")
        c, v, w, _s = (int(x) for x in loc.split(":"))
        feats = feat.split("|")
        tag = "PREF" if "PREF" in feats else "SUFF" if "SUFF" in feats else pos
        raw[(c, v, w)].append((form, tag, feats))
    order = sorted(qac)
    out: list[dict[str, object]] = []
    for number, (line, key) in enumerate(
        zip(text.split("\n"), order, strict=True), start=1
    ):
        tokens = line.replace("<sel>", " ").split()
        if len(tokens) != max(qac[key]):
            continue
        for i, token in enumerate(tokens):
            segs = raw[(key[0], key[1], i + 1)]
            root = next(
                (
                    f[5:]
                    for _fm, _t, feats in segs
                    for f in feats
                    if f.startswith("ROOT:")
                ),
                None,
            )
            if not root:
                continue
            vf = next(
                (
                    int(f[3:])
                    for _fm, t, feats in segs
                    if t == "V"
                    for f in feats
                    if f.startswith("VF:")
                ),
                0,
            )
            found = factor(token, segs, TEMPLATE.fold_root(root))
            out.append(
                {
                    "line": number,
                    "root": TEMPLATE.fold_root(root),
                    "vf": vf,
                    "units": tuple(TEMPLATE.units(token)),
                    "factors": found,
                }
            )
    return out


def census(text: str, qac_path: Path, sizes_only: bool = False) -> dict[str, object]:
    obs = observations(text, qac_path)
    aligned = [o for o in obs if o["factors"] is not None]
    even = [o for o in aligned if o["line"] % 2 == 0]  # type: ignore[operator]
    odd = [o for o in aligned if o["line"] % 2 == 1]  # type: ignore[operator]
    prefixes: Counter[Units] = Counter(o["factors"][0] for o in even)  # type: ignore[index]
    suffixes: Counter[Suffix] = Counter(o["factors"][2] for o in even)  # type: ignore[index]
    wazn_count: Counter[Wazn] = Counter(o["factors"][1] for o in even)  # type: ignore[index]
    roots = {o["root"] for o in even}
    consistent = sum(
        o["factors"][3] == o["units"]
        for o in aligned  # type: ignore[index]
    )
    sizes = {
        "observations": len(obs),
        "aligned": len(aligned),
        "consistent": consistent,
        "prefixes": len(prefixes),
        "suffixes": len(suffixes),
    }
    if sizes_only:
        return sizes
    whole_templates = {
        TEMPLATE.template(list(o["units"]), o["root"])
        for o in even  # type: ignore[arg-type]
    }
    roundtrip = sum(
        build(o["factors"][0], o["factors"][1], o["factors"][2], o["root"])  # type: ignore[index,arg-type]
        == o["factors"][3]  # type: ignore[index]
        for o in aligned
    )
    forms_even = {o["units"] for o in even}
    novel = [o for o in odd if o["units"] not in forms_even]
    covered = [
        o
        for o in novel
        if o["factors"][0] in prefixes  # type: ignore[index]
        and o["factors"][1] in wazn_count  # type: ignore[index]
        and o["factors"][2] in suffixes  # type: ignore[index]
        and o["root"] in roots
    ]
    by_length: dict[int, Counter[Wazn]] = defaultdict(Counter)
    for w, c in wazn_count.items():
        by_length[len(w)][w] = c
    right = 0
    for o in novel:
        got = blind_peel(o["units"], prefixes, suffixes, by_length)  # type: ignore[arg-type]
        r = o["root"]
        assert isinstance(r, str)
        right += (
            got is not None
            and len(got) == len(r)
            and all(g in ("?", c) for g, c in zip(got, r, strict=True))
        )
    vf_of: dict[Wazn, Counter[int]] = defaultdict(Counter)
    for o in even:
        if o["vf"]:
            vf_of[o["factors"][1]][o["vf"]] += 1  # type: ignore[index]
    verbs_odd = [o for o in odd if o["vf"] and o["factors"][1] in vf_of]  # type: ignore[index]
    vf_right = sum(
        vf_of[o["factors"][1]].most_common(1)[0][0] == o["vf"]  # type: ignore[index]
        for o in verbs_odd
    )
    return {
        **sizes,
        "roundtrip": roundtrip,
        "wazns": len(wazn_count),
        "whole_templates": len(whole_templates),
        "novel": len(novel),
        "covered": len(covered),
        "peeled_right": right,
        "verbs_odd_seen": len(verbs_odd),
        "verbs_odd": sum(1 for o in odd if o["vf"]),
        "vf_right": vf_right,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--qac", type=Path, required=True)
    parser.add_argument("--sizes-only", action="store_true")
    given = parser.parse_args()
    found = census(
        given.text.read_text(encoding="utf-8").rstrip("\n"), given.qac, given.sizes_only
    )
    for k, v in found.items():
        print(k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
