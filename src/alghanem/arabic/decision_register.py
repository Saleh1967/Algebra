"""سجلُّ القرارات: ما ينتظر قرارًا يدخل الشجرةَ شيئًا مُقيَّدًا، لا سؤالًا في محادثة.

**ما تفعله هذه الوحدة**: تُقيِّد القراراتَ المعلَّقةَ **أعيانًا** لها أنواعٌ
مغلقةٌ وشروطُ إنشاء: لكلّ قرارٍ سؤالُه، وما يَحجُبه، **وفروعُه بأثمانها**. فما
كان معلَّقًا في محادثةٍ يُنسى أو يُقرأ بعد جلساتٍ كأنّه حُسِم؛ وما كان مُقيَّدًا
هنا يُفحَص عند كلّ استيراد، ويرفض أن يُقرأ محسومًا وهو معلَّق.

`A_PENDING_DECISION_IS_NOT_A_DEFAULT`: القرارُ المعلَّق لا يصير فرعًا بالسكوت.
ولذلك `assert_not_reportable_as_done` تردُّ كلَّ إعلانِ تمامٍ لشيءٍ يحجُبه قرارٌ
معلَّق؛ فالحجبُ يُقال ولا يُسكَت عنه.

`THE_SESSION_CANNOT_SIGN_A_DECISION`: القرارُ المتَّخَذ يحتاج **سلطةً مسمّاةً
وتاريخًا**، والوحدةُ ترفض أن تكون السلطةُ الجلسةَ أو المساعدَ. فليس لي أن
أُدخِل قراري مكانَ قرارك، ولا أن أُسمّي سكوتَك موافقةً. والبنيةُ تمنع ذلك، لا
الأدبُ وحدَه.

`DELEGATION_IS_NOT_A_SIGNATURE`: سُئل المودِعُ عن الفروع فأجاب «لا تفضيل» في
ثلاثتها. وذلك تفويضٌ لا اختيارُ فرع، فلا يُقيَّد `TAKEN` باسمه — إذ يُنسِب إليه
فرعًا لم يُسمِّه — ولا يبقى `PENDING` — إذ يُخفي أنّه فوَّض. فأُضيفت منزلةٌ
رابعةٌ `DELEGATED` بتاريخها وسببها، وفيها يُسمّى **الوكيلُ** في حقلٍ آخَرَ غيرِ
حقل السلطة؛ فالجلسةُ لا تكون سلطةً أبدًا، وتكون وكيلًا مُسمًّى.

`BLOCKED_IS_NOT_FAILED`: اختبار [123] ليس أحمرَ؛ هو **غيرُ مُشغَّل**، والسجلُّ
يقول بأيّ قرارٍ حُجِب. وبين «سقط» و«لم يُجرَ» فرقٌ لا يُطوى.

`A_RECORDED_PRICE_IS_NOT_A_LIVE_ONE`: الأثمانُ المذكورةُ قراءاتٌ بتاريخها، لا
قياسٌ حاضر. و`recompute_scope_price` تُعيد القياسَ حين تكون الشجرةُ الأصليّةُ
قابلةً للاستيراد، وتُرجِع `None` حين لا تكون — ولا تُلفّق رقمًا.

`THE_QUIETER_FORK_IS_PRICED_TOO`: لفرعٍ واحدٍ من قرار النطاق ثمنٌ ليس رقمًا:
يُخرِج الإيداعاتِ من تعريف النطاق، فلا يتغيّر عددٌ ويتغيّر **معنى** المقيس بلا
أن يُعلِن مقياسٌ تغيُّرَه. فذُكِر بثمنه كي لا يُختار مجّانًا.

`THE_REGISTER_IS_INSIDE_WHAT_IT_PRICES`: هذه الوحدةُ ملفٌّ في النطاق الذي
تُسعّره، فإدخالُ القرار الشجرةَ حرّك بواحدٍ العددَ الذي يُقاس به فرعٌ من فروعه.
فكُشِف القِدَمُ ولم يُصحَّح الرقمُ في محلّه؛ وهو بعضُ ثمنِ «إعادة التجميد»
معروضًا على نفسه.

`ABSENCE_IS_NOT_A_DECISION`: حاجزُ جدول الصفة ليس قرارًا معلَّقًا بل **بايتاتٌ
غائبة**؛ فلا يدخل هذا السجلَّ، ويبقى في `sifa_table_deposit` حيث يُقاس ثمنُ
استيراده قبل الاستيراد.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا حكمَ هنا على العربيّة، ولا ولادةَ، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Final

__all__ = [
    "ABSENCE_IS_NOT_A_DECISION_NOTE",
    "A_PENDING_DECISION_IS_NOT_A_DEFAULT_NOTE",
    "A_RECORDED_PRICE_IS_NOT_A_LIVE_ONE_NOTE",
    "DELEGATION_IS_NOT_A_SIGNATURE_NOTE",
    "BLOCKED_IS_NOT_FAILED_NOTE",
    "DECISIONS",
    "DECISION_REGISTER_NAMED_RESIDUALS",
    "REFUSED_AUTHORITIES",
    "SCOPE_READING",
    "THE_QUIETER_FORK_IS_PRICED_TOO_NOTE",
    "THE_REGISTER_IS_INSIDE_WHAT_IT_PRICES_NOTE",
    "THE_SESSION_CANNOT_SIGN_A_DECISION_NOTE",
    "Branch",
    "Decision",
    "DecisionRegisterError",
    "DecisionStanding",
    "LivePrice",
    "ScopeReading",
    "assert_not_reportable_as_done",
    "blocked_items",
    "bonferroni_denominator",
    "delegated_decisions",
    "blockers_of",
    "is_blocked",
    "pending_decisions",
    "recompute_scope_price",
    "register_digest",
    "render_register",
    "taken_decisions",
]


class DecisionRegisterError(ValueError):
    """رُفض قرارٌ ناقصٌ أو تمامٌ محجوب؛ ولا يُحمَل على أقرب مقبول."""


class DecisionStanding(Enum):
    """منازلُ القرار، مغلقةً أربعًا: لا منزلةَ اسمُها «مفترَض» ولا «الأرجح».

    و`DELEGATED` أُضيفت بتعديلٍ مؤرَّخ (2026-09-22) لسببٍ مُسمًّى: سُئل المودِعُ
    عن فروع القرارات الثلاثة فأجاب «لا تفضيل» في ثلاثتها، وذلك **تفويضٌ لا
    اختيارُ فرع**. فتقييدُه `TAKEN` باسمه يُنسِب إليه فرعًا لم يُسمِّه، وتركُه
    `PENDING` يُخفي أنّه فوَّض. فصارت المنزلةُ الرابعةُ هي ما يُقال فيه الصدق.
    """

    PENDING = "معلَّق"
    TAKEN = "متَّخَذ"
    DELEGATED = "مُفوَّض"
    DECLINED = "مردود"


REFUSED_AUTHORITIES: Final[tuple[str, ...]] = (
    "الجلسة",
    "المساعد",
    "claude",
    "Claude",
    "assistant",
)
"""سلطاتٌ مرفوضةٌ بالبناء: لا يُوقِّع القرارَ مَن يكتب السجلّ."""

_REFUSED_STANDING_NAMES: Final[tuple[str, ...]] = (
    "ASSUMED",
    "DEFAULT",
    "IMPLIED",
    "LIKELY",
    "PROBABLY",
)


@dataclass(frozen=True, slots=True)
class Branch:
    """فرعُ قرارٍ باسمه وأثرِه **وثمنِه**؛ وفرعٌ بلا ثمنٍ لا يُقيَّد."""

    label: str
    what_changes: str
    price: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.label, "اسمُ الفرع"),
            (self.what_changes, "ما يتغيّر"),
            (self.price, "الثمن"),
        ):
            if not value.strip():
                raise DecisionRegisterError(
                    f"{name} شرطُ إنشاءٍ لا وصفٌ اختياريّ؛ وفرعٌ بلا ثمنٍ "
                    "يُختار مجّانًا ثمّ يُدفع ثمنُه بعد النظر."
                )


@dataclass(frozen=True, slots=True)
class Decision:
    """قرارٌ مُقيَّد: سؤالُه، وما يحجُبه، وفروعُه، ومنزلتُه — ولا سلطةَ مُلفَّقة."""

    identifier: str
    question: str
    blocks: tuple[str, ...]
    branches: tuple[Branch, ...]
    standing: DecisionStanding = DecisionStanding.PENDING
    taken_branch: str | None = None
    authority: str | None = None
    delegate: str | None = None
    decided_on: date | None = None
    note: str = ""

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise DecisionRegisterError("قرارٌ بلا معرِّفٍ لا يُحال إليه باسمه.")
        if not self.question.strip().endswith("؟"):
            raise DecisionRegisterError(
                f"{self.identifier}: سؤالُ القرار يُصاغ سؤالًا وينتهي بعلامته؛ "
                "وصياغتُه خبرًا تُخفي أنّه لم يُحسَم."
            )
        if not self.blocks:
            raise DecisionRegisterError(
                f"{self.identifier}: ما يحجُبه القرارُ شرطُ إنشاء؛ وقرارٌ لا "
                "يحجُب شيئًا لا يُقيَّد سجلًّا."
            )
        if len(self.branches) < 2:
            raise DecisionRegisterError(
                f"{self.identifier}: القرارُ فرعان على الأقلّ؛ وفرعٌ واحدٌ ليس "
                "قرارًا بل إعلانًا."
            )
        labels = [branch.label for branch in self.branches]
        if len(set(labels)) != len(labels):
            raise DecisionRegisterError(f"{self.identifier}: فرعان بالاسم نفسِه.")
        if self.authority is not None and self.authority.strip() in REFUSED_AUTHORITIES:
            raise DecisionRegisterError(
                f"{self.identifier}: السلطةُ «{self.authority}» مرفوضةٌ بالبناء؛ "
                "ولا يُوقِّع القرارَ مَن يكتب السجلّ."
            )
        if self.standing is DecisionStanding.DELEGATED:
            if self.delegate is None or not self.delegate.strip():
                raise DecisionRegisterError(
                    f"{self.identifier}: قرارٌ مُفوَّضٌ بلا مَن اختار؛ "
                    "والوكيلُ يُسمّى وإلّا قُرئ اختيارُه كلامَ الموكِّل."
                )
            if self.taken_branch is None:
                raise DecisionRegisterError(
                    f"{self.identifier}: قرارٌ مُفوَّضٌ بلا فرعٍ مُسمًّى؛ "
                    "والتفويضُ لا يُغلِق قرارًا بلا فرع."
                )
            if self.taken_branch not in labels:
                raise DecisionRegisterError(
                    f"{self.identifier}: الفرعُ «{self.taken_branch}» ليس من "
                    "فروعه المُقيَّدة."
                )
        elif self.delegate is not None:
            raise DecisionRegisterError(
                f"{self.identifier}: وكيلٌ في قرارٍ غيرِ مُفوَّض؛ ومَن اختار "
                "بنفسه ليس وكيلًا عن نفسه."
            )
        if self.standing is DecisionStanding.PENDING:
            if self.taken_branch is not None or self.authority is not None:
                raise DecisionRegisterError(
                    f"{self.identifier}: قرارٌ معلَّقٌ بفرعٍ مُتَّخَذٍ أو سلطةٍ "
                    "مُوقِّعة؛ والمعلَّقُ لا يصير فرعًا بالسكوت."
                )
            if self.decided_on is not None:
                raise DecisionRegisterError(f"{self.identifier}: قرارٌ معلَّقٌ بتاريخِ حسم.")
        else:
            if self.authority is None or not self.authority.strip():
                raise DecisionRegisterError(
                    f"{self.identifier}: قرارٌ محسومٌ أو مُفوَّضٌ بلا سلطةٍ "
                    "مسمّاة؛ ومَن يملك القرارَ شرطُ إنشاءٍ لا حاشية."
                )
            if self.decided_on is None:
                raise DecisionRegisterError(f"{self.identifier}: قرارٌ محسومٌ بلا تاريخ.")
        if self.standing is DecisionStanding.TAKEN:
            if self.taken_branch is None:
                raise DecisionRegisterError(
                    f"{self.identifier}: قرارٌ متَّخَذٌ بلا فرعٍ مُسمًّى."
                )
            if self.taken_branch not in labels:
                raise DecisionRegisterError(
                    f"{self.identifier}: الفرعُ «{self.taken_branch}» ليس من "
                    "فروعه المُقيَّدة."
                )
        if self.standing is DecisionStanding.DECLINED and self.taken_branch is not None:
            raise DecisionRegisterError(f"{self.identifier}: قرارٌ مردودٌ بفرعٍ مُتَّخَذ.")


@dataclass(frozen=True, slots=True)
class ScopeReading:
    """قراءةُ ثمنِ قرار النطاق بتاريخها؛ وهي قراءةٌ لا قياسٌ حاضر."""

    read_on: date
    measured_files: int
    frozen_files: int
    measured_text_bytes: int
    frozen_text_bytes: int
    measured_pairs: int
    frozen_pairs: int
    red_tests: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.measured_files == self.frozen_files:
            raise DecisionRegisterError(
                "قراءةٌ لا فرقَ فيها لا تُقيَّد ثمنًا؛ فإن تساوى العددان فلا "
                "قرارَ نطاقٍ ههنا."
            )
        if not self.red_tests:
            raise DecisionRegisterError(
                "أسماءُ الاختبارات الحمراء شرطُ إنشاء؛ وثمنٌ بلا شاهدٍ مسمًّى " "يُقرأ تقديرًا."
            )

    @property
    def added_files(self) -> int:
        """ما زادته الإيداعاتُ على النطاق المُجمَّد، مُشتَقًّا لا مكتوبًا."""

        return self.measured_files - self.frozen_files

    @property
    def added_pairs(self) -> int:
        """ما زاده الاتّساعُ على أزواج الرُّتبة الثالثة."""

        return self.measured_pairs - self.frozen_pairs


SCOPE_READING: Final[ScopeReading] = ScopeReading(
    read_on=date(2026, 9, 22),
    measured_files=430,
    frozen_files=414,
    measured_text_bytes=8_013_569,
    frozen_text_bytes=7_731_852,
    measured_pairs=17_800,
    frozen_pairs=17_154,
    red_tests=(
        "tests/arabic/test_pair_sample_widening.py::"
        "test_the_scope_fingerprint_is_read_from_disk_and_matches_the_frozen_one",
        "tests/arabic/test_pair_sample_widening.py::"
        "test_the_transcribed_third_rung_figures_match_what_disk_measures",
        "tests/program/test_project_state.py::"
        "test_vision_document_carries_the_rendered_block_verbatim",
    ),
)
"""ثمنُ قرار النطاق كما قُرئ في 2026-09-22؛ والحمرةُ خبرٌ عن الاتّساع لا عطب."""


DECISIONS: Final[tuple[Decision, ...]] = (
    Decision(
        identifier="ق-1 بسطُ بونفيروني",
        question="ما الذي يعدُّه الرقمُ ٦ في α = 0.05/6؟",
        blocks=("تشغيلُ اختبار [123] كما جُمِّد",),
        branches=(
            Branch(
                label="تعدادُ الخلايا الستّ صراحةً",
                what_changes=(
                    "يصير المقامُ مفحوصًا قبل العدّ، فيُقارَن بعدد الخلايا "
                    "المُختبَرة فعلًا كما يشترط المقياسُ المُعلَن"
                ),
                price=(
                    "إن كانت الخلايا أكثرَ من ستٍّ فالحدُّ المُعلَن أوسعُ من "
                    "الصحيح، وتُعاد قراءةُ كلّ دلالةٍ حُسِبت به"
                ),
            ),
            Branch(
                label="إعلانُ عائلةٍ أوسعَ بمقامٍ جديد",
                what_changes=(
                    "يُعلَن مقامُ التصحيح على العائلة كلِّها (كتلة × كتلة × "
                    "نوعَ علاقة) لا على ستٍّ"
                ),
                price=(
                    "يشتدُّ الحدُّ فيضعف كلُّ فرقٍ حُدوديّ، وقد يسقط أثرٌ كان "
                    "دالًّا تحت المقام الأوّل"
                ),
            ),
            Branch(
                label="العائلةُ كما نصَّ المقياس: 75 خليّةً مرتَّبة",
                what_changes=(
                    "يُشتَقُّ المقامُ من نصّ المقياس المُجمَّد حرفيًّا: خمسُ "
                    "كتلٍ × خمسُ كتلٍ **مرتَّبةً** (فالخانتان متمايزتان، "
                    "فكتلةُ C₁ ليست كتلةَ C₃) × ثلاثةَ أزواجِ خانات = 75؛ "
                    "فيصير α = 0.05/75 ≈ 0.000667"
                ),
                price=(
                    "أشدُّ الحدود: يضعف كلُّ فرقٍ حُدوديّ وقد يسقط أثرٌ كان "
                    "دالًّا تحت المقام الأوّل. وقد تكون الخلايا المُختبَرةُ "
                    "فعلًا أقلَّ من 75، والأقلُّ لا يُستعمَل إلّا إن أُعلِن "
                    "قبل النظر — و75 هو الحدُّ المُعلَن قَبْلِيًّا"
                ),
            ),
            Branch(
                label="تثبيتُ α بلا تصحيحٍ وإعلانُ ذلك",
                what_changes="يُرفَع التصحيحُ ويُعلَن أنّ الحدَّ غيرُ مصحَّح",
                price=(
                    "يعلو احتمالُ الإيجاب الكاذب مع عدد الخلايا، ويصير كلُّ "
                    "أثرٍ مُعلَنًا تحت هذا الحدّ مشروطًا به صريحًا"
                ),
            ),
        ),
        standing=DecisionStanding.DELEGATED,
        authority="Saleh1967 (المودِع) — فوَّض بـ«لا تفضيل» في 2026-09-22",
        delegate="وكيلُ الجلسة (Claude Code)",
        decided_on=date(2026, 9, 22),
        taken_branch="العائلةُ كما نصَّ المقياس: 75 خليّةً مرتَّبة",
        note=(
            "المقياسُ المُجمَّد يقول: «بونفيروني على عدد خلايا (كتلة × كتلة × "
            "نوع علاقة) المُختبَرة، ويُعلَن العددُ قبل العدّ لا بعده». **والرقمُ "
            "6 لا يُعاد بناؤه من هذا النصّ بأيّ قراءة**: الكتلُ المولودةُ خمسٌ "
            "وأزواجُ الخانات ثلاثةٌ، فالمرتَّبُ 75 وغيرُ المرتَّب 45؛ ولا يُخرِج "
            "6 إلّا قراءةٌ أخرى لم يكتبها المقياسُ (ثلاثةُ أزواجِ خانات × "
            "قيدَي التجانس والتماثل). فاختار الوكيلُ نصَّ المقياس على الرقم: "
            "يُشتَقُّ المقامُ من النصّ المُجمَّد ولا يُعدَّل النصُّ ليوافق رقمًا. "
            "وسقوطُ 6 يُسجَّل نتيجةً لا يُصحَّح صمتًا"
        ),
    ),
    Decision(
        identifier="ق-2 فرعُ الإغلاق",
        question="أفضاءٌ بمخرجَين، أم δ ثانيةٌ لفرع الإغلاق؟",
        blocks=("تشغيلُ اختبار [123] كما جُمِّد",),
        branches=(
            Branch(
                label="فضاءٌ بمخرجَين",
                what_changes=(
                    "يُلغى فرعُ «الإغلاق بشاهدٍ موجب»، فيصير المخرَجان: فرقٌ "
                    "دالٌّ، أو فرقٌ لم يظهر"
                ),
                price=(
                    "لا يُقال بعدها إنّ السلسلةَ كافيةٌ، بل إنّ الفرقَ لم يظهر "
                    "في هذا الحجم — وهو أضعفُ ممّا كان مُسجَّلًا"
                ),
            ),
            Branch(
                label="δ ثانيةٌ لفرع الإغلاق",
                what_changes=(
                    "يُعلَن فرقٌ أصغرُ حدًّا للتكافؤ، فيصير الإغلاقُ بشاهدٍ "
                    "موجبٍ فرعًا قابلًا للبلوغ"
                ),
                price=(
                    "يحتاج حجمَ عيّنةٍ أكبرَ؛ فعند δ = 0.10 كان فرعُ الإغلاق "
                    "غيرَ قابلٍ للبلوغ أصلًا بحساب القوّة"
                ),
            ),
        ),
        standing=DecisionStanding.DELEGATED,
        authority="Saleh1967 (المودِع) — فوَّض بـ«لا تفضيل» في 2026-09-22",
        delegate="وكيلُ الجلسة (Claude Code)",
        decided_on=date(2026, 9, 22),
        taken_branch="فضاءٌ بمخرجَين",
        note=(
            "سقوطُ إغلاق التركيب مُعاد إنتاجُه (تماثل C1C3: 0.139 و0.144)، وهو "
            "دافعٌ لا تأكيد: يقول إنّ السلسلةَ لا تكفي، ولا يقول إنّ المثلّثَ "
            "هو البديل. واختار الوكيلُ الأضعفَ دعوًى: عند δ = 0.10 كان فرعُ "
            "«الإغلاق بشاهدٍ موجب» غيرَ قابلٍ للبلوغ بحساب القوّة، فإبقاؤه "
            "يجعل «لم يظهر الفرقُ» يُقرأ «السلسلةُ كافية» — وهو ما لا يحمله "
            "الحساب. فالمخرَجان: فرقٌ دالٌّ، أو فرقٌ لم يظهر في هذا الحجم"
        ),
    ),
    Decision(
        identifier="ق-3 نطاقُ النثر",
        question=(
            "أتُعاد أرقامُ نطاق النثر تجميدًا على الشجرة بعد الإيداعات، أم "
            "تبقى كما نُشرت؟"
        ),
        blocks=(
            "خضرةُ المجموعة كاملةً في Alghanem",
            "قراءةُ أرقام النطاق في README خبرًا عن الحاضر",
        ),
        branches=(
            Branch(
                label="إعادةُ التجميد",
                what_changes=(
                    "تعود الاختباراتُ الثلاثةُ خضراءَ، ويصير المُجمَّدُ مطابقًا "
                    "لما تقيسه الشجرةُ اليوم"
                ),
                price=(
                    "تتغيّر أرقامٌ منشورةٌ في السجلّ (414 → 430 ملفًا، "
                    "و17,154 → 17,800 زوجًا)، فيحتاج ما قِيس عليه سابقًا "
                    "إحالةً بالاسم لا استبدالًا صامتًا"
                ),
            ),
            Branch(
                label="الإبقاءُ على المُجمَّد",
                what_changes="لا يتحرّك رقمٌ منشور، ويبقى المُجمَّدُ شاهدًا على وقته",
                price=(
                    "تبقى ثلاثةُ اختباراتٍ حمراءَ؛ وحمرتُها خبرٌ صحيحٌ عن "
                    "اتّساع النطاق لا عطبٌ يُسكَت"
                ),
            ),
            Branch(
                label="إخراجُ الإيداعات من تعريف النطاق",
                what_changes="يعود العددُ المقيسُ إلى 414 بلا تغيير رقمٍ منشور",
                price=(
                    "تفريعٌ أهدأ: لا يتغيّر عددٌ ويتغيّر **معنى** «النطاق» بلا "
                    "أن يُعلِن مقياسٌ تغيُّرَه — وهو أخفى الفروع أثرًا وأثقلُها"
                ),
            ),
        ),
        standing=DecisionStanding.DELEGATED,
        authority="Saleh1967 (المودِع) — فوَّض بـ«لا تفضيل» في 2026-09-22",
        delegate="وكيلُ الجلسة (Claude Code)",
        decided_on=date(2026, 9, 22),
        taken_branch="الإبقاءُ على المُجمَّد",
        note=(
            "الاختباراتُ الثلاثةُ الحمراءُ أثرُ إيداعاتي أنا، والرابعُ "
            "(test_external_audit) سابقٌ لها وبيئيّ: مسارٌ مُجمَّدٌ لبيئة CI. "
            "واختار الوكيلُ أقلَّ الفروع رجعةً: الإبقاءُ لا يُحرّك رقمًا "
            "منشورًا في سجلٍّ لا يملك الوكيلُ الدفعَ إليه، والحمرةُ تبقى خبرًا "
            "صحيحًا يُقرأ في سطرٍ واحد. وهو الفرعُ الوحيدُ الذي يُنقَض بكلمةٍ "
            "من المودِع بلا أن يكون شيءٌ قد تغيّر"
        ),
    ),
)
"""القراراتُ المُقيَّدة؛ وثلاثتُها **مُفوَّضةٌ** لا متَّخَذةٌ ولا معلَّقة."""


def pending_decisions() -> tuple[Decision, ...]:
    """ما لم يُحسَم، مُشتَقًّا بالمنزلة لا مكتوبًا."""

    return tuple(
        decision
        for decision in DECISIONS
        if decision.standing is DecisionStanding.PENDING
    )


def taken_decisions() -> tuple[Decision, ...]:
    """ما حُسِم بفرعٍ مُسمًّى وسلطةٍ مسمّاة."""

    return tuple(
        decision
        for decision in DECISIONS
        if decision.standing is DecisionStanding.TAKEN
    )


def delegated_decisions() -> tuple[Decision, ...]:
    """ما فوَّضه مالكُه فاختار الوكيلُ فرعَه؛ وهو منزلةٌ بين المعلَّق والمتَّخَذ."""

    return tuple(
        decision
        for decision in DECISIONS
        if decision.standing is DecisionStanding.DELEGATED
    )


def blocked_items() -> tuple[str, ...]:
    """كلُّ ما يحجُبه قرارٌ معلَّق، مرتَّبًا ترتيبًا ثابتًا."""

    items = {item for decision in pending_decisions() for item in decision.blocks}
    return tuple(sorted(items))


def blockers_of(item: str) -> tuple[Decision, ...]:
    """القراراتُ المعلَّقةُ التي تحجُب شيئًا بعينه."""

    return tuple(
        decision for decision in pending_decisions() if item in decision.blocks
    )


def is_blocked(item: str) -> bool:
    """هل يحجُبه قرارٌ معلَّق؟"""

    return bool(blockers_of(item))


def assert_not_reportable_as_done(item: str) -> None:
    """ردُّ إعلانِ تمامٍ لشيءٍ يحجُبه قرارٌ معلَّق؛ والحجبُ يُقال لا يُسكَت."""

    blockers = blockers_of(item)
    if blockers:
        named = "، ".join(decision.identifier for decision in blockers)
        raise DecisionRegisterError(
            f"«{item}» محجوبٌ بقرارٍ معلَّق ({named})؛ ولا يُعلَن تمامًا. "
            "والمحجوبُ ليس ساقطًا: هو غيرُ مُشغَّل، والسجلُّ يقول بأيّ قرار."
        )


@dataclass(frozen=True, slots=True)
class LivePrice:
    """ثمنُ ق-3 مقيسًا الآن، مع قِدَمِ القراءة المُقيَّدة مكشوفًا لا مُصحَّحًا."""

    live_files: int
    frozen_files: int
    recorded_files: int

    @property
    def drift_from_recording(self) -> int:
        """كم تحرّك العددُ المقيسُ عن القراءة المُقيَّدة."""

        return self.live_files - self.recorded_files

    @property
    def recording_is_stale(self) -> bool:
        """هل صارت القراءةُ المُقيَّدةُ قديمة؟"""

        return self.drift_from_recording != 0


def recompute_scope_price() -> LivePrice | None:
    """أعِد قياسَ ثمن ق-3 من الشجرة إن كانت قابلةً للاستيراد، وإلّا `None`.

    ولا يُلفَّق رقمٌ عند الغياب، ولا تُصحَّح القراءةُ المُقيَّدةُ في محلّها: هي
    قراءةٌ بتاريخها، وهذه الدالّةُ هي ما يُعرَف به أنّها قديمة.
    """

    try:
        from .pair_sample_widening import (
            PROSE_SCOPE_AT_MEASUREMENT,
            prose_scope_fingerprint,
        )
    except Exception:
        return None
    return LivePrice(
        live_files=prose_scope_fingerprint().files,
        frozen_files=PROSE_SCOPE_AT_MEASUREMENT.files,
        recorded_files=SCOPE_READING.measured_files,
    )


def bonferroni_denominator() -> int:
    """مقامُ بونفيروني **مُشتَقًّا** من نصّ المقياس المُجمَّد لا مكتوبًا.

    النصُّ: «بونفيروني على عدد خلايا (كتلة × كتلة × نوع علاقة) المُختبَرة».
    والكتلُ المولودةُ في `slgae_deposit`، وأزواجُ الخانات في `slot_rights_algebra`؛
    والخانتان متمايزتان فكتلةُ `C₁` ليست كتلةَ `C₃`، فالضربُ مرتَّب.

    وهذه الدالّةُ هي ما يجعل الفرعَ المُختار في ق-1 **حسابًا لا جملة**: إن
    تغيّرت الكتلُ أو الأزواجُ تغيّر المقامُ معها، ولا يبقى رقمًا مُجمَّدًا في
    نصّ.
    """

    from .slgae_deposit import BORN_BLOCKS
    from .slot_rights_algebra import RelationType

    return len(BORN_BLOCKS) ** 2 * len(RelationType)


def register_digest() -> str:
    """بصمةُ السجلّ: قرارٌ يُغيَّر لاحقًا يُعرَف بتغيُّر البصمة."""

    parts: list[str] = []
    for decision in DECISIONS:
        parts.append(decision.identifier)
        parts.append(decision.question)
        parts.append(decision.standing.name)
        parts.append(decision.taken_branch or "-")
        parts.append(decision.authority or "-")
        parts.append(decision.delegate or "-")
        parts.extend(decision.blocks)
        for branch in decision.branches:
            parts.extend((branch.label, branch.what_changes, branch.price))
        parts.append(decision.note)
    payload = "\n".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def render_register() -> str:
    """اعرض السجلَّ جدولًا؛ والوحدةُ سلطةُ هذا النصّ، فلا يُحرَّر في محلّه."""

    lines = [
        "| القرار | السؤال | المنزلة | الفرعُ المُختار | مَن اختار | ما يحجُبه |",
        "|---|---|---|---|---|---|",
    ]
    for decision in DECISIONS:
        blocks = "؛ ".join(decision.blocks)
        chosen = decision.taken_branch or "—"
        chooser = decision.delegate or decision.authority or "—"
        lines.append(
            f"| {decision.identifier} | {decision.question} | "
            f"{decision.standing.value} | {chosen} | {chooser} | {blocks} |"
        )
    lines.append("")
    lines.append(f"بصمةُ السجلّ: `{register_digest()[:16]}…`")
    return "\n".join(lines)


A_PENDING_DECISION_IS_NOT_A_DEFAULT_NOTE: Final[str] = (
    "APendingDecisionIsNotADefault: المعلَّقُ لا يصير فرعًا بالسكوت، وإعلانُ "
    "تمامِ ما يحجُبه قرارٌ معلَّقٌ مردودٌ عند الاستدعاء لا موصوفٌ في حاشية"
)

THE_SESSION_CANNOT_SIGN_A_DECISION_NOTE: Final[str] = (
    "TheSessionCannotSignADecision: القرارُ المحسومُ يحتاج سلطةً مسمّاةً "
    "وتاريخًا، والجلسةُ والمساعدُ مرفوضان سلطةً بالبناء؛ فلا يُدخَل قراري "
    "مكانَ قرارك ولا يُسمّى السكوتُ موافقة"
)

BLOCKED_IS_NOT_FAILED_NOTE: Final[str] = (
    "BlockedIsNotFailed: اختبار [123] غيرُ مُشغَّلٍ لا ساقط، والسجلُّ يقول بأيّ "
    "قرارٍ حُجِب؛ وبين «سقط» و«لم يُجرَ» فرقٌ لا يُطوى"
)

A_RECORDED_PRICE_IS_NOT_A_LIVE_ONE_NOTE: Final[str] = (
    "ARecordedPriceIsNotALiveOne: أثمانُ ق-3 قراءةُ 2026-09-22 لا قياسٌ حاضر، "
    "وrecompute_scope_price تُرجِع None عند الغياب ولا تُلفّق رقمًا"
)

THE_QUIETER_FORK_IS_PRICED_TOO_NOTE: Final[str] = (
    "TheQuieterForkIsPricedToo: إخراجُ الإيداعات من تعريف النطاق لا يغيّر عددًا "
    "ويغيّر معنى المقيس بلا أن يُعلِن مقياسٌ تغيُّرَه؛ فذُكِر بثمنه كي لا يُختار "
    "مجّانًا"
)

THE_REGISTER_IS_INSIDE_WHAT_IT_PRICES_NOTE: Final[str] = (
    "TheRegisterIsInsideWhatItPrices: هذه الوحدةُ ملفٌّ في النطاق الذي تُسعّره، "
    "فإدخالُ القرار الشجرةَ يزيد العددَ الذي يُقاس به أحدُ فروعه بواحد؛ فقراءةُ "
    "430 صارت قديمةً بإيداعها نفسِه، ولم تُصحَّح في محلّها بل كُشِف قِدَمُها — "
    "وذلك بعضُ ثمن فرع «إعادة التجميد»: كلُّ إيداعٍ يُحرّك ما يُجمَّد"
)

DELEGATION_IS_NOT_A_SIGNATURE_NOTE: Final[str] = (
    "DelegationIsNotASignature: «لا تفضيل» تفويضٌ لا اختيارُ فرع، فالفرعُ "
    "المُقيَّدُ ههنا قراءةُ الوكيل لا كلمةُ المودِع؛ ولا يُستشهَد به تجميدًا "
    "منه، ويُنقَض بكلمةٍ واحدةٍ منه بلا أن يكون شيءٌ قد تغيّر. ومنزلةُ "
    "«مُفوَّض» أُضيفت لهذا وحدَه: لئلّا يُنسَب إليه فرعٌ لم يُسمِّه، ولا يُخفى "
    "أنّه فوَّض"
)

ABSENCE_IS_NOT_A_DECISION_NOTE: Final[str] = (
    "AbsenceIsNotADecision: حاجزُ جدول الصفة بايتاتٌ غائبةٌ لا قرارٌ معلَّق، "
    "فلا يدخل هذا السجلَّ ويبقى حيث يُقاس ثمنُ استيراده قبل الاستيراد"
)

DECISION_REGISTER_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_PENDING_DECISION_IS_NOT_A_DEFAULT_NOTE,
    THE_SESSION_CANNOT_SIGN_A_DECISION_NOTE,
    BLOCKED_IS_NOT_FAILED_NOTE,
    A_RECORDED_PRICE_IS_NOT_A_LIVE_ONE_NOTE,
    THE_QUIETER_FORK_IS_PRICED_TOO_NOTE,
    THE_REGISTER_IS_INSIDE_WHAT_IT_PRICES_NOTE,
    DELEGATION_IS_NOT_A_SIGNATURE_NOTE,
    ABSENCE_IS_NOT_A_DECISION_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


# يُفحَص عند كلّ استيراد: سجلٌّ يفقد شرطًا يمنع تحميلَ الوحدة.
if len(DecisionStanding) != 4:  # pragma: no cover - حارس
    raise RuntimeError("منازلُ القرار أربعٌ مغلقةٌ: معلَّقٌ ومتَّخَذٌ ومُفوَّضٌ ومردود.")
if any(name in _REFUSED_STANDING_NAMES for name in DecisionStanding.__members__):
    raise RuntimeError(  # pragma: no cover - حارس
        "منزلةٌ اسمُها «مفترَض» أو «الأرجح» تجعل المعلَّقَ محسومًا بالسكوت."
    )
if not DECISIONS:  # pragma: no cover - حارس
    raise RuntimeError("سجلٌّ بلا قرارٍ واحدٍ لا يُقيَّد.")
if len({decision.identifier for decision in DECISIONS}) != len(DECISIONS):
    raise RuntimeError("معرِّفان متكرّران في السجلّ.")  # pragma: no cover - حارس
if any(
    decision.authority is not None and decision.authority in REFUSED_AUTHORITIES
    for decision in DECISIONS
):  # pragma: no cover - حارس
    raise RuntimeError("سلطةٌ مرفوضةٌ وقّعت قرارًا في السجلّ.")
if any(
    decision.delegate is not None and decision.delegate == decision.authority
    for decision in DECISIONS
):  # pragma: no cover - حارس
    raise RuntimeError("الوكيلُ هو الموكِّلُ في قرارٍ؛ وذلك يُلغي الفرقَ بينهما.")
if bonferroni_denominator() != 75:  # pragma: no cover - حارس
    raise RuntimeError(
        "مقامُ بونفيروني المُشتَقُّ من نصّ المقياس تغيّر؛ فالفرعُ المُختار في "
        "ق-1 يُعاد إليه قبل أيّ تشغيل."
    )
if len(register_digest()) != 64:  # pragma: no cover - حارس
    raise RuntimeError("بصمةُ السجلّ ليست sha256.")
