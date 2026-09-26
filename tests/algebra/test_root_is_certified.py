"""جذرُ الشجرة مُشتَقٌّ ومعتمَد — والاعتمادُ يُفصِح عن وكالته أو يُردّ.

**العطلُ الذي يحرسه**: كان `README.md` **أشدَّ ملفٍّ يُقرَأ وأقلَّه
حراسةً** — مكتوبًا بيدٍ لا مولّدَ له ولا فحصَ يقابله. وفي `docs/` سبعةَ
عشرَ مولّدًا ولكلٍّ فحصٌ يمنع تحريرَ رقمٍ فيه بيد، **والجذرُ خارجٌ عنها
كلِّها**. فكلُّ رقمٍ فيه كان يَبلى صامتًا، **وأوّلُ ما يُقرَأ أوّلُ ما
يَكذِب**.

**وما يُفحَص ههنا** ثلاثةٌ لا يُجمَعها واحد:

١) **الاشتقاق**: `README.md` يُعاد توليدُه مطابقًا حرفًا بحرف، وأعدادُه
   تُعاد من الشجرة لا من الذاكرة، وكلُّ إشارةٍ فيه تقع على ملفٍّ موجود.

٢) **الإفصاح**: الاعتمادُ **بالوكالة**، والاسمُ اسمُ صاحب المستودع واليدُ
   يدُ الآلة — **ويُردّ توقيعٌ يُخفي ذلك**. والصائغُ هو الموقِّعُ نفسُه،
   فهو تصديقُ المؤلِّف على ما ألَّف، **ويُسجَّل ولا يُكتَم**.

٣) **النطاق**: لكلّ بندٍ معتمَدٍ نظيرٌ **مستثنًى مُسمًّى**. فتوقيعٌ بلا
   استثناءٍ يُقرَأ تصديقًا على كلّ ما في الشجرة، **وذلك أوسعُ ممّا
   حُقِّق** — ويردُّه البناء.

`AND_THE_GUARD_DOES_NOT_CHECK_THAT_A_CLAIM_IS_TRUE`: **وحدُّه مُعلَن**:
يحرس أن يكون الجذرُ مُشتَقًّا، وأن يُفصِح التوقيعُ عن وكالته، وأن يُسمّى
المستثنى. **ولا يحرس صوابَ بندٍ اعتُمِد** — بندٌ خاطئٌ يمرُّ عليه. فهو
يردُّ **الصمتَ والتلبيسَ**، لا الخطأ.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
TOOLS = REPOSITORY / "tools"
DOCS = REPOSITORY / "docs"
DEPOSITS = REPOSITORY / "deposits"
ROOT = REPOSITORY / "README.md"


def _tool(name: str) -> Any:
    path = TOOLS / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None, name
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_the_root_is_regenerated_and_never_typed() -> None:
    """المكتوبُ في الجذر مطابقٌ لما يولّده مولّدُه — حرفًا بحرف."""

    assert _tool("write_root.py").render() == ROOT.read_text(encoding="utf-8")


def test_the_counts_in_the_root_follow_the_tree() -> None:
    """أعدادُ الجذر تُعاد من الشجرة، ولا تُقابَل بثابتٍ مكتوبٍ ههنا."""

    root = _tool("write_root.py")
    index = _tool("write_seal_index.py")
    written = ROOT.read_text(encoding="utf-8")
    seals = index.gather()
    marks = sum(int(one["count"]) for one in seals)
    flaws = re.findall(
        r"^## [٠-٩]+\) ",
        (DOCS / "سجل-الأعطال.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    logs = sorted(DEPOSITS.glob("*.log"))
    said, whole, left = root.ceilings()
    for number in (
        len(seals),
        marks,
        len(index.records()),
        len(flaws),
        len(logs),
        said,
        whole,
    ):
        assert root.grouped(number) in written, number
    assert left == whole - said
    assert len(seals) > 30 and marks > 200 and len(logs) > 30


def test_every_pointer_in_the_root_resolves() -> None:
    """كلُّ إشارةٍ في الجذر تقع على ملفٍّ موجود — ولا رابطَ معلَّق."""

    links = re.findall(r"\]\((?!https?:)([^)]+)\)", ROOT.read_text(encoding="utf-8"))
    assert links
    for one in links:
        assert (REPOSITORY / one).resolve().is_file(), one


def test_every_package_the_root_names_is_in_the_tree() -> None:
    """ما سُمّيت حزمةً في الجذر موجودةٌ في `src/` — لا تُوصَف حزمةٌ غائبة."""

    named = _tool("write_root.py").PACKAGES
    assert len(named) >= 8
    for name, does in named:
        head, _, tail = name.partition(".")
        where = (REPOSITORY / "src" / head / f"{tail}.py") if tail else None
        assert (where or (REPOSITORY / "src" / head)).exists(), name
        assert len(does) > 40, name


def test_the_adoption_verifies_against_the_root() -> None:
    """الجذرُ يحمل إفصاحَ الوكالة وكلَّ بندٍ اعتُمِد واستُثنِي."""

    assert _tool("root_certificate.py").verify_against_root() == []


def test_the_adoption_digest_is_rederived_not_written() -> None:
    """البصمةُ مُشتَقّةٌ من الحقول، ويُستشهَد بها في الجذر."""

    tool = _tool("root_certificate.py")
    assert tool.RECORD_DIGEST == tool.rederive_record_digest()
    assert len(tool.RECORD_DIGEST) == 64
    assert tool.RECORD_DIGEST[:8] in ROOT.read_text(encoding="utf-8")


def test_the_root_discloses_that_the_drafter_is_the_signer() -> None:
    """تصديقُ المؤلِّف على ما ألَّف يُسجَّل — ولا يُقرَأ شهادةً مستقلّة."""

    tool = _tool("root_certificate.py")
    sealed = tool.FROZEN_ADOPTION
    written = ROOT.read_text(encoding="utf-8")
    assert sealed.drafter == sealed.executed_by
    assert sealed.executed_by != sealed.signer
    for line in tool.DISCLOSURE:
        assert line in written, line
    assert "**والصائغُ هو الموقِّعُ نفسُه**" in written
    assert "فقد قُرِئ عليه غيرُ الواقع" in written


def test_a_machine_may_be_a_hand_but_never_a_name() -> None:
    """المادّةُ ٢٧: الآلةُ تكون يدًا ولا تكون اسمًا — مفحوصًا لا مقولًا."""

    tool = _tool("root_certificate.py")
    with pytest.raises(tool.RootAdoptionError):
        replace(tool.FROZEN_ADOPTION, signer="آلةُ القياس")


def test_a_proxy_without_a_dated_authority_is_refused() -> None:
    """وكالةٌ بلا سندٍ مُسمًّى مؤرَّخٍ **تُردّ** — ولا تُحمَل على النيّة."""

    tool = _tool("root_certificate.py")
    for broken in ({"authority": ""}, {"authority_dated": ""}, {"authority": "تفويض"}):
        with pytest.raises(tool.RootAdoptionError):
            replace(tool.FROZEN_ADOPTION, **broken)


def test_an_adoption_without_named_exceptions_is_refused() -> None:
    """اعتمادٌ بلا مستثنًى يُقرَأ تصديقًا على الكلّ — فيُردّ بناءً."""

    tool = _tool("root_certificate.py")
    with pytest.raises(tool.RootAdoptionError):
        replace(tool.FROZEN_ADOPTION, withheld=())
    with pytest.raises(tool.RootAdoptionError):
        replace(tool.FROZEN_ADOPTION, certifies=tool.FROZEN_ADOPTION.certifies[:2])
    with pytest.raises(tool.RootAdoptionError):
        replace(tool.FROZEN_ADOPTION, withheld=("قصير",))


def test_what_is_withheld_is_as_wide_as_what_is_adopted() -> None:
    """لا يُوقَّع على سبعةٍ ويُستثنى واحد — والنطاقان يُقرآن معًا."""

    sealed = _tool("root_certificate.py").FROZEN_ADOPTION
    assert len(sealed.certifies) == 7
    assert len(sealed.withheld) == 7
    for one in sealed.withheld:
        assert len(one) > 60, one


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّ الفحص مكتوبٌ في متنه — يردُّ الصمتَ والتلبيس لا الخطأ."""

    text = Path(__file__).read_text(encoding="utf-8")
    assert "AND_THE_GUARD_DOES_NOT_CHECK_THAT_A_CLAIM_IS_TRUE" in text
    assert "**ولا يحرس صوابَ بندٍ اعتُمِد**" in text
    assert "بندٌ خاطئٌ يمرُّ عليه" in text
