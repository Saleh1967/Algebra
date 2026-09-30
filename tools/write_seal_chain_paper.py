"""تُكتَب وثيقةُ السلسلة **من السجلّ والشاهد** — لا رقمَ يُطبَع بيد."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any, Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DOCS: Final[Path] = REPOSITORY / "docs"
PAPER: Final[Path] = DOCS / "سلسلةُ-الأختام.md"
CHAIN: Final[Path] = REPOSITORY / "deposits" / "seal_chain.json"
WITNESS: Final[Path] = REPOSITORY / "deposits" / "nun_ruling_witness.log"
TOOL: Final[Path] = REPOSITORY / "tools" / "seal_chain.py"
GUARD: Final[Path] = REPOSITORY / "tests" / "algebra" / "test_seal_chain.py"
EASTERN: Final[dict[int, int]] = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _chain() -> Any:
    spec = importlib.util.spec_from_file_location(TOOL.stem, TOOL)
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لآلة السلسلة")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def grab(pattern: str) -> str:
    found = re.search(pattern, WITNESS.read_text(encoding="utf-8"), re.M)
    if found is None:
        raise SystemExit(f"لا شاهدَ لـ{pattern}")
    return found.group(1)


def render() -> str:
    tool = _chain()
    chain = tool.deposited()
    rings = chain["الحلقات"]
    kinds = tool.precedence(chain)
    first, last = rings[0], rings[-1]

    out: list[str] = []
    add = out.append
    add("# سلسلةُ الأختام — الترتيبُ مشدودٌ، والسبقُ مقيس")
    add("")
    add("**هذه الوثيقةُ مُشتَقّة** من `deposits/seal_chain.json` ومن شاهدِ")
    add("`deposits/nun_ruling_witness.log`، وتُعاد بـ`tools/write_seal_chain_paper.py`.")
    add("")
    add("## الدعوى التي كانت تُقال ولا تُقاس")
    add("")
    add("كُتِب في كلّ دفعةِ دمج: «ترتيبُ الختم قبل تشغيله شاهدٌ في التاريخ،")
    add("والكبسُ يطويه». **وهي صحيحةٌ ولم يكن يمسكها فحص** — لا شيءَ كان")
    add("يقرأ التاريخَ فيسأله. **فالدعوى كانت مُحالةً إلى `git` ولا أحدَ**")
    add("**يستنطقه.**")
    add("")
    add("## والمقياس")
    add("")
    add("لكلّ ختمٍ **مرساةٌ**: أوّلُ دفعةٍ أدخلت بصمتَه، تُستخرَج بـ`git log -S`")
    add("على مواضعه. ولسجلِّ تشغيله مرساةٌ مثلُها. **والسبقُ فرقُ تاريخين**")
    add("**مقروءين** لا قولًا في متن.")
    add("")
    add("| الصنف | العدد |")
    add("|---|---:|")
    add(f"| **سبق الختمُ سجلَّه** | **{grouped(len(kinds['سبق']))}** |")
    add(f"| أُودِعا معًا — ولا يُحسَب سبقًا | {grouped(len(kinds['مودعان معا']))} |")
    add(f"| **تأخّر الختمُ عن سجلِّه** | **{grouped(len(kinds['تأخر']))}** |")
    add(f"| بلا سجلٍّ مُودَع — يُسمّى ولا يُقحَم | {grouped(len(kinds['بلا سجل']))} |")
    add(f"| **جملةُ الحلقات** | **{grouped(len(rings))}** |")
    add("")
    add("## والسلسلة")
    add("")
    add(f"    {chain['صيغة_الحلقة']}")
    add("")
    add(f"من جذرِ أصفارٍ إلى خاتمةِ `{last['بصمة_الحلقة'][:16]}…`، وأوّلُ حلقةٍ")
    add(f"مرساتُها `{first['المرساة'][:10]}` في {eastern(first['تاريخ_المرساة'][:10])}.")
    add("")
    add("**والمرساةُ بصمةُ دفعةٍ لا حقلًا زمنيًّا مكتوبًا** — وهي بصمةٌ على")
    add("الشجرة كلِّها في لحظتها، فلا يُزوَّر تاريخُها إلّا بإعادة كتابةِ")
    add("تاريخٍ منشور، **وذلك أثرٌ يُرى**.")
    add("")
    add("## وحدُّها مُعلَن")
    add("")
    add("تُثبت أنّ البصمةَ **كانت في تلك الدفعة**، **ولا تُثبت أنّ التشغيلَ**")
    add("**جرى بعد الختم** — بل أنّ **إيداعَ** سجلِّه تأخّر عن إيداع ختمه.")
    add("ومن ختم وشغّل وأودعهما معًا يُصنَّف «مُودَعان معًا». ونسخةٌ ضحلةٌ لا")
    add("تحمل تاريخًا **فتُصنَّف الحالُ ولا تُصفَّر**.")
    add("")
    add("**ولا يُقبَل مقياسٌ لا يُرى عضُّه**: في")
    add(f"[`{GUARD.name}`](../{GUARD.relative_to(REPOSITORY)}) ثلاثُ صورٍ")
    add("مكذِّبةٍ يُشترَط أن يردَّها — تبديلُ حمولةٍ، وإقحامُ حلقةٍ في الوسط،")
    add("وقلبُ تاريخَي ختمٍ وسجلِّه.")
    add("")
    add("## وما حُجِز عند غيرنا وقِسناه")
    add("")
    add("سجلُّ شجرةٍ جارةٍ يقول: «لا مولِّدَ في هذه الشجرة يُخرِج عددًا لواحدةٍ")
    add("من السبع» — والسبعُ أجناسٌ صوتيّةٌ محجوزة. **وذلك صادقٌ عن شجرةٍ، ولا**")
    add("**يلزم منه أنّ الرسمَ لا يحمل الحكم.** فأربعةٌ منها مقيسةٌ من الرسم")
    add("وحدَه في `examples/rasm/run_nun_ruling_witness.py`:")
    add("")
    add("| الحكم | العدد |")
    add("|---|---:|")
    for name in ("إدغام", "إخفاء", "إظهار", "إقلاب"):
        count = grouped(int(grab("^  " + name + r"\s+(\d+)$")))
        add(f"| {name} | {count} |")
    held = grouped(int(grab(r"يليه U\+0652: (\d+)")))
    add(f"| القلقلة | {held} |")
    add("")
    add("**والمفتاحُ أنّ الحكمَ يُقرَأ من العلامة وغيابِها معًا**: النونُ")
    marked = grouped(int(grab(r"^  سكون\s+(\d+)$")))
    bare = grouped(int(grab(r"^  عُري\s+(\d+)$")))
    add(f"الموسومةُ بالسكون ({marked}) لا تقع قبل")
    add(f"حرفِ إخفاءٍ ولا إقلابٍ قطّ، والعاطلةُ ({bare})")
    add("لا تقع قبل حرفِ إظهارٍ قطّ — **تقاطعان صفران مطبوعان في الشاهد**.")
    add("")
    add("**فالغيابُ بصمةٌ** إذا كان توزيعُه تكامليًّا مشهودًا. وهذا صنفٌ ثالثٌ")
    add("لا تعرفه ثنائيّةُ «لها بصمةٌ فتُقاس، أو لا بصمةَ لها فتُحجَز».")
    add("")
    add("**وما يبقى محجوزًا بحقّ**: الإمالةُ والرومُ والإشمام، ومعها المقاديرُ")
    add("والمراتب. **ولا يقول القياسُ إنّ الحكمَ مسموع — يقول إنّه مُشتَقّ.**")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِبت {PAPER.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
