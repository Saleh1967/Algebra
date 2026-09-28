"""حارسُ المتونِ المُودَعة في التاريخ — **ما يُكتَب في حقلِ أداةٍ لا يُقرَأ**.

**العطلُ الذي يحرسه (٣٣)**: دفعةُ دمجِ الطلب ٥٢ (`a13e735`) تحمل في آخرها
`</commit_message>` و`</invoke>` — **وسمَي بروتوكولٍ دخلا نصًّا**. وسببُه
أنّ المتنَ كُتِب **في حقلِ الأداة مباشرةً**، فلم يُقرَأ قبل إرساله؛ وأختُها
`ca09705` كُتِبت في ملفٍّ (`git commit -F -`) فسلِمت. **ولا يُحرَّر المتنُ
بعد نشره** — إعادةُ كتابةِ تاريخٍ منشورٍ أسوأُ من الوسم — فيبقى ويُقرَأ
بحدِّه، كما بقي `folding_proof_witness.log` (العطل ٢٩).

**فالحرزُ ههنا شيئان**:

١) `objections()` — تُقرَأ على متنٍ **قبل** إيداعه فتردُّ ما فيه من وسوم،
   و`read_message()` تجمع القراءةَ والردَّ في فعلٍ واحدٍ يُستدعى قبل
   `git commit -F`.

٢) `history_stray()` — تمسح متونَ التاريخ الحاضر، **فيُرى العطلُ حيث وقع**
   ولا يُدفَن. والمعروفُ منه مُسمًّى في `REGISTERED`، **وما زاد عليه يُرَدّ**.

`AND_THE_GUARD_DOES_NOT_READ_MEANING`: **وحدُّه مُعلَن**: يحرس **الشكلَ** —
وسمًا شكلُه شكلُ وسمِ بروتوكولٍ خارجَ الشفرة — **ولا يحرس صوابَ المتن**.
متنٌ سليمُ الشكلِ يقول عددًا خاطئًا يمرُّ عليه. **ولا يحرس تاريخًا لا
يبلغه**: نسخةٌ ضحلةٌ لا تحمل إلّا دفعةً واحدة، **فتُصنَّف الحالُ ولا تُصفَّر**
(`shallow_here`).
"""

from __future__ import annotations

import argparse
import re
import subprocess  # noqa: S404
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]

TAG = re.compile(r"</?[A-Za-z_][A-Za-z0-9_.:-]*>")
"""وسمٌ شكلُه شكلُ وسمِ بروتوكول: `<name>` أو `</name>` بلا فراغٍ فيه."""

CODE = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)
"""شفرةٌ مُحاطةٌ بعلامةٍ خلفيّة — ما فيها نصٌّ مقصودٌ لا وسمٌ سارب."""

ALLOWED: frozenset[str] = frozenset({"<sel>"})
"""وسمُ الاختيار في المدوّنة يُذكَر نصًّا في المتون، فلا يُرَدّ."""

REGISTERED: dict[str, tuple[str, ...]] = {
    "a13e73571bd357ec54ac2ef28c8406383d87a874": (
        "</commit_message>",
        "</invoke>",
    ),
}
"""العطلُ ٣٣ بعينه: دفعةٌ منشورةٌ لا تُحرَّر، **فتُسمّى ولا تُخفى**."""


class MessageError(RuntimeError):
    """متنٌ يُرَدّ قبل إيداعه — ويُسمّى ما رُدَّ به."""


def without_code(text: str) -> str:
    """المتنُ بلا ما أُحيط بعلامةٍ خلفيّة — فلا يُرَدّ وسمٌ مقصودٌ في شفرة."""

    return CODE.sub(" ", text)


def stray_tags(text: str) -> tuple[str, ...]:
    """الوسومُ الساربةُ في المتن، مرتَّبةً بلا تكرار."""

    found = {one.group(0) for one in TAG.finditer(without_code(text))}
    return tuple(sorted(found - ALLOWED))


def objections(text: str) -> tuple[str, ...]:
    """ما يُرَدّ به متنٌ — قائمةٌ فارغةٌ تعني أنّه يُودَع."""

    said: list[str] = []
    if not text.strip():
        said.append("متنٌ خالٍ: لا يُودَع في التاريخ")
    for one in stray_tags(text):
        said.append(f"وسمٌ ساربٌ خارجَ الشفرة: {one}")
    return tuple(said)


def read_message(where: Path) -> str:
    """يُقرَأ المتنُ من ملفٍّ ويُرَدّ إن أُعيب — **وهذا موضعُ القراءة**."""

    text = where.read_text(encoding="utf-8")
    said = objections(text)
    if said:
        raise MessageError(f"{where.name}: " + "؛ ".join(said))
    return text


def shallow_here() -> bool:
    """أَنسخةٌ ضحلة؟ فالتاريخُ لا يُمسَح، **وتُصنَّف الحالُ ولا تُصفَّر**."""

    return (REPOSITORY / ".git" / "shallow").exists()


def messages(ref: str = "HEAD") -> dict[str, str]:
    """متونُ ما يبلغه `ref` في هذه النسخة — بصمةً كاملةً ومتنًا."""

    done = subprocess.run(  # noqa: S603
        ["git", "log", "--format=%H%x1f%B%x1e", ref],  # noqa: S607
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=True,
    )
    found: dict[str, str] = {}
    for record in done.stdout.split("\x1e"):
        if "\x1f" not in record:
            continue
        digest, body = record.split("\x1f", 1)
        found[digest.strip()] = body
    return found


def history_stray(ref: str = "HEAD") -> dict[str, tuple[str, ...]]:
    """كلُّ دفعةٍ يبلغها `ref` وفيها وسمٌ سارب — المعروفُ منها والزائد."""

    return {
        digest: found
        for digest, body in messages(ref).items()
        if (found := stray_tags(body))
    }


def unregistered(ref: str = "HEAD") -> dict[str, tuple[str, ...]]:
    """ما زاد على المسجَّل — **وهو ما يُرَدّ**، والمسجَّلُ يُقرَأ ولا يُكرَّر."""

    return {
        digest: found
        for digest, found in history_stray(ref).items()
        if REGISTERED.get(digest) != found
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="حارسُ المتون")
    parser.add_argument("--file", type=Path, help="متنٌ يُقرَأ ويُرَدّ إن أُعيب")
    parser.add_argument("--history", action="store_true", help="مسحُ متون التاريخ")
    given = parser.parse_args()
    if given.file is not None:
        try:
            read_message(given.file)
        except MessageError as why:
            print(f"رُدَّ: {why}")
            return 1
        print(f"يُودَع: {given.file.name}")
    if given.history:
        if shallow_here():
            print("نسخةٌ ضحلة: التاريخُ لا يُمسَح — والحالُ مُصنَّفةٌ لا مُصفَّرة")
            return 0
        extra = unregistered()
        for digest, found in sorted(extra.items()):
            print(f"وسمٌ ساربٌ غيرُ مسجَّل: {digest[:10]} — {' · '.join(found)}")
        print(f"— مسجَّلٌ: {len(REGISTERED)} | وزائدٌ: {len(extra)}")
        return 1 if extra else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
