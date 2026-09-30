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

`ONE_GATE_IN_ONE_FILE_LEAVES_NO_ROOM_FOR_DIVERGENCE`: **وقد كان
الخلافُ قائمًا فأُزيل**. سُجِّل في الدفعة السابقة أنّ mypy على Runner
«أضعفُ في محورين: بلا `--strict` وبنطاقٍ لا يبلغ `tools/`» —
**والشقُّ الأوّلُ من السبب كان خاطئًا** (العطل ٣٥): `pyproject` فيه
`strict = true`، فالفحصُ صارمٌ في الحالين. **والخلافُ نطاقٌ وحدَه**:
٢٨ ملفًّا على Runner مقابل ١٠٧ محلّيًّا.

**والإصلاحُ لم يكن ترقيعَ سطر**: صار Runner يُشغِّل `tools/verify.sh`
**نفسَه** بمفسّره عبر `PY`. **فالبوّابةُ ملفٌّ واحدٌ لا ملفّان**، ولا
يبقى موضعٌ لخلافٍ يُسجَّل — فجدولُ `DECLARED` **خالٍ**، وامتلاؤه يعني
عودةَ الازدواج.

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

DECLARED: dict[str, tuple[str, str, str]] = {}
"""خلافاتٌ باقيةٌ بين البوّابتين — **خالٍ بعد التوحيد**، وامتلاؤه ازدواج."""


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


def test_the_runner_invokes_the_one_gate_script() -> None:
    """Runner يُشغِّل `tools/verify.sh` نفسَه — **فالبوّابةُ ملفٌّ واحد**."""

    text = _workflow()
    assert "bash tools/verify.sh" in text, runs(text)
    assert "PY=python" in text, "المفسّرُ لا يُمرَّر، فالبوّابةُ تسقط على Runner"
    assert set(GATES) <= {kind_of(one) for one in local_gates()} - {None}


def test_a_removed_gate_is_refused() -> None:
    """الصورةُ المكذِّبة: تُحذَف بوّابةٌ من `verify.sh` **فتُرَدّ**."""

    body = LOCAL.read_text(encoding="utf-8")
    for gate in GATES:
        hurt = "\n".join(one for one in body.splitlines() if gate not in one)
        found = {
            kind_of(one.strip())
            for one in re.findall(r'^"\$PY"\s+-m\s+(.+)$', hurt, re.MULTILINE)
        } - {None}
        assert gate not in found, gate


def test_no_gate_is_spelled_twice_so_no_divergence_can_exist() -> None:
    """ولا بوّابةَ مكتوبةً مرّتين — **فالازدواجُ ممتنعٌ بناءً لا محروسًا**."""

    text = _workflow()
    spelled = {kind_of(one) for one in runs(text)} - {None}
    assert spelled == set(), sorted(spelled)
    assert DECLARED == {}, DECLARED


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
    assert len(runs(text)) == 2
    assert len(re.findall(r"^\s*-\s*uses:\s*(\S+)", text, re.MULTILINE)) == 2
    assert "actions/checkout@v4" in text
    assert "actions/setup-python@v5" in text


def test_the_skip_reasons_are_printed_so_a_vacancy_is_classified() -> None:
    """`-rs` في البوّابة — **فالفجوةُ تُسمّى ولا تُعَدّ وحدَها**.

    والعطلُ الذي قاسه الطلبُ ٦٠: Runner يتخطّى ٣٦ والقرصُ يتخطّى واحدًا،
    ولا يُعرَف من السجلِّ أيُّها ولا لماذا. **وفجوةٌ معدودةٌ بلا اسمٍ
    فجوةٌ مطويّةٌ بعدد.**

    والصورةُ المكذِّبة: يُحذَف العَلَمُ في نسخةٍ في الذاكرة **فتُرَدّ**.
    """

    body = LOCAL.read_text(encoding="utf-8")
    found = [one for one in local_gates() if kind_of(one) == "pytest"]
    assert len(found) == 1, found
    assert "-rs" in found[0].split(), found[0]
    # ولو حُذِف العَلَمُ لَما بقي في الأمرِ ما يطبع السبب
    hurt = body.replace("pytest -q -rs", "pytest -q")
    loose = re.findall(r'^"\$PY"\s+-m\s+(pytest.+)$', hurt, re.MULTILINE)
    assert loose == ["pytest -q"], loose
    assert "-rs" not in loose[0].split()


def test_the_checkout_is_not_shallow_or_the_history_guards_vanish() -> None:
    """`fetch-depth: 0` — **وبلا هذا يسقط حارسُ سلسلةِ الأختام كلُّه**.

    فأربعةُ فحوصٍ مشروطةٌ بنفيِ الضحالة، وهي التي تُثبِت أنّ الختمَ سبقَ
    التشغيل. **وهي حجّةُ المنهجِ كلِّها**، فكانت تُتخطّى على البوّابةِ
    التي تحكم الدمجَ وحدَها.

    ويقيس هذا الفحصُ شيئين لا واحدًا: أنّ العمقَ صفرٌ في الوصف، **وأنّ
    الأربعةَ ما زالت موجودةً ومشروطةً بالضحالة** — فلو حُذِف شرطُها
    يومًا لَصار هذا الفحصُ يحرس عمقًا لا يحرسه أحد.
    """

    text = _workflow()
    found = re.search(r"^\s*fetch-depth:\s*(\S+)\s*$", text, re.MULTILINE)
    assert found is not None, "الاستنساخُ ضحلٌ افتراضًا، فالعمقُ يُكتَب صريحًا"
    assert found.group(1) == "0", found.group(1)
    # وموضعُه تحتَ `checkout` لا تحتَ `setup-python`
    before = text[: found.start()]
    assert before.rfind("actions/checkout@v4") > before.rfind("actions/setup-python@v5")

    guarded = {
        "tests/algebra/test_seal_chain.py": 2,
        "tests/algebra/test_message_guard.py": 2,
    }
    for name, how_many in guarded.items():
        body = (REPOSITORY / name).read_text(encoding="utf-8")
        assert "pytest.mark.skipif(" in body and "hallow" in body, name
        assert body.count("@needs_history") == how_many, name


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوب: نصٌّ لا YAML، وحضورُ البوّابات لا صحّةُ الوصف."""

    here = Path(__file__).read_text(encoding="utf-8")
    assert "`AND_THE_READING_IS_TEXT_NOT_YAML`" in here
    assert "**فلا يحرس صحّةَ YAML نحويًّا**" in here
    assert "`ONE_GATE_IN_ONE_FILE_LEAVES_NO_ROOM_FOR_DIVERGENCE`" in here
    assert "**والشقُّ الأوّلُ من السبب كان خاطئًا**" in here
