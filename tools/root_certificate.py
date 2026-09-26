"""اعتمادُ جذرِ المشروع: **ما تحمله الشجرةُ فرضًا موقَّعًا، وما لا تحمله**.

`A_ROOT_IS_WHAT_A_STRANGER_READS_FIRST`: جذرُ الشجرة أوّلُ ما يُقرَأ، فهو
**أخطرُ موضعٍ يَبلى فيه رقمٌ صامتًا**. وكان `README.md` مكتوبًا بيدٍ لا
مولّدَ له ولا فحصَ يقابله — فكلُّ ما في الشجرة من موانعَ لا يبلغه.
**فيُشتَقّ من الشجرة ويُقابَل بمولّده**، كسائر الوثائق المولَّدة.

`AND_AN_ADOPTION_IS_NOT_A_PROOF_BUT_A_LIABILITY`: **والاعتمادُ لا يجعل ما
في الجذر مبرهَنًا** — يجعله **فرضًا معلَنًا قابلًا للسقوط**. وذاك نفعُه:
جذرٌ بلا اعتمادٍ لا يُكذَّب لأنّ أحدًا لم يتبنَّه، **وجذرٌ معتمَدٌ
يُكذَّب**. فالاعتمادُ يُدخِل الجذرَ في دائرة النقض ولا يُخرِجه منها.

`AND_THE_NAME_ON_AN_ADOPTION_IS_A_PERSON_NOT_A_MACHINE`: أذِن صاحبُ
المستودع بالتوقيع **باسمه**، والمادّةُ ٢٧ تُسمّي صاحبَ الحقّ ولا تمنع
توكيلَه. **فالآلةُ تكون يدًا ولا تكون اسمًا**؛ وشرطُ الوكالة أن **يُعلَم
أنّها وكالة**، فيردُّ البناءُ توقيعًا يُخفيها، ويُلزِم سندًا مُسمًّى
ومؤرَّخًا وسطرَ إفصاحٍ في الجذر نفسِه.

`AND_THE_DRAFTER_IS_THE_SIGNER_SO_IT_IS_SAID`: **وصائغُ الجذر هو اليدُ
الموقِّعة** — فهذا تصديقُ المؤلِّف على ما ألَّف، **ولا يُقرَأ شهادةً
مستقلّة**، ويُسجَّل في التوقيع لا يُكتَم.

`AND_THE_BINDING_IS_TO_THE_CLAIMS_NOT_TO_THE_WHOLE_ROOT`: وتُربَط البصمةُ
بـ**الدعاوى المعتمَدة والمستثنياتِ وحدَها**، لا بنصّ الجذر كلِّه. فالجذرُ
يحمل أعدادًا تنمو بكلّ تشغيل، **ولو رُبِط التوقيعُ بها لانكسر عند كلّ
قياسٍ** فيصير كسرُه عادةً فلا يُقرَأ. **وأمّا الدعوى فإن بُدِّل حرفٌ منها
انكسر التوقيع**، وذلك المقصود.

`AND_WHAT_IS_WITHHELD_IS_NAMED_OR_THE_SIGNATURE_COVERS_EVERYTHING`: ولا
يُقفَل اعتمادٌ بلا مستثنياتٍ مُسمّاة؛ فتوقيعٌ بلا استثناءٍ يُقرَأ تصديقًا
على كلّ ما في الشجرة، **وذلك أوسعُ ممّا حُقِّق**.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
ROOT: Final[str] = "README.md"

_FIELD_SEPARATOR: Final[str] = "\x1f"
_RECORD_SEPARATOR: Final[str] = "\x1e"
_MACHINES: Final[tuple[str, ...]] = ("آلة", "الآلة", "Claude", "claude", "المولّد")

DISCLOSURE: Final[tuple[str, ...]] = (
    "**وهذا اعتمادٌ بالوكالة لا باليد**",
    "**والاسمُ اسمُ صاحب المستودع، واليدُ يدُ الآلة**",
    "**والصائغُ هو الموقِّعُ نفسُه**",
    "**ولا يجعل الاعتمادُ ما في الجذر مبرهَنًا**",
)
"""أسطرُ الإفصاح؛ ويُفحَص وجودُ كلٍّ منها في الجذر بنصّه."""


class RootAdoptionError(ValueError):
    """رُدَّ اعتمادٌ يُخفي وكالتَه، أو بلا دعاوى، أو بلا مستثنيات."""


@dataclass(frozen=True, slots=True)
class SealedAdoption:
    """اعتمادٌ مُقفَل: الاسمُ، واليدُ، والسندُ، وما اعتُمِد وما استُثنِي."""

    signer: str
    executed_by: str
    authority: str
    authority_dated: str
    drafter: str
    root: str
    certifies: tuple[str, ...]
    withheld: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.signer.strip():
            raise RootAdoptionError("اعتمادٌ بلا اسم.")
        if any(one in self.signer for one in _MACHINES):
            raise RootAdoptionError("الآلةُ تكون يدًا ولا تكون اسمًا — المادّة ٢٧.")
        proxy = self.executed_by != self.signer
        if proxy:
            if not any(one in self.executed_by for one in _MACHINES):
                raise RootAdoptionError("مُنفِّذٌ غيرُ الأصيل ولا هو آلةٌ مُسمّاة.")
            if not self.authority.strip() or self.signer not in self.authority:
                raise RootAdoptionError("وكالةٌ بلا سندٍ يُسمّي صاحبَ الاسم.")
            if not self.authority_dated.strip():
                raise RootAdoptionError("سندُ وكالةٍ بلا تاريخ.")
            if self.drafter != self.executed_by:
                raise RootAdoptionError("الصائغُ غيرُ المُنفِّذ — يُسمّى ولا يُفترَض.")
        elif self.authority.strip():
            raise RootAdoptionError("أصيلٌ يحمل سندَ وكالةٍ — وذلك تلبيس.")
        if self.root != ROOT:
            raise RootAdoptionError(f"اعتمادُ غيرِ الجذر: {self.root}")
        if len(self.certifies) < 4:
            raise RootAdoptionError("اعتمادٌ بدعوًى أو دعوتين — والجذرُ أوسع.")
        if not self.withheld:
            raise RootAdoptionError("اعتمادٌ بلا مستثنياتٍ يُقرَأ تصديقًا على الكلّ.")
        for one in self.certifies + self.withheld:
            if len(one.strip()) < 30:
                raise RootAdoptionError(f"بندٌ أقصرُ من أن يُفحَص: {one}")


FROZEN_ADOPTION: Final[SealedAdoption] = SealedAdoption(
    signer="صاحبُ المستودع — Saleh1967",
    executed_by="آلةُ القياس",
    authority="تفويضٌ صريحٌ بالاعتماد والتوقيع باسمِه، من: صاحبُ المستودع — Saleh1967",
    authority_dated="٢٠٢٦-٠٩-٢٦",
    drafter="آلةُ القياس",
    root=ROOT,
    certifies=(
        "الشرطُ يُكتَب ويُدفَع قبل التشغيل، **وترتيبُه في تاريخ المستودع** "
        "لا في نثرِ أحد — فالتاريخُ هو الشاهد، ويُقرَأ من `git` لا منّا",
        "لا يُعاد تفسيرُ شرطٍ بعد رؤية رقمه؛ **والساقطُ يبقى ساقطًا** "
        "كما خُتِم، ولا يُقلَب إلّا بختمٍ جديدٍ يُدفَع قبل تشغيله",
        "ما لم يُقَس **يُقال إنّه لم يُقَس**، والخلوُّ **يُصنَّف ولا "
        "يُصفَّر**: `IMPOSSIBLE` و`UNATTESTED` و`UNREACHABLE` و`REFUSED` "
        "و`UNRUN` أبوابٌ مُسمّاةٌ لا صفرٌ مكتوم",
        "المقيسُ **بايتاتٌ مُجمَّدةٌ ببصمة** لا نصٌّ يُكتَب بيد؛ والحرفُ "
        "يُقتطَع من المدوّنة ولا يُطبَع — **فلا يدخل قياسًا حرفٌ كتبناه**",
        "كلُّ سجلٍّ مُودَعٍ **يُعاد تشغيلُه ويُقابَل بتًّا ببت**، "
        "و`tools/rerun_audit.py` يُعيد الخمسةَ والعشرين ويُبصِم المقابلة",
        "كلُّ شرطٍ نسبتُه محدودةٌ **يُصرَّح بسقفه قبل حدّه**، وحدٌّ فوق "
        "سقفه **خلوٌّ لا سقوط** — والمانعُ هـ) يردُّ الصمتَ عن السقف",
        "ولا دعوى في هذه الشجرة **على العربيّة** تُقرَأ مبرهَنة: تُقاس "
        "بايتاتٌ ووحداتٌ وألفاظٌ وأسطر، وما فوقها **يُصنَّف ولا يُخترَع**",
    ),
    withheld=(
        "**قراءةُ بتّةٍ لفظًا** — جسرُ البتّات فروضٌ موقَّعةٌ بوصفها فروضًا، "
        "ولا تُقرَأ برهانًا على معنًى نحويٍّ ولا صرفيّ",
        "**جدولا `bridge_tables.md`** — صاغتهما الآلةُ من معرفتها لا من "
        "كتابٍ مُودَعٍ في الشجرة، فيُقاس لازمُهما ولا يُعتمَد نصُّهما",
        "**`separation_rule.md` و`praise_blame_rule.md`** — مُودَعتان "
        "**غيرَ موقَّعتين**، ومضمونُهما تفسيرٌ لم يُعتمَد بعد",
        "**`src/alghanem`** — نقلٌ مغلقٌ مُبصَّمٌ من شجرةٍ أخرى، "
        "و`PORT_MANIFEST.json` يحرس تباعدَه؛ وليس من عمل هذه الشجرة",
        "**كلُّ رقمٍ نُقِل من أنبوبٍ خارجيّ** — يُعاد حسابُه حيث يسمح "
        "منشورُه، ويُحَدُّ بحدّين حيث لا يسمح، **ولا يُوقَّع تأويلُه**",
        "**المستوياتُ الأربعةُ فوق الوحدة** — الكلمةُ المفردة والتركيبان "
        "والجملة، `UNCLASSIFIED` بأسبابها؛ ولا يُسمّى السطرُ جملة",
        "**سقفُ ي٥** — ثمنُ هروبٍ وهجاءٍ لا يحدُّه الواحد، ولم يُشتَقّ؛ "
        "فهو الدَّينُ الواحدُ الباقي في سقوف الشروط",
    ),
)
"""اعتمادُ الجذر مُقفَلًا — ويُبدَّل بختمٍ جديدٍ لا بتحريرِ سطر."""


def record_bytes(record: SealedAdoption = FROZEN_ADOPTION) -> bytes:
    """تسلسلٌ قانونيٌّ للحقول؛ وترتيبُها ترتيبُ تعريفها."""

    rows: list[str] = []
    for one in fields(record):
        value = getattr(record, one.name)
        flat = _RECORD_SEPARATOR.join(value) if isinstance(value, tuple) else str(value)
        rows.append(f"{one.name}{_FIELD_SEPARATOR}{flat}")
    return _RECORD_SEPARATOR.join(rows).encode("utf-8")


def rederive_record_digest(record: SealedAdoption = FROZEN_ADOPTION) -> str:
    """بصمةُ الاعتماد مُشتَقّةً من حقوله، لا مكتوبةً."""

    return hashlib.sha256(record_bytes(record)).hexdigest()


RECORD_DIGEST: Final[str] = rederive_record_digest()
"""ختمُ الاعتماد؛ وبه يُستشهَد بدل النثر."""


def verify_against_root(record: SealedAdoption = FROZEN_ADOPTION) -> list[str]:
    """أَيحمل الجذرُ إفصاحَ الوكالة وكلَّ بندٍ اعتُمِد واستُثنِي؟

    **وما نقص يُسمّى** — ولا يُقال «مطابق» على غيابٍ لم يُفحَص.
    """

    complaints: list[str] = []
    path = REPOSITORY / record.root
    if not path.is_file():
        return [f"جذرٌ غائب: {record.root}"]
    flat = " ".join(path.read_text(encoding="utf-8").split())
    for row in (
        record.signer,
        record.executed_by,
        record.authority_dated,
        record.drafter,
        RECORD_DIGEST[:8],
        *DISCLOSURE,
    ):
        if " ".join(row.split()) not in flat:
            complaints.append(f"إفصاحٌ ناقصٌ في الجذر: {row[:40]}")
    for one in record.certifies:
        if " ".join(one.split()) not in flat:
            complaints.append(f"بندٌ معتمَدٌ غائبٌ عن الجذر: {one[:40]}")
    for one in record.withheld:
        if " ".join(one.split()) not in flat:
            complaints.append(f"مستثنًى غائبٌ عن الجذر: {one[:40]}")
    return complaints


def main() -> int:
    print(f"ختمُ الاعتماد: {RECORD_DIGEST}")
    print(f"الاسم: {FROZEN_ADOPTION.signer}")
    print(
        f"اليد: {FROZEN_ADOPTION.executed_by} — بسندٍ مؤرَّخٍ "
        f"{FROZEN_ADOPTION.authority_dated}"
    )
    print(f"معتمَدٌ: {len(FROZEN_ADOPTION.certifies)} بندًا")
    print(f"مستثنًى: {len(FROZEN_ADOPTION.withheld)} بندًا")
    complaints = verify_against_root()
    for one in complaints:
        print(f"  ✗ {one}")
    if complaints:
        return 1
    print("والجذرُ يحمل الإفصاحَ وكلَّ بندٍ — مطابق.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
