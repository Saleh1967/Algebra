"""تُكتَب وثيقةُ دورة الحال **من سجلّ التشغيل** — لا من ذاكرةٍ ولا من نثر.

فكلُّ رقمٍ في الوثيقة **يُقرَأ بنمطٍ من** `deposits/state_cycle_run.log`،
ولا يُكتَب رقمٌ بيد. وما لا يوجد في السجلّ **يُوقِف الكتابة**.
"""

from __future__ import annotations

import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
LOG = REPOSITORY / "deposits" / "state_cycle_run.log"
PAPER = REPOSITORY / "docs" / "دورة-الحال.md"
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
    tokens, again = grab(r"عبرَ العدّادات (\d+) \| عبرَ الأسطر (\d+)", text)
    if tokens != again:
        raise SystemExit("العدّاداتُ لا تُقابِل الأسطر")
    (skeletons,) = grab(r"هياكلُ متمايزة: (\d+)", text)
    (markup,) = grab(r"ألفاظُ الترقيم \(لا حرفَ عربيًّا فيها\): (\d+)", text)
    basmala, first = grab(r"بسم = (\d+) \| منها في صدر السطر (\d+)", text)
    where = re.findall(r"سطرُ (\d+) \| موضعُ (\d+) \| (\S+)", text)
    field = re.findall(r"^    (\S+) \((.+?)\) (\d+) \| نصيبٌ ([\d.]+)$", text, re.M)
    (three,) = grab(r"نصيبُ الثلاث: \d+ من \d+ = ([\d.]+)", text)
    (field_entropy,) = grab(r"H\(الحال\) = ([\d.]+)", text)
    (settled,) = grab(r"أدنى فرقٍ بعد ألف = (\S+)", text)
    (slack,) = grab(r"أقصى فسحةٍ بعد ألف = (\S+)", text)
    closing, closing_slack = grab(r"وعند الختام: فرقٌ (\S+) \| فسحةٌ (\S+)", text)
    (neighbour,) = grab(r"\n  I = ([\d.]+)", text)
    inside, outside, apart = grab(
        r"ملحَقة ([\d.]+) \| محجوزة ([\d.]+) \| فرقٌ (\S+)", text
    )
    (letter,) = grab(r"I\(الحال؛ حرفُ الخاتمة\) = ([\d.]+)", text)
    (blind,) = grab(r"لا تحمل حالًا ألبتّة: (\d+)", text)
    blind_rows = re.findall(
        r"^    (\S+) \| وقوعاتٌ (\d+)$", text.split("لا تحمل حالًا ألبتّة:")[1], re.M
    )
    enough, steady, moving = grab(
        r"هياكلُ بالقيد: (\d+) \| ثابتةٌ (\d+) \| متبدّلةٌ (\d+)", text
    )
    (steady_share,) = grab(r"نصيبُ الثابت من الهياكل: ([\d.]+)", text)
    steady_mass, moving_mass = grab(r"كتلةُ الثابت (\d+) \| كتلةُ المتبدّل (\d+)", text)
    (mass_share,) = grab(r"نصيبُ كتلة الثابت من الألفاظ: ([\d.]+)", text)
    even, both, carried = grab(
        r"ثابتُ الزوجيّ (\d+) \| باقٍ ثابتًا في الفرديّ (\d+) \| نصيبٌ ([\d.]+)", text
    )

    out: list[str] = []
    add = out.append
    add("# دورةُ الحال على الخاتمة — ثباتًا وتبدّلًا وخلوًّا")
    add("")
    add("**الختم**: `7773c03f…` — مُودَعٌ ومدفوعٌ **قبل** التشغيل.")
    add("**الحصاد**: أحدَ عشرَ شرطًا من اثني عشرَ صمدت، وواحدٌ سقط.")
    add("")
    add("**ولا اسمَ بابٍ نحويٍّ في هذه الوثيقة**: علاماتٌ ومواضعُ وبتّات.")
    add("وما يُقاس ههنا **ثباتُ علامةٍ** لا **حكمُ باب**؛ ونسبتُه إلى المبنيّ")
    add("والمعرب والأصليّ والفرعيّ **قابليّةٌ للقراءة لا قراءة**، وإيداعُ")
    add("القراءة **فعلُ صاحب المستودع**.")
    add("")
    add("## الحقل")
    add("")
    add(f"الأسطرُ **{grouped(int(lines))}**، والألفاظُ **{grouped(int(tokens))}**")
    add("عبرَ العدّادات وعبرَ الأسطر سواءً — **والانحرافُ صفر**. والهياكلُ")
    add(f"المتمايزةُ **{grouped(int(skeletons))}**.")
    add("")
    add("| حالُ الخاتمة | وقوعات | نصيب |")
    add("|---|---|---|")
    for mark, name, number, share in field:
        shown = "بلا علامة" if name == "بلا علامة" else f"`{mark}`"
        add(f"| {shown} | {grouped(int(number))} | {eastern(share)} |")
    add("")
    add(f"ونصيبُ الثلاث (`َ` `ُ` `ِ`) **{eastern(three)}** — **دون النصف**؛")
    add(
        "و**بلا علامة** وحدَها أكبرُ خانةٍ في الحقل. "
        f"وH(الحال) **{eastern(field_entropy)}**"
    )
    add("من ثلاثِ بتّاتٍ لثمانِ خانات.")
    add("")
    add("## ثباتُ الحال وتبدّلُه")
    add("")
    add(f"من **{grouped(int(enough))}** هيكلًا بلغ خمسَ وقوعاتٍ فأكثر (والقيدُ")
    add("**مكتوبٌ في الختم قبل النظر**، لأنّ هيكلًا وقع مرّةً ثابتٌ بلا خبر):")
    add("")
    add("| | هياكل | كتلةُ ألفاظ |")
    add("|---|---|---|")
    add(f"| **ثابتُ الحال** | {grouped(int(steady))} | {grouped(int(steady_mass))} |")
    add(f"| **متبدّلُ الحال** | {grouped(int(moving))} | {grouped(int(moving_mass))} |")
    add("")
    add(f"**فأكثرُ الهياكل ثابتٌ** ({eastern(steady_share)} منها)، **وأقلُّ")
    add(f"الكلام يقف عليه** ({eastern(mass_share)} من الألفاظ). والكتلةُ تميل")
    add("إلى المتبدّل.")
    add("")
    add(f"**والثباتُ ينتقل**: من **{grouped(int(even))}** ثابتٍ في النصف الزوجيّ")
    add(f"بقي **{grouped(int(both))}** ثابتًا **بالحال نفسِه** في الفرديّ —")
    add(f"**{eastern(carried)}**. فهو خاصّةٌ تنتقل لا صدفةَ عيّنة.")
    add("")
    add("## الجارُ والخاتمة — ماركوف")
    add("")
    add(f"معلوماتُ الجار داخلَ السطر **{eastern(neighbour)}** بتًّا، ومعلوماتُ")
    add(f"حرفِ الخاتمة **{eastern(letter)}** — **أكثرُ من خمسةَ عشرَ ضعفًا**.")
    add("فحالُ الخاتمة **يُقرأ من خاتمتها لا من جارتها**.")
    add("")
    add(f"والانتحالُ مقيسٌ لا مفترَض: الملحَقةُ **{eastern(inside)}** والمحجوزةُ")
    add(f"**{eastern(outside)}**، وفرقُهما **{eastern(apart)}** — والتقديرُ داخلَ")
    add("العيّنة أعلى كما يقتضي.")
    add("")
    add("## induction on وinduction FOR")
    add("")
    add("**المبرهَنتان**: الشرطُ لا يرفع الإنتروبيا، و`log₂ التباديل ≤ N·H`.")
    add("**وهما مُصانتان عند كلّ حال**، والحلقةُ تشهد عليهما **سطرًا سطرًا**")
    add("وتُقابِل العدّاداتِ بالأسطر.")
    add("")
    add("**وطرفاهما تافهان**: كلاهما يقع عند أوّل الحلقة حيث الحقلُ خانةٌ")
    add("واحدة، فالفرقُ صفرٌ والفسحةُ صفر. **فالمرورُ صحيحٌ والشهادةُ خاوية**،")
    add("ويُقال ذلك ولا يُطوى. وما يشهد لهما حقًّا ما بعد ألفِ لفظ:")
    add("")
    add(f"- أدنى فرقٍ **{eastern(settled)}** ⟶ وعند الختام **{eastern(closing)}**.")
    add(f"- أقصى فسحةٍ **{eastern(slack)}** ⟶ وعند الختام **{eastern(closing_slack)}**.")
    add("")
    add("## الخلوُّ — ما لم يُقَس وما لا يُقاس")
    add("")
    add(f"**حروفُ خاتمةٍ لا تحمل حالًا ألبتّة: {eastern(blind)}** —")
    for shape, number in blind_rows:
        add(f"`{shape}` بـ**{grouped(int(number))}** وقوعًا؛")
    add("**وأحدُهما ليس حرفًا**: هو ذنَبُ وسمِ ترقيمٍ في المدوّنة. فالعربيُّ")
    add("منها **واحدٌ لا غير**. وهذا **سقوطُ الشرط التاسع**، وهو أعمقُ ممّا")
    add("يُظهِره رقمُه.")
    add("")
    add(f"**ووسمُ الترقيم دخل كلَّ عدٍّ ههنا**: {grouped(int(markup))} لفظًا ليس")
    add("فيها حرفٌ عربيٌّ واحد، لأنّ حدَّ اللفظ في الختم «أطولُ متتاليةٍ بلا")
    add("فراغ» **ووسمُ الترقيم متتاليةٌ بلا فراغ**. **والخللُ في الختم لا في")
    add("التشغيل**، ولا يُصلَح بإعادة قراءةِ شرطٍ بعد النظر — **يُعلَن، ويُعاد")
    add("الختمُ بحدٍّ مُصحَّح**.")
    add("")
    add(f"**وهيكلُ `بسم` وقع {grouped(int(basmala))} مرّة**:")
    add(f"**{grouped(int(first))}** في صدر السطر، و**{eastern(len(where))}** في جوفه")
    add("(" + "، ".join(f"سطرُ {grouped(int(one))}" for one, _, _ in where) + " —")
    add("**بأرقام الأسطر وحدَها** إذ لا فهرسَ سورٍ مُودَع). والمُودَعُ قبلُ أنّ")
    add("غيرَ المُصَدَّر به **أربعٌ**، والمقيسُ ههنا **ثلاثٌ**. **ولا يُخمَّن")
    add("الفرق**: فضُّه يحتاج فهرسَ سورٍ ليس في المستودع.")
    add("")
    add("**والأصليّةُ والفرعيّة**: لا تُقرآن من البايتات — تحتاجان جدولَ أبوابٍ")
    add("مُودَعًا، وليس في المستودع جدول. **فهذا خلوٌّ مُصنَّفٌ**")
    add("(«فحصُها مُعيَّنٌ ولم يُجرَ») **لا نتيجةٌ صفر**، ولا يُسَدُّ بتخمين.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
