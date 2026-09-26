"""توقيعُ الجسر: **فعلُ صاحب المستودع**، مُسجَّلًا ومربوطًا بما وُقِّع عليه.

`THE_MACHINE_RECORDS_A_SIGNATURE_AND_NEVER_IS_ONE`: المادّةُ ٢٧ من
`docs/دستور-القياس.md` تقول: **التوقيعُ فعلُ صاحب المستودع لا فعلُ
الآلة**. فالآلةُ ههنا **كاتبُ عدلٍ لا شاهد**: تُسجّل مَن وقَّع، وعلى ماذا
وقَّع بعينه، ومتى — **وتردُّ أن يكون المُوقِّعُ آلةً**.

`AND_A_SIGNATURE_IS_NOT_A_PROOF_BUT_A_LIABILITY`: **والتوقيعُ لا يجعل
القراءةَ مبرهَنة** — يجعلها **فرضًا معلَنًا قابلًا للسقوط**. وهذا هو
نفعُه: قراءةٌ بلا توقيعٍ لا تُكذَّب لأنّ صاحبَها لم يقلها، **وقراءةٌ
موقَّعةٌ تُكذَّب**. فالتوقيعُ **يُدخِل القراءةَ في دائرة النقض**، ولا
يُخرِجها منها.

`AND_THE_BINDING_IS_TO_THE_READINGS_NOT_TO_THE_WHOLE_PAPER`: وتُربَط
البصمةُ بـ**القراءات الأربع وحدَها**، لا بوثيقة الجسر كلِّها. فالوثيقةُ
تحمل مقاديرَ تنمو بكلّ تشغيلٍ جديد، **ولو رُبِط التوقيعُ بها لانكسر عند
كلّ قياس** — فيصير كسرُه عادةً فلا يُقرَأ. **وأمّا القراءةُ فإن بُدِّل
حرفٌ منها انكسر التوقيعُ**، وذلك المقصود.

`AND_WHAT_THE_SIGNATURE_DOES_NOT_COVER_IS_NAMED_IN_IT`: ولا تُرخَّص
بالتوقيع **جداولُ لم تُودَع**. فكلُّ عائلةٍ في الجسر تُعلِن ما يُلزَمها
(فهرسُ آياتٍ، جدولُ أبواب، جدولُ صرف) **وليس في المستودع واحدٌ منها**.
فالتوقيعُ **تبنٍّ للقراءة فرضًا**، لا إيداعٌ للجدول ولا برهانٌ عليه —
ويُكتَب ذلك في السجلّ بنصّه كي لا يُقرَأ ترخيصًا.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
SIGNED: Final[str] = "bridge_signature.md"
BRIDGE: Final[Path] = REPOSITORY / "docs" / "جسر-البتّات.md"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_HEX: Final[str] = "0123456789abcdef"
_MACHINES: Final[tuple[str, ...]] = ("الآلة", "Claude", "claude", "آلة", "المولّد")


class BridgeSignatureError(ValueError):
    """رُدَّ توقيعٌ لا يحمل شكلَه، أو ادّعى ترخيصًا لم يُودَع له جدول."""


@dataclass(frozen=True, slots=True)
class SealedSignature:
    """توقيعٌ مُقفَل: مَن، وعلى ماذا، وما لا يُرخِّصه."""

    signer: str
    capacity: str
    dated: str
    readings: str
    families: int
    adopts_as: str
    licenses: tuple[str, ...]
    withheld: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.readings) != 64 or set(self.readings) - set(_HEX):
            raise BridgeSignatureError(f"بصمةٌ ليست sha256: {self.readings}")
        if not self.signer.strip():
            raise BridgeSignatureError("توقيعٌ بلا مُوقِّع.")
        for one in _MACHINES:
            if one in self.signer:
                raise BridgeSignatureError(
                    "الآلةُ لا تُوقِّع — المادّة ٢٧: التوقيعُ فعلُ صاحب المستودع."
                )
        if self.families <= 0:
            raise BridgeSignatureError("توقيعٌ على صفرِ قراءة.")
        if self.licenses:
            raise BridgeSignatureError("توقيعٌ يدّعي ترخيصًا: ولا جدولَ مُودَعٌ يُرخِّص شيئًا.")
        if len(self.withheld) < self.families:
            raise BridgeSignatureError("ما لا يُرخِّصه التوقيعُ يُسمّى لكلّ عائلةٍ — ولا يُطوى.")
        if "فرض" not in self.adopts_as:
            raise BridgeSignatureError("التوقيعُ تبنٍّ **فرضًا**، ويُقال كذلك.")


def _bridge() -> Any:
    path = REPOSITORY / "tools" / "write_bit_bridge.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise BridgeSignatureError("لا قارئَ لمولّد الجسر")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def readings_bytes(
    families: dict[str, tuple[str, str, str]] | None = None,
) -> bytes:
    """تسلسلٌ قانونيٌّ للقراءات — وهو ما يُوقَّع عليه لا غيرُه.

    **والقراءاتُ تُمرَّر أو تُقرَأ**: تُقرَأ من المولّد في العمل، وتُمرَّر
    في الفحص. **وبلا تمريرٍ لا يُمكِن أن يُفحَص الكسرُ** — فيبقى الربطُ
    دعوًى لا بوّابة.
    """

    rows = [
        _FIELD_SEPARATOR.join((name, reading, kind, needed))
        for name, (reading, kind, needed) in (
            families if families is not None else _bridge().FAMILIES
        ).items()
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_readings_digest(
    families: dict[str, tuple[str, str, str]] | None = None,
) -> str:
    """بصمةُ القراءات **الآن** — وتبديلُ حرفٍ فيها يكسر التوقيع."""

    return hashlib.sha256(readings_bytes(families)).hexdigest()


FROZEN_SIGNATURE: Final[SealedSignature] = SealedSignature(
    signer="صاحبُ المستودع — Saleh1967",
    capacity="مالكُ الشجرة، وإليه التوقيعُ بمقتضى المادّة ٢٧",
    dated="٢٠٢٦-٠٩-٢٦",
    readings="20941c33e8a3396e5b24fdb8935230f7609b2e04124e674dc763b020615916f5",
    families=4,
    adopts_as=(
        "تبنٍّ للقراءات الأربع **فرضًا معلَنًا قابلًا للسقوط** — لا حقيقةً "
        "مبرهَنة، ولا ترخيصًا لجدولٍ لم يُودَع"
    ),
    licenses=(),
    withheld=(
        "«آخرُ السطر»: لا فهرسَ آياتٍ مُودَعٌ، فكونُ حدِّ السطر موضعَ وقفٍ غيرُ مُرخَّص",
        "«حالُ السابق»: لا جدولَ أبوابٍ مُودَعٌ، فقراءةُ العلامة حكمًا غيرُ مُرخَّصة",
        "«حالُ ما قبله»: لا جدولَ أبوابٍ ولا حدَّ صدرٍ مُودَعٌ",
        "«حرفُ خاتمةِ السابق»: لا جدولَ صرفٍ مُودَعٌ، فقراءةُ الحرف بنيةً غيرُ مُرخَّصة",
    ),
)


def record_bytes(record: SealedSignature = FROZEN_SIGNATURE) -> bytes:
    """تسلسلٌ قانونيٌّ لحقول التوقيع؛ وترتيبُها ترتيبُ تعريفها."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedSignature = FROZEN_SIGNATURE) -> str:
    """بصمةُ سجلّ التوقيع مُشتَقّةً من حقوله."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ سجلّ التوقيع؛ وبه يُستشهَد بدل النثر."""


