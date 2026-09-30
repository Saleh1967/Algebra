"""سلسلةُ الأختام: الترتيبُ مشدودٌ، **وسبقُ الختم على سجلِّه مقيسٌ لا مقولٌ**.

**الدعوى التي كانت تُقال ولا تُقاس**: كُتِب في كلّ دفعةِ دمجٍ من هذه
الجلسة «ترتيبُ الختم قبل تشغيله شاهدٌ في التاريخ، والكبسُ يطويه». **وهي
صحيحةٌ ولم يكن يمسكها فحص**: لا شيءَ في الشجرة كان يقرأ `git` فيتحقّق أنّ
دفعةَ الختم سبقت دفعةَ سجلِّ تشغيله. **فالدعوى كانت مُحالةً إلى التاريخ
ولا أحدَ يسأله.**

وههنا يُسأل: لكلّ ختمٍ **مرساةٌ** — أوّلُ دفعةٍ أدخلت بصمتَه — ولسجلِّه
مرساةٌ مثلُها، **والسبقُ فرقُ تاريخين مقروءين**.

`A_GUARD_THAT_CANNOT_BITE_IS_NOT_A_GUARD`: ولا يُقبَل مقياسٌ لا يُرى
عضُّه. **فثلاثُ صورٍ مكذِّبةٍ تُبنى ههنا** ويُشترَط أن يردَّها: تبديلُ
حمولةٍ، وإقحامُ حلقةٍ في الوسط، وقلبُ تاريخَي ختمٍ وسجلِّه. **فلو مرّت
واحدةٌ منها لكان الفحصُ زينة.**

`AND_WHAT_IT_DOES_NOT_PROVE_IS_WRITTEN`: **وحدُّه مُعلَن**: يُثبت أنّ
البصمةَ **كانت في تلك الدفعة**، و**لا يُثبت أنّ التشغيل جرى بعد الختم** —
بل أنّ **إيداعَ** سجلِّه تأخّر عن إيداع ختمه. ومن ختم وشغّل وأودعهما معًا
يُصنَّف «مُودَعان معًا» **ولا يُحسَب سبقًا**. ولا يحرس صوابَ شرطٍ ولا صدقَ
عدد.

`AND_A_SHALLOW_CLONE_IS_CLASSIFIED_NOT_ZEROED`: ونسخةُ CI ضحلةٌ لا تحمل
تاريخًا، **فما يحتاجه يُتخطّى بسببٍ مُسمًّى**؛ **وفحصُ السلسلة نفسِه
يعمل في الحالين** لأنّه حسابٌ لا يسأل التاريخ.
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
CHAIN = REPOSITORY / "deposits" / "seal_chain.json"


def _tool() -> Any:
    path = REPOSITORY / "tools" / "seal_chain.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TOOL = _tool()
SHALLOW = "نسخةٌ ضحلة: لا مراسيَ في التاريخ — والحالُ مُصنَّفةٌ لا مُصفَّرة"
needs_history = pytest.mark.skipif(TOOL.shallow(), reason=SHALLOW)


def test_the_chain_rebuilds_from_the_genesis_hash() -> None:
    """تُعاد السلسلةُ من جذر الأصفار حسابًا — ولا تُصدَّق بصمةٌ مكتوبة."""

    chain = TOOL.deposited()
    assert chain["بصمة_الجذر"] == "0" * 64
    assert TOOL.objections(chain) == []
    assert len(chain["الحلقات"]) >= 45


def test_a_changed_payload_is_refused() -> None:
    """صورةٌ مكذِّبةٌ أولى: يُبدَّل شرطٌ في الوسط **فتُرَدّ**."""

    hurt = copy.deepcopy(TOOL.deposited())
    hurt["الحلقات"][10]["الحمولة"]["الشروط"] += 1
    assert TOOL.objections(hurt), "حمولةٌ بُدِّلت ومرّت — فالفحصُ زينة"


def test_an_inserted_ring_invalidates_everything_after_it() -> None:
    """صورةٌ ثانية: تُقحَم حلقةٌ في الوسط **فيبطل ما بعدها كلُّه** لا جارُها."""

    chain = TOOL.deposited()
    hurt = copy.deepcopy(chain)
    hurt["الحلقات"].insert(10, copy.deepcopy(chain["الحلقات"][0]))
    said = TOOL.objections(hurt)
    assert len(said) > len(chain["الحلقات"]) - 10
    assert any("الخاتمة" in one for one in said)


def test_a_reordered_pair_of_dates_is_seen_by_the_precedence_measure() -> None:
    """صورةٌ ثالثة: يُقلَب تاريخا ختمٍ وسجلِّه **فيُعَدّ في «تأخّر»**."""

    hurt = copy.deepcopy(TOOL.deposited())
    for one in hurt["الحلقات"]:
        if one["مرساة_السجل"]:
            one["تاريخ_مرساة_السجل"], one["تاريخ_المرساة"] = (
                one["تاريخ_المرساة"],
                one["تاريخ_مرساة_السجل"],
            )
            break
    assert TOOL.precedence(hurt)["تأخر"], "قلبُ التاريخين مرَّ — فالمقياسُ أعمى"


def test_no_seal_was_deposited_after_the_log_that_runs_it() -> None:
    """**والقياسُ نفسُه**: لا ختمَ أُودِع بعد سجلِّ تشغيله — صفرٌ في «تأخّر»."""

    kinds = TOOL.precedence(TOOL.deposited())
    assert kinds["تأخر"] == [], kinds["تأخر"]
    assert len(kinds["سبق"]) >= 20, len(kinds["سبق"])


def test_the_seals_without_a_deposited_log_are_named_not_hidden() -> None:
    """وما لا سجلَّ له **يُسمّى ويُعَدّ** — فلا يُقرَأ صمتُه سبقًا."""

    chain = TOOL.deposited()
    kinds = TOOL.precedence(chain)
    assert kinds["بلا سجل"], "صنفُ «بلا سجلّ» خالٍ — وذلك ادّعاءُ تمامٍ لا يصحّ"
    assert sum(len(one) for one in kinds.values()) == len(chain["الحلقات"])
    for name in kinds["بلا سجل"]:
        assert any(one["الاسم"] == name for one in chain["الحلقات"]), name


def test_every_ring_carries_a_commit_not_a_written_time() -> None:
    """المرساةُ **بصمةُ دفعة** لا حقلًا زمنيًّا يكتبه صاحبُ السجلّ."""

    for one in TOOL.deposited()["الحلقات"]:
        assert len(one["المرساة"]) == 40, one["الاسم"]
        assert one["تاريخ_المرساة"].endswith("+00:00"), one["الاسم"]
        assert len(one["الحمولة"]["البصمة"]) == 64


@needs_history
def test_the_deposited_chain_is_what_the_tool_derives_from_the_tree() -> None:
    """المُودَعُ مطابقٌ لما تشتقّه الآلةُ الآن — فلا حقلَ حُرِّر بيد."""

    assert TOOL.build() == TOOL.deposited()


@needs_history
def test_each_anchor_really_contains_its_digest() -> None:
    """وكلُّ مرساةٍ **تحمل بصمتَها فعلًا** — تُقرَأ من الدفعة لا من السجلّ."""

    import subprocess  # noqa: S404

    for one in TOOL.deposited()["الحلقات"][:6]:
        done = subprocess.run(  # noqa: S603
            ["git", "show", "--format=", "--unified=0", str(one["المرساة"])],  # noqa: S607
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=True,
        )
        assert str(one["الحمولة"]["البصمة"]) in done.stdout, one["الاسم"]


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوبٌ في متنه: يُثبت الإيداعَ لا التشغيل، والضحلُ يُصنَّف."""

    here = Path(__file__).read_text(encoding="utf-8")
    assert "`A_GUARD_THAT_CANNOT_BITE_IS_NOT_A_GUARD`" in here
    assert "**ولا يُثبت أنّ التشغيل جرى بعد الختم**" in here
    assert "`AND_A_SHALLOW_CLONE_IS_CLASSIFIED_NOT_ZEROED`" in here
    tool = (REPOSITORY / "tools" / "seal_chain.py").read_text(encoding="utf-8")
    assert "`AND_WHAT_THE_CHAIN_DOES_NOT_PROVE`" in tool
    assert "**لا تُثبت أنّ التشغيل جرى بعد الختم**" in tool
