"""شُغِّلت لامُ الناقص: **∅ غلب ههنا، لكنّ ثلثَ إطارِه قام على التباس**.

**وهذا الختمُ سبق آلتَه حقًّا**: دُفِع `6aca9ee4…` في `8c31a53` الساعةَ
٢٢:٠٠، وأوّلُ سطرٍ من آلته في `74ee0d0` الساعةَ ٢٢:٠٢ — دقيقتان يشهد بهما
تاريخُ الدفع لا قولي. فما يلي حكمٌ على شروطٍ لم تُفصَّل على مقاسِ مخرَجها.

`THE_DELETION_DOES_WIN_HERE_AND_THAT_IS_THE_OPPOSITE_OF_THE_HOLLOW`: ففي
الأجوف سقطت دعوى «المحايدُ هو الحذف» — الألفُ ٠٫٨١١٠ و∅ رابعُ الشواهد.
وفي الناقص **تقوم الدعوى نفسُها**: ∅ **٣٤** من ٥١ أي ٠٫٦٦٦٧، والألفُ ١٧.
فالدعوى **ليست صوابًا مطلقًا ولا خطأً مطلقًا، بل تابعةٌ لموضع الاعتلال** —
وهذا ما لا يُقال إلّا بعد أن يُقاس البابان بآلةٍ واحدة.

`A_COUNTER_THAT_FELL_ON_MARKS_WAS_FALLING_ON_A_CATEGORY_ERROR`: وأوّلُ
تشغيلٍ لهذه الآلة أعلن ثمانيةَ متطفّلين، فلمّا سُمّوا بأعيانهم كما يوجب
ق٥ كانوا **فتحةَ `كَسَبَ` وتنوينَ `كَبَدٍ`** — أي **حركاتٍ لا حروفًا**.
والحركةُ علامةٌ على الحرف قبلها لا شاغلٌ للموضع بعده، فكان السقوطُ **خطأ
فئةٍ في المحارف لا خبرًا في اللغة**. فحُصِر موضعُ اللام في كتلة الحروف،
**ولم يُذكَر حرفُ علّةٍ في شرطه** — فبقي قادرًا على السقوط، وصار **صفرًا
حقيقيًّا: ٠ من ٥١**. وهذا هو الفرقُ بين تنظيفِ عدّادٍ وتدجينِه.

`BUT_THE_PRE_REGISTERED_LIMIT_CAUGHT_WHAT_THE_MAJORITY_HID`: وق٧ — وهو
شرطٌ كُتِب قبل أن يُرى رقمٌ واحد — **سقط: ٢ من ٦ أي ٠٫٣٣٣٣ فوق حدّ الربع**.
والإطاران اللذان أسقطاه هما بعينهما الإطاران الزائفان: `(س·ب)` قائمٌ كلُّه
على `كَسَبَتْ` و`كَسَبَا` — و`كَسَبَ` فعلٌ **سالم** قُلِعت كافُه سابقةً،
وألفُ `كَسَبَا` ضميرُ تثنيةٍ لا لام. و`(س·ع)` يجمع `سَعَى` إلى `وَسِعَتْ`
وهما **مادّتان لا مادّة**. فالحدُّ المُعلَن سلفًا أمسك العطلَ الذي كانت
الأغلبيّةُ تخفيه.

`AND_STRIPPING_THE_AMBIGUOUS_DROPS_THE_CORPUS_BELOW_ITS_OWN_DOOR`: فإذا
طُرِح الملتبسان بقي **٤ أُطُرٍ و٢٨ سطحًا** — و∅ باقٍ غالبًا (١٧ مقابل ١١)
لكنّ الأُطُرَ **دون عتبة ق١ نفسِها (٥)**. فالنتيجةُ الصحيحةُ أنّ هذه
المدوّنةَ **لا تحمل إطارَ الناقص حملًا نظيفًا**: إمّا ستّةٌ ثلثُها ملتبس،
وإمّا أربعةٌ نظيفةٌ دون بابِ الدخول. والدعوى تبقى **مفتوحةً موصوفةً**.

**وق٦ مرّت ولا يُقرأ مرورُها جوابًا**: الموادُّ ٦ دون التعادل ١٨٣، والختمُ
نفسُه كتب قبل العدّ أنّ عدمَ المجاوزة **يُبقي السؤالَ مفتوحًا** لأنّ
المقيسَ حدٌّ أدنى والمدوّنةُ ليست اللغة. فهي في `REASONING_NOT_SUPPORTED`.

**وجردُ ختم `6aca9ee4…`: ستٌّ مرّت وواحدةٌ سقطت** — ق١ وق٢ وق٣ وق٤ وق٥
وق٦ مرّت، وسقطت ق٧ (حدُّ التشغيل المُعلَن).
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from frozen_corpus import CORPUS, requires_corpus
from test_naqis_witness_seal import BREAK_EVEN, DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Prediction, Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_naqis_witness.py"

pytestmark = requires_corpus

TOKENS = 78_245
FRAMES = 6
HELD = 51
ZERO = 34
ALIF = 17
WAW = 0
INTRUDERS = 0
PARTICLES_IN = 0
BORROWED = 2
BARE_FRAMES = 4
BARE_HELD = 28
BARE_ZERO = 17
BARE_ALIF = 11
LEAD_SHARE = 0.6667
BORROWED_SHARE = 0.3333
SHADOW = 0.9183
ROOF = 1.0235
SQUEEZE = 0.8972
RAW_MAQSURA = 896
RAW_ALIF = 1_097

REASONING_NOT_SUPPORTED = ("ق٦",)
"""ق٦ مرّت — ٦ موادَّ دون ١٨٣ — و**تعليلُها غيرُ مؤيَّد**: الختمُ أعلن قبل
العدّ أنّ عدمَ المجاوزة لا يُقرأ جوابًا، لأنّ المقيسَ حدٌّ أدنى لموادّ
اللغة لا جردٌ لها. فمرورُها لا يشتري القانونَ جدولَه، والسؤالُ مفتوح."""


def _one(identifier: str) -> Prediction:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _module() -> Any:
    spec = importlib.util.spec_from_file_location("run_naqis_witness", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _split(
    reader: Any,
    witnessed: dict[tuple[str, str], Counter[str]],
    census: dict[tuple[str, str], Counter[str]],
    frames: set[tuple[str, str]],
) -> tuple[Counter[str], Counter[str]]:
    """شواهدُ الأُطُر ومتطفّلوها مفروزَين بفضاءٍ مُعلَنٍ قبل العدّ."""

    witness: Counter[str] = Counter()
    intruder: Counter[str] = Counter()
    for frame in frames:
        witness[reader.DELETION] += witnessed[frame][reader.DELETION]
        for letter, count in census[frame].items():
            if letter in reader.WITNESSES:
                witness[letter] += count
            else:
                intruder[letter] += count
    return witness, intruder


def _measured() -> tuple[Any, list[str], set[tuple[str, str]], Counter[str], Any]:
    reader = _module()
    tokens = reader.read_tokens(CORPUS)
    witnessed, frames, raw = reader.alternating(tokens)
    census = reader.lam_census(tokens, frames)
    witness, intruder = _split(reader, witnessed, census, frames)
    return reader, tokens, frames, raw, (witness, intruder, witnessed, census)


def test_the_seal_is_rederived_and_it_predates_its_own_machine() -> None:
    """البصمةُ تُشتَقّ ثانيةً، والبوّابةُ تُقِرّ بسبقها ويشهد التاريخ."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("6aca9ee4")
    assert "37633090" in ORACLE.source
    assert len(PREDICTIONS) == 7


