"""جبرُ الربح الجشع — بالتوافيق والتباديل، وماركوف. ختم `cfdb2184…`.

**ما يُفسَّر**: قِيس في `c8602c00…` أنّ الترتيبَ بالربح **معاكسٌ** للترتيب
بالوقوع (وسيطُ رتبةِ المختار ٢٢ من ٢٤). فلِمَ ينقلب؟

**الاشتقاق**: تكلفةُ البيان لنموذجٍ بلا سياقٍ هي **لوغاريتم عددِ التباديل
المتمايزة** لمتعدّد المجموعة — `log₂ C(N; n₁,…,n_k) = log₂ N!/∏nₛ!`. فإذا
دُمِج الزوجُ `(a,b) ⟶ f` بـ`m` استبدالًا صار الربحُ **نسبةَ معاملين
حدّيّين**، وهي بالتباديل النازلة:

    G = log₂ N^(m) − log₂ nₐ^(m) − log₂ n_b^(m) + log₂ m!

حيث `x^(m) = x!/(x−m)!` تباديلُ `m` من `x`. وبالتقريب الأوّل:

    G ≈ m · (PMI − log₂ e),    PMI = log₂ ( m·N / (nₐ·n_b) )

**فالربحُ ليس `m` بل `m` مضروبًا في فائضِ الاقتران على الاستقلال**، ناقصًا
ثابتًا `log₂ e ≈ ١٫٤٤٢٧`. **وثَمَّ ينقلب الترتيب**: زوجٌ طرفاه كثيرا الوقوع
يلتقيان بالمصادفة فـ`PMI` صغيرة ولو كان `m` كبيرًا؛ وزوجٌ نادرٌ لا يقع
طرفاه إلّا معًا فـ`PMI` كبيرة.

**وماركوف**: `Σ p(a,b)·PMI(a,b) = I(Xₜ ; Xₜ₊₁)` — فالمُستخرَجُ بالدمج هو
**بعينه** ما تحمله السلسلةُ من اقترانٍ يُغفِله نموذجُ اللاسياق.

**والاستقراءان**: `induction on` — الهويّةُ تُصان عند كلّ دمجة (تُفحَص
عند نقاط الفحص)؛ و`induction FOR` — الحلقةُ التي تشهد عليها عددًا عددًا.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ ووقوعاتٌ وتكلفةٌ فقط.
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
LOOKED = 200
CHECK_EVERY = 500
STEPS = 2_000
LOG2E = math.log2(math.e)

# من `deposits/huffman_ascent_run.log` — تُقابَل بالسجلّ في الحكم لا تُنقَل ثقةً
ZERO_INSIDE = 2_044_336
BEST_INSIDE = 1_383_540
BEST_BOOK = 163_822

Pair = tuple[int, int]


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def falling(whole: int, take: int) -> float:
    """log₂ من التباديل النازلة `x^(m) = x!/(x−m)!` — بلا فيض."""

    if take <= 0:
        return 0.0
    return (math.lgamma(whole + 1) - math.lgamma(whole - take + 1)) / math.log(2)


def arrangements(counts: Counter[int]) -> float:
    """log₂ من عدد التباديل المتمايزة لمتعدّد المجموعة — `log₂ N!/∏nₛ!`."""

    total = sum(counts.values())
    return (
        math.lgamma(total + 1)
        - math.fsum(math.lgamma(one + 1) for one in counts.values())
    ) / math.log(2)


def gain_exact(total: int, left: int, right: int, taken: int, same: bool) -> float:
    """الربحُ بالتباديل تامًّا — ونصفُ الحالة حين يكون الطرفان واحدًا."""

    if same:
        return falling(total, taken) - falling(left, 2 * taken) + falling(taken, taken)
    return (
        falling(total, taken)
        - falling(left, taken)
        - falling(right, taken)
        + falling(taken, taken)
    )


def pointwise(total: int, left: int, right: int, taken: int) -> float:
    """فائضُ الاقتران على الاستقلال، بتًّا للوقوع الواحد."""

    return math.log2(taken * total / (left * right))


def ranks(values: list[float]) -> list[float]:
    """رتبٌ بمتوسّط المتساوي — فلا يُرجَّح تساوٍ بترتيبِ ورودٍ عارض."""

    order = sorted(range(len(values)), key=lambda one: values[one])
    found = [0.0] * len(values)
    place = 0
    while place < len(order):
        stop = place
        while stop + 1 < len(order) and values[order[stop + 1]] == values[order[place]]:
            stop += 1
        middle = (place + stop) / 2 + 1
        for index in range(place, stop + 1):
            found[order[index]] = middle
        place = stop + 1
    return found


def spearman(first: list[float], second: list[float]) -> float:
    """ارتباطُ الرتب — ولا يُفترَض خطّيّةٌ ولا توزيع."""

    one, two = ranks(first), ranks(second)
    count = len(one)
    if count < 2:
        return 0.0
    mean_one = math.fsum(one) / count
    mean_two = math.fsum(two) / count
    top = math.fsum((a - mean_one) * (b - mean_two) for a, b in zip(one, two))
    left = math.sqrt(math.fsum((a - mean_one) ** 2 for a in one))
    right = math.sqrt(math.fsum((b - mean_two) ** 2 for b in two))
    return top / (left * right) if left and right else 0.0


def markov(verses: list[list[int]]) -> tuple[float, float, float, float, int]:
    """(H للتالي، H للتالي بشرط السابق، I، Σ p·PMI، عددُ المواضع الزوجيّة).

    `I = H(Xₜ₊₁) − H(Xₜ₊₁|Xₜ)` — **فالهامشُ الأيمنُ لا الأيسر**؛ وخلطُهما
    يُخرِج رقمًا يشبه `I` ولا يساوي `Σ p·PMI`، فيُقرَأ اتّساقًا وليس به.
    """

    joint: Counter[Pair] = Counter()
    for row in verses:
        for one, two in zip(row, row[1:]):
            joint[(one, two)] += 1
    total = sum(joint.values())
    left: Counter[int] = Counter()
    right: Counter[int] = Counter()
    for (one, two), number in joint.items():
        left[one] += number
        right[two] += number
    first = -math.fsum((one / total) * math.log2(one / total) for one in right.values())
    after = -math.fsum(
        (number / total) * math.log2(number / left[one])
        for (one, _two), number in joint.items()
    )
    carried = math.fsum(
        (number / total)
        * math.log2((number / total) / ((left[one] / total) * (right[two] / total)))
        for (one, two), number in joint.items()
    )
    return (first, after, first - after, carried, total)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    licence = _load(LICENCE, "run_greedy_licence")
    verses, _heads, order, _lines, _reach = ascent.corpus_of(  # type: ignore[attr-defined]
        given.text.read_text(encoding="utf-8")
    )
    whole: Counter[int] = Counter()
    for row in verses:
        whole.update(row)
    total = sum(whole.values())
    print(f"L₀: {total} وحدةً | أبجديّة {len(order)} | آيات {len(verses)}")

    print("\n— ١) التكلفةُ لوغاريتمُ التباديل المتمايزة")
    laid = arrangements(whole)
    coded_now = licence.coded(whole, whole)[0]  # type: ignore[attr-defined]
    level = -math.fsum((one / total) * math.log2(one / total) for one in whole.values())
    print(f"  log₂ من تباديل متعدّد المجموعة: {laid:.4f} بتًّا")
    print(f"  N·H بالإنتروبيا:                {total * level:.4f} بتًّا")
    print(f"  الفرقُ للرمز الواحد:            {(total * level - laid) / total:+.6f}")
    print(f"  N·L بشفرة هوفمان:               {total * coded_now:.4f} بتًّا")
    print(f"  L − H للرمز:                    {coded_now - level:+.6f}")

    print("\n— ٢) ماركوف: ما تحمله السلسلةُ ويُغفِله اللاسياق")
    one_h, after_h, carried, summed, places = markov(verses)
    print(f"  H(Xₜ₊₁) = {one_h:.6f} | H(Xₜ₊₁|Xₜ) = {after_h:.6f}")
    print(f"  I(Xₜ;Xₜ₊₁) = {carried:.6f} بتًّا للموضع")
    print(f"  Σ p·PMI    = {summed:.6f}")
    print(f"  |I − Σ p·PMI| = {abs(carried - summed):.12f}")
    print(
        f"  مواضعُ الجوار {places} | السقفُ من الرتبة الأولى {places * carried:.0f} بتًّا"
    )

    print(f"\n— ٣) {LOOKED} زوجًا: الربحُ المشتَقّ مقابلَ الربح المقيس")
    _raw, even_pairs, odd_pairs = licence.census(verses)  # type: ignore[attr-defined]
    taken: Counter[Pair] = Counter()
    for pair, number in even_pairs.items():
        taken[pair] += number
    for pair, number in odd_pairs.items():
        taken[pair] += number
    candidates = [pair for pair, number in taken.most_common(LOOKED) if number > 1]
    counts: list[float] = []
    derived: list[float] = []
    leading: list[float] = []
    excess: list[float] = []
    measured: list[float] = []
    fresh = len(order)
    for pair in candidates:
        number = taken[pair]
        same = pair[0] == pair[1]
        left, right = whole[pair[0]], whole[pair[1]]
        after = licence.moved(whole, pair, fresh, number)  # type: ignore[attr-defined]
        rest = sum(after.values())
        was = licence.coded(whole, whole)[0] * total  # type: ignore[attr-defined]
        now = licence.coded(after, after)[0] * rest  # type: ignore[attr-defined]
        counts.append(float(number))
        derived.append(gain_exact(total, left, right, number, same))
        excess.append(pointwise(total, left, right, number))
        leading.append(number * (excess[-1] - LOG2E))
        measured.append(was - now)
    print(f"  أزواجٌ مقيسة: {len(candidates)}")
    print(f"  ρ(الوقوع، الربحِ المقيس)   = {spearman(counts, measured):+.4f}")
    print(f"  ρ(المشتَقّ، الربحِ المقيس)  = {spearman(derived, measured):+.4f}")
    print(f"  ρ(التقريبِ، الربحِ المقيس) = {spearman(leading, measured):+.4f}")
    print(f"  ρ(PMI، الربحِ المقيس)      = {spearman(excess, measured):+.4f}")
    print(f"  ρ(الوقوع، PMI)             = {spearman(counts, excess):+.4f}")
    agree = sum(1 for one, two in zip(derived, measured) if (one > 0) == (two > 0))
    print(
        f"  توافقُ الإشارة: {agree} من {len(candidates)} = {agree / len(candidates):.4f}"
    )
    threshold = sum(
        1 for one, two in zip(excess, measured) if (one > LOG2E) == (two > 0)
    )
    print(
        f"  عتبةُ PMI > log₂e ({LOG2E:.4f}): توافقٌ {threshold} من "
        f"{len(candidates)} = {threshold / len(candidates):.4f}"
    )
    errors = sorted(
        abs(one - two) / abs(two)
        for one, two in zip(derived, measured)
        if abs(two) >= 1.0
    )
    edge = errors[min(len(errors) - 1, int(0.9 * len(errors)))]
    print(
        f"  |المشتَقّ − المقيس| ÷ |المقيس| على ما |ربحُه| ≥ ١ بتًّا "
        f"({len(errors)} زوجًا): وسيطٌ {errors[len(errors) // 2]:.4f} "
        f"| أدنى {errors[0]:.4f} | المئينُ ٩٠ {edge:.4f} | أعلى {errors[-1]:.4f}"
    )

    print("\n— ٤) السقفُ الماركوفيُّ من الرتبة الأولى")
    saved = (ZERO_INSIDE - 0) - (BEST_INSIDE - BEST_BOOK)
    ceiling = places * carried
    print(f"  بيانُ نقطة الصفر داخلَ العيّنة: {ZERO_INSIDE}")
    print(f"  بيانُ أفضلِ نقطةٍ كتليّةٍ داخلَ العيّنة: {BEST_INSIDE - BEST_BOOK}")
    print(f"  فالمُوفَّرُ: {saved} بتًّا")
    print(f"  والسقفُ من الرتبة الأولى: {ceiling:.0f} بتًّا")
    print(f"  النسبةُ المُوفَّر ÷ السقف: {saved / ceiling:.4f}")
    print(
        "  فإن جاوزت الواحدَ فالصعودُ يبلغ ما فوق الرتبة الأولى، "
        "وإن لم تجاوزه فما بلغه يسعه اقترانُ الجارين وحدَه"
    )

    print("\n— ٥) استقراءٌ على الدمجات: أتُصان الهويّةُ صعودًا؟")
    widths: dict[int, int] = {index: 1 for index in range(len(order))}
    state = [list(row) for row in verses]
    live = Counter(whole)
    worst = 0.0
    marked: set[Pair] = set()
    made = 0
    nid = len(order)
    while made < STEPS:
        pick = ascent.best_pair(state)  # type: ignore[attr-defined]
        if pick is None or pick[0] in marked:
            break
        pair = pick[0]
        _raw2, even2, odd2 = licence.census(state)  # type: ignore[attr-defined]
        number = even2.get(pair, 0) + odd2.get(pair, 0)
        widths[nid] = widths[pair[0]] + widths[pair[1]]
        live = licence.moved(live, pair, nid, number)  # type: ignore[attr-defined]
        ascent.apply_merge(state, pair, nid)  # type: ignore[attr-defined]
        nid += 1
        made += 1
        if made % CHECK_EVERY == 0:
            here: Counter[int] = Counter()
            for row in state:
                here.update(row)
            assert here == live, f"العدّاداتُ فارقت الآياتِ عند {made}"
            count = sum(here.values())
            laid_now = arrangements(here)
            level_now = -math.fsum(
                (one / count) * math.log2(one / count) for one in here.values()
            )
            code_now = licence.coded(here, here)[0]  # type: ignore[attr-defined]
            drift = (count * level_now - laid_now) / count
            worst = max(worst, abs(drift))
            print(
                f"  بعد {made}: أبجديّة {len(here)} | N {count} "
                f"| تباديلُ {laid_now:.0f} | N·H {count * level_now:.0f} "
                f"| للرمز {drift:+.6f} | L−H {code_now - level_now:+.6f}"
            )
    print(f"  أقصى فرقٍ للرمز بين التباديل وN·H على النقاط: {worst:+.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
