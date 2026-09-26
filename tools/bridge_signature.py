"""توقيعُ الجسر: **فعلُ صاحب المستودع**، مُسجَّلًا ومربوطًا بما وُقِّع عليه.

`THE_MACHINE_MAY_SIGN_ONLY_BY_A_RECORDED_DELEGATION`: المادّةُ ٢٧ من
`docs/دستور-القياس.md` تقول: **التوقيعُ فعلُ صاحب المستودع لا فعلُ
الآلة**. **ولصاحب المستودع أن يُفوِّض** — فالمادّةُ تُسمّي صاحبَ الحقّ لا
تمنع توكيلَه. فتوقيعُ الآلة **مردودٌ إلّا بتفويضٍ مُسجَّلٍ يُسمّي
المُفوِّضَ وتاريخَه**.

`AND_A_DELEGATED_SIGNATURE_MUST_DISCLOSE_THAT_IT_IS_SELF_CERTIFICATION`:
**والتفويضُ لا يُزيل الدور**. صاغت الآلةُ القراءاتَ، فتوقيعُها عليها
**تصديقُ المؤلِّف على ما ألَّف** — وذلك لا يُكتَم بل **يُسجَّل في
التوقيع**: يُذكَر الصائغُ والمُوقِّعُ، فإن كانا واحدًا **لزِم التصريحُ
بذلك**، ويردُّ البناءُ توقيعًا آليًّا يُخفيه. **فالقارئُ يُنزِله منزلتَه،
ولا يُقرَأ تصديقًا مستقلًّا.**

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
TABLES: Final[str] = "bridge_tables.md"
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
    drafter: str
    delegated_by: str
    delegation_dated: str
    readings: str
    families: int
    adopts_as: str
    licenses: tuple[str, ...]
    withheld: tuple[str, ...]
    tables: str

    def __post_init__(self) -> None:
        if len(self.readings) != 64 or set(self.readings) - set(_HEX):
            raise BridgeSignatureError(f"بصمةٌ ليست sha256: {self.readings}")
        if not self.signer.strip():
            raise BridgeSignatureError("توقيعٌ بلا مُوقِّع.")
        machine = any(one in self.signer for one in _MACHINES)
        if machine:
            if not self.delegated_by.strip():
                raise BridgeSignatureError("توقيعٌ آليٌّ بلا تفويضٍ مُسجَّل — المادّة ٢٧.")
            if any(one in self.delegated_by for one in _MACHINES):
                raise BridgeSignatureError("المُفوِّضُ إنسانٌ لا آلة.")
            if not self.delegation_dated.strip():
                raise BridgeSignatureError("تفويضٌ بلا تاريخ.")
            if self.drafter != self.signer:
                raise BridgeSignatureError(
                    "توقيعٌ آليٌّ يُسنِد الصياغةَ إلى غيره — والصائغُ ههنا "
                    "هو المُوقِّع، فلا يُخفى."
                )
            if "تصديقُ المؤلِّف" not in self.adopts_as:
                raise BridgeSignatureError(
                    "توقيعٌ آليٌّ لا يُصرِّح أنّه تصديقُ المؤلِّف على ما ألَّف."
                )
        elif self.drafter == self.signer:
            raise BridgeSignatureError(
                "مُوقِّعٌ بشريٌّ يُسنِد الصياغةَ إلى نفسه — والصائغُ الآلة."
            )
        if self.families <= 0:
            raise BridgeSignatureError("توقيعٌ على صفرِ قراءة.")
        if len(set(self.licenses)) != len(self.licenses):
            raise BridgeSignatureError("عائلةٌ مُرخَّصةٌ مرّتين.")
        if len(self.licenses) > self.families:
            raise BridgeSignatureError("ترخيصٌ لأكثرَ من العائلات.")
        if self.licenses and not self.tables.strip():
            raise BridgeSignatureError(
                "ترخيصٌ بلا جدولٍ مُودَع — والترخيصُ لا يقوم إلّا على جدول."
            )
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
    signer="آلةُ القياس",
    capacity="وكيلٌ بتفويضٍ، لا أصيلٌ — والأصلُ صاحبُ المستودع",
    dated="٢٠٢٦-٠٩-٢٦",
    drafter="آلةُ القياس",
    delegated_by="صاحبُ المستودع — Saleh1967",
    delegation_dated="٢٠٢٦-٠٩-٢٦",
    readings="20941c33e8a3396e5b24fdb8935230f7609b2e04124e674dc763b020615916f5",
    families=4,
    adopts_as=(
        "تبنٍّ للقراءات الأربع **فرضًا معلَنًا قابلًا للسقوط** — لا حقيقةً "
        "مبرهَنة، ولا ترخيصًا لجدولٍ لم يُودَع. **وهو تصديقُ المؤلِّف على "
        "ما ألَّف**: الصائغُ هو المُوقِّع، فلا يُقرَأ شهادةً مستقلّة"
    ),
    licenses=(
        "آخرُ السطر",
        "حالُ السابق",
        "حالُ ما قبله",
        "حرفُ خاتمةِ السابق",
    ),
    tables=TABLES,
    withheld=(
        "«آخرُ السطر»: المُودَعُ حدُّ السطر لا حكمُ الوقف — ولا فهرسَ وقوفٍ",
        "«حالُ السابق»: العلامةُ الواحدةُ تحمل حكمين — والجدولُ يُعلِن ذلك استثناءً",
        "«حالُ ما قبله»: لا حدَّ صدرٍ مُودَعٌ غيرَ حدّ السطر",
        "«حرفُ خاتمةِ السابق»: الرسمُ لا يُنبئ عن البنية — والجدولُ يُعلِن ذلك",
        "وما لزِم عن الجداول **لم يُقَس بعد** — دَينٌ مُعلَنٌ لا نتيجة",
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
    for row in (
        record.signer,
        record.dated,
        record.readings,
        record.delegated_by,
        record.delegation_dated,
    ):
        if row not in text:
            complaints.append(f"لا شاهدَ في الإيداع لـ«{row}»")
    for one in record.withheld:
        if one not in text:
            complaints.append(f"ما لا يُرخَّص غيرُ مذكورٍ في الإيداع: {one[:30]}")
    if record.licenses:
        tables = DEPOSITS / record.tables
        if not tables.is_file():
            complaints.append(f"جدولُ الترخيص غائب: {record.tables}")
        else:
            rows = tables.read_text(encoding="utf-8")
            for one in record.licenses:
                if one not in families:
                    complaints.append(f"ترخيصٌ لعائلةٍ غيرِ موجودة: {one}")
            for row in ("جدولُ الأبواب", "جدولُ الصرف", "حدُّ الآية"):
                if row not in rows:
                    complaints.append(f"جدولٌ ناقصٌ في الإيداع: {row}")
            if "فرضٌ إسناديٌّ أوّليٌّ" not in rows:
                complaints.append("الجدولُ لا يُصرِّح أنّه فرضٌ لا نقل")
    for name in families:
        if f"«{name}»" not in text:
            complaints.append(f"عائلةٌ بلا ذكرٍ في الإيداع: {name}")
    if record.drafter == record.signer:
        for row in (
            "**الصائغُ هو المُوقِّع**",
            "تصديقُ المؤلِّف على ما ألَّف",
            "ولا يُقرَأ شهادةً مستقلّة",
        ):
            if row not in text:
                complaints.append(f"إفصاحُ الدور ناقصٌ في الإيداع: {row}")
    return complaints
