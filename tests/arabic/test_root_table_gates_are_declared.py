"""كلُّ فحصٍ يقرأ متنًا لم يُنقَل **يحمل بوّابتَه** — العطل ٢٨.

**ما كان**: بوّابةُ جدول المقاييس **قائمةٌ مكتوبةٌ** في `conftest.py` تُسمّي
أربعةً وعشرين فحصًا **بأسمائها العشرينيّة**. وأُضيف
`test_root_projection_run` بعدها ولم يُضَفّ إليها — **فلم تنمُ القائمةُ مع
الشجرة**. وعلى نسخةٍ نظيفةٍ (وهي حالُ CI) سقطت أربعةُ فحوصٍ بـ
`FileNotFoundError`، **لا بتخطٍّ مُصنَّف**.

`A_HAND_KEPT_LIST_IS_NOT_A_GATE_BUT_A_MEMORY`: وهذا **العطلُ ٢٧ في صورةٍ
ثانية**: الحراسةُ تتبع **ما كُتِب في قائمةٍ** لا **ما يقرؤه الفحصُ فعلًا**.
فمن نسي السطرَ مرَّ، **والنسيانُ لا يُردّ بالنيّة**.

`AND_THE_CONDITION_BELONGS_BESIDE_WHAT_IT_CONDITIONS`: فالشرطُ يُوضَع **عند
الفحص** (`@requires_root_table`) لا في مركزٍ بعيد — فمن كتب فحصًا يقرأ
المتنَ رأى البوّابةَ في جاره، ومن لم يرَها **ردَّه هذا الفحص**.

`AND_ITS_LIMIT_IS_DECLARED`: **ولا يُبرهن هذا المانعُ أنّ فحصًا يقرأ
المتنَ** — يقرأ الأسماءَ في المتن لا مسارَ التنفيذ. فوحدةٌ تقرأ الجدولَ
باسمٍ غيرِ مذكورٍ في متنها تمرُّ عليه. **فهو يردُّ إغفالَ البوّابة عند من
ذكر المتن، لا كلَّ إغفال.**
"""

from __future__ import annotations

from pathlib import Path

from frozen_corpus import ROOT_TABLE, requires_root_table

HERE = Path(__file__).resolve().parent
CONFTEST = HERE / "conftest.py"
TABLE = ROOT_TABLE.name

MINE = Path(__file__).name
"""هذا الملفُّ يذكر المتنَ ليحرسه، فيُستثنى من نفسه — ولا يُستثنى غيرُه."""

DECLARED_BY_THE_CENTRAL_LIST: frozenset[str] = frozenset(
    {
        "test_composition_closure_replication.py",
        "test_interaction_complex_lemmas.py",
        "test_movement_workbook_crosscheck.py",
        "test_slot_rights_algebra.py",
        "test_word_schema_falsification.py",
    }
)
"""ما بوّابتُه في القائمة المركزيّة بعدُ — **أربعةٌ وعشرون فحصًا**، ولا تنمو.

وتُسمّى ههنا كي **يُرى بقاؤها**: هي الصورةُ القديمةُ من البوّابة، ومن أضاف
إليها فحصًا جديدًا **أعاد العطل ٢٨**. والجديدُ يحمل بوّابتَه بجانبه.
"""


def _mentions_the_table(text: str) -> bool:
    return TABLE in text or "ROOT_TABLE" in text


def test_every_module_that_names_the_table_gates_on_it() -> None:
    """وحدةٌ تذكر المتنَ ولا تشترطه **تُردّ** — لا تُحمَل على الانضباط."""

    ungated: list[str] = []
    for path in sorted(HERE.glob("test_*.py")):
        if path.name == MINE:
            continue
        text = path.read_text(encoding="utf-8")
        if not _mentions_the_table(text):
            continue
        gated = "requires_root_table" in text or (
            "skipif" in text and "ROOT_TABLE" in text
        )
        if not (gated or path.name in DECLARED_BY_THE_CENTRAL_LIST):
            ungated.append(path.name)
    assert not ungated, ungated


def test_the_run_that_fell_on_a_clean_tree_now_carries_its_gate() -> None:
    """الأربعةُ التي سقطت بـ`FileNotFoundError` صارت مشروطةً بحضور المتن."""

    text = (HERE / "test_root_projection_run.py").read_text(encoding="utf-8")
    fell = (
        "test_the_run_reproduces_the_recorded_counts",
        "test_the_projection_is_not_a_function_on_a_third_of_what_it_reaches",
        "test_the_reached_roots_include_the_right_one_and_four_others",
        "test_unanchored_roots_are_classified_not_declared_impossible",
    )
    for one in fell:
        head = text.index(f"def {one}(")
        assert "@requires_root_table" in text[max(0, head - 60) : head], one
    assert text.count("@requires_root_table") == len(fell)


def test_the_test_that_needs_no_table_is_not_gated() -> None:
    """ولا يُبوَّب ما لا يقرأ المتنَ — **فالتخطّي الزائدُ يُخفي فحصًا عاملًا**.

    والخامسُ في تلك الوحدة يفحص أنّ الإيداعَ **يُسمّي جدولًا لا يحمله** —
    وذلك يُقرَأ من نصّ الإيداع، فيعمل حضر المتنُ أو غاب.
    """

    text = (HERE / "test_root_projection_run.py").read_text(encoding="utf-8")
    spared = "test_the_second_decision_names_a_table_the_deposit_does_not_carry"
    head = text.index(f"def {spared}(")
    assert "@requires_root_table" not in text[max(0, head - 60) : head]
    assert "pytestmark = requires_corpus" in text


def test_the_central_list_is_named_so_its_staleness_is_visible() -> None:
    """القائمةُ المركزيّةُ باقيةٌ، **وبقاؤها يُرى** — ولا تُضاف إليها زيادة."""

    written = CONFTEST.read_text(encoding="utf-8")
    assert "NEEDS_THE_ROOT_TABLE" in written
    for name in DECLARED_BY_THE_CENTRAL_LIST:
        assert name in written, name
    listed = written.count("test_root_projection_run.py::")
    assert listed == 0, "الجديدُ يحمل بوّابتَه، ولا يُضاف إلى القائمة"


def test_the_gate_is_a_skip_with_a_named_cause() -> None:
    """والتخطّي يُسمّي سببَه — **خلوٌّ يُصنَّف ولا يُصفَّر**."""

    mark = requires_root_table
    assert mark.kwargs["reason"].startswith("متنٌ لم يُنقَل")
    assert TABLE in mark.kwargs["reason"]


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوبٌ في متنه — يردُّ إغفالَ من ذكر المتنَ لا كلَّ إغفال."""

    text = Path(__file__).read_text(encoding="utf-8")
    assert "`AND_ITS_LIMIT_IS_DECLARED`" in text
    assert "**ولا يُبرهن هذا المانعُ أنّ فحصًا يقرأ" in text
    assert "لا كلَّ إغفال" in text
