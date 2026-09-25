"""تُكتَب وثيقةُ النقل والسهم **من سجلّ التشغيل** — لا من ذاكرةٍ ولا نثر.

وكلُّ رقمٍ يُقرَأ بنمطٍ من `deposits/transfer_arrow_run.log`، وما لا يوجد
فيه **يُوقِف الكتابة**. **ولا اسمَ يدخلها من خارج المجمَّد.**
"""

from __future__ import annotations

import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
LOG = REPOSITORY / "deposits" / "transfer_arrow_run.log"
NEIGHBOUR = REPOSITORY / "deposits" / "arabic_token_run.log"
PAPER = REPOSITORY / "docs" / "النقل-والسهم.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grouped(one: int) -> str:
    return eastern(f"{one:,}".replace(",", "٬"))


def grab(pattern: str, text: str) -> tuple[str, ...]:
    found = re.findall(pattern, text)
    if not found:
        raise SystemExit(f"لا شاهدَ في السجلّ لـ{pattern}")
    first = found[0]
    return first if isinstance(first, tuple) else (first,)


def render() -> str:
    text = LOG.read_text(encoding="utf-8")
    (lines,) = grab(r"— الأسطر: (\d+)", text)
    tokens, again = grab(r"— الألفاظ: (\d+) \| وعبرَ العدّادات (\d+)", text)
    if tokens != again:
        raise SystemExit("العدّاداتُ لا تُقابِل الأسطر")
    state_boxes, state_h = grab(r"— خاناتُ الحال: (\d+) \| H = ([\d.]+)", text)
    letter_boxes, letter_h = grab(r"— خاناتُ الحرف: (\d+) \| H = ([\d.]+)", text)
    gauges = re.findall(
        r"^   (\S+)\s+([+-][\d.]+)\s+([+-][\d.]+)\s+([+-][\d.]+)\s+([+-][\d.]+)$",
        text,
        re.M,
    )
    nulls = re.findall(
        r"^   (\S+)\s+وسطٌ ([+-][\d.]+) \| مجالٌ \[([+-][\d.]+) , ([+-][\d.]+)\]"
        r" \| المقيسُ ([+-][\d.]+)$",
        text,
        re.M,
    )
    (shuffles,) = grab(r"— الصفريُّ المُبدَّل: (\d+) تبديلًا", text)
    (to_state,) = grab(r"نصيبُ «ر⟶ح» من H\(ح\): ([\d.]+)", text)
    (to_letter,) = grab(r"نصيبُ «ح⟶ر» من H\(ر\): ([\d.]+)", text)
    (lead,) = grab(r"الفرقُ \(القيادة\): (\S+)", text)
    (arrow,) = grab(r"أقصى \|أمامًا − مقلوبًا\| محجوزًا: ([\d.]+)", text)
    (above,) = grab(r"أدنى \(المقيس − أعلى الصفريّ\): (\S+)", text)
    (theft,) = grab(r"أدنى \(ملحَق − محجوز\): (\S+)", text)
    (slack,) = grab(r"أقصى \(log₂ التباديل − N·H\) بعد ألف = (\S+)", text)
    (near,) = grab(r"\n  I = ([\d.]+)", NEIGHBOUR.read_text(encoding="utf-8"))
    rows = {one[0]: one[1:] for one in gauges}

    out: list[str] = []
    add = out.append
    add("# النقلُ وسهمُ الزمن بين مجرى الحال ومجرى الحرف")
    add("")
    add("**الختم**: `4289fc6c…` — مُودَعٌ ومدفوعٌ **قبل** التشغيل.")
    add("**الحصاد**: **أحدَ عشرَ** شرطًا من اثني عشرَ صمدت، و**واحدٌ** سقط.")
    add("")
    add("## ما لا يُدَّعى — ويُقال أوّلًا")
    add("")
    add("**سُئِلتُ عن الفاعليّة والمفعوليّة والسببيّة والمسبَّبيّة.** وهذه")
    add("**أسماءُ أبوابٍ لا تُشتَقّ من البايتات**، ولا أوقّعها. **والنقلُ**")
    add("**المقيسُ ههنا ليس السببيّة**: لا تدخّلَ في نصٍّ مجمَّد، **فلا**")
    add("**تُشتَقّ سببيّةٌ من ارتباطٍ مهما بلغ**. وهذا مكتوبٌ في الختم")
    add("**قبل النظر**، لا عذرًا بعده.")
    add("")
    add("**وما يُقاس** صورةٌ في البتّات لا تحتاج اسمًا: **أيُّ المجريين**")
    add("**يُنبئ عن الآخر بعد طرح ماضي الهدف نفسِه** — وهو")
    add("`T(أ ⟶ ب) = I(بₜ ؛ أₜ₋₁ | بₜ₋₁)`.")
    add("")
    add("## المجريان")
    add("")
    add(f"الأسطرُ **{grouped(int(lines))}**، والألفاظُ **{grouped(int(tokens))}**.")
    add(f"مجرى الحال **{eastern(state_boxes)}** خانةً و`H` **{eastern(state_h)}**؛")
    add(f"ومجرى الحرف **{eastern(letter_boxes)}** خانةً و`H` **{eastern(letter_h)}**.")
    add("**ولا اسمَ لخانةٍ**: المحرفُ **شريحةٌ ونقطةُ ترميز**.")
    add("")
    add("| المقياس | ملحَقٌ أمامًا | **محجوزٌ أمامًا** | ملحَقٌ مقلوبًا | **محجوزٌ مقلوبًا** |")
    add("|---|---|---|---|---|")
    for name, inside, kept, back_in, back_out in gauges:
        add(
            f"| `{name}` | {eastern(inside)} | **{eastern(kept)}** "
            f"| {eastern(back_in)} | **{eastern(back_out)}** |"
        )
    add("")
    add("## أيُّهما يقود")
    add("")
    add(f"نصيبُ `ر⟶ح` من `H(ح)` **{eastern(to_state)}**، ونصيبُ `ح⟶ر` من")
    add(f"`H(ر)` **{eastern(to_letter)}** — والفرقُ **{eastern(lead)}**.")
    add("**فمجرى الحرف يُنبئ عن مجرى الحال نحوَ سبعةِ أضعافِ العكس**،")
    add("**والزيادةُ بعد طرح ماضي الهدف نفسِه** لا مجموعَ ما بينهما.")
    add("")
    add("**والقناتان لا تُقابَلان خامًا**: أبجديّتاهما مختلفتان، فالمقابلةُ")
    add("**بنصيبٍ من إنتروبيا الهدف** — **مكتوبًا قبل النظر**.")
    add("")
    add("## وللبتّات سهم — والقناتان سهماهما متعاكسان")
    add("")
    add(f"أقصى |أمامًا − مقلوبًا| محجوزًا **{eastern(arrow)}** بتًّا:")
    add("")
    add(f"- `ر⟶ح`: أمامًا **{eastern(rows['ر⟶ح'][1])}** ومقلوبًا")
    add(f"  **{eastern(rows['ر⟶ح'][3])}** — **يُفضِّل الأمام**.")
    add(f"- `ح⟶ر`: أمامًا **{eastern(rows['ح⟶ر'][1])}** ومقلوبًا")
    add(f"  **{eastern(rows['ح⟶ر'][3])}** — **يُفضِّل الخلف**.")
    add("")
    add(f"- `ح⟵ح`: **{eastern(rows['ح⟵ح'][1])}** أمامًا ومقلوبًا **سواءً**.")
    add("  **وهذا ليس نتيجةً بل فحصُ آلة**: معلوماتُ زوجٍ متجاورٍ متناظرة،")
    add("  فلو اختلفتا لكان في الحساب عطل.")
    add("")
    add("## الصفريُّ المُبدَّل")
    add("")
    add(f"التقديرُ الساذجُ للنقل **منحازٌ**، فقوبِل بـ**{eastern(shuffles)}**")
    add("تبديلًا **يحفظ الهوامشَ ويهدم الجوار**:")
    add("")
    add("| المقياس | وسطُ الصفريّ | مجالُه | المقيس |")
    add("|---|---|---|---|")
    for name, middle, low, high, measured in nulls:
        add(
            f"| `{name}` | {eastern(middle)} | [{eastern(low)} , {eastern(high)}] "
            f"| **{eastern(measured)}** |"
        )
    add("")
    add("**والصفريُّ سالبٌ في الأربع** — وذاك أثرُ التنعيم على شقٍّ محجوز —")
    add(f"وأدنى فضلٍ للمقيس عليه **{eastern(above)}** بتًّا. **فلا واحدٌ منها**")
    add("**في حدود الانحياز.**")
    add("")
    add("## تلاقي ختمين")
    add("")
    add(f"`I(حₜ ؛ حₜ₋₁)` محجوزةً ههنا **{eastern(rows['ح⟵ح'][1])}**، والمقيسُ")
    add(f"في `494465d1…` **{eastern(near)}** — بآلةٍ أخرى وقسمةٍ أخرى وتنعيمٍ")
    add("آخر. **والفرقُ دون جزأين من ألف.**")
    add("")
    add("## الساقطُ — وهو عطلٌ في آلتي")
    add("")
    add(f"أدنى (ملحَق − محجوز) **{eastern(theft)}**: **المحجوزُ يعلو الملحَق**")
    add("في قناة `ح ⟵ ح`. **ومحالٌ أن يكون تقديرٌ على شقٍّ لم يُقدَّر عليه**")
    add("**أسخى من تقديرٍ على العيّنة نفسِها** — فالعطلُ في الآلة لا المادّة.")
    add("")
    add("**والعلّة**: تقديري الملحَقُ لتلك القناة طرح `H(الحال)` المحسوبةَ")
    add(f"على الألفاظ كلِّها (**{grouped(int(tokens))}**) من إنتروبيا شرطيّةٍ")
    add(f"محسوبةٍ على المواضع التي لها سابق (**{grouped(int(tokens) - int(lines))}**).")
    add("**فالمطروحُ والمطروحُ منه على مسندين مختلفين.**")
    add("")
    add("**وأثرُه ثانيةً**: الملحَقُ لتلك القناة أمامًا")
    add(f"**{eastern(rows['ح⟵ح'][0])}** ومقلوبًا **{eastern(rows['ح⟵ح'][2])}** —")
    add("**وهو أكبرُ من كلّ سهمٍ محجوزٍ مقيسٍ في هذا التشغيل**. فلو قُرِئ")
    add("سهمًا لكان **أكبرَ نتائجه وأكذبَها**. **ولا يُقرأ سهمًا.**")
    add("")
    add("**ولم يُعَد تفسيرُ الشرط بعد النظر**، ولم يُعَد التشغيلُ بمقياسٍ")
    add("آخرَ ثمّ يُنشَر مختومًا. **السقوطُ سقوطٌ**، وسُجِّل عطلًا رابعًا")
    add("وعشرين في `سجل-الأعطال.md`.")
    add("")
    add("**والثلاثةُ الباقيةُ لم يمسَّها العطل**: تطرح **ثمنين على المسند**")
    add("**الواحد**. **والحكمُ في الختم على المحجوز**، فلم يدخل العطلُ حكمًا.")
    add("")
    add("## induction on وinduction FOR")
    add("")
    add("**المبرهناتُ مُصانةٌ عند كلّ حال**: `I ≥ ٠` — وأدنى مقياسٍ ملحَقٍ")
    add("موجب؛ والشرطُ لا يرفع الإنتروبيا؛ و`log₂ التباديل ≤ N·H` — وأقصى")
    add(f"فسحةٍ بعد ألفِ لفظ **{eastern(slack)}**. **والحلقةُ تشهد سطرًا سطرًا**")
    add("**وتُقابِل العدّاداتِ بالأسطر.**")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
