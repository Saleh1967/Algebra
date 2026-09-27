"""شُغِّل فهرسُ السور: **البايتُ يحلّ مئةً وثلاثةَ عشرَ حدًّا، والرابعُ عشرَ لا**.

**الحصاد**: **الاثنتا عشرةَ كلُّها صمدت** — ولا سقوط. وذلك يُقال كما هو:
ختمٌ تمرُّ شروطُه كلُّها **أضعفُ شهادةً من ختمٍ يسقط بعضُه**، لأنّ الشروطَ
كانت في مقدور الحدس. **فلا يُقرَأ صمودُها فتحًا.**

`THE_INDEX_IS_DERIVED_AND_ITS_ONE_GAP_IS_CLASSIFIED`: والعلامةُ في
البايتات **هيكلُ البسملة الرباعيُّ**، وهي تحلّ **١١٣** رأسًا: واحدٌ
**قائمٌ بنفسه** (السطرُ الأوّل) و**١١٢ ملحَقةٌ** بأوّل ما بعدها. ومجموعُ
أطوال الكتل **٦٬٢٣٦ بالضبط**، **فلا سطرَ يسقط ولا يُعَدّ مرّتين**.

`AND_THE_HUNDRED_AND_FOURTEENTH_IS_UNATTESTED_NOT_ZEROED`: وأنّ السورَ
**١١٤** معلومٌ من خارجٍ — **لا مقيسٌ ههنا**. فحدٌّ واحدٌ **لا علامةَ له في
البايتات**: `Vacancy.UNATTESTED`. **ولا يُخترَع له موضعٌ**، ولا يُقال
«الكتلةُ الفلانيّةُ سورتان»، ولا يُصفَّر. **ويُسدّ بإيداع جردٍ موقَّعٍ لا
باستنباط.**

`AND_THE_MARKER_APPEARS_ONCE_OUTSIDE_A_HEAD`: وسطرٌ **واحدٌ** يحمل
الكلماتِ الأربعَ متتالياتٍ **في غير موضع الابتداء** — السطرُ ٣٬١٨٩.
**فالعلامةُ ملتبسةٌ مرّةً واحدةً**، وقد وُضِع الشرطُ عند مرّتين فمرَّ.
**ولو كانت العلامةُ «بسم» وحدَها لكان الالتباسُ أوسع** — والرباعيّةُ هي
التي حدَّته، وذلك قرارٌ مختومٌ قبل النظر لا بعده.

`AND_THE_LENGTHS_AGREE_WITH_WHAT_IS_KNOWN_OUTSIDE_AND_THAT_IS_NOT_A_PROOF`:
وأطوالُ أوّل أربعِ كتلٍ **٧ · ٢٨٦ · ٢٠٠ · ١٧٦** — وهي أعدادُ آيِ الفاتحة
والبقرة وآل عمران والنساء في العدّ الكوفيّ **معلومةً من خارج**.
**وموافقتُها شاهدُ اتّساقٍ لا برهانَ صحّة**: لو خالفت لَسقط الفهرس، **ولا
يُرقّي اتّفاقُها الفهرسَ إلى جردٍ مُودَع**.

**ولا يُرقَّم رأسٌ برقم سورة في هذا السجلّ** — وهو حدُّ التشغيل المكتوبُ
قبله.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from frozen_corpus import requires_corpus
from test_surah_index_seal import (
    DIGEST,
    NO_SURAH_IS_NUMBERED_HERE,
    ORACLE,
    PREDICTIONS,
    THE_HUNDRED_AND_FOURTEENTH_HAS_NO_MARKER,
)

from algebra.results import Vacancy
from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "surah_index_run.log"
LIFTED = REPOSITORY / "examples" / "rasm" / "run_basmala_lifted.py"

pytestmark = requires_corpus

LINES = 6_236
HEADS = 113
ALONE = 1
PREPENDED = 112
ASIDE = 1
ASIDE_AT = 3_189
SHORTEST = 3
LONGEST = 286
UNDER_SIX = 9
EXACTLY_THREE = 3
OUTSIDE = 0
ZERO_LENGTH = 0
KNOWN_OUTSIDE = 114
FIRST_FOUR = (7, 286, 200, 176)

REASONING_NOT_SUPPORTED: tuple[str, ...] = ()
"""شروطٌ مرّت وتعليلُها لم يُؤيَّد بالقياس — **ولا واحدَ ههنا**.

