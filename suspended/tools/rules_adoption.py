"""اعتمادُ القاعدتين المُودَعتين — **وكالةً، وفرضًا لا برهانًا**.

`THE_TWO_RULES_WERE_DEPOSITED_UNSIGNED_AND_THAT_WAS_A_NAMED_DEBT`: أُودِعت
`separation_rule.md` (صاغتها الآلةُ مواصفةً) و`praise_blame_rule.md`
(أودعها صاحبُ المستودع نقلًا عن مقالٍ خارجيّ) **غيرَ موقَّعتين**، فكانتا
تُقاسان ولا يُبنى عليهما. **وذلك دَينٌ مُعلَنٌ**، وههنا يُسدّ بالوكالة
المُسجَّلة.

`AND_THE_DOCUMENTS_THEMSELVES_ARE_NOT_EDITED_BECAUSE_A_SEALED_LOG_READS
_THEM`: **ولم تُحرَّر الوثيقتان بحرف.** فـ`run_separation_rule.py` يقرأ
سطرَ التوقيع في `separation_rule.md` ويطبع `غيرُ موقَّعة: True` **في سجلٍّ
مُودَعٍ مُبصَّمٍ يُقابَل بايتةً ببايتة**. فلو حُرِّر السطرُ لانقلب المطبوعُ
وانكسر السجلُّ وبصمتُه وتدقيقُ الإعادة — **فتحريرُ مُدخَلٍ لسجلٍّ مُقفَلٍ
تعديلٌ للسجلّ بطريقٍ خفيّ**.

**والقاعدةُ المستخرَجة**: **مُدخَلُ سجلٍّ مُقفَلٍ مُقفَلٌ مثلُه.** فالاعتمادُ
يُودَع **وثيقةً ثانيةً** تُبصِم الأولى ولا تمسّها، وبصمتا الوثيقتين في هذا
السجلّ: فإن بُدِّل حرفٌ منهما **انكسر الاعتماد** — وذلك المقصود.

`AND_AN_ADOPTION_IS_NOT_A_PROMOTION`: **ولا يُرقّي الاعتمادُ مستوًى.** حالُ
«الكلمة المفردة» `UNCLASSIFIED` في `tools/ladder_seal.py` — **سجلٌّ مُقفَلٌ
لا يُعدَّل بعد الحدث**. فالاعتمادُ يرفع المانعَ **القانونيَّ** عن الترقية
ولا يُرقّي؛ **والترقيةُ قياسٌ يحتاج ختمًا جديدًا يُدفَع قبل تشغيله**.

`AND_WHAT_IS_ADOPTED_IS_THE_HYPOTHESIS_NOT_THE_READING`: وتُعتمَد الأولى
**فرضًا يُقاس** والثانيةُ **مُدخَلًا يُختبَر** — ولا يُعتمَد في واحدةٍ
منهما **حكمٌ نحويّ**. فالبتّاتُ لا ترى رفعًا ولا فاعلًا، وما لا تراه
**لا يُوقَّع عليه**.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DEPOSITS: Final[Path] = REPOSITORY / "deposits"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_HEX: Final[str] = "0123456789abcdef"
_MACHINES: Final[tuple[str, ...]] = ("آلة", "الآلة", "Claude", "claude", "المولّد")
_PROOF_WORDS: Final[tuple[str, ...]] = ("مبرهَن", "برهان")
"""ما لا يقوله نافٍ: **والفحصُ أعمى عن النفي**، فلا يُوسَّع.

