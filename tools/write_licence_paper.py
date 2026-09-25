"""تُكتَب وثيقةُ الترخيص **من السجلّ** لا باليد — فلا صورةَ عربيّةٌ تُطبَع.

كلُّ رقمٍ وكلُّ صورةٍ في الوثيقة مقتطعةٌ من `deposits/greedy_licence_run.log`
و`deposits/greedy_licence_refusal.log` بنمطٍ صريح. وما لم يُوجَد في السجلّ
**لا يُكتَب**.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
RUN = REPOSITORY / "deposits" / "greedy_licence_run.log"
REFUSAL = REPOSITORY / "deposits" / "greedy_licence_refusal.log"
PAPER = REPOSITORY / "docs" / "الترخيص-بتّةً-بتّة.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: str) -> str:
    return one.translate(EASTERN)


def grouped(one: str) -> str:
    return eastern(f"{int(one):,}".replace(",", "٬"))


def mixed(one: str) -> str:
    """رقمٌ بكسرٍ: صحيحُه مجمَّعٌ وكسرُه شرقيّ."""

    whole, _, part = one.partition(".")
    return f"{grouped(whole)}٫{eastern(part)}" if part else grouped(whole)


def grab(text: str, pattern: str) -> tuple[str, ...]:
    found = re.search(pattern, text, re.MULTILINE)
    if found is None:
        raise SystemExit(f"لا مطابقَ في السجلّ: {pattern}")
    return found.groups()


def render() -> str:
    """نصُّ الوثيقة — يُبنى من السجلّ وحدَه فيُقارَن به المكتوب."""

    run = RUN.read_text(encoding="utf-8")
    refusal = REFUSAL.read_text(encoding="utf-8")

    (units, alphabet, verses) = grab(
        run, r"^L₀: (\d+) وحدةً \| أبجديّة (\d+) \| آيات (\d+)$"
    )
    (zero,) = grab(run, r"^نقطةُ الصفر: الجملة (\d+) ")
    (stop,) = grab(run, r"^الوقوف: (.+)$")
    (proposals, commits, refused, first) = grab(
        run,
        r"^  اقتراحاتٌ (\d+) \| التزاماتٌ (\d+) \| مرفوضاتٌ (\d+) "
        r"\| أوّلُ رفضٍ بعد (\d+) التزامًا$",
    )
    (rises,) = grab(run, r"^  التزاماتٌ بفرقٍ غيرِ سالب: (\d+)$")
    (drift,) = grab(run, r"^  أقصى انحرافٍ بين الآلتين عند نقاط الفحص: ([\d.]+)$")
    (total, ratio, inside, gap) = grab(
        run,
        r"^  الجملة (\d+) \| النسبةُ إلى L₀ ([\d.]+) \| الملحَقة (\d+) "
        r"\| فرقٌ \+(\d+)$",
    )
    (back,) = grab(run, r"^  الرجعة: مواضعُ الخلاف بين بسطِ الرموز ومجرى L₀ = (\d+)$")
    (clean, crossed, share) = grab(
        run, r"^  لا يعبر الفراغَ: (\d+) من (\d+) = ([\d.]+)$"
    )
    (symbols, mass) = grab(run, r"^    الجملة: رموزٌ (\d+) \| وقوعاتٌ (\d+)$")

    (at, left, right) = grab(
        refusal, r"^— الرفضُ عند الاقتراح (\d+): الزوجُ \((\d+), (\d+)\) \| عَرضٌ 2$"
    )
    (even, odd) = grab(refusal, r"^  استبدالاتُه شفعًا (\d+) ووترًا (\d+)$")
    (shapes,) = grab(refusal, r"^  بايتاتُ طرفيه: (.+)$")
    (rise,) = grab(refusal, r"^  الفرقُ من الآيات   \+([\d.]+)$")
    (mirror,) = grab(refusal, r"^  الفرقُ من العدّادات \+([\d.]+)$")
    (book_before, book_after, book_delta) = grab(
        refusal, r"^  المعجم ([\d.]+) ⟶ ([\d.]+) \(\+([\d.]+)\)$"
    )
    (data_before, data_after, data_delta) = grab(
        refusal, r"^  البيان ([\d.]+) ⟶ ([\d.]+) \(\+([\d.]+)\)$"
    )
    (count_before, count_after, count_delta) = grab(
        refusal, r"^  العدد  (\d+) ⟶ (\d+) \(-(\d+)\)$"
    )
    (per_before, per_after, per_delta) = grab(
        refusal, r"^  طولُ الرمز ([\d.]+) ⟶ ([\d.]+) \(\+([\d.]+)\)$"
    )
    (takes,) = grab(refusal, r"^وهي الزوجُ الذي رفضه الترخيص: (\w+)$")
    (mass_left, code_left) = grab(refusal, r"^قبلُ: وقوعُ الأوّل (\d+) بشفرةٍ (\d+) بتًّا$")
    (mass_right, code_right) = grab(
        refusal, r"^      وقوعُ الثاني (\d+) بشفرةٍ (\d+) بتًّا$"
    )
    (pair_price,) = grab(refusal, r"^      فثمنُ الزوج معًا (\d+) بتًّا للوقوع")
    (born_mass, born_code) = grab(refusal, r"^بعدُ: وقوعُ المولود (\d+) بشفرةٍ (\d+) بتًّا$")
    (on_pair,) = grab(refusal, r"^  فالفرقُ على الاستبدالات وحدَها -(\d+)$")
    (others_before, others_after, others_delta) = grab(
        refusal, r"^  سائرُ الرموز: (\d+) ⟶ (\d+) \(\+(\d+)\)$"
    )
    (kept_delta,) = grab(refusal, r"^  الطرفان فيما لم يُستبدَل: \d+ ⟶ \d+ \(\+(\d+)\)$")

    widths = re.findall(
        r"^    عَرضُ (\d+): رموزٌ (\d+) \| وقوعاتٌ (\d+) \| نصيبٌ ([\d.]+)$",
        run,
        re.MULTILINE,
    )
    refusals = re.findall(r"^    عَرضُ (\d+): مرفوضاتٌ (\d+)$", run, re.MULTILINE)
    (low, middle, high) = grab(
        refusal if False else run,
        r"^    استبدالاتُ المرفوض: أدنى (\d+) \| وسيطٌ (\d+) \| أعلى (\d+)$",
    )
    top = re.findall(r"^    (\S+)  \((\d+)\) وحداتُه (\d+)$", run, re.MULTILINE)

    lines: list[str] = []
    add = lines.append
    add("# الترخيصُ الجشع بتّةً بتّة — أربعةٌ من سبعة، والثلاثةُ الساقطةُ دعاوايَ")
    add("")
    add("**الختم**: `69a1c10c…` — مُودَعٌ ومدفوعٌ **قبل** التشغيل.")
    add(
        f"**المدوّنة**: البصمة `37633090…` — {grouped(units)} وحدةً "
        f"في {grouped(verses)} آيةً على أبجديّة {grouped(alphabet)}."
    )
    add("")
    add("## ١) ما جرى")
    add("")
    add("الرخصةُ في `34133d54…` كانت **كتلةً** — كلَّ خمس مئةِ دمجة. وههنا")
    add("**للدمجة الواحدة**: تُقاس التكلفةُ المحجوزةُ قبلها وبعدها، فتُلتزَم إن")
    add("نزلت، وتُرفَض وتُوسَم **ولا تُعاد** إن لم تنزل.")
    add("")
    add(f"- **الوقوف**: {eastern(stop)}.")
    add(
        f"- اقتراحاتٌ **{grouped(proposals)}** ⟵ التزاماتٌ **{grouped(commits)}** "
        f"ومرفوضاتٌ **{grouped(refused)}**."
    )
    add(f"- أوّلُ رفضٍ بعد **{grouped(first)}** التزامًا فقط.")
    add(f"- التزاماتٌ لم تنزل عندها التكلفة: **{grouped(rises)}**.")
    add(f"- انحرافُ الآلتين عند نقاط الفحص: **{eastern(drift)}**.")
    add(f"- الرجعة: مواضعُ الخلاف بين بسطِ الرموز ومجرى L₀ = **{grouped(back)}**.")
    add("")
    add("## ٢) الحكمُ على الشروط السبعة")
    add("")
    add("| الشرط | الحدّ | المقيس | الحكم |")
    add("|---|---|---|---|")
    add(f"| ر١ انحرافُ الآلتين | ≤ ٠٫٠٠١ | {eastern(drift)} | **مستوفًى** |")
    add(f"| ر٢ رجعةُ البسط إلى L₀ | ≤ ٠ | {grouped(back)} | **مستوفًى** |")
    add(f"| ر٣ التزامٌ بلا نزول | ≤ ٠ | {grouped(rises)} | **مستوفًى** |")
    add(f"| ر٤ الالتزامات | ≥ ٤٬٥٠١ | {grouped(commits)} | **منقوض** |")
    add(f"| ر٥ الالتزاماتُ قبل أوّل رفض | ≤ ٤٬٥٠٠ | {grouped(first)} | **مستوفًى** |")
    add(f"| ر٦ النسبةُ إلى L₀ | ≤ ٠٫٦٨٢ | {eastern(ratio)} | **منقوض** |")
    add(f"| ر٧ ما لا يعبر الفراغ | ≤ ٠٫٨٣٧٩ | {eastern(share)} | **منقوض** |")
    add("")
    add("**والثلاثةُ الساقطةُ دعاوايَ أنا** — لا الآلةَ ولا المادّة. والأربعةُ")
    add("الصامدةُ ثلاثةٌ منها فحصُ آلةٍ لا تقول عن المادّة شيئًا.")
    add("")
    add("## ٣) المقابلةُ بالكتليّ")
    add("")
    add("| | الكتليُّ `34133d54…` | الترخيصُ بتّةً بتّة |")
    add("|---|---|---|")
    add("| الدمجات | ٤٬٥٠٠ | " + grouped(commits) + " |")
    add("| الرموز | ٤٬٥٣٨ | " + grouped(symbols) + " |")
    add("| الوقوعات | ١١٠٬٩٩٤ | " + grouped(mass) + " |")
    add("| الجملةُ المحجوزة | ١٬٣٩٤٬٦٣٨ | " + grouped(total) + " |")
    add("| النسبةُ إلى L₀ | ٠٫٦٨٢١ | " + eastern(ratio) + " |")
    add("| لا يعبر الفراغ | ٠٫٨٣٧٩ | " + eastern(share) + " |")
    add("")
    add("**فالترخيصُ بتّةً بتّة يخسر الضغطَ ويكسب البنية**: أغلى بـ")
    add(f"**{grouped(str(int(total) - 1_394_638))}** بتًّا (٠٫٤١٪)، وأصغر بـ")
    add(
        f"**{grouped(str(4_538 - int(symbols)))}** رمزًا، "
        f"و**{eastern(f'{float(share) - 0.8379:+.4f}')}** في حفظ الفراغ."
    )
    add("")
    add("## ٤) أوّلُ رفضٍ — مفصولًا بتًّا بتًّا")
    add("")
    add(f"عند الاقتراح **{grouped(at)}** رُفِض زوجٌ عَرضُه ٢، طرفاه بالبايتات")
    add(f"**{shapes}**، واستبدالاتُه **{grouped(even)}** شفعًا و**{grouped(odd)}**")
    add(f"وترًا — **{grouped(str(int(even) + int(odd)))}** جملةً.")
    add("")
    add("| المقدار | قبلُ | بعدُ | الفرق |")
    add("|---|---|---|---|")
    add(
        f"| المعجم | {eastern(book_before)} | {eastern(book_after)} "
        f"| {eastern('+' + book_delta)} |"
    )
    add(
        f"| البيان | {mixed(data_before)} | {mixed(data_after)} "
        f"| {eastern('+' + data_delta)} |"
    )
    add(
        f"| عددُ الرموز | {grouped(count_before)} | {grouped(count_after)} "
        f"| {eastern('−') + grouped(count_delta)} |"
    )
    add(
        f"| طولُ الرمز | {eastern(per_before)} | {eastern(per_after)} "
        f"| {eastern('+' + per_delta)} |"
    )
    add("")
    add("**وأين ذهب البتُّ؟ يُقاس لا يُستنتَج**:")
    add("")
    add("| الوجه | البتّات |")
    add("|---|---|")
    add(
        f"| ثمنُ الطرفين معًا قبلُ | {grouped(code_left)} + {grouped(code_right)} "
        f"= **{grouped(pair_price)}** للوقوع |"
    )
    add(f"| ثمنُ المولود بعدُ | **{grouped(born_code)}** للوقوع |")
    add(f"| فالوفرُ على الاستبدالات وحدَها | **{eastern('−') + grouped(on_pair)}** |")
    add(f"| وما حُمِّله سائرُ الرموز | **{eastern('+') + grouped(others_delta)}** |")
    add(f"| والطرفان فيما لم يُستبدَل | {eastern('+') + grouped(kept_delta)} |")
    add(f"| والمعجم | {eastern('+' + book_delta)} |")
    add("")
    add("**فالدمجةُ تربح على وقوعاتها وتخسر على غيرها**: الاستبدالاتُ توفّر")
    add(f"**{grouped(on_pair)}** بتًّا حقًّا، غير أنّ إدخالَ رمزٍ جديدٍ في الشفرة")
    add(f"يطيل شفراتِ سواه فيكلّف **{grouped(others_delta)}** — **والطرفان")
    add(f"نفساهما لم يتغيّر ثمنُهما** ({grouped(code_left)} و{grouped(code_right)}")
    add("قبلُ وبعدُ، وما لم يُستبدَل منهما بفرقٍ صفر).")
    add("")
    add("**فليس الحدُّ من المادّة بل من الشفرة**: فضاءُ الشفرات محدودٌ")
    add("بمتراجحة كرافت، وكلُّ رمزٍ يُدخَل يقتطع منه — فيدفع الثمنَ من لا")
    add("ناقةَ له فيه ولا جمل.")
    add("")
    add(
        f"والفرقُ **{eastern('+' + rise)}** بتًّا — مقيسًا من الآيات، "
        f"و**{eastern('+' + mirror)}** من العدّادات، وهما رقمٌ واحد."
    )
    add("")
    add(
        "**والصعودُ الكتليُّ يلتزم هذا الزوجَ بعينه** "
        f"({'نعم' if takes.lower() == 'true' else 'لا'} — مقيسًا):"
    )
    add("فالآلتان تقترحانه سواءً، وتلتزمه الكتلةُ لأنّها لا ترخّص، ويرفضه")
    add("الترخيص.")
    add("")
    add("**وما لم يُقَس**: أنّ هذه الدمجةَ بعينها **درجةٌ** لِما فوقها. المقيسُ")
    add("أنّ الكتليَّ يلتزمها وينتهي أرخص؛ **ولم يُعزَل أثرُها وحدَها**، فنسبةُ")
    add("الفرق إليها **استنتاجٌ لا قياس**، ويُوسَم كذلك حتّى يُعزَل بختمٍ خاصّ.")
    add("")
    add("## ٥) المجموعةُ المولَّدةُ مقسومةً بالعَرض")
    add("")
    add("| عَرض | رموز | وقوعات | نصيب |")
    add("|---|---|---|---|")
    for width, kinds, number, part in widths:
        add(
            f"| {grouped(width)} | {grouped(kinds)} | {grouped(number)} "
            f"| {eastern(part)} |"
        )
    add("")
    add("## ٦) المرفوضاتُ مقسومةً بالعَرض")
    add("")
    add("| عَرض | مرفوضات |")
    add("|---|---|")
    for width, number in refusals:
        add(f"| {grouped(width)} | {grouped(number)} |")
    add("")
    add(f"واستبدالاتُ المرفوض: أدنى **{grouped(low)}**، ووسيطٌ **{grouped(middle)}**،")
    add(f"وأعلى **{grouped(high)}**. **فالمرفوضُ نادرٌ عريض** — وهو نفسُه ما")
    add("يعبر الفراغَ؛ ولذلك ارتفع حفظُ الفراغ حين رُفِض.")
    add("")
    add("## ٧) أكثرُ الرموز وقوعًا — ببايتاتها من المصحف")
    add("")
    add("| رمز | وقوعات | عَرض |")
    add("|---|---|---|")
    for shape, number, width in top:
        add(f"| **{shape}** | {grouped(number)} | {grouped(width)} |")
    add("")
    add("**ولا عمودَ رابع**: لا يُعرَف لهذه البايتات اسمٌ ولا وظيفة.")
    add("")
    add("## ٨) ما يُستفاد")
    add("")
    add(
        "**١.** الترخيصُ بتّةً بتّة **مُحقَّق**: لا التزامَ واحدٌ بلا نزول، "
        f"والرجعةُ **{grouped(back)}**."
    )
    add("")
    add(
        "**٢.** وهو **ليس أمثلَ**: الخسارةُ مقيسةٌ "
        f"(**{grouped(str(int(total) - 1_394_638))}** بتًّا) — وسببُها المقترَح،"
    )
    add("أنّ الوسمَ الأبديَّ يقطع الطريقَ إلى ما فوق المرفوض، **غيرُ معزولٍ بعد**.")
    add("")
    add("**٣.** ودعوايَ الثالثةُ سقطت **معكوسةً**: ظننتُ الرخصةَ تشتري الضغطَ")
    add(f"بعبورٍ أكثر، والمقيسُ أنّها تحفظ الفراغَ **أكثر** — {eastern(share)}.")
    add("")
    add("**٤.** وهذا حدٌّ على **الجشع** لا على المادّة: أن يكون الاختيارُ")
    add("محلّيًّا أمثلَ لا يجعل المسارَ أمثل، ولا يُعرَف الأمثلُ من ههنا.")
    add("")
    return "\n".join(lines) + "\n"


def main() -> int:
    text = render()
    PAPER.write_text(text, encoding="utf-8")
    print(f"كُتِبت {PAPER.relative_to(REPOSITORY)} — {len(text.splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    sys.exit(main())
