"""بوّابةُ Runner تُحرَس كما تُحرَس الشجرة — **وآخرُ سطحٍ بلا حارسٍ يُنصَب**.

**العطلُ الذي يحرسه**: `.github/workflows/ci.yml` هو **البوّابةُ التي
تحرس كلَّ شيءٍ ولا شيءَ يحرسها**. بحثتُ في `tests/` و`tools/` كلِّها فلم
أجد فحصًا واحدًا يقرؤها. فلو حُذِفت منها خطوةُ `mypy`، أو بُدِّلت
`"3.10"` إلى `3.10` بلا اقتباس، أو أُسقِط `ruff format --check`،
**لمرّ ذلك على ألفَي فحصٍ بلا شكوى** — لأنّ الفحوصَ تعمل بما تقوله هي.

**وهذا من جنس العطل ٢٧**: كان `README.md` أشدَّ ملفٍّ يُقرَأ وأقلَّه
حراسة، فصار مولَّدًا ومفحوصًا. **و`ci.yml` اليوم في موضعه**، وخرج من كلّ
شبكةٍ نُصِبت لأنّه **وصفٌ لا عمل**: لو كان بايثون لقرأه فحصُ الحزمة مع
إخوته.

`THE_TWO_GATES_MUST_AGREE_OR_THE_DIVERGENCE_IS_NAMED`: **والقياسُ كشف
خلافًا قائمًا**: `tools/verify.sh` يُشغّل `mypy --strict src tools`،
و`ci.yml` يُشغّل `mypy src/algebra src/hawk_dove` — **فـCI أضعفُ في
محورين**: بلا `--strict`، وبنطاقٍ لا يبلغ `tools/`. فخطأُ نوعٍ في
`tools/` يمرُّ على Runner ويسقط محلّيًّا. **ولا يُخفى ههنا**: يُسجَّل في
`DECLARED` بسببه، **وما زاد عليه يُرَدّ**. فالتسجيلُ سقفٌ يمنع الزيادة،
لا إذنٌ بها.

`AND_THE_READING_IS_TEXT_NOT_YAML`: **وحدُّه مُعلَن**: يقرأ الملفَّ
**نصًّا** لا بمفسّر YAML — إذ لا مفسّرَ في المسموح، ولا يُستورَد تابعٌ
خارجيٌّ لأجل فحص. **فلا يحرس صحّةَ YAML نحويًّا**، ولا يمنع مفتاحًا
مجهولًا يُهمِله Runner صامتًا. **يحرس حضورَ البوّابات وثباتَ صياغتها.**
"""

from __future__ import annotations

import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
WORKFLOW = REPOSITORY / ".github" / "workflows" / "ci.yml"
LOCAL = REPOSITORY / "tools" / "verify.sh"

GATES = ("pytest", "ruff check", "ruff format", "mypy")

DECLARED: dict[str, tuple[str, str, str]] = {
    "mypy": (
        "mypy --strict src tools",
        "mypy src/algebra src/hawk_dove",
        "بوّابةُ Runner أضعفُ: بلا --strict وبنطاقٍ لا يبلغ tools/ — "
        "فخطأُ نوعٍ في tools يمرُّ عليها ويسقط محلّيًّا",
    ),
    "pytest": (
        "pytest -q",
        "pytest",
        "خلافُ إسهابٍ لا اختيار: `-q` يُقصِّر المخرَج ولا يُغيِّر ما "
        "يُجمَع ولا ما يُشغَّل — **فالمقيسُ واحدٌ والمطبوعُ مختصر**",
    ),
}
"""خلافٌ قائمٌ بين البوّابتين، **مُسمًّى بطرفيه وسببه** — وما زاد يُرَدّ."""


def _workflow() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def runs(text: str) -> list[str]:
    """أوامرُ `- run:` مرتَّبةً كما كُتِبت — والتعليقاتُ لا تدخل."""

    return [
        one.strip() for one in re.findall(r"^\s*-\s*run:\s*(.+)$", text, re.MULTILINE)
    ]


def local_gates() -> list[str]:
    """أوامرُ البوّابة المحلّيّة — تُقرَأ من `verify.sh` لا تُكتَب ههنا."""

    body = LOCAL.read_text(encoding="utf-8")
    return [
        one.strip() for one in re.findall(r'^"\$PY"\s+-m\s+(.+)$', body, re.MULTILINE)
    ]


