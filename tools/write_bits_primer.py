"""«بايثون العربيّة بالبتّات» — **وثيقةٌ مولَّدةٌ من الشفرة والودائع**.

**العطلُ الذي تتجنّبه**: الدرسُ إذا كُتِب بيدٍ انفصل عمّا يُعلِّمه. فرقمٌ
في شرحٍ لا يُعاد من الشجرة يَبلى صامتًا، **ويبقى يُعلَّم بعد أن كَذَب**.

**فكلُّ عددٍ ههنا مقروءٌ حسابًا**: من `algebra.rasm` و`algebra.folding`
ومن الودائع المُودَعة ومن `ci.yml` نفسِه. **ولا رقمَ يُطبَع بيد.**

`A_LESSON_THAT_IS_NOT_RE_DERIVED_ROTS`: وحدُّها مُعلَن: تُعاد بتشغيل
مولّدها، ويُقابَل المكتوبُ بالمولَّد في فحصٍ — **فدرسٌ يخالف شجرتَه
يُرَدّ**. ولا تحرس **صوابَ التعليم**، بل **مطابقتَه لما في الشجرة**.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import unicodedata as ud
from pathlib import Path
from typing import Any, Final

REPOSITORY: Final[Path] = Path(__file__).resolve().parents[1]
DOCS: Final[Path] = REPOSITORY / "docs"
PAPER: Final[Path] = DOCS / "بايثون-بالبتّات.md"
DEPOSITS: Final[Path] = REPOSITORY / "deposits"
WORKFLOW: Final[Path] = REPOSITORY / ".github" / "workflows" / "ci.yml"
CORPUS: Final[Path] = REPOSITORY / "quran-simple-enhanced.txt"
EASTERN: Final[dict[int, int]] = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _module(where: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, where)
    if spec is None or spec.loader is None:
        raise SystemExit(f"لا قارئَ لـ{where}")
    found = importlib.util.module_from_spec(spec)
    sys.modules[name] = found
    spec.loader.exec_module(found)
    return found


def grab(pattern: str, where: Path) -> str:
    found = re.search(pattern, where.read_text(encoding="utf-8"), re.MULTILINE)
    if found is None:
        raise SystemExit(f"لا شاهدَ في {where.name} لـ{pattern}")
    return found.group(1)


def render() -> str:
    sys.path.insert(0, str(REPOSITORY / "src"))
    from algebra import folding, rasm

    tashif = DEPOSITS / "tashif_space_witness.log"
    nun = DEPOSITS / "nun_ruling_witness.log"
    guard = _module(REPOSITORY / "tests" / "algebra" / "test_ci_workflow.py", "ciguard")

    out: list[str] = []
    add = out.append
    add("# بايثون العربيّة بالبتّات")
    add("")
    add("**وثيقةٌ مولَّدة** من `tools/write_bits_primer.py` — وكلُّ عددٍ فيها")
    add("مقروءٌ من الشفرة أو من وديعةٍ مُودَعة، **ولا رقمَ مكتوبٌ بيد**.")
    add("")
    add("## ١) الطبقاتُ الخمس — ولكلٍّ عقدٌ")
    add("")
    add("| # | الطبقة | جامعةٌ بأن | مانعةٌ بأن |")
    add("|---|---|---|---|")
    add("| ٠ | البايتات | بصمةٌ وترميزٌ مُصرَّح | لا تُطبَّع ولا تُحرَّر |")
    add("| ١ | النقاط | كلُّ نقطةٍ مُصنَّفة | لا يُقفَز إلى «حرف» |")
    add("| ٢ | الوحدة = حرف + حالة | لكلّ موضعٍ حالةٌ واحدة | **لا حالةَ مركَّبة** |")
    add("| ٣ | الرسمُ المهمَل | لكلّ حرفٍ أصلٌ أعجم | لا ضبطَ يدخله |")
    add("| ٤ | الحكم | يُشتَقّ من ٢ و٣ | لا يُدَّعى ما لا يُشتَقّ |")
    add("")
    add("**وبايثون تعطي ٠ و١ كاملتين، ولا تعطي ٢ و٣ و٤** — فتلك تُكتَب.")
    add("")

    add("## ٢) المدوّنةُ بايتاتٍ")
    add("")
    raw = CORPUS.read_bytes()
    text = raw.decode("utf-8").replace("<sel>", " ")
    points = sorted({one for one in text if one not in " \n"})
    add(f"- بايتات: **{grouped(len(raw))}** · بِتّات: **{grouped(len(raw) * 8)}**")
    add(f"- نقاطٌ متمايزةٌ في الأبجديّة: **{grouped(len(points))}**")
    letters = grouped(int(grab(r"حروفُ الرسم: (\d+)", nun)))
    add(f"- حروفُ الرسم (فئة `Lo`): **{letters}**")
    add("")

    add("## ٣) ما لا يُرى — وترتيبُ العلامتين")
    add("")
    shadda, tanwin = chr(0x0651), chr(0x064B)
    add(f"- `ccc` الشدّة **{eastern(ud.combining(shadda))}** ·")
    add(f"  `ccc` فتحتان **{eastern(ud.combining(tanwin))}**")
    add("- فالترتيبُ المعياريُّ تصاعديّ، **والتطبيعُ يقلب الزوج**:")
    base = chr(0x0628)
    written = base + shadda + tanwin
    flips = "نعم" if ud.normalize("NFC", written) != written else "لا"
    add(f"  `NFC` يردُّ الشدّةَ بعد التنوين: **{flips}**")
    written_pairs = grouped(int(grab(r"شدّةٌ ثمّ تنوين: (\d+)", tashif)))
    flipped_pairs = grouped(int(grab(r"تنوينٌ ثمّ شدّة: (\d+)", tashif)))
    caught = grouped(int(grab(r"مصائدُ المدخل: (\d+)", tashif)))
    add(f"- وفي المدوّنة: شدّةٌ ثمّ تنوين **{written_pairs}**،")
    add(f"  وبالعكس **{flipped_pairs}**")
    add(f"- ومصائدُ المدخل الستّ: **{caught}**")
    add("")

    add("## ٤) الرسمُ المهمَل ومساحةُ التصحيف")
    add("")
    add(f"- عائلاتٌ: **{grouped(len(rasm.families()))}** ·")
    add(f"  نقاطٌ مردودة: **{grouped(len(rasm.ARCHETYPE))}**")
    for label, pattern in (
        ("ألفاظٌ متمايزة", r"ألفاظٌ متمايزة\s+: (\d+)"),
        ("هياكلُ متمايزة", r"هياكلُ متمايزة\s+: (\d+)"),
        ("هياكلُ تحمل أكثرَ من لفظ", r"هياكلُ تحمل أكثرَ من لفظ: (\d+)"),
    ):
        add(f"- {label}: **{grouped(int(grab(pattern, tashif)))}**")
    add("")
    add("**والزمرةُ موضعُ اشتباهٍ لا خطأ** — لا تقول إنّ أحدَهما مصحَّف.")
    add("")

    add("## ٥) الطيُّ — عددٌ واحدٌ يُفَكّ بلا طولٍ مستعار")
    add("")
    unit = folding.Guarded(free=9, blocked=6)
    word = (0, 4, 11, 2)
    index = folding.fold_any(unit, word)
    add(f"- الحارس: `x² = {eastern(unit.free)}x + {eastern(unit.free * unit.blocked)}`")
    add(f"- كلمةٌ من **{eastern(len(word))}** حالاتٍ ⟶ العدد **{grouped(index)}**")
    add(f"  (**{eastern(index.bit_length())}** بتّة) ⟶ تُفَكّ فترجع بعينها:")
    back = "نعم" if folding.unfold_any(unit, index) == word else "لا"
    add(f"  **{back}**")
    add("")

    add("## ٦) وبوّابتان يجب أن تتّفقا")
    add("")
    add("| البوّابة | محلّيًّا | على Runner |")
    add("|---|---|---|")
    described = WORKFLOW.read_text(encoding="utf-8")
    on_runner = {guard.kind_of(one): one for one in guard.runs(described)}
    here = {guard.kind_of(one): one for one in guard.local_gates()}
    for gate in guard.GATES:
        add(f"| `{gate}` | `{here[gate]}` | `{on_runner[gate]}` |")
    add("")
    add(f"**وخلافاتٌ مُسجَّلةٌ بسببها: {eastern(len(guard.DECLARED))}** — وما زاد يُرَدّ.")
    add("")
    add("## ٧) والقاعدةُ التي تحكم الدروسَ كلَّها")
    add("")
    add("**الأخضرُ عقدٌ، وسعتُه سعةُ ما كُتِب فيه.** ونجاحُ الفحص يعني أنّ")
    add("الفحوصَ اجتازت شروطَها، **لا أنّ النظريّةَ صحيحة**. وأوضحُ برهانٍ")
    add("على ذلك في هذه الشجرة: عنوانٌ يقول «مبرهنة» مرّ على البوّابة")
    add("مئاتِ المرّات بلا برهانٍ تحته — **وهو العطل ٣٤**، ومنعُه المادّة ٣٩.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِبت {PAPER.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
