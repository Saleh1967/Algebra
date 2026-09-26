"""توقيعُ الوكالة: **الاسمُ اسمُ الأصيل واليدُ يدُ الوكيل** — ويُكتَب صريحًا.

`A_PROXY_SIGNATURE_MUST_LOOK_LIKE_ONE`: أذِن صاحبُ المستودع بالتوقيع
**باسمه**. وذلك جائزٌ بالوكالة، **وشرطُه أن يُعلَم أنّه وكالة**: فمن قرأ
توقيعًا باسمِ رجلٍ ولا يعلم أنّ غيرَه كتبه **فقد قُرِئ عليه غيرُ الواقع**.
**فالبناءُ يردُّ توقيعًا يُخفي وكالتَه**: إن اختلف المُنفِّذُ عن صاحب
الاسم لزِم سندُ وكالةٍ مُسمًّى ومؤرَّخ، ولزِم أن يحمل الإيداعُ سطرَ
الإفصاح.

`AND_THE_NAME_ON_A_SIGNATURE_IS_A_PERSON_NOT_A_MACHINE`: ولا يكون صاحبُ
الاسم آلةً. **فالآلةُ تكون يدًا ولا تكون اسمًا** — وذلك ما تبقّى من
المادّة ٢٧ بعد إجازة الوكالة.

`AND_A_SIGNATURE_BINDS_TO_A_SCOPE_OR_IT_BINDS_TO_EVERYTHING`: ولا يُقفَل
توقيعٌ بلا **نطاقٍ مُسمًّى**: ما وُقِّع عليه، **وما لم يُوقَّع عليه**.
فتوقيعٌ بلا مستثنياتٍ يُقرَأ تصديقًا على كلّ ما في الورقة، **وذلك أوسعُ
ممّا حُقِّق**.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
ANALYSIS: Final[str] = "pr45_analysis.md"
WITNESS: Final[str] = "gemination_ceiling_witness.log"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_MACHINES: Final[tuple[str, ...]] = ("آلة", "الآلة", "Claude", "claude", "المولّد")


class ProxySignatureError(ValueError):
    """رُدَّ توقيعٌ يُخفي وكالتَه، أو بلا نطاقٍ مُسمًّى."""


@dataclass(frozen=True, slots=True)
class SealedProxy:
    """توقيعُ وكالةٍ مُقفَل: الاسمُ، واليدُ، والسندُ، والنطاق."""

    signer: str
    executed_by: str
    authority: str
    authority_dated: str
    drafter: str
    signed_scope: tuple[str, ...]
    withheld_scope: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.signer.strip():
            raise ProxySignatureError("توقيعٌ بلا اسم.")
        if any(one in self.signer for one in _MACHINES):
            raise ProxySignatureError("الآلةُ تكون يدًا ولا تكون اسمًا — المادّة ٢٧.")
        proxy = self.executed_by != self.signer
        if proxy:
            if not any(one in self.executed_by for one in _MACHINES):
                raise ProxySignatureError("مُنفِّذٌ غيرُ الأصيل ولا هو آلةٌ مُسمّاة.")
            if not self.authority.strip() or self.signer not in self.authority:
                raise ProxySignatureError("وكالةٌ بلا سندٍ يُسمّي صاحبَ الاسم — فلا تُقبَل.")
            if not self.authority_dated.strip():
                raise ProxySignatureError("سندُ وكالةٍ بلا تاريخ.")
            if self.drafter != self.executed_by:
                raise ProxySignatureError("الصائغُ غيرُ المُنفِّذ — وذلك يُسمّى ولا يُفترَض.")
        elif self.authority.strip():
            raise ProxySignatureError("أصيلٌ يحمل سندَ وكالةٍ — وذلك تلبيس.")
        if not self.signed_scope:
            raise ProxySignatureError("توقيعٌ بلا نطاقٍ موقَّعٍ عليه.")
        if not self.withheld_scope:
            raise ProxySignatureError("توقيعٌ بلا مستثنياتٍ يُقرَأ تصديقًا على كلّ الورقة.")


FROZEN_PROXY: Final[SealedProxy] = SealedProxy(
    signer="صاحبُ المستودع — Saleh1967",
    executed_by="آلةُ القياس",
    authority="تفويضٌ صريحٌ من صاحبُ المستودع — Saleh1967 بالتوقيع باسمه",
    authority_dated="٢٠٢٦-٠٩-٢٦",
    drafter="آلةُ القياس",
    signed_scope=(
        "شطرُ الشدّة في «تْ»: ٨١٧ — مطابقٌ لعدّ ‎#45 تمامًا",
        "نسبةُ «تْ» آخرَ لفظها: ٠٫٢٧٠٢ — تطابقٌ إلى أربع منازل",
        "شطرُ الشدّة لا يكون آخرَ لفظه: صفرٌ من ٨١٧ ومن ٣٬٢٤٤",
        "السقفُ الأعلى: ٠٫٤٥٥٠ لـ«تْ» و٠٫٦٥٦٤ لـ«مْ»",
        "نسبةُ «مْ» بلا المشدَّد: ٠٫٨٧٨٦",
    ),
    withheld_scope=(
        "الخاناتُ الـ١٬٦٨٠ وتصنيفُها — لا سجلَّ لها في هذه الشجرة",
        "الـ٨٢٤ خانةً التي ملأها الجدولُ الموقَّع — غيرُ محقَّقةٍ ههنا",
        "الاقتباساتُ الخمسةَ عشرَ ومطابقتُها — لا كتابَ ههنا",
        "ترتيبُ الختم قبل التشغيل في ذاك الفرع — يُقرَأ من تاريخه",
        "الرقمُ ٠٫٥٦٧٢ — وصوابُه عندي ٠٫٥٩٣٨، وكلاهما تشخيصٌ بعد النظر",
    ),
)


def record_bytes(record: SealedProxy = FROZEN_PROXY) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedProxy = FROZEN_PROXY) -> str:
    """بصمةُ سجلّ التوقيع مُشتَقّةً من حقوله."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ توقيع الوكالة؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: SealedProxy = FROZEN_PROXY) -> list[str]:
    """أَيحمل الإيداعُ إفصاحَ الوكالة ونطاقَها؟ **وما نقص يُسمّى**."""

    complaints: list[str] = []
    for name in (ANALYSIS, WITNESS):
        if not (DEPOSITS / name).is_file():
            complaints.append(f"إيداعٌ غائب: {name}")
    if complaints:
        return complaints
    text = (DEPOSITS / ANALYSIS).read_text(encoding="utf-8")
    flat = " ".join(text.split())
    for row in (
        record.signer,
        record.executed_by,
        record.authority_dated,
        "**وهذا توقيعُ وكالةٍ لا توقيعُ أصيل**",
        "**واليدُ يدُ الآلة**",
        "كي لا يُقرَأ كأنّه بخطّ صاحبه",
    ):
        if row not in flat:
            complaints.append(f"إفصاحُ الوكالة ناقصٌ: {row[:36]}")
    for one in record.withheld_scope:
        head = one.split("—")[0].strip()
        if head not in flat:
            complaints.append(f"مستثنًى غيرُ مذكورٍ في الإيداع: {head[:30]}")
    return complaints
