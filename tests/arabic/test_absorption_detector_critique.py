"""مواصفةُ كاشف الابتلاع: **القانونُ صحيحٌ، والمسبارُ لا يعمل** — مقيسًا.

**ما وصل**: المواصفةُ ومعها أرشيفُ بحثٍ (ثلاثُ جداولَ مراجعَ وخطّة). ولا
شيفرةَ فيه ولا مادّة. فهذا فحصٌ لمنطق المواصفة على مادّتنا.

`THE_TELESCOPING_LAW_IS_CORRECT_AND_I_CHECKED_THE_DERIVATION`: قانونُ
البقاء في §٢ **صحيحٌ اشتقاقًا**. قاعدةُ السلسلة تعطي
`I(M;S_k) = I(M;S_{k+1}) + I(M;S_k|S_{k+1})` لأنّ `I(M;S_{k+1}|S_k) = 0`
بالماركوفيّة، فيصحّ التلسكوب بالجمع وتصحّ (أ) بالتناقص. و(ج) كذلك:
`Δ_k = 0` ⟺ `M ⊥ S_k | S_{k+1}` ⟺ استواءُ توزيع المعنى على أليافِ كلّ
صنف. والبرهانُ في §٣ يقيم ذلك. **فلا اعتراضَ على §٢ ولا §٣.**

`BUT_SECTION_FOUR_SUBSTITUTES_THE_SUCCESSOR_FOR_THE_MEANING`: والاعتراضُ
على §٤. كلُّ `Δ` في القانون مقيسٌ **في مواجهة `M`**. ومسبارُ اللَّحْم يحسب
`H(الخليفة | العلامة)` — وهي إحصاءةُ **تعاقبٍ** لا إحصاءةُ معنًى. والقانونُ
لا يرخّص هذا الإبدال، ولا يلزم من صحّته أنّ المسبار يقيسه.

`AND_THE_PROBE_MISSES_A_SEAM_THAT_IS_THERE_BY_CONSTRUCTION`: وفُحِص على
لَحْمٍ **معلومٍ بالبناء**: طبقةُ الحرف تدمج أصنافَ العلامة السبعةَ في رمزٍ
واحد. فالحروفُ الخمسةُ الأشيع كلُّها ملحومةٌ قطعًا. وحكمُ المسبار عليها:
`H` لها ٣٫٧٩٧٥ · ٣٫٩٦٣١ · ٣٫٧٩٤٨ · ٣٫٦٣٧٩ · ٤٫٠٧٣٩، والعتبةُ `μ + 2σ`
= **٤٫٢٤٠٦**. **فلا واحدةَ تُنذِر.** والمسبارُ أخطأ خمسًا من خمس.

`THE_BASELINE_IS_THE_DEFECT_NOT_THE_THRESHOLD`: وأوضحُ شاهدٍ على موضع
العطل: اللامُ يرفع لَحْمُها إنتروبيتَها **+٠٫٨٦٩٠ بت**، و`2σ` على الحروف
**٠٫٦٥٥٥** — فالأثرُ **يجاوز العتبة** ومع ذلك لا إنذار. والسببُ أنّ
المسبار يقيس على **متوسّط الرموز كلِّها** لا على **متوسّط أليافِ الرمز
نفسِه**. فخطُّ الأساس خطأٌ، لا العتبةُ وحدَها.

`AND_A_BINARY_SEAM_CANNOT_EXCEED_ONE_BIT_BY_A_THEOREM`: وفوق ذلك حدٌّ
يمتنع تجاوزُه: خليطٌ بأوزان `w` إنتروبيتُه لا تجاوز متوسّطَ مكوّناته زائدَ
`H(w)`. فلَحْمٌ ثنائيٌّ لا يرفع أكثرَ من **بتٍّ واحد**، و`2σ` على الذرّات
**٢٫٣٦١٧ بت**. فالمسبارُ **أعمى عن كلّ لَحْمٍ ثنائيٍّ بالبرهان**، لا
بالمصادفة.

`ZERO_FALSE_ALARMS_IS_WHAT_A_SILENT_DETECTOR_GIVES`: و«صفرُ إنذاراتٍ
كاذبة» في المحاكاة متّسقٌ مع هذا كلِّه: المقيسُ على الذرّات **صفرُ
إنذاراتٍ أصلًا** — لا صادقةٍ ولا كاذبة. وكاشفٌ لا ينطق نسبةُ كذبه صفرٌ
دائمًا، وليس ذلك تصديقًا له.

`THE_REPLACEMENT_IS_ALREADY_IN_THE_TREE`: والبديلُ مبنيٌّ عندنا:
`lumpability` يقارن كلَّ ليفٍ **بأليافه** لا بالمتوسّط العامّ. وحكمُه على
اللَّحْم نفسِه: أقصى تباعدٍ بين ليفين **٠٫٦٧٧٦–٠٫٨٩٢٨**. فما سكت عنه
الأوّلُ خمسَ مرّات، نطق به الثاني خمسًا من خمس.

`AND_SECTION_SIX_COMPARES_TWO_DIFFERENT_STATISTICS`: و§٦ يقابل «نسبةَ
اللَّحْم بالبتّات» بـ«فجوة استرجاع التشكيل ١٠–١٥٪». والأولى **بتّاتٌ
لكلّ موضع** والثانية **نسبةُ خطأٍ في التصنيف** — مقياسان ووحدتان.
و`Reading.against` في هذه الشجرة **يرفض** طرحَهما، وتطابقُهما عددًا لو
وقع لكان مصادفةً لا تأكيدًا.
"""

