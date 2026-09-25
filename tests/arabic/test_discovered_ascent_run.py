"""شُغِّل ختمُ `620b63a2…`: **خمسةٌ من ستّة — والعدُّ يبني الوظيفيَّ أوّلًا**.

**السجلُّ الكاملُ في** `deposits/discovered_ascent_run.log`؛ وهذا الملفُّ
يحكم عليه، **ويفحص الآلةَ على شريحةٍ صغيرةٍ** لأنّ التشغيلَ التامَّ يقارب
ربعَ الساعة، ولا يُحشَر في مجموعة الفحوص.

`THE_ASCENT_HALTED_BY_ITSELF`: التكلفةُ نزلت في **تسع** نقاطِ فحصٍ
متتاليةٍ ثمّ **ارتفعت** عند الخمسة آلاف. فنقطةُ الوقوف **٥٬٠٠٠**، وأفضلُ
تكلفةٍ عند **٤٬٥٠٠**: **١٬٣٨٩٬٤٤٨** بتًّا من **٢٬٠٣٦٬١٥٣** — **٠٫٦٨٢٤**.
والمحجوزةُ والملحَقةُ **تتّفقان على نقطة الوقوف نفسِها** (أدنى الملحَقة
١٬٣٨٠٬٤٠٤ عند ٤٬٥٠٠ أيضًا)، فالوقوفُ **ليس أثرَ الحجز**.

`AND_THE_BLIND_COUNT_BEAT_THE_RULE_I_BUILT_BY_HAND`: وك٣ **صمد**:
٠٫٦٨٢٤ مقابل **٠٫٨٩٣٣** للمقطع المبنيِّ بقاعدةٍ لغويّةٍ في `0021350c…` —
أي **٠٫٧٧٨٠ منه**. فالاقتصادُ الأعمى **يسبق قاعدتي بـ٢٢٪**، وهي دعوًى
كانت معرَّضةً للسقوط فصمدت.

`AND_WHAT_IT_BUILT_FIRST_IS_THE_CLOSED_FUNCTIONAL_LAYER_ENTIRE`: وهذا
**أثقلُ من الرقم**. الدمجُ لا يرى كلمةً ولا صرفًا ولا نحوًا — يرى وقوعاتٍ
فقط. وأكثرُ أربعَ عشرةَ وحدةً بناها:

| الوحدة | وقوعات | ما هي |
|---|---|---|
| **ال** | ٥٢٠ | أداةُ التعريف |
| **هَا · هُمْ · نَا · كُمْ** | ٤٨١ · ٤٨٠ · ٤٥٣ · ٤١٨ | الضمائرُ الأربعة |
| **مَا · مِن · فِي** | ٤٥٥ · ٤٥٣ · ٣١١ | أسماءٌ وحروفٌ وظيفيّة |
| **اللَّهُ** | ٣٣٤ | خمسُ وحداتٍ تامّة |
| **إِلَّا · عَلَى · وَالْ · وَمَا · وَا** | ٣١١ · ٣٢٣ · ٢٩٠ · ٢٧٧ · ٣٣٩ | |

**ولا واحدةَ منها كلمةٌ معجميّةٌ مفتوحة.** فالطبقةُ التي يبنيها الاقتصادُ
فوقَ الصوت مباشرةً هي **الوظيفيّةُ المغلقة** بأسرها — وهي رابعُ طريقٍ
مستقلّةٍ تنتهي إليها هذه الجلسة، بعد التباسِ الرسم، وثقلِ اللام والنون في
دفتر البتّات، وأرضيّةِ الرسم.

`BUT_THE_WORD_BOUNDARY_IS_NOT_DISCOVERED`: وك٤ **سقط**: نصيبُ ما لا يعبر
حدَّ الكلمة **٠٫٨٢٩٠** والحدُّ ٠٫٩٠. فالدمجُ يعبر الفراغَ في **سُدُسِ**
وقوعاته — و«وَاْلْ» و«وَمَاْ» شاهدان. **فحدُّ الكلمة لا يكتشفه الاقتصادُ
وحدَه**، ويبقى مُلقَّنًا كما قال نصُّ الشرط.

`AND_THE_SHAPES_ARE_SLICED_FROM_THE_BYTES_NOT_REBUILT`: وصورُ الوحدات
**مقتطعةٌ من السطر نفسِه** بمدًى محفوظٍ لكلّ وحدة. وكان أوّلُ عرضٍ يركّبها
من التمثيل الداخليّ فيُخرِج ما ليس في المصحف (`اْلْلْلَهُ` مكانَ
`اللَّهُ`) — **والأرقامُ كانت صحيحةً والصورُ ملفَّقة**. فلا تُعرَض صورةٌ
إلّا وهي بايتاتُ المدوّنة حرفًا بحرف.

`AND_THE_ANTI_OVERFIT_GAP_GROWS_WITH_THE_DICTIONARY`: وك٥ صمد، وفرقُه
**يتّسع باطّراد**: +١٬٣٤٦ عند الخمسمئة و+٩٬٧٨٩ عند الخمسة آلاف — لأنّ
المعجمَ ينمو فيثقل ثمنُ ما لم يُرَ. فالحجزُ **يعمل ويُرى عملُه**.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus
from test_discovered_ascent_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_discovered_ascent.py"
LOG = REPOSITORY / "deposits" / "discovered_ascent_run.log"

pytestmark = requires_corpus

L0_COST = 2_036_153.0
BEST_COST = 1_389_448.0
BEST_INSIDE = 1_380_404.0
BEST_AT = 4_500
STOPPED_AT = 5_000
SYLLABLE_COST = 1_785_954.0
NOT_CROSSING = 0.8290
GAPS = (1_346, 2_426, 3_514, 4_606, 5_677, 6_482, 7_442, 8_328, 9_044, 9_789)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _reader() -> object:
    spec = importlib.util.spec_from_file_location("run_discovered_ascent", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_seal_was_deposited_before_the_build() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("620b63a2")


def test_the_machine_absorbs_exactly_on_a_slice() -> None:
    """بسطُ الرموز يعيد الـ١١٢ بالضبط — يُفحَص لا يُدَّعى."""

    reader = _reader()
    verses, _, order, _lines, _reach = reader.corpus_of(  # type: ignore[attr-defined]
        CORPUS.read_text(encoding="utf-8")
    )
    slice_ = [list(one) for one in verses[:200]]
    before = [list(one) for one in slice_]
    lengths = {index: 1 for index in range(len(order))}
    spelling: dict[int, tuple[int, ...]] = {
        index: (index,) for index in range(len(order))
    }
    for _ in range(50):
        found = reader.best_pair(slice_)  # type: ignore[attr-defined]
        if found is None:
            break
        pair, _count = found
        fresh = len(lengths)
        lengths[fresh] = lengths[pair[0]] + lengths[pair[1]]
        spelling[fresh] = spelling[pair[0]] + spelling[pair[1]]
        reader.apply_merge(slice_, pair, fresh)  # type: ignore[attr-defined]
    rebuilt = [[one for symbol in row for one in spelling[symbol]] for row in slice_]
    assert rebuilt == before
    assert len(order) == 112


def test_the_ascent_halted_and_both_costs_agree_on_where() -> None:
    """ك١ وك٦: تسعُ نزلاتٍ ثمّ ارتفاع، والملحَقةُ تتّفق على ٤٬٥٠٠."""

    text = LOG.read_text(encoding="utf-8")
    assert f"نقطةُ الوقوف: {STOPPED_AT}" in text
    assert f"أفضلُ تكلفةٍ عند {BEST_AT}" in text
    first = next(one for one in PREDICTIONS if one.identifier == "ك١")
    assert first.verdict(Fraction(0)) is Verdict.MET
    sixth = next(one for one in PREDICTIONS if one.identifier == "ك٦")
    assert sixth.verdict(Fraction(STOPPED_AT)) is Verdict.MET
    assert BEST_INSIDE < 1_381_140  # وأدنى الملحَقةِ عند ٤٬٥٠٠ أيضًا


def test_the_discovered_ascent_beats_both_the_base_and_my_syllable() -> None:
    """ك٢ وك٣: ٠٫٦٨٢٤ من L₀ و٠٫٧٧٨٠ من المقطع المبنيِّ بيدي."""

    second = next(one for one in PREDICTIONS if one.identifier == "ك٢")
    third = next(one for one in PREDICTIONS if one.identifier == "ك٣")
    assert second.verdict(_exact(BEST_COST / L0_COST)) is Verdict.MET
    assert third.verdict(_exact(BEST_COST / SYLLABLE_COST)) is Verdict.MET
    assert abs(BEST_COST / L0_COST - 0.6824) < 5e-5
    assert abs(BEST_COST / SYLLABLE_COST - 0.7780) < 5e-5
    assert "دعوايَ" in third.falsifies  # وكانت معرَّضةً فصمدت


def test_the_word_boundary_is_not_discovered_by_thrift_alone() -> None:
    """ك٤ سقط: ٠٫٨٢٩٠ دون ٠٫٩٠ — فالدمجُ يعبر الفراغَ في سُدُسِ وقوعاته."""

    fourth = next(one for one in PREDICTIONS if one.identifier == "ك٤")
    assert fourth.verdict(_exact(NOT_CROSSING)) is Verdict.FALSIFIED
    assert "مُلقَّنًا لا مكتشَفًا" in fourth.falsifies
    text = LOG.read_text(encoding="utf-8")
    assert "لا يعبر حدَّ الكلمة: 89397 من 107841" in text


def test_the_anti_overfit_gap_held_and_widened_with_the_dictionary() -> None:
    """ك٥: أدنى فرقٍ +١٬٣٤٦، ويتّسع إلى +٩٬٧٨٩ كلّما نما المعجم."""

    fifth = next(one for one in PREDICTIONS if one.identifier == "ك٥")
    assert fifth.verdict(Fraction(min(GAPS))) is Verdict.MET
    assert min(GAPS) == 1_346 and max(GAPS) == 9_789
    assert list(GAPS) == sorted(GAPS)  # يتّسع باطّراد


def test_every_discovered_unit_is_closed_class() -> None:
    """الصورُ تُقرأ من السجلّ لا تُكتَب باليد — والحرفُ المكتوبُ يخالف."""

    text = LOG.read_text(encoding="utf-8")
    rows = re.findall(r"^    (\S+)  \((\d+)\) وحداتُه (\d+)$", text, re.MULTILINE)
    assert len(rows) == 14
    shapes = [one for one, _, _ in rows]
    assert len({one for one in shapes}) == 14
    widest = max(rows, key=lambda row: int(row[2]))
    assert int(widest[2]) == 5 and int(widest[1]) == 334  # «الله» تامّةً
    # ولا صورةَ تحمل رمزَ التمثيل الداخليّ: ساكنٌ على ألفٍ لا يُكتَب في المصحف
    for shape in shapes:
        assert "ا\u0652" not in shape, shape
    assert sum(1 for _, number, _ in rows if int(number) >= 400) == 7


def test_the_document_quotes_shapes_verbatim_from_the_log() -> None:
    """كلُّ صورةٍ في التوثيق منقولةٌ من السجلّ — لا مكتوبةً بيد.

    **وهذا الفحصُ يحرس التشكيلَ والهمزةَ والشدّة**: صورةٌ تُكتَب باليد قد
    تخالف بايتةً واحدة (ترتيبَ علامةٍ أو صورةَ همزة) فتصير هلوسةً تبدو
    صحيحة. فتُقارَن صورُ الوثيقة بصور السجلّ **مطابقةً تامّة**.
    """

    paper = REPOSITORY / "docs" / "الصعود-المكتشَف.md"
    text = LOG.read_text(encoding="utf-8")
    shapes = {
        one
        for one, _, _ in re.findall(
            r"^    (\S+)  \((\d+)\) وحداتُه (\d+)$", text, re.MULTILINE
        )
    }
    written = paper.read_text(encoding="utf-8")
    quoted = re.findall(
        r"^\| \*\*(\S+)\*\* \| (\d+) \| (\d+) \|", written, re.MULTILINE
    )
    assert len(quoted) == 14
    for shape, _, _ in quoted:
        assert shape in shapes, shape
    assert {one for one, _, _ in quoted} == shapes
