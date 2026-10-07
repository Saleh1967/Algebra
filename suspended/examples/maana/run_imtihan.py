"""مُشغِّلُ امتحان المعنى: ثلاثةُ شروطٍ مبنيّةٌ لا موعودٌ بها.

**لماذا مُشغِّلٌ لا نتيجة**: كتابُ الغريب ليس في هذه الجلسة، ولا مخرَجُ
النظام. فما يُبنى ههنا **الآلةُ** التي تُجري الامتحانَ متى وصلت المدخلات،
وتُجريه بحيث **يتعذّر** إغفالُ ما اتُّفق عليه قبل التشغيل:

  ١. **القسمةُ باللِّمّة لا بالموضع.** `assert_split_is_by_lemma` يرُدّ أيَّ
     قسمةٍ تضع لِمّةً في القسمين — وهو شرطُ تشغيلٍ لا تنبيهٌ في هامش.
  ٢. **التصنيفُ بعدد الشروح.** `report` لا يطبع رقمًا مجمَّعًا إلّا ومعه
     شرائحُ `k`؛ وطلبُ المجمَّع وحدَه يُرَدّ.
  ٣. **المعنويّةُ على اللِّمَم.** المجالُ يُحسَب من متوسّطات اللِّمَم لا من
     المواضع، فلا يُضاعَف اليقينُ بعنقودٍ لم يُحسَب.

وشرطٌ رابعٌ من جنسها: **حكمٌ على الاحتمالين لا يُطبَع من تمثيلٍ واحد**.
فـ«تمثيلُ السياق خاطئ» و«المعنى مدخولٌ من خارج» يفسّران معًا أيَّ رقمٍ
منخفض، والفاصلُ ميلٌ عبر تمثيلاتٍ متدرّجة. فإن لم يُعطَ إلّا تمثيلٌ واحدٌ
طُبِعت الأرقامُ وامتنع الحكم.

**المدخلات**:

    --glosses  gloss_id ⭾ lemma ⭾ text
    --runs     representation ⭾ ref ⭾ lemma ⭾ gold_gloss_id ⭾ ranked_ids

و`ranked_ids` مفصولةٌ بفواصل، أعلاها رتبةً أوّلُها. والمقياسُ **تداخلُ
الكلمات الدالّة** (جاكار بعد إسقاط قائمةِ وقفٍ مُعلَنة) لا المطابقةُ الحرفيّة.
"""

from __future__ import annotations

import argparse
import math
import statistics
import unicodedata
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

STOPWORDS: frozenset[str] = frozenset(
    {
        "في",
        "من",
        "على",
        "عن",
        "إلى",
        "هو",
        "هي",
        "ما",
        "لا",
        "أن",
        "إن",
        "و",
        "أو",
        "التي",
        "الذي",
        "به",
        "له",
        "بها",
        "لها",
        "أي",
        "أيْ",
        "ذلك",
        "هذا",
        "هذه",
        "كان",
        "قد",
        "ثم",
        "بل",
        "كل",
        "بعض",
    }
)
"""قائمةُ وقفٍ مُعلَنةٌ صغيرة؛ وتغييرُها يُغيّر الأرقامَ فيُعلَن معها."""


class ImtihanError(ValueError):
    """رُفض تشغيلٌ يُخالف شرطًا اتُّفق عليه قبل النظر."""


@dataclass(frozen=True, slots=True)
class Authority:
    """الجهةُ الواسمة: كتابٌ مُسمًّى، يُقارَن بمُعلِن الدعوى ولا يُفترَض استقلالُه.

    القانونُ مأخوذٌ من شجرة الغانم بنصّه: **شهادةُ ورودِ اللفظ ليست شهادةَ صحّةِ
    تفسيره**. فحلُّ موضعٍ في مصدرٍ مُبصَّمٍ يُثبِت الوقوعَ وحدَه، ولا يُثبِت
    جنسَه ولا محمولَه ولا مضمونَ إفادته؛ وذلك وسمٌ يحتاج **جهةً تُسمّى**.
    وفصلُ الملفّ عن الشفرة لا يصنع استقلالًا؛ إنّما يجعله مكتوبًا يُقارَن.
    فيُكتَب مُعلِنُ الدعوى ههنا لتقع المقارنة، ولا يُطوى.
    """

    authority_id: str
    authority_note: str
    declarer_id: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.authority_id, "اسمُ الجهة الواسمة"),
            (self.authority_note, "بيانُ الجهة"),
            (self.declarer_id, "مُعلِنُ الدعوى"),
        ):
            if not value.strip():
                raise ImtihanError(f"{name} يُكتَب؛ وبدونه لا تقع المقارنة.")
        if self.authority_id.strip() == self.declarer_id.strip():
            raise ImtihanError(
                f"«{self.authority_id}» واسمٌ ومُعلِنٌ معًا — ووسمٌ يكتبه صاحبُ "
                "الدعوى على دعواه مردودٌ بالبناء، وفصلُ الملفّ لا يُغني."
            )


