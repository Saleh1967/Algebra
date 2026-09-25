"""شُغِّل ختمُ `26ae5b5b…`: **أربعةٌ من ثلاثةَ عشرَ — والخللُ في الاستقبال**.

`THE_SUBSTANCE_HELD_IN_EVERY_FORM_I_MEASURED`: خ٨ صمد، وهو جوهرُ العرض:
**خاتمةُ الآية مكثَّفةٌ عن خاتمة الكلمة**. والفرقُ سالبٌ في **الصور الستّ
كلِّها** — من **−٠٫٠٦١٣** إلى **−٠٫٥١٣٤** — فهو خبرٌ عن المادّة لا عن
تعريفٍ بعينه. **والعتبةُ تمنع الترخيص ولا تمنع القياس، وقد قِيس.**

`AND_MARKOV_SAYS_THE_BOUNDARY_CARRIES_SOMETHING`: خ٩ صمد:
`I(الحال ؛ الموضع) = ٠٫٠٥٦٥٢٩` بتًّا للموضع — **٤٬٤٢٣ بتًّا** جملةً،
ونصيبُ الخاتمة من المواضع ٠٫٠٧٩٦٩٨ فقط. **فالحدُّ الآييُّ يترك أثرًا.**

`AND_THE_PROVEN_INEQUALITY_HELD`: خ١٠ صمد: `H(الحال|شرط) ≤ H(الحال)`
في الشرطين — أقصى ارتفاعٍ **−٠٫٠١٦٩٦٤**. وهي `induction on` ههنا،
و`induction FOR` الحلقةُ التي تشهد عليها شرطًا شرطًا.

`BUT_NINE_FELL_AND_THE_CAUSE_IS_ONE_AND_IT_IS_MINE_TO_OWN`: **البسملةُ
ملحقةٌ بأوّل آيةٍ من كلّ سورة في المُجمَّد** — **١١٢** سطرًا، **٤٤٨**
كلمة. ولم يُسجَّل ذلك في أيّ ختمٍ قبلَه، **وكلُّ رقمٍ كلميٍّ نشرتُه يحمله**.

`AND_THE_RECONCILIATION_IS_EXACT`: فبرفع الملحقة:
**٧٨٬٢٤٥ − ٤٤٨ = ٧٧٬٧٩٧**، وبإبقاء البسملة القائمة بنفسها (السطر ١)
**٧٧٬٨٠١** — **وهو المعروضُ بعينه**. والآياتُ وحيدةُ الكلمة **٢ ⟶ ٢٨**
— **وهو المعروضُ بعينه**. وما يبدأ منها هيكليًّا بـ«ال» **١٠** — **وهو
المعروضُ بعينه**. و«بسم» **١١٥ ⟶ ٣**، ومعها اثنتان بشدّةٍ على الباء
رُفِعتا مع الملحقة، **فخمسٌ مرشَّحة** — والعرضُ يقول «أربعٌ لا خمس»،
**والنزولُ من خمسٍ إلى أربعٍ حكمٌ لا يُؤتَمَن عليه القياس**.

`AND_THE_FOUR_SHARES_MATCH_NO_FORM_OF_MINE`: وخ٢–خ٧ منقوضة. وأقربُ ما
بلغتُ إنتروبيا الآية **٢٫٢٠٧٤** مقابلَ المعروض **٢٫٢٠٨٤** — بفارق
**٠٫٠٠١٠** — في التعريف ب بالتنوين المفرَّق. **والنصيبان لا يطابقان صورةً
من الستّ، ولم أخترع تعريفًا سابعًا ليطابق.**
"""

from __future__ import annotations

import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

from test_verse_ending_seal import DIGEST, ORACLE, PREDICTIONS, VERSES

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "verse_ending_run.log"
BASMALA = REPOSITORY / "deposits" / "verse_ending_basmala.log"
FORMS = REPOSITORY / "deposits" / "verse_ending_definitions.log"

VERSE_H = 1.9213
WORD_H = 2.4347
FLOW = 0.056529
RISE = -0.016964
PREFIXED = 112
PREFIXED_WORDS = 448
TOKENS = 78_245


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _grab(pattern: str, path: Path = LOG) -> str:
    found = re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE)
    assert found is not None, pattern
    return found.group(1)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("26ae5b5b")


def test_the_corpus_did_not_move() -> None:
    """خ١: ٦٬٢٣٦ سطرًا — والمحرّكُ يصرخ عند التبدّل."""

    assert _one("خ١").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    assert f"— الأسطر: {VERSES}" in LOG.read_text(encoding="utf-8")


def test_the_substance_held_in_every_form() -> None:
    """خ٨: خاتمةُ الآية مكثَّفةٌ — والفرقُ سالبٌ في الصور الستّ."""

    apart = VERSE_H - WORD_H
    assert _one("خ٨").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    gaps = [
        float(one)
        for one in re.findall(r"الفرق (-[\d.]+)", FORMS.read_text(encoding="utf-8"))
    ]
    assert len(gaps) == 6
    assert max(gaps) < 0, gaps
    assert abs(min(gaps) - -0.5134) < 5e-5 and abs(max(gaps) - -0.0613) < 5e-5


