"""الرقم 78,215: بابُ مدوّنته، وقاعدةُ عدِّه، ومنزلتُه بعد المسح.

يَرِد في هذه الشجرة رقمٌ واحدٌ منقولٌ عن نصٍّ خارجيّ — **78,215** — مسنوبًا
إلى مدوّنة `quran-simple-enhanced.txt` في
`docs/reference/word_hierarchy_rebuild.md`، ومُسجَّلًا في
`gflk_specification_deposit` أنّ الأربعةَ المُودَعة تجمع 78,081 فيبقى فرقُ
134 لا تحسمه الشجرة. وهذه الوحدة لا تحسم الفرقَ أيضًا، لكنّها تنقل الرقمَ من
**مجهول القاعدة** إلى **معلوم الموضع من قاعدةٍ مقيسة**، فتفترق ههنا أربعةٌ
كانت تُقرأ رقمًا واحدًا::

    ADigestedSource       != ResolvableBytes
    AQuotedTotal          != ARecomputedTotal
    AMirrorMeasurement    != TheFrozenBytes
    AByteOption           != ACountingRule

**أوّلًا: بابُ هذه المدوّنة لم يكن مبنيًّا أصلًا.** `FROZEN_CORPUS` يحمل
الطولَ والبصمةَ والترميز، و`decode_corpus_bytes` تُطابق عليهما قبل أيّ فكِّ
ترميز — غير أنّ الشجرة لم تكن فيها **دالّةٌ تَحُلّ مسارًا** إلى تلك البايتات،
ولا موضعٌ مسنونٌ في `corpora/`، ولا مثالٌ يُشغَّل. فبوّابةُ البصمة كانت قائمةً
على بابٍ لا يُفتَح. وههنا يُبنى البابُ بترتيب مصادرَ مسنونٍ كترتيب MASAQ:
المُمرَّرُ، ثمّ `ALGHANEM_QURAN_CORPUS_PATH`، ثمّ الموضعُ المُودَع، ولا رابعَ
(`A_DIGEST_WITHOUT_A_RESOLVER_IS_A_GATE_ON_NO_DOOR`).

**ثانيًا: لا رقمَ بغير البايتات المبصومة.** `word_total()` لا تُخرِج عددًا
إلّا بعد مطابقةِ الطول والبصمة معًا؛ وغيابُ البايتات **رفضُ إخراجٍ** لا قيمةٌ
افتراضيّة، وملفٌّ مُحَلٌّ مخالفُ البصمة يَفشَل ولا يُتخطّى
(`NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES`).

**ثالثًا: العدُّ لا يكون بلا قاعدةٍ مُعلَنة.** «عددُ الكلمات» ليس وصفًا
مُحدِّدًا: يختلف العددُ باختلاف ما يُعَدّ سطرًا، وما يُقتطَع حقلًا، وما
يُعَدّ فاصلًا. فأُعلِنت القواعدُ في `WordCountingRule` قبل أيّ قياس، وكلُّ
عددٍ يخرج من هنا يحمل قاعدتَه معه (`A_COUNT_WITHOUT_A_DECLARED_RULE_IS_NOT_A_COUNT`).

**رابعًا: المسحُ العامّ أخرج نتيجةً، لا عجزًا.** طُلِبت نسخةٌ عامّةٌ تطابق
`1,319,901` بايتًا فلم تُوجَد في المرايا المفحوصة؛ ثمّ قِيست خمسُ مرايا
بأنفسها، فخرج عددُ الرموز البيضاء **78,245 ثابتًا** عبر أسرة «simple» كلِّها
— على اختلاف أطوالها وبصماتها وفواصل أسطرها — و**77,878** في العثمانيّ. وهذا
يُثبت أنّ عددَ الرموز **لا يتغيّر بخيارات العلامات** التي تُغيّر الطول؛ فلا
يُفسَّر فرقُ 78,215 عن 78,245 بخيار تنزيل. والفرقُ ثلاثون، وهو **غيرُ
محسومٍ ههنا**: لم تُبلَغ قاعدةُ عدٍّ تُخرِجه، ولم تصل البايتاتُ التي قِيس
عليها (`THE_TOKEN_TOTAL_IS_INVARIANT_UNDER_THE_MARK_OPTIONS`).

**خامسًا: المرآةُ قرينةٌ لا بديل.** ما قِيس أعلاه قِيس على بايتاتٍ **مُصرَّحٍ
بأنّها ليست المُجمَّدة**: بصماتُها مسجَّلةٌ ومخالفةٌ، وتسجيلُها قرينةٌ على
استقرار قاعدة العدّ لا شهادةٌ على المدوّنة المقصودة
(`A_MIRROR_IS_A_CORROBORATION_NOT_A_SUBSTITUTE`).

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

from .compression_model_preregistration import FROZEN_CORPUS
from .pipeline_stations import repository_root_path

__all__ = [
    "strip_diacritics",
    "muqattaat_occurrences",
    "assess_gap_account",
    "MuqattaatOccurrence",
    "GapAccountStanding",
    "GapAccountReading",
    "THE_THIRTY_ARE_THE_DISJOINED_LETTERS_NOTE",
    "THE_RULE_IS_NOT_FITTED_TO_ITS_RESULT_NOTE",
    "THE_MUQATTAAT_FORMS",
    "THE_BASMALA_IS_INLINE_IN_THIS_CORPUS_NOTE",
    "THE_ACCOUNT_IS_TIED_TO_THE_ORTHOGRAPHY_NOTE",
    "AN_EXACT_MATCH_IS_NOT_A_UNIQUE_ACCOUNT_NOTE",
    "AN_ACCOUNT_OF_THE_GAP_IS_NOT_A_REDERIVATION_NOTE",
    "AYAH_FIELD_SEPARATOR",
    "A_COUNT_WITHOUT_A_DECLARED_RULE_IS_NOT_A_COUNT_NOTE",
    "A_DIGEST_WITHOUT_A_RESOLVER_IS_A_GATE_ON_NO_DOOR_NOTE",
    "A_MIRROR_IS_A_CORROBORATION_NOT_A_SUBSTITUTE_NOTE",
    "A_SURVEY_IS_NOT_A_PROHIBITION_NOTE",
    "NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE",
    "QURAN_CORPUS_NAMED_RESIDUALS",
    "QURAN_CORPUS_PATH_VARIABLE",
    "QURAN_CORPUS_RELATIVE_PATH",
    "SURVEYED_MIRRORS",
    "THE_ONE_HUNDRED_AND_THIRTY_FOUR_IS_NOT_THE_THIRTY_NOTE",
    "THE_QUOTED_WORD_TOTAL",
    "THE_TOKEN_TOTAL_IS_INVARIANT_UNDER_THE_MARK_OPTIONS_NOTE",
    "MirrorMeasurement",
    "QuotedTotalStanding",
    "QuranCorpusError",
    "SurveyReading",
    "WordCountingRule",
    "ayah_texts",
    "count_words",
    "quran_corpus_bytes_are_resolvable",
    "quran_corpus_path",
    "read_quran_corpus_bytes",
    "run_quoted_total_survey",
    "vendored_quran_corpus_path",
    "word_total",
]


class QuranCorpusError(ValueError):
    """رفضٌ في باب المدوّنة: مسارٌ لا يُحَلّ، أو بايتاتٌ لا تطابق المُجمَّد."""


QURAN_CORPUS_RELATIVE_PATH: Final[str] = "corpora/quran-simple-enhanced.txt"
"""الموضعُ المسنونُ للبايتات داخل الشجرة، وليس فيها الآن."""

QURAN_CORPUS_PATH_VARIABLE: Final[str] = "ALGHANEM_QURAN_CORPUS_PATH"
"""متغيّرُ البيئة الذي يُصرَّح به بالمسار حين تكون البايتاتُ خارج الشجرة."""

AYAH_FIELD_SEPARATOR: Final[str] = "|"
"""فاصلُ حقول تنزيل تنزيل: `sura|ayah|text`، وهو المُعلَن لا المُخمَّن."""

THE_QUOTED_WORD_TOTAL: Final[int] = 78_215
"""الرقمُ المنقول، محفوظًا بحروفه؛ وحفظُه ليس تصديقَه."""


def vendored_quran_corpus_path() -> Path:
    """الموضعُ المسنونُ داخل الشجرة، محسوبًا لا مُخمَّنًا من `cwd`."""

    return repository_root_path() / QURAN_CORPUS_RELATIVE_PATH


def quran_corpus_path(path: Path | str | None = None) -> Path:
    """مسارُ البايتات: المُمرَّرُ، وإلّا متغيّرُ البيئة، وإلّا المُودَعُ في الشجرة.

    والترتيبُ مقصودٌ كترتيب `masaq_path`: تصريحُ المستدعي أوّلًا، ثمّ تصريحُ
    البيئة، ثمّ الموضعُ المسنونُ **إن كان موجودًا فعلًا**. وغيابُ الثلاثة
    رفضٌ صريحٌ لا قيمةٌ افتراضيّة.
    """

    if path is not None:
        return Path(path)
    declared = os.environ.get(QURAN_CORPUS_PATH_VARIABLE)
    if declared:
        return Path(declared)
    vendored = vendored_quran_corpus_path()
    if vendored.is_file():
        return vendored
    raise QuranCorpusError(
        "بايتاتُ المدوّنة ليست في هذه الشجرة ولا صُرِّح بمسارها؛ فتُودَع في "
        f"`{QURAN_CORPUS_RELATIVE_PATH}` أو يُصرَّح به في "
        f"`{QURAN_CORPUS_PATH_VARIABLE}`، ولا يُخمَّن موضعُها."
    )


def quran_corpus_bytes_are_resolvable(path: Path | str | None = None) -> bool:
    """أيُحَلُّ مسارٌ إلى ملفٍّ **موجود** بأبواب `quran_corpus_path` الثلاثة؟

    وهذا شرطُ التخطّي وحدَه، لا خلوُّ متغيّر البيئة: فمتغيّرٌ مضبوطٌ على مسارٍ
    لا ملفَّ فيه ليس بايتاتٍ حاضرة، وملفٌّ مُحَلٌّ مخالفُ البصمة **لا يُتخطّى**
    بل يَفشَل في `read_quran_corpus_bytes`.
    """

    try:
        resolved = quran_corpus_path(path)
    except QuranCorpusError:
        return False
    return resolved.is_file()


def read_quran_corpus_bytes(path: Path | str | None = None) -> bytes:
    """يقرأ البايتات ويُطابق الطولَ والبصمةَ معًا قبل أن يُسلِّمها.

    والموضعُ ليس شهادة: ملفٌّ بهذا الاسم في الموضع المسنون يُرفَض كما يُرفَض
    في أيّ مسارٍ آخر إن خالف، والموافقةُ في الطول وحدَه لا تُغني عن البصمة.
    """

    resolved = quran_corpus_path(path)
    if not resolved.is_file():
        raise QuranCorpusError(f"لا ملفَّ في المسار المُحَلّ: {resolved}")
    data = resolved.read_bytes()
    if len(data) != FROZEN_CORPUS.byte_length:
        raise QuranCorpusError(
            f"طولُ البايتات {len(data)} لا يطابق المُجمَّد " f"{FROZEN_CORPUS.byte_length}"
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != FROZEN_CORPUS.sha256_hex:
        raise QuranCorpusError(
            f"بصمةُ البايتات {digest} لا تطابق المُجمَّد {FROZEN_CORPUS.sha256_hex}"
        )
    return data


class WordCountingRule(Enum):
    """قواعدُ العدّ، مُعلَنةٌ قبل القياس؛ ولا يخرج عددٌ من هنا بلا واحدةٍ منها."""

    WHITESPACE_TOKENS_IN_AYAH_TEXT = "رموزٌ يفصلها بياضٌ في حقل النصّ وحدَه"
    """يُقتطَع الحقلُ الثالثُ من كلّ سطر آيةٍ ثمّ يُقسَم بـ`split()`."""

    WHITESPACE_TOKENS_IN_WHOLE_LINE = "رموزٌ يفصلها بياضٌ في السطر كلِّه"
    """لا يُقتطَع حقلٌ: يُعَدّ رقما السورة والآية والفاصلُ رموزًا كسائرها."""

    AYAH_LINES = "أسطرُ الآيات: ما فيه فاصلا حقلٍ وليس بتعليق"
    """ليس عدَّ كلماتٍ أصلًا، وإنّما مقامُ العدّ؛ ويُسجَّل معه ليُفحَص."""

    WHITESPACE_TOKENS_EXCLUDING_MUQATTAAT = (
        "رموزٌ يفصلها بياضٌ في حقل النصّ، مطروحًا منها فواتحُ السور المقطَّعة"
    )
    """القاعدةُ التي تُخرِج الثلاثين؛ وليست حذفًا بل تمييزُ ما ليس بكلمة.

    فالحروفُ المقطَّعةُ لا جذرَ لها ولا وزنَ ولا بِنيةَ صرفيّة، فخروجُها من
    عدّ الكلمات مقتضى بابها لا معالجةً للفرق.
    """


THE_MUQATTAAT_FORMS: Final[frozenset[str]] = frozenset(
    {
        "الم",
        "المص",
        "الر",
        "المر",
        "كهيعص",
        "طه",
        "طسم",
        "طس",
        "يس",
        "ص",
        "حم",
        "عسق",
        "ق",
        "ن",
    }
)
"""صورُ فواتح السور المقطَّعة الأربعَ عشرةَ، مجرّدةً من التشكيل.