def _exact(first: str, second: str) -> Fraction:
    """تطابقٌ تامٌّ بعد التسوية: واحدٌ أو صفرٌ، ولا ثالث."""

    left = unicodedata.normalize("NFC", first.strip())
    right = unicodedata.normalize("NFC", second.strip())
    return Fraction(1) if left == right and left else Fraction(0)


@dataclass(frozen=True, slots=True)
class Trial:
    """موضعُ اختبارٍ واحد: لِمّتُه، وجوابُه، وترتيبُ النظام."""

    representation: str
    ref: str
    lemma: str
    gold: str
    ranked: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.ranked:
            raise ImtihanError(f"{self.ref}: ترتيبٌ خالٍ ليس ترتيبًا.")
        if self.gold not in self.ranked:
            raise ImtihanError(
                f"{self.ref}: الجوابُ الصحيحُ ليس في المرشَّحين — "
                "فالموضعُ غيرُ قابلٍ للحلّ ولا يُحتسَب صامتًا."
            )


def content_words(text: str) -> frozenset[str]:
    """كلماتُ النصّ الدالّة بعد إسقاط قائمة الوقف المُعلَنة."""

    return frozenset(one for one in text.split() if one and one not in STOPWORDS)


def overlap(first: str, second: str) -> Fraction:
    """جاكار على الكلمات الدالّة؛ ونصّان خاليان تداخلُهما صفرٌ لا واحد."""

    left, right = content_words(first), content_words(second)
    if not (left | right):
        return Fraction(0)
    return Fraction(len(left & right), len(left | right))


MATCH_POLICIES: dict[str, Callable[[str, str], Fraction]] = {
    "تطابقٌ_تامّ": _exact,
    "تداخلُ_جاكار": lambda first, second: overlap(first, second),
}
"""سياساتُ المقابلة المُعلَنة؛ ومقابلةٌ غيرُ مُسمّاةٍ اختيارٌ يقع بلا إعلان."""


def assert_match_policy_is_declared(name: str) -> Callable[[str, str], Fraction]:
    """سياسةُ المقابلة تُعلَن؛ والتطابقُ التامُّ وجاكار يُعطيان حكمين مختلفين.

    وهذا هو الموضعُ الذي تركته شجرةُ الغانم غيرَ مُعدَّد: بوّابتُها الثالثة
    تقابل مضمونَ الوسم بمضمون الحالة **تطابقًا حرفيًّا بعد التسوية**، ولا
    تُسمّي ذلك اختيارًا. فجهةٌ مستقلّةٌ تكتب نثرَها لا تطابقه حرفًا بحرف،
    فلا تُجاز إلّا أن يُنقَل عنها نصًّا — وحينئذٍ يقيس الفحصُ النقلَ لا الموافقة.
    """

    if not name.strip():
        raise ImtihanError(
            "سياسةُ المقابلة تُعلَن بـ`--match`؛ والتطابقُ التامُّ وجاكار "
            f"حكمان لا حكمٌ واحد. والمُعلَنُ منها: {'، '.join(MATCH_POLICIES)}."
        )
    if name not in MATCH_POLICIES:
        raise ImtihanError(
            f"سياسةٌ غيرُ مُعلَنةٍ «{name}»؛ والمُعلَنُ: {'، '.join(MATCH_POLICIES)}."
        )
    return MATCH_POLICIES[name]


def read_glosses(path: Path) -> dict[str, tuple[str, str]]:
    table: dict[str, tuple[str, str]] = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 3:
            raise ImtihanError(
                f"شروحٌ، السطرُ {number}: {len(fields)} عمودًا والمُعلَنُ ثلاثة."
            )
        table[fields[0]] = (fields[1], fields[2])
    if not table:
        raise ImtihanError("جدولُ شروحٍ خالٍ لا يُمتحَن به.")
    return table


def read_runs(path: Path) -> list[Trial]:
    trials: list[Trial] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 5:
            raise ImtihanError(
                f"تشغيلٌ، السطرُ {number}: {len(fields)} عمودًا والمُعلَنُ خمسة."
            )
        representation, ref, lemma, gold, ranked = fields
        trials.append(
            Trial(
                representation=representation.strip(),
                ref=ref.strip(),
                lemma=lemma.strip(),
                gold=gold.strip(),
                ranked=tuple(one for one in ranked.split(",") if one),
            )
        )
    if not trials:
        raise ImtihanError("تشغيلٌ خالٍ لا يُقاس.")
    return trials


