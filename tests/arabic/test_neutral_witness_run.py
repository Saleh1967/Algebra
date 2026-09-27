"""شُغِّل شاهدُ الوسط: **الصفرُ الشرطيُّ سقط، والألفُ غلب و∅ معدودٌ معه**.

**ما جرى**: قياسٌ سابقٌ أعلن «صفرًا شرطيًّا» و«الألفُ ظلُّه الأعظم»،
وأرقامُه أُعيد اشتقاقُها ههنا فتكرّرت حرفًا — ثمّ سقط إجراؤه بثلاثة أعطال:
إطارٌ يُقام بقلع أوّل حرف، و∅ غائبٌ عن عدّه وهو مُدَّعاه، وصفرٌ يُرشَّح
بشرطٍ يمنع عدّادَه. وهذا التشغيلُ يرفع الثلاثةَ ويُعيد السؤالَ قابلًا للسقوط.

`THE_FRAME_IS_RAISED_BY_ATTESTED_ALTERNATION_NOT_BY_STRIPPING`: فالأجوفُ
يُعرَف بأنّه يُرى **بوجهَين** في البايتات نفسِها: ممدودًا (`قَالَ`) ومقصورًا
يليه ضميرُ رفع (`قُلْنَا`). والجامدُ لا يقصُر — فـ`شَيْء` لا يدخل إطارَ
`شَاءَ`، ويسقط بالبناء لا باستثناءٍ يُكتَب. و**١٨ إطارًا** بقيت من ٣١٥
ممدودًا، وهي أُطُرُ الأجوف كما تعرفها الصناعة: قال · تاب · عاد · خاف ·
زاد · مات · كاد · دام · قام · زال.

`THE_DELETION_IS_COUNTED_OR_THE_CLAIM_IS_NOT_TESTED`: و∅ صار شاهدًا رابعًا
بموضعه: **١٠٦ سطحًا** من ١٬٣٦٠. فدعوى «المحايدُ هو الحذف» صارت تُقاس؛
ونتيجتُها أنّ الحذفَ **رابعُ الشواهد لا أوّلُها**، والألفُ **١٬١٠٣** أي
٠٫٨١١٠ — وهو غالبٌ على ∅ نفسِه بعشرةِ أضعاف.

`A_ZERO_THAT_CAN_FALL_IS_THE_ONLY_ZERO_WORTH_ANNOUNCING`: والترشيحُ لا يذكر
المتطفّلَ بحرف — شرطُه المناوبةُ وحدَها — ثمّ يُمسَح وسطُ الإطار على
المدوّنة كلِّها. **فسقط الصفرُ الشرطيّ: ٢٠٧ متطفّلًا (٠٫١٣٢١)، كلُّها
نونٌ ساكنة** (`عِندَ` · `تُنبِتُ` · `مُنتَظِرُونَ`). فالإطارُ **لا يسترجع
المحذوفَ وحدَه**، والدعوى الأولى تسقط بعدّادٍ كان يملك ألّا يسقط.

`AND_A_CEILING_THAT_IS_ASSUMED_INFLATES_THE_COMPRESSION_UNDER_IT`: والسقفُ
يُقاس ولا يُفترَض: `H(وسطٌ مرصود) = 1.6839` لا `log₂28 = 4.8074`. فالضغطُ
**٠٫٥٧٨٧** لا ٠٫٣٠ — والموضعُ يحمل أكثرَ من نصف حمولته، لا ثلثَها.

**وجردُ ختم `c46dfbe3…`: أربعةٌ مرّت وثلاثةٌ سقطت** — ش١ وش٢ وش٤ وش٧ مرّت،
وسقطت ش٣ (دعوى الحذف) وش٥ (الصفر الشرطيّ) وش٦ (ضغطُ ٠٫٣٠). والساقطاتُ
**حدودُها منقولةٌ من دعوى القياس السابق**، فليست عتباتٍ فُصِّلت لتسقط.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from frozen_corpus import CORPUS, requires_corpus
from test_neutral_witness_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Prediction, Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_neutral_witness.py"

pytestmark = requires_corpus

TOKENS = 78_245
FRAMES = 18
HELD = 1_360
ALIF = 1_103
YA = 113
ZERO = 106
WAW = 38
INTRUDERS = 207
BORROWED = 4
EXTENDED = 315
LEAD_SHARE = 0.8110
STRAY_SHARE = 0.1321
SHADOW = 0.9744
ROOF = 1.6839
SQUEEZE = 0.5787


def _one(identifier: str) -> Prediction:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _module() -> Any:
    spec = importlib.util.spec_from_file_location("run_neutral_witness", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _measured() -> (
    tuple[Any, list[str], set[tuple[str, str]], Counter[str], Counter[str]]
):
    reader = _module()
    tokens = reader.read_tokens(CORPUS)
    witnessed, frames = reader.alternating(tokens)
    census = reader.middle_census(tokens, frames)
    witness: Counter[str] = Counter()
    intruder: Counter[str] = Counter()
    for frame in frames:
        witness[reader.DELETION] += witnessed[frame][reader.DELETION]
        for letter, count in census[frame].items():
            if letter in reader.WEAK:
                witness[letter] += count
            else:
                intruder[letter] += count
    return reader, tokens, frames, witness, intruder


def test_the_seal_is_rederived_before_any_verdict_is_read() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد الحكم."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("c46dfbe3")
    assert "37633090" in ORACLE.source


def test_the_run_reproduces_the_recorded_counts() -> None:
    """السجلُّ يُعاد اشتقاقُه من الشيفرة لا يُنقَل."""

    reader, tokens, frames, witness, intruder = _measured()
    assert len(tokens) == TOKENS
    assert len(frames) == FRAMES
    assert sum(witness.values()) == HELD
    assert witness["ا"] == ALIF
    assert witness["ي"] == YA
    assert witness[reader.DELETION] == ZERO
    assert witness["و"] == WAW
    assert sum(intruder.values()) == INTRUDERS


def test_the_frame_is_raised_by_alternation_and_admits_no_frozen_noun() -> None:
    """المناوبةُ هي الوسمُ: جامدٌ لا يقصُر فلا يدخل — و«شيء» خارجٌ بالبناء."""

    reader, tokens, frames, _, _ = _measured()
    extended = {
        reading[0]
        for reading in (reader.extended_frame(one) for one in tokens)
        if reading is not None
    }
    assert len(extended) == EXTENDED
    assert _one("ش١").verdict(Fraction(len(frames))) is Verdict.MET
    assert _one("ش٢").verdict(Fraction(int(("ش", "ء") in frames))) is Verdict.MET
    assert reader.shortened_frame("شَيْءٍ") is None
    assert reader.shortened_frame("قُلْنَا") == ("ق", "ل")
    assert reader.extended_frame("قَالُوا") == (("ق", "ل"), "ا")
    assert ("ش", "ء") not in frames  # خلطُ «شاءَ/شيء» لا يقوم ههنا
    assert {("ق", "ل"), ("ت", "ب"), ("خ", "ف"), ("م", "ت")} <= frames
    for first, last in frames:
        assert first not in reader.HAMZA and last not in reader.HAMZA


def test_the_deletion_is_counted_and_is_not_the_greatest_shadow() -> None:
    """∅ شاهدٌ رابعٌ معدودٌ — ودعوى «المحايدُ هو الحذف» تُقاس فتُردّ."""

    reader, _, _, witness, _ = _measured()
    assert set(witness) == set(reader.WITNESSES)  # و∅ منها، فالدعوى مفحوصة
    assert witness[reader.DELETION] > 0  # قِيسَ ولم يُغفَل
    held = sum(witness.values())
    leader, lead = witness.most_common(1)[0]
    assert leader == "ا"
    assert witness["ا"] > 10 * witness[reader.DELETION]
    assert abs(lead / held - LEAD_SHARE) < 5e-5
    assert _one("ش٤").verdict(Fraction(lead, held)) is Verdict.MET
    fallen = _one("ش٣")
    assert fallen.verdict(Fraction(witness[reader.DELETION], held)) is Verdict.FALSIFIED
    assert "الحذفُ ليس أعظمَ الظلال" in fallen.falsifies


def test_the_conditional_zero_could_fall_and_it_did() -> None:
    """الترشيحُ لا يذكر المتطفّل — فسقط الصفرُ بـ٢٠٧ نونًا مرصودة."""

    reader, tokens, frames, witness, intruder = _measured()
    assert sum(intruder.values()) == INTRUDERS
    assert set(intruder) == {"ن"}  # ونونُ `عِندَ` و`تُنبِتُ` تُسمّى ولا تُكنَس
    total = sum(witness.values()) + sum(intruder.values())
    assert Fraction(sum(intruder.values()), total) > Fraction(13, 100)
    assert "ن" not in reader.WEAK and reader.DELETION not in reader.WEAK
    census = reader.middle_census(tokens, frames)
    strayed = {
        frame for frame in frames if set(census[frame]) - reader.WEAK
    }  # وأُطُرٌ بعينها تطفّلت، فالسقوطُ مسنودٌ إلى إطارٍ مسمًّى
    assert ("ع", "د") in strayed  # `عِندَ` — والإطارُ لم يسترجع محذوفَه
    strayed_share = sum(intruder.values()) / total
    assert abs(strayed_share - STRAY_SHARE) < 5e-5
    fallen = _one("ش٥")
    assert fallen.verdict(_exact(strayed_share)) is Verdict.FALSIFIED
    assert "مشتقًّا من المُرشِّح لا من البايتات" in fallen.falsifies


def test_the_ceiling_is_measured_and_the_compression_is_not_inflated() -> None:
    """السقفُ مرصودٌ لا مفترَض: `log₂28` سعةٌ، والمقيسُ أدنى منها."""

    reader, tokens, _, witness, _ = _measured()
    ceiling = reader.measured_ceiling(tokens)
    roof = reader.entropy(ceiling)
    shadow = reader.entropy(witness)
    assert roof < 2.0  # ودون `log2(28) = 4.8074` بكثير
    assert abs(roof - ROOF) < 5e-5
    assert abs(shadow - SHADOW) < 5e-5
    assert abs(shadow / roof - SQUEEZE) < 5e-5
    fallen = _one("ش٦")
    assert fallen.verdict(_exact(shadow / roof)) is Verdict.FALSIFIED
    assert "السقفُ المنفوخُ يصنع ضغطًا" in fallen.falsifies
    assert reader.entropy(Counter()) == 0.0


def test_the_proclitic_limit_is_measured_and_not_hidden() -> None:
    """حدُّ التشغيل معدودٌ: ٤ أُطُرٍ لا مقصورَ لها إلّا بقلع سابقة."""

    reader, tokens, frames, _, _ = _measured()
    borrowed = reader.proclitic_only(tokens, frames)
    assert len(borrowed) == BORROWED
    assert ("م", "ع") in borrowed  # `سَمِعْنَا` سليمٌ يُقرأ مقصورًا إن قُلِعت السين
    assert ("ق", "ل") not in borrowed  # و`قُلْنَا` قائمةٌ بلا سابقة
    assert borrowed < frames
    assert _one("ش٧").verdict(Fraction(len(borrowed), len(frames))) is Verdict.MET


def test_four_stood_and_three_fell_and_each_is_named() -> None:
    """الجردُ صريحٌ، ولا يُعاد تفسيرُ شرطٍ بعد رقمه."""

    met = {"ش١", "ش٢", "ش٤", "ش٧"}
    fell = {"ش٣", "ش٥", "ش٦"}
    assert met | fell == {one.identifier for one in PREDICTIONS}
    assert not met & fell


REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ **مرّت** وتعليلُها المكتوبُ معها **لم يُؤيَّد بالقياس** — إن وُجِدت.

وههنا فارغٌ: ش١ وش٢ وش٧ أعدادٌ مرصودةٌ لا تعليلَ معها، وش٤ غلبةٌ معدودةٌ
بموضعها. والسؤالُ مسؤولٌ في كلّ مرّةٍ ولا يُطوى بالسكوت.
"""