وهي القائمةُ المعروفةُ قبل هذا القياس لا مُستخرَجةٌ منه؛ وكلُّ صورةٍ منها
واقعةٌ في المدوّنة فعلًا، فلا مدخلَ ميّتٌ يُوهِم ضبطًا.
"""

_DIACRITICS: Final[frozenset[str]] = frozenset(
    chr(point) for point in range(0x64B, 0x653)
)


def strip_diacritics(token: str) -> str:
    """صورةُ الرمز مجرّدةً من التشكيل، ولا يُمَسّ منها حرفٌ."""

    return "".join(char for char in token if char not in _DIACRITICS)


@dataclass(frozen=True)
class MuqattaatOccurrence:
    """موقعُ فاتحةٍ مقطَّعةٍ بعينه: سورتُها وآيتُها وصورتُها ورتبتُها في الآية."""

    sura: int
    ayah: int
    index_in_ayah: int
    form: str


def muqattaat_occurrences(text: str) -> tuple[MuqattaatOccurrence, ...]:
    """مواقعُ الفواتح المقطَّعة في المدوّنة كلِّها، **بلا تقييدٍ موضعيّ**.

    ولا تُقيَّد المطابقةُ بصدر السورة ولا بالآيتين الأوليين: تُمسَح المدوّنةُ
    كلُّها، فإن لم تُصِب المطابقةُ إلّا الفواتحَ فذلك **نتيجةُ قياسٍ** لا
    شرطٌ وُضِع ليُخرِجها. وتقييدُها بالموضع كان يجعل القاعدةَ مُفصَّلةً على
    ما تُراد له (`THE_RULE_IS_NOT_FITTED_TO_ITS_RESULT`).
    """

    found: list[MuqattaatOccurrence] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.count(AYAH_FIELD_SEPARATOR) < 2:
            continue
        sura_field, ayah_field, body = stripped.split(AYAH_FIELD_SEPARATOR, 2)
        if not (sura_field.isdigit() and ayah_field.isdigit()):
            continue
        for index, token in enumerate(body.split()):
            form = strip_diacritics(token)
            if form in THE_MUQATTAAT_FORMS:
                found.append(
                    MuqattaatOccurrence(
                        sura=int(sura_field),
                        ayah=int(ayah_field),
                        index_in_ayah=index,
                        form=form,
                    )
                )
    return tuple(found)


def ayah_texts(text: str) -> tuple[str, ...]:
    """نصوصُ الآيات وحدَها: ما كان فيه فاصلا حقلٍ وليس سطرَ تعليقٍ ولا خاليًا.

    وكتلةُ رخصة تنزيل في ذيل الملفّ تُستبعَد بأنّها تعليق (`#`)، لا بعدِّ
    أسطرٍ من الذيل: فحذفُ عددٍ ثابتٍ من الأسطر قاعدةٌ تنكسر بصمتٍ عند نسخةٍ
    أخرى، وهذه لا تنكسر صامتةً.
    """

    collected: list[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.count(AYAH_FIELD_SEPARATOR) < 2:
            continue
        collected.append(stripped.split(AYAH_FIELD_SEPARATOR, 2)[2])
    return tuple(collected)


def count_words(text: str, rule: WordCountingRule) -> int:
    """العدُّ تحت قاعدةٍ مُعلَنة، والقاعدةُ وسيطٌ إلزاميٌّ لا افتراضيّ."""

    if rule is WordCountingRule.WHITESPACE_TOKENS_IN_AYAH_TEXT:
        return sum(len(item.split()) for item in ayah_texts(text))
    if rule is WordCountingRule.WHITESPACE_TOKENS_IN_WHOLE_LINE:
        return sum(
            len(line.split())
            for line in text.split("\n")
            if line.strip() and not line.strip().startswith("#")
        )
    if rule is WordCountingRule.WHITESPACE_TOKENS_EXCLUDING_MUQATTAAT:
        return sum(len(item.split()) for item in ayah_texts(text)) - len(
            muqattaat_occurrences(text)
        )
    return len(ayah_texts(text))


def word_total(
    rule: WordCountingRule = WordCountingRule.WHITESPACE_TOKENS_IN_AYAH_TEXT,
    path: Path | str | None = None,
) -> int:
    """عددُ الكلمات من البايتات المبصومة وحدَها، تحت قاعدةٍ مُعلَنة.

    ولا قيمةَ افتراضيّةَ عند غياب البايتات: يُرفَع `QuranCorpusError`.
    """

    data = read_quran_corpus_bytes(path)
    return count_words(data.decode("utf-8"), rule)


@dataclass(frozen=True)
class MirrorMeasurement:
    """ما قِيس على مرآةٍ عامّةٍ **ببصمةٍ أخرى**، مُصرَّحًا بأنّه ليس المُجمَّدة."""

    mirror_name: str
    mirror_byte_length: int
    mirror_sha256_prefix: str
    ayah_lines: int
    whitespace_tokens: int
    muqattaat_tokens: int

    def __post_init__(self) -> None:
        if not 0 <= self.muqattaat_tokens <= self.whitespace_tokens:
            raise QuranCorpusError(
                "عددُ الفواتح المقطَّعة لا يكون سالبًا ولا يتجاوز عددَ الرموز."
            )
        if self.mirror_byte_length == FROZEN_CORPUS.byte_length:
            raise QuranCorpusError(
                f"مرآةٌ بطول المُجمَّد ({self.mirror_byte_length}) ليست مرآةً "
                "أخرى؛ فإن كانت هي فتُقاس بابَ البايتات لا بابَ المرايا."
            )
        if not self.mirror_sha256_prefix:
            raise QuranCorpusError("مرآةٌ بلا بادئةِ بصمةٍ لا تُسجَّل مرآةً.")
        if FROZEN_CORPUS.sha256_hex.startswith(self.mirror_sha256_prefix):
            raise QuranCorpusError("مرآةٌ ببادئة بصمة المُجمَّد لا تُسجَّل مرآةً.")

    def matches_quoted_total(self) -> bool:
        """أيُخرِج عددُ رموز هذه المرآة الرقمَ المنقول بلا استثناءِ شيء؟"""

        return self.whitespace_tokens == THE_QUOTED_WORD_TOTAL

    def tokens_excluding_muqattaat(self) -> int:
        """عددُ الرموز بعد تمييز ما ليس بكلمةٍ من فواتح السور."""

        return self.whitespace_tokens - self.muqattaat_tokens

    def account_reaches_the_quoted_total(self) -> bool:
        """أتبلغ هذه المرآةُ الرقمَ المنقولَ تحت قاعدة استثناء الفواتح؟"""

        return self.tokens_excluding_muqattaat() == THE_QUOTED_WORD_TOTAL


SURVEYED_MIRRORS: Final[tuple[MirrorMeasurement, ...]] = (
    MirrorMeasurement(
        mirror_name="drnesr/QuranDataset — quran-simple-enhanced.txt",
        mirror_byte_length=1_331_429,
        mirror_sha256_prefix="31a71ecae9273530",
        ayah_lines=6_236,
        whitespace_tokens=78_245,
        muqattaat_tokens=30,
    ),
    MirrorMeasurement(
        mirror_name="rizaumami/quran-epub — quran-simple-enhanced.txt (CRLF)",
        mirror_byte_length=1_337_695,
        mirror_sha256_prefix="8a22d96de8351a2e",
        ayah_lines=6_236,
        whitespace_tokens=78_245,
        muqattaat_tokens=30,
    ),
    MirrorMeasurement(
        mirror_name="drnesr/QuranDataset — quran-simple.txt",
        mirror_byte_length=1_337_820,
        mirror_sha256_prefix="7b2b601fa5e9b825",
        ayah_lines=6_236,
        whitespace_tokens=78_245,
        muqattaat_tokens=30,
    ),
    MirrorMeasurement(
        mirror_name="drnesr/QuranDataset — quran-simple-min.txt",
        mirror_byte_length=1_160_550,
        mirror_sha256_prefix="9afe44e4717223c1",
        ayah_lines=6_236,
        whitespace_tokens=78_245,
        muqattaat_tokens=30,
    ),
    MirrorMeasurement(
        mirror_name="drnesr/QuranDataset — quran-uthmani.txt",
        mirror_byte_length=1_370_238,
        mirror_sha256_prefix="9cae2cb7e075379e",
        ayah_lines=6_236,
        whitespace_tokens=77_878,
        muqattaat_tokens=1,
    ),
)
"""خمسُ مرايا قِيست بأنفسها، أطوالُها وبصماتُها مخالفةٌ للمُجمَّد كلُّها."""


class GapAccountStanding(Enum):
    """منزلةُ حسابِ الثلاثين، وهي غيرُ منزلة الرقم المنقول نفسِه."""

    REPRODUCED_ON_EVERY_SIMPLE_MIRROR = "بلغت الرقمَ كلُّ مرايا أسرة «simple»"
    """قاعدةُ استثناء الفواتح أخرجت 78,215 من كلّ مرآةٍ من الأسرة، بلا استثناء."""

    REPRODUCED_ON_SOME_MIRRORS = "بلغته بعضُ المرايا دون بعض"
    """بلوغٌ جزئيّ؛ وهو أضعفُ من الأوّل ولا يُقرأ مكانَه."""

    NOT_REPRODUCED = "لم تبلغه مرآةٌ"
    """لا تُخرِج القاعدةُ الرقمَ من شيءٍ مقيس، فالحسابُ ساقط."""


@dataclass(frozen=True)
class GapAccountReading:
    """قراءةُ حسابِ الثلاثين: ما بلغ، وما انكسر، وما بقي غيرَ مُثبَت."""

    standing: GapAccountStanding
    mirrors_reaching_the_quoted_total: int
    simple_family_mirrors: int
    mirrors_where_the_rule_breaks: tuple[str, ...]
    muqattaat_token_count: int

    def __post_init__(self) -> None:
        if self.mirrors_reaching_the_quoted_total > self.simple_family_mirrors:
            raise QuranCorpusError(
                "بالغُ الرقمِ لا يتجاوز عددَ مرايا الأسرة؛ وعدٌّ يتجاوز مقامَه "
                "خطأُ قياسٍ لا نتيجة."
            )


def assess_gap_account() -> GapAccountReading:
    """يقرأ حسابَ الثلاثين على المرايا المقيسة، ويُسمّي حيث ينكسر.

    والانكسارُ مقصودُ التسجيل: العثمانيُّ لا يُخرِج الرقمَ لأنّ فواتحَه
    مرسومةٌ بعلاماتٍ أُخَر، فتُصيبها صورةٌ واحدةٌ من أربعَ عشرة. وذلك يُثبت
    أنّ القاعدةَ **معلَّقةٌ برسم النصّ** لا بالنصّ نفسِه
    (`THE_ACCOUNT_IS_TIED_TO_THE_ORTHOGRAPHY`).
    """

    family = tuple(
        mirror for mirror in SURVEYED_MIRRORS if "uthmani" not in mirror.mirror_name
    )
    reaching = tuple(
        mirror for mirror in family if mirror.account_reaches_the_quoted_total()
    )
    broken = tuple(
        mirror.mirror_name
        for mirror in SURVEYED_MIRRORS
        if not mirror.account_reaches_the_quoted_total()
    )
    if not reaching:
        standing = GapAccountStanding.NOT_REPRODUCED
    elif len(reaching) == len(family):
        standing = GapAccountStanding.REPRODUCED_ON_EVERY_SIMPLE_MIRROR
    else:
        standing = GapAccountStanding.REPRODUCED_ON_SOME_MIRRORS
    counts = {mirror.muqattaat_tokens for mirror in family}
    return GapAccountReading(
        standing=standing,
        mirrors_reaching_the_quoted_total=len(reaching),
        simple_family_mirrors=len(family),
        mirrors_where_the_rule_breaks=broken,
        muqattaat_token_count=counts.pop() if len(counts) == 1 else -1,
    )


class QuotedTotalStanding(Enum):
    """منزلةُ الرقم المنقول بعد المسح، ولا رابعَ لثلاثتها."""

    REDERIVED_FROM_THE_FROZEN_BYTES = "أُعيد اشتقاقُه من البايتات المبصومة"
    """البايتاتُ حاضرةٌ ومطابقة، وقاعدةٌ مُعلَنةٌ أخرجت الرقمَ نفسَه."""

    CONTRADICTED_BY_THE_FROZEN_BYTES = "خالفته البايتاتُ المبصومة"
    """البايتاتُ حاضرةٌ ومطابقة، ولم تُخرِج قاعدةٌ مُعلَنةٌ الرقمَ."""

    WITHHELD_FOR_WANT_OF_THE_BYTES = "موقوفٌ لغياب البايتات"
    """لا بايتاتٍ تُطابِق، فلا يُشتَقّ ولا يُنقَض؛ وهذا هو الحالُ الآن."""


@dataclass(frozen=True)
class SurveyReading:
    """قراءةُ الرقم المنقول: منزلتُه، وموقعُه من الثابت المقيس على المرايا."""

    quoted_total: int
    standing: QuotedTotalStanding
    bytes_are_resolvable: bool
    mirror_invariant_total: int | None
    distance_from_mirror_invariant: int | None
    mirrors_matching_the_quoted_total: int
    gap_account: GapAccountReading

    def __post_init__(self) -> None:
        if self.standing is QuotedTotalStanding.WITHHELD_FOR_WANT_OF_THE_BYTES:
            if self.bytes_are_resolvable:
                raise QuranCorpusError(
                    "وقفٌ لغياب البايتات مع بايتاتٍ تُحَلّ تناقض؛ فالمنزلةُ "
                    "تُقرأ من البايتات لا تُعلَن عليها."
                )


def _mirror_invariant() -> int | None:
    """العددُ الذي أجمعت عليه مرايا أسرة «simple»، أو `None` إن لم تُجمِع."""

    totals = {
        mirror.whitespace_tokens
        for mirror in SURVEYED_MIRRORS
        if "uthmani" not in mirror.mirror_name
    }
    if len(totals) != 1:
        return None
    return totals.pop()


def run_quoted_total_survey(path: Path | str | None = None) -> SurveyReading:
    """يقرأ منزلةَ 78,215 الآن: من البايتات إن حضرت، ومن المسح وإلّا.

    ومنزلةُ الرقم غيرُ منزلةِ حسابِ فرقِه: `standing` تُقرأ من البايتات
    المبصومة وحدَها فتبقى موقوفةً حتى تصل، و`gap_account` تُقرأ من المرايا
    فتبلغ ما تبلغ. وخلطُهما كان يجعل حسابًا على مرآةٍ يُقرأ اشتقاقًا من
    المُجمَّد (`AN_ACCOUNT_OF_THE_GAP_IS_NOT_A_REDERIVATION`).
    """

    resolvable = quran_corpus_bytes_are_resolvable(path)
    invariant = _mirror_invariant()
    distance = None if invariant is None else THE_QUOTED_WORD_TOTAL - invariant
    matching = sum(1 for mirror in SURVEYED_MIRRORS if mirror.matches_quoted_total())
    if not resolvable:
        standing = QuotedTotalStanding.WITHHELD_FOR_WANT_OF_THE_BYTES
    else:
        recomputed = word_total(WordCountingRule.WHITESPACE_TOKENS_IN_AYAH_TEXT, path)
        standing = (
            QuotedTotalStanding.REDERIVED_FROM_THE_FROZEN_BYTES
            if recomputed == THE_QUOTED_WORD_TOTAL
            else QuotedTotalStanding.CONTRADICTED_BY_THE_FROZEN_BYTES
        )
    return SurveyReading(
        quoted_total=THE_QUOTED_WORD_TOTAL,
        standing=standing,
        bytes_are_resolvable=resolvable,
        mirror_invariant_total=invariant,
        distance_from_mirror_invariant=distance,
        mirrors_matching_the_quoted_total=matching,
        gap_account=assess_gap_account(),
    )


THE_THIRTY_ARE_THE_DISJOINED_LETTERS_NOTE: Final[str] = (
    "TheThirtyAreTheDisjoinedLetters: الفرقُ بين 78,245 و78,215 مُعيَّنٌ "
    "بأعيانه — ثلاثون رمزًا صورتُها المجرّدةُ إحدى فواتح السور المقطَّعة "
    "الأربعَ عشرة، في تسعٍ وعشرين سورةً تُسهِم الشورى فيها باثنين (حم آيةً "
    "١، عسق آيةً ٢). وهي الرموزُ التي **ليست بكلمات** أصلًا: لا جذرَ لها ولا "
    "وزنَ ولا بِنيةَ صرفيّة، فخروجُها من عدّ الكلمات مقتضى بابها"
)

THE_RULE_IS_NOT_FITTED_TO_ITS_RESULT_NOTE: Final[str] = (
    "TheRuleIsNotFittedToItsResult: المطابقةُ تُمسَح في المدوّنة كلِّها بلا "
    "تقييدٍ بصدر سورةٍ ولا بآيةٍ أولى، فتُصيب الثلاثين نفسَها وصفرَ إيجابٍ "
    "كاذبٍ خارجَ الفواتح؛ وكونُها لا تُصيب سواها **نتيجةُ قياسٍ** لا شرطٌ "
    "وُضِع ليُخرِجها. والصورُ الأربعَ عشرةَ معروفةٌ قبل القياس وكلُّها واقعةٌ "
    "في المدوّنة، فلا مدخلَ ميّتٌ يُوهِم ضبطًا"
)

AN_ACCOUNT_OF_THE_GAP_IS_NOT_A_REDERIVATION_NOTE: Final[str] = (
    "AnAccountOfTheGapIsNotARederivation: بلوغُ القاعدةِ الرقمَ على المرايا "
    "**لا يُعيد اشتقاقَه** من البايتات المبصومة، ولا ينقل `standing` عن "
    "الوقف. فالمقيسُ ما في المرايا، والمنقولُ منسوبٌ إلى بصمةٍ أخرى لم تصل؛ "
    "وحقلا القراءة منفصلان لهذا السبب عينِه"
)

THE_ACCOUNT_IS_TIED_TO_THE_ORTHOGRAPHY_NOTE: Final[str] = (
    "TheAccountIsTiedToTheOrthography: القاعدةُ تبلغ الرقمَ في مرايا أسرة "
    "«simple» الأربع، و**تنكسر** في العثمانيّ: فواتحُه مرسومةٌ بعلاماتٍ أُخَر "
    "فلا تُصيبها إلّا صورةٌ واحدةٌ من أربعَ عشرة، ولا يخرج منه 78,215. فما "
    "قِيس معلَّقٌ برسم النصّ لا بالنصّ، وذلك مُسجَّلٌ لا مُلطَّف"
)

AN_EXACT_MATCH_IS_NOT_A_UNIQUE_ACCOUNT_NOTE: Final[str] = (
    "AnExactMatchIsNotAUniqueAccount: مُسِحت أصنافٌ أُخَر من الرموز طلبًا "
    "لمنافسٍ عدّتُه ثلاثون — الأحاديّةُ، والثنائيّة، وما لا حرفَ علّةٍ فيه، "
    "والفريدةُ، وطبقاتُ التردّد كلُّها — فلم يُصَب صنفٌ واحد. وذلك يُقوّي "
    "الحسابَ ولا يُفرِده: المسحُ محدودٌ بما خطر، وقاعدةٌ أخرى تُخرِج ثلاثين "
    "تبقى ممكنةً حتى تصل البايتاتُ فتَحكُم"
)

THE_BASMALA_IS_INLINE_IN_THIS_CORPUS_NOTE: Final[str] = (
    "TheBasmalaIsInlineInThisCorpus: في هذه المدوّنة البسملةُ **مُدرَجةٌ في "
    "الآية الأولى** من كلّ سورةٍ سوى الفاتحة والتوبة — ١١٢ بسملةً هي ٤٤٨ "
    "رمزًا داخلةٌ في 78,245. وهذه بنيةٌ في النصّ لا في القاعدة، ومن عدّ "
    "ظانًّا أنّ البسملة خارجُ الآيات عدّ غيرَ ما عدّت هذه الوحدة؛ فتُسجَّل "
    "كيلا يُقارَن رقمٌ برقمٍ على مقامين"
)

A_DIGEST_WITHOUT_A_RESOLVER_IS_A_GATE_ON_NO_DOOR_NOTE: Final[str] = (
    "ADigestWithoutAResolverIsAGateOnNoDoor: `FROZEN_CORPUS` كان يحمل الطولَ "
    "والبصمةَ و`decode_corpus_bytes` تُطابق عليهما، ولا دالّةَ في الشجرة "
    "تَحُلّ مسارًا إلى تلك البايتات ولا موضعَ إيداعٍ مسنونٍ لها؛ فكانت "
    "البوّابةُ قائمةً على بابٍ لا يُفتَح. وبناءُ الباب لا يُنزِل البايتات، "
    "لكنّه يجعل غيابَها **مقيسًا** بدل أن يكون غيرَ مذكور"
)

NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE: Final[str] = (
    "NoFigureWithoutTheFingerprintedBytes: لا يخرج عددٌ من هذه الوحدة إلّا "
    "بعد مطابقة الطول والبصمة معًا؛ وغيابُ البايتات رفضُ إخراجٍ لا قيمةٌ "
    "افتراضيّة، وملفٌّ مُحَلٌّ مخالفُ البصمة يَفشَل ولا يُتخطّى"
)

A_COUNT_WITHOUT_A_DECLARED_RULE_IS_NOT_A_COUNT_NOTE: Final[str] = (
    "ACountWithoutADeclaredRuleIsNotACount: «عددُ كلمات المدوّنة» وصفٌ غيرُ "
    "محدِّد؛ فالعددُ يختلف باقتطاع الحقل وعدِّ التعليق وحدِّ الفاصل. "
    "و`WordCountingRule` مُعلَنةٌ قبل القياس، وكلُّ عددٍ يخرج من هنا يحمل "
    "قاعدتَه معه، فلا يُقارَن رقمٌ برقمٍ إلّا تحت القاعدة نفسِها"
)

THE_TOKEN_TOTAL_IS_INVARIANT_UNDER_THE_MARK_OPTIONS_NOTE: Final[str] = (
    "TheTokenTotalIsInvariantUnderTheMarkOptions: قِيست خمسُ مرايا، فخرج "
    "78,245 من أربعِ نسخٍ من أسرة «simple» تختلف أطوالُها (1,160,550 و"
    "1,331,429 و1,337,695 و1,337,820) وبصماتُها وفواصلُ أسطرها — و77,878 من "
    "العثمانيّ. فعددُ الرموز لا تُغيّره خياراتُ العلامات التي تُغيّر الطول، "
    "وعليه **لا يُفسَّر** فرقُ 78,215 عن 78,245 بخيار تنزيل. والفرقُ ثلاثون "
    "ولا تحسمه هذه الشجرة: لم تُبلَغ قاعدةُ عدٍّ تُخرِجه، ولم تصل البايتاتُ "
    "التي قِيس عليها"
)

A_MIRROR_IS_A_CORROBORATION_NOT_A_SUBSTITUTE_NOTE: Final[str] = (
    "AMirrorIsACorroborationNotASubstitute: المرايا الخمسُ مُصرَّحٌ بأطوالها "
    "وبادئات بصماتها، وكلُّها **تخالف** المُجمَّد؛ فما قِيس عليها قرينةٌ على "
    "استقرار قاعدة العدّ عبر النسخ، لا شهادةٌ على المدوّنة المقصودة. "
    "و`MirrorMeasurement` يردُّ عند الإنشاء ما وافق طولَ المُجمَّد أو بادئةَ "
    "بصمته، كيلا تتسلّل البايتاتُ المقصودةُ من باب المرايا"
)

A_SURVEY_IS_NOT_A_PROHIBITION_NOTE: Final[str] = (
    "ASurveyIsNotAProhibition: لم تُوجَد في المرايا المفحوصة نسخةٌ بطول "
    "1,319,901؛ وهذا **حدُّ مسحٍ** لا حكمٌ بعدم الوجود. وفهرسُ بحث الشيفرة "
    "في GitHub يُسقِط الملفّاتِ الكبيرةَ أصلًا، فالمسحُ واسعٌ غيرُ مستوعِب، "
    "ونزولُ البايتات لاحقًا يَنقُل المنزلةَ بلا سطرِ تعديلٍ واحد"
)

THE_ONE_HUNDRED_AND_THIRTY_FOUR_IS_NOT_THE_THIRTY_NOTE: Final[str] = (
    "TheOneHundredAndThirtyFourIsNotTheThirty: في "
    "`gflk_specification_deposit` فرقٌ مُسجَّلٌ قدرُه 134 بين 78,215 ومجموع "
    "الأربعة 78,081؛ وههنا فرقٌ آخرُ قدرُه 30 بين 78,215 والثابت المقيس "
    "78,245. وهما فرقان في جهتين مختلفتين على طرفَي الرقم المنقول، ولا "
    "يُجمَعان ولا يُطرَحان ولا يُفسَّر أحدُهما بالآخر ما لم تصل البايتات"
)

QURAN_CORPUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ADigestWithoutAResolverIsAGateOnNoDoor": (
        A_DIGEST_WITHOUT_A_RESOLVER_IS_A_GATE_ON_NO_DOOR_NOTE
    ),
    "NoFigureWithoutTheFingerprintedBytes": (
        NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
    ),
    "ACountWithoutADeclaredRuleIsNotACount": (
        A_COUNT_WITHOUT_A_DECLARED_RULE_IS_NOT_A_COUNT_NOTE
    ),
    "TheTokenTotalIsInvariantUnderTheMarkOptions": (
        THE_TOKEN_TOTAL_IS_INVARIANT_UNDER_THE_MARK_OPTIONS_NOTE
    ),
    "AMirrorIsACorroborationNotASubstitute": (
        A_MIRROR_IS_A_CORROBORATION_NOT_A_SUBSTITUTE_NOTE
    ),
    "ASurveyIsNotAProhibition": A_SURVEY_IS_NOT_A_PROHIBITION_NOTE,
    "TheThirtyAreTheDisjoinedLetters": THE_THIRTY_ARE_THE_DISJOINED_LETTERS_NOTE,
    "TheRuleIsNotFittedToItsResult": THE_RULE_IS_NOT_FITTED_TO_ITS_RESULT_NOTE,
    "AnAccountOfTheGapIsNotARederivation": (
        AN_ACCOUNT_OF_THE_GAP_IS_NOT_A_REDERIVATION_NOTE
    ),
    "TheAccountIsTiedToTheOrthography": (THE_ACCOUNT_IS_TIED_TO_THE_ORTHOGRAPHY_NOTE),
    "AnExactMatchIsNotAUniqueAccount": AN_EXACT_MATCH_IS_NOT_A_UNIQUE_ACCOUNT_NOTE,
    "TheBasmalaIsInlineInThisCorpus": THE_BASMALA_IS_INLINE_IN_THIS_CORPUS_NOTE,
    "TheOneHundredAndThirtyFourIsNotTheThirty": (
        THE_ONE_HUNDRED_AND_THIRTY_FOUR_IS_NOT_THE_THIRTY_NOTE
    ),
}
"""ما لم يُحسَم، مُسمًّى بأسمائه؛ وكلُّ قيمةٍ تبدأ بمفتاحها ثمّ `: `."""


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "birth",
    "freeze",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ يتسلّل إلى قراءةٍ لا سلطةَ فيها."""

    for dataclass_type in (
        GapAccountReading,
        MirrorMeasurement,
        MuqattaatOccurrence,
        SurveyReading,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise QuranCorpusError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى "
                        f"{dataclass_type.__name__}: {declared.name}؛ وهذه "
                        "قراءةٌ لا سلطةَ فيها ولا رتبة."
                    )


_assert_no_authority_field()

if any(mirror.matches_quoted_total() for mirror in SURVEYED_MIRRORS):
    raise RuntimeError(
        "مرآةٌ تُخرِج الرقمَ المنقولَ تنقل منزلتَه، فلا تُترَك في سجلّ " "المخالفات بلا قراءة."
    )