جرّبتُ فيه «صحيح» فردَّ `«فرضًا يُقاس — لا وصفًا صحيحًا للتقطيع»` — **وهو
نفيٌ لا دعوى**. فحُصِر في كلمتين **لا تردان في نفي**، ويُقال إنّ الفحصَ
يردُّ اللفظَ لا المعنى.
"""


class RuleAdoptionError(ValueError):
    """رُدَّ اعتمادٌ يُخفي وكالتَه، أو يدّعي برهانًا، أو بلا مستثنيات."""


@dataclass(frozen=True, slots=True)
class SealedRule:
    """اعتمادُ وثيقةٍ مُقفَل: ماذا، وببصمةِ ماذا، وبأيّ صفةٍ، وما لا يُعتمَد."""

    document: str
    digest: str
    drafted_by: str
    origin: str
    adopts_as: str
    adopted: tuple[str, ...]
    withheld: tuple[str, ...]
    measured_by: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.digest) != 64 or set(self.digest) - set(_HEX):
            raise RuleAdoptionError(f"بصمةٌ ليست sha256: {self.digest}")
        if not (DEPOSITS / self.document).is_file():
            raise RuleAdoptionError(f"وثيقةٌ غائبة: {self.document}")
        if not self.origin.strip() or not self.drafted_by.strip():
            raise RuleAdoptionError("اعتمادٌ لا يُسمّي صائغَ الوثيقة ولا مصدرَها.")
        if not any(one in self.adopts_as for one in ("فرضًا", "مُدخَلًا")):
            raise RuleAdoptionError("صفةُ الاعتماد ليست فرضًا ولا مُدخَلًا — فتُقرَأ حكمًا.")
        if any(one in self.adopts_as for one in _PROOF_WORDS):
            raise RuleAdoptionError("اعتمادٌ يدّعي برهانًا — والاعتمادُ لا يُبرهن.")
        if not self.adopted:
            raise RuleAdoptionError("اعتمادٌ لا يُسمّي ما اعتُمِد.")
        if not self.withheld:
            raise RuleAdoptionError("اعتمادٌ بلا مستثنياتٍ يُقرَأ تصديقًا على الكلّ.")
        if not self.measured_by:
            raise RuleAdoptionError("اعتمادٌ بلا سجلٍّ قاس لوازمَه.")
        for one in self.measured_by:
            if not (DEPOSITS / one).is_file():
                raise RuleAdoptionError(f"سجلٌّ غائب: {one}")
        for one in self.adopted + self.withheld:
            if len(one.strip()) < 30:
                raise RuleAdoptionError(f"بندٌ أقصرُ من أن يُفحَص: {one}")

    def matches_its_document(self) -> bool:
        """أَبصمةُ الوثيقة اليومَ هي المُقفَلة؟ — **فإن بُدِّلت انكسر**."""

        data = (DEPOSITS / self.document).read_bytes()
        return hashlib.sha256(data).hexdigest() == self.digest


@dataclass(frozen=True, slots=True)
class SealedAdoption:
    """مَن اعتمد، وبأيّ سندٍ، وعلى أيّ وثائق."""

    signer: str
    executed_by: str
    authority: str
    authority_dated: str
    rules: tuple[SealedRule, ...]
    promotes: str

    def __post_init__(self) -> None:
        if not self.signer.strip():
            raise RuleAdoptionError("اعتمادٌ بلا اسم.")
        if any(one in self.signer for one in _MACHINES):
            raise RuleAdoptionError("الآلةُ تكون يدًا ولا تكون اسمًا — المادّة ٢٧.")
        if self.executed_by != self.signer:
            if not any(one in self.executed_by for one in _MACHINES):
                raise RuleAdoptionError("مُنفِّذٌ غيرُ الأصيل ولا هو آلةٌ مُسمّاة.")
            if not self.authority.strip() or self.signer not in self.authority:
                raise RuleAdoptionError("وكالةٌ بلا سندٍ يُسمّي صاحبَ الاسم.")
            if not self.authority_dated.strip():
                raise RuleAdoptionError("سندُ وكالةٍ بلا تاريخ.")
        if not self.rules:
            raise RuleAdoptionError("اعتمادٌ بلا وثيقة.")
        if "لا يُرقّي" not in self.promotes:
            raise RuleAdoptionError("اعتمادٌ لا يُعلِن أنّه لا يُرقّي مستوًى.")


SEPARATION: Final[SealedRule] = SealedRule(
    document="separation_rule.md",
    digest="d3ebd323907b83a8214e3c92299bca3e0d9d28733988cd6cb225319f33fa1215",
    drafted_by="آلةُ القياس — مسوَّدةً",
    origin="صياغةٌ في هذه الشجرة، لا نقلٌ من كتاب",
    adopts_as="فرضًا يُقاس — **لا وصفًا صحيحًا للتقطيع**",
    adopted=(
        "أنّها **مواصفةٌ لا دعوى**: تقول ما تفعله بالضبط — ثلاثُ رتبٍ من "
        "المقدّمات، ولواحقُ الأطولِ أوّلًا، وشرطُ وحدتين لا تقلّ عنهما "
        "البقيّة — فتُشغَّل كما كُتِبت ولا تُؤوَّل",
        "أنّها **فرضُ التقطيع العاملُ في هذه الشجرة**: فما قِيس بها يُنسَب "
        "إليها بالاسم، ويُقرَأ خبرًا عنها لا عن العربيّة",
        "أنّ **الحَكَمَ عليها الثمنُ المحجوز** لا جردٌ صحيح: إن لاقطت بنيةً "
        "نزل الثمنُ، وإن قطّعت بلا بنيةٍ لم ينزل — وذلك مقيسٌ ومُودَع",
        "أنّ **الرجعةَ شرطُ آلةٍ فيها**: فصلُ اللفظ ثمّ وصلُه يعيده وحدةً "
        "وحدة، ومفحوصٌ على المدوّنة كلِّها",
    ),
    withheld=(
        "**أنّها الفصلُ الصحيح** — لا جردَ صحيحًا في الشجرة تُقابَل به، "
        "**فدقّتُها غيرُ مقيسة**، ولا يُدَّعى أنّها تلتقط الملتصقَ وحدَه",
        "**ترقيةُ مستوى «الكلمة المفردة»** — حالُه `UNCLASSIFIED` في سجلٍّ "
        "مُقفَلٍ لا يُعدَّل، والترقيةُ **قياسٌ يحتاج ختمًا جديدًا**",
        "**كلُّ حكمٍ نحويٍّ** — لا إعرابَ ولا اشتقاقَ ولا معجم؛ والمواصفةُ "
        "تقشر ما يشبه الملتصقَ **وإن لم يكن**، وذلك مقصودٌ فيها",
    ),
    measured_by=("separation_rule_run.log", "basmala_lifted_run.log"),
)

PRAISE_BLAME: Final[SealedRule] = SealedRule(
    document="praise_blame_rule.md",
    digest="c0a77fc199bce0d35f119b029a7847083f045553f4edd3977c5ff283215561be",
    drafted_by="صاحبُ المستودع — نقلًا بنصّه",
    origin="مقالٌ خارجيّ: «الأساليب اللغوية في القرآن الكريم ودلالاتها وطرق استعمالاتها»",
    adopts_as="مُدخَلًا يُختبَر — **لا قراءةً نحويّةً مُعتمَدة**",
    adopted=(
        "أنّ الصورَ العشرين **منقولةٌ بنصّها** من المقال، ولكلٍّ موضعُ نقلٍ "
        "مُسمًّى في الجدول — فتُقرَأ من الجدول ولا تُكتَب في الشيفرة",
        "أنّ **اللوازمَ الأربعةَ في البايتات هي ما يُقاس**: اختلافُ حقل "
        "الحال، وانضغاطُ إنتروبيته، وغلبةُ علامةٍ، وذلك في الموضع الثالث",
        "أنّ **ما غاب من الصور يُصنَّف غيابُه ولا يُصفَّر**: يُطبَع بالاسم، "
        "ويُقال إنّه **ليس في هذا المجمَّد** لا إنّه ليس في العربيّة",
    ),
    withheld=(
        "**القراءةُ النحويّةُ نفسُها** — «فاعلٌ مرفوع» و«مخصوصٌ مرفوع»: "
        "**لا ترى البتّاتُ رفعًا ولا فاعلًا**، فلا يُوقَّع عليهما",
        "**الأعاريبُ الأربعةُ للمخصوص المتأخّر** — لا تفترق في البايتات "
        "ألبتّة: الحروفُ واحدةٌ والعلاماتُ واحدة، **فلا ترجّح بينها**",
        "**الشاهدان الشعريّان** (حبذا · لاحبذا) — شعرٌ لا آية، ولا يُقاسان "
        "على هذا المجمَّد ولا يُعَدّ غيابُهما خبرًا عنه",
        "**أنّ صمودَ لازمٍ تصديقٌ للقراءة** — صمودُ اللازم صمودُ لازمٍ، "
        "وسقوطُه سقوطُ لازمٍ بأرقامه، **ولا يُعاد تفسيرُه**",
    ),
    measured_by=("praise_blame_run.log",),
)

FROZEN_ADOPTION: Final[SealedAdoption] = SealedAdoption(
    signer="صاحبُ المستودع — Saleh1967",
    executed_by="آلةُ القياس",
    authority="تفويضٌ صريحٌ بالاعتماد والتوقيع باسمِه، من: صاحبُ المستودع — Saleh1967",
    authority_dated="٢٠٢٦-٠٩-٢٦",
    rules=(PRAISE_BLAME, SEPARATION),
    promotes=(
        "**لا يُرقّي مستوًى**: حالُ «الكلمة المفردة» يبقى `UNCLASSIFIED` في "
        "السجلّ المُقفَل، والترقيةُ تحتاج ختمًا جديدًا يُدفَع قبل تشغيله"
    ),
)


def record_bytes(record: SealedAdoption = FROZEN_ADOPTION) -> bytes:
    """تسلسلٌ قانونيٌّ: حقولُ الاعتماد ثمّ حقولُ كلّ وثيقةٍ بترتيب تعريفها."""

    rows: list[str] = []
    for one in fields(record):
        value = getattr(record, one.name)
        if one.name == "rules":
            for rule in value:
                for two in fields(rule):
                    inner = getattr(rule, two.name)
                    flat = (
                        _RECORD_SEPARATOR.join(inner)
                        if isinstance(inner, tuple)
                        else str(inner)
                    )
                    rows.append(f"{rule.document}.{two.name}{_FIELD_SEPARATOR}{flat}")
            continue
        rows.append(f"{one.name}{_FIELD_SEPARATOR}{value}")
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedAdoption = FROZEN_ADOPTION) -> str:
    """بصمةُ الاعتماد مُشتَقّةً من حقوله."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ اعتماد القاعدتين؛ وبه يُستشهَد بدل النثر."""


