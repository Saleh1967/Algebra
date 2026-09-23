"""مُشغِّلُ القياس المختوم: يأخذ محاذاةً ويُخرِج الأحكامَ التسعةَ كلَّها.

**لماذا مُشغِّلٌ لا نتيجة**: المدوَّنةُ ليست في هذه الجلسة — `corpora/` و
`case_data/` فارغتان، ولا مخرَجَ ط٢ ولا وسمَ QAC ولا `particles.json`. فما
يُبنى ههنا هو **الآلةُ** التي تُجري القياسَ المختومَ في أمرٍ واحدٍ متى وصلت
المدخلات، لا رقمٌ يُدَّعى. وتشغيلُها على عيّنةٍ مُصطنَعةٍ (`--smoke`) يُثبِت
أنّها تعمل، ولا يقول شيئًا عن العربيّة — وهذا يُطبَع في رأس المخرَج.

**المدخل** — جدولٌ مفصولٌ بالجدولات، سبعةُ أعمدةٍ مُعلَنة:

    surface  prefixes  suffixes  pos  deictic  prev_jarr  gold

حيث `prefixes`/`suffixes` مفصولةٌ بفواصلَ وقد تخلو، و`pos` من {harf, fi'l,
ism} كما يقوله ط٧، و`deictic` و`prev_jarr` صفرٌ أو واحد، و`gold` من
{raf', nasb, jarr} أو `-` لما لم يسمه العرّافُ بحالة.

**ما يُخرِجه**:

  ١. العدُّ: الكلُّ، والموسومُ، وغيرُ الموسوم.
  ٢. الثلاثيُّ على الموسوم، والرباعيُّ على الكلّ.
  ٣. جدولُ الاستئصال: زيادةُ **كلّ قاعدةٍ وحدَها** — وهو الشرط (هـ)، ولا
     يُطبَع مجموعٌ بلا تفصيله.
  ٤. الأحكامُ التسعة، كلٌّ ببصمة تسجيله.

`A_SEALED_RULE_NAMED_BY_NUMBER_BREAKS_WHEN_THE_NUMBERING_MOVES`: التسجيلُ
الثاني يقول «ك١ — **ق٥** الممنوعُ من الصرف»، وفي النسخة الحاليّة ق٥ هي
**الامتناع** والممنوعُ من الصرف صار **ق٦**. فرقمُ القاعدة ليس اسمًا ثابتًا،
والشرطُ المختومُ عليه يصير غيرَ مقروءٍ بعد إعادة الترقيم. فههنا خريطةٌ
**مُعلَنةٌ** من معرّفات التسجيلات إلى رايات النسخة، تُطبَع مع المخرَج ولا
تُخمَّن.

`THE_DEFER_POLICY_IS_AN_ARGUMENT_NOT_A_DEFAULT`: `--defer` مطلوبٌ ولا قيمةَ
افتراضيّةَ له، لأنّ مصير «لم يُحسَم» يحرّك الرباعيَّ في اتّجاهين والتسجيلُ
لا يقول. فالمُشغِّلُ يرفض العملَ حتى يُعلَن.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY / "tests" / "algebra"))

from harf_rules import (  # noqa: E402
    ALL_RULES,
    DEFER,
    NO_CASE,
    SEALED_RULES,
    four_way,
    revised_irab_of,
)

# خريطةٌ مُعلَنةٌ من معرّفات التسجيلات إلى رايات النسخة الحاليّة
SEALED_TO_CURRENT: dict[str, tuple[str, ...]] = {
    "أ' — ق٠ تقشيرُ الضمير": ("ق٠",),
    "ب' — لواحقُ الحرف وفضُّها وجمعُ المؤنّث": ("ق١", "ق٢", "ق٤"),
    "ك١ — الممنوعُ من الصرف (ق٥ في التسجيل، ق٦ الآن)": ("ق٦",),
    "ك٢ — جمعُ المؤنّث «ات» (ق٤ في الموضعين)": ("ق٤",),
}
"""ولا يُقرَأ شرطٌ مختومٌ برقمِ قاعدةٍ إلّا عبر هذه الخريطة."""

SECOND_SEAL = "ff690f9f6ab3135c95c825bc1ea2841b4c77e9129840b00a314b06d732abe1e8"
THIRD_SEAL = "ee1f32efb07d9718591f63f977faa1b0da4f08f59dee767a145f4648d5a7c797"


@dataclass(frozen=True, slots=True)
class Token:
    """رمزٌ محاذًى: مخرَجُ الطبقات، ومعه وسمُ العرّاف أو غيابُه."""

    surface: str
    prefixes: tuple[str, ...]
    suffixes: tuple[str, ...]
    pos: str
    deictic: bool
    prev_jarr: bool
    gold: str | None  # None لِما لم يسمه العرّافُ بحالة

    def record(self) -> dict[str, object]:
        return {
            "surface": self.surface,
            "pos": self.pos,
            "suffixes": list(self.suffixes),
            "prefixes": list(self.prefixes),
            "components": [{"kind": "deictic"}] if self.deictic else [],
        }


def read_alignment(path: Path) -> list[Token]:
    """قراءةُ الجدول من ملفّ."""

    return parse_alignment(path.read_text(encoding="utf-8"))


def parse_alignment(text: str) -> list[Token]:
    """تحليلُ الجدول؛ وسطرٌ ناقصُ الأعمدة يُرَدّ باسمه لا يُكمَّل صمتًا."""

    tokens: list[Token] = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 7:
            raise ValueError(f"السطرُ {number}: {len(fields)} عمودًا والمُعلَنُ سبعة.")
        surface, prefixes, suffixes, pos, deictic, prev_jarr, gold = fields
        tokens.append(
            Token(
                surface=surface,
                prefixes=tuple(one for one in prefixes.split(",") if one),
                suffixes=tuple(one for one in suffixes.split(",") if one),
                pos=pos.strip(),
                deictic=deictic.strip() == "1",
                prev_jarr=prev_jarr.strip() == "1",
                gold=None if gold.strip() in ("-", "") else gold.strip(),
            )
        )
    if not tokens:
        raise ValueError("محاذاةٌ خاليةٌ لا يُقاس عليها.")
    return tokens


def predict(token: Token, rules: tuple[str, ...], oracle_pos: bool = False) -> str:
    return revised_irab_of(
        token.record(),
        token.prev_jarr,
        rules=rules,
        oracle_pos=_true_pos(token) if oracle_pos else None,
    )[0]


def _true_pos(token: Token) -> str:
    """وسمٌ صحيحٌ مُشتَقٌّ من العرّاف: ما سُمّي بحالةٍ اسمٌ، وما لم يُسَمّ ليس اسمًا.

    وهذا تقريبٌ مُعلَنٌ لا حقيقة: العرّافُ يفرّق الحرفَ من الفعل، وهذه
    المحاذاةُ لا تحمل ذلك الفرق. فـ(ز) تُقاس به، ويُقال إنّه تقريب.
    """

    return "ism" if token.gold else "harf"


def three_way(tokens: list[Token], rules: tuple[str, ...]) -> Fraction:
    """الإصابةُ على الموسوم وحدَه؛ والامتناعُ هناك خطأٌ بالتعريف."""

    marked = [token for token in tokens if token.gold]
    if not marked:
        raise ValueError("لا رمزَ موسومًا بحالة، فلا ثلاثيَّ يُقاس.")
    hits = sum(1 for token in marked if predict(token, rules) == token.gold)
    return Fraction(hits, len(marked))


def four_way_score(
    tokens: list[Token], rules: tuple[str, ...], defer_as: str, oracle_pos: bool = False
) -> Fraction:
    """الإصابةُ على الكلّ بأربعة أصناف، ومصيرُ «لم يُحسَم» مُعلَنٌ لا مفترَض."""

    hits = 0
    for token in tokens:
        target = token.gold if token.gold else NO_CASE
        got = four_way(predict(token, rules, oracle_pos), defer_counts_as=defer_as)
        hits += int(got == target)
    return Fraction(hits, len(tokens))


def abstention_counts(
    tokens: list[Token], rules: tuple[str, ...]
) -> tuple[int, int, int]:
    """(مصيبٌ، مخطئٌ، ممتنعٌ) على الموسوم — ثلاثةُ أرقامٍ لا واحد."""

    correct = wrong = held = 0
    for token in tokens:
        if not token.gold:
            continue
        got = predict(token, rules)
        if got in (DEFER, NO_CASE):
            held += 1
        elif got == token.gold:
            correct += 1
        else:
            wrong += 1
    return correct, wrong, held


def ablation(
    tokens: list[Token], defer_as: str
) -> dict[str, tuple[Fraction, Fraction]]:
    """زيادةُ كلّ قاعدةٍ وحدَها على المقياسين — وهو الشرط (هـ) مُستوفًى."""

    whole3, whole4 = (
        three_way(tokens, ALL_RULES),
        four_way_score(tokens, ALL_RULES, defer_as),
    )
    table: dict[str, tuple[Fraction, Fraction]] = {}
    for rule in ALL_RULES:
        without = tuple(one for one in ALL_RULES if one != rule)
        table[rule] = (
            whole3 - three_way(tokens, without),
            whole4 - four_way_score(tokens, without, defer_as),
        )
    return table


def _pct(value: Fraction) -> str:
    return f"{float(value) * 100:6.2f}٪"


def _verdict(measured: Fraction, threshold: Fraction, at_least: bool = True) -> str:
    met = measured >= threshold if at_least else measured <= threshold
    return "MET" if met else "FALSIFIED"


def report(tokens: list[Token], defer_as: str) -> None:
    """الأحكامُ التسعةُ كلُّها، كلٌّ ببصمة تسجيله وبالخريطة المُعلَنة."""

    marked = sum(1 for token in tokens if token.gold)
    unmarked = len(tokens) - marked
    print(f"الرموزُ المحاذاة: {len(tokens)}  ·  موسومٌ {marked}  ·  غيرُ موسومٍ {unmarked}")
    print(
        f"نصيبُ «لا إعراب» (خطُّ الأساس الرباعيّ): {_pct(Fraction(unmarked, len(tokens)))}"
    )
    print(f"مصيرُ «لم يُحسَم» كما أُعلن: {defer_as}")
    print()

    whole3 = three_way(tokens, ALL_RULES)
    whole4 = four_way_score(tokens, ALL_RULES, defer_as)
    sealed4 = four_way_score(tokens, SEALED_RULES, defer_as)
    oracle4 = four_way_score(tokens, ALL_RULES, defer_as, oracle_pos=True)
    print(f"الثلاثيُّ على الموسوم        : {_pct(whole3)}")
    print(f"الرباعيُّ على الكلّ          : {_pct(whole4)}")
    print(f"الرباعيُّ بق٥ المختومة وحدَها : {_pct(sealed4)}")
    print(f"الرباعيُّ بوسمٍ صحيحٍ لط٧     : {_pct(oracle4)}")
    print()

    print("جدولُ الاستئصال — زيادةُ كلّ قاعدةٍ وحدَها (الشرط هـ):")
    table = ablation(tokens, defer_as)
    for rule, (gain3, gain4) in table.items():
        print(f"  {rule:5} ثلاثيّ {_pct(gain3)}   رباعيّ {_pct(gain4)}")
    print()

    print("الخريطةُ المُعلَنةُ من التسجيلات إلى الرايات:")
    for sealed, current in SEALED_TO_CURRENT.items():
        print(f"  {sealed} ← {'، '.join(current)}")
    print()

    def joint(rules: tuple[str, ...]) -> Fraction:
        without = tuple(one for one in ALL_RULES if one not in rules)
        return whole3 - three_way(tokens, without)

    correct, wrong, held = abstention_counts(tokens, ALL_RULES)
    assigned = correct + wrong
    coverage = Fraction(assigned, marked) if marked else Fraction(0)
    precision = Fraction(correct, assigned) if assigned else Fraction(0)
    baseline4 = Fraction(unmarked, len(tokens))

    rows = (
        ("أ' ", SECOND_SEAL, joint(("ق٠",)), Fraction("0.05"), True),
        ("ب' ", SECOND_SEAL, joint(("ق١", "ق٢", "ق٤")), Fraction("0.05"), True),
        ("ك١ ", SECOND_SEAL, joint(("ق٦",)), Fraction("0.01"), True),
        ("ك٢ ", SECOND_SEAL, joint(("ق٤",)), Fraction(0), True),
        ("ك٣ ", SECOND_SEAL, whole3, Fraction("0.88"), True),
        ("ك٤ ", SECOND_SEAL, precision, Fraction("0.90"), True),
        ("ك٥ ", SECOND_SEAL, coverage, Fraction("0.93"), True),
        ("و  ", THIRD_SEAL, sealed4, baseline4 + Fraction("0.15"), True),
        ("ز  ", THIRD_SEAL, oracle4 - whole4, Fraction("0.05"), False),
    )
    print("الأحكام:")
    for name, fingerprint, measured, threshold, at_least in rows:
        sign = "≥" if at_least else "≤"
        print(
            f"  {name} {fingerprint[:8]}…  المقيس {_pct(measured)}  "
            f"{sign} {_pct(threshold)}  ⇒  {_verdict(measured, threshold, at_least)}"
        )


SMOKE = """\
# عيّنةٌ مُصطنَعةٌ لفحص الآلة — لا تقول شيئًا عن العربيّة
ٱلْمُؤْمِنُونَ\tال\tون\tism\t0\t0\traf'
ٱلْمُؤْمِنِينَ\tال\tين\tism\t0\t1\tjarr
ٱلْمُؤْمِنِينَ\tال\tين\tism\t0\t0\tnasb
ٱلصَّٰلِحَٰتُ\tال\tات\tism\t0\t0\traf'
ٱلصَّٰلِحَٰتِ\tال\tات\tism\t0\t0\tnasb
ٱلصَّٰلِحَٰتِ\tال\tات\tism\t0\t1\tjarr
إِبْرَٰهِيمَ\t\t\tism\t0\t1\tjarr
إِبْرَٰهِيمَ\t\t\tism\t0\t0\tnasb
ٱلْكِتَٰبَ\tال\t\tism\t0\t0\tnasb
ٱللَّهِ\tال\t\tism\t0\t1\tjarr
كِتَٰبُهُۥ\t\tه\tism\t0\t0\traf'
رَبِّهِمْ\t\tهم\tism\t0\t1\tjarr
مِن\t\t\tharf\t0\t0\t-
فِى\t\t\tharf\t0\t0\t-
قَالَ\t\t\tfi'l\t0\t0\t-
يَعْلَمُونَ\t\tون\tfi'l\t0\t0\t-
هَٰذَا\t\t\tism\t1\t0\t-
قَالُوا\t\t\tfi'l\t0\t0\t-
# حالاتٌ معاكسةٌ مقصودة: لولاها لم يُعرَف أنّ الآلةَ تستطيع أن تقول «لا»
ءَايَٰتِ\t\tات\tism\t0\t0\tjarr
بَيِّنَٰتِ\t\tات\tism\t0\t0\tjarr
سَحَرْ\t\t\tism\t0\t0\tnasb
ٱلَّذِينَ\tال\tين\tism\t0\t0\t-
يَقُولُ\t\t\tism\t0\t0\t-
مَا\t\t\tism\t0\t0\t-
# مبنيٌّ ساكنُ الآخر فاته ط٧: يُؤجَّل وهو غيرُ موسوم — وعليه يفترق قرارا «لم يُحسَم»
كَمْ\t\t\tism\t0\t0\t-
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__ and __doc__.splitlines()[0])
    parser.add_argument("--aligned", type=Path, help="جدولُ المحاذاة بسبعة أعمدة")
    parser.add_argument(
        "--defer",
        required=True,
        choices=("no-case", "error"),
        help="مصيرُ «لم يُحسَم» — يُعلَن ولا يُفترَض",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="تشغيلٌ على عيّنةٍ مُصطنَعةٍ لفحص الآلة وحدَها",
    )
    args = parser.parse_args(argv)

    if args.smoke:
        tokens = parse_alignment(SMOKE)
        print("=" * 72)
        print("تشغيلُ فحصٍ على عيّنةٍ **مُصطنَعة**: يُثبِت أنّ الآلةَ تعمل،")
        print("ولا يقول شيئًا عن العربيّة. والأحكامُ أدناه ليست أحكامَ التسجيلات.")
        print("=" * 72)
    elif args.aligned:
        tokens = read_alignment(args.aligned)
    else:
        parser.error("إمّا `--aligned` وإمّا `--smoke`؛ ولا قياسَ بلا مدخل.")

    report(tokens, NO_CASE if args.defer == "no-case" else "خطأ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
