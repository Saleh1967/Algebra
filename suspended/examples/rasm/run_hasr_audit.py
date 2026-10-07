"""إعادةُ اشتقاقِ فصل الحصر والاستثناء — وتصعيدٌ بتّةً بتّة على توزيعه.

**لا قياسَ جديدًا ههنا**: لا تشجيرَ في هذه الشجرة. وإنّما **إعادةُ حسابٍ**
من الأعداد المعروضة في `deposits/hasr_rule_note.md`، **وحدٌّ لِما لا
يُعاد**، **وتسميةٌ لِما لا يُقابِل**.
"""

from __future__ import annotations

import argparse
import itertools
import math
import re
import sys
from pathlib import Path

EASTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
WESTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")
Z = 1.959963984540054


def eastern(one: object) -> str:
    return str(one).translate(WESTERN)


def western(one: str) -> str:
    return one.translate(EASTERN)


def binary(share: float) -> float:
    if share <= 0.0 or share >= 1.0:
        return 0.0
    found = -(share * math.log2(share) + (1 - share) * math.log2(1 - share))
    return 0.0 if found == 0.0 else found


def conditional(cells: list[tuple[int, int]]) -> float:
    total = sum(one for one, _ in cells)
    return math.fsum(one / total * binary(two / one) for one, two in cells if one)


def miller_madow(cells: int, total: int) -> float:
    """تصحيحُ ميلر–مادو من الرتبة الأولى لمعلوماتٍ بين حقلٍ وبتّة."""

    return (cells - 1) * (2 - 1) / (2 * total * math.log(2))


def wilson(hits: int, tries: int) -> tuple[float, float]:
    share = hits / tries
    middle = share + Z * Z / (2 * tries)
    spread = Z * math.sqrt(share * (1 - share) / tries + Z * Z / (4 * tries * tries))
    return (middle - spread) / (1 + Z * Z / tries), (middle + spread) / (
        1 + Z * Z / tries
    )


