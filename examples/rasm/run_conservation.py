"""مبرهنةُ الحفظ: البناءُ الجامعُ المانعُ من البتّ إلى المصحف — تشغيلُ ختم.

**السلّم** (والصعودُ من الأدنى):

    ط١ الحرف   = ٥ بتّات   (٢٨ رمزًا من ٣٢؛ والأربعةُ الباقيةُ غيرُ مرخّصة)
    ط٢ الحال   = ٢ بتّان    (فتحة ٠٠، ضمّة ٠١، كسرة ١٠، سكون ١١)
    ط٣ الوحدة  = حرفٌ ⊗ حال (١١٢ خانة = ٧ بتّات)
    ط٤ اللفظ   = معجمٌ مغلق، أو سابقةٌ ⊗ ι(وزن، إعلال)(جذر) ⊗ لاحقة، أو ذرّة
    ط٥ المكتوب = وحداتُ اللفظ + البقيّة (الحاملُ، والمربوطة، والشدّة، والتنوين،
                 والسكونُ العاري، وعلاماتُ الضبط التي ليست حرفًا)
    ط٦ الآية   = ألفاظٌ وفواصل (« » و« <sel> »)
    ط٧ المصحف  = آياتٌ بين أسطر

**الهبوطُ مرصود**: من بايتات المصحف إلى البتّات، ويُحفظ ما رُئي في كلّ طبقة.
**والصعودُ من البتّ**: كلُّ طبقةٍ تُبنى ممّا تحتها وتُقارَن بمرصودها.
**والترخيصُ متتالٍ**: لا تُرخَّص طبقةٌ حتى تستنفد التي قبلها — أي يعود
صعودُها إلى مرصودها في المدوّنة كلّها بلا بقيّةٍ غير محسوبة؛ فإن لم تستنفد
وقف السلّمُ عندها وما فوقها **غيرُ مرخّص**. وفي البتّ نفسه: لا تُرخَّص بتّةُ
الحال قبل استنفاد بتّات الحرف الخمس، ولا الحرفُ التالي قبل بتّتي الحال.

**والمبرهنة**: كلُّ طبقةٍ زوجٌ (صعود، هبوط) والصعودُ ∘ الهبوط = الهويّة على
مرصودها؛ فبالاستقراء على الطبقات يعود المصحفُ من البتّات والبقايا بايتةً
بايتة. والبرهانُ بالإنشاء، **وكلُّ خطوةٍ منه فحصٌ مقيسٌ** على المدوّنة كلّها.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from types import ModuleType

RASM = Path(__file__).resolve().parent
REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
SEPARATOR = re.compile(r"( <sel> | )")
FINGERPRINT = "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
LEXEME = "معجم"
COMPOUND = "مركّب"
ATOM = "ذرّة"

Unit = tuple[str, str]
Units = tuple[Unit, ...]


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, RASM / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ILAL = _load("run_ilal")
PEELER = ILAL.PEELER
TEMPLATE = ILAL.TEMPLATE
LETTERS = PEELER.BASE28
STATES = (PEELER.FATHA, PEELER.DAMMA, PEELER.KASRA, PEELER.SUKUN)
LETTER_BITS = 5
STATE_BITS = 2
UNIT_BITS = LETTER_BITS + STATE_BITS


# ———————————————————— ط١–ط٣: البتّ والحرف والحال والوحدة ————————————————————


def _bits(number: int, width: int) -> tuple[int, ...]:
    return tuple((number >> (width - 1 - k)) & 1 for k in range(width))


def encode(unit: Unit) -> tuple[int, ...]:
    """الوحدة ⟼ ٧ بتّات: خمسٌ لرتبة الحرف في الثمانية والعشرين، واثنتان للحال."""

    letter, state = unit
    return _bits(LETTERS.index(letter), LETTER_BITS) + _bits(
        STATES.index(state), STATE_BITS
    )


def licensed_prefixes() -> dict[int, frozenset[tuple[int, ...]]]:
    """لكلّ موضعٍ في دورة السبع: البادئاتُ المرخّصةُ بعده (شجرةُ الرموز المرخّصة)."""

    codes = [_bits(i, LETTER_BITS) for i in range(len(LETTERS))]
    out: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    for code in codes:
        for k in range(LETTER_BITS + 1):
            out[k].add(code[:k])
    return {k: frozenset(v) for k, v in out.items()}


LICENCE = licensed_prefixes()


class Ascent:
    """آلةُ الصعود بتّةً بتّة: كلُّ انتقالٍ يُسأل عن رخصته قبل أن يُقبَل.

    المواضعُ ٠–٤ بتّاتُ الحرف، ولا تُقبَل بتّةٌ إلّا إن بقي بعدها رمزٌ مرخّص؛
    و٥–٦ بتّتا الحال، ولا تبدآن قبل استنفاد الخمس؛ ثمّ تُسلَّم الوحدةُ
    ويبدأ حرفٌ جديد.
    """

    def __init__(self) -> None:
        self.buffer: list[int] = []
        self.used: Counter[tuple[tuple[int, ...], int]] = Counter()
        self.units: list[Unit] = []

    def step(self, bit: int) -> bool:
        where = len(self.buffer)
        if where < LETTER_BITS:
            prefix = tuple(self.buffer)
            if prefix + (bit,) not in LICENCE[where + 1]:
                return False
        self.used[(tuple(self.buffer), bit)] += 1
        self.buffer.append(bit)
        if len(self.buffer) == UNIT_BITS:
            letter = int("".join(map(str, self.buffer[:LETTER_BITS])), 2)
            state = int("".join(map(str, self.buffer[LETTER_BITS:])), 2)
            self.units.append((LETTERS[letter], STATES[state]))
            self.buffer = []
        return True


def licensed_transitions() -> set[tuple[tuple[int, ...], int]]:
    """كلُّ (بادئة، بتّة) مرخّصةٍ في دورة السبع."""

    out: set[tuple[tuple[int, ...], int]] = set()
    for i in range(len(LETTERS)):
        code = _bits(i, LETTER_BITS)
        for s in range(len(STATES)):
            whole = code + _bits(s, STATE_BITS)
            for k in range(UNIT_BITS):
                out.add((whole[:k], whole[k]))
    return out


def unlicensed_codes_rejected() -> tuple[int, int]:
    """(المرفوض، المجموع) من رموز السبع التي حرفُها خارج الثمانية والعشرين."""

    total = rejected = 0
    for letter in range(len(LETTERS), 2**LETTER_BITS):
        for state in range(len(STATES)):
            total += 1
            machine = Ascent()
            bits = _bits(letter, LETTER_BITS) + _bits(state, STATE_BITS)
            rejected += not all(machine.step(b) for b in bits)
    return (rejected, total)


# ———————————————————— ط٤: اللفظ ————————————————————


def stores(text: str, qac_path: Path) -> dict[str, object]:
    """مخازنُ اللفظ من الآيات المتطابقة مع QAC: السوابقُ واللواحقُ وأزواجُ
    (الوزن، الإعلال) والجذور، والمعجمُ المغلق: ألفاظٌ لا جذرَ لها."""

    obs = [o for o in ILAL.observations(text, qac_path) if o["factors"] is not None]
    prefixes: Counter[Units] = Counter(o["factors"][0] for o in obs)  # type: ignore[index]
    suffixes: Counter[object] = Counter(o["factors"][3] for o in obs)  # type: ignore[index]
    pairs: Counter[object] = Counter(
        (o["factors"][1], o["factors"][2])  # type: ignore[index]
        for o in obs
    )
    by_length: dict[int, Counter[object]] = defaultdict(Counter)
    for key, c in pairs.items():
        by_length[len(key[0])][key] = c  # type: ignore[index]
    roots: Counter[str] = Counter(o["root"] for o in obs)  # type: ignore[misc]
    return {
        "prefixes": prefixes,
        "suffixes": suffixes,
        "wazns": by_length,
        "store": ILAL.RootStore(roots, ILAL.WEAK),
        "lexicon": closed_lexicon(text, qac_path),
    }


def closed_lexicon(text: str, qac_path: Path) -> frozenset[Units]:
    raw: dict[tuple[int, int, int], list[list[str]]] = defaultdict(list)
    for line in qac_path.read_text(encoding="utf-8").split("\n"):
        if not line.strip():
            continue
        loc, _form, _pos, feat = line.split("\t")
        c, v, w, _s = (int(x) for x in loc.split(":"))
        raw[(c, v, w)].append(feat.split("|"))
    verses = sorted({(c, v) for c, v, _w in raw})
    count = Counter((c, v) for c, v, _w in raw)
    out: set[Units] = set()
    for line, key in zip(text.split("\n"), verses, strict=True):
        tokens = line.replace("<sel>", " ").split()
        if len(tokens) != count[key]:
            continue
        for i, token in enumerate(tokens):
            feats = raw[(key[0], key[1], i + 1)]
            if not any(f.startswith("ROOT:") for fs in feats for f in fs):
                out.add(tuple(TEMPLATE.units(token)))
    return frozenset(out)


def parse(word: Units, s: dict[str, object]) -> tuple[object, ...] | None:
    """التقشيرُ الأعمى كما في ختم 8fc24141، ويُسلِّم العواملَ لا الجذرَ وحده."""

    best: tuple[tuple[bool, int], tuple[object, ...]] | None = None
    prefixes: Counter[Units] = s["prefixes"]  # type: ignore[assignment]
    suffixes: Counter[object] = s["suffixes"]  # type: ignore[assignment]
    wazns: dict[int, Counter[object]] = s["wazns"]  # type: ignore[assignment]
    for p, cp in prefixes.items():
        if not ILAL.WAZN._prefix(word, p):
            continue
        for suffix, cs in suffixes.items():
            ending, s_units = suffix  # type: ignore[misc]
            size = len(ending) + len(s_units)
            if len(p) + size + 1 > len(word):
                continue
            if s_units and word[len(word) - len(s_units) :] != s_units:
                continue
            e_at = len(word) - size
            last = word[e_at][0]
            e = tuple(
                (ILAL.TAIL if a == last else a, b)
                for a, b in word[e_at : e_at + len(ending)]
            )
            if e != ending:
                continue
            middle = word[len(p) : e_at]
            for (w, ops), cw in wazns.get(len(middle) + 1, Counter()).items():  # type: ignore[misc]
                got = ILAL._fill(w, ops, middle, last)
                if got is None:
                    continue
                score = ILAL._score(cp * cw * cs, got, s["store"])
                if best is None or score > best[0]:
                    best = (score, (p, w, ops, suffix, got))
    return None if best is None else best[1]


def word_down(word: Units, s: dict[str, object]) -> tuple[object, ...]:
    """الهبوط: المعجمُ المغلقُ أوّلًا، ثمّ التركيب، وما بقي ذرّة."""

    if word in s["lexicon"]:  # type: ignore[operator]
        return (LEXEME, word)
    found = parse(word, s)
    if found is not None:
        return (COMPOUND, *found)
    return (ATOM, word)


def word_up(factors: tuple[object, ...]) -> Units | None:
    """الصعود: P ⊗ ι(W, I)(r) ⊗ S، أو المعجم، أو الذرّة."""

    kind = factors[0]
    if kind in (LEXEME, ATOM):
        return factors[1]  # type: ignore[return-value]
    p, w, ops, suffix, root = factors[1:]
    return ILAL.build(p, w, ops, suffix, root)  # type: ignore[no-any-return]


# ———————————————————— ط٥: المكتوب ————————————————————


def written_down(token: str) -> tuple[Units, tuple[object, ...]]:
    """(وحداتُ اللفظ، البقيّة): مواضعُ ما ليس حرفًا وقنواتُ الحامل والشدّة…"""

    units, extras = PEELER.peel(token)
    kept = tuple(u for u in units if u[0] != PEELER.STRUCTURE)
    marks = tuple((i, u[1]) for i, u in enumerate(units) if u[0] == PEELER.STRUCTURE)
    notes = tuple(
        tuple(sorted(e.items())) for e, u in zip(extras, units, strict=True)
        if u[0] != PEELER.STRUCTURE
    )
    return (kept, (marks, notes))


def written_up(kept: Units, residue: tuple[object, ...]) -> str:
    marks, notes = residue  # type: ignore[misc]
    units: list[Unit] = []
    extras: list[dict[str, str]] = []
    at = dict(marks)
    source = iter(zip(kept, notes, strict=True))
    for i in range(len(kept) + len(at)):
        if i in at:
            units.append((PEELER.STRUCTURE, at[i]))
            extras.append({})
        else:
            u, n = next(source)
            units.append(u)
            extras.append(dict(n))
    return PEELER.rebuild(units, extras)  # type: ignore[no-any-return]


# ———————————————————— السلّم ————————————————————


def ladder(text: str, qac_path: Path) -> dict[str, object]:
    """الهبوطُ المرصود ثمّ الصعودُ طبقةً طبقة، ولا تُرخَّص طبقةٌ قبل استنفاد سابقتها."""

    # الهبوطُ المرصود
    verses = text.split("\n")
    pieces = [SEPARATOR.split(v) if v else [] for v in verses]
    tokens = [t for piece in pieces for t in piece[0::2]]
    written = {t: written_down(t) for t in set(tokens)}
    s = stores(text.rstrip("\n"), qac_path)
    forms = {written[t][0] for t in written}
    factored = {w: word_down(w, s) for w in forms}
    stream = [bit for t in tokens for u in written[t][0] for bit in encode(u)]

    found: dict[str, object] = {"tokens": len(tokens), "forms": len(forms)}
    reached: list[str] = []

    def gate(name: str, held: bool) -> bool:
        if held:
            reached.append(name)
        return held

    # ط١–ط٣: البتّ ⟼ الحرف ⟼ الحال ⟼ الوحدة
    machine = Ascent()
    accepted = sum(machine.step(b) for b in stream)
    observed_units = [u for t in tokens for u in written[t][0]]
    found["bits"] = len(stream)
    found["bits_accepted"] = accepted
    found["units"] = len(observed_units)
    found["units_returned"] = sum(
        a == b for a, b in zip(machine.units, observed_units, strict=False)
    )
    found["cells_attested"] = len(set(observed_units))
    found["transitions_licensed"] = len(licensed_transitions())
    found["transitions_used"] = len(set(machine.used))
    rejected, total = unlicensed_codes_rejected()
    found["unlicensed_rejected"] = rejected
    found["unlicensed_codes"] = total
    held = (
        accepted == len(stream)
        and not machine.buffer
        and len(machine.units) == len(observed_units)
        and found["units_returned"] == len(observed_units)
        and rejected == total
    )
    if not gate("ط١–ط٣", held):
        return {**found, "reached": tuple(reached)}

    # ط٤: الوحدات ⟼ اللفظ
    kinds = Counter(f[0] for f in factored.values())
    found["lexemes"] = kinds[LEXEME]
    found["compounds"] = kinds[COMPOUND]
    found["atoms"] = kinds[ATOM]
    by_token = Counter(factored[written[t][0]][0] for t in tokens)
    found["tokens_lexeme"] = by_token[LEXEME]
    found["tokens_compound"] = by_token[COMPOUND]
    found["tokens_atom"] = by_token[ATOM]
    found["words_returned"] = sum(word_up(f) == w for w, f in factored.items())
    rng = random.Random(0)
    tried = refused = unrooted = 0
    store = s["store"]
    for w in sorted(forms):
        if len(w) < 3:
            continue
        shuffled = tuple(rng.sample(w, len(w)))
        if shuffled == w or shuffled in forms:
            continue
        tried += 1
        down = word_down(shuffled, s)
        refused += down[0] == ATOM
        unrooted += down[0] == ATOM or (
            down[0] == COMPOUND and store.mass(down[-1]) == 0  # type: ignore[attr-defined]
        )
    found["shuffled"] = tried
    found["shuffled_refused"] = refused
    found["shuffled_unrooted"] = unrooted
    if not gate("ط٤", found["words_returned"] == len(forms)):
        return {**found, "reached": tuple(reached)}

    # ط٥: اللفظ + البقيّة ⟼ المكتوب
    rebuilt = {
        t: written_up(word_up(factored[written[t][0]]), written[t][1])  # type: ignore[arg-type]
        for t in written
    }
    found["written_returned"] = sum(rebuilt[t] == t for t in tokens)
    found["residue_marks"] = sum(len(written[t][1][0]) for t in tokens)  # type: ignore[arg-type]
    found["residue_notes"] = sum(
        sum(bool(n) for n in written[t][1][1])  # type: ignore[union-attr]
        for t in tokens
    )
    if not gate("ط٥", found["written_returned"] == len(tokens)):
        return {**found, "reached": tuple(reached)}

    # ط٦: الألفاظ + الفواصل ⟼ الآية
    returned = 0
    for verse, piece in zip(verses, pieces, strict=True):
        out = [rebuilt[p] if k % 2 == 0 else p for k, p in enumerate(piece)]
        returned += "".join(out) == verse
    found["verses"] = len(verses)
    found["verses_returned"] = returned
    found["separators"] = Counter(p for piece in pieces for p in piece[1::2])
    if not gate("ط٦", returned == len(verses)):
        return {**found, "reached": tuple(reached)}

    # ط٧: الآيات ⟼ المصحف
    whole = "\n".join(
        "".join(rebuilt[p] if k % 2 == 0 else p for k, p in enumerate(piece))
        for piece in pieces
    )
    digest = hashlib.sha256(whole.encode("utf-8")).hexdigest()
    found["corpus_returned"] = whole == text
    found["fingerprint_returned"] = digest == FINGERPRINT
    gate("ط٧", whole == text and digest == FINGERPRINT)
    return {**found, "reached": tuple(reached)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--qac", type=Path, required=True)
    given = parser.parse_args()
    for k, v in ladder(given.text.read_text(encoding="utf-8"), given.qac).items():
        print(k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
