"""البنيةُ الليفيّةُ مقروءةً من البتّات: `π: E → B` بلا مرمِّزٍ ولا مخطَّطٍ مُسبَق.

سبق في هذه الشجرة كلامٌ كثيرٌ في الألياف — `carrier_state_observed_fiber`
و`fiber_bundle_verdict` و`position_bundle_sections` — وكلُّه قائمٌ على
**المرمِّز** `CarrierStateCodec` وعلى **مخطَّطٍ محوريٍّ مُسجَّلٍ قبل العدّ**.
وهذه الوحدةُ تسأل السؤالَ الليفيَّ نفسَه من طريقٍ أخرى: `π: E → B` مقروءًا من
جداول اليونيكود وحدَها، على المحمول المُقرَّر في `written_haraka_mark`.

    B = المواضعُ (ما ليس `Mn`)          E_b = ما لصق بالموضع من السبع
    π(e) = الموضعُ الذي لصقت به العلامة

**والحكمُ الأوّل: ليست حزمةَ ألياف.** حزمةُ الأليافِ تقتضي تساويَ الألياف؛
والمقيسُ ههنا ليفان لا ليفٌ واحد: ليفٌ خالٍ وليفٌ مفردٌ، ولا ثالثَ لهما. في
الفاتحة 40 خاليًا و103 مفردًا، وفي الفتح 61 و188. فلا تماثلَ، فلا حزمة
(`THE_FIBERS_ARE_NOT_EQUINUMEROUS_SO_THIS_IS_NOT_A_BUNDLE`). والذي قام فعلًا
**قطاعٌ جزئيّ**: دالّةٌ مُعرَّفةٌ على بعض القاعدة لا كلِّها.

**والحكمُ الثاني: لا قطاعَ كلّيًّا ألبتّة.** القطاعُ `s: B → E` بشرط
`π∘s = id_B` يقتضي نقطةً فوق **كلّ** نقطةٍ قاعديّة؛ وفوق الأربعين الخاليةِ لا
نقطة. فعددُ القطاعات الكلّيّة **صفرٌ** لا واحدًا، وهو حاصلُ ضربٍ فيه عاملٌ
معدوم. وفوق القاعدة الموسومة وحدَها القطاعُ **واحدٌ لا غير**، لأنّ كلَّ ليفٍ
هناك مفردٌ فلا اختيارَ فيه (`A_PARTIAL_SECTION_IS_NOT_A_SECTION`).

**والحكمُ الثالث — وهو المقصود — أنّ إفرادَ الليف صنيعُ الاستيراد لا صنيعُ
الرسم.** قُرِّر في `written_haraka_mark` أنّ إدخالَ الشدّة والخنجريّة يحرّك
**صفرَ** مواضع؛ وذلك حقٌّ **في السؤال الثنائيّ**: أموسومٌ أم لا. فإذا سُئل
السؤالُ الليفيُّ — كم في هذا الليف؟ — انقلب الخمولُ إلى فاعليّةٍ تامّة:

| | الفاتحة | الفتح ٢٩ |
|---|---|---|
| يتحرّك حكمُه الثنائيّ | 0 | 0 |
| ينتقل من ليفٍ مفردٍ إلى مزدوج | **16** | **16** |

فالسبعةُ تُنتج أليافًا ≤ 1، والتسعةُ تُنتج أليافًا تبلغ 2. ومعنى ذلك أنّ
«الليفُ مفردٌ» **ليست خاصّيّةً للخطّ العربيّ**، بل أثرٌ مباشرٌ لقصر الاختيار
على سبع. والدرسُ أعمُّ من الرقم: **الخمولُ ليس صفةً للاستيراد، بل صفةٌ
للسؤال المطروح عليه**؛ فاستيرادٌ خاملٌ في إسقاطٍ ثنائيٍّ قد يكون حاسمًا في
البنية فوقه (`AN_INERT_IMPORT_IN_THE_PROJECTION_IS_DECISIVE_IN_THE_FIBER`).

**والستّةَ عشرَ ليست عددًا واحدًا مرّتين.** يُفصَّل العددُ بسببه لا يُترَك
مصادفةً: في الفاتحة 14 شدّةً و2 خنجريّة، وفي الفتح 16 شدّةً و0 خنجريّة.
فتساوي المجموعين لا يدلّ على تساوي السببين
(`THE_TWO_SIXTEENS_DO_NOT_HAVE_THE_SAME_CAUSE`).

**ورَدُّ الحزمة ممكنٌ بثمنٍ مُعلَن.** لو أُلحق «الغياب» عضوًا في الليف لصارت
الألياف متساويةً ثمانيةً فوق كلّ موضع، ولعادت الحزمةُ تافهةً `B × 8` ولها
قطاعٌ كلّيّ. وهذا عينُ ما فعله المخطَّطُ المُودَعُ قبلُ إذ جعل «قيمةَ الغياب
عضوًا في كلّ محور». لكنّ هذا **إلحاقٌ لا قياس**: ليس في البتّات نقطةُ ترميزٍ
اسمُها الغياب، فالعضوُ الثامنُ يُؤتى به من خارج الجدول. فالبنيةُ الليفيّةُ
ههنا **تدور على اصطلاحٍ لا على قياس**، وهذا مُسمًّى لا مطويّ
(`ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT`).

**ولا تفاهةَ موضعيّةً فوق الحروف أيضًا.** لو جُمعت فوق كلّ حرفٍ قاعديٍّ
مجموعةُ ما تحقّق عليه من السبع لاختلفت الأحجام: في الفاتحة من 0 إلى 4، وفي
الفتح من 0 إلى 5. فلا الحرفُ الواحدُ يحمل السبعَ، ولا الحروفُ تتساوى فيما
تحمل (`THE_REALIZED_SETS_OVER_LETTERS_ARE_NOT_EQUINUMEROUS`).

**وما لم يُقَس لا يُقال.** خلوُّ ليفٍ خبرٌ عن الرسم لا عن النطق، وقد سبق
تسميتُه في المحمول نفسِه. وكونُ الليف ≤ 1 مقيسٌ على مُودَعَين لا على مدوّنة
(`A_FIBER_MEASURED_ON_TWO_TEXTS_IS_NOT_A_CORPUS_FIBER`). وهذه الوحدةُ **قياسٌ
لا حكم**: لا تُرخِّص بنيةً ولا تُبطِلها، بل تقول ما قام وما لم يقم.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from alghanem.arabic.written_haraka_mark import (
    THE_IMPORTED_HARAKAT,
    Position,
    positions_of,
)

__all__ = [
    "ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT",
    "AN_INERT_IMPORT_IN_THE_PROJECTION_IS_DECISIVE_IN_THE_FIBER",
    "A_FIBER_MEASURED_ON_TWO_TEXTS_IS_NOT_A_CORPUS_FIBER",
    "A_PARTIAL_SECTION_IS_NOT_A_SECTION",
    "FIBER_STRUCTURE_NAMED_RESIDUALS",
    "THE_CONTESTED_MARKS",
    "THE_FIBERS_ARE_NOT_EQUINUMEROUS_SO_THIS_IS_NOT_A_BUNDLE",
    "THE_REALIZED_SETS_OVER_LETTERS_ARE_NOT_EQUINUMEROUS",
    "THE_TWO_SIXTEENS_DO_NOT_HAVE_THE_SAME_CAUSE",
    "FiberProfile",
    "FiberStructureError",
    "WideningEffect",
    "fiber_over",
    "fiber_profile_of",
    "realized_sets_over_letters",
    "total_sections_over",
    "widening_effect_on",
]


class FiberStructureError(ValueError):
    """خطأٌ في قراءة البنية الليفيّة."""


THE_CONTESTED_MARKS: Final[frozenset[str]] = frozenset({"\u0651", "\u0670"})


def fiber_over(position: Position) -> tuple[str, ...]:
    """ليفُ الموضع: ما لصق به من السبع المستورَدة، بترتيب وروده."""

    return position.haraka_marks


@dataclass(frozen=True)
class FiberProfile:
    """توزيعُ أحجام الألياف فوق قاعدةٍ مقروءة، بلا رقمٍ مخزون."""

    scope: str
    sizes: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.scope.strip():
            raise FiberStructureError("لا بدّ للنطاق من اسمٍ يُنسَب إليه القياس.")
        if any(size < 0 for size in self.sizes):
            raise FiberStructureError("حجمُ ليفٍ سالبٌ لا يكون.")

    @property
    def base_points(self) -> int:
        """عددُ نقاط القاعدة."""

        return len(self.sizes)

    @property
    def empty_fibers(self) -> int:
        """كم ليفًا خلا."""

        return sum(1 for size in self.sizes if size == 0)

    @property
    def distinct_sizes(self) -> tuple[int, ...]:
        """أحجامُ الألياف المتحقّقة، مرتّبة."""

        return tuple(sorted(set(self.sizes)))

    @property
    def is_equinumerous(self) -> bool:
        """أتساوت الألياف؟ وهو شرطُ الحزمة."""

        return len(self.distinct_sizes) == 1

    @property
    def largest_fiber(self) -> int:
        """أكبرُ ليفٍ متحقّق."""

        return max(self.sizes, default=0)


def fiber_profile_of(
    text: str,
    scope: str,
    *,
    marks: frozenset[str] = THE_IMPORTED_HARAKAT,
) -> FiberProfile:
    """يقرأ توزيعَ أحجام الألياف فوق مواضع النصّ، بمجموعةِ علاماتٍ مُعلَنة."""

    return FiberProfile(
        scope=scope,
        sizes=tuple(
            sum(1 for mark in position.marks if mark in marks)
            for position in positions_of(text)
        ),
    )


def total_sections_over(profile: FiberProfile) -> int:
    """عددُ القطاعات الكلّيّة: حاصلُ ضرب أحجام الألياف، فيصفر بليفٍ خالٍ."""

    count = 1
    for size in profile.sizes:
        count *= size
        if count == 0:
            return 0
    return count


@dataclass(frozen=True)
class WideningEffect:
    """أثرُ توسيع الاختيار، مقيسًا في السؤالين: الثنائيِّ والليفيّ."""

    scope: str
    decisions_moved: int
    fibers_enlarged: int
    by_shadda: int
    by_dagger: int

    def __post_init__(self) -> None:
        if not self.scope.strip():
            raise FiberStructureError("لا بدّ للنطاق من اسمٍ يُنسَب إليه القياس.")
        for value in (
            self.decisions_moved,
            self.fibers_enlarged,
            self.by_shadda,
            self.by_dagger,
        ):
            if value < 0:
                raise FiberStructureError("عددٌ سالبٌ لا يكون في عدٍّ للمواضع.")

    @property
    def the_projection_is_inert(self) -> bool:
        """أخمَد التوسيعُ في السؤال الثنائيّ؟"""

        return self.decisions_moved == 0

    @property
    def the_fiber_moves(self) -> bool:
        """أتحرّك التوسيعُ في السؤال الليفيّ؟"""

        return self.fibers_enlarged > 0


def widening_effect_on(text: str, scope: str) -> WideningEffect:
    """يقيس التوسيعَ في الموضعين معًا فيُظهِر افتراقَ السؤالين."""

    widened = THE_IMPORTED_HARAKAT | THE_CONTESTED_MARKS
    moved = 0
    enlarged = 0
    shadda = 0
    dagger = 0
    for position in positions_of(text):
        narrow = [mark for mark in position.marks if mark in THE_IMPORTED_HARAKAT]
        wide = [mark for mark in position.marks if mark in widened]
        if bool(wide) != bool(narrow):
            moved += 1
        if len(wide) > len(narrow):
            enlarged += 1
        if "\u0651" in position.marks:
            shadda += 1
        if "\u0670" in position.marks:
            dagger += 1
    return WideningEffect(
        scope=scope,
        decisions_moved=moved,
        fibers_enlarged=enlarged,
        by_shadda=shadda,
        by_dagger=dagger,
    )


def realized_sets_over_letters(text: str) -> dict[str, frozenset[str]]:
    """لكلّ حرفٍ قاعديّ: ما تحقّق عليه من السبع في هذا النصّ."""

    realized: dict[str, set[str]] = {}
    for position in positions_of(text):
        realized.setdefault(position.carrier, set()).update(position.haraka_marks)
    return {carrier: frozenset(marks) for carrier, marks in realized.items()}


THE_FIBERS_ARE_NOT_EQUINUMEROUS_SO_THIS_IS_NOT_A_BUNDLE: Final[str] = (
    "THE_FIBERS_ARE_NOT_EQUINUMEROUS_SO_THIS_IS_NOT_A_BUNDLE: حزمةُ الأليافِ "
    "تقتضي تساويَ الألياف، والمقيسُ ههنا حجمان لا حجمٌ واحد: خالٍ ومفرد "
    "(الفاتحة 40 و103، والفتح 61 و188). فلا يُسمّى هذا حزمةً، وإنّما هو "
    "قطاعٌ جزئيٌّ على قاعدةٍ بعضُها خالٍ."
)

A_PARTIAL_SECTION_IS_NOT_A_SECTION: Final[str] = (
    "A_PARTIAL_SECTION_IS_NOT_A_SECTION: القطاعُ يقتضي نقطةً فوق كلّ نقطةٍ "
    "قاعديّة، وفوق الألياف الخالية لا نقطة. فعددُ القطاعات الكلّيّة صفرٌ لا "
    "واحد. وأمّا فوق القاعدة الموسومة وحدَها فالقطاعُ واحدٌ لأنّ الليفَ "
    "مفردٌ فلا اختيارَ فيه؛ وهذا خبرٌ عن قاعدةٍ أصغرَ لا عن القاعدة."
)

AN_INERT_IMPORT_IN_THE_PROJECTION_IS_DECISIVE_IN_THE_FIBER: Final[str] = (
    "AN_INERT_IMPORT_IN_THE_PROJECTION_IS_DECISIVE_IN_THE_FIBER: قِيس أنّ "
    "إدخال الشدّة والخنجريّة يحرّك صفرَ أحكامٍ ثنائيّة، وهو حقٌّ في ذلك "
    "السؤال وحدَه. وفي السؤال الليفيّ ينتقل 16 موضعًا في كلٍّ من النصّين من "
    "ليفٍ مفردٍ إلى مزدوج. فإفرادُ الليف صنيعُ الاستيراد لا صنيعُ الرسم، "
    "والخمولُ صفةٌ للسؤال المطروح لا للاستيراد نفسِه."
)

THE_TWO_SIXTEENS_DO_NOT_HAVE_THE_SAME_CAUSE: Final[str] = (
    "THE_TWO_SIXTEENS_DO_NOT_HAVE_THE_SAME_CAUSE: تساوى المجموعان عند 16 في "
    "النصّين، ويفترق سببُهما بالتفصيل: الفاتحة 14 شدّةً و2 خنجريّة، والفتح "
    "16 شدّةً و0 خنجريّة. فلا يُقرأ التساوي قانونًا ولا نمطًا."
)

ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT: Final[str] = (
    "ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT: "
    "لو أُلحق «الغياب» عضوًا في الليف لتساوت الألياف ثمانيةً ولعادت الحزمةُ "
    "تافهةً ولها قطاعٌ كلّيّ. لكنّ الغيابَ ليس نقطةَ ترميز، فالعضوُ الثامنُ "
    "مُلحَقٌ من خارج الجدول. فالحكمُ بالحزمة أو بنفيها يدور على اصطلاحٍ "
    "مُعلَنٍ لا على قياسٍ في البتّات."
)

THE_REALIZED_SETS_OVER_LETTERS_ARE_NOT_EQUINUMEROUS: Final[str] = (
    "THE_REALIZED_SETS_OVER_LETTERS_ARE_NOT_EQUINUMEROUS: مجموعاتُ ما تحقّق "
    "فوق الحروف القاعديّة مختلفةُ الأحجام — من 0 إلى 4 في الفاتحة، ومن 0 "
    "إلى 5 في الفتح — فلا تفاهةَ موضعيّةً فوق الحروف. وصِغَرُ هذه المجموعات "
    "قد يكون أثرَ قلّة النصّ لا أثرَ منعٍ في الخطّ، ولا يُقرأ منعًا."
)

A_FIBER_MEASURED_ON_TWO_TEXTS_IS_NOT_A_CORPUS_FIBER: Final[str] = (
    "A_FIBER_MEASURED_ON_TWO_TEXTS_IS_NOT_A_CORPUS_FIBER: كلُّ ما ههنا مقيسٌ "
    "على مُودَعَين اثنين بمنزلةِ نقلٍ واحدة، فلا تُرفَع أحكامُ البنية إلى "
    "المدوّنة، ولا يُستثنى منها كونُ الليف ≤ 1."
)

FIBER_STRUCTURE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_FIBERS_ARE_NOT_EQUINUMEROUS_SO_THIS_IS_NOT_A_BUNDLE": (
        THE_FIBERS_ARE_NOT_EQUINUMEROUS_SO_THIS_IS_NOT_A_BUNDLE
    ),
    "A_PARTIAL_SECTION_IS_NOT_A_SECTION": A_PARTIAL_SECTION_IS_NOT_A_SECTION,
    "AN_INERT_IMPORT_IN_THE_PROJECTION_IS_DECISIVE_IN_THE_FIBER": (
        AN_INERT_IMPORT_IN_THE_PROJECTION_IS_DECISIVE_IN_THE_FIBER
    ),
    "THE_TWO_SIXTEENS_DO_NOT_HAVE_THE_SAME_CAUSE": (
        THE_TWO_SIXTEENS_DO_NOT_HAVE_THE_SAME_CAUSE
    ),
    "ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT": (
        ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT
    ),
    "THE_REALIZED_SETS_OVER_LETTERS_ARE_NOT_EQUINUMEROUS": (
        THE_REALIZED_SETS_OVER_LETTERS_ARE_NOT_EQUINUMEROUS
    ),
    "A_FIBER_MEASURED_ON_TWO_TEXTS_IS_NOT_A_CORPUS_FIBER": (
        A_FIBER_MEASURED_ON_TWO_TEXTS_IS_NOT_A_CORPUS_FIBER
    ),
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
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في قياسٍ لا سلطةَ فيه."""

    for holder in (FiberProfile, WideningEffect):
        for declared in fields(holder):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise FiberStructureError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى {holder.__name__}: "
                        f"{declared.name}؛ وهذا قياسٌ لا سلطةَ فيه."
                    )


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in FIBER_STRUCTURE_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise FiberStructureError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_every_residual_is_named_by_its_key()
