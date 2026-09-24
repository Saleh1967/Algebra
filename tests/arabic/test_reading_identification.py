"""الروايةُ سُمِّيت — مخرَجَ قياسٍ لا إقرارَ جلسة، وبمداها لا مطلقةً.

**كيف رُفِعت الخانةُ الصفراء**: لم أوقّع اسمًا. سُمِّيت **ثلاثةُ فوارقَ
قبل النظر**، ولكلٍّ وجهان: وجهٌ لحفصٍ عن عاصم ووجهٌ يخالفه بصاحبه. ثمّ
قُرِئت من البايتات المُجمَّدة، فوافقتها **ثلاثةٌ من ثلاثة**.

| الموضع | وجهُ حفص | الوجهُ المخالف | صاحبُه |
|---|---|---|---|
| الفاتحة ٤ | مالك | ملك | نافع — ورش وقالون |
| الفاتحة ٦ | الصراط | السراط | قنبل |
| البقرة ٢٥٩ | ننشزها | ننشرها | قراءةُ الراء |

`THE_NAME_IS_AN_OUTPUT_NOT_A_SIGNATURE`: فالاسمُ **يخرج من الآلة**: إن
وافقت الفوارقُ كلُّها نُسِب، وإن خالف واحدٌ بقيت الخانةُ صفرًا ويُطبَع
العدد. وموافقةُ اثنين من ثلاثةٍ **لا تنسب**: النسبةُ بأغلبيّةٍ ليست نسبة.

`ITS_KIND_IS_INFERRED_NOT_ATTESTED`: ومنزلتُه `Evidence.INFERRED` لا
`ATTESTED`: ليس في الشجرة سندٌ يقول «هذه رواية كذا»، وإنّما بناءٌ على فوارقَ
مقيسة. ولو وُجِد السندُ لتبدّلت المنزلةُ لا الاسم.

`AND_ITS_SCOPE_IS_WHAT_WAS_NAMED`: ومداه ما سُمِّي: يفصل عن نافعٍ وقنبلٍ
وقراءةِ الراء، **لا عن كلّ راوٍ**. فمن أراد مدًى أوسعَ زاد فوارقَ وأعاد.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

from algebra.results import Evidence, trial_for

REPOSITORY = Path(__file__).resolve().parents[2]
CORPUS = REPOSITORY / "corpora" / "quran-simple-enhanced.txt"
RUNNER = REPOSITORY / "examples" / "rasm" / "run_schema_transition_audit.py"

pytestmark = pytest.mark.skipif(
    not CORPUS.is_file(),
    reason="بايتاتُ المدوّنة المُجمَّدة غيرُ مستقبَلةٍ في هذه الشجرة",
)


def _audit() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_schema_transition_audit", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


audit = _audit()


def test_the_three_discriminators_are_named_with_their_rivals() -> None:
    """ثلاثةُ مواضعَ، لكلٍّ وجهان وصاحبٌ للوجه المخالف — ولا وجهَ بلا صاحب."""

    table = audit.READING_DISCRIMINATORS
    assert len(table) == 3
    assert len({number for number, _, _, _ in table}) == 3
    for _, expected, other, rival in table:
        assert expected != other
        assert rival.strip()


def test_the_deposited_bytes_agree_with_every_discriminator() -> None:
    """ثلاثةٌ من ثلاثة، فيُنسَب الاسم؛ ولا يُنسَب بأقلَّ منها."""

    lines = CORPUS.read_text(encoding="utf-8").splitlines()
    named, agreed = audit.identify_reading(lines)
    assert agreed == len(audit.READING_DISCRIMINATORS) == 3
    assert named == (audit.CANDIDATE_READING,)
    assert audit.CANDIDATE_READING == "حفص عن عاصم"


def test_a_majority_does_not_name_and_a_disagreement_empties_the_field() -> None:
    """خلافُ واحدٍ يُبقي الخانةَ صفرًا — والنسبةُ بأغلبيّةٍ ليست نسبة."""

    lines = CORPUS.read_text(encoding="utf-8").splitlines()
    broken = list(lines)
    number, expected, other, _ = audit.READING_DISCRIMINATORS[0]
    # والاستبدالُ يجري على سطرٍ مجرَّدٍ من الضبط: فالعلاماتُ تتخلّل الحروفَ
    # في الأصل، فلا يُوجَد اللفظُ فيه متّصلًا — وذلك نفسُه سببُ التجريد قبل
    # المطابقة في `identify_reading`.
    broken[number - 1] = f"{other} يوم الدين"
    assert expected not in audit._bare(broken[number - 1])

    named, agreed = audit.identify_reading(broken)
    assert agreed == 2
    assert named == ()


def test_the_kind_of_this_naming_is_inference_not_attestation() -> None:
    """منزلتُه استنتاجٌ بمقامٍ وصفريّ، لا نصًّا يُروى — ولكلٍّ مِقامُ برهان."""

    assert Evidence.INFERRED is not Evidence.ATTESTED
    assert trial_for(Evidence.INFERRED) != trial_for(Evidence.ATTESTED)

    # ولو وُجِد سندٌ في الشجرة لتبدّلت المنزلةُ لا الاسم
    assert audit.CANDIDATE_READING not in trial_for(Evidence.ATTESTED)


def test_the_scope_is_the_named_rivals_only() -> None:
    """المدى ما سُمِّي: نافعٌ وقنبلٌ وقراءةُ الراء — لا كلُّ راوٍ."""

    rivals = {rival for _, _, _, rival in audit.READING_DISCRIMINATORS}
    assert len(rivals) == 3
    assert any("نافع" in one for one in rivals)
    assert any("قنبل" in one for one in rivals)
