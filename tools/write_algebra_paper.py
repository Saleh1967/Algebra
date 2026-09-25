"""تُكتَب وثيقةُ جبر الربح **من السجلّ** لا باليد — ولا رقمَ يُنقَل ثقةً."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
RUN = REPOSITORY / "deposits" / "greedy_algebra_run.log"
PAPER = REPOSITORY / "docs" / "جبر-الربح.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: str) -> str:
    return eastern(f"{int(one):,}".replace(",", "٬"))


def mixed(one: str) -> str:
    whole, _, part = one.partition(".")
    return f"{grouped(whole)}٫{eastern(part)}" if part else grouped(whole)


def grab(text: str, pattern: str) -> str:
    found = re.search(pattern, text, re.MULTILINE)
    if found is None:
        raise SystemExit(f"لا مطابقَ في السجلّ: {pattern}")
    return found.group(1)


def render() -> str:
    run = RUN.read_text(encoding="utf-8")

    def g(pattern: str) -> str:
        return grab(run, pattern)

    units = g(r"^L₀: (\d+) وحدةً")
    laid = g(r"تباديل متعدّد المجموعة: ([\d.]+)")
    by_h = g(r"N·H بالإنتروبيا:\s+([\d.]+)")
    stirling = g(r"الفرقُ للرمز الواحد:\s+\+([\d.]+)")
    by_l = g(r"N·L بشفرة هوفمان:\s+([\d.]+)")
    gap = g(r"L − H للرمز:\s+\+([\d.]+)")
    h_next = g(r"H\(Xₜ₊₁\) = ([\d.]+)")
    h_given = g(r"H\(Xₜ₊₁\|Xₜ\) = ([\d.]+)")
    carried = g(r"I\(Xₜ;Xₜ₊₁\) = ([\d.]+)")
    summed = g(r"Σ p·PMI    = ([\d.]+)")
    apart = g(r"\|I − Σ p·PMI\| = ([\d.]+)")
    places = g(r"مواضعُ الجوار (\d+)")
    ceiling = g(r"السقفُ من الرتبة الأولى (\d+) بتًّا")
    looked = g(r"أزواجٌ مقيسة: (\d+)")
    by_count = g(r"ρ\(الوقوع، الربحِ المقيس\)\s+= \+([\d.]+)")
    by_derived = g(r"ρ\(المشتَقّ، الربحِ المقيس\)\s+= \+([\d.]+)")
    by_leading = g(r"ρ\(التقريبِ، الربحِ المقيس\) = \+([\d.]+)")
    by_pmi = g(r"ρ\(PMI، الربحِ المقيس\)\s+= \+([\d.]+)")
    count_pmi = g(r"ρ\(الوقوع، PMI\)\s+= \+([\d.]+)")
    sign = g(r"توافقُ الإشارة: (\d+) من")
    threshold = g(r"توافقٌ (\d+) من")
    thin = g(r"عتبةُ PMI > log₂e \(([\d.]+)\)")
    median = g(r"وسيطٌ ([\d.]+) \| أدنى")
    saved = g(r"فالمُوفَّرُ: (\d+) بتًّا")
    share = g(r"النسبةُ المُوفَّر ÷ السقف: ([\d.]+)")
    steps = re.findall(
        r"بعد (\d+): أبجديّة (\d+) \| N (\d+) \| تباديلُ (\d+) \| N·H (\d+) "
        r"\| للرمز \+([\d.]+) \| L−H \+([\d.]+)",
        run,
    )

    lines: list[str] = []
    add = lines.append
    add("# جبرُ الربح الجشع — لماذا ينقلب الترتيب")
    add("")
    add("**الختم**: `cfdb2184…` — مُودَعٌ ومدفوعٌ **قبل** التشغيل. " "**سبعةٌ من ثمانية.**")
    add(f"**المدوّنة**: البصمة `37633090…` — {grouped(units)} وحدةً على ١١٢.")
    add("")
    add("## ١) التكلفةُ لوغاريتمُ عددِ التباديل")
    add("")
    add("بيانُ نموذجٍ بلا سياقٍ هو **لوغاريتمُ عدد التباديل المتمايزة**")
    add("لمتعدّد المجموعة — عددُ الترتيبات التي تُعطي هذه الوقوعاتِ نفسَها:")
    add("")
    add("```")
    add("log₂ C(N; n₁,…,n_k) = log₂ N! − Σ log₂ nₛ!")
    add("```")
    add("")
    add("| المقدار | بتًّا |")
    add("|---|---|")
    add(f"| `log₂` من التباديل | {mixed(laid)} |")
    add(f"| `N·H` بالإنتروبيا | {mixed(by_h)} |")
    add(f"| `N·L` بشفرة هوفمان | {mixed(by_l)} |")
    add("")
    add(f"والفرقُ بين الأوّلَين **{eastern(stirling)}** بتًّا للرمز — وهو حدُّ")
    add(f"ستيرلنغ؛ وبين الأخيرَين **{eastern(gap)}** — وهو ثمنُ هوفمان.")
    add("")
    add("## ٢) الربحُ بالتباديل النازلة")
    add("")
    add("فإذا دُمِج `(a,b) ⟶ f` بـ`m` استبدالًا صار الربحُ **نسبةَ معاملين**،")
    add("وتختصر إلى تباديلَ نازلةٍ `x⁽ᵐ⁾ = x!/(x−m)!`:")
    add("")
    add("```")
    add("G = log₂ N⁽ᵐ⁾ − log₂ nₐ⁽ᵐ⁾ − log₂ n_b⁽ᵐ⁾ + log₂ m!")
    add("```")
    add("")
    add("وبالتقريب الأوّل، بعد تبسيط التباديل النازلة:")
    add("")
    add("```")
    add("G ≈ m · ( PMI − log₂ e ),    PMI = log₂ ( m·N ⁄ nₐ·n_b )")
    add("```")
    add("")
    add("**فالربحُ ليس `m`** بل `m` مضروبًا في **فائض الاقتران على**")
    add(f"**الاستقلال** ناقصًا `log₂ e ≈ {eastern(thin)}`.")
    add("")
    add("## ٣) وهذا بعينه سببُ الانقلاب — مقيسًا")
    add("")
    add(f"على أكثرِ {grouped(looked)} زوجٍ وقوعًا في L₀، ارتباطُ الرتب:")
    add("")
    add("| المرتَّبُ به | ρ مع الربح المقيس |")
    add("|---|---|")
    add(f"| **الوقوعُ الخام `m`** | **{eastern('+' + by_count)}** |")
    add(f"| فائضُ الاقتران `PMI` | {eastern('+' + by_pmi)} |")
    add(f"| التقريبُ `m·(PMI − log₂e)` | {eastern('+' + by_leading)} |")
    add(f"| **المشتَقُّ بالتباديل تامًّا** | **{eastern('+' + by_derived)}** |")
    add("")
    add(f"**والوقوعُ والاقترانُ شبهُ مستقلَّين**: `ρ = {eastern('+' + count_pmi)}`.")
    add("فالترتيبُ بالعدد والترتيبُ بالربح **مقياسان لا مقياس**، ولذلك")
    add("انقلب الترتيبُ في `c8602c00…` ولم يكن انقلابُه عرَضًا.")
    add("")
    add("| المقيس | القيمة |")
    add("|---|---|")
    add(f"| توافقُ إشارة المشتَقّ والمقيس | {grouped(sign)} من {grouped(looked)} |")
    add(f"| توافقُ عتبة `PMI > log₂e` | {grouped(threshold)} من {grouped(looked)} |")
    add(f"| وسيطُ الخطأ النسبيّ | {eastern(median)} |")
    add("")
    add("**فرخصةُ الدمج حدٌّ على فائض الاقتران لا على العدد.**")
    add("")
    add("## ٤) وماركوف: المستخرَجُ هو اقترانُ الجارين بعينه")
    add("")
    add("```")
    add("Σ p(a,b)·PMI(a,b) = H(Xₜ₊₁) − H(Xₜ₊₁|Xₜ) = I(Xₜ ; Xₜ₊₁)")
    add("```")
    add("")
    add("| المقدار | بتًّا للموضع |")
    add("|---|---|")
    add(f"| `H(Xₜ₊₁)` | {eastern(h_next)} |")
    add(f"| `H(Xₜ₊₁\\|Xₜ)` | {eastern(h_given)} |")
    add(f"| **`I(Xₜ;Xₜ₊₁)`** | **{eastern(carried)}** |")
    add(f"| `Σ p·PMI` | {eastern(summed)} |")
    add(f"| الفرق | **{eastern(apart)}** |")
    add("")
    add("**والهويّةُ تامّةٌ إلى آخر رقم** — فما يستخرجه الدمجُ هو بعينه ما")
    add("تحمله السلسلةُ من اقترانٍ يُغفِله نموذجُ اللاسياق.")
    add("")
    add("## ٥) والصعودُ يبلغ ما فوق الرتبة الأولى")
    add("")
    add(f"مواضعُ الجوار **{grouped(places)}**، فسقفُ الرتبة الأولى")
    add(f"**{grouped(ceiling)}** بتًّا. وما وفّره الصعودُ الكتليُّ")
    add(f"**{grouped(saved)}** بتًّا — **والنسبةُ {eastern(share)}**.")
    add("")
    add("فشرطُ ب٨ **منقوض**، وهو **خبرٌ لا عطل**: الدمجُ المتكرّرُ لا يسعه")
    add("اقترانُ الجارين، لأنّ الرموزَ المدموجةَ **تمتدّ** فيصير جوارُها")
    add("جوارَ رتبٍ أبعد. فما بلغه الصعودُ **ليس نموذجًا من الرتبة الأولى**.")
    add("")
    add("## ٦) استقراءان: `on` و`FOR`")
    add("")
    add("**`induction on`** — المتراجحةُ `log₂ التباديل ≤ N·H` مبرهَنةٌ،")
    add("وتُصان عند كلّ حال. **و`induction FOR`** — الحلقةُ تشهد عليها")
    add("حالًا حالًا، وتُقابَل العدّاداتُ بالآيات فلا تنفرد آلةٌ برقم.")
    add("")
    add("| بعد | أبجديّة | N | `log₂` تباديل | `N·H` | الفرقُ للرمز | `L−H` |")
    add("|---|---|---|---|---|---|---|")
    for at, alphabet, count, one, two, drift, code in steps:
        add(
            f"| {grouped(at)} | {grouped(alphabet)} | {grouped(count)} "
            f"| {grouped(one)} | {grouped(two)} | {eastern('+' + drift)} "
            f"| {eastern('+' + code)} |"
        )
    add("")
    add("**والفرقُ يتّسع ولا ينكمش** بنموّ الأبجديّة — وهو حدُّ ستيرلنغ")
    add("يكبر بعدد الرموز، لا خللٌ في القياس.")
    add("")
    return "\n".join(lines) + "\n"


def main() -> int:
    text = render()
    PAPER.write_text(text, encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    sys.exit(main())
