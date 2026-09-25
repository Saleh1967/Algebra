"""قراءةٌ موازيةٌ لختم `d44f23ce…`: **الثلاثةُ تنقص، والختمُ لا يُستوفى**.

`THE_SEAL_IS_NOT_DISCHARGED_AND_THAT_IS_SAID_FIRST`: أوراكلُ الختم يسمّي
**«عمودَ الرسم من المحاذاة الكاملة ببصمته وإغلاقه»**، و**المحاذاةُ ليست
في الشجرة** (فحصٌ آليٌّ أدناه). فهذه قراءةٌ على **مدوّنةٍ أخرى مُعلَنة**،
بالحدود نفسِها **غيرَ مبدَّلة**؛ و`d44f23ce…` يبقى **غيرَ مُشغَّل**. ومَن
بدّل المادّةَ وأبقى الاسمَ أفسد الختمَ من حيث أراد حفظَه.

`AND_CONDITION_FIVE_IS_MET_BY_THE_OWNERS_SIGNATURE_NOT_BY_MINE`: ون٥ —
«لا يُقاس بلا روايةٍ مُسمّاة» — مستوفًى بـ`tools/corpus_seal.py`:
`reading_name="حفص عن عاصم"` بوسمِ مصدرٍ **موقَّعٍ من صاحب المستودع**،
و٣ فوارقَ من ٣ موافقة. **ولا أنسب أنا متنًا إلى راوٍ** — وهذا هو الحاجزُ
الذي ارتفع، وارتفاعُه بتوقيعه لا بقولي.

`ALL_THREE_PAIRS_FALL_WELL_UNDER_THE_LINE`: والمرصود:

| الزوج | مرصود | متوقَّع | النسبة | وسيطُ الصفريّ |
|---|---|---|---|---|
| ق ك | ٢١٩ | ٩٢٣٫٨ | **٠٫٢٣٧١** | ٧٨١ |
| س ش | ٤٨ | ١٦٤٫٦ | **٠٫٢٩١٦** | ١٤٤ |
| ب ف | ٤٦٨ | ١٢٣٣٫٥ | **٠٫٣٧٩٤** | ١٠٥٧ |

وحدُّ ن١ «لا يجاوز ٠٫٨٠» — والثلاثةُ دون **نصفِه**. ولا سحبةَ من ألفين
بلغت المرصودَ، فالمئينُ **≤ ١/٢٠٠١** وهي **أرضيّةُ البلوغ** لا رقمًا أصغر.

`AND_THE_FOLDING_POLICY_DOES_NOT_BITE_HERE`: وسياسةُ الطيّ نُشرت بوجهيها
(ن٤) **وأعطت الرقمَ نفسَه حرفًا بحرف** — لأنّ حروفَ الأزواج الستّةَ ليست
من المطويّات. فاستيفاءُ ن٤ ههنا **صوريٌّ**، ويُقال كذلك: السياسةُ التي
بدّلت جوابًا آخرَ من ١٤٤ إلى ٣٧٤ **لا تمسّ هذه الأزواج**.

`BUT_THE_NULL_IS_TOO_FREE_AND_THAT_IS_THE_REAL_LIMIT`: **والقيدُ الأهمّ**:
الصفريُّ يوزّع الحروفَ توزيعًا حرًّا على المواضع، **فيهدم بنيةَ الجذر**.
والكلمُ العربيُّ مبنيٌّ على جذورٍ تتكرّر، فنقصُ اللقاء قد يكون **أثرَ
تكرارِ الجذر** لا قيدًا على الاقتران. والصفريُّ الصحيحُ يحفظ الجذرَ —
**ويحتاج π_اشتقاقي، وهو علاقةٌ لا دالّة** (١٤٬١٠٥ توكنًا بأكثرَ من مرشّح).
فالنتيجةُ **في الاتّجاه المتوقَّع ومشوبةٌ بمُربِكٍ مسمًّى**، والمُربِكُ هو
الإسقاطُ المسدود بعينه.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

from algebra.attainability import permutation_floor

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_tanafur_pairs.py"
SEAL = REPOSITORY / "tests" / "algebra" / "test_tanafur_preregistration.py"
CORPUS_TOOL = REPOSITORY / "tools" / "corpus_seal.py"

pytestmark = requires_corpus

ELIGIBLE = 78_242
SEEN = {("ق", "ك"): 219, ("س", "ش"): 48, ("ب", "ف"): 468}
RATIO = {("ق", "ك"): 0.2371, ("س", "ش"): 0.2916, ("ب", "ف"): 0.3794}
LIMIT = Fraction(80, 100)
SMALLEST = 48
REPLICATES = 2_000


def _reader() -> object:
    spec = importlib.util.spec_from_file_location("run_tanafur_pairs", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _words(folded: bool) -> list[list[str]]:
    reader = _reader()
    return reader.eligible(CORPUS.read_text(encoding="utf-8"), folded)  # type: ignore[attr-defined,no-any-return]


def test_the_alignment_the_seal_names_is_absent_from_the_tree() -> None:
    """أوراكلُ الختم يسمّي المحاذاة، ولا ملفَّ لها — فالختمُ لا يُستوفى."""

    text = SEAL.read_text(encoding="utf-8")
    assert "المحاذاة الكاملة" in text
    found = [
        one for one in REPOSITORY.rglob("*align*") if "__pycache__" not in str(one)
    ]
    assert not found
    assert "d44f23ce" in text  # والبصمةُ باقيةٌ بلا تشغيل


def test_condition_five_is_met_by_a_signed_deposit() -> None:
    """الروايةُ مُسمّاةٌ بتوقيع صاحب المستودع لا بنسبةٍ منّي."""

    text = CORPUS_TOOL.read_text(encoding="utf-8")
    assert 'reading_name="حفص عن عاصم"' in text
    assert 'source_authority="صاحبُ المستودع"' in text
    assert "reading_discriminators=3" in text and "reading_agreed=3" in text


def test_all_three_pairs_fall_under_the_sealed_line() -> None:
    """الثلاثةُ دون نصفِ حدّ ن١ — والحدُّ لم يُمَسّ."""

    reader = _reader()
    words = _words(folded=True)
    assert len(words) == ELIGIBLE
    for pair, count in SEEN.items():
        assert reader.observed(words, pair) == count  # type: ignore[attr-defined]
        due = reader.expected(words, pair)  # type: ignore[attr-defined]
        ratio = count / due
        assert abs(ratio - RATIO[pair]) < 5e-4
        assert Fraction(ratio).limit_denominator(10**6) <= LIMIT
        assert ratio < 0.4 < float(LIMIT)


def test_the_smallest_observed_count_clears_the_reporting_floor() -> None:
    """أقلُّ لقاءٍ ٤٨، وحدُّ ن٣ اثنا عشر — فالثلاثةُ تُقرأ."""

    assert min(SEEN.values()) == SMALLEST >= 12


def test_the_percentile_is_the_attainability_floor_not_a_smaller_number() -> None:
    """لا سحبةَ بلغت المرصود — فالمنشورُ ١/٢٠٠١ لا صفر."""

    floor = permutation_floor(REPLICATES)
    assert floor == Fraction(1, 2_001)
    assert float(floor) < 5e-4


def test_the_folding_policy_gives_the_same_number_both_ways() -> None:
    """ن٤ مستوفًى صوريًّا: حروفُ الأزواج ليست من المطويّات."""

    reader = _reader()
    folded = _words(folded=True)
    apart = _words(folded=False)
    for pair in SEEN:
        assert reader.observed(folded, pair) == reader.observed(apart, pair)  # type: ignore[attr-defined]
    fold = reader.FOLD  # type: ignore[attr-defined]
    for pair in SEEN:
        assert not set(pair) & set(fold)


def test_the_null_destroys_root_structure_and_that_is_declared() -> None:
    """الصفريُّ حرٌّ فيهدم الجذر — والمُربِكُ هو الإسقاطُ المسدود."""

    text = Path(__file__).read_text(encoding="utf-8")
    assert "يهدم بنيةَ الجذر" in text
    assert "علاقةٌ لا دالّة" in text
    projection = REPOSITORY / "tests" / "arabic" / "test_root_projection_run.py"
    assert "14_105" in projection.read_text(encoding="utf-8")
