"""سقفُ سلّم السياق المادّيّ — تشغيلُ ختم `3fbbac9a…`.

**لا تُكتَب شفرةُ السلّم ههنا ولا تُحرَّر هناك**: تُحمَّل
`examples/rasm/run_context_ladder.py` ويُرفَع `MOST` **في الذاكرة**، ثمّ
تُشغَّل `main` نفسُها. فالمقيسُ **شفرةُ الختم `9034199d…` بعينها**، والسقفُ
وحدَه يتبدّل.

`AND_THE_SEALED_FILE_IS_NOT_TOUCHED`: العطل ٢٩ — **مُدخَلُ سجلٍّ مُقفَلٍ
مُقفَلٌ مثلُه**. و`deposits/context_ladder_run.log` مخرَجُ ذلك الملفّ
مُبصَّمًا يُقابَل بايتةً ببايتة، فلو حُرِّر `MOST` فيه **لانكسر السجلُّ
وتدقيقُ الإعادة**.

`AND_THE_PREFIX_IS_COMPARED_LINE_BY_LINE`: **والاثنتا عشرةَ الأولى تُقابَل
بالسجلّ المُودَع سطرًا سطرًا**. فاختيارُ الجشع لا يتعلّق بالسقف، فإن خالفت
درجةٌ **فالغلافُ يقيس شيئًا آخر** — ويسقط التشغيلُ لا المادّة.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import re
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
LADDER = REPOSITORY / "examples" / "rasm" / "run_context_ladder.py"
SEALED = REPOSITORY / "deposits" / "context_ladder_run.log"
LIFT_TO = 100
COMPARE = 12

STEP = re.compile(
    r"^— د(\d+) «(.+?)»: ملحَقة ([\d.]+) \| محجوزة ([\d.]+)"
    r" \| ربحٌ ملحَقٌ ([+-][\d.]+) \| ربحٌ محجوزٌ ([+-][\d.]+) \| كتلٌ (\d+)$",
    re.M,
)

Step = tuple[int, str, float, float, float, float, int]


def _ladder() -> object:
    spec = importlib.util.spec_from_file_location("run_context_ladder", LADDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للسلّم")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def summed(text: str, label: str) -> float:
    """مقدارٌ يُقرَأ من سطر السلّم نفسِه — **لا يُعاد جمعُه من المطبوع**."""

    found = re.search(rf"{re.escape(label)}: ([+-]?[\d.]+)", text)
    if found is None:
        raise SystemExit(f"لا شاهدَ في مخرَج السلّم لـ{label}")
    return float(found.group(1))


def steps_of(text: str) -> list[Step]:
    return [
        (
            int(depth),
            label,
            float(inside),
            float(outside),
            float(gain_in),
            float(gain_out),
            int(blocks),
        )
        for depth, label, inside, outside, gain_in, gain_out, blocks in STEP.findall(
            text
        )
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ladder = _ladder()
    written = getattr(ladder, "MOST")
    setattr(ladder, "MOST", LIFT_TO)
    print(f"— السقفُ المكتوبُ في الملفّ: {written} — ورُفِع في الذاكرة إلى {LIFT_TO}")
    print("— والملفُّ لم يُحرَّر بحرف (العطل ٢٩)")
    print()

    held = io.StringIO()
    saved = sys.argv
    sys.argv = ["run_context_ladder", "--text", str(given.text)]
    try:
        with contextlib.redirect_stdout(held):
            code = ladder.main()  # type: ignore[attr-defined]
    finally:
        sys.argv = saved
        setattr(ladder, "MOST", written)
    if code != 0:
        raise SystemExit(f"السلّمُ خرج برمزٍ {code}")

    deep = held.getvalue()
    print("═══ مخرَجُ السلّم بالسقف المرفوع ═══")
    print(deep.rstrip())
    print()

    here = steps_of(deep)
    there = steps_of(SEALED.read_text(encoding="utf-8"))
    print("═══ الحكم ═══")
    print()
    print(f"— مقابلةُ الأولى بالسجلّ المُودَع (أوّلُ {COMPARE} درجة)")
    apart = 0
    for one, two in zip(here[:COMPARE], there[:COMPARE]):
        if one != two:
            apart += 1
            print(f"  خلافٌ عند د{one[0]}: ههنا {one} | وفي السجلّ {two}")
    print(f"  درجاتٌ في السجلّ: {len(there)} | وههنا: {len(here)}")
    print(f"  درجاتٌ خالفت: {apart}")

    stopped = re.search(r"الوقوف: لا سؤالَ يربح محجوزًا عند الدرجة (\d+)", deep)
    reached = len(here)
    print()
    print(f"— الدرجاتُ المبلوغة: {reached}")
    if stopped is None:
        print("  ولا سطرَ وقوفٍ — فالحلقةُ نفدت أسئلتُها أو بلغت السقفَ المرفوع")
    else:
        print(f"  وسطرُ الوقوف عند الدرجة {stopped.group(1)} — **فالوقوفُ بالمادّة**")

    lowest = here[-1][3] if here else 0.0
    total_out = summed(deep, "مجموعُ الكسب المحجوز")
    total_in = summed(deep, "مجموعُ الكسب الملحَق")
    share = summed(deep, "نصيبُ الدرجة الأولى من الكسب المحجوز")
    # **والمجموعُ يُقرَأ من سطر السلّم لا يُعاد جمعُه**: أرباحُ الدرجات
    # مطبوعةٌ بأربع منازل، فجمعُها **تقريبٌ للتقريب**. ويُطبَع الفرقُ عددًا
    # كي لا يُظَنّ خلافًا في المقيس — وهو خطوةُ تدوير لا غير.
    my_out = sum(one[5] for one in here)
    my_in = sum(one[4] for one in here)
    print(f"  أدنى إنتروبيا محجوزة: {lowest:.4f}")
    print(f"  مجموعُ الكسب المحجوز (من سطر السلّم): {total_out:+.6f}")
    print(f"  مجموعُ الكسب الملحَق (من سطر السلّم): {total_in:+.6f}")
    print(f"  نصيبُ الدرجة الأولى من المحجوز (من سطر السلّم): {share:.4f}")
    print(f"  وبجمع المطبوعِ بأربع منازل: {my_out:+.6f} و{my_in:+.6f}")
    print(f"  فالفرقُ تدويرٌ: {abs(my_out - total_out):.6f} و{abs(my_in - total_in):.6f}")
    print(f"  ربحُ الدرجة الأخيرة محجوزًا: {here[-1][5]:+.6f}")
    print(f"  درجاتٌ ربحُها المحجوزُ ≤ صفر: {sum(1 for one in here if one[5] <= 0)}")
    print(f"  درجاتٌ ربحُها الملحَقُ ≤ صفر: {sum(1 for one in here if one[4] <= 0)}")
    print(f"  كتلُ آخر درجة: {here[-1][6] if here else 0}")

    print()
    print("— ما زاده الرفعُ على السقف المكتوب")
    # والزائدُ يُجمَع من المطبوع — ولا سطرَ في السلّم يفصله، فيُقال تقريبًا
    extra_out = sum(one[5] for one in here[COMPARE:])
    extra_in = sum(one[4] for one in here[COMPARE:])
    print(f"  درجاتٌ زائدة: {max(reached - COMPARE, 0)}")
    print(f"  كسبٌ محجوزٌ زائد: {extra_out:+.6f}")
    print(f"  كسبٌ ملحَقٌ زائد: {extra_in:+.6f}")
    if total_out:
        print(f"  ونصيبُ الزائد من المحجوز: {extra_out / total_out:.4f}")

    print()
    print("— ما لا يُدَّعى")
    print("  بلوغُ السقف لا يستنفد السياق: العائلاتُ خمسٌ على هذه القسمة،")
    print("  وعائلةٌ سادسةٌ (طولُ اللفظ، موقعُه، جارُه التالي) لم تُقَس ههنا.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