def verify_against_logs(record: SealedSignature = FROZEN_SIGNATURE) -> list[str]:
    """أَتوافقُ القراءاتُ ما وُقِّع عليه؟ **وما خالف يُسمّى ولا يُصلَح صمتًا**."""

    complaints: list[str] = []
    found = rederive_readings_digest()
    if found != record.readings:
        complaints.append(
            f"القراءاتُ بُدِّلت بعد التوقيع: بصمتُها {found[:16]}"
            f" والموقَّعُ عليه {record.readings[:16]}"
        )
    families = _bridge().FAMILIES
    if len(families) != record.families:
        complaints.append(f"العائلاتُ {len(families)} والموقَّعُ عليه {record.families}")
    deposit = DEPOSITS / SIGNED
    if not deposit.is_file():
        complaints.append(f"إيداعُ التوقيع غائب: {SIGNED}")
        return complaints
    text = deposit.read_text(encoding="utf-8")
    for row in (record.signer, record.dated, record.readings):
        if row not in text:
            complaints.append(f"لا شاهدَ في الإيداع لـ«{row}»")
    for one in record.withheld:
        if one not in text:
            complaints.append(f"ما لا يُرخَّص غيرُ مذكورٍ في الإيداع: {one[:30]}")
    for name in families:
        if f"«{name}»" not in text:
            complaints.append(f"عائلةٌ بلا ذكرٍ في الإيداع: {name}")
    return complaints
