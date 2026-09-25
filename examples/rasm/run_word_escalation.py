"""التصعيدُ الجشع إلى الكلمة — تشغيلُ ختم `2a849c9a…`.

**الدعوى المعروضة**: الجشعُ الذي رُخِّص من `69a1c10c…` إلى `0c070831…`
جشعُ **مواضع**: يرخّص وحداتِ (حرفٍ × حال). والعضويّةُ الصنفيّةُ خاصّةُ
**كلمةٍ** لا موضع. فالوحدةُ التي يعمل عليها الجشعُ **تنتهي عند حدّ
الكلمة**، والصنفُ يقف فوقها.

**وتُعَدّ الدعوى لا تُناقَش**، بأربعة أعداد: الكلمُ، والهياكلُ المتمايزة
(الوحداتُ بلا حال)، والغامضُ منها (ما حمل أكثرَ من صورةٍ مضبوطة)،
وكتلتُها من الكلم.

**والتصعيدُ**: تُعاد آلةُ `69a1c10c…` بقيدٍ واحد — **لا دمجةَ تعبر حدَّ
الكلمة**. فالوحدةُ تنتهي حيث تنتهي الكلمةُ، ويُقاس كم من الكلم يصير
رمزًا واحدًا، وكم يكلّف القيدُ.

**ويُسعَّر الدَّينان**: `H(الصورة | الهيكل)` **محجوزًا** هو ثمنُ ما لا
يقرؤه البناء — دَينٌ معجميّ؛ و`H(الصورة | الهيكل، هيكلِ ما قبلها)` هو
ثمنُه بسياقٍ من الرتبة الأولى. **والمحجوزُ يقول أيهما دَينٌ وأيهما وهم.**

**ولا اسمٌ لصنفٍ يدخل**: لا يُقال اسمٌ ولا فعلٌ ولا حرف — **تُعَدّ الصورُ
المضبوطةُ على الهيكل الواحد وتُعرَض ببايتاتها**، ولا يُسمّى فرقُها.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
ASCENT = REPOSITORY / "examples" / "rasm" / "run_discovered_ascent.py"
HUFFMAN = REPOSITORY / "examples" / "rasm" / "run_huffman_ascent.py"
LICENCE = REPOSITORY / "examples" / "rasm" / "run_greedy_licence.py"
PEEL = REPOSITORY / "examples" / "rasm" / "run_cv_peel.py"
CHECK_EVERY = 500
PATIENCE = 500
MOST_PROPOSALS = 60_000
SHOWN = ("كتب", "علم")

Pair = tuple[int, int]
Unit = tuple[str, str]


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def words_of(text: str, peeler: object) -> list[tuple[tuple[Unit, ...], str]]:
    """(صورةُ الكلمة بوحداتها، بايتاتُها من السطر) — لكلّ كلمةٍ في المصحف."""

    found: list[tuple[tuple[Unit, ...], str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        units, _ = peeler.peel(line)  # type: ignore[attr-defined]
        wide = peeler.spans(line)  # type: ignore[attr-defined]
        current: list[Unit] = []
        edges: list[tuple[int, int]] = []
        for (base, value), edge in zip(units, wide):
            if base == peeler.STRUCTURE:  # type: ignore[attr-defined]
                if current:
                    found.append((tuple(current), line[edges[0][0] : edges[-1][1]]))
                current, edges = [], []
            else:
                current.append((base, value))
                edges.append(edge)
        if current:
            found.append((tuple(current), line[edges[0][0] : edges[-1][1]]))
    return found


def census_within(
    verses: list[list[int]], flags: list[list[bool]]
) -> tuple[Counter[Pair], Counter[Pair], Counter[Pair]]:
    """أزواجٌ **داخلَ الكلمة وحدَها** — خامًا للترتيب، واستبدالًا بالشفع والوتر.

    **وممرّان لا ممرّ**: الأوّلُ يعدّ كلَّ موضعٍ مجاورٍ مشروع، والثاني
    يعدّ المتماثلَ بالمقاطع المشروعة. وجمعُهما في ممرٍّ واحدٍ **يُسقِط
    الأزواجَ التي تبدأ داخلَ مقطعٍ متماثل**، فتفارق العدّاداتُ الآياتِ —
    وقد وقع ذلك وأُصلِح قبل الختم.
    """

    raw: Counter[Pair] = Counter()
    even: Counter[Pair] = Counter()
    odd: Counter[Pair] = Counter()
    for index, (row, head) in enumerate(zip(verses, flags)):
        here = even if index % 2 == 0 else odd
        for place in range(len(row) - 1):
            if head[place + 1]:
                continue
            one, two = row[place], row[place + 1]
            raw[(one, two)] += 1
            if one != two:
                here[(one, two)] += 1
        place = 0
        while place < len(row):
            stop = place
            while (
                stop + 1 < len(row)
                and not head[stop + 1]
                and row[stop + 1] == row[place]
            ):
                stop += 1
            paired = (stop - place + 1) // 2
            if paired:
                here[(row[place], row[place])] += paired
            place = stop + 1
    return (raw, even, odd)


def apply_within(
    verses: list[list[int]], flags: list[list[bool]], pair: Pair, fresh: int
) -> None:
    """الدمجُ لا يعبر حدَّ الكلمة — فالوحدةُ تنتهي حيث تنتهي الكلمة."""

    left, right = pair
    for index, row in enumerate(verses):
        head = flags[index]
        built: list[int] = []
        marks: list[bool] = []
        place = 0
        while place < len(row):
            joined = (
                place + 1 < len(row)
                and row[place] == left
                and row[place + 1] == right
                and not head[place + 1]
            )
            if joined:
                built.append(fresh)
                marks.append(head[place])
                place += 2
            else:
                built.append(row[place])
                marks.append(head[place])
                place += 1
        verses[index] = built
        flags[index] = marks


def entropy_of(table: dict[tuple[str, ...], Counter[tuple[Unit, ...]]]) -> float:
    """`H(الصورة | الهيكل)` داخلَ العيّنة، بتًّا للكلمة."""

    mass = sum(sum(one.values()) for one in table.values())
    return math.fsum(
        sum(one.values())
        / mass
        * -math.fsum(
            (number / sum(one.values())) * math.log2(number / sum(one.values()))
            for number in one.values()
        )
        for one in table.values()
    )


def held_out(
    pairs: list[tuple[tuple[str, ...], tuple[Unit, ...]]],
) -> tuple[float, float, float]:
    """(الثمنُ على الكلم كلِّها، على المشهودِ مفتاحُها، نصيبُ غيرِ المشهود).

    **والفصلُ لازم**: ثمنُ كلمةٍ لم يُرَ مفتاحُها قطُّ ليس ثمنَ **غموضِ
    الهيكل** بل ثمنَ **غيابِه**؛ وخلطُهما يُضخِّم الدَّينَ المعجميَّ بما
    ليس منه. فيُفصَل، ويُنشَر النصيبان.
    """

    even = [one for index, one in enumerate(pairs) if index % 2 == 0]
    odd = [one for index, one in enumerate(pairs) if index % 2]
    first = _cross(even, odd)
    second = _cross(odd, even)
    return (
        (first[0] + second[0]) / 2,
        (first[1] + second[1]) / 2,
        (first[2] + second[2]) / 2,
    )


def _cross(
    support: list[tuple[tuple[str, ...], tuple[Unit, ...]]],
    measure: list[tuple[tuple[str, ...], tuple[Unit, ...]]],
) -> tuple[float, float, float]:
    table: dict[tuple[str, ...], Counter[tuple[Unit, ...]]] = defaultdict(Counter)
    plain: Counter[tuple[Unit, ...]] = Counter()
    for key, form in support:
        table[key][form] += 1
        plain[form] += 1
    alphabet = max(len(plain), 1)
    base = sum(plain.values())
    charge = 0.0
    seen_charge = 0.0
    seen = 0
    for key, form in measure:
        counts = table.get(key)
        if counts is None:
            charge -= math.log2((plain.get(form, 0) + 1) / (base + alphabet))
            continue
        mass = sum(counts.values())
        price = -math.log2((counts.get(form, 0) + 1) / (mass + alphabet))
        charge += price
        seen_charge += price
        seen += 1
    whole = max(len(measure), 1)
    return (
        charge / whole,
        seen_charge / max(seen, 1),
        (whole - seen) / whole,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    huffman = _load(HUFFMAN, "run_huffman_ascent")
    licence = _load(LICENCE, "run_greedy_licence")
    peeler = _load(PEEL, "run_cv_peel")
    text = given.text.read_text(encoding="utf-8")

    print("— ١) عدُّ الكلم والهياكل")
    words = words_of(text, peeler)
    table: dict[tuple[str, ...], Counter[tuple[Unit, ...]]] = defaultdict(Counter)
    bytes_of: dict[tuple[Unit, ...], str] = {}
    for form, shape in words:
        table[tuple(base for base, _ in form)][form] += 1
        bytes_of.setdefault(form, shape)
    tokens = len(words)
    skeletons = len(table)
    vague = {key: one for key, one in table.items() if len(one) > 1}
    vague_mass = sum(sum(one.values()) for one in vague.values())
    print(f"  الكلمُ: {tokens}")
    print(f"  هياكلُ متمايزة: {skeletons}")
    print(f"  غامضةٌ منها: {len(vague)} " f"({len(vague) / skeletons:.4f} من الهياكل)")
    print(f"  كتلتُها من الكلم: {vague_mass} " f"({vague_mass / tokens:.4f} من الكلم)")

    print("\n— ٢) الفصلُ على هيكلٍ واحد — ببايتاته لا باسمه")
    for name in SHOWN:
        key = tuple(name)
        counts = table.get(key)
        if counts is None:
            print(f"  {name}: لا هيكلَ بهذه الوحدات")
            continue
        total = sum(counts.values())
        parts = " | ".join(
            f"{bytes_of[form]}×{number}" for form, number in counts.most_common()
        )
        print(f"  هيكلٌ بـ{len(key)} وحدات ({total} كلمة، {len(counts)} صورة): {parts}")

    print("\n— ٣) ثمنُ الدَّينين — محجوزًا")
    inside = entropy_of(table)
    plain_pairs = [(tuple(base for base, _ in form), form) for form, _ in words]
    plain_debt, plain_seen, plain_missing = held_out(plain_pairs)
    before: list[tuple[str, ...]] = [()] + [
        tuple(base for base, _ in form) for form, _ in words[:-1]
    ]
    context_pairs = [
        (tuple(base for base, _ in form) + ("|",) + earlier, form)
        for (form, _), earlier in zip(words, before)
    ]
    context_debt, context_seen, context_missing = held_out(context_pairs)
    print(f"  H(الصورة | الهيكل) داخلَ العيّنة: {inside:.4f} بتًّا للكلمة")
    print(
        f"  الدَّينُ المعجميُّ محجوزًا على الكلم كلِّها: {plain_debt:.4f} "
        f"(غيرُ مشهودٍ مفتاحُه {plain_missing:.4f})"
    )
    print(f"  وعلى ما شُهِد مفتاحُه وحدَه:              {plain_seen:.4f} بتًّا للكلمة")
    print(
        f"  وبسياقِ هيكلٍ واحدٍ قبلَه: على الكلم كلِّها {context_debt:.4f} "
        f"(غيرُ مشهودٍ {context_missing:.4f})"
    )
    print(f"  وعلى ما شُهِد مفتاحُه وحدَه:              {context_seen:.4f} بتًّا للكلمة")
    print(f"  الفرقُ على المشهود (بسياقٍ − بلا سياق): {context_seen - plain_seen:+.4f}")
    print(f"  جملةُ الدَّين على المشهود: {plain_seen * tokens:.0f} بتًّا")

    print("\n— ٤) التصعيدُ الجشع إلى الكلمة")
    verses, heads, order, lines, reach = ascent.corpus_of(text)  # type: ignore[attr-defined]
    flags = [list(one) for one in heads]
    origin = [list(one) for one in verses]
    widths: dict[int, int] = {index: 1 for index in range(len(order))}
    spelling: dict[int, tuple[int, ...]] = {
        index: (index,) for index in range(len(order))
    }
    even: Counter[int] = Counter()
    odd: Counter[int] = Counter()
    for index, row in enumerate(verses):
        (even if index % 2 == 0 else odd).update(row)
    here = licence.cost_of(even, odd, widths)  # type: ignore[attr-defined]
    start = here
    print(f"  نقطةُ الصفر: الجملة {here[0]:.0f} | وحداتٌ {here[3]}")

    banned: set[Pair] = set()
    ranking: list[Pair] = []
    pointer = 0
    exact_even: Counter[Pair] = Counter()
    exact_odd: Counter[Pair] = Counter()
    commits = proposals = refusals = rises = streak = 0
    worst = abs(here[0] - huffman.cost_now(verses, widths)[0])  # type: ignore[attr-defined]
    nid = len(order)
    stop = "الأزواجُ نفدت"
    while proposals < MOST_PROPOSALS and streak < PATIENCE:
        if pointer >= len(ranking):
            raw, exact_even, exact_odd = census_within(verses, flags)
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
        after_even = licence.moved(  # type: ignore[attr-defined]
            even, pair, nid, exact_even.get(pair, 0)
        )
        after_odd = licence.moved(  # type: ignore[attr-defined]
            odd, pair, nid, exact_odd.get(pair, 0)
        )
        there = licence.cost_of(after_even, after_odd, widths)  # type: ignore[attr-defined]
        if there[0] < here[0]:
            spelling[nid] = spelling[pair[0]] + spelling[pair[1]]
            apply_within(verses, flags, pair, nid)
            even, odd, here = after_even, after_odd, there
            nid += 1
            commits += 1
            streak = 0
            ranking = []
            pointer = 0
            if commits % CHECK_EVERY == 0:
                mirror = huffman.cost_now(verses, widths)  # type: ignore[attr-defined]
                worst = max(worst, abs(here[0] - mirror[0]))
                print(
                    f"    بعد {commits}: الجملة {here[0]:.0f} | أبجديّة {here[4]} "
                    f"| رموزٌ {here[3]} | نسبةٌ {here[0] / start[0]:.4f} "
                    f"| مرفوضاتٌ {refusals}"
                )
        else:
            del widths[nid]
            banned.add(pair)
            refusals += 1
            streak += 1
    else:
        stop = f"توالى {PATIENCE} رفضًا" if streak >= PATIENCE else "بلغ سقفَ الاقتراحات"

    whole = 0
    covered = 0
    for row, head in zip(verses, flags):
        for place, symbol in enumerate(row):
            if head[place] and (place + 1 == len(row) or head[place + 1]):
                whole += 1
            covered += 1
    print(f"  الوقوف: {stop}")
    print(
        f"    اقتراحاتٌ {proposals} | التزاماتٌ {commits} | مرفوضاتٌ {refusals} "
        f"| بلا نزولٍ {rises}"
    )
    print(
        f"    الجملة {here[0]:.0f} | النسبةُ إلى L₀ {here[0] / start[0]:.4f} "
        f"| رموزٌ {here[3]} | أبجديّة {here[4]}"
    )
    mismatch = 0
    for row, source in zip(verses, origin):
        laid: list[int] = []
        for symbol in row:
            laid.extend(spelling[symbol])
        mismatch += abs(len(laid) - len(source))
        mismatch += sum(1 for one, two in zip(laid, source) if one != two)
    print(f"    الرجعة: مواضعُ الخلاف = {mismatch}")
    crossing, total_units = ascent.straddles(verses, heads, widths)  # type: ignore[attr-defined]
    print(f"    العابرُ لحدّ الكلمة: {crossing} من {total_units}")
    print(f"    كلمٌ صارت رمزًا واحدًا: {whole} من {tokens} = {whole / tokens:.4f}")
    print(f"    أقصى انحرافٍ بين الآلتين: {worst:.9f}")
    print("    وجملةُ `69a1c10c…` بلا قيدٍ كانت 1400392")
    return 0


if __name__ == "__main__":
    sys.exit(main())
