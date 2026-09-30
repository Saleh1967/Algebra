"""حارسُ «مدى الإحاطة».

**العطلُ الذي يحرسه**: وثيقةٌ تقيس قدرةَ الشجرةِ على ضبطِ نفسها
**هي أخطرُ ما يُجمَّل**. فعددٌ يُطري كاتبَه يُطبَع ولا يُراجَع، إذ من
ذا يراجع شهادةً في مصلحته؟

فهذه الفحوصُ تُثبّت أربعةً:

١. أنّ العددَ المُشتَقَّ من **بنيةِ الشجرة** يصالح عددًا قِيس في
   **بيئةٍ أخرى بأداةٍ أخرى**: ٣٢ متخطًّى طبعها Runner في الطلب ٦١.
   **وهذا هو الشرطُ الحامل**: قياسٌ واحدٌ لا يُكذِّب نفسَه.
٢. أنّ قراءةَ الشرطِ بـ`ast` لا بنافذةِ محارف — **والحالةُ المُكذِّبةُ
   مُجرَّبة**: النافذةُ تُعطي ٤٢٦ والعقدةُ تُعطي ٧.
٣. أنّ عدَّ الردِّ بنمطِ الاسمِ **يُسمّى حدًّا أدنى** لا عددًا، وأنّ
   الفجوةَ بينه وبين المُعلَنِ مطبوعةٌ لا مطويّة.
٤. أنّ المكتوبَ في `docs/` يطابق المولَّدَ حسابًا.
"""

from __future__ import annotations

import ast
import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[2]
GENERATOR: Final[Path] = REPOSITORY / "tools" / "write_reach_audit.py"
PAPER: Final[Path] = REPOSITORY / "docs" / "مدى-الإحاطة.md"

# ما طبعه Runner في الطلب ٦١ — **قياسٌ في بيئةٍ أخرى، لا رقمٌ مُختار**.
RUNNER_SKIPPED: Final[int] = 32


def _loaded() -> ModuleType:
    spec = importlib.util.spec_from_file_location("write_reach_audit", GENERATOR)
    assert spec is not None and spec.loader is not None
    found = importlib.util.module_from_spec(spec)
    sys.modules["write_reach_audit"] = found
    spec.loader.exec_module(found)
    return found


AUDIT: Final[ModuleType] = _loaded()


def test_the_structural_count_reconciles_with_what_another_machine_printed() -> None:
    """**الشرطُ الحامل**: بنيةُ الشجرةِ تُعطي ما طبعته بيئةٌ أخرى.

    فالعددُ ههنا مُشتَقٌّ من `ast` ومن `git ls-files`، والعددُ ثَمَّ
    مطبوعٌ من `pytest -rs` على ubuntu بـgit 2.55. **ولو تفارقا لكان
    أحدُ القياسين خاطئًا، ولا يُعرَف أيُّهما بلا ثالث.**
    """

    counted = AUDIT.census()
    assert counted["المجموع"] == RUNNER_SKIPPED
    assert counted["متنٌ غائب"] == counted["بالمُزيِّن"] + counted["بالقائمة"]
    assert counted["بالمُزيِّن"] == 7
    assert counted["بالقائمة"] == 24
    assert counted["تُخطّى في كلّ بيئة"] == 1


def test_only_the_untracked_corpus_makes_a_gate_unreachable() -> None:
    """بوّابةٌ على ملفٍّ متعقَّبٍ تُنال؛ وعلى غيرِ متعقَّبٍ لا تُنال.

    ويُقاس الطرفان: أنّ المدوّنةَ متعقَّبةٌ فبوّابتُها تعمل، وأنّ جدولَ
    المقاييسِ غيرُ متعقَّبٍ فبوّابتُه لا تعمل. **فلو صار متعقَّبًا يومًا
    سقط هذا الفحصُ ولزم تصحيحُ العدد** — وذلك صوابٌ لا عطل.
    """

    assert AUDIT.tracked("quran-simple-enhanced.txt")
    assert not AUDIT.tracked("maqayis_by_root_csv_999.csv")
    blocked = {one.name for one in AUDIT.unreachable(AUDIT.merged())}
    assert blocked == {"needs_roots", "requires_root_table"}


def test_the_condition_is_read_as_a_node_not_a_character_window() -> None:
    """الحالةُ المُكذِّبة: النافذةُ تنساب إلى التعريفِ الذي يليها.

    وهذا عطلٌ وقع فعلًا: قرأتُ الشرطَ بنافذةِ ٤٠٠ محرفٍ بعد اسمِ
    البوّابة، **فنسبت إلى `requires_corpus` ملفًّا ليس لها** وأعطت
    ٤٢٦ بدلَ ٧. ويُعاد اصطناعُ الخطأِ ههنا **فيُرى الفرقُ مقيسًا**.
    """

    where = REPOSITORY / "tests" / "arabic" / "frozen_corpus.py"
    body = where.read_text(encoding="utf-8")
    named = re.compile(r'"([A-Za-z0-9_.\-]+\.(?:csv|txt|json|md))"')
    head = r"^requires_corpus\s*=\s*pytest\.mark\.skipif\("
    hit = re.search(head, body, re.MULTILINE)
    assert hit is not None
    # ١. النافذةُ تقتنص ملفًّا ليس للشرط
    window = body[hit.start() : hit.start() + 400]
    assert "maqayis_by_root_csv_999.csv" in named.findall(window)
    # ٢. والعقدةُ لا تقتنصه
    gate = next(one for one in AUDIT.merged() if one.name == "requires_corpus")
    assert gate.files == ()
    assert gate.condition == "not HELD"
    # ٣. والفرقُ في العدِّ مطبوعٌ في الوثيقةِ لا مسكوتٌ عنه
    written = PAPER.read_text(encoding="utf-8")
    assert "٤٢٦" in written and "نافذةُ محارفَ ليست قراءةً" in written


def test_the_refusal_count_is_named_a_lower_bound_not_a_count() -> None:
    """عدٌّ بنمطِ اسمٍ يُسمّى حدًّا أدنى — **والفجوةُ تُطبَع**."""

    by_name, by_text = AUDIT.refusing()
    assert by_name > by_text > 0
    written = PAPER.read_text(encoding="utf-8")
    assert "**حدٌّ أدنى**" in written
    assert "هو الفجوة" in written
    # وكلُّ نمطٍ معدودٍ مُعلَنٌ في الوثيقةِ باسمه
    for one in AUDIT.REFUSAL:
        assert f"`{one}`" in written


def test_every_counted_gate_is_read_from_a_real_skipif_node() -> None:
    """ولا بوّابةَ في الجدولِ إلّا ولها عقدةُ `skipif` في الشجرة."""

    for gate in AUDIT.merged():
        first = gate.where.split(" · ")[0]
        tree = ast.parse(
            (REPOSITORY / first).read_text(encoding="utf-8"), filename=first
        )
        found = [
            node
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                one.id == gate.name for one in node.targets if isinstance(one, ast.Name)
            )
            and AUDIT._condition_of(node) is not None
        ]
        assert len(found) == 1, gate.name
        assert ast.unparse(AUDIT._condition_of(found[0])) == gate.condition


def test_the_written_audit_equals_the_generated_one() -> None:
    """وثيقةٌ تخالف شجرتَها تُرَدّ."""

    assert PAPER.read_text(encoding="utf-8") == AUDIT.render()