def test_the_run_reproduces_the_recorded_counts() -> None:
    """السجلُّ يُعاد اشتقاقُه من الشيفرة لا يُنقَل."""

    reader, tokens, frames, raw, (witness, intruder, _, _) = _measured()
    assert len(tokens) == TOKENS
    assert len(frames) == FRAMES
    assert sum(witness.values()) == HELD
    assert witness[reader.DELETION] == ZERO
    assert witness["ا"] == ALIF
    assert witness["و"] == WAW
    assert sum(intruder.values()) == INTRUDERS
    assert raw[reader.MAQSURA] == RAW_MAQSURA  # الخامُ مطبوعٌ فالقرارُ مكشوف
    assert raw["ا"] == RAW_ALIF


def test_the_deletion_wins_here_unlike_the_hollow_and_the_particles_stay_out() -> None:
    """∅ غالبٌ في الناقص — والدعوى تابعةٌ لموضع الاعتلال لا مطلقة."""

    reader, _, frames, _, (witness, _, _, _) = _measured()
    leader, lead = witness.most_common(1)[0]
    assert leader == reader.DELETION  # وفي الأجوف كان الألف — فالبابان يفترقان
    assert abs(lead / HELD - LEAD_SHARE) < 5e-5
    assert _one("ق٣").verdict(Fraction(witness[reader.DELETION])) is Verdict.MET
    assert _one("ق٤").verdict(Fraction(witness["ا"] - witness["و"])) is Verdict.MET
    admitted = reader.particles_admitted(frames)
    assert admitted == []  # `عَلَى` و`إِلَى` لم تجدا إطارًا، فالمناوبةُ فصلت
    assert _one("ق٢").verdict(Fraction(len(admitted))) is Verdict.MET
    assert _one("ق١").verdict(Fraction(len(frames))) is Verdict.MET


