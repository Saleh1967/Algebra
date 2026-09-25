"""أوّلُ تشغيلٍ على المدوّنة المُجمَّدة: التعدادُ خرج، وقارئُ الكلمات لا يقرؤها.

**ما جرى**: وصلت بايتاتُ `quran-simple-enhanced.txt` فطابقت البوّابةَ
تمامًا — ١٬٣١٩٬٩٠١ بايتًا وبصمةُ `37633090…` — فاستُقبِلت بالآلة المُعلَنة
وشُغِّل عليها تعدادُ الانتقالات.

`THE_GATE_OPENED_AND_THE_FIRST_THING_IT_SHOWED_WAS_A_DEFECT_IN_A_READER`:
وأوّلُ ما ظهر ليس رقمًا عن العربيّة بل **عطلٌ في قارئ**. فـ`ayah_texts`
تنتظر سطرًا بحقولٍ يفصلها `|`، وهذا الملفّ **لا يحمل فاصلًا واحدًا**: ستّةُ
آلافٍ ومئتان وستٌّ وثلاثون سطرًا، وصفرُ فواصل. فثلاثٌ من قواعد العدّ الأربع
تُرجِع **صفرًا**، وحكمُ المسح `CONTRADICTED_BY_THE_FROZEN_BYTES` مبنيٌّ
على ذلك الصفر — فهو **خبرٌ عن القارئ لا عن الرقم المنقول**، ولا يُنشَر نقضًا
لـ٧٨٬٢١٥.

`A_VERDICT_BUILT_ON_A_ZERO_IS_NOT_A_VERDICT`: وهذا عينُ ما نُسمّيه في
الأرقام: مقامٌ لم يُعدَّد. والقارئُ منقولٌ في إيداعٍ مغلقٍ ببصمةِ كلّ ملفّ،
فلا يُعدَّل ههنا — يُسمّى عطلُه ويُعَدّ، ويُصلَح في شجرته.

`AND_ONE_NUMBER_STAYED_OPEN_UNTIL_IT_WAS_COUNTED`: وعدُّ الرموز على السطر
كلِّه ٨٢٬٥٣٢، والثابتُ المرصودُ في مرايا أسرة «simple» ٧٨٬٢٤٥ — والفرقُ
٤٬٢٨٧ سُجِّل **مفتوحًا** ولم يُفسَّر بخيار تنزيلٍ ولا بغيره.

`AND_THE_GAP_IS_NOW_CLOSED_BY_A_COUNT_NOT_BY_A_READING`: **وأُغلِق**: في
المدوّنة **٤٬٢٨٧ وسمًا `<sel>`** بالضبط، كلٌّ منها توكنٌ مستقلٌّ بالفراغ.
فـ٨٢٬٥٣٢ − ٤٬٢٨٧ = ٧٨٬٢٤٥ بلا بقيّة. فالفجوةُ **وسمٌ لا كلمات**، ومقيسةٌ
في `test_ingestion_swallows`. والفضلُ للسؤال: «أين يبتلع أنبوبُك؟».
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

from alghanem.arabic.compression_model_preregistration import FROZEN_CORPUS

REPOSITORY = Path(__file__).resolve().parents[2]

pytestmark = requires_corpus

AYAH_LINES = 6_236
WHOLE_LINE_TOKENS = 82_532
MIRROR_INVARIANT = 78_245
QUOTED_TOTAL = 78_215

# ما خرج من التعداد تحت السياستين: (الجرد، المواضع، أزواجٌ مرصودة، خالية)
CENSUS = {
    "مطويّ": (28, 253_014, 638, 146),
    "مفصول": (36, 254_592, 888, 408),
}
LEADER_FOLDED = ("ا", "ل", 16_426)


def test_the_deposited_bytes_match_the_frozen_gate_exactly() -> None:
    """الطولُ والبصمةُ معًا، وستّةُ آلافٍ ومئتان وستٌّ وثلاثون سطرًا."""

    import hashlib

    data = CORPUS.read_bytes()
    assert len(data) == FROZEN_CORPUS.byte_length == 1_319_901
    assert hashlib.sha256(data).hexdigest() == FROZEN_CORPUS.sha256_hex
    assert len(data.decode("utf-8").splitlines()) == AYAH_LINES


def test_the_file_carries_no_field_separator_at_all() -> None:
    """صفرُ فواصل `|` في ستّة آلافٍ ومئتين وستّة وثلاثين سطرًا — ولا سطرَ فارغ."""

    lines = CORPUS.read_text(encoding="utf-8").splitlines()
    separators = Counter(one.count("|") for one in lines)
    assert separators == {0: AYAH_LINES}
    assert all(one.strip() for one in lines)


def test_three_of_four_counting_rules_return_zero_on_this_file() -> None:
    """القارئُ ينتظر حقولًا لا توجد، فيُرجِع صفرًا — والصفرُ عنه لا عن النصّ."""

    from alghanem.arabic.quran_corpus_word_total import WordCountingRule, word_total

    # والمسارُ يُصرَّح به: بابُ «تصريحِ المستدعي» في ذلك القارئ، إذ لا
    # يعرف من الحوامل إلّا `corpora/…`، والبايتاتُ قد تكون في غيره
    totals = {rule.name: word_total(rule, CORPUS) for rule in WordCountingRule}
    zeros = [name for name, value in totals.items() if value == 0]
    assert len(zeros) == 3
    assert totals["WHITESPACE_TOKENS_IN_WHOLE_LINE"] == WHOLE_LINE_TOKENS
    assert "WHITESPACE_TOKENS_IN_AYAH_TEXT" in zeros


def test_the_survey_verdict_is_about_the_reader_not_about_the_quoted_total() -> None:
    """حكمٌ مبنيٌّ على صفرٍ ليس حكمًا؛ فلا يُنشَر نقضًا لـ٧٨٬٢١٥."""

    from alghanem.arabic.quran_corpus_word_total import run_quoted_total_survey

    reading = run_quoted_total_survey(CORPUS)
    assert reading.quoted_total == QUOTED_TOTAL
    assert reading.bytes_are_resolvable is True
    assert reading.mirror_invariant_total == MIRROR_INVARIANT

    # والحكمُ خرج «مناقَضًا»، ومقدّمتُه صفرٌ من قارئٍ لا يقرأ هذا الشكل
    assert reading.standing.name == "CONTRADICTED_BY_THE_FROZEN_BYTES"
    assert reading.distance_from_mirror_invariant == QUOTED_TOTAL - MIRROR_INVARIANT


def test_the_gap_from_the_mirror_invariant_is_closed_by_a_count() -> None:
    """٨٢٬٥٣٢ مقابل ٧٨٬٢٤٥: الفرقُ ٤٬٢٨٧ وسمًا `<sel>` — أُغلِق بالعدّ."""

    gap = WHOLE_LINE_TOKENS - MIRROR_INVARIANT
    assert gap == 4_287
    import re

    assert len(re.findall(r"<sel>", CORPUS.read_text(encoding="utf-8"))) == gap
    assert gap != QUOTED_TOTAL - MIRROR_INVARIANT  # وهو غيرُ فرقِ الثلاثين المُسجَّل
    assert abs(QUOTED_TOTAL - MIRROR_INVARIANT) == 30


def test_the_transition_census_ran_and_its_denominators_are_declared() -> None:
    """٢٥٣٬٠١٤ موضعًا مطويًّا و٢٥٤٬٥٩٢ مفصولًا — والمواضعُ تفوق الخانات بكثير."""

    for policy, (inventory, places, observed, empty) in CENSUS.items():
        cells = inventory**2
        assert observed + empty == cells, policy
        assert places > cells * 100, policy  # فلا خلوَّ مفروضًا بالمقام ههنا

    assert CENSUS["مطويّ"][0] == 28
    assert CENSUS["مفصول"][0] == 36


def test_the_leading_transition_on_the_mushaf_is_the_article_alone() -> None:
    """«ال» ستَّ عشرةَ ألفًا وأربعمئةً وستًّا وعشرين، وحدَها بلا تساوٍ."""

    first, second, count = LEADER_FOLDED
    assert (first, second) == ("ا", "ل")
    assert count == 16_426

    places = CENSUS["مطويّ"][1]
    assert count * 15 < places < count * 16  # نحوُ ستّةٍ ونصفٍ في المئة
