"""شُغِّل الإسقاطُ المُودَع: **π_اشتقاقي ليس دالّةً — بل علاقة**.

**ما جرى**: أُودع `projection_specs.md` موقَّعًا، فزال الحاجزُ الذي قيل في
`7ef2c4b` إنّه «فعلُك لا فعلي». وأوّلُ ما يفعله المودَعُ أن **يُشغَّل**.

`THE_FIRST_DECISION_IS_THE_ONLY_RUNNABLE_ONE`: والقرارُ الثاني يُحيل إلى
«الجدول الموروث» لردّ المعتلّ **ولم يُودَع معه** — فالإيداعُ يسمّي جدولًا لا
يحمله. فشُغِّل القرارُ الأوّلُ وحدَه، **وأثرُ النقص معلنٌ في الاتّجاهين**:
ردُّ المعتلّ يزيد المرشّحات، فالتغطيةُ ههنا حدٌّ أدنى **والالتباسُ حدٌّ أدنى
أيضًا** — فلا يرفعه القرارُ الثاني بل يرفعه إن رُفِع.

`THE_PROJECTION_RETURNS_MORE_THAN_ONE_ROOT_ON_ONE_TOKEN_IN_SIX`: ومن
٧٨٬٢٤٥ توكنًا: **٢٣٬٨٨٤** بمرشّحٍ واحد، و**١٤٬١٠٥ بأكثرَ من مرشّح**
(٠٫١٨٠٣ من الكلّ، و**٠٫٣٧١٣ ممّا بُلِغ**)، و٤٠٬٢٥٦ بلا مرشّح. فعلى أكثرَ من
ثلث ما يبلغه الإسقاطُ **لا يعطي قيمةً واحدة**، ولا فاصلَ في الإيداع يرجّح.
و«العالمين» تبلغ خمسةً: علم · علن · عمن · عين · لعن — **والصوابُ فيها وأربعةٌ
معه، والقرارُ لا يميّزه**.

`AND_A_RELATION_IS_NOT_A_RANDOM_VARIABLE`: وهذا هو الفرقُ الحاسم: المبرهنةُ
تحتاج **دالّةً** π: Σ → Λ لتُعرَّف عليها المتغيّراتُ والمعلوماتُ والتكتيل.
وعلاقةٌ بمتوسّطٍ يزيد على الواحد **لا تُعرِّف متغيّرًا عشوائيًّا**، فلا
I(X;Y) ولا خللَ كيمني–سنل عليها. فالحاجزُ **لم يُرفَع بالتوقيع**؛ زُحزِح:
صار الناقصُ **فاصلَ ترجيحٍ معلنًا**، لا إسقاطًا معدومًا.

`AND_TWO_HUNDRED_AND_THIRTY_ROOTS_HAVE_NO_ANCHOR_IN_THE_FIRST_DECISION`:
و٢٣٠ جذرًا من ٤٬٥٦٥ (٠٫٠٥٠٤) **كلُّ حروفها من الزوائد** (سأل، أمن، موت…)،
فليس في الكلمة المبنيّةِ منها حرفٌ **يمتنع حذفُه** — والقرارُ الأوّلُ يميّز
بالامتناع، فلا مرساةَ له فيها. وهذا ليس امتناعَ بلوغٍ (القرارُ الثاني قد
يبلغها)، بل **انعدامُ دليلٍ في القرار الأوّل** — ويُصنَّف كذلك لا أشدّ.

`THE_VACANCY_IS_RECLASSIFIED_NOT_FILLED`: فتُنقَل الطبقةُ الاشتقاقيّةُ من
`UNREACHABLE` إلى **`UNCLASSIFIED`**: الإسقاطُ حاضرٌ ويُشغَّل ويُقرأ، ولا
يصلح **مستوًى** حتّى يُودَع فاصلُه. وسجلُّ `test_layer_induction_run` يبقى
كما كُتِب: **السجلُّ لا يُعدَّل بعد الحدث** — وهذا موضعُه الجديد لا تصحيحُه.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_root_projection.py"

pytestmark = requires_corpus

TOTAL = 78_245
EMPTY = 40_256
SINGLE = 23_884
MANY = 14_105
ROOTS = 4_565
UNANCHORED = 230


def _module() -> object:
    spec = importlib.util.spec_from_file_location("run_root_projection", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _survey() -> tuple[Counter[int], frozenset[str], frozenset[str]]:
    reader = _module()
    roots = reader.read_roots(reader.ROOT_TABLE)  # type: ignore[attr-defined]
    tokens = reader.read_tokens(CORPUS)  # type: ignore[attr-defined]
    return (
        reader.survey(tokens, roots),  # type: ignore[attr-defined]
        roots,
        reader.unanchored(roots),  # type: ignore[attr-defined]
    )


def test_the_run_reproduces_the_recorded_counts() -> None:
    """السجلُّ يُعاد اشتقاقُه من الشيفرة لا يُنقَل."""

    spread, roots, bare = _survey()
    assert sum(spread.values()) == TOTAL
    assert spread[0] == EMPTY
    assert spread[1] == SINGLE
    assert sum(spread.values()) - spread[0] - spread[1] == MANY
    assert len(roots) == ROOTS
    assert len(bare) == UNANCHORED


def test_the_projection_is_not_a_function_on_a_third_of_what_it_reaches() -> None:
    """١٤٬١٠٥ توكنًا بأكثرَ من جذر — ولا فاصلَ في الإيداع."""

    spread, _, _ = _survey()
    reached = SINGLE + MANY
    assert Fraction(MANY, TOTAL) > Fraction(18, 100)
    assert Fraction(MANY, reached) > Fraction(37, 100)
    assert max(spread) >= 5  # وبعضُ التوكنات تبلغ العشرات
    assert spread[2] + spread[3] + spread[4] == 12_513


def test_the_reached_roots_include_the_right_one_and_four_others() -> None:
    """«العالمين» → علم وأربعةٌ معها، والقرارُ لا يرجّح."""

    reader = _module()
    roots = reader.read_roots(reader.ROOT_TABLE)  # type: ignore[attr-defined]
    reached = reader.candidates("العالمين", roots)  # type: ignore[attr-defined]
    assert "علم" in reached
    assert len(reached) == 5
    assert reached >= {"علم", "علن", "عين", "لعن"}


def test_unanchored_roots_are_classified_not_declared_impossible() -> None:
    """٢٣٠ جذرًا بلا حرفٍ يمتنع حذفُه — انعدامُ دليلٍ لا امتناعُ بلوغ."""

    _, roots, bare = _survey()
    assert Fraction(len(bare), len(roots)) < Fraction(6, 100)
    assert {"سأل", "أمن", "موت"} <= bare
    reader = _module()
    for root in bare:
        assert set(root) <= reader.AUGMENTS  # type: ignore[attr-defined]


def test_the_second_decision_names_a_table_the_deposit_does_not_carry() -> None:
    """«بالجدول الموروث» مذكورٌ والجدولُ غيرُ محمول — فالقرارُ غيرُ مشغَّل."""

    deposit = REPOSITORY / "deposits" / "projection_specs.md"
    text = deposit.read_text(encoding="utf-8")
    assert "الجدول الموروث" in text  # مُسمًّى
    for letter in ("قال ⟵ قول", "باع ⟵ بيع"):
        assert letter not in text  # وغيرُ محمول: لا سطرَ ردٍّ واحدًا
    assert "معتلّ معلَّق" in text  # والرايةُ مُعلَنةٌ بدلَ التخمين