def test_the_boundary_carries_information() -> None:
    """خ٩: `I = ٠٫٠٥٦٥٢٩` بتًّا للموضع، و٤٬٤٢٣ بتًّا جملةً."""

    carried = float(_grab(r"I\(الحال ; الموضع\) = ([\d.]+)"))
    assert _one("خ٩").verdict(_exact(carried)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(carried - FLOW) < 5e-7
    assert "وجملةُ ما تحمله الخاتمةُ: 4423 بتًّا" in LOG.read_text(encoding="utf-8")


def test_conditioning_never_raised_the_entropy() -> None:
    """خ١٠ — `induction on`: الشرطُ لا يرفع الإنتروبيا."""

    rise = float(_grab(r"أقصى ارتفاعٍ بالشرط: (-[\d.]+)"))
    assert _one("خ١٠").verdict(_exact(rise)) is Verdict.MET  # type: ignore[attr-defined]
    assert abs(rise - RISE) < 5e-7 and rise < 0


def test_the_intake_flaw_is_found_and_it_is_the_basmala() -> None:
    """البسملةُ ملحقةٌ بأوّل آيةٍ من كلّ سورة — ١١٢ سطرًا و٤٤٨ كلمة."""

    text = BASMALA.read_text(encoding="utf-8")
    assert f"أسطرٌ تبدأ بالبسملة ثمّ زيادة: {PREFIXED}" in text
    assert f"جملةُ كلمِ البسملات الملحقة:   {PREFIXED_WORDS}" in text
    assert PREFIXED * 4 == PREFIXED_WORDS
    assert TOKENS - PREFIXED_WORDS == 77_797


def test_removing_the_basmala_reproduces_the_presented_counts_exactly() -> None:
    """٧٧٬٨٠١ و٢٨ و١٠ — ثلاثتُها تُطابَق بعد رفع الملحقة."""

    text = BASMALA.read_text(encoding="utf-8")
    assert "الكلمُ بعد رفع الملحقة:   77797" in text
    assert "والمعروضُ ٧٧٨٠١، فالفرقُ: -4" in text  # والأربعةُ بسملةُ السطر الأوّل
    assert 77_797 + 4 == 77_801
    assert "وبعد رفع البسملة الملحقة:            28" in text
    assert "منها ما يبدأ هيكليًّا بـ«ال»:          10" in text
    assert _one("خ١٢").verdict(Fraction(abs(2 - 28))) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    assert _one("خ١٣").verdict(Fraction(abs(0 - 10))) is Verdict.FALSIFIED  # type: ignore[attr-defined]


def test_the_basmala_count_lands_on_five_candidates_not_four() -> None:
    """١١٥ ⟶ ٣، ومعها اثنتان بشدّةٍ رُفِعتا — فخمسٌ مرشَّحة، والنزولُ حكم."""

    text = BASMALA.read_text(encoding="utf-8")
    assert "مواضعُ «بسم» كما هي: 115" in text
    assert "وبعد رفع الملحقة:    3" in text
    assert _one("خ١١").verdict(Fraction(abs(115 - 4))) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    run = LOG.read_text(encoding="utf-8")
    shapes = Counter(
        re.findall(r"^    سطرُ \d+ \| موضعُ \d+ من \d+ \| (\S+)$", run, re.MULTILINE)
    )
    assert sum(shapes.values()) == 115
    assert len(shapes) == 2, shapes  # صورتان لا صورة — ولا تُكتَب واحدةٌ منهما بيد
    assert sorted(shapes.values()) == [2, 113]
    assert __doc__ is not None
    assert "حكمٌ لا يُؤتَمَن عليه القياس" in __doc__


def test_the_four_shares_match_no_declared_form_and_none_was_invented() -> None:
    """خ٢–خ٧ منقوضة — وأقربُ ما بلغتُ ٢٫٢٠٧٤ مقابلَ ٢٫٢٠٨٤."""

    for identifier in ("خ٢", "خ٣", "خ٤", "خ٥", "خ٦", "خ٧"):
        assert _one(identifier).verdict(Fraction(1, 10)) is Verdict.FALSIFIED  # type: ignore[attr-defined]
    text = FORMS.read_text(encoding="utf-8")
    assert "H     آيةً 2.2074" in text
    assert "ولا يُخترَع تعريفٌ سابعٌ ليطابق" in text
    assert abs(2.2074 - 2.2084) < 0.0011


def test_what_could_not_be_derived_was_not_guessed() -> None:
    """لا فهرسَ سورٍ — فلا سورةٌ ولا آيةٌ تُذكَر، وأرقامُ الأسطر وحدَها."""

    run = LOG.read_text(encoding="utf-8")
    assert "ولا فهرسَ سورٍ مُودَعٌ" in run
    assert not re.search(r"\b\d+:\d+\b", run)
    assert "سطرُ 1 | موضعُ 1" in run


def test_four_of_thirteen_and_the_nine_share_one_cause() -> None:
    """الجردُ صريحٌ، والسببُ واحدٌ في تسعةٍ منها."""

    met = {"خ١", "خ٨", "خ٩", "خ١٠"}
    fell = {"خ٢", "خ٣", "خ٤", "خ٥", "خ٦", "خ٧", "خ١١", "خ١٢", "خ١٣"}
    assert met | fell == {one.identifier for one in PREDICTIONS}  # type: ignore[attr-defined]
    assert len(met) == 4 and len(fell) == 9 and not met & fell
