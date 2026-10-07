"""تشغيلُ الإسقاط المُودَع π_اشتقاقي: توكن ⟼ جذر — وقياسُ كونِه دالّة.

**المُودَع** (`projection_specs.md` §١): Σ وحداتُ الكلم، وΛ جذورُ ابن فارس،
والقرارُ الأوّلُ **«التجريدُ بحذف الزوائد العشر — مفتاحُها سألتمونيها»**.

**ما يُشغَّل ههنا هو القرارُ الأوّلُ وحدَه**، لأنّ القرارَ الثاني يُحيل إلى
«الجدول الموروث» لردّ المعتلّ **ولم يُودَع معه**. ويُعلَن أثرُ ذلك في
الاتّجاهين: ردُّ المعتلّ **يزيد** المرشّحات، فرقمُ التغطية ههنا **حدٌّ
أدنى**، ورقمُ الالتباس **حدٌّ أدنى أيضًا** — فلا يُصلِحه القرارُ الثاني.

**القراءةُ الحرفيّةُ للقرار الأوّل**: الجذرُ ثلاثةُ حروفٍ تُبقى على ترتيبها،
وكلُّ محذوفٍ من الزوائد العشر. فإن وقع الناتجُ في Λ فهو مرشّح. والدالّةُ
تقتضي مرشّحًا **واحدًا**؛ وما زاد فالإسقاطُ عليه **علاقةٌ لا دالّة**.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
ROOT_TABLE = REPOSITORY / "maqayis_by_root_csv_999.csv"
AUGMENTS = frozenset("سألتمونيها")
"""مفتاحُ الزوائد العشر — القرارُ الأوّلُ من الإيداع."""

MARKUP = "<sel>"
MARKS = re.compile(r"[ً-ْٰـ]")
ROOT_LENGTH = 3


def read_roots(table: Path) -> frozenset[str]:
    """Λ: الجذورُ المتمايزةُ في مادّة المقاييس."""

    csv.field_size_limit(1 << 30)
    found: set[str] = set()
    with table.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            root = (row.get("root_full") or "").strip()
            if root:
                found.add(root)
    if not found:
        raise ValueError("لا جذرَ في الجدول")
    return frozenset(found)


def read_tokens(corpus: Path) -> list[str]:
    """توكناتُ المدوّنة مجرَّدةً من الشكل، والوسمُ مطروح."""

    text = MARKS.sub("", corpus.read_text(encoding="utf-8"))
    return [one for one in text.split() if one != MARKUP]


def candidates(word: str, roots: frozenset[str]) -> frozenset[str]:
    """كلُّ جذرٍ يُبلَغ بحذف زوائدَ وحدَها من هذه الكلمة."""

    length = len(word)
    if length < ROOT_LENGTH:
        return frozenset()
    reached: set[str] = set()
    for kept in combinations(range(length), ROOT_LENGTH):
        keep = set(kept)
        if all(word[index] in AUGMENTS for index in range(length) if index not in keep):
            candidate = "".join(word[index] for index in kept)
            if candidate in roots:
                reached.add(candidate)
    return frozenset(reached)


def unanchored(roots: frozenset[str]) -> frozenset[str]:
    """جذورٌ كلُّ حروفها زوائد — لا مرساةَ فيها للقرار الأوّل."""

    return frozenset(root for root in roots if set(root) <= AUGMENTS)


def survey(tokens: list[str], roots: frozenset[str]) -> Counter[int]:
    """توزيعُ عددِ المرشّحات لكلّ توكن."""

    cache: dict[str, int] = {}
    spread: Counter[int] = Counter()
    for word in tokens:
        if word not in cache:
            cache[word] = len(candidates(word, roots))
        spread[cache[word]] += 1
    return spread


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--table", type=Path, default=ROOT_TABLE)
    given = parser.parse_args()

    roots = read_roots(given.table)
    tokens = read_tokens(given.text)
    spread = survey(tokens, roots)
    total = sum(spread.values())
    empty = spread[0]
    single = spread[1]
    many = total - empty - single
    bare = unanchored(roots)

    print(f"|Λ| جذورًا متمايزة: {len(roots)}")
    print(f"جذورٌ بلا مرساةٍ في القرار الأوّل: {len(bare)}")
    print(f"توكنات: {total}")
    print(f"بلا مرشّح: {empty}")
    print(f"مرشّحٌ واحد: {single}")
    print(f"أكثرُ من مرشّح: {many}")
    print("توزيعُ المرشّحات:", dict(sorted(spread.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