def assert_split_is_by_lemma(train: frozenset[str], test: frozenset[str]) -> None:
    """يُرَدّ أيُّ اشتراكٍ في لِمّة؛ فجردُ شروحها مشترَكٌ والقسمةُ تُسرِّبه."""

    shared = train & test
    if shared:
        shown = "، ".join(sorted(shared)[:4])
        raise ImtihanError(
            f"{len(shared)} لِمّةً في القسمين ({shown}…) — والقسمةُ باللِّمّة "
            "لا بالموضع، وإلّا تسرّب جردُ الشروح."
        )
    if not train or not test:
        raise ImtihanError("قسمةٌ أحدُ طرفيها خالٍ ليست قسمة.")


def gloss_count(glosses: dict[str, tuple[str, str]]) -> dict[str, int]:
    """عددُ شروح كلّ لِمّة — وهو محورُ التصنيف `k`."""

    counts: dict[str, int] = defaultdict(int)
    for lemma, _ in glosses.values():
        counts[lemma] += 1
    return dict(counts)


def score(
    trial: Trial,
    glosses: dict[str, tuple[str, str]],
    match: Callable[[str, str], Fraction],
) -> Fraction:
    """مقابلةُ أعلى المرشَّحين رتبةً بالجواب الصحيح، بالسياسة المُعلَنة."""

    top = trial.ranked[0]
    if top not in glosses or trial.gold not in glosses:
        raise ImtihanError(f"{trial.ref}: شرحٌ غيرُ موجودٍ في الجدول.")
    return match(glosses[top][1], glosses[trial.gold][1])


def by_lemma(
    trials: list[Trial],
    glosses: dict[str, tuple[str, str]],
    match: Callable[[str, str], Fraction],
) -> dict[str, float]:
    """متوسّطُ كلّ لِمّةٍ — وهو وحدةُ المعنويّة، لا الموضع."""

    buckets: dict[str, list[float]] = defaultdict(list)
    for trial in trials:
        buckets[trial.lemma].append(float(score(trial, glosses, match)))
    return {lemma: statistics.fmean(values) for lemma, values in buckets.items()}


def clustered_interval(means: dict[str, float]) -> tuple[float, float]:
    """مجالُ ٩٥٪ من متوسّطات اللِّمَم — فلا يُضاعَف اليقينُ بعنقودٍ مُهمَل."""

    values = list(means.values())
    if len(values) < 2:
        raise ImtihanError("لِمّةٌ واحدةٌ لا يُحسَب منها مجال.")
    centre = statistics.fmean(values)
    spread = statistics.stdev(values) / math.sqrt(len(values))
    return centre, 1.96 * spread


BANDS = ((2, 2), (3, 4), (5, 9), (10, 19), (20, 10**9))


def band_of(count: int) -> str:
    for low, high in BANDS:
        if low <= count <= high:
            return (
                f"k={low}"
                if low == high
                else f"k={low}–{high if high < 10**9 else '∞'}"
            )
    raise ImtihanError(f"عددُ شروحٍ خارجَ النطاقات: {count}")


def assert_order_is_declared(
    order: tuple[str, ...], present: frozenset[str]
) -> tuple[str, ...]:
    """ترتيبُ التمثيلات من الأفقر إلى الأغنى **يُعلَن**، ولا يُستنتَج من الاسم.

    وقد أخرج الفرزُ الأبجديُّ ميلًا **سالبًا** لبيانٍ ميلُه موجب، لأنّ
    «+نافذة» تسبق «الطبقات» في الترتيب لا في الغنى. فالغنى ليس خاصّةً في
    الاسم، ومن استنتجه منه قرأ عكسَ ما في البيانات.
    """

    if not order:
        raise ImtihanError(
            "ترتيبُ التمثيلات من الأفقر إلى الأغنى يُعلَن بـ`--order`؛ "
            "والفرزُ بالاسم يقلب الميلَ ولا يُنبِّه."
        )
    named, seen = set(order), set()
    for one in order:
        if one in seen:
            raise ImtihanError(f"«{one}» مذكورٌ مرّتين في الترتيب.")
        seen.add(one)
    if named != set(present):
        missing = sorted(set(present) - named)
        extra = sorted(named - set(present))
        raise ImtihanError(
            f"الترتيبُ لا يطابق التمثيلات — ناقصٌ {missing} · زائدٌ {extra}."
        )
    return order


