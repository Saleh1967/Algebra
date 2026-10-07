"""النسخةُ ٧: **التصحيحُ أُلحِق ولم يُنشَر** — والقانونُ المشطوبُ يعمل.

**الوثيقةُ وردت هذه المرّة**، فالفحصُ يجري على بايتاتها لا على منقولٍ عنها.

`THE_STRUCK_LAW_IS_STILL_OPERATIVE_IN_TWO_PLACES`: وF13 مشطوبةٌ في §٠
ومُعلَنٌ نقضُها في §١-ط — **وهي عاملةٌ في §٣ و§٤**: جدولُ Δ يحمل «نقلَ الحالة
رفع→نصب **مع حفظ الحامل**» بحكم «Δ = ٠ كلّي» ويُسنِده إلى **Q14** (لا
Q14′)؛ و§٤ تعدّ «**حفظ رفع الحامل عند النسخ**» في باب **المقيس**. فمن دخل
الوثيقةَ من §٣ قرأ القانونَ المنقوضَ قانونًا.

`AND_THE_REFUTED_SENTENCE_SURVIVES_TWENTY_FOUR_LINES_ABOVE_ITS_RETRACTION`:
و«**منطقةُ الانعكاس هي العقدُ الأوّلُ وحدَه**» قائمةٌ في §١-ك، وQ16′ تعلن
بطلانَها بعدَها بأربعةٍ وعشرين سطرًا. فالنصُّ يقول الشيءَ ونقيضَه، والترتيبُ
وحدَه يفصل.

`A_CORRECTION_THAT_DOES_NOT_PROPAGATE_IS_A_SEVENTH_GENUS`: وهذا **جنسُ عطلٍ
سابع** يلحق بالستّة: **التصحيحُ المُلحَقُ لا المنشور**. وهو أخطرُ من الخطأ
المفرد، لأنّ الوثيقةَ تبدو مصحَّحةً وتظلّ عاملةً بالمنقوض؛ وهو **نفسُ بنية**
«٩ صوابُها ١٢» التي مرّت أربعَ دورات. وقاعدةُ §١-م نفسُها تُنتهَك على
الصفحة التي تُعلنها: ما صُحِّح في الصفحة يُنشَر كاملًا قبل أن يُبنى عليه.

`AND_THE_ASSUMPTION_TABLE_DISAGREES_WITH_ITS_OWN_TABLE`: وF17 في §٠ تنصّ
على **خمسةِ مديات** («العقودُ والمئاتُ محايدة»)، و§١-ك تعرض **ستّة** (العقودُ
٢٠–٩٠ صفًّا، ومئة/ألف صفًّا). فالانشطارُ وقع في الجدول ولم يقع في فرضه —
و§٤ تعدّ **٦** فتوافق الجدولَ وتخالف الفرض.

`AND_ONLY_ONE_OF_THREE_REFUTED_ASSUMPTIONS_IS_STRUCK`: وF13 وحدَها نالت
الشطبَ، وF17 وF18 **قائمتان بلا علامة** وإن أعلنت Q16′ وQ17′ بطلانَهما.
فالمعاملةُ غيرُ مطّردة، وعلامةُ الشطب — وهي أحسنُ ما في المنهج — تُطبَّق
على واحدٍ من ثلاثة.

`THE_NINE_MARKERS_ARE_FOUR_PLUS_FIVE_AND_THE_FIVE_OMIT_THREE`: و«٩ علامات»
صارت **مشتقّةً** في §١-ب (٤ أصليّة + ٥ فرعيّة) — وهذا كسبٌ: العددُ يُحسب
بعدَ أن كان يُساق. والفرعيّاتُ المعدودةُ خمس (واو، ألف، ياء، نون، حذفُ
النون)، **وثلاثٌ ساقطةٌ منها كلُّها مشهودةٌ في المدوّنة**: الكسرةُ نيابةً عن
الفتحة في جمع المؤنّث السالم («إنّ المسلمينَ **والمسلماتِ**»)، والفتحةُ
نيابةً عن الكسرة في الممنوع من الصرف («ملّةِ **إبراهيمَ**» — ستّةُ مواضع)،
وحذفُ حرف العلّة في جزم المعتلّ («**ولا تدعُ** مع الله») مقابلَ السكون في
الصحيح («**ولم يكن** له كفوًا أحد»). فالفرعيّاتُ **ثمانٍ**، والعلاماتُ
**١٢** لا ٩ — والفرقُ ٣، مشهودٌ لا مُدَّعًى.
"""

from __future__ import annotations

import re
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

