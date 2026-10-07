"""اتّفاقُ ممتحِنَين على ج٩: مقياسٌ يَرُدّ خمسةً قبل أن يطبع رقمًا.

**الدعوى المقيسة**: «معدّلُ اتّفاقهما سقفُ أيّ نظام». وهي صائبةٌ **بتقييد**:
الاتّفاقُ يقيس **ثباتَ الوسم** لا حدَّ الدقّة. فنظامٌ يُقاس على ممتحِنٍ واحدٍ
**قد يتجاوز** معدّلَ الاتّفاق — بأن يتعلّم خصوصيّةَ ذلك الممتحِن بعينه. فما
يَحُدُّه الاتّفاقُ هو **ما يُحسَب دون تعيينِ أيِّهما الحَكَم**. ولذلك تُرَدّ
ههنا كلمةُ «سقف» ما لم يُسَمَّ الممتحِنُ الذي قِيس عليه.

`THE_TWO_COVERAGES_DO_NOT_BOUND_THE_INTERSECTION`: ٣٨٬٨٠٥ + ٣٢٬٦١٧ = ٧١٬٤٢٢
وهي **دون** ٧٧٬٤٢٨. فالتقاطعُ في المجال [٠، ٣٢٬٦١٧]، وحدُّه الأدنى **صفر**.
فلا يُشتَقّ مقامُ الاتّفاق من النسبتين؛ يُحسَب بالوصل على المرجع أو لا يُطبَع.

`A_MAPPING_IS_NOT_A_TRANSLATION_OF_NAMES`: والمفردتان مختلفتان لا مترجمتان.
وثلاثُ مقابلاتٍ ظاهرةٍ نسبُها: `subj`/فاعل = ١٫٥٢ · `pred`/خبر = ٠٫٥١ ·
`gen`/مضاف إليه = ٣٫٧٦ — واحدةٌ أكبرُ وواحدةٌ أصغرُ وواحدةٌ قريبةٌ من أربعة.
فلو كان الاختلافُ في الأسماء وحدَها لتقاربت النسبُ من الواحد. فجدولُ المقابلة
**يُعلَن كاملًا**: كلُّ وسمٍ في الطرفين إمّا مقابَلٌ وإمّا مُعلَنٌ بلا مقابل،
والمُعلَنُ بلا مقابلٍ يُعَدّ ويخرج من المقام صراحةً لا صمتًا.

`AN_EDGE_IS_NOT_A_LABEL_ON_A_TOKEN`: والكتابُ يَسِم **رمزًا** بوظيفته، وQAC
يَسِم **حافّةً** بين تابعٍ ومتبوع. وإسقاطُ الحافّة على تابعها يُهمِل المتبوع —
وهو العاملُ بعينه، أي السؤالُ الأصليّ. فالوحدةُ تُعلَن، ومقارنةُ وسمٍ بحافّةٍ
بلا إعلانِ الإسقاط مردودة.

`RAW_AGREEMENT_WITHOUT_CHANCE_IS_NOT_A_READING`: ومفردتان مائلتا الحوافّ
يتّفقان بالصدفة كثيرًا. فيُطبَع الخامُ ومعه كابّا، ونموذجُ الصدفة يُسمّى؛
وطلبُ الخامِ وحدَه يُرَدّ.

`ONE_NUMERATOR_AND_THREE_DENOMINATORS`: و«على المشمول» عبارةٌ تحتمل مقامين لا
مقامًا واحدًا: أن يكون وسمُ الطرفين داخلَ الجردين، أو أن يكون وسمُ **الأوّل**
وحدَه داخلَ جرده. والبسطُ في الثلاثة **واحد**، والمقاماتُ ثلاثةٌ فالنسبُ ثلاث.
ووقع ذلك فعلًا: ٣٬٣٩٥ على ٤٬٢٧٢ و٤٬٩٦٥ و٦٬٦٢٠ يعطي ٧٩٫٤٧٪ و٦٨٫٣٨٪ و٥١٫٢٨٪،
وكابّا +٠٫٧٣٤٥ و+٠٫٦١٠٢ و+٠٫٤٤٢٥ — **وحكمُ تنبّؤٍ مسجَّلٍ انقلب بينها**.
فتُطبَع الثلاثةُ معًا، ويُرَدّ نشرُ واحدٍ وحدَه.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

NO_COUNTERPART = "لا مقابلَ له"
"""وسمٌ مُعلَنٌ بلا مقابلٍ في المفردة الأخرى؛ يُعَدّ ويخرج من المقام صراحةً."""

UNITS: tuple[str, ...] = ("وسمٌ على رمز", "حافّةٌ بين رمزين")
"""وحدتا الوسم المُعلَنتان؛ ولا ثالثةَ تُقبَل بلا إعلان."""

CHANCE_MODELS: tuple[str, ...] = ("كوهين — حوافُّ كلِّ ممتحِنٍ على حدة",)
"""نماذجُ الصدفة المُعلَنة؛ واحدٌ اليوم، ويُزاد بالإعلان لا بالاستعمال."""

DENOMINATOR_POLICIES: tuple[str, ...] = (
    "الجردان معًا",
    "جردُ الأوّل وحدَه",
    "الوصلُ كلُّه والخارجُ خلاف",
)
"""المقاماتُ الثلاثة؛ بسطُها واحدٌ ونسبُها ثلاث، فتُطبَع معًا أو لا تُطبَع."""


class IttifaqError(ValueError):
    """رُفض قياسُ اتّفاقٍ يُخالف شرطًا اتُّفق عليه قبل النظر."""


@dataclass(frozen=True, slots=True)
class Examiner:
    """ممتحِنٌ مُسمًّى: كتابُه، ووحدةُ وسمه، وتغطيتُه معدودةً لا موصوفة."""

    name: str
    unit: str
    covered: int
    corpus: int

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise IttifaqError("ممتحِنٌ بلا اسمٍ لا يُقارَن به.")
        if self.unit not in UNITS:
            raise IttifaqError(
                f"وحدةٌ غيرُ مُعلَنةٍ «{self.unit}»؛ والمُعلَنُ: {'، '.join(UNITS)}."
            )
        if not 0 < self.covered <= self.corpus:
            raise IttifaqError(f"تغطيةُ «{self.name}» خارجَ مدوّنتها.")

    @property
    def coverage(self) -> Fraction:
        return Fraction(self.covered, self.corpus)


def intersection_bounds(one: Examiner, other: Examiner) -> tuple[int, int]:
    """حدّا التقاطع من التغطيتين وحدَهما: [أدنى، أعلى].

    وحدُّه الأدنى `max(0, a + b − n)`. فإن كان صفرًا فالنسبتان **لا تضمنان
    تقاطعًا أصلًا**، ولا يُطبَع منهما مقامُ اتّفاق.
    """

    if one.corpus != other.corpus:
        raise IttifaqError("مدوّنتان مختلفتان لا يُحَدّ تقاطعُهما بهذا الحساب.")
    lower = max(0, one.covered + other.covered - one.corpus)
    return lower, min(one.covered, other.covered)


@dataclass(frozen=True, slots=True)
class Correspondence:
    """جدولُ مقابلةٍ **تامّ**: لا وسمَ في الطرفين يمرّ بلا حكم."""

    left: str
    right: str
    pairs: tuple[tuple[str, str], ...]
    left_labels: tuple[str, ...]
    right_labels: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.pairs:
            raise IttifaqError("جدولُ مقابلةٍ خالٍ ليس جدولًا.")
        named_left = {one for one, _ in self.pairs}
        named_right = {other for _, other in self.pairs if other != NO_COUNTERPART}
        missing_left = set(self.left_labels) - named_left
        missing_right = set(self.right_labels) - named_right - {NO_COUNTERPART}
        unmapped_right = {
            one for one, other in self.pairs if one == NO_COUNTERPART and other
        }
        missing_right -= unmapped_right
        if missing_left or missing_right:
            raise IttifaqError(
                f"وسومٌ لم يُحكَم عليها — من {self.left}: {sorted(missing_left)} · "
                f"من {self.right}: {sorted(missing_right)}. وكلُّ وسمٍ إمّا "
                f"مقابَلٌ وإمّا مُعلَنٌ «{NO_COUNTERPART}»، ولا يمرّ صمتًا."
            )

    @property
    def mapped(self) -> dict[str, str]:
        """المقابلاتُ الفعليّة وحدَها، بلا ما أُعلِن بلا مقابل."""

        return {
            one: other
            for one, other in self.pairs
            if NO_COUNTERPART not in (one, other)
        }

    @property
    def declared_without_counterpart(self) -> tuple[str, ...]:
        return tuple(
            one if other == NO_COUNTERPART else other
            for one, other in self.pairs
            if NO_COUNTERPART in (one, other)
        )

    def agree(self, left_label: str, right_label: str) -> bool:
        """أيتّفق الوسمان بمقتضى الجدول المُعلَن؟"""

        return self.mapped.get(left_label) == right_label


def under(
    rows: tuple[tuple[str, str], ...], table: Correspondence, policy: str
) -> tuple[tuple[str, str], ...]:
    """الصفوفُ الداخلةُ في المقام بمقتضى سياسةٍ **مُسمّاة** من الثلاث."""

    if policy not in DENOMINATOR_POLICIES:
        raise IttifaqError(
            f"مقامٌ غيرُ مُعلَنٍ «{policy}»؛ والمُعلَنُ: " f"{'، '.join(DENOMINATOR_POLICIES)}."
        )
    right_side = set(table.mapped.values())
    if policy == DENOMINATOR_POLICIES[0]:
        return tuple(
            (one, other)
            for one, other in rows
            if one in table.mapped and other in right_side
        )
    if policy == DENOMINATOR_POLICIES[1]:
        return tuple((one, other) for one, other in rows if one in table.mapped)
    return tuple(rows)


def _project(table: Correspondence, label: str) -> str:
    """وسمُ الأوّل مُسقَطًا؛ والخارجُ يبقى مميَّزًا فيُعَدّ خلافًا لا اتّفاقًا."""

    return table.mapped.get(label, f"خارج:{label}")


def raw_agreement(
    rows: tuple[tuple[str, str], ...],
    table: Correspondence,
    policy: str = DENOMINATOR_POLICIES[0],
) -> Fraction:
    """نسبةُ الاتّفاق الخام تحت مقامٍ **مُسمًّى**؛ ولا مقامَ ضمنيّ."""

    scored = under(rows, table, policy)
    if not scored:
        raise IttifaqError("لا صفَّ واحدٌ يقع تحت هذا المقام، فلا نسبة.")
    hits = sum(1 for one, other in scored if _project(table, one) == other)
    return Fraction(hits, len(scored))


def cohen_kappa(
    rows: tuple[tuple[str, str], ...],
    table: Correspondence,
    policy: str = DENOMINATOR_POLICIES[0],
) -> Fraction:
    """كابّا كوهين تحت مقامٍ مُسمًّى، بحوافِّ كلِّ ممتحِنٍ على حدة."""

    scored = under(rows, table, policy)
    total = len(scored)
    if total < 2:
        raise IttifaqError("صفٌّ واحدٌ لا تُحسَب منه صدفة.")
    observed = Fraction(
        sum(1 for one, other in scored if _project(table, one) == other), total
    )
    left = Counter(_project(table, one) for one, _ in scored)
    right = Counter(other for _, other in scored)
    expected = sum(
        Fraction(left[label], total) * Fraction(right[label], total)
        for label in set(left) | set(right)
    )
    if expected == 1:
        raise IttifaqError("صدفةٌ تامّةٌ: لا مجالَ فوقها تُقاس فيه كابّا.")
    return (observed - expected) / (1 - expected)


def three_readings(
    rows: tuple[tuple[str, str], ...], table: Correspondence
) -> dict[str, tuple[int, int, Fraction, Fraction]]:
    """المقاماتُ الثلاثةُ ببسطٍ واحد: (مقام، بسط، خام، كابّا) لكلٍّ.

    والبسطُ واحدٌ **بالبناء**: إصابةٌ تحت مقامٍ أضيقَ إصابةٌ تحت أوسعَ منه.
    فالذي يتغيّر المقامُ وحدَه، والنسبُ تتباعد بعشرين نقطةً فأكثر.
    """

    out: dict[str, tuple[int, int, Fraction, Fraction]] = {}
    for policy in DENOMINATOR_POLICIES:
        scored = under(rows, table, policy)
        hits = sum(1 for one, other in scored if _project(table, one) == other)
        out[policy] = (
            len(scored),
            hits,
            raw_agreement(rows, table, policy),
            cohen_kappa(rows, table, policy),
        )
    return out


def assert_gold_is_named(claim: str, gold: str) -> None:
    """«سقف» كلمةٌ تحتاج حَكَمًا مُسمًّى؛ وبدونه تُرَدّ."""

    if "سقف" in claim and not gold.strip():
        raise IttifaqError(
            "«سقفٌ» بلا تسمية الممتحِن الذي قِيس عليه: الاتّفاقُ يقيس ثباتَ "
            "الوسم، ونظامٌ يتعلّم خصوصيّةَ ممتحِنٍ بعينه قد يتجاوزه. "
            "فيُسمّى الحَكَمُ أو تُحذَف الكلمة."
        )


def report(
    rows: tuple[tuple[str, str], ...],
    table: Correspondence,
    chance_model: str = "",
    gold: str = "",
) -> None:
    """التقرير؛ ويُرَدّ الخامُ وحدَه، وتُرَدّ صدفةٌ غيرُ مُسمّاة."""

    if not chance_model.strip():
        raise IttifaqError(
            "نموذجُ الصدفة يُعلَن بـ`--chance`؛ والخامُ وحدَه لا يُقرَأ في "
            f"مفردتين مائلتَي الحوافّ. والمُعلَنُ: {'، '.join(CHANCE_MODELS)}."
        )
    if chance_model not in CHANCE_MODELS:
        raise IttifaqError(f"نموذجُ صدفةٍ غيرُ مُعلَنٍ «{chance_model}».")

    readings = three_readings(rows, table)
    print(f"المقابلةُ: {table.left} × {table.right}")
    print(
        f"وسومٌ مقابَلة: {len(table.mapped)}  ·  مُعلَنةٌ بلا مقابل: "
        f"{len(table.declared_without_counterpart)}"
    )
    print(f"الوصلُ: {len(rows)}")
    numerators = {hits for _, hits, _, _ in readings.values()}
    if len(numerators) != 1:
        raise IttifaqError("بسطٌ مختلفٌ بين المقامات؛ وذلك عيبٌ في الحساب لا خبر.")
    print(f"البسطُ واحدٌ في الثلاثة: {numerators.pop()}\n")
    for policy, (denominator, _, observed, kappa) in readings.items():
        print(
            f"  {policy:26} مقام {denominator:5} · خام "
            f"{float(observed) * 100:6.2f}٪ · كابّا {float(kappa):+.4f}"
        )
    print(f"\nنموذجُ الصدفة: {chance_model}")
    assert_gold_is_named("هذا سقفٌ", gold)
    print(f"والحَكَمُ المُسمّى: {gold}")


SMOKE_TABLE = Correspondence(
    left="كتابُ إعرابٍ مُصطنَع",
    right="شجرةٌ مُصطنَعة",
    pairs=(
        ("فاعل", "subj"),
        ("مفعول به", "obj"),
        ("مضاف إليه", "gen"),
        ("حال", NO_COUNTERPART),
        (NO_COUNTERPART, "poss"),
    ),
    left_labels=("فاعل", "مفعول به", "مضاف إليه", "حال"),
    right_labels=("subj", "obj", "gen", "poss"),
)

SMOKE_ROWS: tuple[tuple[str, str], ...] = (
    ("فاعل", "subj"),
    ("فاعل", "subj"),
    ("فاعل", "obj"),
    ("مفعول به", "obj"),
    ("مفعول به", "obj"),
    ("مضاف إليه", "gen"),
    ("مضاف إليه", "subj"),
    ("مفعول به", "subj"),
    ("حال", "subj"),  # وسمُ الأوّل خارجَ جرده
    ("فاعل", "poss"),  # وسمُ الثاني خارجَ جرده
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="قياسُ اتّفاق ممتحِنَين")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--chance", default="")
    parser.add_argument("--gold", default="")
    args = parser.parse_args(argv)

    if not args.smoke:
        parser.error("لا بياناتِ ممتحِنَين في الصندوق؛ و`--smoke` يفحص الآلة.")
    print("=" * 64)
    print("عيّنةٌ **مُصطنَعة**: تُثبِت أنّ الآلةَ تعمل، ولا تقول شيئًا عن العربيّة.")
    print("=" * 64)
    report(
        SMOKE_ROWS,
        SMOKE_TABLE,
        chance_model=args.chance or CHANCE_MODELS[0],
        gold=args.gold or "كتابُ إعرابٍ مُصطنَع",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
