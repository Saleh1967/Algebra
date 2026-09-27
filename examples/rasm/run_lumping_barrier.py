"""حاجزُ التكتيل: الهويّةُ تُغلِق، والأمثلُ في `3ⁿ`، **وdalّةُ الكتلة ليست submodular**.

**ولا مدوّنةَ ههنا ولا لغة**: عدّاداتٌ مولَّدةٌ ببذرةٍ مُعلَنة، فالتشغيلُ
**يُعاد بعينه** عند كلّ أحد. وما يُقاس **رياضيّاتٌ تامّةٌ على أيّ مُدخَل**.

**وثلاثةُ أشياء تُعرَض**: أنّ الصيغتين مقدارٌ واحد، وأنّ البرمجةَ
الديناميكيّةَ تبلغ ما يبلغه التعدادُ التامّ، وأنّ الحاجزَ `3ⁿ` لا `B(n)`.
**ورابعٌ يُنقَض**: دعوى الضمان للجشع بـ`submodular`.
"""

from __future__ import annotations

import math
import random
from itertools import combinations

from algebra.lumping_loss import (
    best_partition,
    block_cost,
    constant_term,
    greedy_partition,
    identity_drift,
    loss_by_blocks,
)
from algebra.stirling import bell

SEED = 7
UNITS = 8
BOXES = 4
CEILING = 40
TRIALS = 200
NOISE = 2**-52
WIDE = 112
FAILING_SEED = 339
FAILING_UNITS = 7
FAILING_BOXES = 3
FAILING_CEILING = 9


def counts_of(many: int, wide: int, seed: int, ceiling: int) -> list[list[int]]:
    stream = random.Random(seed)
    return [[stream.randint(1, ceiling) for _ in range(wide)] for _ in range(many)]


def partitions_of(many: int) -> list[list[list[int]]]:
    """تعدادٌ تامٌّ لقسمات المجموعة — **للمقابلة لا للاستعمال**."""

    if many == 1:
        return [[[0]]]
    found: list[list[list[int]]] = []
    for smaller in partitions_of(many - 1):
        for index in range(len(smaller)):
            found.append(
                [
                    [*block, many - 1] if index == place else list(block)
                    for place, block in enumerate(smaller)
                ]
            )
        found.append([list(block) for block in smaller] + [[many - 1]])
    return found