def test_the_conditional_zero_holds_on_a_counter_that_names_no_weak_letter() -> None:
    """صفرٌ حقيقيّ: العدّادُ لا يذكر العلّة، ولو وقع حرفٌ لَسُمّي."""

    reader, _, _, _, (witness, intruder, _, _) = _measured()
    assert sum(intruder.values()) == INTRUDERS and dict(intruder) == {}
    slot = reader.LAM_PLACE.pattern.rsplit("(", 1)[-1]
    assert slot.endswith(")$") and "?!" not in slot  # لا استثناءَ في الموضع
    for sound in "نبتمدلسك":
        assert reader.LAM_PLACE.match(f"بَد{sound}") is not None  # كان يَقبَلُه
    assert all(one not in reader.WITNESSES for one in "نبتمدلسك")
    assert reader.LAM_PLACE.match("كَسَبَ") is None  # والحركةُ لم تعد تُعَدّ حرفًا
    assert reader.LAM_PLACE.match("كَبَدٍ") is None
    assert reader.LAM_PLACE.match("بَدَا") is not None  # والحرفُ ما زال يُلتقَط
    total = sum(witness.values()) + sum(intruder.values())
    assert _one("ق٥").verdict(Fraction(sum(intruder.values()), total)) is Verdict.MET


def test_the_declared_limit_fell_and_it_named_the_two_false_frames() -> None:
    """ق٧ سقط: ٢ من ٦ — وهما الإطاران الزائفان بعينهما."""

    reader, tokens, frames, _, _ = _measured()
    borrowed = reader.proclitic_only(tokens, frames)
    assert len(borrowed) == BORROWED
    assert borrowed == {("س", "ب"), ("س", "ع")}
    share = Fraction(len(borrowed), len(frames))
    assert abs(float(share) - BORROWED_SHARE) < 5e-5
    fallen = _one("ق٧")
    assert fallen.verdict(share) is Verdict.FALSIFIED
    assert "مبنيٌّ على التباسٍ لا على مناوبة" in fallen.falsifies
    assert reader.BARE_DROPPED.match("كَسَبَتْ") is None  # لا يقوم إلّا بقلعِ الكاف
    assert reader.BARE_DROPPED.match("بَدَتْ") is not None  # وهذا يقوم بلا قلع


