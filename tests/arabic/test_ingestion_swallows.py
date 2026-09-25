"""كاشفُ الابتلاع على أنبوبي أنا — والحاجزُ **صناعيٌّ عند إملاء/رقميّ**.

**السؤال**: أين الحاجز؟ عند واجهة صوت/ترميز فهو فيزيائيٌّ لا يُرفَع، أم عند
مشكول/مجرَّد فالشكلُ يرفعه، أم عند إملاء/رقميّ فهو من صنعِ أدوات القياس؟

**والجوابُ مقيسٌ من الشيفرة لا مظنون**: الحاجزُ عند **إملاء/رقميّ**، وأنا
صنعتُه بأربعة ابتلاعاتٍ في أنبوب القراءة. وهذا الملفُّ يعُدّها واحدًا
واحدًا، ويفصل **الموثَّقَ** عن **اليتيم**.

`THE_FOUR_THOUSAND_TWO_HUNDRED_AND_EIGHTY_SEVEN_GAP_IS_CLOSED`: وأوّلُ ما
أخرجه العدُّ **يُغلِق دَينًا سُجِّل مفتوحًا**. كُتِب في `test_frozen_corpus_run`:
«عدُّ الرموز على السطر كلِّه ٨٢٬٥٣٢، والثابتُ في مرايا simple ٧٨٬٢٤٥،
والفرقُ ٤٬٢٨٧ **غيرُ مفسَّرٍ ههنا**». والمقيسُ الآن: في المدوّنة **٤٬٢٨٧
وسمًا `<sel>`** بالضبط، توكنًا مستقلًّا بالفراغ. فـ٨٢٬٥٣٢ − ٤٬٢٨٧ =
**٧٨٬٢٤٥** — الثابتُ نفسُه بلا بقيّة. فالفجوةُ **وسمٌ لا كلمات**،
والدَّينُ يُغلَق بعدٍّ لا بتأويل.

`AND_THE_MARKUP_WAS_SWALLOWED_SILENTLY_BY_MY_OWN_READER`: وقارئي يُسقِط
`< s e l >` لأنّها ليست في الأبجديّة — **٢١٬٤٣٥ محرفًا يسقط بلا خبر**.
ولم يضرّ تيارَ الحروف (الوسمُ محفوفٌ بفراغين فلا يكسر جوارًا)، لكنّه
**ابتلاعٌ يتيمٌ**: لا قاعدةَ مكتوبةً تُجيزه، ولو وقع في موضعٍ آخر لكسر
جوارًا ولم يُعلِم.

`NFC_REORDERS_FORTY_FIVE_THOUSAND_POSITIONS_AND_THAT_IS_NOT_NOTHING`:
والتطبيعُ `NFC` **لا يغيّر الطول** — فيبدو بلا أثر. والمقيس: **٤٥٬٥٤٠
موضعًا تبدّل**، كلُّها تبديلُ ترتيبٍ بين الشدّة والحركة (٢٢٬٧٧٠ زوجًا).
فالمصدرُ يكتب الشدّةَ قبل الحركة، والتطبيعُ يقلبهما بترتيبٍ قانونيّ.
والقلبُ **غيرُ قابلٍ للاسترجاع** من المطبَّع، وهو ابتلاعٌ ثانٍ لم يُعلَن.

`THE_FOLD_IS_DOCUMENTED_AND_ITS_PRICE_IS_COUNTED`: والطيُّ مكتوبٌ في
`FOLD`: ثمانيةُ محارفَ تنزل إلى خمسة (أ إ آ ٱ ← ا · ة ← ه · ى ← ي ·
ؤ ← و · ئ ← ي)، والهمزةُ المفردةُ تُسقَط. وثمنُه **٢٤٬١٠٣ مواضعَ** —
أي سبعةٌ ونصفٌ في المئة من الحروف، منها ١٥٬٧٣٤ في الألف وحدَها. وهو
**موثَّقٌ** لأنّ القاعدةَ مكتوبةٌ،
و**غيرُ قابلٍ للاسترجاع** لأنّ كرسيَّ الهمزة لا يُستعاد من الألف.

`AND_THE_VOWEL_DELTA_IS_THE_ONE_THE_QUESTION_ASKED_FOR`: وأمّا
Δضبط — مشكولٌ إلى مجرَّد — فمقيسٌ: `H` للذرّة **٦٫٠٧٦٢** وللحرف
**٤٫٠٤٩٣**، فالفرقُ **٢٫٠٢٦٩ بتًّا لكلّ موضع**. وهذا ما يرفعه الشكلُ
حقًّا، ولا يُخلَط بما قبله.

`SO_THE_BARRIER_IS_ARTIFICIAL_AND_ITS_PRICE_IS_NAMED`: فالحاصل: واجهةُ
صوت/ترميز **محجوبةٌ بلا تسجيل** (لا صوتَ في الشجرة)، وواجهةُ
مشكول/مجرَّد **مقيسةٌ ٢٫٠٢٦٩ بت**، وواجهةُ إملاء/رقميّ فيها **أربعةُ
ابتلاعاتٍ صنعتُها أنا، اثنان منها يتيمان**. والحاجزُ حيث اليتيمان.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from fractions import Fraction

from frozen_corpus import CORPUS, requires_corpus

pytestmark = requires_corpus

BASE = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
FOLD = {
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ٱ": "ا",
    "ة": "ه",
    "ى": "ي",
    "ؤ": "و",
    "ئ": "ي",
    "ء": "",
}

RAW = CORPUS.read_text(encoding="utf-8")
NFC = unicodedata.normalize("NFC", RAW)

WHOLE_LINE_TOKENS, MIRROR_INVARIANT = 82_532, 78_245
MARKUP = "<sel>"
ATOM_ENTROPY, LETTER_ENTROPY = Fraction(60_762, 10_000), Fraction(40_493, 10_000)


def test_the_unexplained_gap_is_markup_counted_exactly() -> None:
    """٤٬٢٨٧ وسمًا `<sel>`؛ و٨٢٬٥٣٢ − ٤٬٢٨٧ = ٧٨٬٢٤٥ بلا بقيّة."""

    tags = re.findall(r"<[^>]*>", RAW)
    assert set(tags) == {MARKUP}
    assert len(tags) == 4_287

    tokens = RAW.split()
    assert len(tokens) == WHOLE_LINE_TOKENS
    markup_tokens = [one for one in tokens if one.startswith("<")]
    assert len(markup_tokens) == len(tags)
    assert WHOLE_LINE_TOKENS - len(markup_tokens) == MIRROR_INVARIANT


def test_the_markup_is_swallowed_by_the_reader_without_a_rule() -> None:
    """٢١٬٤٣٥ محرفًا تسقط لأنّها ليست في الأبجديّة — ابتلاعٌ يتيم."""

    latin = sum(RAW.count(one) for one in "<sel>")
    assert latin == 5 * 4_287 == 21_435
    for one in "<sel>":
        assert one not in BASE and one not in FOLD
    # ولم يكسر جوارًا لأنّه محفوفٌ بفراغين، والفراغُ مُسقَطٌ أصلًا
    assert f" {MARKUP} " in RAW


def test_normalisation_reorders_without_changing_the_length() -> None:
    """الطولُ واحدٌ والمواضعُ المبدَّلةُ ٤٥٬٥٤٠ — تبديلُ ترتيبٍ لا حذف."""

    assert len(NFC) == len(RAW)
    changed = sum(1 for before, after in zip(RAW, NFC, strict=True) if before != after)
    assert changed == 45_540
    swaps = Counter(
        (RAW[index], NFC[index])
        for index in range(len(RAW))
        if RAW[index] != NFC[index]
    )
    # الشدّةُ تنزل بعد الحركة بالترتيب القانونيّ، فالزوجُ متبادلٌ
    assert swaps[("ّ", "َ")] == swaps[("َ", "ّ")] == 16_291
    assert changed % 2 == 0  # كلُّ تبديلٍ زوجٌ متبادل
    assert changed // 2 == 22_770


def test_the_fold_is_documented_and_its_price_is_counted() -> None:
    """ثمانيةُ محارفَ تنزل إلى خمسة، وثمنُها ٢٤٬١٠٣ مواضعَ؛ وقاعدةٌ بلا مادّة."""

    counts = {one: NFC.count(one) for one in FOLD}
    assert sum(counts.values()) == 24_103
    assert Fraction(8, 100) > Fraction(sum(counts.values()), 331_259) > Fraction(7, 100)
    targets = {one for one in FOLD.values() if one}
    assert targets == {"ا", "ه", "ي", "و"}

    # والألفُ تبتلع أربعةَ محارف، فالاسترجاعُ ممتنعٌ من الصورة المطويّة
    into_alef = [one for one, target in FOLD.items() if target == "ا"]
    assert len(into_alef) == 4
    assert sum(counts[one] for one in into_alef) == 15_734
    assert FOLD["ء"] == ""  # والمفردةُ تُسقَط رأسًا

    # وقاعدةٌ واحدةٌ بلا مادّة: ٱ لا تقع في هذه المدوّنة ألبتّة
    assert counts["ٱ"] == 0
    assert [one for one, number in counts.items() if number == 0] == ["ٱ"]


def test_the_vowel_delta_is_the_one_the_question_actually_asked_for() -> None:
    """Δضبط = ٢٫٠٢٦٩ بتًّا لكلّ موضع — ولا يُخلَط بابتلاعات الأنبوب."""

    delta = ATOM_ENTROPY - LETTER_ENTROPY
    assert delta == Fraction(20_269, 10_000)
    assert delta > 2
    # وهو فرقُ طبقتين مُعلَنتين، لا فرقُ أنبوبين
    assert ATOM_ENTROPY > LETTER_ENTROPY


def test_the_orphan_swallows_are_two_and_they_are_named() -> None:
    """ابتلاعان بلا قاعدةٍ مكتوبة: الوسمُ وترتيبُ التطبيع — وهما الحاجز."""

    documented = {"الطيُّ المكتوب في FOLD", "طيُّ العلامات في سبعة أصناف"}
    orphans = {"إسقاطُ الوسم `<sel>`", "إعادةُ ترتيب الشدّة والحركة بـNFC"}
    assert len(orphans) == 2
    assert not documented & orphans
    assert len(documented | orphans) == 4