def read_cells(deposit: Path, pattern: str) -> list[tuple[str, int, int]]:
    text = deposit.read_text(encoding="utf-8")
    (row,) = re.findall(pattern, text)
    out: list[tuple[str, int, int]] = []
    for piece in row.split("·"):
        hit = re.search(r"(\S+)\s+([٠-٩]+)/([٠-٩]+)", piece.strip())
        if hit:
            out.append(
                (hit.group(1), int(western(hit.group(3))), int(western(hit.group(2))))
            )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rule", type=Path, required=True)
    given = parser.parse_args()

    text = given.rule.read_text(encoding="utf-8")
    (whole,) = re.findall(r"من \*\*([٠-٩]+)\*\*", text)
    total = int(western(whole))
    print("— لا قياسَ جديدًا: إعادةُ حسابٍ من أعدادٍ معروضةٍ في أنبوبٍ آخر")
    print(f"— المقام: {total} موضعًا")

    near = read_cells(given.rule, r"م٢ حالةُ التالي \| [٠٫\d]+ \| (.+?) \|")
    sign = read_cells(given.rule, r"م١ النفيُ السابق \| [٠٫\d]+ \| (.+?) \|")
    print(
        f"— خاناتُ «حالة التالي» المنشورة: {len(near)}" f" | «النفي السابق»: {len(sign)}"
    )

    print("\n— أيُّ عددٍ للاستثناء يُغلِق الحساب؟")
    closed: list[int] = []
    for astray in (105, 102):
        shown = sum(two for _, _, two in sign)
        covered = sum(one for _, one, _ in sign)
        fits = shown == astray and covered == total
        print(
            f"    استثناء={astray}: خانتا «النفي» تحملان {shown}"
            f" على {covered} موضعًا | أيُغلِق؟ {fits}"
        )
        if fits:
            closed.append(astray)
    if len(closed) != 1:
        raise SystemExit(f"لا عددَ واحدًا يُغلِق: {closed}")
    astray = closed[0]
    print(f"  ⇒ العددُ الذي يُغلِق وحدَه: {astray}")
    print("  والعددُ الآخرُ المعروضُ في الإيداع لا يُغلِق — ويُسمّى ولا يُخمَّن")

    flat = binary(astray / total)
    print(f"\n— H(الوظيفة) = {flat:.6f} بت")

    print("\n— إعادةُ اشتقاق المعلومات: خامًا وبتصحيح ميلر–مادو")
    published = {"م١": 0.0079, "م٢": 0.0378}
    rebuilt: dict[str, tuple[float, float, int]] = {}
    for name, cells in (("م١", sign), ("م٢", near)):
        rows = [(one, two) for _, one, two in cells]
        seen = sum(one for one, _ in rows)
        if seen < total:  # بقيّةٌ غيرُ منشورةٍ تُحمَل خانةً واحدة
            rows.append((total - seen, astray - sum(two for _, two in rows)))
        raw = flat - conditional(rows)
        fixed = raw - miller_madow(len(rows), total)
        rebuilt[name] = (raw, fixed, len(rows))
        print(
            f"    {name}: خاناتٌ {len(rows)} | خامًا {raw:.6f}"
            f" | مُصحَّحًا {fixed:.6f} | المنشور {published[name]:.4f}"
            f" | فرقٌ {abs(fixed - published[name]):.6f}"
        )
    print("  ⇒ والتصحيحُ المستعمَلُ ميلر–مادو، يُشتَقّ ولا يُنقَل")

    print("\n— induction ON: التنقيحُ لا يُنقِص المعلومات — مبرهنةٌ مُصانة")
    rows = [(one, two) for _, one, two in near]
    rows.append(
        (total - sum(one for one, _ in rows), astray - sum(two for _, two in rows))
    )
    names = [one for one, _, _ in near] + ["بقيّة"]
    worst = 0.0
    for size in range(1, len(rows)):
        for chosen in itertools.combinations(range(len(rows)), size):
            block = [sum(one[index] for index in chosen) for one in zip(*rows)]
            other = [
                sum(
                    rows[index][side]
                    for index in range(len(rows))
                    if index not in chosen
                )
                for side in (0, 1)
            ]
            coarse = flat - conditional([(block[0], block[1]), (other[0], other[1])])
            worst = max(worst, coarse - rebuilt["م٢"][0])
    print(f"  أقصى (معلوماتُ قسمةٍ خشنةٍ − معلوماتُ التامّة): {worst:+.6f}")
    print("  فما من تكتيلٍ يزيد على التفصيل — والحدُّ الأدنى للمنشور محفوظ")

    print("\n— التصعيدُ بتّةً بتّة على «حالة التالي»")
    groups = [frozenset(range(len(rows)))]
    here = conditional(rows) if False else flat
    asked_before: list[frozenset[int]] = []
    gains_seen: list[float] = []
    for depth in range(1, len(rows)):
        best: tuple[float, frozenset[int]] | None = None
        for size in range(1, len(rows)):
            for chosen in itertools.combinations(range(len(rows)), size):
                asked = frozenset(chosen)
                if (
                    asked in asked_before
                    or frozenset(range(len(rows))) - asked in asked_before
                ):
                    continue
                fresh: list[frozenset[int]] = []
                for group in groups:
                    for part in (group & asked, group - asked):
                        if part:
                            fresh.append(part)
                after = math.fsum(
                    sum(rows[index][0] for index in part)
                    / total
                    * binary(
                        sum(rows[index][1] for index in part)
                        / sum(rows[index][0] for index in part)
                    )
                    for part in fresh
                )
                if best is None or here - after > best[0]:
                    best = (here - after, asked)
        if best is None or best[0] <= 1e-12:
            print(f"  الوقوف: لا سؤالَ يربح عند الدرجة {depth}")
            break
        gain, asked = best
        groups = [
            part for group in groups for part in (group & asked, group - asked) if part
        ]
        asked_before.append(asked)
        gains_seen.append(gain)
        here -= gain
        label = " و".join(names[index] for index in sorted(asked))
        print(
            f"  د{depth} «أمن {label}؟»: H = {here:.6f}"
            f" | ربحٌ {gain:+.6f} | كتلٌ {len(groups)}"
        )
    print(
        f"  عددُ البتّات المصروفة: {len(asked_before)}"
        f" | والسقفُ الخام ⌈log₂{len(rows)}⌉ = {(len(rows) - 1).bit_length()}"
    )
    spent, ceiling = len(asked_before), (len(rows) - 1).bit_length()
    raw_gain = flat - here
    first = gains_seen[0] if gains_seen else 0.0
    print(f"  نصيبُ البتّة الأولى من الكسب الخام: {first / raw_gain:.6f}")
    print(f"  أأسرف الجشعُ بتّةً؟ {spent > ceiling}" f" — صرف {spent} حيث تكفي {ceiling}")

    print("— ما تبقّى من الحيرة بعد أقوى ملمح")
    left = flat - rebuilt["م٢"][1]
    print(
        f"  H بعد أقوى ملمحٍ مُصحَّحًا: {left:.6f} من {flat:.6f}"
        f" = {left / flat:.4%} باقيةٌ بلا مساس"
    )

    print("\n— induction FOR: ما أعلنه الأنبوبُ عن المحجوز")
    for hits, tries, label in ((270, 341, "بايز"), (269, 341, "الأغلبُ الأعمى")):
        low, high = wilson(hits, tries)
        print(
            f"    {label:14s} {hits}/{tries} = {hits / tries:.4%}"
            f" | ويلسن ٩٥٪ [{low:.4%} , {high:.4%}]"
        )
    low_one, _ = wilson(270, 341)
    _, high_two = wilson(269, 341)
    print(f"  أيتداخل المجالان؟ {low_one <= high_two}")
    print(f"  واستردادُ الاستثناء: 1 من 72 = {1 / 72:.4%}")
    print(f"  فالزيادةُ موضعٌ واحدٌ من {341}: {1 / 341:.4%}")

    print("\n— ما لا يُعاد اشتقاقُه")
    print("  م٣ وم٤ وم٥ بلا تفصيلٍ منشور — فلا تُعاد، ولا تُصدَّق ولا تُكذَّب")
    print("  وجداءُ الملامح غيرُ منشور — فلا يُبنى سلّمٌ عبر ملمحين")
    print("\n— ما لا يُدَّعى")
    print("  لا تشجيرَ في هذه الشجرة: لا يُعاد القياسُ، ويُعاد الحسابُ وحدَه")
    print("  ولا تُوقَّع قراءةُ الكتاب في «إنّما» ولا حكمُ المُشجِّر في «إلّا»")
    print(f"  والمقامُ {total} موضعًا: لا حكمٌ على العربيّة")
    return 0


if __name__ == "__main__":
    sys.exit(main())
