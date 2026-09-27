"""الإعلالُ عاملًا رابعًا: w = P ⊗ ι(W, I)(r) ⊗ S — تشغيلُ ختم (يُثبَّت في اختبار التشغيل).

سقط في ختم الأوزان أنّ التقشيرَ الأعمى يعمّم، وكان الساقطُ الإعلال: أصاب في
الصحيح ٠٫٩٢ وفي المعتلّ والمهموز ٠٫٤٦. فالوزنُ وحده لا يحمل حرفَ العلّة إذا
قُلب أو حُذف.

**التعريف**: حروفُ العلّة والهمز صنفٌ واحد A = {ا، و، ي} (والهمزُ مطويٌّ ألفًا).
ويُحاذى الجذرُ بالجذع محاذاةً تحفظ الترتيب: الحرفُ يطابق نفسَه، أو — إن كان من
A — يطابق حرفًا آخرَ من A **قلبًا**، أو لا يطابق شيئًا **حذفًا**. ويُختار أعلى
المحاذيات (المطابقةُ ٢، والقلبُ ١، والحذفُ ٠؛ والتعادلُ لأبكر المواضع). فعاملُ
الإعلال I مجموعةُ عمليّات: (قلب، رتبةُ الحرف، الحرفُ الظاهر) و(حذف، رتبةُ الحرف).
والوزنُ W كما في ختم الأوزان، غير أنّ الحرفَ المقلوبَ خانةٌ لا حرف. فالبناءُ:
الخانةُ تُملأ بحرف الجذر إلّا المقلوبة فبحرفها الظاهر.

**والتقشيرُ الأعمى** بالعوامل من الزوجيّ: الخانةُ المقلوبةُ والمحذوفةُ تعطيان
حرفًا مجهولًا «?» في رتبتها، فيُعرف طولُ الجذر ولو سقط آخرُه. **والجذرُ عاملٌ
أيضًا** (R، مخزنُ جذور الزوجيّ): الرسمُ وحده لا يفرّق «صيّب» من صوب أو من صيب،
فالمقلوبُ «?» لا يوافق من الجذور إلّا حرفَ علّة، ويُقدَّم ما له في R جذرٌ موافق.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter, defaultdict
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
WEAK = frozenset("اوي")
SUB = "قلب"
DEL = "حذف"
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()

Unit = tuple[str, str]
Units = tuple[Unit, ...]
Wazn = tuple[tuple[str, str], ...]
Ilal = tuple[tuple[str, int, str], ...]
Suffix = tuple[Units, Units]


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


WAZN = _load("run_wazn")
PEELER = WAZN.PEELER
TEMPLATE = WAZN.TEMPLATE
QACRUN = WAZN.QACRUN
SLOT, LAST, TAIL, SUN = WAZN.SLOT, WAZN.LAST, WAZN.TAIL, WAZN.SUN


def align(stem: Units, root: str) -> dict[int, int | None]:
    """رتبةُ كلّ حرفٍ من الجذر ⟼ موضعُه في الجذع، أو None إن حُذف.

    أعلى مجموعٍ (مطابقة ٢، قلب ١، حذف ٠)، والتعادلُ لأبكر المواضع.
    """

    n, m = len(root), len(stem)
    # best[i][j]: أعلى مجموعٍ للحروف i.. من المواضع j..
    best = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m, -1, -1):
            score = best[i + 1][j]
            for k in range(j, m):
                gain = _gain(root[i], stem[k][0])
                if gain:
                    score = max(score, gain + best[i + 1][k + 1])
            best[i][j] = score
    out: dict[int, int | None] = {}
    j = 0
    for i in range(n):
        target = best[i][j]
        chosen: int | None = None
        for k in range(j, m):
            gain = _gain(root[i], stem[k][0])
            if gain and gain + best[i + 1][k + 1] == target:
                chosen = k
                break
        if chosen is None:
            out[i] = None
        else:
            out[i] = chosen
            j = chosen + 1
    return out


def _gain(radical: str, letter: str) -> int:
    if radical == letter:
        return 2
    if radical in WEAK and letter in WEAK:
        return 1
    return 0


def template(stem: Units, geminate: set[int], root: str) -> tuple[Wazn, Ilal]:
    """(W, I): الوزنُ بخاناته، وعمليّاتُ الإعلال."""

    at = align(stem, root)
    slot_of = {k: i for i, k in at.items() if k is not None}
    ops: list[tuple[str, int, str]] = []
    for i, k in sorted(at.items()):
        if k is None:
            ops.append((DEL, i, ""))
        elif stem[k][0] != root[i]:
            ops.append((SUB, i, stem[k][0]))
    t = [
        ((SLOT, f"{slot_of[j]}{s}") if j in slot_of else (letter, s))
        for j, (letter, s) in enumerate(stem)
    ]
    for j in sorted(geminate):
        if t[j - 1][0] == SLOT and t[j][0] != SLOT:
            t[j] = (SLOT, t[j - 1][1][0] + stem[j][1])
    return (tuple(t), tuple(ops))


def factor(
    token: str, segments: list[tuple[str, str, list[str]]], root: str
) -> tuple[Units, Wazn, Ilal, Suffix, Units] | None:
    """(P, W, I, S, وحداتُ اللفظ) كما في ختم الأوزان، والوزنُ بمحاذاة الإعلال."""

    cl = WAZN.clusters(token)
    head = [
        c for form, tag, _f in segments if tag == "PREF" for c in WAZN.skeleton(form)
    ]
    tail = [
        c for form, tag, _f in segments if tag == "SUFF" for c in WAZN.skeleton(form)
    ]
    letters = [b for b, _u in cl]
    if len(head) + len(tail) >= len(letters):
        return None
    if not WAZN._same(head, letters[: len(head)]):
        return None
    if tail and not WAZN._same(tail, letters[len(letters) - len(tail) :]):
        return None
    pre = cl[: len(head)]
    stem = cl[len(head) : len(letters) - len(tail)]
    suf = cl[len(letters) - len(tail) :]
    assimilated: Units = ()
    det = any("DET" in f for _form, tag, f in segments if tag == "PREF")
    if det and len(stem[0][1]) >= 2 and 0 in {g - 1 for g in WAZN._geminate(stem[:1])}:
        assimilated = ((SUN, PEELER.SUKUN),)
        stem = [(stem[0][0], stem[0][1][1:]), *stem[1:]]
    stem_units = tuple(u for _b, us in stem for u in us)
    t, ops = template(stem_units, WAZN._geminate(stem), root)
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
    return (p, w, ops, (ending, s_units), whole)


def build(p: Units, w: Wazn, ops: Ilal, s: Suffix, root: str) -> Units | None:
    """P ⊗ ι(W, I)(r) ⊗ S ⟼ وحداتُ اللفظ."""

    shown = {i: letter for kind, i, letter in ops if kind == SUB}
    out: list[Unit] = list(p)
    last = ""
    sun = bool(out) and out[-1][0] == SUN
    for k, (letter, state) in enumerate(w):
        if letter == SLOT:
            index = int(state[0])
            if index >= len(root):
                return None
            letter, state = shown.get(index, root[index]), state[1:]
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


def _fill(w: Wazn, ops: Ilal, middle: Units, last: str) -> str | None:
    """يطابق الوسطَ والآخرَ بالوزن والإعلال ويقرأ الجذر؛ «?» للمجهول والمُعَلّ."""

    shown = {i: letter for kind, i, letter in ops if kind == SUB}
    letters: dict[int, str] = {}
    cells = [*zip(w[:-1], middle, strict=True), (w[-1], (last, None))]
    for (tl, ts), (ml, ms) in cells:
        if tl == SLOT:
            if ms is not None and ts[1:] != ms:
                return None
            i = int(ts[0])
            if i in shown:
                if ml != shown[i]:
                    return None
                ml = "?"
            if letters.get(i, ml) != ml:
                return None
            letters[i] = ml
        elif ms is None:
            if tl != ml:
                return None
        elif (tl, ts) != (ml, ms):
            return None
    size = max([*letters, *(i for _k, i, _l in ops)], default=-1) + 1
    return "".join(letters.get(i, "?") for i in range(size))


class RootStore:
    """R: وزنُ الجذور الموافقة لقراءةٍ فيها «?» — والمجهولُ لا يوافق إلّا ما في wild."""

    def __init__(self, roots: Counter[str], wild: frozenset[str] | None) -> None:
        self.roots = roots
        self.wild = wild
        self.memo: dict[str, int] = {}

    def mass(self, got: str) -> int:
        if got not in self.memo:
            self.memo[got] = sum(
                c
                for r, c in self.roots.items()
                if len(r) == len(got)
                and all(
                    g == x or (g == "?" and (self.wild is None or x in self.wild))
                    for g, x in zip(got, r, strict=True)
                )
            )
        return self.memo[got]


def _score(product: int, got: str, store: RootStore | None) -> tuple[bool, int]:
    """بلا R: حاصلُ ضرب الورود. وبـR: ما له جذرٌ موافقٌ أوّلًا، ثمّ الحاصلُ في وزنه."""

    if store is None:
        return (True, product)
    mass = store.mass(got)
    return (mass > 0, product * max(mass, 1))


def blind_peel(
    word: Units,
    prefixes: Counter[Units],
    suffixes: Counter[Suffix],
    wazns: dict[int, Counter[tuple[Wazn, Ilal]]],
    store: RootStore | None = None,
) -> str | None:
    """أعمى: كلُّ سابقةٍ ولاحقةٍ ووزنٍ مُعَلٍّ من الزوجيّ يطابق، وأعلاها رتبةً."""

    best: tuple[tuple[bool, int], str] | None = None
    for p, cp in prefixes.items():
        if not WAZN._prefix(word, p):
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
            for (w, ops), cw in wazns.get(len(middle) + 1, Counter()).items():
                got = _fill(w, ops, middle, last)
                if got is None:
                    continue
                score = _score(cp * cw * cs, got, store)
                if best is None or score > best[0]:
                    best = (score, got)
    return None if best is None else best[1]


def plain_peel(
    word: Units,
    prefixes: Counter[Units],
    suffixes: Counter[Suffix],
    wazns: dict[int, Counter[Wazn]],
    store: RootStore,
) -> str | None:
    """الضابط: أوزانُ ختم الأوزان بلا إعلال، مع R؛ و«?» فيه يوافق أيَّ حرف."""

    best: tuple[tuple[bool, int], str] | None = None
    for p, cp in prefixes.items():
        if not WAZN._prefix(word, p):
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
                got = WAZN._fill(w, middle)
                if got is None:
                    continue
                if w[-1][0] == SLOT:
                    i = int(w[-1][1][0])
                    letters = list(got) + ["?"] * max(0, i + 1 - len(got))
                    if letters[i] not in ("?", last):
                        continue
                    letters[i] = last
                    got = "".join(letters)
                score = _score(cp * cw * cs, got, store)
                if best is None or score > best[0]:
                    best = (score, got)
    return None if best is None else best[1]


def _right(got: str | None, root: str) -> bool:
    return (
        got is not None
        and len(got) == len(root)
        and all(g in ("?", c) for g, c in zip(got, root, strict=True))
    )


def _weak(root: str) -> bool:
    return any(c in WEAK for c in root)


def observations(text: str, qac_path: Path) -> list[dict[str, object]]:
    """كما في ختم الأوزان، والعواملُ بالإعلال."""

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
    verses = sorted({(c, v) for c, v, _w in raw})
    count = Counter((c, v) for c, v, _w in raw)
    out: list[dict[str, object]] = []
    for number, (line, key) in enumerate(
        zip(text.split("\n"), verses, strict=True), start=1
    ):
        tokens = line.replace("<sel>", " ").split()
        if len(tokens) != count[key]:
            continue
        for i, token in enumerate(tokens):
            segs = raw[(key[0], key[1], i + 1)]
            root = next(
                (f[5:] for _fm, _t, fs in segs for f in fs if f.startswith("ROOT:")),
                None,
            )
            if not root:
                continue
            folded = TEMPLATE.fold_root(root)
            out.append(
                {
                    "line": number,
                    "root": folded,
                    "units": tuple(TEMPLATE.units(token)),
                    "factors": factor(token, segs, folded),
                }
            )
    return out


def census(
    text: str, qac_path: Path, learn: int = 2, test: int = 1, modulus: int = 2
) -> dict[str, object]:
    """يُستقرَأ من السطور ≡ learn ويُمتحن على ≡ test (بمقياس modulus)."""

    obs = [o for o in observations(text, qac_path) if o["factors"] is not None]
    plain = [
        o
        for o in WAZN.observations(text, qac_path)
        if o["factors"] is not None and o["line"] % modulus == learn % modulus  # type: ignore[operator]
    ]
    even = [o for o in obs if o["line"] % modulus == learn % modulus]  # type: ignore[operator]
    odd = [o for o in obs if o["line"] % modulus == test % modulus]  # type: ignore[operator]
    prefixes: Counter[Units] = Counter(o["factors"][0] for o in even)  # type: ignore[index]
    suffixes: Counter[Suffix] = Counter(o["factors"][3] for o in even)  # type: ignore[index]
    wazns: Counter[tuple[Wazn, Ilal]] = Counter(
        (o["factors"][1], o["factors"][2])  # type: ignore[index]
        for o in even
    )
    shapes = {w for w, _i in wazns}
    ilal = {i for _w, i in wazns}
    root_count: Counter[str] = Counter(o["root"] for o in even)  # type: ignore[misc]
    roots = set(root_count)
    roundtrip = sum(
        build(*o["factors"][:4], o["root"]) == o["factors"][4]  # type: ignore[index,misc]
        for o in obs
    )
    consistent = sum(o["factors"][4] == o["units"] for o in obs)  # type: ignore[index]
    by_length: dict[int, Counter[tuple[Wazn, Ilal]]] = defaultdict(Counter)
    for key, c in wazns.items():
        by_length[len(key[0])][key] = c
    forms = {o["units"] for o in even}
    novel = [o for o in odd if o["units"] not in forms]
    covered = sum(
        o["factors"][0] in prefixes  # type: ignore[index]
        and (o["factors"][1], o["factors"][2]) in wazns  # type: ignore[index]
        and o["factors"][3] in suffixes  # type: ignore[index]
        and o["root"] in roots
        for o in novel
    )
    store = RootStore(root_count, WEAK)
    plain_store = RootStore(root_count, None)
    old = {o["units"]: o for o in plain}
    old_even = [old[o["units"]] for o in even if o["units"] in old]
    old_prefixes: Counter[Units] = Counter(o["factors"][0] for o in old_even)  # type: ignore[index]
    old_suffixes: Counter[Suffix] = Counter(o["factors"][2] for o in old_even)  # type: ignore[index]
    old_wazns: dict[int, Counter[Wazn]] = defaultdict(Counter)
    for o in old_even:
        w = o["factors"][1]  # type: ignore[index]
        old_wazns[len(w)][w] += 1
    tally: Counter[str] = Counter()
    for o in novel:
        r = o["root"]
        assert isinstance(r, str)
        word = o["units"]
        kind = "معتل" if _weak(r) else "صحيح"
        tally[kind] += 1
        tally[kind + " إعلال"] += _right(
            blind_peel(word, prefixes, suffixes, by_length), r  # type: ignore[arg-type]
        )
        tally[kind + " إعلال وجذر"] += _right(
            blind_peel(word, prefixes, suffixes, by_length, store), r  # type: ignore[arg-type]
        )
        tally[kind + " جذر"] += _right(
            plain_peel(word, old_prefixes, old_suffixes, old_wazns, plain_store), r  # type: ignore[arg-type]
        )
    return {
        "aligned": len(obs),
        "consistent": consistent,
        "roundtrip": roundtrip,
        "wazns": len(wazns),
        "shapes": len(shapes),
        "ilal": len(ilal),
        "novel": len(novel),
        "covered": covered,
        "weak": tally["معتل"],
        "sound": tally["صحيح"],
        "weak_ilal": tally["معتل إعلال"],
        "sound_ilal": tally["صحيح إعلال"],
        "weak_ilal_root": tally["معتل إعلال وجذر"],
        "sound_ilal_root": tally["صحيح إعلال وجذر"],
        "weak_root": tally["معتل جذر"],
        "sound_root": tally["صحيح جذر"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--qac", type=Path, required=True)
    given = parser.parse_args()
    found = census(given.text.read_text(encoding="utf-8").rstrip("\n"), given.qac)
    for k, v in found.items():
        print(k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
