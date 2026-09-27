"""أين بايتاتُ المدوّنة في هذه الشجرة؟ — تُسأل البصمةُ لا الاسم.

**العطلُ الذي عالجه هذا الملفّ**: أودِع صاحبُ المستودع بايتاتِ المصحف في
**جذر الشجرة** (`quran-simple-enhanced.txt`)، وهي مطابقةٌ للسجلّ المُجمَّد
بايتةً بايتة. وكانت الفحوصُ كلُّها تسأل عن `corpora/…` وحدَها — وهو مسارٌ
**مُستبعَدٌ من التتبّع** — فتتخطّى بسببٍ نصُّه «غيرُ مستقبَلةٍ في هذه
الشجرة»، **وهو نصٌّ صار كاذبًا**: البايتاتُ حاضرةٌ ومتتبَّعة.

`A_SKIP_WHOSE_STATED_CAUSE_IS_FALSE_IS_WORSE_THAN_A_FAILURE`: وتخطٍّ يُعلِن
سببًا غيرَ قائمٍ أسوأُ من سقوطٍ: السقوطُ يُرى ويُصلَح، وهذا **يُقرأ انضباطًا**
ويُخفي أنّ القياسَ لم يجرِ على مادّةٍ موجودة.

`THE_HOLDERS_ARE_DECLARED_AND_THE_DIGEST_DECIDES`: فالحواملُ مُعلَنةٌ في
`tools/corpus_seal.py`، والمقبولُ منها ما طابقت بصمتُه `37633090…`. فملفٌّ
باسم المدوّنة ببايتاتٍ أخرى **لا يفتح البوّابة**، وملفٌّ ببايتاتها في غير
موضعها **يفتحها** — والاسمُ عنوانٌ والبصمةُ دليل.

`AND_A_SECOND_TEXT_NEEDS_A_SECOND_GATE`: ومتنٌ ثانٍ يُقرَأ ههنا وليس
المدوّنة: جدولُ المقاييس `maqayis_by_root_csv_999.csv` — خمسةُ ميغابايتٍ
ونصف، **متنٌ لا شفرة، فلم يُنقَل**. وكانت بوّابتُه **قائمةً مكتوبةً** في
`conftest.py` تُسمّي أربعةً وعشرين فحصًا بأسمائها، **فلم تنمُ مع الشجرة**:
أُضيف `test_root_projection_run` بعدها ولم يُضَفّ إليها، فسقط أربعةُ فحوصٍ
بـ`FileNotFoundError` على نسخةٍ نظيفةٍ — **والعطلُ ٢٨ بنصّه**. فالشرطُ
ههنا **بجانب ما يشترطه** لا في قائمةٍ مركزيّة، ويحرسه
`tests/arabic/test_root_table_gates_are_declared.py`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
TOOL = REPOSITORY / "tools" / "corpus_seal.py"


def _tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("corpus_seal", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SEAL_TOOL = _tool()
DECLARED_HOLDERS: tuple[str, ...] = SEAL_TOOL.DECLARED_HOLDERS
HOLDER: Path | None = SEAL_TOOL.holder_in(REPOSITORY)
HELD: bool = HOLDER is not None

CORPUS: Path = HOLDER if HOLDER is not None else REPOSITORY / DECLARED_HOLDERS[-1]
"""بايتاتُ المدوّنة إن حضرت؛ وإلّا فعنوانُ الاستقبال ليُطبَع في السبب."""

ABSENT = "بايتاتُ المدوّنة المُجمَّدة (37633090…) ليست في حاملٍ مُعلَن: " + "، ".join(
    DECLARED_HOLDERS
)

requires_corpus = pytest.mark.skipif(not HELD, reason=ABSENT)
"""بوّابةٌ واحدةٌ لكلّ فحصٍ يقيس المدوّنة؛ وسببُ تخطّيه يُسمّي الحوامل."""

ROOT_TABLE: Path = REPOSITORY / "maqayis_by_root_csv_999.csv"
"""جدولُ المقاييس — متنٌ لم يُنقَل؛ وحضورُه يُسأل ولا يُفترَض."""

TABLE_ABSENT = f"متنٌ لم يُنقَل: {ROOT_TABLE.name} — نُقِلت الشفرةُ وحدَها"

requires_root_table = pytest.mark.skipif(not ROOT_TABLE.is_file(), reason=TABLE_ABSENT)
"""بوّابةُ كلّ فحصٍ يقرأ جدولَ المقاييس — **توضَع عند الفحص لا في قائمة**."""