def kind_of(command: str) -> str | None:
    """صنفُ البوّابة من أمرها — ولا تُخمَّن، تُطابَق بأوّل كلمتين."""

    for gate in GATES:
        if command.startswith(gate):
            return gate
    return None


def test_the_workflow_exists_and_is_read_as_text() -> None:
    """الملفُّ حاضرٌ ويُقرَأ — فلا حارسَ على غائب."""

    assert WORKFLOW.is_file()
    assert LOCAL.is_file()
    assert _workflow().startswith("name: CI")


def test_every_gate_is_present_in_both_files() -> None:
    """أربعُ بوّاباتٍ في الملفّين كليهما — ولا بوّابةَ تسقط من أحدهما."""

    on_runner = {kind_of(one) for one in runs(_workflow())} - {None}
    here = {kind_of(one) for one in local_gates()} - {None}
    assert set(GATES) <= on_runner, sorted(set(GATES) - on_runner)
    assert set(GATES) <= here, sorted(set(GATES) - here)


def test_a_removed_gate_is_refused() -> None:
    """الصورةُ المكذِّبة: تُحذَف خطوةٌ في نسخةٍ بالذاكرة **فتُرَدّ**."""

    for gate in GATES:
        hurt = "\n".join(
            one for one in _workflow().splitlines() if f"run: {gate}" not in one
        )
        missing = set(GATES) - ({kind_of(one) for one in runs(hurt)} - {None})
        assert gate in missing, gate


def test_the_divergence_between_the_gates_is_declared_not_silent() -> None:
    """وكلُّ خلافٍ في الوسائط **مُسجَّلٌ بطرفيه** — وما زاد عليه يُرَدّ."""

    on_runner = {kind_of(one): one for one in runs(_workflow()) if kind_of(one)}
    here = {kind_of(one): one for one in local_gates() if kind_of(one)}
    found: dict[str, tuple[str, str]] = {}
    for gate in GATES:
        mine, theirs = here[gate], on_runner[gate]
        if mine.split() != theirs.split():
            found[gate] = (mine, theirs)
    assert set(found) == set(DECLARED), (sorted(found), sorted(DECLARED))
    for gate, (mine, theirs) in found.items():
        said_mine, said_theirs, why = DECLARED[gate]
        assert mine == said_mine, (gate, mine)
        assert theirs == said_theirs, (gate, theirs)
        assert len(why) > 40, gate


def test_the_python_version_is_quoted_against_the_float_trap() -> None:
    """`"3.10"` بين اقتباسين — فبلا اقتباسٍ يقرؤها YAML عائمًا `3.1`."""

    found = re.search(r"python-version:\s*(\S+)", _workflow())
    assert found is not None
    value = found.group(1)
    assert value.startswith('"') and value.endswith('"'), value
    assert value.strip('"').count(".") == 1
    # والمصيدةُ بعينها: بلا اقتباسٍ يصير النصُّ عددًا فيسقط الجزءُ الأخير
    assert str(float(value.strip('"'))) != value.strip('"')


def test_the_workflow_runs_on_pull_requests_not_only_on_main() -> None:
    """يعمل على الطلبات — **وبه صار «CI أخضرُ قبل الدمج» ممكنًا**."""

    text = _workflow()
    assert re.search(r"^\s*pull_request:\s*$", text, re.MULTILINE)
    assert re.search(r"^\s*branches:\s*\[main\]\s*$", text, re.MULTILINE)
    assert re.search(r"^\s*contents:\s*read\s*$", text, re.MULTILINE)


def test_no_step_is_added_without_being_counted() -> None:
    """وعددُ الخطوات مُثبَت — فلا خطوةٌ تُدَسّ ولا تُحذَف صامتة."""

    text = _workflow()
    assert len(runs(text)) == 5
    assert len(re.findall(r"^\s*-\s*uses:\s*(\S+)", text, re.MULTILINE)) == 2
    assert "actions/checkout@v4" in text
    assert "actions/setup-python@v5" in text


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوب: نصٌّ لا YAML، وحضورُ البوّابات لا صحّةُ الوصف."""

    here = Path(__file__).read_text(encoding="utf-8")
    assert "`AND_THE_READING_IS_TEXT_NOT_YAML`" in here
    assert "**فلا يحرس صحّةَ YAML نحويًّا**" in here
    assert "`THE_TWO_GATES_MUST_AGREE_OR_THE_DIVERGENCE_IS_NAMED`" in here