def main() -> int:
    print(f"— لا مدوّنةَ ههنا: عدّاداتٌ ببذرةٍ {SEED}")
    print(f"— وحداتٌ {UNITS} | خاناتٌ {BOXES} | سقفُ العدّاد {CEILING}")
    counts = counts_of(UNITS, BOXES, SEED, CEILING)
    print(f"— مجموعُ الوقوعات: {sum(sum(one) for one in counts)}")
    print(f"— الثابتُ Σ w·H(P_u): {constant_term(counts):.6f}")

    print(f"\n— الهويّةُ على {TRIALS} قسمةٍ عشوائيّة")
    stream = random.Random(SEED + 4)
    worst = 0.0
    for _ in range(TRIALS):
        blocks = stream.randint(2, 5)
        labels = [stream.randrange(blocks) for _ in range(UNITS)]
        parts = [
            [one for one in range(UNITS) if labels[one] == which]
            for which in range(blocks)
        ]
        parts = [one for one in parts if one]
        worst = max(worst, identity_drift(counts, parts))
    print(f"— أقصى انحرافٍ بين الصيغتين: {worst:.6e}")
    hum = sum(sum(one) for one in counts) * NOISE
    print(f"— وضجيجُ الآلة على هذا المقدار نحو: {hum:.6e}")
    print(f"— أتُغلِق؟ {'نعم' if worst < 1e-9 else 'لا'}")

    print("\n— البرمجةُ الديناميكيّةُ مقابَلةً بالتعداد التامّ")
    print("  وحداتٌ | كتلٌ | قسماتٌ عُدَّت | أمثلُ التعداد | أمثلُ البرمجة | فرقٌ")
    astray = 0
    for many in (6, 7):
        here = counts_of(many, BOXES, SEED + many, CEILING)
        every = partitions_of(many)
        for blocks in range(1, many + 1):
            same = [one for one in every if len(one) == blocks]
            lowest = min(loss_by_blocks(here, one) for one in same)
            found, _ = best_partition(here, blocks)
            gap = abs(found - lowest)
            if gap >= 1e-9:
                astray += 1
            print(
                f"  {many} | {blocks} | {len(same)} | {lowest:.6f}"
                f" | {found:.6f} | {gap:.3e}"
            )
    print(f"— مقاماتٌ خالفت: {astray}")

    print("\n— الحاجزُ: 3ⁿ دون B(n) — والفرقُ يُعَدّ لا يُوصَف")
    print("  n | 3ⁿ | B(n) | B(n)/3ⁿ")
    for many in range(8, 15):
        print(f"  {many} | {3**many} | {bell(many)} | {bell(many) / 3**many:.2f}")
    print(f"— وعند n = {WIDE}: log₁₀(3ⁿ) = {math.log10(3**WIDE):.4f}")
    print("— فيبقى ممتنعًا، والامتناعُ يُقال عددًا لا ظنًّا")

    print("\n— الجشعُ مقابَلًا بالأمثل اليقينيّ على المُدخَل نفسِه")
    print("  كتلٌ | أمثلُ يقينيّ | جشعٌ | زيادةٌ مئويّة")
    ties = 0
    tried = 0
    highest = 0.0
    for blocks in range(2, UNITS):
        exact, _ = best_partition(counts, blocks)
        rough, _ = greedy_partition(counts, blocks)
        share = (rough - exact) / exact * 100 if exact else 0.0
        highest = max(highest, share)
        tried += 1
        ties += abs(rough - exact) < 1e-9
        print(f"  {blocks} | {exact:.6f} | {rough:.6f} | {share:.4f}")
    print(f"— مقاماتٌ طابق فيها الجشعُ الأمثلَ: {ties} من {tried}")
    print(f"— أقصى زيادةٍ مئويّة: {highest:.4f}")
    print("— والجشعُ غيرُ مبرهَن: ما بُلِغ حدٌّ أعلى للخسارة، لا ضمانٌ")

    print("\n— وشاهدُ سقوطِ الجشع — **مطلوبٌ لا مفترَض**")
    print("  فمُدخَلٌ يطابق فيه الجشعُ الأمثلَ لا يُثبِت أنّه يطابقه دائمًا،")
    print("  **فيُطلَب مُدخَلٌ يسقط فيه** ويُعرَض ببذرته كي يُعاد.")
    fail = counts_of(FAILING_UNITS, FAILING_BOXES, FAILING_SEED, FAILING_CEILING)
    print(f"— بذرةٌ {FAILING_SEED} | وحداتٌ {FAILING_UNITS} | خاناتٌ {FAILING_BOXES}")
    print("  كتلٌ | أمثلُ يقينيّ | جشعٌ | زيادةٌ مئويّة")
    steepest = 0.0
    at_blocks = 0
    for blocks in range(2, FAILING_UNITS):
        exact, _ = best_partition(fail, blocks)
        rough, _ = greedy_partition(fail, blocks)
        share = (rough - exact) / exact * 100 if exact else 0.0
        if share > steepest:
            steepest, at_blocks = share, blocks
        print(f"  {blocks} | {exact:.6f} | {rough:.6f} | {share:.4f}")
    print(f"— أقصى زيادةٍ: {steepest:.4f} عند كتلٍ {at_blocks}")
    print("— وأقصاها عند أصغرِ عددِ كتل — وذلك مقامُ n الكبيرة بـk صغيرة")

    print("\n— دعوى الضمان بـsubmodular — تُنقَض عددًا")
    lowest_gap: float | None = None
    place: tuple[int, int, int] = (0, 0, 0)
    for size in range(1, UNITS - 1):
        for base in combinations(range(UNITS), size):
            here_cost = block_cost(counts, base)
            rest = [one for one in range(UNITS) if one not in base]
            for first, second in combinations(rest, 2):
                gap = (
                    block_cost(counts, (*base, first))
                    + block_cost(counts, (*base, second))
                ) - (block_cost(counts, (*base, first, second)) + here_cost)
                if lowest_gap is None or gap < lowest_gap:
                    lowest_gap = gap
                    place = (size, first, second)
    assert lowest_gap is not None
    scale = max(block_cost(counts, (one,)) for one in range(UNITS))
    print(f"— أدنى f(S+a)+f(S+b) − f(S+ab) − f(S): {lowest_gap:.6e}")
    print(f"— عند |S| = {place[0]} وعنصرين {place[1]} و{place[2]}")
    print(f"— ومقياسُ المقادير: {scale:.6f} | وضجيجُ الآلة عليه: {scale * NOISE:.6e}")
    print(f"— نسبةُ النقض إلى الضجيج: {abs(lowest_gap) / (scale * NOISE):.6e}")
    real = abs(lowest_gap) > scale * NOISE * 1e9
    print(f"— أنقضٌ حقيقيٌّ فوق الضجيج؟ {'نعم' if real else 'لا'}")

    print("\n— ما لا يدخل هذا السجلّ")
    print("  لا مدوّنةَ ولا لغةَ ولا اسمَ بابٍ — عدّاداتٌ ببذرةٍ مُعلَنة")
    print("  والحاجزُ 3ⁿ لا B(n)، وذلك تصحيحُ وصفٍ سابقٍ لا نتيجةٌ جديدة")
    print("  والنقضُ يقطع طريقَ ضمانٍ واحدًا ولا يُثبِت أنّ الجشعَ سيّئ")
    print("  و3ⁿ لا تفوق B(n) إلّا من n = 9؛ وعند 8 التعدادُ أرخص")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
