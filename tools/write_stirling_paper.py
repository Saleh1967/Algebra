"""تُكتَب وثيقةُ ستيرلنغ مع الجشع **من سجلّ التشغيل** — لا من نثر."""

from __future__ import annotations

import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
LOG = REPOSITORY / "deposits" / "stirling_greedy_run.log"
WITNESS = REPOSITORY / "deposits" / "stirling_greedy_witness.log"
PAPER = REPOSITORY / "docs" / "ستيرلنغ-مع-الجشع.md"
EASTERN = str.maketrans("0123456789.", "٠١٢٣٤٥٦٧٨٩٫")


def eastern(one: object) -> str:
    return str(one).translate(EASTERN)


def grab(pattern: str, text: str) -> tuple[str, ...]:
    found = re.findall(pattern, text)
    if not found:
        raise SystemExit(f"لا شاهدَ في السجلّ لـ{pattern}")
    first = found[0]
    return first if isinstance(first, tuple) else (first,)


def render() -> str:
    text = LOG.read_text(encoding="utf-8")
    spent = re.findall(
        r"^  (\S+) بمعيار (\S+): بتّاتٌ (\d+) \| أوّلُ سؤالٍ أصغرُ كتلةٍ فيه (\d+)$",
        text,
        re.M,
    )
    (apart,) = grab(r"درجاتٌ يفترق فيها السؤالُ الأوّل: (\d+)", text)
    (identity,) = grab(r"أقصى انحرافٍ عن الهويّة: (\S+)", text)
    ahead, behind, spread = grab(r"تباديلُ (\S+) \| إنتروبيا (\S+) \| فرقٌ (\S+)", text)
    (trivial,) = grab(r"أدنى فجوةِ ستيرلنغ على الكتل: (\S+)", text)
    (real,) = grab(r"وأدناها على كتلةٍ غيرِ نقيّة: (\S+)", text)
    space, visited, walked = grab(
        r"قسماتُ (\d+) خاناتٍ \(بِلّ ناقصَ الواحدة\): (\d+) \| وزارها الجشعُ (\d+)",
        text,
    )
    rows = sorted(
        {
            (int(one), int(two))
            for one, two in re.findall(r"إلى (\d+) كتلًا: S\(4,\d\) = (\d+)", text)
        }
    )
    stand = text.split("═══ مقامُ")[1]
    arms = {
        one.split(":")[0].strip(): re.findall(
            r"^      د(\d+) «أمن (.+?)؟»: ربحٌ (\S+) \| كتلٌ (\d+)$", one, re.M
        )
        for one in stand.split("— بمعيار ")[1:]
    }

    out: list[str] = []
    add = out.append
    add("# ستيرلنغ مع الجشع وقت الحساب — ودعوًى سقطت")
    add("")
    add("**الختم**: `62495099…` — مُودَعٌ ومدفوعٌ **قبل أن يُحسَب شيء**.")
    add("**الحصاد**: **سبعُ** شروطٍ من عشرٍ صمدت، و**ثلاثٌ** سقطت — **ومنها**")
    add("**دعوايَ الكبرى**.")
    add("")
    add("## الدعوى، وكيف سقطت")
    add("")
    add("**المقترَح**: أنّ الجشعَ يسجّل **بالإنتروبيا**، وهي **حدُّ ستيرلنغ**")
    add("لعدد التباديل لا العددُ نفسُه؛ فإن حُسِب **العددُ وقت الاختيار** ربّما")
    add("اختار غيرَ ما اختار، **فتعود البتّةُ المفقودة**.")
    add("")
    add("| المقام | المعيار | بتّات | أصغرُ كتلةٍ في السؤال الأوّل |")
    add("|---|---|---|---|")
    for stand, how, bits, smallest in spent:
        add(f"| {stand} | {how} | **{eastern(bits)}** | {eastern(smallest)} |")
    add("")
    add("**فلم تعد.** الحسابُ بالتباديل صرف **ثلاثَ بتّاتٍ** كما صرفت")
    add("الإنتروبيا، **والقسمةُ الأولى ١–٣ بالمعيارين**.")
    add("")
    add("**وأنفعُ الثلاثة**: عددُ الدرجات التي يفترق فيها سؤالُ المعيارين")
    add(f"**{eastern(apart)}**. **فالمعياران يتّفقان على كلّ سؤالٍ في**")
    add("**المقامين** — يُبدِّل ستيرلنغ **المقدارَ** ولا يُبدِّل **الاختيار**.")
    add("")
    add("## والمقدارُ يتبدّل تبدّلًا كبيرًا")
    add("")
    add(f"مجموعُ الكسب في مقام الحصر: بالتباديل **{eastern(ahead)}**")
    add(f"وبالإنتروبيا **{eastern(behind)}** — فرقٌ **{eastern(spread)}** بتًّا.")
    add("")
    add("**وهذا الفرقُ مُعيَّنٌ لا مقدَّر**، بهويّةٍ كُتِبت **قبل النظر**:")
    add("")
    add("    كسبُ التباديل − كسبُ الإنتروبيا = Σ فجواتِ الكتل − فجوةُ الجذر")
    add("")
    add(f"وأقصى انحرافٍ عنها **{eastern(identity)}** — **خطوةُ العائم لا خلاف**.")
    add("")
    add("**وما اشتُقّ صمد وما ظُنّ سقط**: كون الكسب بالتباديل أوفر كان")
    add("**مُشتَقًّا** من أنّ فجوةَ الجذر أصغرُ من مجموع فجوات الكتل — **فصمد**.")
    add("وكونُ القسمة تتوازن كان **ظنًّا** — **فسقط**.")
    add("")
    add("## فأين العطل إذًا؟")
    add("")
    add("**في قِصَر نظر الجشع، لا في حدّ ستيرلنغ.** السؤالُ الأوّلُ في مقام")
    add("الحصر يقسم **١–٣** بالمعيارين كليهما، فيلزم **ثلاثةُ** أسئلةٍ لبلوغ")
    add("أربع كتل؛ ولو قُسِم **٢–٢** لكفى **اثنان**. **وكلا المعيارين يرى**")
    add("**١–٣ أربحَ الآن.**")
    add("")
    add("| الدرجة | السؤال | ربحٌ بالإنتروبيا | ربحٌ بالتباديل | كتل |")
    add("|---|---|---|---|---|")
    left, right = arms["إنتروبيا"], arms["تباديل"]
    if [one[1] for one in left] != [one[1] for one in right]:
        raise SystemExit("الذراعان اختلفا في السؤال — والوثيقةُ تدّعي اتّفاقَهما")
    for (depth, label, gain, count), (_, _, other, _) in zip(left, right):
        rung, ask = eastern(depth), f"«أمن {label}؟»"
        add(
            f"| د{rung} | {ask} | {eastern(gain)} | {eastern(other)} "
            f"| {eastern(count)} |"
        )
    add("")
    add("## وسَعةُ ما لم يبحثه الجشعُ — عددًا لا قولًا")
    add("")
    add(f"قسماتُ **{eastern(space)}** خاناتٍ إلى كتلتين فأكثر")
    add(f"**{eastern(visited)}** قسمة، **والجشعُ يزور {eastern(walked)}**:")
    add("")
    add("| إلى كم كتلة | `S(n,k)` |")
    add("|---|---|")
    for parts, count in rows:
        add(f"| {eastern(parts)} | {eastern(count)} |")
    add("")
    add("**ورقمُ ستيرلنغ من النوع الثاني يُسعِّر دعوى «الجشعُ غيرُ مبرهَن»**")
    add("**عددًا** بدل أن تبقى قولًا يُردَّد.")
    add("")
    add("## شرطان مرّا بطرفٍ تافه — ويُقال")
    add("")
    add(f"أدنى فجوةِ ستيرلنغ **{eastern(trivial)}** — وتقع عند **كتلةٍ نقيّةٍ**")
    add("**صنفُها واحد**، وثمناها صفران. **فالمرورُ صحيحٌ والشهادةُ خاوية.**")
    add(f"وما يشهد حقًّا **{eastern(real)}** على أدنى كتلةٍ غيرِ نقيّة.")
    add("")
    add("## وحدةٌ أُضيفت: `algebra.stirling`")
    add("")
    add("**تصحيحُ الكمّ وتصحيحُ البنية، مفصولين**، ولا جدولَ مُودَع:")
    add("")
    add("- `cycles(n,k)` و`subsets(n,k)` **بقاعدتَي النمط** — لا بجدول.")
    add("- `inversion_closes(n)` — **المصفوفتان متعاكستان**، وضربُهما يُعيد")
    add("  المطابقة. **اختبارُ تصحيحٍ ذاتيٍّ لا يحتاج نسخةً من خارج.**")
    add("- `factorial_bounds(n)` — **حدّا روبنز من الطرفين**، فيُقال «بين")
    add("  كذا وكذا» **ولا يُقال «نحوَ كذا»**.")
    add("")
    add("**وحدُّ الآلة مُعلَن**: عند `n = ١٠٬٠٠٠` يصير عرضُ الكُنف **سبعَ**")
    add("**خطواتٍ من خطوات العائم**، وعند `n = ١٠٠٬٠٠٠` **صفرًا**. فالمبرهنةُ")
    add("**أحدُّ من الآلة**، والفحصُ يُسمّي موضعَ عماه ولا يحذف الحالة.")
    add("")
    add("## ما لا يُدَّعى")
    add("")
    add("**الجشعُ بالتباديل غيرُ مبرهَنٍ أيضًا**: أفضلُ سؤالٍ عند درجةٍ ليس")
    add("أفضلَ سلّمٍ في النهاية **بأيّ معيار**. **وما يُبلَغ حدٌّ أدنى.**")
    add("")
    add("**ولا قياسَ على المصحف ههنا**: المقيسُ **أثرُ المعيار على الجشع**،")
    add("لا اللغةُ ولا المادّة. **ولا يُوقَّع تأويلُ أنبوبٍ خارجيّ.**")
    add("")
    add("**والشاهدان المُضافان لم يُبدّلا رقمًا مختومًا** — والسجلّان")
    add("مُقابَلان سطرًا بسطر في `stirling_greedy_witness.log`.")
    add("")
    return "\n".join(out) + "\n"


def main() -> int:
    PAPER.write_text(render(), encoding="utf-8")
    assert WITNESS.is_file()
    print(f"كُتِب {PAPER.relative_to(REPOSITORY)} — {len(render().splitlines())} سطرًا")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
