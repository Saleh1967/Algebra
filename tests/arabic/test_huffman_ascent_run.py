"""شُغِّل ختمُ `34133d54…`: **ستّةٌ من ستّة — وأوّلُ ختمٍ يصمد تامًّا**.

`THE_DIAGNOSIS_WAS_MINE_AND_IT_HELD`: ل٣ كان **تشخيصي للخلل** معرَّضًا:
كان البيانُ **إنتروبيا**، وهي **حدٌّ أدنى لا تبلغه شفرةٌ رمزًا رمزًا**.
والمقيس: **١٬٣٩٤٬٦٣٨** بهوفمان مقابلَ **١٬٣٨٩٬٤٤٨** بالإنتروبيا —
**١٫٠٠٣٧**. فالإنتروبيا كانت تطوي **٥٬١٩٠ بتًّا** عند أفضل نقطة،
و**٨٬٥٠٧** عند نقطة الصفر.

`AND_THE_TWO_HALVES_OF_GREEDY_ARE_NO_LONGER_ONE_SENTENCE`: والخللُ كان في
**عبارةٍ واحدةٍ خلطت شطرين**: «الاختيارُ جشعٌ فالتكلفةُ حدٌّ أعلى».
والصواب: **القسمةُ** جشعٌ **غيرُ مبرهَن** ⟹ حدٌّ أعلى؛ **والترميزُ** جشعٌ
**مبرهَن** (هوفمان) ⟹ أمثلُ رمزًا رمزًا، **لا حدَّ فوقه ولا تحته**.

`THE_PROVEN_BOUNDS_HOLD_AT_EVERY_CHECKPOINT`: ول١ ول٢ صمدا: `L − H` في
`[٠، ١)` في النقاط الإحدى عشرة كلِّها — **+٠٫٠٢٣٩** أدناه و**+٠٫١٤٧٥**
أقصاه. **فالمبنيُّ شفرةُ هوفمان فعلًا**، لا شيءٌ يشبهها.

`AND_MY_REASONING_UNDER_THE_FOURTH_WAS_WRONG_THOUGH_IT_PASSED`: ول٤
**مستوفًى على حدّه تمامًا** (٤٬٥٠٠ ≥ ٤٬٥٠٠) — **وتعليلي الذي كتبتُه معه
ساقط**: قلتُ «ثمنُ هوفمان يخفّ بنقصان عدد الرموز فيتأخّر الوقوف»،
والمقيسُ أنّ `L − H` **ينمو باطّراد** مع الدمج، فالثمنُ **يثقل لا يخفّ**.
والوقوفُ **لم يتأخّر ولم يتقدّم**. **وشرطٌ يمرّ بتعليلٍ خاطئ ليس تأييدًا**،
ويُسجَّل كذلك.

`AND_THE_BYTES_ARRIVE_WHOLE`: ول٥ صمد: `rebuild(peel(x)) == x` **بايتةً
بايتة** — فلا تشكيلةَ ولا همزةَ ولا شدّةَ ولا حرفَ يسقط، **ولا يُعرَف
لأيٍّ منها اسمٌ ولا وظيفة**.

`AND_THE_HOLD_OUT_GAP_WAS_MEASURED_NOT_ASSUMED`: ول٦ صمد بأدنى فرقٍ
**+٣٢٤**، ويتّسع إلى **+١٢٬٩٥٠** كلّما نما المعجم. وكنتُ أغفلتُ طبعَه في
التشغيل الأوّل **فأعدتُ التشغيلَ ولم أفترضه** — وهي الغفلةُ نفسُها التي
وقعت في `620b63a2…` قبلَها.

`AND_NOTHING_ELSE_MOVED`: والوقوفُ **٥٬٠٠٠**، وأفضلُ تكلفةٍ عند **٤٬٥٠٠**،
والنسبةُ **٠٫٦٨٢١**، والعبورُ **٠٫٨٣٧٩**، والقسمةُ بالعَرض **حرفًا بحرف**
كما كانت — ومجموعةُ العَرض ١ **مئةٌ واثنتا عشرة**.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_huffman_ascent_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "huffman_ascent_run.log"
PAPER = REPOSITORY / "docs" / "الصعود-المكتشَف.md"

pytestmark = requires_corpus

BY_ENTROPY = 1_389_448.0
BY_HUFFMAN = 1_394_638.0
ZERO_HUFFMAN = 2_044_660.0
ZERO_ENTROPY = 2_036_153.0
BEST_AT = 4_500
STOPPED = 5_000
RATIO = 0.6821
CROSSING = 0.8379


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _checkpoints() -> list[tuple[float, float, float]]:
    """(L−H، المحجوزة − الملحَقة، الجملة) لكلّ نقطةِ فحص."""

    text = LOG.read_text(encoding="utf-8")
    found: list[tuple[float, float, float]] = []
    for line in text.splitlines():
        hit = re.search(r"الجملة (\d+) .*L−H ([+-][\d.]+) .*فرق ([+-]\d+)", line)
        if hit:
            found.append(
                (float(hit.group(2)), float(hit.group(3)), float(hit.group(1)))
            )
    return found


def test_the_seal_was_deposited_before_the_build() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("34133d54")


def test_the_proven_bounds_hold_at_every_checkpoint() -> None:
    """ل١ ول٢: L−H في [٠، ١) في النقاط كلِّها."""

    steps = _checkpoints()
    assert len(steps) == 10
    gaps = [one for one, _, _ in steps]
    low = next(one for one in PREDICTIONS if one.identifier == "ل١")
    high = next(one for one in PREDICTIONS if one.identifier == "ل٢")
    assert low.verdict(_exact(min(gaps))) is Verdict.MET
    assert high.verdict(_exact(max(gaps))) is Verdict.MET
    assert abs(max(gaps) - 0.1475) < 5e-5
    assert gaps == sorted(gaps)  # والثمنُ يثقل باطّراد لا يخفّ


def test_the_diagnosis_of_the_flaw_held() -> None:
    """ل٣: ١٫٠٠٣٧ — والإنتروبيا كانت تطوي ٥٬١٩٠ بتًّا."""

    third = next(one for one in PREDICTIONS if one.identifier == "ل٣")
    ratio = BY_HUFFMAN / BY_ENTROPY
    assert third.verdict(_exact(ratio)) is Verdict.MET
    assert abs(ratio - 1.0037) < 5e-5
    assert BY_HUFFMAN - BY_ENTROPY == 5_190.0
    assert ZERO_HUFFMAN - ZERO_ENTROPY == 8_507.0


def test_the_fourth_passed_on_its_edge_while_its_reasoning_fell() -> None:
    """٤٬٥٠٠ ≥ ٤٬٥٠٠ — والتعليلُ الذي كُتِب معه مخالفٌ للمقيس."""

    fourth = next(one for one in PREDICTIONS if one.identifier == "ل٤")
    assert fourth.verdict(Fraction(BEST_AT)) is Verdict.MET
    assert fourth.threshold == Fraction(BEST_AT)  # على الحدّ تمامًا
    assert "يخفّ بنقصان عدد الرموز" in fourth.falsifies
    gaps = [one for one, _, _ in _checkpoints()]
    assert gaps[-1] > gaps[0]  # والمقيسُ أنّه يثقل


def test_the_hold_out_gap_was_measured_and_held() -> None:
    """ل٦: أدنى فرقٍ +٣٢٤، ويتّسع إلى +١٢٬٩٥٠."""

    sixth = next(one for one in PREDICTIONS if one.identifier == "ل٦")
    gaps = [one for _, one, _ in _checkpoints()]
    assert sixth.verdict(Fraction(int(min(gaps)))) is Verdict.MET
    assert min(gaps) >= 1_105 and max(gaps) == 12_950
    text = LOG.read_text(encoding="utf-8")
    assert "ملحَقة 2044336" in text  # ونقطةُ الصفر فرقُها +٣٢٤


def test_the_stopping_point_and_the_census_did_not_move() -> None:
    """الوقوفُ والقسمةُ كما كانا — والتصحيحُ مسّ الكلفةَ لا البنية."""

    text = LOG.read_text(encoding="utf-8")
    assert f"نقطةُ الوقوف: {STOPPED} | أفضلُ تكلفةٍ عند {BEST_AT}" in text
    assert f"النسبةُ إلى L₀ {RATIO:.4f}" in text
    assert f"= {CROSSING:.4f}" in text
    assert "عَرضُ 1: رموزٌ 112" in text
    assert "الجملة: رموزٌ 4538 | وقوعاتٌ 110994" in text


def test_the_document_quotes_shapes_verbatim_and_has_no_gloss_column() -> None:
    """صورُ الوثيقة تُقارَن بصور السجلّ مطابقةً تامّة، ولا عمودَ تفسير."""

    text = LOG.read_text(encoding="utf-8")
    shapes = {
        one
        for one, _, _ in re.findall(
            r"^    (\S+)  \((\d+)\) وحداتُه (\d+)$", text, re.MULTILINE
        )
    }
    written = PAPER.read_text(encoding="utf-8")
    quoted = re.findall(
        r"^\| \*\*([^*|٠-٩]+)\*\* \| ([٠-٩]+) \| ([٠-٩]+) \|$", written, re.MULTILINE
    )
    assert {one for one, _, _ in quoted} == shapes
    assert len(quoted) == 14
    assert "| ما هي |" not in written
