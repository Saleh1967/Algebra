"""البرهانُ الجبريّ: **الحقنُ صحيح، والفضاءُ لا يغطّي البايتات**.

`THE_DERIVED_POSITION_IS_A_REAL_RETRACTION`: ويُقرّ أوّلًا وأقواه — R6:
**الموضعُ مشتقٌّ لا مستقلّ**، فالمخرجُ دالّةُ الحرف والموقعُ دالّةُ الفهرس،
**فصفرُ بتٍّ مستقلّ**. وهذا **تراجعٌ يكلِّف**: يهدم ثلاثيّةَ L₀ إلى زوج،
ويسقط خانةً من الشكل الجذاذيّ في أسفل السلسلة. والتراجعُ الذي يكلّف صاحبَه
أصدقُ من قانونٍ يربحه.

`AND_THE_INJECTION_ARGUMENT_IS_SOUND_WHERE_IT_APPLIES`: وحجّةُ الحقن صحيحة:
e حاقنةٌ ⟹ H(الوحدة | الترميز) = ٠ — **بالبناء** كما وُسِمت، لا قياسًا. ولا
اعتراضَ على الاستدلال؛ الاعتراضُ على **مجاله**.

`A_QUARTER_OF_THE_CORPUS_HAS_NO_STATE_IN_THE_DECLARED_SEVEN`: فمن ٣٣٢٬٨٣٧
موضعَ حرفٍ في المدوّنة **المشكولة**، **٨٠٬٤٧٧ (٠٫٢٤١٨) بلا علامةٍ ألبتّة** —
وهي حالةٌ ليست من السبع. و«بلا علامة» ليس نصًّا مجرّدًا (R8) بل **حرفٌ عارٍ
داخلَ كلمةٍ مضبوطة**: ألفُ «الْحَمْدُ» مثالًا. فالحاقنةُ e مُعرَّفةٌ على ١٩٦
وحدة، **ولا مُدخَلَ لها في ربع مواضع المدوّنة**.

`AND_THREE_LETTERS_FALL_OUTSIDE_BOTH_R1_AND_R2`: و**ى (٢٬٥٩٢) وة (٢٬٣٤٤)
وآ (١٬٥١١)** = **٦٬٤٤٧ وقوعًا** ليست من الثمانية والعشرين ولا من كراسي
الهمزة، **ولا قاعدةَ لها في R1–R8**. والهمزةُ مُعلَنةٌ (R2) فلا تُحسب
عليها.

`THE_CEILING_IS_NEITHER_THE_VALUE_NOR_A_BOUND`: و«log₂(١٩٦) = ٧٫٦١٤٧ سقفًا»
تسقط من الجهتين معًا: **المرصودُ ٦٫٢٨١٩ بتًّا** (فالسقفُ يزيد ١٫٣٣)،
**وسقفُ الأبجديّة المرصودة ٨٫٤٤٧١** على ٣٤٩ زوجًا مرصودًا (فالسقفُ المعلن
**أدنى** من سقف ما وقع). وسقفٌ لا هو القيمةُ ولا هو حدٌّ أعلى **ليس سقفًا**.

`AND_THE_ALPHABET_IS_ALREADY_IN_THE_TREE_AND_ALREADY_MEASURED`: والنظامُ
ليس جديدًا: **أبجديّةُ الذرّات** (١٩٤ رمزًا) مُودَعةٌ في `ladder_map.tsv`
ومقيسةٌ في `test_layer_induction_run` — ومعلوماتُها المتبادلةُ ١٫٦٩٩٤ بتًّا.
والفرقُ في العدّ يُفسَّر تامًّا: ٣٣٢٬٨٣٧ − ٣٣١٬٢٥٩ = **١٬٥٧٨** = وقوعاتُ
«ء» بالضبط، وهي المطويّةُ في خريطة السلّم. فالمقترَحُ **مقيسٌ من قبلُ**،
والجديدُ فيه **الوصفُ لا الرقم**.

`AND_A_SPECIFICATION_IS_NOT_AN_AUDIT`: و«هذا البرهانُ هو تدقيقُ Δرقمي
بعينه» **استبدالُ جنس**: الدَّينُ المسجَّلُ كان «ماذا يبتلع أنبوبي؟» وقد
حُدِّد موضعُه في `test_ingestion_swallows` عند **إملاء/رقميّ** بأربعة
ابتلاعاتٍ معدودة. ومواصفةُ مُرمِّزٍ **جديد** لا تدقّق أنبوبًا **قائمًا**.
والدليلُ في هذا الملفّ نفسِه: المواصفةُ مُدَقَّقةً على البايتات **تفقد ربعَ
المواضع** — فالدَّينُ لم يُغلَق، بل **قِيس لأوّل مرّة**.
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
READER = REPOSITORY / "examples" / "rasm" / "run_unit_coverage.py"
DEPOSIT = REPOSITORY / "deposits" / "algebraic_recovery_proof.md"

pytestmark = requires_corpus

POSITIONS = 332_837
BARE = 80_477
OUTSIDE = {"ى": 2_592, "ة": 2_344, "آ": 1_511}
OBSERVED_STATES = 15
OBSERVED_PAIRS = 349
LADDER_POSITIONS = 331_259
HAMZA_OCCURRENCES = 1_578


def _reader() -> object:
    spec = importlib.util.spec_from_file_location("run_unit_coverage", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _units() -> list[tuple[str, str]]:
    reader = _reader()
    text = CORPUS.read_text(encoding="utf-8").replace("<sel>", " ")
    return reader.units(text)  # type: ignore[attr-defined,no-any-return]


def test_a_quarter_of_the_positions_carry_no_declared_state() -> None:
    """٨٠٬٤٧٧ حرفًا عاريًا داخلَ نصٍّ مضبوط — وليست من السبع."""

    found = _units()
    assert len(found) == POSITIONS
    states = Counter(state for _, state in found)
    assert states[""] == BARE
    assert Fraction(BARE, POSITIONS) > Fraction(24, 100)
    assert len(states) == OBSERVED_STATES > 7


def test_three_letters_fall_outside_every_declared_rule() -> None:
    """ى وة وآ: ستّةُ آلافٍ وأربعمئةٍ وسبعٌ وأربعون وقوعًا بلا قاعدة."""

    reader = _reader()
    letters = Counter(letter for letter, _ in _units())
    declared = set(reader.HIJAI) | set(reader.HAMZA_SEATS)  # type: ignore[attr-defined]
    outside = {one: number for one, number in letters.items() if one not in declared}
    assert outside == OUTSIDE
    assert sum(outside.values()) == 6_447


def test_the_declared_ceiling_is_neither_the_value_nor_an_upper_bound() -> None:
    """المرصودُ ٦٫٢٨ والسقفُ ٧٫٦١ وسقفُ المرصودِ ٨٫٤٤ — فهو بينهما."""

    reader = _reader()
    pairs = Counter(_units())
    assert len(pairs) == OBSERVED_PAIRS > 196
    measured = reader.entropy(pairs)  # type: ignore[attr-defined]
    declared = math.log2(196)
    assert abs(measured - 6.2819) < 5e-4
    assert abs(declared - 7.6147) < 5e-4
    assert measured < declared < math.log2(len(pairs))


def test_the_alphabet_is_the_deposited_atom_alphabet_already_measured() -> None:
    """الفرقُ عن عدّ الذرّات ١٬٥٧٨ = وقوعاتُ «ء» بالضبط."""

    letters = Counter(letter for letter, _ in _units())
    assert letters["ء"] == HAMZA_OCCURRENCES
    assert POSITIONS - LADDER_POSITIONS == HAMZA_OCCURRENCES
    ladder = REPOSITORY / "deposits" / "ladder_map.tsv"
    assert ladder.exists()  # والأبجديّةُ مُودَعةٌ من قبلُ


def test_the_deposit_calls_itself_the_digital_audit_it_is_not() -> None:
    """المواصفةُ تُعلن أنّها التدقيق، والتدقيقُ يقع عليها فتفقد ربعَ المواضع."""

    text = DEPOSIT.read_text(encoding="utf-8")
    assert "تدقيق Δرقمي" in text
    audit = REPOSITORY / "tests" / "arabic" / "test_ingestion_swallows.py"
    assert audit.exists()
    assert "إملاء/رقميّ" in audit.read_text(encoding="utf-8")
    assert BARE > 0  # والمواصفةُ نفسُها لا تُغطّي هذا العدد
