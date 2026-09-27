"""تُكتَب وثيقةُ الحصر والاستثناء **من السجلّ المُقفَل** — لا من نثر."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
SEAL = REPOSITORY / "tools" / "hasr_ledger_seal.py"
PAPER = REPOSITORY / "docs" / "الحصر-والاستثناء-حسابًا.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("hasr_ledger_seal", SEAL)
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لسجلّ الحصر والاستثناء")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render() -> str:
    tool = _seal()
    r = tool.FROZEN_HASR
    complaints = tool.verify_against_logs()
    if complaints:
        raise SystemExit(f"لا تُكتَب وثيقةٌ على سجلٍّ مخالف: {complaints}")
    flat = tool.binary(r.exception / r.total)
    gains = [float(one) for one in r.ladder_gains]

    out: list[str] = []
    add = out.append
    add("# الحصرُ والاستثناء — حسابًا لا قياسًا")
    add("")
    add(f"**ختمُ السجلّ**: `{tool.RECORD_DIGEST[:8]}…` — مُشتَقٌّ من حقوله.")
    add("")
    add("**فصلٌ لم تُجرِه هذه الشجرة**، على **تشجيرٍ ليس في هذا المستودع**.")
    add("**ولا أوقّع تأويلَه**: لا قراءةَ الكتاب في «إنّما»، ولا حكمَ")
    add("المُشجِّر في «إلّا». **وما فعلتُه إعادةُ حسابه على أعداده.**")
    add("")
    add("## ثلاثةُ أشياءَ وجدها الحساب")
    add("")
    add("### ١) التقديرُ سُمّي باسمه — ولم يُسمَّ المنشورُ خطأً")
    add("")
    add("المنشورُ من المعلومات **لا يوافق التقديرَ الخام**. ولم أقل «خطأ»:")
    add("جرّبتُ **تصحيحَ الانحياز من الرتبة الأولى** فأعاد الرقمين معًا.")
    add("")
    add("| الملمح | خامًا | مُصحَّحًا | المنشور |")
    add("|---|---|---|---|")
    for name, cells in (
        ("م١ النفيُ السابق", r.sign_cells),
        ("م٢ حالةُ التالي", r.case_cells),
    ):
        rows = list(cells)
        seen = sum(one for one, _ in rows)
        if seen < r.total:
            rows.append((r.total - seen, r.exception - sum(two for _, two in rows)))
        raw = flat - tool.conditional(tuple(rows))
        fixed = raw - tool.miller_madow(len(rows), r.total)
        shown = dict(r.published)[name.split()[0]]
        add(
            f"| {name} | {eastern(f'{raw:.6f}')} | {eastern(f'{fixed:.6f}')} "
            f"| **{eastern(shown)}** |"
        )
    add("")
    add("**فالمقدارُ مُشتَقٌّ لا مظنون**، والسجلُّ **يردُّ نفسَه إن لم**")
    add("**يُعِده**. وهذا ليس تصحيحًا لأحدٍ، بل **تسميةُ ما لم يُسمَّ**.")
    add("")
    add("### ٢) عددان للاستثناء لا يجتمعان")
    add("")
    add(f"العرضُ يحمل **{eastern(r.exception)}** و**{eastern(r.rejected_count)}**.")
    add(f"وخانتا «النفي السابق» تحملان **{eastern(r.exception)}** على")
    add(f"**{eastern(r.total)}** موضعًا — **فيُغلِق {eastern(r.exception)}**")
    add(f"**وحدَه**، و**{eastern(r.restriction)} + {eastern(r.rejected_count)}**")
    add("لا يبلغ المقام. **وسببُ الآخر لا يُخمَّن**؛ وقد ورد")
    add(f"**{eastern(r.rejected_count)}** في إيداعٍ سابقٍ أيضًا.")
    add("")
    add("### ٣) الجشعُ صرف بتّةً لم يحتجها")
    add("")
    add("| الدرجة | الربح |")
    add("|---|---|")
    for index, gain in enumerate(r.ladder_gains):
        add(f"| د{eastern(index + 1)} | {eastern(gain)} |")
    add("")
    add(f"**صرف {eastern(r.bits_spent)} بتّاتٍ والسقفُ الخام**")
    add(f"**{eastern(r.bits_needed)}** — لأنّ أسئلته «واحدٌ ضدّ الباقي»، ولو")
    add("قُسِمت الكتلتان معًا لكفت بتّتان. **فهذا شاهدٌ مقيسٌ على أنّ الجشعَ**")
    add("**غيرُ مبرهَن** — في السلّم نفسِه لا في النصّ.")
    add("")
    add(f"**والبتّةُ الأولى تشتري {eastern(f'{gains[0] / math.fsum(gains):.6f}')}**")
    add("**من الكسب الخام** — أكثرَ من ستّة أسباعه.")
    add("")
    add("## وما تبقّى من الحيرة")
    add("")
    add(f"`H(الوظيفة)` = **{eastern(f'{flat:.6f}')}** بت. وأقوى ملمحٍ يشتري")
    best = float(dict(r.published)["م٢"])
    bought, left = eastern(f"{best / flat:.2%}"), eastern(f"{1 - best / flat:.2%}")
    add(f"**{eastern(dict(r.published)['م٢'])}** — **{bought}**")
    add(f"منها. **فـ{left} باقيةٌ بلا مساس.**")
    add("")
    add("**وهذا هو مقدارُ ما ترجمه المصنِّف**:")
    add("")
    add("| الواقع | تنبّأ حصرًا | تنبّأ استثناءً |")
    add("|---|---|---|")
    right, wrong, missed, caught = r.confusion
    add(f"| حصر ({eastern(right + wrong)}) | {eastern(right)} | {eastern(wrong)} |")
    seen = eastern(missed + caught)
    add(f"| استثناء ({seen}) | {eastern(missed)} | {eastern(caught)} |")
    add("")
    add(f"**أصاب من الاستثناء {eastern(caught)} من {eastern(missed + caught)}**")
    add(f"= **{eastern(f'{caught / (missed + caught):.4%}')}**. والزيادةُ على")
    add(f"الأغلب الأعمى **موضعٌ واحدٌ من {eastern(r.held_out[0][2])}**.")
    add("")
    add(f"**فـ{left} من الحيرة باقية، والترجمةُ موضعٌ واحدٌ من ٣٤١** —")
    add("والرقمان **يقولان الشيءَ نفسَه من طريقين**.")
    add("")
    add("## induction ON وinduction FOR")
    add("")
    add("**ON**: تعدادٌ تامٌّ على المقام، **والتنقيحُ لا يُنقِص المعلومات** —")
    add("مبرهنةٌ مُصانةٌ عند كلّ تكتيلٍ للخانات الأربع.")
    add("")
    add("**FOR**: **لم ينجح، وذاك إعلانُ الأنبوب نفسِه** —")
    add("")
    add("| الذراع | المحجوز |")
    add("|---|---|")
    for label, hits, tries in r.held_out:
        add(f"| {label} | {eastern(hits)}/{eastern(tries)} |")
    add("")
    add("**والمجالان متداخلان.**")
    add("")
    add("## ما لم يُنشَر فلم يُبنَ")
    add("")
    for one in r.unbuilt:
        add(f"- {one}")
    add("")
    add("**ولا تُصدَّق ولا تُكذَّب.**")
    add("")
    add("## الدُّيونُ — مُسمّاةٌ بنصّها")
    add("")
    for name, why in r.debts:
        add(f"- **{name}** — {why}.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
