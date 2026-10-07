"""شُغِّل التدقيقُ على المواصفة المُصلَحة: **الساقطُ صفر، والدَّينُ الأوّل يُغلَق بالعدّ**.

**ما جرى**: `run_unit_coverage` عرض المواصفةَ كما وردت فأسقطت ربعَ المواضع.
فأُعلن إصلاحٌ ثلاثيٌّ **قبل التشغيل** — حالةٌ ثامنةٌ «عُرْي» مصنَّفةٌ لا
خالية، وحروفٌ اثنان وثلاثون، وسقفٌ على الفضاء المعلن — **ومعه تنبّؤٌ مكتوب:
الساقطُ صفر**. ثمّ شُغِّل.

`THE_FALLOUT_IS_ZERO_AND_THAT_CLOSES_THE_FIRST_DEBT`: والمقيس: **٠**. لا
موضعَ واحدًا من ٣٥٥٬٨٥٣ وحدةً مُخرَجةً يقع خارج الفضاء المعلن — لا بحرفٍ
ولا بحالة. وعلى قاعدتك أنت: **العدُّ على مجمَّدٍ متناهٍ استدلالٌ تامّ**؛
فالدَّينُ الأوّل (Δرقمي) **مُغلَقٌ برهانًا لا بدعوى** — وهو أوّلُ دَينٍ في
هذه الشجرة يُغلَق بتشغيلِ مواصفةٍ على بايتاتها.

`AND_THE_CEILING_IS_NOW_A_CEILING`: والسقفُ صار حدًّا: **log₂(٢٥٦) = ٨٫٠٠٠٠
بالضبط**، والمرصودُ **٦٫٠٢٠١**، والأبجديّةُ الواقعةُ **٢١٧ من ٢٥٦** فسقفُها
٧٫٧٦١٦ — فالثلاثةُ مرتّبةٌ كما يجب: المقيسُ ≤ سقفُ الواقع ≤ سقفُ المعلن.
وكان المعلنُ قبلَ الإصلاح **بينهما** (٧٫٦١٤٧ فوقَ المقيس وتحتَ سقفِ الواقع)
— وذلك ما جعله ليس سقفًا.

`AND_THE_OPENING_QUESTION_OF_THE_SESSION_HAS_A_NUMBER`: وأثمنُ ما خرج:
**Δضبط = H(حالة | حرف) = ١٫٩٥١٨ بتًّا للموضع** على ٣٣٢٬٨٣٧ موضعَ رسم —
أي **٣١٫٢٪ من إفادة الموضع**، و٦٤٩٬٦٠٠ بتًّا على المدوّنة كلِّها. فالسؤالُ
الذي فُتحت به الجلسة — «ماذا يعطي المشكولُ ممّا يفقده المجرّد؟» — صار له
**رقمٌ مقيسٌ لا تقدير**.

`AND_IT_IS_AN_UPPER_BOUND_DECLARED_AS_SUCH`: وهو **حدٌّ أعلى** لا قيمةً
نهائيّة: الشرطُ على السياق لا يزيد الإنتروبيا، فـH(حالة | حرف، سياق) ≤
H(حالة | حرف). ويُنشَر بهذا القيد لا بدونه. ويُقرَأ على **مواضع الرسم** لا
على الموسَّع، لأنّ المجرّدَ لا شدّةَ فيه فلا توسيعَ له — والمقارنةُ على
مواضعَ واحدة.

`AND_THE_REPAIR_IS_MINE_NOT_THE_DEPOSITS`: **والإصلاحُ من عندي**: الحالةُ
الثامنةُ والحروفُ الثلاثةُ لم تَرِدا في `algebraic_recovery_proof.md`،
فتُنسَبان إلى هذا الملفّ لا إلى الإيداع. والمُودَعُ كما ورد **يُسقِط ربعَ
المواضع**، وذلك مقيسٌ في `test_recovery_proof_audit` ويبقى كما هو.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_encoding_audit.py"

pytestmark = requires_corpus

EMITTED = 355_853
RASM_POSITIONS = 332_837
SPACE = 256
OBSERVED_PAIRS = 217
PREDICTED_FALLOUT = 0
"""كُتِب قبل التشغيل، ولم يُعدَّل بعده."""


def _reader() -> object:
    spec = importlib.util.spec_from_file_location("run_encoding_audit", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _text() -> str:
    return CORPUS.read_text(encoding="utf-8").replace("<sel>", " ")


def test_the_fallout_is_zero_as_predicted_before_the_run() -> None:
    """لا موضعَ واحدًا خارج الفضاء المعلن — والتنبّؤُ مكتوبٌ قبلَ النظر."""

    reader = _reader()
    units = reader.emit(_text())  # type: ignore[attr-defined]
    assert len(units) == EMITTED
    missed = reader.fallout(units)  # type: ignore[attr-defined]
    assert sum(missed.values()) == PREDICTED_FALLOUT == 0
    assert not missed


def test_the_declared_space_is_thirty_two_by_eight() -> None:
    """ثمانيةٌ وعشرون وهمزةٌ وة وى وآ، وثمانِ حالاتٍ منها العُري."""

    reader = _reader()
    assert len(reader.DECLARED_LETTERS) == 32  # type: ignore[attr-defined]
    assert len(reader.DECLARED_STATES) == 8  # type: ignore[attr-defined]
    assert "" in reader.DECLARED_STATES  # type: ignore[attr-defined]  # العُري
    assert set("ةىآء") <= reader.DECLARED_LETTERS  # type: ignore[attr-defined]
    assert not set("أإؤئ") & reader.DECLARED_LETTERS  # type: ignore[attr-defined]
    assert 32 * 8 == SPACE


def test_the_ceiling_now_bounds_both_the_measured_and_the_observed() -> None:
    """المقيسُ ≤ سقفُ الواقع ≤ سقفُ المعلن — وكان المعلنُ بينهما."""

    reader = _reader()
    seen = Counter(reader.emit(_text()))  # type: ignore[attr-defined]
    assert len(seen) == OBSERVED_PAIRS < SPACE
    measured = reader.entropy(seen)  # type: ignore[attr-defined]
    declared = math.log2(SPACE)
    assert abs(measured - 6.0201) < 5e-4
    assert declared == 8.0
    assert measured < math.log2(len(seen)) < declared
    # وقبلَ الإصلاح كان المعلنُ واقعًا بين المقيس وسقف الواقع
    assert 6.2819 < math.log2(196) < 8.4471


def test_the_vowelling_information_is_measured_as_an_upper_bound() -> None:
    """Δضبط = ١٫٩٥١٨ بتًّا للموضع — وهو حدٌّ أعلى لا قيمةٌ نهائيّة."""

    reader = _reader()
    rasm = reader.rasm_units(_text())  # type: ignore[attr-defined]
    assert len(rasm) == RASM_POSITIONS
    joint = reader.entropy(Counter(rasm))  # type: ignore[attr-defined]
    alone = reader.entropy(  # type: ignore[attr-defined]
        Counter((letter, "") for letter, _ in rasm)
    )
    delta = joint - alone
    assert abs(delta - 1.9518) < 5e-4
    assert abs(joint - 6.2428) < 5e-4
    assert abs(alone - 4.2910) < 5e-4
    assert Fraction(31, 100) < Fraction(int(delta * 10_000), int(joint * 10_000))
    assert delta < joint  # والشرطُ على السياق ينزل به لا يرفعه


def test_the_repair_is_recorded_as_mine_and_the_deposit_is_left_as_written() -> None:
    """المُودَعُ كما ورد يُسقِط ربعَ المواضع، وقياسُه يبقى بلا تعديل."""

    deposit = REPOSITORY / "deposits" / "algebraic_recovery_proof.md"
    text = deposit.read_text(encoding="utf-8")
    assert "٢٨ × ٧" in text  # الفضاءُ المُودَعُ على حاله
    assert "عُرْي" not in text and "عري" not in text
    earlier = REPOSITORY / "tests" / "arabic" / "test_recovery_proof_audit.py"
    assert "80_477" in earlier.read_text(encoding="utf-8")
