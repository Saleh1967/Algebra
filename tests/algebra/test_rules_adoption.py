"""اعتمادُ القاعدتين: موقَّعٌ وكالةً، **والوثيقتان لم تُمَسَّا** — العطل ٢٩.

**الدَّينُ الذي سُدَّ**: كانت `separation_rule.md` و`praise_blame_rule.md`
مُودَعتين **غيرَ موقَّعتين**، فتُقاسان ولا يُبنى عليهما. وصارتا معتمَدتين
**فرضًا ومُدخَلًا** بنطاقٍ مكتوب، بتفويضٍ مُسجَّلٍ من صاحب المستودع.

`AND_THE_OBVIOUS_WAY_TO_SIGN_WOULD_HAVE_BROKEN_A_SEALED_LOG`: وأقربُ
طريقٍ إلى التوقيع **تحريرُ سطر التوقيع في الوثيقة** — وهو **العطل ٢٩**:
`run_separation_rule.py` يقرأ ذلك السطرَ بنصّه ويطبع `غيرُ موقَّعة: True`
في `deposits/separation_rule_run.log`، **وهو سجلٌّ مُبصَّمٌ يُقابَل بايتةً
ببايتة** في تدقيق الإعادة. فتحريرُ سطرٍ في الوثيقة **يُبدِّل مخرَجَ
التشغيل ويكسر السجلَّ وبصمتَه وتدقيقَه**.

**والقاعدةُ المستخرَجة**: **مُدخَلُ سجلٍّ مُقفَلٍ مُقفَلٌ مثلُه** — ومن
حرَّره فقد **عدَّل السجلَّ بطريقٍ خفيّ**، وهو أخفى من تعديله مباشرةً.

`SO_THE_ADOPTION_IS_A_SECOND_DOCUMENT_THAT_SEALS_THE_FIRST`: فيُودَع
الاعتمادُ **وثيقةً ثانيةً تُبصِم الأولى ولا تمسّها**، وبصمتا الوثيقتين في
السجلّ المُقفَل. **فإن بُدِّل حرفٌ منهما انكسر الاعتماد** — ويُفحَص ذلك
أدناه لا يُوعَد به.

`AND_AN_ADOPTION_IS_NOT_A_PROMOTION`: ولا يُرقّي الاعتمادُ مستوًى. حالُ
«الكلمة المفردة» `UNCLASSIFIED` في سجلٍّ مُقفَلٍ لا يُعدَّل بعد الحدث.
**فالاعتمادُ يرفع المانعَ القانونيَّ عن الترقية ولا يُرقّي**، والترقيةُ
**قياسٌ يحتاج ختمًا يُدفَع قبل تشغيله**.

`AND_ITS_LIMIT_IS_DECLARED`: **وحدُّه**: يحرس أن تكون الوثيقتان كما
قُفِلتا، وأن يُفصِح التوقيعُ عن وكالته، وأن يُسمّى المستثنى، **وأن لا
يُدَّعى برهان**. ولا يحرس **صوابَ بندٍ اعتُمِد**، ولا يمنع أن تُحرَّر
وثيقةٌ ثالثةٌ يقرؤها سجلٌّ مُقفَلٌ ولم تُبصَم ههنا — **وذلك دَينٌ يُسمّى
ولا يُدَّعى سدُّه**.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
TOOLS = REPOSITORY / "tools"
DEPOSITS = REPOSITORY / "deposits"
PAPER = DEPOSITS / "rules_adoption.md"
RUN = REPOSITORY / "examples" / "rasm" / "run_separation_rule.py"
SEALED_LOG = DEPOSITS / "separation_rule_run.log"
LADDER = TOOLS / "ladder_seal.py"


def _tool(name: str) -> Any:
    path = TOOLS / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None, name
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_both_documents_are_byte_identical_to_what_was_sealed() -> None:
    """بصمةُ كلّ وثيقةٍ كما قُفِلت — **وهذا ما يجعل الاعتمادَ قابلًا للكسر**."""

    tool = _tool("rules_adoption.py")
    assert tool.verify_against_documents() == []
    for rule in tool.FROZEN_ADOPTION.rules:
        data = (DEPOSITS / rule.document).read_bytes()
        assert hashlib.sha256(data).hexdigest() == rule.digest, rule.document


def test_editing_a_document_breaks_the_adoption() -> None:
    """وبصمةٌ لا تُطابِق **تُسمّى بموضعها** — لا تمرُّ صامتة."""

    tool = _tool("rules_adoption.py")
    bent = replace(
        tool.FROZEN_ADOPTION,
        rules=(replace(tool.FROZEN_ADOPTION.rules[0], digest="0" * 64),),
    )
    complaints = tool.verify_against_documents(bent)
    assert len(complaints) == 1
    assert tool.FROZEN_ADOPTION.rules[0].document in complaints[0]
    assert "00000000" in complaints[0]


def test_the_sealed_log_still_reads_the_documents_unsigned_line() -> None:
    """السجلُّ المُقفَل يقرأ سطرَ التوقيع — **فالسطرُ لا يُحرَّر**.

    وهذا هو العطلُ ٢٩ مفحوصًا: إن زال أحدُ الطرفين (قراءةُ التشغيل أو
    مطبوعُ السجلّ) **بطل السبب** الذي مُنِع به التحرير، فيُعاد النظر.
    """

    assert "**التوقيع**: — (غيرُ موقَّعة)" in RUN.read_text(encoding="utf-8")
    assert "غيرُ موقَّعة: True" in SEALED_LOG.read_text(encoding="utf-8")
    paper = PAPER.read_text(encoding="utf-8")
    assert "**مُدخَلُ سجلٍّ مُقفَلٍ مُقفَلٌ مثلُه.**" in paper
    assert "تعديلٌ للسجلّ بطريقٍ خفيّ" in paper


def test_the_adoption_promotes_no_level() -> None:
    """حالُ «الكلمة المفردة» كما هو في السجلّ المُقفَل — والاعتمادُ يقولها."""

    tool = _tool("rules_adoption.py")
    assert "لا يُرقّي" in tool.FROZEN_ADOPTION.promotes
    ladder = LADDER.read_text(encoding="utf-8")
    assert "الكلمةُ المفردة" in ladder
    assert "قاعدةٌ لا تُشتَقّ من البايتات" in ladder
    paper = PAPER.read_text(encoding="utf-8")
    assert "UNCLASSIFIED" in paper
    assert "**خلوٌّ يُصنَّف ولا يُصفَّر**" in paper


def test_the_paper_is_regenerated_and_never_typed() -> None:
    """الوثيقةُ مطابقةٌ لما يولّده مولّدُها — فلا بصمةٌ تُطبَع بيد."""

    assert _tool("write_rules_adoption.py").render() == PAPER.read_text(
        encoding="utf-8"
    )


def test_the_adoption_discloses_its_proxy_and_names_its_scope() -> None:
    """الاسمُ اسمُ صاحب المستودع واليدُ يدُ الآلة — ولكلّ وثيقةٍ مستثنًى."""

    tool = _tool("rules_adoption.py")
    sealed = tool.FROZEN_ADOPTION
    paper = PAPER.read_text(encoding="utf-8")
    assert sealed.executed_by != sealed.signer
    assert sealed.signer in sealed.authority
    assert sealed.authority_dated.strip()
    assert "**وهذا اعتمادٌ بالوكالة لا باليد**" in paper
    assert "كي لا يُقرَأ كأنّه بخطّه" in paper
    assert "**ولا يجعل الاعتمادُ ما اعتُمِد مبرهَنًا**" in paper
    for rule in sealed.rules:
        assert rule.withheld, rule.document
        for one in rule.adopted + rule.withheld:
            assert " ".join(one.split()) in " ".join(paper.split()), one[:40]


def test_a_machine_may_be_a_hand_but_never_a_name() -> None:
    """المادّةُ ٢٧ مفحوصةً — الآلةُ يدٌ لا اسم."""

    tool = _tool("rules_adoption.py")
    with pytest.raises(tool.RuleAdoptionError):
        replace(tool.FROZEN_ADOPTION, signer="آلةُ القياس")
    for broken in ({"authority": ""}, {"authority_dated": ""}, {"authority": "تفويض"}):
        with pytest.raises(tool.RuleAdoptionError):
            replace(tool.FROZEN_ADOPTION, **broken)


def test_an_adoption_may_not_claim_a_proof_nor_hide_its_exceptions() -> None:
    """ويُردّ اعتمادٌ يدّعي برهانًا، أو بلا مستثنًى، أو بلا سجلٍّ قاسه."""

    tool = _tool("rules_adoption.py")
    first = tool.FROZEN_ADOPTION.rules[0]
    with pytest.raises(tool.RuleAdoptionError):
        replace(first, adopts_as="مبرهَنٌ على المدوّنة")
    with pytest.raises(tool.RuleAdoptionError):
        replace(first, adopts_as="حكمًا يُبنى عليه")
    with pytest.raises(tool.RuleAdoptionError):
        replace(first, withheld=())
    with pytest.raises(tool.RuleAdoptionError):
        replace(first, measured_by=())
    with pytest.raises(tool.RuleAdoptionError):
        replace(first, measured_by=("لا_وجودَ_له.log",))


def test_the_word_blind_check_is_declared_as_word_blind() -> None:
    """والفحصُ أعمى عن النفي، **فيُحصَر في لفظين لا يردان في نفي**."""

    tool = _tool("rules_adoption.py")
    assert tool._PROOF_WORDS == ("مبرهَن", "برهان")
    assert "لا وصفًا صحيحًا" in tool.SEPARATION.adopts_as
    text = TOOLS.joinpath("rules_adoption.py").read_text(encoding="utf-8")
    assert "**والفحصُ أعمى عن النفي**" in text
    assert "يردُّ اللفظَ لا المعنى" in text


def test_the_guard_says_what_it_does_not_do() -> None:
    """حدُّه مكتوبٌ: لا يحرس صوابَ بندٍ، ولا يبلغ وثيقةً ثالثة."""

    text = Path(__file__).read_text(encoding="utf-8")
    assert "`AND_ITS_LIMIT_IS_DECLARED`" in text
    assert "ولا يحرس **صوابَ بندٍ اعتُمِد**" in text
    assert "**وذلك دَينٌ يُسمّى\nولا يُدَّعى سدُّه**" in text
