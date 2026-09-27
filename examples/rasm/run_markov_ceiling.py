"""سقفُ ي٥ مُشتَقًّا **من السجلّ المُودَع وحدَه** — لا قياسٌ جديد.

**الدَّينُ الذي يسدُّه**: ي٥ كان آخرَ شرطٍ محدودٍ بلا سقفٍ مُصرَّحٍ به
(العطل ٢٦). وإحصاؤه **أقصى ارتفاعٍ في الثمن المحجوز للوحدة صعودًا** —
وهو **فرقٌ بين ثمنين**، لا نسبةٌ يحدُّها الواحد. فسقفُه يحتاج حدًّا على
أعلى ثمنٍ ممكنٍ للوحدة، وذلك يحتاج حدًّا على **أطول شفرةِ هفمان**.

`THE_PRICE_PER_UNIT_HAS_AN_ELEMENTARY_CEILING`: يشحن `spelled` الرمزَ
المشهودَ بطول شفرته، وغيرَ المشهود **هروبًا ثمّ هجاءً**:
`(أطول + ١) + عرضٌ × log₂ ١١٢`. فثمنُ الوحدة لأيّ رمزٍ عرضُه `w`:

    المشهود: طولُه ÷ w ≤ أطول
    غيرُ المشهود: (أطول + ١) ÷ w + log₂ ١١٢

و`w ≥ ١` فأقصاه عند `w = ١`. **فثمنُ الوحدة ≤ أطول + ١ + log₂ ١١٢**،
والارتفاعُ فرقٌ بين ثمنين أدناهما صفر، **فالسقفُ هو أعلى ثمنٍ للوحدة**.

`AND_THE_LONGEST_HUFFMAN_WORD_IS_BOUNDED_BY_THE_ALPHABET`: وشجرةُ هفمان
على `k` رمزًا **عمقُها ≤ k − ١** بالبناء: كلُّ دمجةٍ تُنقِص العُقَدَ
واحدةً، فأعمقُ ما يكون سلسلةٌ من `k − ١` دمجة. **وهذا حدٌّ ابتدائيٌّ لا
يُستورَد**، ويُقرَأ `k` من أبجديّة كلّ مستوًى في السجلّ.

`AND_A_TIGHTER_BOUND_EXISTS_BUT_IS_IMPORTED_SO_IT_IS_NOT_RELIED_UPON`:
ولحدٍّ أحكمَ مبرهنةٌ منقولة (كاتونا–نيمتز ١٩٧٦): `أطول ≤ log_φ(١/أدنى
احتمال)` و`φ` النسبةُ الذهبيّة. وبعدِّ صحيحٍ أدناه واحدٌ من `N` نصفًا،
فتصير `أطول ≤ log_φ(N/٢)`. **ويُحسَب ههنا ويُعلَن، ولا يُبنى عليه
السقفُ المُصرَّح** — فما لا يُبرهَن في هذه الشجرة **يُسمّى منقولًا**.

`AND_THE_LOOSENESS_IS_PRINTED_NOT_HIDDEN`: ويُطبَع الفرقُ بين السقف
والمقيس **عددًا**. فحدٌّ بعيدٌ **يمنع العطلَ ولا يُقرَأ قياسًا**، ومن
كتم بُعدَه قرأه القارئُ تقديرًا.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "markov_ladder_run.log"
UNITS = 112
GOLDEN = (1 + math.sqrt(5)) / 2

ROW = re.compile(
    r"^  (م\d [^|]+?) \| (\d+) \| (\d+) \| [\d.]+ \| [\d.]+ \| ([\d.]+) \| "
    r"[\d.]+ \| [\d.]+ \| [\d.]+ \| ([\d.]+) \|",
    re.M,
)


def rows(text: str) -> list[tuple[str, int, int, float]]:
    """(المستوى، N، الأبجديّة، ثمنُ الوحدة محجوزًا) — من السجلّ لا من حساب."""

    found = ROW.findall(text)
    if not found:
        raise SystemExit("لا صفوفَ في السجلّ — والسقفُ لا يُخمَّن")
    return [
        (name.strip(), int(number), int(alphabet), float(per_unit))
        for name, number, alphabet, _held, per_unit in found
    ]


def climb(text: str) -> float:
    """أقصى ارتفاعٍ للمحجوز صعودًا — المقيسُ المختوم، مقروءًا."""

    found = re.findall(r"أقصى ارتفاعٍ للمحجوز صعودًا: \+([\d.]+)", text)
    if not found:
        raise SystemExit("لا مقيسَ لي٥ في السجلّ")
    return float(found[0])


def elementary(alphabet: int) -> int:
    """عمقُ شجرة هفمان على `k` رمزًا ≤ `k − ١` — بالبناء لا بنقل."""

    return max(alphabet - 1, 0)


def imported(number: int) -> int:
    """حدُّ كاتونا–نيمتز على النصف — **منقولٌ ويُسمّى كذلك**."""

    half = number / 2
    if half <= 1:
        return 0
    return int(math.log(half) / math.log(GOLDEN))


def price_ceiling(longest: int) -> float:
    """أعلى ثمنٍ للوحدة عند `أطول` — و`w = ١` أسوأُ الحالات."""

    return longest + 1 + math.log2(UNITS)


def main() -> int:
    text = LOG.read_text(encoding="utf-8")
    table = rows(text)
    measured = climb(text)

    print("سقفُ ي٥ — مُشتَقٌّ من السجلّ المُودَع، ولا تشغيلَ جديد")
    print(f"المصدر: deposits/{LOG.name}")
    print(f"هجاءُ المرتدّ: log₂ {UNITS} = {math.log2(UNITS):.6f} بتًّا للوحدة")
    print()
    print("المستوى | N | أبجديّة | أطولُ ابتدائيًّا | سقفُ الثمن | أطولُ منقولًا | سقفُه")
    best = 0.0
    tight = 0.0
    for name, number, alphabet, _per_unit in table:
        plain = elementary(alphabet)
        cited = imported(number)
        here = price_ceiling(plain)
        there = price_ceiling(cited)
        best = max(best, here)
        tight = max(tight, there)
        print(
            f"  {name} | {number} | {alphabet} | {plain} | {here:.6f} "
            f"| {cited} | {there:.6f}"
        )
    print()
    print("— الثمنُ للوحدة محجوزًا، مقروءًا من السجلّ")
    for name, _number, _alphabet, per_unit in table:
        print(f"  {name}: {per_unit:.4f}")
    print()
    print("— الحكم")
    print(f"  السقفُ الابتدائيُّ (المُصرَّحُ به): {best:.6f}")
    print(f"  والسقفُ بالمبرهنة المنقولة: {tight:.6f} — **لا يُبنى عليه**")
    print(f"  والمقيسُ المختوم: {measured:.6f}")
    print(f"  فالمقيسُ دون السقف بمعامل: {best / measured:.1f}×")
    print(f"  ودون المنقول بمعامل: {tight / measured:.1f}×")
    print(f"  وحدُّ ي٥ المختوم: 0.001 — ودونه بمعامل {best * 1000:.1f}×")
    print()
    print("— ما لا يُدَّعى")
    print("  السقفُ سليمٌ **غيرُ محكَم**: بُعدُه مطبوعٌ أعلاه ولا يُقرَأ قياسًا.")
    print("  ولم يُحسَب أطولُ شفرةٍ فعلًا — ذلك يحتاج إعادةَ بناء المستويات،")
    print("  **وهو دَينٌ مسمًّى لا سكوت**: يُسدّ بتشغيلٍ لا باشتقاق.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
