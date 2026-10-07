"""سلّمُ ماركوف بالمستويات — تشغيلُ ختم `248f10df…`.

**العطلُ الذي يُصلَح**: في `2a849c9a…` سمّيتُ الفاصلَ البنيويَّ **كلمةً**،
وهو **لفظٌ** — ما بين فاصلين في البايتات. واللفظُ قد يحمل أكثرَ من كلمة،
فتسميتُه كلمةً **خلطُ مستويين**، والعدُّ صحيحٌ والاسمُ خطأ.

**فالسلّمُ ههنا مستوياتٌ مُشتَقّةٌ من البايتات وحدَها**:

- `م٠` الوحدةُ (١١٢)
- `م١` الرمزُ المُرخَّصُ عند وقوف القيد (جشعٌ لا يعبر الفاصل)
- `م٢` اللفظُ المفرد (ما بين فاصلين)
- `م٣` السطرُ (وهو **ليس الجملة**، بل حاملُ بايتاتٍ في المصدر)

**وما فوق ذلك لا تُرخّصه البايتات**: الكلمةُ المفردة، والتركيبُ
الإسناديّ، والتركيبُ المزجيّ، والجملة — **كلُّها تحتاج إيداعًا موقَّعًا**،
فتُصنَّف ولا تُخترَع، ولا يُسمّى السطرُ جملةً ولا اللفظُ كلمة.

**و`induction on`**: متراجحتان مبرهَنتان تُصانان عند كلّ مستوًى —
`log₂ التباديل ≤ N·H`، و`H ≤ L < H+1`. **و`induction FOR`**: الحلقةُ
تشهد عليهما مستوًى مستوًى، وتُري أين ينقلب **المحجوزُ** على **الملحَق**.

**ولا اسمٌ لصنفٍ يدخل**: وحداتٌ وألفاظٌ وأسطرٌ وبتّات.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
ASCENT = REPOSITORY / "examples" / "rasm" / "run_discovered_ascent.py"
LICENCE = REPOSITORY / "examples" / "rasm" / "run_greedy_licence.py"
ALGEBRA = REPOSITORY / "examples" / "rasm" / "run_greedy_algebra.py"
BOUND = REPOSITORY / "examples" / "rasm" / "run_word_escalation.py"
PATIENCE = 500
MOST_PROPOSALS = 60_000

VACANT = (
    ("الكلمةُ المفردة", "حدُّها فصلُ ملتصقٍ عن أصلٍ — قاعدةٌ لا تُشتَقّ من البايتات"),
    ("التركيبُ الإسناديّ", "يحتاج إسنادًا موقَّعًا بين لفظين، ولا أثرَ له في الرسم"),
    ("التركيبُ المزجيّ", "يحتاج جردًا مُودَعًا لما مُزِج، ولا يميّزه فاصلٌ"),
    ("الجملة", "حدُّها ليس السطرَ ولا الفاصلَ، ويحتاج وقفًا مُودَعًا"),
)

Pair = tuple[int, int]


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def entropy(counts: Counter[int]) -> float:
    total = sum(counts.values())
    return -math.fsum((one / total) * math.log2(one / total) for one in counts.values())


def arrangements(counts: Counter[int]) -> float:
    total = sum(counts.values())
    return (
        math.lgamma(total + 1)
        - math.fsum(math.lgamma(one + 1) for one in counts.values())
    ) / math.log(2)


def carried(stream: list[int]) -> float:
    """`I(Xₜ;Xₜ₊₁)` على المجرى المسطَّح — والجوارُ يعبر السطرَ في كلّ مستوًى."""

    joint: Counter[Pair] = Counter()
    for one, two in zip(stream, stream[1:]):
        joint[(one, two)] += 1
    total = sum(joint.values())
    if not total:
        return 0.0
    left: Counter[int] = Counter()
    right: Counter[int] = Counter()
    for (one, two), number in joint.items():
        left[one] += number
        right[two] += number
    after = -math.fsum(
        (number / total) * math.log2(number / left[one])
        for (one, _two), number in joint.items()
    )
    return entropy(right) - after


def spelled(
    support: Counter[int],
    measure: Counter[int],
    width: dict[int, int],
    licence: object,
) -> tuple[float, float]:
    """(متوسّطُ الطول، نصيبُ المرتدّ) — **والمرتدُّ يُهجّى بالـ١١٢ لا يُفلِت**.

    شحنُ رمزٍ لم يُرَ بـ`أطول+١` ليس شفرةً يُفَكّ بها: لا تعيّنه تلك
    البتّاتُ من بين ما لم يُرَ. فيُشحَن **هروبًا ثمّ هجاءً** —
    `عرضُه × log₂ ١١٢` — فيصير الطولُ قابلًا للفكّ، ويصدق المقارنةُ
    بين مستوًى مرتدُّه صفرٌ ومستوًى مرتدُّه واحد.
    """

    lengths = licence.huffman_lengths(support)  # type: ignore[attr-defined]
    if not lengths:
        return (0.0, 1.0)
    longest = max(lengths.values())
    total = sum(measure.values())
    if not total:
        return (0.0, 0.0)
    charge = 0.0
    missing = 0
    for symbol, number in measure.items():
        seen = lengths.get(symbol)
        if seen is None:
            missing += number
            charge += number * (longest + 1 + width[symbol] * math.log2(112))
        else:
            charge += number * seen
    return (charge / total, missing / total)


def price(
    stream: list[int], width: dict[int, int], licence: object
) -> tuple[float, ...]:
    """(H، L ملحقًا، L محجوزًا مهجًّى، نصيبُ المرتدّ، I، log₂ تباديل، الأبجديّة)."""

    counts = Counter(stream)
    even = Counter(stream[0::2])
    odd = Counter(stream[1::2])
    first = spelled(even, odd, width, licence)
    second = spelled(odd, even, width, licence)
    inside = licence.coded(counts, counts)  # type: ignore[attr-defined]
    return (
        entropy(counts),
        inside[0],
        (first[0] + second[0]) / 2,
        (first[1] + second[1]) / 2,
        carried(stream),
        arrangements(counts),
        float(len(counts)),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    licence = _load(LICENCE, "run_greedy_licence")
    bound = _load(BOUND, "run_word_escalation")
    _load(ALGEBRA, "run_greedy_algebra")
    text = given.text.read_text(encoding="utf-8")
    verses, heads, order, _lines, _reach = ascent.corpus_of(text)  # type: ignore[attr-defined]
    units = sum(len(one) for one in verses)
    print(f"L₀: {units} وحدةً | أبجديّة {len(order)} | أسطر {len(verses)}")

    levels: list[tuple[str, list[int], dict[int, int]]] = []
    levels.append(
        (
            "م٠ الوحدة",
            [one for row in verses for one in row],
            {index: 1 for index in range(len(order))},
        )
    )

    print("\n— بناءُ م١: الرمزُ المُرخَّصُ بقيدِ الفاصل")
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
    exact_even: Counter[Pair] = Counter()
    exact_odd: Counter[Pair] = Counter()
    commits = proposals = streak = 0
    nid = len(order)
    while proposals < MOST_PROPOSALS and streak < PATIENCE:
        if pointer >= len(ranking):
            raw, exact_even, exact_odd = bound.census_within(work, flags)  # type: ignore[attr-defined]
            ranking = [
                pair
                for pair, number in raw.most_common()
                if number > 1 and pair not in banned
            ]
            pointer = 0
            if not ranking:
                break
        pair = ranking[pointer]
        pointer += 1
        proposals += 1
        widths[nid] = widths[pair[0]] + widths[pair[1]]
        after_even = licence.moved(even, pair, nid, exact_even.get(pair, 0))  # type: ignore[attr-defined]
        after_odd = licence.moved(odd, pair, nid, exact_odd.get(pair, 0))  # type: ignore[attr-defined]
        there = licence.cost_of(after_even, after_odd, widths)  # type: ignore[attr-defined]
        if there[0] < here[0]:
            bound.apply_within(work, flags, pair, nid)  # type: ignore[attr-defined]
            even, odd, here = after_even, after_odd, there
            nid += 1
            commits += 1
            streak = 0
            ranking = []
            pointer = 0
        else:
            del widths[nid]
            banned.add(pair)
            streak += 1
    print(f"  التزاماتٌ {commits} | رموزٌ {sum(len(one) for one in work)}")
    levels.append(
        ("م١ الرمزُ المُرخَّص", [one for row in work for one in row], dict(widths))
    )

    tokens: list[int] = []
    table: dict[tuple[int, ...], int] = {}
    for row, head in zip(verses, heads):
        current: list[int] = []
        for symbol, fresh in zip(row, head):
            if fresh and current:
                key = tuple(current)
                tokens.append(table.setdefault(key, len(table)))
                current = []
            current.append(symbol)
        if current:
            key = tuple(current)
            tokens.append(table.setdefault(key, len(table)))
    token_width = {one: len(key) for key, one in table.items()}
    levels.append(("م٢ اللفظُ المفرد", tokens, token_width))

    rows: dict[tuple[int, ...], int] = {}
    line_stream = [rows.setdefault(tuple(row), len(rows)) for row in verses]
    levels.append(
        ("م٣ السطر", line_stream, {one: len(key) for key, one in rows.items()})
    )

    print("\n— السلّم: كلُّ مستوًى بثمنه")
    print(
        "  المستوى | N | أبجديّة | H | L ملحقًا | L محجوزًا | مرتدّ | I "
        "| للوحدة ملحقًا | للوحدة محجوزًا | L−H | N·H − تباديل"
    )
    measured: list[tuple[str, tuple[float, ...], int]] = []
    for name, stream, width in levels:
        one = price(stream, width, licence)
        measured.append((name, one, len(stream)))
        print(
            f"  {name} | {len(stream)} | {int(one[6])} | {one[0]:.4f} "
            f"| {one[1]:.4f} | {one[2]:.4f} | {one[3]:.4f} | {one[4]:.4f} "
            f"| {one[1] * len(stream) / units:.4f} "
            f"| {one[2] * len(stream) / units:.4f} "
            f"| {one[1] - one[0]:+.4f} | {one[0] * len(stream) - one[5]:+.1f}"
        )

    inside = [one[1] * count / units for _, one, count in measured]
    outside = [one[2] * count / units for _, one, count in measured]
    gaps = [one[1] - one[0] for _, one, _ in measured]
    stirling = [one[0] * count - one[5] for _, one, count in measured]
    flow = [one[4] for _, one, _ in measured]
    print("\n— الحكمُ على السلّم")
    print(f"  أقصى ارتفاعٍ للملحَق صعودًا: {max(_rises(inside)):+.6f}")
    print(f"  أقصى ارتفاعٍ للمحجوز صعودًا: {max(_rises(outside)):+.6f}")
    print(f"  المحجوزُ في القمّة − في القاع: {outside[-1] - outside[0]:+.4f}")
    print(f"  أدنى L−H {min(gaps):+.6f} | أقصى L−H {max(gaps):+.6f}")
    print(f"  أدنى (N·H − تباديل): {min(stirling):+.1f}")
    print(f"  I في القمّة − في القاع: {flow[-1] - flow[0]:+.4f}")

    print("\n— مستوياتٌ لا تُرخّصها البايتات")
    for name, why in VACANT:
        print(f"  {name}: UNCLASSIFIED — {why}")
    print(f"  جملتُها: {len(VACANT)}")
    return 0


def _rises(values: list[float]) -> list[float]:
    """فروقُ الصعود — موجبُها ارتفاعٌ، وسالبُها نزول."""

    return [two - one for one, two in zip(values, values[1:])] or [0.0]


if __name__ == "__main__":
    sys.exit(main())
