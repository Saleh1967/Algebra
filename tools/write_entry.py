"""مدخلُ البرنامج — **يُشتَقّ من الشجرة** لا يُكتَب يدًا، فلا يَبلى صامتًا.

`تقرير-الإنجاز.md` مؤرَّخٌ بيومه ويصدق عليه، **وأعدادُه لا تتبع الشجرة**.
فهذا المدخلُ يَعُدّ ما في الشجرة عند كلّ توليد: الأختامَ وشروطَها،
والأعطالَ، والسجلّاتِ المُقفَلة، والوثائقَ المولَّدةَ بمولّداتها.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
TOOLS = REPOSITORY / "tools"
DOCS = REPOSITORY / "docs"
ENTRY = DOCS / "مدخل.md"
INDEX = "tools/write_seal_index.py"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")

STANDING: tuple[tuple[str, str, str], ...] = (
    (
        "كلُّ رقمٍ كلميٍّ له نسختان",
        "المُجمَّدُ يُلحِق البسملةَ بأوّل آيةٍ من كلّ سورة — ١١٢ سطرًا و٤٤٨ "
        "كلمة. فما قِيس على الكلم يُقال فيه: **أبالبسملات أم بدونها**.",
        "الأرقام-مرفوعة-البسملات.md",
    ),
    (
        "الجشعُ ليس أمثل",
        "الاختيارُ الأمثلُ محلّيًّا **أضرُّ** من الكافي محلّيًّا، وبتّةٌ "
        "واحدةٌ التُزِمت لأنّها بدت أربحَ كلّفت ١١٬١٩٤ بتًّا.",
        "الانقلاب-المجمَّد.md",
    ),
    (
        "التصعيدُ يقف دون اللفظ",
        "أرخصُ درجةٍ محجوزًا هي الرمزُ المُرخَّص، لا اللفظُ ولا السطر — "
        "والملحَقُ ينزل بلا انقطاع، فالانقلابُ **انتحالٌ لا مادّة**.",
        "السلّم-المجمَّد.md",
    ),
    (
        "أربعةُ مستوياتٍ لا تُرخّصها البايتات",
        "الكلمةُ المفردة، والتركيبُ الإسناديّ، والتركيبُ المزجيّ، والجملة "
        "— `UNCLASSIFIED` بأسبابها. **ولا يُسمّى السطرُ جملةً ولا اللفظُ "
        "كلمة.**",
        "السلّم-المجمَّد.md",
    ),
    (
        "قاعدةُ الفصل مُودَعةٌ غيرُ موقَّعة",
        "صاغتها الآلةُ مسوَّدةً، ومضمونُها تفسير. **فتُقاس ولا تُرقّي "
        "مستوًى**، والتوقيعُ فعلُ صاحب المستودع.",
        "../deposits/separation_rule.md",
    ),
    (
        "أوّلُ بتّةٍ يدفع لها المجمَّد بتّةُ الموضع لا بتّةُ الجار",
        "الجشعُ اختار من سبعةٍ وخمسين سؤالًا «أآخرُ السطر؟» بربحٍ محجوزٍ "
        "**+٠٫٠٥٦٩** — الأكبرِ في السلّم. **وختمٌ آخرُ لم يقرأه قاس "
        "`I(الحال ؛ الموضع)` = ٠٫٠٥٦٥٢٩** — فالتلاقي **محروسٌ ببناء "
        "السجلّ** لا مرويّ.",
        "سلّم-السياق-بلا-تسريب.md",
    ),
    (
        "مجرى الحرف يقود مجرى الحال، وللبتّات سهمٌ زمنيّ",
        "النقلُ محجوزًا **٠٫٠٣٦٦٧٢** من `H(ح)` مقابلَ **٠٫٠٠٥٥٠٧** من "
        "`H(ر)`، وقلبُ السطر يُبدِّل المقيس **٠٫٠٥٧٥٤٦** بتًّا "
        "والقناتان سهماهما متعاكسان. **والنقلُ ليس السببيّة**: لا "
        "تدخّلَ في نصٍّ مجمَّد.",
        "النقل-والسهم.md",
    ),
    (
        "ما نُقِل من خارجٍ يُودَع غيرَ موقَّع ويُعاد حسابُه لا قياسُه",
        "ثلاثةُ أنابيبَ خارجيّةٍ أُودِعت بنصّها: يُعاد **كلُّ رقمٍ يسمح "
        "منشورُها بإعادة اشتقاقه**، ويُحَدُّ ما لا يسمح **بحدّين**، "
        "وتُسمّى الدُّيونُ بأرقامها. **ولا يُوقَّع تأويلٌ ولا يُنقَل رقمٌ "
        "بين مقامين.**",
        "العدد-والمعدود-حسابًا.md",
    ),
)


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _index() -> Any:
    spec = importlib.util.spec_from_file_location(
        "write_seal_index", REPOSITORY / INDEX
    )
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لفهرس الأختام")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def generated() -> list[tuple[str, str]]:
    """(الوثيقةُ المولَّدة، مولّدُها) — تُكتشَف من الأدوات لا تُعَدّ يدًا."""

    found: list[tuple[str, str]] = []
    for path in sorted(TOOLS.glob("write_*.py")):
        text = path.read_text(encoding="utf-8")
        hit = re.search(r'^(?:PAPER|INDEX|ENTRY) = DOCS / "(.+?)"', text, re.MULTILINE)
        if hit is None:
            hit = re.search(
                r'^(?:PAPER|INDEX|ENTRY) = REPOSITORY / "docs" / "(.+?)"',
                text,
                re.MULTILINE,
            )
        if hit is not None:
            found.append((hit.group(1), str(path.relative_to(REPOSITORY))))
    return found


def render() -> str:
    tool = _index()
    seals = tool.gather()
    records = tool.records()
    marks = sum(int(one["count"]) for one in seals)
    flaws = re.findall(
        r"^## [٠-٩]+\) ",
        (DOCS / "سجل-الأعطال.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    made = generated()
    # المدخلُ يعدّ نفسَه ولو لم يُكتَب بعد — وإلّا لم يستقرّ على عددٍ أبدًا
    papers = sorted({one.name for one in DOCS.glob("*.md")} | {ENTRY.name})

    out: list[str] = []
    add = out.append
    add("# مدخلُ البرنامج — ما يقف، وأين يُقرأ")
    add("")
    add("**هذا الملفُّ مُشتَقٌّ من الشجرة** ويُعاد توليدُه، فأعدادُه تتبعها")
    add("ولا تَبلى صامتة. و`تقرير-الإنجاز.md` **مؤرَّخٌ بيومه** ويصدق عليه،")
    add("ولا تُؤخَذ أعدادُه حالًا راهنة.")
    add("")
    add("## الحالُ عددًا")
    add("")
    add("| المقيس | العدد |")
    add("|---|---|")
    add(f"| أختامٌ مُسجَّلةٌ قبل النظر | **{grouped(len(seals))}** |")
    add(f"| شروطٌ فيها | **{grouped(marks)}** |")
    add(f"| سجلّاتٌ مُقفَلةٌ ببصمةٍ تُعاد | {grouped(len(records))} |")
    add(f"| أعطالٌ مُسجَّلةٌ على الآلة | **{grouped(len(flaws))}** |")
    add(f"| وثائقُ في `docs/` | {grouped(len(papers))} |")
    add(f"| منها مولَّدةٌ ومحروسة | **{grouped(len(made))}** |")
    add("")
    add("## القاعدةُ الواحدة")
    add("")
    add("**الشرطُ يُكتَب ويُدفَع قبل التشغيل، والترتيبُ في تاريخ المستودع.**")
    add("ولا يُعاد تفسيرُ شرطٍ بعد رؤية رقمه؛ وما لم يُقَس **يُقال إنّه لم**")
    add("**يُقَس**؛ وما لا مانعَ له آليًّا **يُقال إنّه بلا مانع**.")
    add("")
    add("**والبوّابة واحدة**: `bash tools/verify.sh` — بلا أنبوبٍ حول الفحص،")
    add("فرمزُ خروجها رمزُ ما سقط.")
    add("")
    add("## ما يقف — ويُقرَأ هكذا")
    add("")
    for index, (title, body, where) in enumerate(STANDING, start=1):
        add(f"**{eastern(index)}. {title}** — {body}")
        add(f"  ← [`{where.rsplit('/', 1)[-1]}`]({where})")
        add("")
    add("## الوثائقُ المولَّدةُ ومولّداتُها")
    add("")
    add("| الوثيقة | تُولَّد بـ |")
    add("|---|---|")
    for name, maker in made:
        add(f"| [`{name}`]({name}) | `{maker}` |")
    add("")
    add("**ويحرس فحصٌ لكلٍّ منها أنّ المكتوبَ مطابقٌ لما يولّده مولّدُها**،")
    add("فلا يُحرَّر رقمٌ فيها بيد.")
    add("")
    add("## الجردُ الحيّ")
    add("")
    add("- [`ما-بُرهن-وما-قِيس.md`](ما-بُرهن-وما-قِيس.md) — ما صمد وما سُحب،")
    add("  والمسحوبُ **بعلامة الشطب لا بالحذف**.")
    add("- [`سجل-الأعطال.md`](سجل-الأعطال.md) — أعطالُ الآلة، لكلٍّ")
    add("  «ما كان / كيف انكشف / ما يمنعه الآن».")
    add("- [`فهرس-الأختام.md`](فهرس-الأختام.md) — كلُّ ختمٍ ببصمةٍ")
    add("  **مُعادةِ الاشتقاق**، ولا ختمَ في الشجرة خارجَه.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    text = render()
    ENTRY.write_text(text, encoding="utf-8")
    print(f"كُتِب {ENTRY.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    sys.exit(main())