REPOSITORY = Path(__file__).resolve().parents[2]
DOCUMENT = REPOSITORY / "deposits" / "hamil_hala_zaman_layers_v7.md"
MARKS = re.compile(r"[ً-ْٰـ]")

PRIMARY = ("ضمّة", "فتحة", "كسرة", "سكون")
COUNTED_SECONDARY = ("واو", "ألف", "ياء", "نون", "حذف النون")
OMITTED_SECONDARY = {
    "كسرة نيابة عن فتحة": "والمسلمات والمؤمنين",
    "فتحة نيابة عن كسرة": "ملة إبراهيم",
    "حذف حرف العلة": "ولا تدع مع الله",
}


def _document() -> str:
    return DOCUMENT.read_text(encoding="utf-8")


def _bare() -> list[str]:
    text = CORPUS.read_text(encoding="utf-8")
    return [MARKS.sub("", line) for line in text.splitlines()]


def _attested(needle: str) -> int:
    return sum(1 for line in _bare() if needle in line)


def test_the_struck_law_is_still_operative_in_the_delta_table() -> None:
    """§٠ تشطبها و§٣ تعمل بها، وتُسنِدها إلى Q14 لا Q14′."""

    text = _document()
    assert "~~F13~~" in text and "منقوض في v6" in text
    delta_rows = [line for line in text.splitlines() if line.startswith("| جملة حرّة")]
    assert len(delta_rows) == 1
    assert "مع حفظ الحامل" in delta_rows[0]
    assert "Q14 |" in delta_rows[0] and "Q14′" not in delta_rows[0]


def test_the_struck_law_is_also_counted_among_the_measured() -> None:
    """§٤ تعدّ «حفظ رفع الحامل عند النسخ» مقيسًا — وهو منقوض."""

    text = _document()
    measured = [line for line in text.splitlines() if "مقيس/معدود" in line]
    assert len(measured) == 1
    assert "حفظ رفع الحامل عند النسخ" in measured[0]


def test_the_refuted_sentence_survives_above_its_own_retraction() -> None:
    """«العقدُ الأوّلُ وحدَه» في §١-ك، وبطلانُها في Q16′ بعدَها."""

    lines = _document().splitlines()
    claim = [
        n
        for n, line in enumerate(lines)
        if "منطقة الانعكاس هي العقد الأول وحده" in line
    ]
    retraction = [
        n for n, line in enumerate(lines) if "Q16′" in line and "باطلة" in line
    ]
    assert len(claim) == 1 and len(retraction) == 1
    assert claim[0] < retraction[0]
    assert retraction[0] - claim[0] == 24


def test_the_assumption_and_its_table_count_differently() -> None:
    """F17 خمسةُ مديات، والجدولُ ستّة، و§٤ تعدّ ستّة."""

    text = _document()
    assumption = [line for line in text.splitlines() if line.startswith("| F17 ")]
    assert len(assumption) == 1
    assert "العقود والمئات محايدة" in assumption[0]
    assert "| العقود ٢٠–٩٠ | محايدة" in text
    assert "| مئة/ألف | محايدة" in text
    assert "ومديات القطبية ٦" in text


def test_only_one_of_three_refuted_assumptions_carries_the_strike() -> None:
    """F13 مشطوبة، وF17 وF18 قائمتان — والبطلانُ معلنٌ للثلاث."""

    text = _document()
    assert "~~F13~~" in text
    assert "| F17 |" in text and "~~F17~~" not in text
    assert "| F18 |" in text and "~~F18~~" not in text
    for law in ("Q16′", "Q17′"):
        assert law in text and "باطلة" in text


@requires_corpus
def test_the_five_secondary_markers_omit_three_that_the_corpus_shows() -> None:
    """٤ + ٨ = ١٢، والثلاثُ الساقطةُ مشهودةٌ واحدةً واحدة."""

    assert len(PRIMARY) == 4
    assert len(COUNTED_SECONDARY) == 5
    assert "والعلامات ٤+٥=٩" in _document()
    for witness in OMITTED_SECONDARY.values():
        assert _attested(witness) >= 1
    assert _attested("ملة إبراهيم") == 6
    assert _attested("ولم يكن له كفوا أحد") == 1  # السكونُ في الصحيح مقابلًا
    secondary = len(COUNTED_SECONDARY) + len(OMITTED_SECONDARY)
    assert secondary == 8
    assert len(PRIMARY) + secondary == 12


def test_the_document_carries_the_plateau_figure_correctly() -> None:
    """الوثيقةُ تكتب ٠٫٠٠١٥٩ — وهو الصحيح."""

    text = _document()
    assert "٠٫٠٠١٥٩" in text
    assert "٠٫٠١٥٩" not in text
