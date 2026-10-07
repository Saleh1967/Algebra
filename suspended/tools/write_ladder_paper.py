"""تُكتَب وثيقةُ السلّم **من السجلّ المُقفَل** — لا من ذاكرةٍ ولا من نثر."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
SEAL = REPOSITORY / "tools" / "ladder_seal.py"
PAPER = REPOSITORY / "docs" / "السلّم-المجمَّد.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("ladder_seal", SEAL)
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لسجلّ السلّم")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render() -> str:
    tool = _seal()
    r = tool.FROZEN_LADDER
    complaints = tool.verify_against_logs()
    if complaints:
        raise SystemExit(f"لا تُكتَب وثيقةٌ على سجلٍّ مخالف: {complaints}")

    best = min(range(4), key=lambda one: float(r.outside_unit[one]))
    lines: list[str] = []
    add = lines.append
    add("# السلّمُ مُجمَّدًا — أين يقف التصعيد")
    add("")
    add(f"**ختمُ السجلّ**: `{tool.RECORD_DIGEST}`")
    add("")
    add("**ولا رقمَ منقولٌ ههنا**: هذه الوثيقةُ تُولَّد من **السجلّ المُقفَل**،")
    add("وحقولُه كلُّها **مقيسةٌ** ومُقابَلةٌ بنصّ السجلّ المُودَع سطرًا بسطر،")
    add("وبصمتُه **تُشتَقّ من حقوله** فتبديلُ حقلٍ يُغيّرها.")
    add("")
    add("## ١) الدرجاتُ الأربعُ التي تُرخّصها البايتات")
    add("")
    add(
        "| المستوى | N | أبجديّة | `H` | للوحدة ملحقًا | **للوحدة محجوزًا** "
        "| مرتدّ | `I` |"
    )
    add("|---|---|---|---|---|---|---|---|")
    for index, name in enumerate(r.names):
        mark = "**" if index == best else ""
        add(
            f"| {mark}{name}{mark} | {grouped(r.counts[index])} "
            f"| {grouped(r.alphabets[index])} | {eastern(r.entropies[index])} "
            f"| {eastern(r.inside_unit[index])} "
            f"| **{eastern(r.outside_unit[index])}** "
            f"| {eastern(r.missing[index])} | {eastern(r.flow[index])} |"
        )
    add("")
    add(
        f"**وأرخصُ مستوًى محجوزًا هو `{r.names[best]}`** — "
        f"**{eastern(r.outside_unit[best])}** بتًّا للوحدة."
    )
    add("")
    add("## ٢) الملحَقُ ينزل، والمحجوزُ ينقلب")
    add("")
    add("الملحَقُ للوحدة ينزل **بلا انقطاع**:")
    add("")
    add("```")
    add(" ⟶ ".join(eastern(one) for one in r.inside_unit))
    add("```")
    add("")
    add("والمحجوزُ ينزل **ثمّ ينقلب**:")
    add("")
    add("```")
    add(" ⟶ ".join(eastern(one) for one in r.outside_unit))
    add("```")
    add("")
    add("**فالانقلابُ انتحالٌ لا مادّة**: ما يربحه المستوى الأعلى داخلَ")
    add("العيّنة يخسره على المحجوز، ونصيبُ المرتدّ يرتفع معه —")
    add(f"**{eastern(r.missing[0])} ⟶ {eastern(r.missing[-1])}**.")
    add("")
    add("## ٣) والتصعيدُ الجشع يقف دون اللفظ")
    add("")
    add(f"اللفظُ **{eastern(r.outside_unit[2])}** — أرخصُ من الوحدة")
    add(f"(**{eastern(r.outside_unit[0])}**) وأغلى من الرمز المُرخَّص")
    add(f"(**{eastern(r.outside_unit[1])}**). **فالانقلابُ بين الدرجة الثانية**")
    add("**والثالثة**، لا عند القاع ولا عند القمّة.")
    add("")
    add(f"والسطرُ **{eastern(r.outside_unit[3])}** — أسوأُ الأربع، ومرتدُّه")
    add(f"**{eastern(r.missing[3])}**: فكلُّ سطرٍ يكاد يُهجّى من أوّله.")
    add("")
    add("## ٤) و`I` ترتفع صعودًا — انتحالًا لا بنيةً")
    add("")
    add("```")
    add(" ⟶ ".join(eastern(one) for one in r.flow))
    add("```")
    add("")
    add("**وارتفاعُها عند السطر انتحالٌ**: كلُّ سطرٍ فريدٌ فيعيّن تاليَه في")
    add(f"العيّنة، والمرتدُّ **{eastern(r.missing[3])}**. فلا يُقرأ الرقمُ بنيةً.")
    add("")
    add("## ٥) والحدودُ المبرهَنةُ صمدت عند الدرجات كلِّها")
    add("")
    add("| المستوى | `L − H` | `N·H − log₂` تباديل |")
    add("|---|---|---|")
    for index, name in enumerate(r.names):
        add(
            f"| {name} | {eastern('+' + r.gaps[index])} "
            f"| {eastern('+' + r.stirling[index])} |"
        )
    add("")
    add("**`induction on`** — `L − H` في `[٠، ١)` و`log₂ تباديل ≤ N·H` عند كلّ")
    add("درجة. **و`induction FOR`** — الحلقةُ تشهد عليهما درجةً درجة.")
    add("")
    add("## ٦) وما لا تُرخّصه البايتات — محمولٌ لا مطويّ")
    add("")
    add("| المستوى | الحال | السبب |")
    add("|---|---|---|")
    for name, why in r.vacant:
        add(f"| {name} | `UNCLASSIFIED` | {why} |")
    add("")
    add("**ولم يُسمَّ السطرُ جملةً ولا اللفظُ كلمة.** وكلُّ واحدٍ من هذه")
    add("الأربعة يحتاج **إيداعًا موقَّعًا**، وليس للآلة أن تخترعه.")
    add("")
    add("## ٧) ما يمنع التبديل")
    add("")
    add("**شكلُ السلّم شرطُ بناءٍ في السجلّ لا وصفٌ فيه.** فلا يُقفَل سجلٌّ:")
    add("")
    add("- يرتفع فيه الملحَقُ للوحدة صعودًا،")
    add("- أو يقع أرخصُ محجوزٍ في غير الدرجة الثانية،")
    add("- أو يكون السطرُ أرخصَ من الوحدة،")
    add("- أو يخرج فيه اللفظُ عن أن يكون بين الرمزِ المُرخَّص والوحدة،")
    add("- أو ينقص فيه نصيبُ المرتدّ صعودًا،")
    add("- أو تخرج `L − H` عن `[٠، ١)`، أو ينزل `N·H − تباديل` عن الصفر،")
    add("- أو تزيد المستوياتُ المحمولةُ على أربعةٍ أو تنقص، أو يخلو أحدُها من سبب.")
    add("")
    add("**فمن بدّل رقمًا ليُلطّف النتيجةَ رُدَّ سجلُّه**، ومن بدّله ليُصحّحه")
    add("**تبدّلت بصمتُه وظهر التبديل**.")
    add("")
    return "\n".join(lines) + "\n"


def main() -> int:
    text = render()
    PAPER.write_text(text, encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    sys.exit(main())