فكلُّ شرطٍ في هذا الختم **عَدٌّ لا تعليل**: عددُ رؤوسٍ، وطولُ كتلةٍ، ومجموعُ
أطوال. **ولا تفسيرَ يُحمَل على عددٍ** إلّا ما أُعلِن معلومًا من خارج.
"""

FORBIDDEN = ("سورة رقم", "مبنيّ", "معرب", "ARABIC")
DECLARATION = "— ما لا يحلُّه البايت"


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _number(pattern: str) -> int:
    text = LOG.read_text(encoding="utf-8")
    found = re.search(pattern, text, re.M)
    assert found is not None, pattern
    return int(found.group(1))


def _lengths() -> list[int]:
    text = LOG.read_text(encoding="utf-8")
    body = text.split("— أطوالُ الكتل بترتيبها")[1].split("— الأطولُ")[0]
    return [int(one) for one in re.findall(r"^  \d+ ← (\d+)$", body, re.M)]


def test_the_seal_is_unchanged() -> None:
    """الختمُ كما دُفِع — ولا يُعاد تفسيرُ شرطٍ بعد رؤية رقمه."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_machine_conditions_hold() -> None:
    """ن١ ون٤: المدوّنةُ هي هي، والقسمةُ تامّةٌ بالبناء."""

    assert _number(r"^— الأسطر: (\d+)$") == LINES
    assert _one("ن١").verdict(Fraction(0)) is Verdict.MET  # type: ignore[attr-defined]
    covered = _number(r"مجموعُ أطوالها: (\d+)")
    outside = _number(r"وأسطرٌ خارجَ كتلةٍ: (\d+)")
    assert covered == LINES and outside == OUTSIDE
    assert sum(_lengths()) == LINES
    assert _one("ن٤").verdict(Fraction(outside)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_marker_resolves_a_hundred_and_thirteen_heads() -> None:
    """ن٢ ون٣ يعضّان العددَ من الطرفين — فهو ١١٣ لا غير."""

    heads = _number(r"^— رؤوسُ الكتل: (\d+)$")
    assert heads == HEADS
    assert _one("ن٢").verdict(Fraction(heads)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ن٣").verdict(Fraction(heads)) is Verdict.MET  # type: ignore[attr-defined]
    assert len(_lengths()) == HEADS


def test_one_head_stands_alone_and_the_rest_are_prepended() -> None:
    """ن١١ ون١٢: سطرٌ واحدٌ هو البسملةُ وحدَها، وهو السطرُ الأوّل."""

    alone = _number(r"منها قائمةٌ بنفسها: (\d+)")
    joined = _number(r"وملحَقةٌ: (\d+)")
    assert alone == ALONE and joined == PREPENDED
    assert alone + joined == HEADS
    assert _one("ن١١").verdict(Fraction(alone)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ن١٢").verdict(Fraction(alone)) is Verdict.MET  # type: ignore[attr-defined]
    assert _number(r"وموضعُ القائمةِ بنفسها: (\d+)") == 1


def test_the_lengths_hold_their_bounds() -> None:
    """ن٥ ون٦ ون٧ ون٨ ون٩: أقصرُ ٣، وأطولُ ٢٨٦، ولا خاويةَ، والقصيراتُ تسعٌ."""

    lengths = _lengths()
    assert min(lengths) == SHORTEST and max(lengths) == LONGEST
    assert _one("ن٥").verdict(Fraction(min(lengths))) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ن٦").verdict(Fraction(max(lengths))) is Verdict.MET  # type: ignore[attr-defined]
    empty = sum(1 for one in lengths if one == 0)
    assert empty == ZERO_LENGTH
    assert _one("ن٧").verdict(Fraction(empty)) is Verdict.MET  # type: ignore[attr-defined]
    short = sum(1 for one in lengths if one <= 5)
    assert short == UNDER_SIX
    assert _one("ن٨").verdict(Fraction(short)) is Verdict.MET  # type: ignore[attr-defined]
    triples = sum(1 for one in lengths if one == 3)
    assert triples == EXACTLY_THREE
    assert _one("ن٩").verdict(Fraction(triples)) is Verdict.MET  # type: ignore[attr-defined]


def test_the_marker_is_ambiguous_exactly_once() -> None:
    """ن١٠: سطرٌ واحدٌ يحملها في غير الابتداء — والشرطُ عند مرّتين فمرَّ."""

    aside = _number(r"وأسطرٌ تحمل العلامةَ غيرَ مبتدأةٍ بها: (\d+)")
    assert aside == ASIDE
    assert _one("ن١٠").verdict(Fraction(aside)) is Verdict.MET  # type: ignore[attr-defined]
    assert str(ASIDE_AT) in LOG.read_text(encoding="utf-8")


def test_all_twelve_held_and_that_is_said_not_celebrated() -> None:
    """الاثنتا عشرةَ كلُّها صمدت — **وذلك يُضعِف الشهادةَ لا يُقوّيها**."""

    assert len(PREDICTIONS) == 12
    assert REASONING_NOT_SUPPORTED == ()
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**أضعفُ شهادةً من ختمٍ يسقط بعضُه**" in text
    assert "**فلا يُقرَأ صمودُها فتحًا.**" in text


def test_the_one_unresolved_boundary_is_classified_not_invented() -> None:
    """الرابعُ عشرَ `UNATTESTED` — انعدامُ دليلٍ لا امتناعُ بلوغ."""

    text = LOG.read_text(encoding="utf-8")
    assert THE_HUNDRED_AND_FOURTEENTH_HAS_NO_MARKER is Vacancy.UNATTESTED
    assert DECLARATION in text
    _, _, owned = text.partition(DECLARATION)
    assert f"السورُ معلومةً من خارج: {KNOWN_OUTSIDE}" in owned
    assert "**لا مقيسةً ههنا**" in owned
    assert f"وحدودٌ حلَّها البايت: {HEADS}" in owned
    assert f"فحدودٌ لا علامةَ لها في البايتات: {KNOWN_OUTSIDE - HEADS}" in owned
    assert "UNATTESTED" in owned
    assert "انعدامُ دليلٍ لا امتناعُ بلوغ" in owned
    assert "لا يُخترَع لها موضعٌ ولا تُصفَّر" in owned


def test_no_head_is_numbered_by_a_surah() -> None:
    """ولا يُرقَّم رأسٌ برقم سورة — حدُّ التشغيل، مفحوصًا في متنه."""

    text = LOG.read_text(encoding="utf-8")
    for word in FORBIDDEN:
        assert word not in text, word
    assert "ولا يُرقَّم رأسٌ برقم سورة" in text
    assert "جردًا مُودَعًا" in NO_SURAH_IS_NUMBERED_HERE


def test_the_marker_is_read_from_the_tree_not_typed_in_the_run() -> None:
    """هيكلُ البسملة يُقرَأ من `run_basmala_lifted.HEAD` — المادّةُ ٩."""

    run = (REPOSITORY / "examples" / "rasm" / "run_surah_index.py").read_text(
        encoding="utf-8"
    )
    assert "lifted.HEAD" in run
    assert "run_basmala_lifted.HEAD" in LOG.read_text(encoding="utf-8")
    assert "HEAD = [" in LIFTED.read_text(encoding="utf-8")


def test_the_agreement_with_outside_counts_is_consistency_not_proof() -> None:
    """أطوالُ الأربع الأُولى توافق المعلومَ من خارج — **شاهدُ اتّساقٍ لا برهان**."""

    assert tuple(_lengths()[:4]) == FIRST_FOUR
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**وموافقتُها شاهدُ اتّساقٍ لا برهانَ صحّة**" in text
    assert "ولا يُرقّي اتّفاقُها الفهرسَ إلى جردٍ مُودَع" in text
