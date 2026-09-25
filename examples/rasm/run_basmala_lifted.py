"""إعادةُ قياس الأرقام الكلميّة مرفوعَ البسملات — تشغيلُ ختم `be03e5be…`.

**المُجمَّدُ لا يُمَسّ**: تُبنى منه **مدوّنةٌ مشتقّةٌ** ببصمةٍ خاصّةٍ بها،
تُرفَع فيها البسملةُ الملحقةُ بأوّل آيةٍ من كلّ سورة — ١١٢ سطرًا، أربعُ
كلماتٍ من كلٍّ — **ولا تُرفَع البسملةُ القائمةُ بنفسها** في السطر الأوّل.

**والرفعُ يحفظ البايتات**: يُؤخَذ السطرُ من مبدأ كلمته الخامسة، فلا
تُعاد كتابةُ ما بعدها ولا تُبدَّل مسافةٌ ولا وسم.

**والقياسُ يُعاد كلُّه**: عدُّ الكلم والهياكل، ودرجاتُ السلّم الأربع،
وقاعدةُ الفصل — و«قبلُ» **تُقرأ من السجلّ المُجمَّد `426f7fc8…` ومن
السجلّات المُودَعة**، لا من الذاكرة.

**ولا يُبدَّل سجلٌّ مُقفَل**: `426f7fc8…` قياسُ المُجمَّد كما هو، ويبقى.
وهذه أرقامٌ **موازية** تُنشَر باسمها.

**ولا اسمٌ لصنفٍ يدخل**: ألفاظٌ وهياكلُ وأسطرٌ وبتّات.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
ASCENT = REPOSITORY / "examples" / "rasm" / "run_discovered_ascent.py"
HUFFMAN = REPOSITORY / "examples" / "rasm" / "run_huffman_ascent.py"
LICENCE = REPOSITORY / "examples" / "rasm" / "run_greedy_licence.py"
LADDER = REPOSITORY / "examples" / "rasm" / "run_markov_ladder.py"
BOUND = REPOSITORY / "examples" / "rasm" / "run_word_escalation.py"
SEPARATE = REPOSITORY / "examples" / "rasm" / "run_separation_rule.py"
FROZEN = REPOSITORY / "tools" / "ladder_seal.py"
SELECTOR = re.compile(r"<sel>")
HEAD = ["بسم", "الله", "الرحمن", "الرحيم"]
PATIENCE = 500
MOST_PROPOSALS = 60_000

Pair = tuple[int, int]


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def bare(one: str) -> str:
    return "".join(c for c in one if unicodedata.category(c) != "Mn")


def lift(text: str) -> tuple[str, int]:
    """(المدوّنةُ مرفوعةً، عددُ الأسطر المرفوعة) — بقصٍّ لا بإعادة كتابة."""

    kept: list[str] = []
    lifted = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        pieces = line.split()
        if len(pieces) > 4 and [bare(one) for one in pieces[:4]] == HEAD:
            fifth = pieces[4]
            place = line.index(fifth, sum(len(one) for one in pieces[:4]))
            kept.append(line[place:])
            lifted += 1
        else:
            kept.append(line)
    return ("\n".join(kept) + "\n", lifted)


def words_of(text: str, peeler: object) -> list[tuple[tuple[str, str], ...]]:
    found: list[tuple[tuple[str, str], ...]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        units, _ = peeler.peel(line)  # type: ignore[attr-defined]
        current: list[tuple[str, str]] = []
        for base, value in units:
            if base == peeler.STRUCTURE:  # type: ignore[attr-defined]
                if current:
                    found.append(tuple(current))
                current = []
            else:
                current.append((base, value))
        if current:
            found.append(tuple(current))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    huffman = _load(HUFFMAN, "run_huffman_ascent")
    licence = _load(LICENCE, "run_greedy_licence")
    ladder = _load(LADDER, "run_markov_ladder")
    bound = _load(BOUND, "run_word_escalation")
    separate = _load(SEPARATE, "run_separation_rule")
    frozen = _load(FROZEN, "ladder_seal")
    before = frozen.FROZEN_LADDER  # type: ignore[attr-defined]

    raw = given.text.read_text(encoding="utf-8")
    text, lifted = lift(raw)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    lines = [one for one in text.splitlines() if one.strip()]
    print("— المدوّنةُ المشتقّة")
    print(f"  أسطرٌ {len(lines)} | أسطرٌ رُفِعت {lifted}")
    print(f"  بصمتُها {digest}")
    print("  بصمةُ المُجمَّد 37633090…")

    peeler = _load(REPOSITORY / "examples" / "rasm" / "run_cv_peel.py", "run_cv_peel")
    words = words_of(text, peeler)
    table: dict[tuple[str, ...], Counter[tuple[tuple[str, str], ...]]] = defaultdict(
        Counter
    )
    for form in words:
        table[tuple(base for base, _ in form)][form] += 1
    vague = {key: one for key, one in table.items() if len(one) > 1}
    vague_mass = sum(sum(one.values()) for one in vague.values())
    print("\n— ١) عدُّ الكلم والهياكل")
    print(f"  الألفاظُ: {len(words)} (قبلُ 78245)")
    print(f"  هياكلُ متمايزة: {len(table)} (قبلُ 15472)")
    print(f"  غامضةٌ منها: {len(vague)} (قبلُ 1886)")
    print(
        f"  كتلتُها: {vague_mass} ({vague_mass / len(words):.4f}) "
        f"(قبلُ 34902 و0.4461)"
    )

    verses, heads, order, _lines, _reach = ascent.corpus_of(text)  # type: ignore[attr-defined]
    units = sum(len(one) for one in verses)
    print("\n— ٢) السلّمُ — وقبلُ من `426f7fc8…`")
    print(f"  L₀: {units} وحدةً (قبلُ {before.counts[0]})")

    work = [list(row) for row in verses]
    flags = [list(one) for one in heads]
    widths: dict[int, int] = {index: 1 for index in range(len(order))}
    even: Counter[int] = Counter()
    odd: Counter[int] = Counter()
    for index, row in enumerate(work):
        (even if index % 2 == 0 else odd).update(row)
    here = licence.cost_of(even, odd, widths)  # type: ignore[attr-defined]
    banned: set[Pair] = set()
    ranking: list[Pair] = []
    pointer = 0
    ee: Counter[Pair] = Counter()
    eo: Counter[Pair] = Counter()
    commits = proposals = streak = 0
    nid = len(order)
    while proposals < MOST_PROPOSALS and streak < PATIENCE:
        if pointer >= len(ranking):
            rawp, ee, eo = bound.census_within(work, flags)  # type: ignore[attr-defined]
            ranking = [
                pair
                for pair, number in rawp.most_common()
                if number > 1 and pair not in banned
            ]
            pointer = 0
            if not ranking:
                break
        pair = ranking[pointer]
        pointer += 1
        proposals += 1
        widths[nid] = widths[pair[0]] + widths[pair[1]]
        ae = licence.moved(even, pair, nid, ee.get(pair, 0))  # type: ignore[attr-defined]
        ao = licence.moved(odd, pair, nid, eo.get(pair, 0))  # type: ignore[attr-defined]
        there = licence.cost_of(ae, ao, widths)  # type: ignore[attr-defined]
        if there[0] < here[0]:
            bound.apply_within(work, flags, pair, nid)  # type: ignore[attr-defined]
            even, odd, here = ae, ao, there
            nid += 1
            commits += 1
            streak = 0
            ranking = []
            pointer = 0
        else:
            del widths[nid]
            banned.add(pair)
            streak += 1

    levels: list[tuple[str, list[int], dict[int, int]]] = [
        (
            "م٠ الوحدة",
            [one for row in verses for one in row],
            {index: 1 for index in range(len(order))},
        ),
        ("م١ الرمزُ المُرخَّص", [one for row in work for one in row], dict(widths)),
    ]
    tokens: list[int] = []
    keys: dict[tuple[int, ...], int] = {}
    for row, head in zip(verses, heads):
        current: list[int] = []
        for symbol, fresh in zip(row, head):
            if fresh and current:
                tokens.append(keys.setdefault(tuple(current), len(keys)))
                current = []
            current.append(symbol)
        if current:
            tokens.append(keys.setdefault(tuple(current), len(keys)))
    levels.append(("م٢ اللفظُ المفرد", tokens, {one: len(k) for k, one in keys.items()}))
    rows: dict[tuple[int, ...], int] = {}
    stream = [rows.setdefault(tuple(row), len(rows)) for row in verses]
    levels.append(("م٣ السطر", stream, {one: len(k) for k, one in rows.items()}))

    print("  المستوى | N | أبجديّة | للوحدة ملحقًا | للوحدة محجوزًا | مرتدّ | I")
    outs: list[float] = []
    for index, (name, flow, width) in enumerate(levels):
        one = ladder.price(flow, width, licence)  # type: ignore[attr-defined]
        inside = one[1] * len(flow) / units
        outside = one[2] * len(flow) / units
        outs.append(outside)
        print(
            f"  {name} | {len(flow)} ({before.counts[index]}) "
            f"| {int(one[6])} ({before.alphabets[index]}) "
            f"| {inside:.4f} ({before.inside_unit[index]}) "
            f"| {outside:.4f} ({before.outside_unit[index]}) "
            f"| {one[3]:.4f} ({before.missing[index]}) "
            f"| {one[4]:.4f} ({before.flow[index]})"
        )
    best = min(range(len(outs)), key=lambda one: outs[one])
    print(f"  أرخصُ درجةٍ محجوزًا: {levels[best][0]} (قبلُ م١)")
    print(f"  والتزاماتُ القيد: {commits}")
    mirror = huffman.cost_now(work, widths)  # type: ignore[attr-defined]
    print(f"  انحرافُ الآلتين: {abs(here[0] - mirror[0]):.9f}")

    print("\n— ٣) قاعدةُ الفصل مرفوعَ البسملات")
    heads_rule, tails_rule = separate.read_rule()  # type: ignore[attr-defined]
    letters = [base for base, _value in order]
    pieces: list[tuple[int, ...]] = []
    cut = 0
    for row, head in zip(verses, heads):
        token: list[int] = []
        for symbol, fresh in zip(row, head):
            if fresh and token:
                widths_list = separate.split_token(  # type: ignore[attr-defined]
                    [letters[one] for one in token], heads_rule, tails_rule
                )
                place = 0
                for one in widths_list:
                    pieces.append(tuple(token[place : place + one]))
                    place += one
                cut += 1 if len(widths_list) > 1 else 0
                token = []
            token.append(symbol)
        if token:
            widths_list = separate.split_token(  # type: ignore[attr-defined]
                [letters[one] for one in token], heads_rule, tails_rule
            )
            place = 0
            for one in widths_list:
                pieces.append(tuple(token[place : place + one]))
                place += one
            cut += 1 if len(widths_list) > 1 else 0
    seen: dict[tuple[int, ...], int] = {}
    cut_stream = [seen.setdefault(one, len(seen)) for one in pieces]
    cut_width = {one: len(k) for k, one in seen.items()}
    two = ladder.price(cut_stream, cut_width, licence)  # type: ignore[attr-defined]
    print(f"  ألفاظٌ فُصِلت: {cut} ({cut / len(tokens):.4f}) (قبلُ 46523 و0.5946)")
    print(f"  الكلماتُ: {len(pieces)} (قبلُ 137834) | أنواعٌ {len(seen)} (قبلُ 12668)")
    print(f"  مرتدُّها {two[3]:.4f} (قبلُ 0.0744)")
    print(
        f"  للوحدة محجوزًا {two[2] * len(cut_stream) / units:.4f} (قبلُ 4.3012) "
        f"| ومستوى اللفظ {outs[2]:.4f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