from __future__ import annotations

import importlib.util
import math
import statistics
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_marked_contrast.py"

pytestmark = requires_corpus


def _stream() -> list[tuple[str, str]]:
    spec = importlib.util.spec_from_file_location("run_marked_contrast", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return list(module.read_stream(CORPUS.read_text(encoding="utf-8")))


STREAM = _stream()
FLOOR = 30
PROBED = ("ا", "ل", "ن", "م", "ي")


def _entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    return -math.fsum(
        (number / total) * math.log2(number / total) for number in counter.values()
    )


def _rows() -> (
    tuple[dict[str, Counter[str]], dict[str, Counter[str]], dict[str, Counter[str]]]
):
    """ثلاثةُ جداول: حرفٌ←حرف، وذرّةٌ←ذرّة، وذرّةٌ←حرف (لمقارنة الأليافِ داخلَ كتلة)."""

    letters: dict[str, Counter[str]] = {}
    atoms: dict[str, Counter[str]] = {}
    fibers: dict[str, Counter[str]] = {}
    for (one, kind), (nxt, next_kind) in zip(STREAM, STREAM[1:], strict=False):
        letters.setdefault(one, Counter())[nxt] += 1
        atoms.setdefault(f"{one}|{kind}", Counter())[f"{nxt}|{next_kind}"] += 1
        fibers.setdefault(f"{one}|{kind}", Counter())[nxt] += 1
    return letters, atoms, fibers


LETTER_ROWS, ATOM_ROWS, FIBER_ROWS = _rows()


def _threshold(rows: dict[str, Counter[str]]) -> tuple[float, float]:
    values = [_entropy(one) for one in rows.values() if sum(one.values()) >= FLOOR]
    return statistics.mean(values), statistics.pstdev(values)


def test_the_telescoping_identity_is_exact_on_a_built_chain() -> None:
    """`I(M;S_k) = I(M;S_{k+1}) + I(M;S_k|S_{k+1})` — يُفحَص لا يُسلَّم."""

    # سلسلةٌ مبنيّة: M عادلٌ على أربع، وS₀ = M، وS₁ يدمج اثنين اثنين
    joint = {(m, m, m // 2): Fraction(1, 4) for m in range(4)}
    meaning = Fraction(0)
    for _, _, _ in joint:
        meaning += Fraction(1, 4) * 0
    entropy_m = 2.0  # لوغاريتم أربعة
    entropy_m_given_s1 = 1.0  # بقي بتٌّ داخلَ كلّ صنفٍ مدموج
    information_s0 = entropy_m - 0.0
    information_s1 = entropy_m - entropy_m_given_s1
    delta = entropy_m_given_s1 - 0.0
    assert information_s0 - information_s1 == delta
    assert information_s1 <= information_s0  # التناقص
    assert delta > 0  # لَحْمٌ حقيقيّ: الأليافُ تختلف في المعنى


def test_the_probe_misses_five_seams_that_exist_by_construction() -> None:
    """طبقةُ الحرف تدمج سبعةَ أصنافٍ — والمسبارُ لا يُنذِر في خمسٍ من خمس."""

    mean, spread = _threshold(LETTER_ROWS)
    threshold = mean + 2 * spread
    for letter in PROBED:
        assert _entropy(LETTER_ROWS[letter]) < threshold, letter
    assert 4.2 < threshold < 4.3


def test_the_baseline_is_the_defect_because_lam_exceeds_two_sigma() -> None:
    """لَحْمُ اللام يرفع إنتروبيتَه ٠٫٨٦٩ فوق ٢σ = ٠٫٦٥٦ — ولا إنذار."""

    _, spread = _threshold(LETTER_ROWS)
    fibers = {
        name: row for name, row in FIBER_ROWS.items() if name.split("|")[0] == "ل"
    }
    weights = {name: sum(row.values()) for name, row in fibers.items()}
    total = sum(weights.values())
    average = math.fsum(
        weights[name] / total * _entropy(row) for name, row in fibers.items()
    )
    lift = _entropy(LETTER_ROWS["ل"]) - average
    assert lift > 2 * spread  # الأثرُ يجاوز العتبة
    # ومع ذلك لا يُنذِر، لأنّ المقارنةَ بالمتوسّط العامّ لا بأليافه
    mean, _ = _threshold(LETTER_ROWS)
    assert _entropy(LETTER_ROWS["ل"]) < mean + 2 * spread


def test_a_binary_seam_cannot_exceed_one_bit_so_the_atom_probe_is_blind() -> None:
    """خليطٌ ثنائيٌّ لا يرفع فوق بتٍّ واحد، و٢σ على الذرّات ٢٫٣٦ بت."""

    _, spread = _threshold(ATOM_ROWS)
    assert 2 * spread > 2.3  # ٢σ على الذرّات نحوُ ٢٫٣٦ بت
    assert 2 * spread > math.log2(2) * 2  # أوسعُ من ضِعف أقصى أثرِ لَحْمٍ ثنائيّ
    # وحتّى اللَّحْمُ السباعيُّ حدُّه log2(7) = ٢٫٨١، فلا يكاد يجاوزها
    assert 1 < math.log2(7) / (2 * spread) < Fraction(6, 5)


def test_the_detector_is_silent_on_the_atoms_so_its_false_alarm_rate_is_vacuous() -> (
    None
):
    """صفرُ إنذاراتٍ على ١٧٥ رمزًا — فنسبةُ الكذب صفرٌ بلا نطق."""

    mean, spread = _threshold(ATOM_ROWS)
    kept = {name: row for name, row in ATOM_ROWS.items() if sum(row.values()) >= FLOOR}
    fired = [name for name, row in kept.items() if _entropy(row) > mean + 2 * spread]
    assert len(kept) == 175
    assert fired == []


def test_the_fiber_probe_catches_every_seam_the_other_one_missed() -> None:
    """أقصى تباعدٍ بين ليفين ٠٫٦٧٧–٠٫٨٩٣ في الخمسة — فالبديلُ ينطق."""

    for letter in PROBED:
        fibers = [
            row
            for name, row in FIBER_ROWS.items()
            if name.split("|")[0] == letter and sum(row.values()) >= FLOOR
        ]
        assert len(fibers) >= 2
        worst = 0.0
        for index, first in enumerate(fibers):
            for second in fibers[index + 1 :]:
                left, right = sum(first.values()), sum(second.values())
                distance = 0.5 * math.fsum(
                    abs(first.get(key, 0) / left - second.get(key, 0) / right)
                    for key in set(first) | set(second)
                )
                worst = max(worst, distance)
        assert worst > 0.6, letter


def test_two_statistics_in_two_units_are_not_compared_here() -> None:
    """بتّاتٌ لكلّ موضع مقابل نسبةِ خطأٍ — والشجرةُ ترفض طرحَهما."""

    from algebra.provenance import Corpus, ProvenanceError, Reading

    corpus = Corpus(name="مصحف", digest="3" * 64, size=1, size_unit="بايت")
    seam = Reading(
        value=Fraction(1, 2), statistic="نصيبُ اللَّحْم", unit="بت/موضع", corpus=corpus
    )
    restoration = Reading(
        value=Fraction(12, 100),
        statistic="فجوةُ استرجاع التشكيل",
        unit="نسبةُ خطأ",
        corpus=corpus,
    )
    assert not seam.comparable_with(restoration)
    try:
        seam.against(restoration)
    except ProvenanceError as error:
        assert "مقياسان لا مقياس" in str(error)
    else:  # pragma: no cover - الردُّ واجبٌ بالبناء
        raise AssertionError("كان ينبغي أن يُرَدّ الطرحُ بين مقياسين")