def test_stripping_the_ambiguous_drops_the_frame_below_its_own_threshold() -> None:
    """أربعةٌ نظيفةٌ دون عتبة ق١ — فالمدوّنةُ لا تحمل الإطارَ نظيفًا."""

    reader, tokens, frames, _, (_, _, witnessed, _) = _measured()
    bare = frames - reader.proclitic_only(tokens, frames)
    assert len(bare) == BARE_FRAMES
    witness, intruder = _split(reader, witnessed, reader.lam_census(tokens, bare), bare)
    assert sum(witness.values()) == BARE_HELD
    assert witness[reader.DELETION] == BARE_ZERO and witness["ا"] == BARE_ALIF
    assert sum(intruder.values()) == 0  # والصفرُ يصمد بعد الطرح أيضًا
    thin = _one("ق١")
    assert thin.verdict(Fraction(len(bare))) is Verdict.FALSIFIED
    assert "فلا فصلَ بهذا الطريق" in thin.falsifies


def test_the_break_even_is_not_reached_and_that_answers_nothing() -> None:
    """٦ موادَّ دون ١٨٣ — ومرورُ ق٦ مُعلَنٌ أنّه لا يُقرأ جوابًا."""

    _, _, frames, _, _ = _measured()
    assert len(frames) == FRAMES and FRAMES < BREAK_EVEN
    assert _one("ق٦").verdict(Fraction(len(frames))) is Verdict.MET
    assert "ق٦" in REASONING_NOT_SUPPORTED  # مرّت وتعليلُها غيرُ مؤيَّد
    assert __doc__ is not None
    assert "لا يُقرأ مرورُها جوابًا" in __doc__


def test_the_ceiling_is_measured_and_the_compression_is_almost_none() -> None:
    """السقفُ مرصودٌ لا مفترَض — والموضعُ يحمل قريبًا من كلّ حمولته."""

    reader, tokens, _, _, (witness, _, _, _) = _measured()
    roof = reader.entropy(reader.measured_ceiling(tokens))
    shadow = reader.entropy(witness)
    assert abs(roof - ROOF) < 5e-5 and abs(shadow - SHADOW) < 5e-5
    assert abs(shadow / roof - SQUEEZE) < 5e-5
    assert shadow / roof > 0.85  # ولا شبهَ بـ٠٫٣٠ المدّعاة في القياس السابق


def test_every_sealed_condition_is_judged_and_the_tally_is_six_to_one() -> None:
    """لا شرطَ يُترَك بلا حكم، والجردُ مطبوعٌ في الشرح."""

    reader, tokens, frames, _, (witness, intruder, witnessed, census) = _measured()
    bare = frames - reader.proclitic_only(tokens, frames)
    total = sum(witness.values()) + sum(intruder.values())
    verdicts = {
        "ق١": _one("ق١").verdict(Fraction(len(frames))),
        "ق٢": _one("ق٢").verdict(Fraction(len(reader.particles_admitted(frames)))),
        "ق٣": _one("ق٣").verdict(Fraction(witness[reader.DELETION])),
        "ق٤": _one("ق٤").verdict(Fraction(witness["ا"] - witness["و"])),
        "ق٥": _one("ق٥").verdict(Fraction(sum(intruder.values()), total)),
        "ق٦": _one("ق٦").verdict(Fraction(len(frames))),
        "ق٧": _one("ق٧").verdict(
            Fraction(len(reader.proclitic_only(tokens, frames)), len(frames))
        ),
    }
    assert set(verdicts) == {one.identifier for one in PREDICTIONS}
    assert [one for one, two in verdicts.items() if two is Verdict.FALSIFIED] == ["ق٧"]
    assert sum(two is Verdict.MET for two in verdicts.values()) == 6
    assert len(bare) < len(frames)
    assert set(census) <= set(witnessed) | set(census)
