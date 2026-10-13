"""شواهدُ بوّابة المدلول وحده من نصّ النبهانيّ (ADR ٩): كلُّ عبارةٍ بعينها في سطرها من الحاوية المختومة.

الحاويةُ: «الشخصية الإسلامية ج3» `docx` في جذر الغانم المثبَّت (`formal/.lake/packages/a116/`)، وبصمتُها
`CONTAINER_SHA256` (مدخلُ سجلّ الغانم f0025). والبابُ هو باب SLGE المعتمد (ADR ٥٩–٦٠ هناك): كلُّ فقرةٍ
`w:p` بترتيبها، نصوصُ `w:t` فيها موصولة، والسطرُ n هو الفقرةُ n، بلا تطبيع؛ فأرقامُ الأسطر هنا أرقامُ النصّ
المختوم المعتمد بعينها.

`ANCHORS` = (المفتاح، السطر، العبارة). الأداةُ تثبت أنّ كلَّ عبارةٍ في سطرها حرفًا حرفًا، وإلّا
`ANCHOR_NOT_IN_LINE`؛ وتكتب `formal/Madlul/Shawahid.lean`. وبـ`--check` تقارنه بما يولَّد الآن ولا تكتب.
"""

from __future__ import annotations

import hashlib
import io
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONTAINER = (ROOT / "formal" / ".lake" / "packages" / "a116"
             / "الشخصية الاسلامية الجزء الثالث ورد (2).docx")
CONTAINER_SHA256 = "360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd"
OUT = ROOT / "formal" / "Madlul" / "Shawahid.lean"
BOOK = "shakhsiyya-3"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

QISM: tuple[tuple[str, int, str], ...] = (
    ("taqsim", 409, "ينقسم اللفظ باعتبار المدلول وحده إلى خمسة أقسام"),
    ("maana", 410, "أن يكون المدلول معنى، أي شيئاً ليس بلفظ، كالحيوان وكزيد علماً على رجل"),
    ("mufradMustamal", 411, "أن يكون المدلول لفظاً مفرداً مستعملاً، مثل لفظ الكلمة"),
    ("mufradMuhmal", 412, "فحروف ضرب وهي: ضه، وره، وبه، لم توضع لمعنى"),
    ("murakkabMustamal", 413, "فإن مدلوله لفظ مركب موضوع، مثل زيد قائم"),
    ("murakkabMuhmal", 414, "وهو الهذيان"),
    ("murakkabMuhmal", 414, "وهذا القسم غير موضوع، أي لم تضعه العرب"),
)
NAW: tuple[tuple[str, int, str], ...] = (
    ("jins", 406, "فهو الجنس أي اسم الجنس"),
    ("mushtaq", 406, "فهو المشتق، كالأسود والفارس"),
    ("alam", 407, "فهو العلم، كزيد وكعبد الله"),
    ("damir", 407, "فهو المضمر، مثل هو وهي"),
)


def door(raw: bytes) -> list[str]:
    root = ET.fromstring(zipfile.ZipFile(io.BytesIO(raw)).read("word/document.xml"))
    return ["".join(t.text or "" for t in p.iter(W + "t")) for p in root.iter(W + "p")]


def lean_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render(lines: list[str]) -> str:
    def rows(name: str, anchors: tuple[tuple[str, int, str], ...]) -> list[str]:
        out = [f"def {name} : List (String × Marsa) := ["]
        for i, (key, n, phrase) in enumerate(anchors):
            if phrase not in lines[n - 1]:
                raise SystemExit(f"ANCHOR_NOT_IN_LINE:{key}:{n}")
            sep = "," if i + 1 < len(anchors) else ""
            out.append(f"  ({lean_str(key)}, ⟨{lean_str(BOOK)}, {n}, {lean_str(phrase)}⟩){sep}")
        out.append("]")
        return out

    head = [
        "/-! مولَّدٌ بـ`tools/gen_madlul_shawahid.py` من الحاوية المختومة (بصمتُها",
        f"`{CONTAINER_SHA256}`)؛ لا يُحرَّر باليد. كلُّ عبارةٍ في سطرها",
        "من النصّ المختوم المعتمد بعينها (ADR ٩). -/",
        "",
        "namespace Madlul.Shawahid",
        "",
        "/-- مرسًى: الكتاب، والسطر، والعبارةُ بعينها. -/",
        "structure Marsa where",
        "  book : String",
        "  line : Nat",
        "  phrase : String",
        "  deriving DecidableEq, Repr",
        "",
        f"def containerSha256 : String := {lean_str(CONTAINER_SHA256)}",
        "",
        "/-- شواهدُ الأقسام الخمسة والقسمة (س409–414). -/",
    ]
    body = rows("qismShawahid", QISM) + ["", "/-- شواهدُ أنواع المعنى (س406–407). -/"]
    body += rows("nawShawahid", NAW) + ["", "end Madlul.Shawahid", ""]
    return "\n".join(head + body)


def main(argv: list[str]) -> int:
    raw = CONTAINER.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CONTAINER_SHA256:
        raise SystemExit("CONTAINER_SHA_MISMATCH")
    text = render(door(raw))
    if "--check" in argv:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == text
        sys.stdout.write("الشواهدُ مطابقة\n" if ok else "MADLUL_SHAWAHID_DRIFTED\n")
        return 0 if ok else 1
    OUT.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