def report(
    trials: list[Trial],
    glosses: dict[str, tuple[str, str]],
    order: tuple[str, ...] = (),
    pooled_only: bool = False,
    authority: Authority | None = None,
    match: str = "",
) -> None:
    """التقرير؛ ويُرَدّ طلبُ المجمَّع وحدَه لأنّ الصفريَّ يتغيّر عشرةَ أضعافٍ بـk."""

    if pooled_only:
        raise ImtihanError(
            "المجمَّعُ وحدَه يُخفي صفريًّا يتغيّر من ٠٫٥٠ إلى ٠٫٠٥ بعدد الشروح؛ "
            "فلا يُطبَع بلا شرائحِ k."
        )
    if authority is None:
        raise ImtihanError(
            "جدولُ شروحٍ بلا جهةٍ واسمةٍ مُسمّاةٍ لا يُقرَأ سندًا: يُكتَب الكتابُ "
            "ومُعلِنُ الدعوى معًا، فإنّ المقارنةَ بينهما هي الشرط."
        )
    scorer = assert_match_policy_is_declared(match)
    counts = gloss_count(glosses)
    grouped: dict[str, list[Trial]] = defaultdict(list)
    for trial in trials:
        grouped[trial.representation].append(trial)

    print(f"الجهةُ الواسمة: {authority.authority_id} — {authority.authority_note}")
    print(f"مُعلِنُ الدعوى: {authority.declarer_id}  ·  سياسةُ المقابلة: {match}")
    print(f"التمثيلات: {len(grouped)}  ·  المواضع: {len(trials)}")
    print(f"اللِّمَم: {len({trial.lemma for trial in trials})}\n")

    sequence = assert_order_is_declared(order, frozenset(grouped))
    curve: dict[str, float] = {}
    for representation in sequence:
        rows = grouped[representation]
        means = by_lemma(rows, glosses, scorer)
        centre, half = clustered_interval(means)
        curve[representation] = centre
        print(f"■ {representation}")
        print(f"   الكلّيّ (على اللِّمَم): {centre * 100:6.2f}٪  ±{half * 100:.2f}")
        bands: dict[str, list[Trial]] = defaultdict(list)
        for trial in rows:
            bands[band_of(counts[trial.lemma])].append(trial)
        for name in sorted(bands, key=lambda key: len(bands[key]), reverse=True):
            slice_ = bands[name]
            lemmas = {trial.lemma for trial in slice_}
            value = statistics.fmean(
                float(score(trial, glosses, scorer)) for trial in slice_
            )
            null = statistics.fmean(1 / counts[trial.lemma] for trial in slice_)
            print(
                f"   {name:<9} مواضعُ {len(slice_):>4} · لِمَمٌ {len(lemmas):>3} · "
                f"مقيسٌ {value * 100:6.2f}٪ · صفريٌّ {null * 100:6.2f}٪"
            )
        print()

    if len(curve) < 2:
        print("⚠ تمثيلٌ واحدٌ: الأرقامُ تُطبَع والحكمُ **يمتنع**.")
        print("  «تمثيلٌ خاطئ» و«معنًى من خارج» يفسّران معًا أيَّ رقمٍ منخفض،")
        print("  والفاصلُ ميلٌ عبر تمثيلاتٍ متدرّجة — لا نقطةٌ واحدة.")
        return
    ordered = [curve[key] for key in sequence]
    rise = ordered[-1] - ordered[0]
    print(f"الميلُ عبر {len(ordered)} تمثيلاتٍ: {rise * 100:+.2f} نقطة")
    print("  موجبٌ معنويٌّ ⇒ التمثيلُ كان ناقصًا · استواءٌ دون السقف ⇒ المعنى مدخول")
    print("  والحدُّ الفاصلُ يُقرَأ من التسجيل، ولا يُختار ههنا.")


SMOKE_GLOSSES = """\
g1\tوليّ\tالناصر المعين
g2\tوليّ\tالقريب في النسب
g3\tوليّ\tالمتولي للأمر
g4\tبيّنة\tالحجة الواضحة
g5\tبيّنة\tالحجة الظاهرة
g6\tأسرى\tسير الليل
g7\tأسرى\tالمشي ليلا
g8\tكتاب\tالتوراة
g9\tكتاب\tالصحيفة المكتوبة
g10\tكتاب\tالفرض والحكم
g11\tكتاب\tالأجل المضروب
"""

