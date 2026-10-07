"""تشغيلُ قاعدة الفصل المُودَعة — تشغيلُ ختم `7bf3ccd8…`.

**تُقرأ القاعدةُ من `deposits/separation_rule.md` ولا تُكتَب ههنا**: الأنماطُ
تُستخرَج من جداول المواصفة بنمطٍ صريح، فإن بُدِّلت المواصفةُ تبدّل التشغيل،
ولا تُنسَخ قائمةٌ في الشفرة تفارقها صامتة.

**والحُكمُ بالمحجوز لا بشاهد**: لا جردَ صحيحًا يُقابَل به، فلا تُقاس
الدقّة. وتُقاس **المنفعة**: أينزل الثمنُ المحجوزُ للوحدة عن مستوى اللفظ
(٤٫٢١١٨) أم لا؟ وأينزل نصيبُ المرتدّ عن ٠٫١٩٧٢؟

**والمواصفةُ غيرُ موقَّعة**، فحالُ مستوى الكلمة المفردة يبقى
`UNCLASSIFIED` مهما كان الرقم — **تُقاس ولا تُرقّي مستوًى**.

**ولا اسمٌ لصنفٍ يدخل**: وحداتٌ وأصولٌ وبتّات.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
ASCENT = REPOSITORY / "examples" / "rasm" / "run_discovered_ascent.py"
LICENCE = REPOSITORY / "examples" / "rasm" / "run_greedy_licence.py"
LADDER = REPOSITORY / "examples" / "rasm" / "run_markov_ladder.py"
RULE = REPOSITORY / "deposits" / "separation_rule.md"
LEAST = 2
BY_TOKEN = 4.2118
BY_SYMBOL = 3.6549
TOKEN_MISSING = 0.1972
TOKEN_KINDS = 17_909


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_rule() -> tuple[tuple[tuple[str, ...], ...], tuple[str, ...]]:
    """(المقدّماتُ برتبها، اللواحق) — مقروءةً من المواصفة لا مكتوبةً ههنا."""

    text = RULE.read_text(encoding="utf-8")
    ranks: list[tuple[str, ...]] = []
    for line in text.splitlines():
        hit = re.match(r"^\| [١٢٣] \| (.+?) \|$", line.strip())
        if hit:
            ranks.append(
                tuple(
                    "".join(one.split())
                    for one in hit.group(1).replace("`", "").split("·")
                )
            )
    block = re.search(r"## ٤\) اللواحق[^\n]*\n\n(.+?)\n\n", text, re.DOTALL)
    if block is None or len(ranks) != 3:
        raise SystemExit("المواصفةُ لا تُقرَأ: جداولُ المقدّمات أو اللواحق")
    tails = tuple(
        "".join(one.split())
        for one in block.group(1).replace("`", "").replace("\n", " ").split("·")
    )
    ordered = tuple(tuple(sorted(rank, key=len, reverse=True)) for rank in ranks)
    return (ordered, tuple(sorted(tails, key=len, reverse=True)))


def split_token(
    bases: list[str],
    heads: tuple[tuple[str, ...], ...],
    tails: tuple[str, ...],
) -> list[int]:
    """أطوالُ الكلمات في اللفظ — والشرطُ: لا تقلّ البقيّةُ عن وحدتين."""

    start = 0
    stop = len(bases)
    cuts: list[int] = []
    for rank in heads:
        for one in rank:
            width = len(one)
            if stop - start - width < LEAST:
                continue
            if "".join(bases[start : start + width]) == one:
                cuts.append(width)
                start += width
                break
    end: list[int] = []
    for one in tails:
        width = len(one)
        if stop - start - width < LEAST:
            continue
        if "".join(bases[stop - width : stop]) == one:
            end.append(width)
            stop -= width
            break
    return [*cuts, stop - start, *reversed(end)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    licence = _load(LICENCE, "run_greedy_licence")
    ladder = _load(LADDER, "run_markov_ladder")
    heads_rule, tails_rule = read_rule()
    print("— القاعدةُ كما قُرئت من المواصفة")
    for index, rank in enumerate(heads_rule, start=1):
        print(f"  مقدّماتُ الرتبة {index}: {' · '.join(rank)}")
    print(f"  اللواحق: {' · '.join(tails_rule)}")
    signed = "**التوقيع**: — (غيرُ موقَّعة)" in RULE.read_text(encoding="utf-8")
    print(f"  غيرُ موقَّعة: {signed}")

    verses, heads, order, _lines, _reach = ascent.corpus_of(  # type: ignore[attr-defined]
        given.text.read_text(encoding="utf-8")
    )
    units = sum(len(one) for one in verses)
    bases = [base for base, _value in order]

    tokens: list[list[int]] = []
    for row, head in zip(verses, heads):
        current: list[int] = []
        for symbol, fresh in zip(row, head):
            if fresh and current:
                tokens.append(current)
                current = []
            current.append(symbol)
        if current:
            tokens.append(current)
    print(f"\n— الألفاظ: {len(tokens)} | وحداتٌ {units}")

    words: list[tuple[int, ...]] = []
    cut_tokens = 0
    mismatch = 0
    pieces: Counter[int] = Counter()
    for token in tokens:
        spelling = [bases[one] for one in token]
        widths = split_token(spelling, heads_rule, tails_rule)
        if sum(widths) != len(token):
            mismatch += 1
            widths = [len(token)]
        place = 0
        for width in widths:
            words.append(tuple(token[place : place + width]))
            place += width
        pieces[len(widths)] += 1
        if len(widths) > 1:
            cut_tokens += 1
    rejoined = 0
    place = 0
    for token in tokens:
        taken: list[int] = []
        while len(taken) < len(token):
            taken.extend(words[place])
            place += 1
        if taken != token:
            rejoined += 1

    table: dict[tuple[int, ...], int] = {}
    stream = [table.setdefault(one, len(table)) for one in words]
    width_of = {one: len(key) for key, one in table.items()}
    print(f"  ألفاظٌ فُصِلت: {cut_tokens} ({cut_tokens / len(tokens):.4f})")
    print(f"  الكلماتُ الناتجة: {len(words)} | أنواعٌ {len(table)}")
    print(f"  قسمةُ القطع: {sorted(pieces.items())}")
    print(f"  الرجعة: ألفاظٌ لا تُستعاد = {rejoined} | أطوالٌ مخالفة = {mismatch}")

    one = ladder.price(stream, width_of, licence)  # type: ignore[attr-defined]
    inside = one[1] * len(stream) / units
    outside = one[2] * len(stream) / units
    print("\n— ثمنُ المستوى المفصول")
    print(
        f"  N {len(stream)} | أبجديّة {int(one[6])} | H {one[0]:.4f} "
        f"| L ملحقًا {one[1]:.4f} | L محجوزًا {one[2]:.4f} | مرتدّ {one[3]:.4f} "
        f"| I {one[4]:.4f}"
    )
    print(f"  للوحدة ملحقًا {inside:.4f} | للوحدة محجوزًا {outside:.4f}")
    thin = one[0] * len(stream) - one[5]
    print(f"  L−H {one[1] - one[0]:+.4f} | N·H − تباديل {thin:+.1f}")
    print("\n— الحكمُ بالمحجوز")
    print(f"  مقابلَ اللفظ ({BY_TOKEN}): {outside - BY_TOKEN:+.4f}")
    print(f"  مقابلَ الرمز المُرخَّص ({BY_SYMBOL}): {outside - BY_SYMBOL:+.4f}")
    print(f"  المرتدُّ مقابلَ اللفظ ({TOKEN_MISSING}): {one[3] - TOKEN_MISSING:+.4f}")
    print(f"  الأنواعُ مقابلَ اللفظ ({TOKEN_KINDS}): {int(one[6]) - TOKEN_KINDS:+d}")
    print(
        "\n— وحالُ مستوى الكلمة المفردة يبقى UNCLASSIFIED: "
        "المواصفةُ غيرُ موقَّعة، والقياسُ لا يُرقّي مستوًى"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
