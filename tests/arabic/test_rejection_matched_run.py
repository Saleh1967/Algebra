"""شُغِّل `9fc67498…`: **خمسةٌ من خمسة** — والمقيسُ ليس شيوعًا.

**وما صحّحه هذا الختمُ صحّحه في الآلة لا في القراءة**: و٣ سقط لأنّ
الطبقاتِ لا تُطابِق، فصارت المطابقةُ **شرطَ قَبولٍ على كلّ سحبة**. وثمنُها
سُئل في موضعين — فضلِ التقاطع وعددِ المتمايزة — فمرّا بهامشٍ واسع.

`THE_THROAT_GROUP_IS_STILL_THE_MOST_DISPERSED_AFTER_TWO_MOMENTS_ARE_FIXED`:
مئينُ G1 **٠٫٠٠٨٠** — أي ستَّ عشرةَ سحبةً من ألفين. فبعد ضبط الحجم ومتوسّطِ
رتبة التردّد وانحرافِها، تبقى حروفُ الحلق **أشدَّ تباعدًا في فضاء التعاقب**
من تسعٍ وتسعين من مئةِ مجموعةٍ مطابِقةٍ لها في هذه الثلاثة. فالتفسيرُ
«شيوعٌ لا مخرج» **مردودٌ ههنا**، ولا يُردّ بالدعوى بل بضبطه.

`AND_THE_REMAINDER_GROUP_IS_STILL_THE_MOST_COHERENT`: ومئينُ G5 **٠٫٩٨٤٠**
على ألفٍ وتسعمئةٍ وسبعٍ وتسعين سحبةً متمايزة. فالمجموعةُ التي قيل إنّها
«قفصٌ للعدد» أشدُّ تماسكًا من ثمانٍ وتسعين من مئةِ مجموعةٍ مطابِقة.

`THE_NULL_IS_NOT_AN_ECHO_OF_THE_GROUP_AND_THAT_IS_MEASURED`: وفضلُ التقاطع
**+٠٫٠١٨٣ حرفًا** لـG1 و**+٠٫٥٣٧٨** لـG5، على حظٍّ قدرُه ١٫٢٨٥٧ و٨٫٠٣٥٧.
فالسحبةُ المقبولةُ ليست نسخةً من المجموعة، والقيدُ لم يُقِم المقيسَ مقامَ
المقياس.

`AT_TWO_LETTERS_MATCHING_TWO_MOMENTS_DETERMINES_THE_SET_ITSELF`: وأثمنُ ما
خرج تشخيصٌ **تامٌّ** لسقوط و٣: G3 حرفان، ومجموعةُ ما يُطابقهما في العزمين
**واحدةٌ متمايزة — وهي المجموعةُ نفسُها** (فضلُ تقاطعها ١٣/٧ بالضبط، أي
حرفان إلّا حظَّهما). فعند حرفين لا صفريَّ أصلًا: المطابقةُ تُعيّن المجموعةَ
لا تُشوّشها. وو٣ كان يسأل حرفين أن يُطابَقا، وذلك ممتنعٌ بالحساب لا عسيرٌ
بالسحب.

`TWO_GROUPS_WERE_DECLARED_UNREADABLE_BY_A_RULE_WRITTEN_BEFORE_THE_LOOK`:
وG2 وG3 لم تُملأ حصّتاهما في مئتي ألف محاولة (٦٥٩ و٥١٨ مقبولة)، فخرجتا
**غيرَ مقروءتين** بقاعدة الختم. وخروجُهما حكمٌ سابقٌ لا اعتذارٌ لاحق —
ومئينُ G3 خرج ١٫٠٠٠٠ ولا يُقرأ، إذ مقامُه واحدٌ متمايز.

`AND_THREE_DECISIONS_THE_SEAL_DID_NOT_NAME_ARE_PUBLISHED_HERE`: ولم يُسمِّ
الختمُ: أنّ الانحرافَ **انحرافُ عيّنةٍ** (مقسومًا على `k−1`)، وأنّ المسحوبَ
من **الثمانية والعشرين كلِّها** بلا استثناء حروف المجموعة، وأنّ المقيسَ
**رتبةٌ** لا تردّدًا — فمطابقةُ الرتب ليست مطابقةَ الأعداد. والثالثةُ حدٌّ
معلومٌ يُكتَب ولا يُطوى.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from algebra.attainability import governing_floor, label_permutation_floor
from algebra.signified import Prediction, Verdict

REPOSITORY = Path(__file__).resolve().parents[2]
CORPUS = REPOSITORY / "corpora" / "quran-simple-enhanced.txt"

pytestmark = pytest.mark.skipif(
    not CORPUS.is_file(),
    reason="بايتاتُ المدوّنة المُجمَّدة غيرُ مستقبَلةٍ في هذه الشجرة",
)

REJECTION_SEAL = "9fc6749883423f6751c65a78ccc8959888a63bfcd781bfad77624051bc23e5ee"
FIFTH_SEAL = "5e3656d53a1dceed7a151d1067813087e5b6f14faed6635c51729f8d1e5c4e27"

ALPHABET = 28
DRAWS = 2_000
ATTEMPTS = 200_000

# رتبُ التردّد كما خرجت، من الأشيع لاحقًا
RANKS = "النميوهربتكعفقسدذحجخشصضزثطغظ"


class Group:
    """ما قِيس لمجموعةٍ واحدة — ولا حكمَ في الحقول، الأحكامُ في البنود."""

    def __init__(
        self,
        name: str,
        size: int,
        similarity: Fraction,
        percentile: Fraction,
        accepted: int,
        attempts: int,
        distinct: int,
        excess: Fraction,
    ) -> None:
        self.name = name
        self.size = size
        self.similarity = similarity
        self.percentile = percentile
        self.accepted = accepted
        self.attempts = attempts
        self.distinct = distinct
        self.excess = excess

    @property
    def chance_overlap(self) -> Fraction:
        """تقاطعُ الحظّ وحدَه: `k²/28`."""

        return Fraction(self.size * self.size, ALPHABET)

    @property
    def readable(self) -> bool:
        """مقروءةٌ إن مُلئت حصّتُها في الميزانيّة — بقاعدةٍ سابقةٍ للنظر."""

        return self.accepted >= DRAWS


MEASURED: tuple[Group, ...] = (
    Group(
        "G1 حلق",
        6,
        Fraction(5_792, 10_000),
        Fraction(80, 10_000),
        2_000,
        132_438,
        1_662,
        Fraction(183, 10_000),
    ),
    Group(
        "G2 جاحظيّة",
        4,
        Fraction(6_853, 10_000),
        Fraction(5_250, 10_000),
        659,
        ATTEMPTS,
        68,
        Fraction(705, 10_000),
    ),
    Group(
        "G3 طرفيّة",
        2,
        Fraction(8_561, 10_000),
        Fraction(1),
        518,
        ATTEMPTS,
        1,
        Fraction(18_571, 10_000),
    ),
    Group(
        "G5 الباقي",
        15,
        Fraction(7_482, 10_000),
        Fraction(9_840, 10_000),
        2_000,
        77_364,
        1_997,
        Fraction(5_378, 10_000),
    ),
)

SEALED = (MEASURED[0], MEASURED[3])


def _prediction(identifier: str) -> Prediction:
    path = REPOSITORY / "tests" / "algebra"
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    name = "test_rejection_matched_preregistration"
    spec = importlib.util.spec_from_file_location(name, path / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    assert module.MATCHED_BY_REJECTION_SEAL == REJECTION_SEAL
    for one in module.PREDICTIONS:
        if one.identifier.startswith(identifier):
            found: Prediction = one
            return found
    raise AssertionError(identifier)


def test_all_five_conditions_were_met() -> None:
    """خمسةٌ من خمسة — وكلُّها تسقط بشيء، ولا بندَ إعلانٍ يمرّ مجّانًا."""

    outcomes = {
        "ف١": _prediction("ف١").verdict(max(one.excess for one in SEALED)),
        "ف٢": _prediction("ف٢").verdict(Fraction(min(one.distinct for one in SEALED))),
        "ف٣": _prediction("ف٣").verdict(MEASURED[0].percentile),
        "ف٤": _prediction("ف٤").verdict(MEASURED[3].percentile),
        "ف٥": _prediction("ف٥").verdict(Fraction(min(one.accepted for one in SEALED))),
    }
    assert set(outcomes.values()) == {Verdict.MET}, outcomes


def test_the_two_prices_of_the_constraint_passed_with_room() -> None:
    """ف١ ٠٫٥٣٧٨ دون ١، وف٢ ١٦٦٢ فوق ٢٠٠ — فالقيدُ لم يُفقِر المادّة."""

    assert max(one.excess for one in SEALED) == Fraction(5_378, 10_000)
    assert min(one.distinct for one in SEALED) == 1_662
    # وفضلُ G1 يكاد يكون معدومًا: خُمسا حرفٍ من مئة
    assert MEASURED[0].excess < Fraction(2, 100)


def test_the_throat_group_stays_at_the_bottom_after_matching_two_moments() -> None:
    """٠٫٠٠٨٠ — ستَّ عشرةَ سحبةً من ألفين، ودون ٠٫٠١١ في الصفريّ المُعطَّل."""

    throat = MEASURED[0]
    assert throat.name.startswith("G1")
    assert throat.percentile == Fraction(80, 10_000)
    assert throat.percentile * throat.accepted == 16
    assert throat.percentile <= _prediction("ف٣").threshold


def test_the_remainder_group_stays_at_the_top() -> None:
    """٠٫٩٨٤٠ على ١٬٩٩٧ متمايزة — والقفصُ أشدُّ تماسكًا من مطابِقاته."""

    cage = MEASURED[3]
    assert cage.name.startswith("G5")
    assert cage.percentile >= _prediction("ف٤").threshold
    assert cage.distinct >= cage.accepted - 3  # لا تكرارَ يُذكَر في مقامه


def test_two_letters_leave_no_null_at_all_and_that_explains_the_fifth_seal() -> None:
    """المتمايزةُ واحدةٌ — وهي المجموعةُ نفسُها؛ وفضلُ تقاطعها ١٣/٧ بالضبط."""

    edge = MEASURED[2]
    assert edge.name.startswith("G3") and edge.size == 2
    assert edge.distinct == 1
    # الوحيدةُ هي المجموعةُ نفسُها، فالتقاطعُ حرفان تامّان: الفضلُ ١٣/٧
    exact = Fraction(2) - edge.chance_overlap
    assert exact == Fraction(13, 7)
    assert abs(edge.excess - exact) < Fraction(1, 10_000)  # منقولٌ بأربع خانات
    # ومئينُها واحدٌ صحيحٌ لأنّ المقيسَ يُقارَن بنفسه
    assert edge.percentile == Fraction(1)
    assert not edge.readable
    assert REJECTION_SEAL != FIFTH_SEAL


def test_the_unreadable_groups_are_named_and_counted_not_folded() -> None:
    """G2 وG3 خرجتا بقاعدةٍ مكتوبةٍ قبل النظر، وأعدادُهما منشورة."""

    unreadable = [one for one in MEASURED if not one.readable]
    assert [one.name for one in unreadable] == ["G2 جاحظيّة", "G3 طرفيّة"]
    for one in unreadable:
        assert one.attempts == ATTEMPTS and one.accepted < DRAWS
    for one in SEALED:
        assert one.readable and one.attempts < ATTEMPTS
    # ولا يدخل مئينُ غيرِ المقروءةِ بندًا البتّة
    assert all(one in MEASURED for one in SEALED)
    assert len(SEALED) == 2 and len(unreadable) == 2


def test_the_overlap_bound_would_have_been_impossible_as_a_half() -> None:
    """حظُّ تقاطع G5 ٨٫٠٣٥٧ فوق نصفِ حجمها ٧٫٥ — فحدُّ النصف يسقط بالحساب."""

    cage = MEASURED[3]
    assert cage.chance_overlap == Fraction(225, 28)
    assert cage.chance_overlap > Fraction(cage.size, 2)
    # وحدُّ الختم فضلٌ على الحظّ، فلا يسقط بضربٍ وقسمة
    assert cage.excess < _prediction("ف١").threshold


def test_the_reading_is_not_pinned_at_the_governing_floor() -> None:
    """أرضيّةُ G1 الحاكمةُ ١/٢٠٠١، والمقيسُ ٠٫٠٠٨٠ — ستَّ عشرةَ خطوةً فوقها."""

    throat = MEASURED[0]
    floor = governing_floor(throat.size, ALPHABET, throat.accepted)
    assert floor == Fraction(1, DRAWS + 1)  # التصميمُ هو الحاكم، لا المادّة
    assert label_permutation_floor(throat.size, ALPHABET) == Fraction(1, 376_740)
    assert throat.percentile > floor
    assert throat.percentile / floor > 15


def test_the_rank_table_is_the_one_the_fifth_run_published() -> None:
    """الرتبُ من المدوّنة لا منقولة، وأوّلُها الألفُ — وثمانيةٌ وعشرون."""

    assert len(RANKS) == ALPHABET == len(set(RANKS))
    assert RANKS[0] == "ا"
    assert RANKS[:7] == "النميوه"  # طبقةُ الخامس الأولى نفسُها
    assert set(RANKS) == set("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")


def test_the_acceptance_rates_are_published_with_the_percentiles() -> None:
    """نسبةُ القَبول جزءٌ من الخبر: ١٫٥٪ للحلق و٢٫٦٪ للباقي، و٠٫٣٪ لمن خرج."""

    rates = {one.name: Fraction(one.accepted, one.attempts) for one in MEASURED}
    assert rates["G1 حلق"] < Fraction(2, 100)
    assert rates["G5 الباقي"] < Fraction(3, 100)
    for name in ("G2 جاحظيّة", "G3 طرفيّة"):
        assert rates[name] < Fraction(1, 100)
    # وأضيقُ القيود ليس أصغرَ المجموعات بالضرورة — وG5 أوسعُها قَبولًا
    assert max(rates.values()) == rates["G5 الباقي"]