SMOKE_RUNS = """\
# تمثيلٌ فقيرٌ ثمّ أغنى — عيّنةٌ مُصطنَعةٌ لفحص الآلة وحدَها
الطبقات\t2:107\tوليّ\tg1\tg2,g1,g3
الطبقات\t4:45\tوليّ\tg1\tg3,g1,g2
الطبقات\t6:14\tوليّ\tg3\tg3,g1,g2
الطبقات\t2:211\tبيّنة\tg4\tg5,g4
الطبقات\t2:87\tبيّنة\tg4\tg4,g5
الطبقات\t17:1\tأسرى\tg6\tg7,g6
الطبقات\t2:53\tكتاب\tg8\tg9,g8,g10,g11
الطبقات\t3:145\tكتاب\tg11\tg10,g11,g9,g8
+نافذة\t2:107\tوليّ\tg1\tg1,g2,g3
+نافذة\t4:45\tوليّ\tg1\tg1,g3,g2
+نافذة\t6:14\tوليّ\tg3\tg3,g1,g2
+نافذة\t2:211\tبيّنة\tg4\tg4,g5
+نافذة\t2:87\tبيّنة\tg4\tg4,g5
+نافذة\t17:1\tأسرى\tg6\tg6,g7
+نافذة\t2:53\tكتاب\tg8\tg9,g8,g10,g11
+نافذة\t3:145\tكتاب\tg11\tg11,g10,g9,g8
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="مُشغِّلُ امتحان المعنى")
    parser.add_argument("--glosses", type=Path)
    parser.add_argument("--runs", type=Path)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument(
        "--order",
        default="",
        help="التمثيلاتُ من الأفقر إلى الأغنى، مفصولةً بفواصل — تُعلَن ولا تُستنتَج",
    )
    parser.add_argument(
        "--authority",
        default="",
        help="اسمُ الجهة الواسمة، ثمّ بيانُها، ثمّ مُعلِنُ الدعوى — مفصولةً بـ`|`",
    )
    parser.add_argument(
        "--match",
        default="",
        help=f"سياسةُ المقابلة المُعلَنة: {'، '.join(MATCH_POLICIES)}",
    )
    parser.add_argument(
        "--pooled-only",
        action="store_true",
        help="يُرَدّ: المجمَّعُ بلا شرائحِ k يُخفي صفريًّا متغيّرًا",
    )
    args = parser.parse_args(argv)

    if args.smoke:
        glosses = read_glosses_text(SMOKE_GLOSSES)
        trials = read_runs_text(SMOKE_RUNS)
        print("=" * 64)
        print("عيّنةٌ **مُصطنَعة**: تُثبِت أنّ الآلةَ تعمل، ولا تقول شيئًا عن العربيّة.")
        print("=" * 64)
        if not args.order:
            args.order = "الطبقات,+نافذة"
        if not args.authority:
            args.authority = "جهةٌ_مُصطنَعة|عيّنةُ فحصٍ للآلة|مُعلِنٌ_مُصطنَع"
        if not args.match:
            args.match = "تداخلُ_جاكار"
    elif args.glosses and args.runs:
        glosses = read_glosses(args.glosses)
        trials = read_runs(args.runs)
    else:
        parser.error("إمّا `--glosses` و`--runs` وإمّا `--smoke`.")

    lemmas = sorted({trial.lemma for trial in trials})
    half = len(lemmas) // 2
    assert_split_is_by_lemma(frozenset(lemmas[:half]), frozenset(lemmas[half:]))
    named = tuple(one.strip() for one in args.authority.split("|"))
    if len(named) != 3:
        parser.error(
            "`--authority` ثلاثةُ حقولٍ مفصولةٍ بـ`|`: الكتابُ، وبيانُه، " "ومُعلِنُ الدعوى."
        )
    report(
        trials,
        glosses,
        order=tuple(one for one in args.order.split(",") if one),
        pooled_only=args.pooled_only,
        authority=Authority(
            authority_id=named[0], authority_note=named[1], declarer_id=named[2]
        ),
        match=args.match,
    )
    return 0


def read_glosses_text(text: str) -> dict[str, tuple[str, str]]:
    table: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        gloss_id, lemma, body = line.split("\t")
        table[gloss_id] = (lemma, body)
    return table


def read_runs_text(text: str) -> list[Trial]:
    trials: list[Trial] = []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        representation, ref, lemma, gold, ranked = line.split("\t")
        trials.append(
            Trial(
                representation=representation,
                ref=ref,
                lemma=lemma,
                gold=gold,
                ranked=tuple(ranked.split(",")),
            )
        )
    return trials


if __name__ == "__main__":
    raise SystemExit(main())
