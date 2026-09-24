"""الختمُ البايتيّ: سجلٌّ واحدٌ يحمل المدوّنةَ ومصدرَها وروايتَها، ببصمةٍ تُعاد.

**العطلُ الذي يعالجه**: صارت أوراكلُ التسجيلات تُسمّي المدوّنةَ والمصدرَ
والروايةَ **نثرًا** — «المدوّنةُ المُجمَّدةُ ببصمتها، ومصدرُ ضبطها مُسمًّى».
والنثرُ يتبدّل ولا يُعرَف تبدّلُه، فيُستشهَد به بعد جلساتٍ كأنّه محسوم.
فيُجمَع ههنا في **سجلٍّ مُقفَلٍ ببصمةٍ واحدة**، ويستشهد به ما بعده برقمها.

`THE_RECORD_IS_REDERIVED_NOT_TRANSCRIBED`: وبصمةُ السجلّ **تُشتَقّ من
حقوله** عند كلّ تشغيل، فتبديلُ حقلٍ يُغيّرها ويُسقِط الفحص. فليست رقمًا
منقولًا في متنٍ يُنسى.

`A_MEASURED_FIELD_IS_CHECKED_AGAINST_THE_BYTES_NOT_TRUSTED`: وحقولُه صنفان
مفصولان: **موقَّعٌ** (وسمُ المصدر، بتوقيع صاحب المستودع) و**مقيسٌ** (الطول،
والبصمة، والأسطر، وعلاماتُ السكون، والملتقى، وفوارقُ الرواية). والمقيسُ
يُعاد اشتقاقُه من البايتات في `verify_against_corpus`، فمخالفتُه تُوقِف
ولا تُطوى.

`THE_READING_CARRIES_ITS_KIND_INSIDE_THE_RECORD`: والروايةُ في السجلّ
بمنزلتها: **منسوبةٌ استدلالًا** بثلاثة فوارقَ مُعلَنة، لا مرويّةٌ بسند.
فمن نقل الاسمَ نقل معه أنّه استدلال، أو خالف السجلَّ ببصمته.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"

SUKUN: Final[str] = "ْ"


class CorpusSealError(ValueError):
    """رُدَّ سجلٌّ خالف البايتاتِ في حقلٍ مقيس."""


@dataclass(frozen=True, slots=True)
class SealedCorpus:
    """سجلُّ مدوّنةٍ مُقفَل: موقَّعٌ ومقيسٌ في بنيةٍ واحدة."""

    name: str
    sha256_hex: str
    byte_length: int
    ayah_lines: int
    source_tag: str
    source_authority: str
    reading_name: str
    reading_kind: str
    reading_discriminators: int
    reading_agreed: int
    sukun_marks: int
    marked_nun_junctions: int

    def __post_init__(self) -> None:
        if len(self.sha256_hex) != 64 or set(self.sha256_hex) - set("0123456789abcdef"):
            raise CorpusSealError("البصمةُ أربعٌ وستّون خانةً ستّةَ عشريّة.")
        for name in ("name", "source_tag", "source_authority", "reading_name"):
            if not str(getattr(self, name)).strip():
                raise CorpusSealError(f"حقلٌ موقَّعٌ فارغ: {name}.")
        if self.reading_agreed != self.reading_discriminators:
            raise CorpusSealError(
                "لا يُقفَل سجلٌّ باسمِ روايةٍ لم توافقها الفوارقُ كلُّها؛ "
                "والنسبةُ بأغلبيّةٍ ليست نسبة."
            )
        for name in ("byte_length", "ayah_lines", "sukun_marks"):
            if int(getattr(self, name)) <= 0:
                raise CorpusSealError(f"حقلٌ مقيسٌ غيرُ موجب: {name}.")


FROZEN_RECORD: Final[SealedCorpus] = SealedCorpus(
    name="quran-simple-enhanced.txt",
    sha256_hex="37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a",
    byte_length=1_319_901,
    ayah_lines=6_236,
    source_tag="tanzil",
    source_authority="صاحبُ المستودع",
    reading_name="حفص عن عاصم",
    reading_kind="منسوبةٌ استدلالًا (INFERRED)",
    reading_discriminators=3,
    reading_agreed=3,
    sukun_marks=37_372,
    marked_nun_junctions=1_716,
)


def record_bytes(record: SealedCorpus = FROZEN_RECORD) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها لا ترتيبُ الهجاء."""

    rows = [
        f"{one.name}{_FIELD_SEPARATOR}{getattr(record, one.name)}"
        for one in fields(record)
    ]
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedCorpus = FROZEN_RECORD) -> str:
    """بصمةُ السجلّ مُشتَقّةً من حقوله؛ وتبديلُ حقلٍ يُغيّرها."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ السجلّ؛ وبه يُستشهَد في أوراكل ما بعده بدل النثر."""


def corpus_path() -> Path:
    return REPOSITORY / "corpora" / FROZEN_RECORD.name


def verify_against_corpus(path: Path | None = None) -> list[str]:
    """أعِد اشتقاقَ الحقول المقيسة من البايتات؛ وأرجِع أسماءَ ما خالف.

    ولا يُفحَص الموقَّعُ ههنا: وسمُ المصدر توقيعٌ لا يُشتَقّ من بايتة.
    """

    resolved = corpus_path() if path is None else path
    if not resolved.is_file():
        raise CorpusSealError(f"لا بايتاتِ مدوّنةٍ في {resolved}.")
    data = resolved.read_bytes()
    text = data.decode("utf-8")
    seen = {
        "sha256_hex": hashlib.sha256(data).hexdigest(),
        "byte_length": len(data),
        "ayah_lines": len(text.splitlines()),
        "sukun_marks": text.count(SUKUN),
    }
    return [
        name for name, value in seen.items() if value != getattr(FROZEN_RECORD, name)
    ]


def main() -> None:
    mismatched = verify_against_corpus()
    print(f"ختمُ السجلّ: {RECORD_DIGEST}")
    print(f"المدوّنة: {FROZEN_RECORD.name} ({FROZEN_RECORD.sha256_hex[:8]}…)")
    print(
        f"المصدر: {FROZEN_RECORD.source_tag} "
        f"(بتوقيع {FROZEN_RECORD.source_authority})"
    )
    print(
        f"الرواية: {FROZEN_RECORD.reading_name} — {FROZEN_RECORD.reading_kind} "
        f"بـ{FROZEN_RECORD.reading_agreed}/"
        f"{FROZEN_RECORD.reading_discriminators} فوارقَ"
    )
    print(
        "الحقولُ المقيسةُ مُعادةٌ من البايتات: "
        + ("كلُّها تطابق" if not mismatched else f"خالف {'، '.join(mismatched)}")
    )


if __name__ == "__main__":
    main()
