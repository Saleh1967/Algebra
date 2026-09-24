"""المزدوجُ الأكثرُ تكرارًا: مقيسٌ على المُودَعَين، ومُهيَّأٌ للمدوّنة لا مُدَّعًى عليها.

سُئل: ما المزدوجُ الأكثرُ تكرارًا **على كلّ المدوّنة**؟ وجوابُ هذه الشجرة يبدأ
بما ليس فيها: **بايتاتُ المدوّنة ليست ههنا**. فـ`quran_corpus_word_total`
تحفظ بصمتَها مُجمَّدةً — 1,319,901 بايتًا و`sha256` معلومًا — ولا تحفظ بايتاتِها،
و`quran_corpus_bytes_are_resolvable()` تردّ `False` في هذه الشجرة. فلا يُنشَر
ههنا رقمٌ عن المدوّنة ألبتّة، ولا يُقدَّر، ولا يُستنبَط من المُودَعَين
(`THE_CORPUS_BYTES_ARE_ABSENT_SO_NO_CORPUS_FIGURE_IS_PUBLISHED`).

والذي يُصنَع بدلًا من التقدير شيئان: **حدٌّ مشتقٌّ من اليونيكود** يصحّ على كلّ
نصّ، و**آلةٌ مُسجَّلةٌ قبل الرؤية** تُشغَّل على البايتات متى حضرت.

**أوّلًا: اليونيكود لا يمنع مزدوجًا واحدًا من الستّة والثلاثين.** الأصنافُ
اللاصقةُ (`Canonical_Combining_Class`) للتسع متمايزةٌ كلُّها بلا تكرار:

    064B=27  064C=28  064D=29  064E=30  064F=31
    0650=32  0651=33  0652=34  0670=35

وتمايزُها يُفيد أمرين مُشتقَّين لا مُصطلَحًا عليهما. الأوّل: **لا تنافيَ في
الجدول**؛ فالتنافي إنّما يلزم عند اتّحاد الصنف، ولا اتّحادَ ههنا، فكلُّ
`C(9,2) = 36` مزدوجًا **جائزٌ يونيكوديًّا**. والثاني: **ترتيبُ المزدوج لا يحمل
خبرًا**؛ إذ ترتّبه التسويةُ القانونيّةُ ترتيبًا تامًّا بالصنف، فالمزدوجُ
**مجموعةٌ لا متتالية**. وقِيس ذلك على المُودَعَين فلم يُخالَف: 16 مزدوجًا في
كلٍّ منهما، متطابقةٌ قبل التسوية وبعدها، ولا واحدَ منها خارجَ ترتيب الصنف
(`THE_ORDER_INSIDE_A_PAIR_CARRIES_NO_INFORMATION`).

**وثانيًا: المانعُ ليس في الجدول بل في النصّ.** أُجيز ستّةٌ وثلاثون، وتحقّق في
الفاتحة **ثلاثةٌ** وفي الفتح **اثنان**. فضيقُ المزدوجات خبرٌ عن هذين النصّين،
وقد يكون أثرَ قِصَرهما لا أثرَ منعٍ في الخطّ، ولا يُقرأ منعًا
(`AN_UNREALIZED_PAIR_IS_NOT_A_FORBIDDEN_PAIR`).

**وثالثًا: المقيسُ على المُودَعَين، مرتَّبًا:**

| المزدوج | الفاتحة | الفتح ٢٩ |
|---|---|---|
| فتحة + شدّة | **10** | **14** |
| كسرة + شدّة | 4 | 0 |
| فتحة + خنجريّة | 2 | 0 |
| ضمّة + شدّة | 0 | 2 |

فالأكثرُ تكرارًا في النصّين جميعًا **فتحةٌ وشدّة**، وصدارتُه غيرُ منازَعة في
كلٍّ منهما على حدة. **وهذا ترتيبٌ على مُودَعَين لا على مدوّنة**، وسَعتُهما 83
كلمةً من 78,245 — أي **0.106%** — فلا تُرفَع الصدارةُ حكمًا على المدوّنة، ولا
تُسمّى «الأكثرَ تكرارًا» مطلقًا
(`A_RANKING_ON_TWO_TEXTS_IS_NOT_A_CORPUS_RANKING`).

**ورابعًا: ما تُلزِم به هذه الوحدةُ نفسَها قبل أن ترى البايتات.** تشغيلُ
`pair_census_over_corpus` على البايتات المُصادَقةِ ببصمتها يُخرِج التعدادَ
كاملًا مرتَّبًا، لا المتصدّرَ وحدَه؛ ويُشترَط عليه أن يُصرِّح بالمزدوجات
المتحقّقة من الستّة والثلاثين، وبأن يُذكَر **الثاني والثالث** مع الأوّل حتّى
يُعلَم أفرقٌ بيّنٌ هو أم تقاربٌ لا يحتمل ترتيبًا. وإن تساوى اثنان فلا يُكسَر
التساوي باختيار، بل يُعلَن تساويًا
(`A_TIE_IS_REPORTED_AND_NOT_BROKEN`). وهذا تسجيلٌ قبل الرؤية، لا وصفٌ بعدها.

**وخامسًا: المزدوجُ ههنا مزدوجُ رسمٍ لا مزدوجُ صوت.** «فتحة + شدّة» تتابعُ
نقطتي ترميزٍ على موضعٍ واحد، ولا يُقرأ منه تشديدٌ ولا مدٌّ ولا مقطع؛ فالحكمُ
على البتّات وحدَها كما في `written_haraka_mark`
(`A_PAIR_OF_MARKS_IS_NOT_A_PHONETIC_UNIT`).
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, fields
from itertools import combinations
from typing import Final

from alghanem.arabic.haraka_fiber_structure import THE_CONTESTED_MARKS
from alghanem.arabic.written_haraka_mark import THE_IMPORTED_HARAKAT, positions_of

__all__ = [
    "AN_UNREALIZED_PAIR_IS_NOT_A_FORBIDDEN_PAIR",
    "A_PAIR_OF_MARKS_IS_NOT_A_PHONETIC_UNIT",
    "A_RANKING_ON_TWO_TEXTS_IS_NOT_A_CORPUS_RANKING",
    "A_TIE_IS_REPORTED_AND_NOT_BROKEN",
    "MARK_PAIR_NAMED_RESIDUALS",
    "THE_CORPUS_BYTES_ARE_ABSENT_SO_NO_CORPUS_FIGURE_IS_PUBLISHED",
    "THE_NINE_MARKS",
    "THE_ORDER_INSIDE_A_PAIR_CARRIES_NO_INFORMATION",
    "MarkPairError",
    "PairCensus",
    "PairCount",
    "combining_classes_are_all_distinct",
    "corpus_run_is_available",
    "pair_census_over",
    "pair_census_over_corpus",
    "possible_pairs",
]


class MarkPairError(ValueError):
    """خطأٌ في عدّ المزدوجات."""


THE_NINE_MARKS: Final[tuple[str, ...]] = tuple(
    sorted(THE_IMPORTED_HARAKAT | THE_CONTESTED_MARKS, key=ord)
)


def combining_classes_are_all_distinct() -> bool:
    """أتمايزت الأصنافُ اللاصقةُ للتسع؟ وعليه يدور الجواز والترتيب."""

    classes = [unicodedata.combining(mark) for mark in THE_NINE_MARKS]
    return len(set(classes)) == len(classes)


def possible_pairs() -> tuple[tuple[str, str], ...]:
    """المزدوجاتُ التي لا يمنعها اليونيكود، مرتَّبةً بالصنف اللاصق."""

    ordered: list[tuple[str, str]] = []
    for pair in combinations(THE_NINE_MARKS, 2):
        first, second = sorted(pair, key=unicodedata.combining)
        ordered.append((first, second))
    return tuple(ordered)


@dataclass(frozen=True)
class PairCount:
    """مزدوجٌ واحدٌ وعددُ وقوعه، بلا نسبةٍ مخزونة."""

    pair: tuple[str, str]
    occurrences: int

    def __post_init__(self) -> None:
        if len(self.pair) != 2:
            raise MarkPairError("المزدوجُ نقطتان لا غير.")
        if self.pair[0] == self.pair[1]:
            raise MarkPairError("لا يزدوج الشيءُ بنفسه على موضعٍ واحد.")
        if self.occurrences < 0:
            raise MarkPairError("عددُ وقوعٍ سالبٌ لا يكون.")

    @property
    def codepoints(self) -> tuple[str, str]:
        """نقطتا الترميز بصورتهما المعهودة."""

        return (f"U+{ord(self.pair[0]):04X}", f"U+{ord(self.pair[1]):04X}")

    @property
    def names(self) -> tuple[str, str]:
        """اسما النقطتين في الجدول."""

        return (unicodedata.name(self.pair[0]), unicodedata.name(self.pair[1]))


@dataclass(frozen=True)
class PairCensus:
    """تعدادُ المزدوجات فوق نطاقٍ مُسمًّى، مرتَّبًا، بلا كسرٍ للتساوي."""

    scope: str
    counts: tuple[PairCount, ...]
    positions_read: int

    def __post_init__(self) -> None:
        if not self.scope.strip():
            raise MarkPairError("لا بدّ للنطاق من اسمٍ يُنسَب إليه القياس.")
        if self.positions_read < 0:
            raise MarkPairError("عددُ مواضعَ سالبٌ لا يكون.")
        seen = {count.pair for count in self.counts}
        if len(seen) != len(self.counts):
            raise MarkPairError("مزدوجٌ مكرَّرٌ في تعدادٍ واحد.")

    @property
    def ranked(self) -> tuple[PairCount, ...]:
        """المزدوجاتُ المتحقّقةُ من الأكثر إلى الأقلّ، وعند التساوي بالترميز."""

        return tuple(
            sorted(
                (count for count in self.counts if count.occurrences > 0),
                key=lambda count: (-count.occurrences, count.codepoints),
            )
        )

    @property
    def realized(self) -> int:
        """كم مزدوجًا تحقّق من الستّة والثلاثين."""

        return len(self.ranked)

    @property
    def total_pairs(self) -> int:
        """مجموعُ وقوعات المزدوجات."""

        return sum(count.occurrences for count in self.counts)

    @property
    def leaders(self) -> tuple[PairCount, ...]:
        """المتصدِّرُ أو المتصدِّرون؛ ولا يُكسَر التساوي باختيار."""

        ranked = self.ranked
        if not ranked:
            return ()
        top = ranked[0].occurrences
        return tuple(count for count in ranked if count.occurrences == top)

    @property
    def the_lead_is_uncontested(self) -> bool:
        """أَتفرّد المتصدّرُ؟ فإن تساوى اثنان فلا صدارةَ مفردة."""

        return len(self.leaders) == 1

    @property
    def trailers(self) -> tuple[PairCount, ...]:
        """أقلُّ المتحقّقِ وقوعًا؛ ولا يُكسَر التساوي باختيار.

        والمعدومُ ليس ههنا: مزدوجٌ لم يقع ليس أقلَّ وقوعًا، بل هو خارجُ
        التعداد رأسًا (`AN_UNREALIZED_PAIR_IS_NOT_A_FORBIDDEN_PAIR`).
        """

        ranked = self.ranked
        if not ranked:
            return ()
        floor = ranked[-1].occurrences
        return tuple(count for count in ranked if count.occurrences == floor)

    @property
    def the_floor_is_uncontested(self) -> bool:
        """أَتفرّد القاعُ؟ فإن تساوى اثنان فلا قاعَ مفرد."""

        return len(self.trailers) == 1


def pair_census_over(text: str, scope: str) -> PairCensus:
    """يعدّ مزدوجاتِ التسع فوق مواضع نصٍّ، مزدوجًا مزدوجًا."""

    tally: dict[tuple[str, str], int] = {pair: 0 for pair in possible_pairs()}
    nine = set(THE_NINE_MARKS)
    read = 0
    for position in positions_of(text):
        read += 1
        marks = tuple(mark for mark in position.marks if mark in nine)
        if len(marks) != 2:
            continue
        first, second = sorted(marks, key=unicodedata.combining)
        key = (first, second)
        if key not in tally:
            raise MarkPairError(f"مزدوجٌ خارج الستّة والثلاثين: {key!r}.")
        tally[key] += 1
    return PairCensus(
        scope=scope,
        counts=tuple(
            PairCount(pair=pair, occurrences=occurrences)
            for pair, occurrences in tally.items()
        ),
        positions_read=read,
    )


def corpus_run_is_available(path: str | None = None) -> bool:
    """أحاضرةٌ بايتاتُ المدوّنة في هذه الشجرة أو بمسارٍ مُصرَّحٍ به؟"""

    from alghanem.arabic.quran_corpus_word_total import (
        quran_corpus_bytes_are_resolvable,
    )

    return quran_corpus_bytes_are_resolvable(path)


def pair_census_over_corpus(path: str | None = None) -> PairCensus:
    """يعدّ المزدوجاتِ على بايتات المدوّنة المُصادَقةِ ببصمتها، أو يرفض.

    ولا قيمةَ افتراضيّةَ ههنا ولا تقدير: إن لم تحضر البايتاتُ مُطابِقةً
    للبصمة المُجمَّدة رُفض الطلبُ صريحًا، ولم يُنشَر رقمٌ عن المدوّنة.
    """

    from alghanem.arabic.quran_corpus_word_total import read_quran_corpus_bytes

    data = read_quran_corpus_bytes(path)
    return pair_census_over(data.decode("utf-8"), "المدوّنة")


THE_CORPUS_BYTES_ARE_ABSENT_SO_NO_CORPUS_FIGURE_IS_PUBLISHED: Final[str] = (
    "THE_CORPUS_BYTES_ARE_ABSENT_SO_NO_CORPUS_FIGURE_IS_PUBLISHED: بايتاتُ "
    "المدوّنة ليست في هذه الشجرة، و`quran_corpus_bytes_are_resolvable()` تردّ "
    "`False`. فالسؤالُ عن «كلّ المدوّنة» لا يُجاب ههنا برقم، ولا يُقدَّر من "
    "المُودَعَين. والآلةُ مكتوبةٌ لتُشغَّل على البايتات متى حضرت مُصادَقةً "
    "ببصمتها، وترفض صريحًا متى غابت."
)

A_RANKING_ON_TWO_TEXTS_IS_NOT_A_CORPUS_RANKING: Final[str] = (
    "A_RANKING_ON_TWO_TEXTS_IS_NOT_A_CORPUS_RANKING: صدارةُ «فتحة + شدّة» "
    "مقيسةٌ على 83 كلمةً من 78,245 — أي 0.106% — وبمنزلةِ نقلٍ واحدةٍ وبخطّ "
    "ناسخٍ واحد. فهي صدارةٌ في المُودَعَين، ولا تُسمّى الأكثرَ تكرارًا في "
    "المدوّنة، ولا يُستدَلّ باتّفاق النصّين على المدوّنة."
)

AN_UNREALIZED_PAIR_IS_NOT_A_FORBIDDEN_PAIR: Final[str] = (
    "AN_UNREALIZED_PAIR_IS_NOT_A_FORBIDDEN_PAIR: أجاز اليونيكودُ ستّةً "
    "وثلاثين مزدوجًا إذ تمايزت أصنافُ التسع اللاصقة كلُّها، ولم يتحقّق في "
    "الفاتحة إلّا ثلاثةٌ وفي الفتح اثنان. وغيابُ الباقي خبرٌ عن قِصَر النصّين "
    "يحتمل أن يكون أثرَ سَعَتهما لا أثرَ منعٍ في الخطّ، فلا يُقرأ منعًا."
)

THE_ORDER_INSIDE_A_PAIR_CARRIES_NO_INFORMATION: Final[str] = (
    "THE_ORDER_INSIDE_A_PAIR_CARRIES_NO_INFORMATION: لمّا تمايزت الأصنافُ "
    "اللاصقةُ رتّبت التسويةُ القانونيّةُ المزدوجَ ترتيبًا تامًّا، فصار "
    "مجموعةً لا متتالية. وقِيس على المُودَعَين فلم يُخالَف: لا مزدوجَ فيهما "
    "خارجَ ترتيب الصنف قبل التسوية. فلا يُقرأ في تقدُّم إحدى العلامتين خبرٌ "
    "عن كتابةٍ ولا عن نطق."
)

A_TIE_IS_REPORTED_AND_NOT_BROKEN: Final[str] = (
    "A_TIE_IS_REPORTED_AND_NOT_BROKEN: إن تساوى مزدوجان في الصدارة أُعلن "
    "التساوي ولم يُكسَر باختيارٍ من خارج العدّ. ولذلك كانت `leaders` جمعًا "
    "لا مفردًا، و`the_lead_is_uncontested` خبرًا يُقرأ لا يُفترَض."
)

A_PAIR_OF_MARKS_IS_NOT_A_PHONETIC_UNIT: Final[str] = (
    "A_PAIR_OF_MARKS_IS_NOT_A_PHONETIC_UNIT: «فتحة + شدّة» تتابعُ نقطتي "
    "ترميزٍ على موضعٍ واحد، لا تشديدٌ ولا مقطعٌ ولا مدّ. والحكمُ ههنا على "
    "البتّات وحدَها، كما في `written_haraka_mark`."
)

MARK_PAIR_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_CORPUS_BYTES_ARE_ABSENT_SO_NO_CORPUS_FIGURE_IS_PUBLISHED": (
        THE_CORPUS_BYTES_ARE_ABSENT_SO_NO_CORPUS_FIGURE_IS_PUBLISHED
    ),
    "A_RANKING_ON_TWO_TEXTS_IS_NOT_A_CORPUS_RANKING": (
        A_RANKING_ON_TWO_TEXTS_IS_NOT_A_CORPUS_RANKING
    ),
    "AN_UNREALIZED_PAIR_IS_NOT_A_FORBIDDEN_PAIR": (
        AN_UNREALIZED_PAIR_IS_NOT_A_FORBIDDEN_PAIR
    ),
    "THE_ORDER_INSIDE_A_PAIR_CARRIES_NO_INFORMATION": (
        THE_ORDER_INSIDE_A_PAIR_CARRIES_NO_INFORMATION
    ),
    "A_TIE_IS_REPORTED_AND_NOT_BROKEN": A_TIE_IS_REPORTED_AND_NOT_BROKEN,
    "A_PAIR_OF_MARKS_IS_NOT_A_PHONETIC_UNIT": A_PAIR_OF_MARKS_IS_NOT_A_PHONETIC_UNIT,
}

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في عدٍّ لا سلطةَ فيه."""

    for holder in (PairCount, PairCensus):
        for declared in fields(holder):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise MarkPairError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى {holder.__name__}: "
                        f"{declared.name}؛ وهذا عدٌّ لا سلطةَ فيه."
                    )


def _assert_the_nine_are_pairwise_orderable() -> None:
    """حارسُ استيراد: لو اتّحد صنفان لبطل الجوازُ والترتيبُ معًا."""

    if not combining_classes_are_all_distinct():
        raise MarkPairError(
            "اتّحد صنفان لاصقان في التسع؛ فلا يصحّ قولُ الجواز ولا قولُ "
            "الترتيب التامّ، ويُعاد النظرُ في الوحدة كلِّها."
        )


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in MARK_PAIR_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise MarkPairError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_nine_are_pairwise_orderable()
_assert_every_residual_is_named_by_its_key()
