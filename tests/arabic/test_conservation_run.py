"""شُغِّل ختمُ `373d928f…`: **مبرهنةُ الحفظ ثبتت طبقةً طبقة، والسلّمُ بلغ ط٧،
والمصحفُ عاد من البتّات والبقايا ببصمته؛ وهو جامعٌ مانع**.

- `BITS_TO_UNITS`: ح٠ **ثبت**: ٢٥٥٣٢٢٩ بتّةً قبلتها آلةُ الرخص كلَّها، فعادت
  ٣٦٤٧٤٧ وحدةً من ٣٦٤٧٤٧ (سبعُ بتّاتٍ للوحدة).
- `UNLICENSED_REFUSED`: ح١ **ثبت**: رُفضت الرموزُ الستّةَ عشرَ غيرُ المرخّصة كلُّها.
- `ALL_112_USED`: ح٢ **ثبت**: الخاناتُ المستعملة ١١٢ من ١١٢، والانتقالاتُ
  المستعملة ٢٢٣ من ٢٢٣ مرخّصة — استُنفدت الرخصُ كلُّها.
- `WORDS_RETURN`: ح٣ **ثبت**: ١٧٩٠٩ صورةَ لفظٍ عادت من عواملها كلُّها.
- `GATHERING`: ح٤ **ثبت**: من ٧٨٢٤٥ لفظًا ليس ذرّةً ٧٧٩٦٩ (٠٫٩٩٦٥): معجمٌ مغلق
  ٢٧٠٧١، ومركّبٌ ٥٠٨٩٨، وذرّةٌ ٢٧٦.
- `FORM_EXCLUDES`: ح٥ **ثبت** على خلاف توقّعي: من ١٧٥١٦ صورةً مخلوطة رُفض
  بالعوامل وحدها ١٣٩٧٨ (٠٫٧٩٨٠). فالتعليلُ
  «الخانةُ تقبل أيَّ حرفٍ فالشكلُ لا يمنع» لم يؤيّده القياس:
  أطرافُ اللفظ (السابقةُ والآخرُ واللاحقة) وحروفُ الوزن غيرُ الخانات
  تُطابَق حرفًا وحالًا، فتمنع.
- `ROOT_EXCLUDES`: ح٦ **ثبت**: وبمخزن الجذور ١٦٢٧٩ (٠٫٩٢٩٤).
- `WRITING_RETURNS`: ح٧ **ثبت**: ٧٨٢٤٥ لفظًا مكتوبًا عادت كلُّها، والبقيّةُ قنواتٌ
  على ١٩٠٢٨٧ وحدة، ولا علامةَ بنيويّةَ في هذه المدوّنة.
- `VERSES_RETURN`: ح٨ **ثبت**: ٦٢٣٧ سطرًا عادت كلُّها (٦٢٣٦ آيةً والسطرُ الفارغُ
  بعد الأخير)، والفواصلُ ٦٧٧٢٢ مسافةً و٤٢٨٧ « <sel> ».
- `MUSHAF_RETURNS`: ح٩ **ثبت**: عاد المصحفُ بايتةً بايتة، وبصمتُه هي البصمةُ المجمَّدة.

وتشخيصُ الذرّات بعد التشغيل: ١٨٨ كتابةً (١٨١ صورة) في ٢٧٦ موضعًا، وأكثرُها فعلٌ
بضميرين متتاليين — فاعلٍ ومفعول — لم يرد تركيبُهما لاحقةً واحدةً في المخزن
(«رَزَقْنَاهُمْ» ١٠، «جَعَلْنَاهُ» ٧، «خَلَقْنَاكُمْ» ٦): **فاللاحقةُ نفسُها حاصلُ ضرب**.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path
from types import ModuleType

import pytest
from frozen_corpus import CORPUS, requires_corpus
from test_conservation_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_conservation.py"
QAC = Path(os.environ.get("QAC_MORPHOLOGY", "/tmp/qm/quran-morphology.txt"))

pytestmark = [
    requires_corpus,
    pytest.mark.skipif(not QAC.exists(), reason="ملفّ QAC (GPL) يُعطى بـQAC_MORPHOLOGY"),
]

FOUND = {
    "tokens": 78_245,
    "forms": 17_909,
    "bits": 2_553_229,
    "bits_accepted": 2_553_229,
    "units": 364_747,
    "units_returned": 364_747,
    "cells_attested": 112,
    "transitions_licensed": 223,
    "transitions_used": 223,
    "unlicensed_rejected": 16,
    "unlicensed_codes": 16,
    "lexemes": 816,
    "compounds": 16_912,
    "atoms": 181,
    "tokens_lexeme": 27_071,
    "tokens_compound": 50_898,
    "tokens_atom": 276,
    "words_returned": 17_909,
    "shuffled": 17_516,
    "shuffled_refused": 13_978,
    "shuffled_unrooted": 16_279,
    "written_returned": 78_245,
    "residue_marks": 0,
    "residue_notes": 190_287,
    "verses": 6_237,
    "verses_returned": 6_237,
    "separators": Counter({" ": 67_722, " <sel> ": 4_287}),
    "corpus_returned": True,
    "fingerprint_returned": True,
    "reached": ("ط١–ط٣", "ط٤", "ط٥", "ط٦", "ط٧"),
}
SHARES = {"ح٤": "0.9965", "ح٥": "0.7980", "ح٦": "0.9294"}
UNIT_BITS = 7
GATHERED = 77_969
ATOM_SPELLINGS = 188
QUOTED_REASONING = "الخانةُ تقبل أيَّ حرفٍ فالشكلُ لا يمنع"


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_conservation", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _ladder() -> dict[str, object]:
    return _reader().ladder(CORPUS.read_text(encoding="utf-8"), QAC)  # type: ignore[no-any-return]


def _one(name: str):  # type: ignore[no-untyped-def]
    return next(one for one in PREDICTIONS if one.identifier == name)


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("373d928f")


def test_the_counts_are_as_recorded() -> None:
    """الأعدادُ كما رُويت، وأجزاؤها تجمع إليها."""

    assert _ladder() == FOUND
    assert FOUND["bits"] == UNIT_BITS * FOUND["units"]
    tokens = FOUND["tokens"]
    kinds = FOUND["tokens_lexeme"] + FOUND["tokens_compound"] + FOUND["tokens_atom"]
    assert kinds == tokens
    assert FOUND["lexemes"] + FOUND["compounds"] + FOUND["atoms"] == FOUND["forms"]
    assert tokens - FOUND["tokens_atom"] == GATHERED
    assert f"{GATHERED / tokens:.4f}" == SHARES["ح٤"]
    assert f"{FOUND['shuffled_refused'] / FOUND['shuffled']:.4f}" == SHARES["ح٥"]
    assert f"{FOUND['shuffled_unrooted'] / FOUND['shuffled']:.4f}" == SHARES["ح٦"]
    assert ATOM_SPELLINGS >= FOUND["atoms"]
    assert FOUND["verses"] == 6_236 + 1


def test_the_verdicts() -> None:
    """الشروطُ العشرةُ ثبتت كلُّها، والسلّمُ بلغ ط٧."""

    shuffled = FOUND["shuffled"]
    assert _one("ح٠").verdict(Fraction(364_747, 364_747)) is Verdict.MET
    assert _one("ح١").verdict(Fraction(16, 16)) is Verdict.MET
    assert _one("ح٢").verdict(Fraction(112, 112)) is Verdict.MET
    assert _one("ح٣").verdict(Fraction(17_909, 17_909)) is Verdict.MET
    assert _one("ح٤").verdict(Fraction(GATHERED, 78_245)) is Verdict.MET
    assert _one("ح٥").verdict(Fraction(13_978, shuffled)) is Verdict.MET
    assert _one("ح٦").verdict(Fraction(16_279, shuffled)) is Verdict.MET
    assert _one("ح٧").verdict(Fraction(78_245, 78_245)) is Verdict.MET
    assert _one("ح٨").verdict(Fraction(6_237, 6_237)) is Verdict.MET
    assert _one("ح٩").verdict(Fraction(1)) is Verdict.MET
    assert FOUND["reached"][-1] == "ط٧"
    assert QUOTED_REASONING in __doc__  # type: ignore[operator]


REASONING_NOT_SUPPORTED: tuple[str, ...] = ("ح٠", "ح١", "ح٣", "ح٥", "ح٧", "ح٨", "ح٩")
"""ح٠ ح١ ح٣ ح٧ ح٨ ح٩ مرّت بالإنشاء: الصعودُ عكسُ الهبوط تعريفًا، والفحصُ يشهد أنّ
الآلةَ هي البرهان لا أنّ للّغة فيه دعوى. وح٥ ثبت على خلاف ما علّلتُ به فسقط التعليل."""