def verify_against_documents(record: SealedAdoption = FROZEN_ADOPTION) -> list[str]:
    """أَبصمةُ كلّ وثيقةٍ كما قُفِلت؟ **وما بُدِّل يُسمّى بموضعه**."""

    complaints: list[str] = []
    for rule in record.rules:
        if not rule.matches_its_document():
            data = (DEPOSITS / rule.document).read_bytes()
            now = hashlib.sha256(data).hexdigest()
            complaints.append(
                f"{rule.document}: قُفِلت على {rule.digest[:8]} وهي اليوم {now[:8]}"
            )
    return complaints


def main() -> int:
    print(f"ختمُ الاعتماد: {RECORD_DIGEST}")
    print(f"الاسم: {FROZEN_ADOPTION.signer}")
    print(f"اليد: {FROZEN_ADOPTION.executed_by} — {FROZEN_ADOPTION.authority_dated}")
    for rule in FROZEN_ADOPTION.rules:
        print(
            f"  {rule.document} ({rule.digest[:8]}…): "
            f"{len(rule.adopted)} معتمَدًا | {len(rule.withheld)} مستثنًى"
        )
    complaints = verify_against_documents()
    for one in complaints:
        print(f"  ✗ {one}")
    if complaints:
        return 1
    print("والوثيقتان كما قُفِلتا — ولم تُحرَّر واحدةٌ منهما بحرف.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
