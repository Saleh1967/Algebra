"""تُكتَب وثيقةُ الانقلاب **من السجلّ المُقفَل** — لا من ذاكرةٍ ولا من نثر."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

REPOSITORY = Path(__file__).resolve().parents[1]
SEAL = REPOSITORY / "tools" / "inversion_seal.py"
PAPER = REPOSITORY / "docs" / "الانقلاب-المجمَّد.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def _seal() -> Any:
    spec = importlib.util.spec_from_file_location("inversion_seal", SEAL)
    if spec is None or spec.loader is None:
        raise SystemExit("لا قارئَ لسجلّ الانقلاب")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render() -> str:
    tool = _seal()
    r = tool.FROZEN_INVERSION
    complaints = tool.verify_against_logs()
    if complaints:
        raise SystemExit(f"لا تُكتَب وثيقةٌ على سجلٍّ مخالف: {complaints}")

    lines: list[str] = []
    add = lines.append
    add("# الانقلابُ مُجمَّدًا — الأكثرُ وقوعًا ليس الأكبرَ ربحًا")
    add("")
    add(f"**ختمُ السجلّ**: `{tool.RECORD_DIGEST}`")
    add("")
    add("**ولا رقمَ منقولٌ ههنا**: هذه الوثيقةُ تُولَّد من **السجلّ المُقفَل**،")
    add("وحقولُه كلُّها **مقيسةٌ** ومُقابَلةٌ بنصّ السجلّات المُودَعة حرفًا")
    add("بحرف، وبصمتُه **تُشتَقّ من حقوله** فتبديلُ حقلٍ يُغيّرها.")
    add("")
    add("## ١) ما رُصِد")
    add("")
    add("لمّا صار الالتزامُ **بأكبرِ ربحٍ** بدل **أوّلِ رابح**، والعمقُ واحد:")
    add("")
    add("| المقيس | القيمة |")
    add("|---|---|")
    add(f"| الحالات | {grouped(r.states)} |")
    add(
        f"| توافقُ الرتبة الأولى | **{grouped(r.rank_agreed)}** "
        f"({eastern(f'{r.rank_agreed / r.states:.4f}')}) |"
    )
    add(
        f"| توافقُ القرار | **{grouped(r.choice_agreed)}** "
        f"({eastern(f'{r.choice_agreed / r.states:.4f}')}) |"
    )
    add(
        f"| وسيطُ رتبةِ المختار (من {grouped(r.search_depth)}) "
        f"| **{grouped(r.median_chosen_rank)}** |"
    )
    add(f"| نصيبُ الرتبتين الأخيرتين | **{eastern(r.edge_share)}** |")
    add(f"| وسيطُ وقوعِ ما يختاره «أكبرُ ربحًا» | {grouped(r.median_count_chosen)} |")
    add(f"| وسيطُ وقوعِ ما يختاره «أوّلُ رابح» | {grouped(r.median_count_first)} |")
    add("")
    add("**فالربحُ الأكبرُ في الأندر** — والترتيبان **متعاكسان**.")
    add("")
    add("## ٢) ولماذا — اشتقاقًا لا وصفًا")
    add("")
    add("التكلفةُ **لوغاريتمُ عدد التباديل المتمايزة**، فالربحُ نسبةُ معاملين:")
    add("")
    add("```")
    add("G = log₂ N⁽ᵐ⁾ − log₂ nₐ⁽ᵐ⁾ − log₂ n_b⁽ᵐ⁾ + log₂ m!")
    add("G ≈ m · ( PMI − log₂ e ),   PMI = log₂ ( m·N ⁄ nₐ·n_b )")
    add("```")
    add("")
    add(
        f"على أكثرِ {grouped(r.pairs_looked)} زوجٍ وقوعًا في L₀ — "
        f"أبجديّةُ {grouped(r.base_units)} على {grouped(r.corpus_units)} وحدةً:"
    )
    add("")
    add("| المرتَّبُ به | ρ مع الربح المقيس |")
    add("|---|---|")
    add(f"| **الوقوعُ الخام `m`** | **{eastern('+' + r.rho_count)}** |")
    add(f"| فائضُ الاقتران `PMI` | {eastern('+' + r.rho_pmi)} |")
    add(f"| التقريبُ `m·(PMI − log₂e)` | {eastern('+' + r.rho_leading)} |")
    add(f"| **المشتَقُّ بالتباديل تامًّا** | **{eastern('+' + r.rho_derived)}** |")
    add("")
    add(f"**والوقوعُ والاقترانُ شبهُ مستقلَّين**: `ρ = {eastern('+' + r.rho_count_pmi)}`.")
    add("فالترتيبُ بالعدد والترتيبُ بالربح **مقياسان لا مقياس** — وثَمَّ ينقلب.")
    add("")
    add("| المقيس | القيمة |")
    add("|---|---|")
    add(f"| توافقُ الإشارة | {grouped(r.sign_agreed)} من {grouped(r.pairs_looked)} |")
    add(
        f"| توافقُ عتبة `PMI > log₂e = {eastern(r.threshold_bits)}` "
        f"| **{grouped(r.threshold_agreed)}** من {grouped(r.pairs_looked)} |"
    )
    add(f"| وسيطُ الخطأ النسبيّ | {eastern(r.median_relative_error)} |")
    add("")
    add("**فرخصةُ الدمج حدٌّ على فائض الاقتران لا على العدد.**")
    add("")
    add("## ٣) وماركوف")
    add("")
    add("```")
    add("Σ p(a,b)·PMI(a,b) = H(Xₜ₊₁) − H(Xₜ₊₁|Xₜ) = I(Xₜ ; Xₜ₊₁)")
    add("```")
    add("")
    add(f"`I = Σ p·PMI = {eastern(r.mutual_information)}` بتًّا للموضع — **هويّةً**.")
    add("")
    add(f"ومواضعُ الجوار {grouped(r.adjacency_places)}، فسقفُ الرتبة الأولى")
    add(f"**{grouped(r.first_order_ceiling)}** بتًّا؛ وما وفّره الصعودُ")
    add(f"**{grouped(r.block_saving)}** — **والنسبةُ {eastern(r.ceiling_ratio)}**.")
    add("")
    add("**فالصعودُ يبلغ ما فوق الرتبة الأولى**: الرموزُ المدموجةُ تمتدّ،")
    add("فيصير جوارُها جوارَ رتبٍ أبعد.")
    add("")
    add("## ٤) وحدُّ ستيرلنغ يتّسع ولا ينكمش")
    add("")
    add(f"الفرقُ للرمز بين `N·H` و`log₂` التباديل: من **{eastern(r.stirling_low)}**")
    add(f"عند L₀ إلى **{eastern(r.stirling_high)}** بعد ألفَي دمجة. **يكبر بعدد**")
    add("**الرموز، لا خللٌ في القياس** — والمتراجحةُ `log₂ تباديل ≤ N·H`")
    add("مبرهَنةٌ ومُصانةٌ عند كلّ حال.")
    add("")
    add("## ٥) ما يمنع التبديل")
    add("")
    add("**الانقلابُ شرطُ بناءٍ في السجلّ لا وصفٌ فيه.** فلا يُقفَل سجلٌّ:")
    add("")
    add("- يكون فيه ارتباطُ العدد الخام أقوى من ارتباط المشتَقّ،")
    add("- أو يقع وسيطُ الرتبة المختارة في النصف الأدنى،")
    add("- أو يكون وقوعُ ما يختاره «أكبرُ ربحًا» أكثرَ من وقوع «أوّلِ رابح»،")
    add("- أو تختلف فيه `I` عن `Σ p·PMI`،")
    add("- أو تنزل نسبةُ السقف عن الواحد.")
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
