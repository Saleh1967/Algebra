"""الجوابُ بالبتّات — نحوٌ مُغلَقٌ **متناهٍ**، فالعدُّ عليه استدلالٌ تامّ.

**ولا مدوّنةَ ههنا ولا لغة**: موضوعُ السؤال **كلُّ بايتةٍ ممكنة** — من ٠
إلى ٢٥٥ — واسمُه من جدولٍ مُغلَقٍ يضمّ المفرداتِ الستَّ واسمين من خارجها.
فالمجموعةُ متناهيةٌ **تُعَدّ كلُّها**، ولا تُنتقى منها عيّنة.

**وما يُعرَض أربعة**: أنّ كلَّ جوابٍ يمرُّ في مُتحقِّقٍ مستقلٍّ لا يستدعي
حاسبَه، وأنّ الردَّ على ما خرج عن المفردات **مُصنَّفٌ لا مسكوتٌ عنه**، وأنّ
توزيعَ الأجوبة يطابق `٢^(ك−١)` بالعدّ التامّ، وأنّ **ثمنَ الجواب أكبرُ من
قيمته** في كلّ حال.

**وما ليس ههنا**: طبقةُ التعلّم. فهذه أوّلُ خطوةٍ — نوعُ سؤالٍ واحد — ولا
يُقترَح فيها شيءٌ ولا يُرتَّب.
"""

from __future__ import annotations

from collections import Counter

from algebra.asking import ANSWERED_TODAY, Answer, Ask, Question, Status, answer, audit

OUTSIDE: tuple[str, ...] = ("PROVE", "GUESS")
"""اسمان **خارجَ المفردات** يُجرَّبان عمدًا — فالردُّ يُقاس لا يُفترَض."""

SUBJECTS: int = 256
"""كلُّ بايتةٍ ممكنة؛ والمجالُ متناهٍ فالعدُّ عليه تامّ."""


def asked() -> list[Ask]:
    """النحوُ المُغلَق مبسوطًا: كلُّ اسمٍ مع كلّ بايتة — ولا اختيار."""

    names = sorted(one.name for one in Question) + list(OUTSIDE)
    return [
        Ask(kind=name, subject=bytes([one]))
        for one in range(SUBJECTS)
        for name in names
    ]


def answered(asks: list[Ask]) -> list[Answer]:
    return [answer(one) for one in asks]


def main() -> int:
    asks = asked()
    found = answered(asks)
    tally = Counter(one.status.name for one in found)
    complaints = [two for one in found for two in audit(one)]
    given = [one for one in found if one.status is Status.ANSWERED]
    widths = Counter(int(one.value) for one in given)
    costs = [one.cost_bits for one in given]
    dearer = sum(1 for one in given if one.cost_bits <= int(one.value))
    astray = sum(
        1
        for one in found
        if (one.ask.kind in OUTSIDE) != (one.status is Status.UNSUPPORTED_QUESTION)
    )
    expected = {0: 1} | {one: 2 ** (one - 1) for one in range(1, 9)}
    drift = sum(
        1 for one, many in sorted(expected.items()) if widths.get(one, 0) != many
    )

    print(f"المفرداتُ {len(Question)} | المُجابُ عنه اليومَ {len(ANSWERED_TODAY)}")
    print(f"الأسماءُ المُجرَّبةُ {len(Question) + len(OUTSIDE)} | المواضيعُ {SUBJECTS}")
    print(f"الأسئلةُ المولَّدة {len(asks)}")
    for name in ("ANSWERED", "NOT_ANSWERABLE_YET", "UNSUPPORTED_QUESTION"):
        print(f"  {name} {tally[name]}")
    print(f"شكاوى المُتحقِّق المستقلّ {len(complaints)}")
    print(f"ردٌّ في غير بابه {astray}")
    print(f"أجوبةٌ ثمنُها لا يجاوز قيمتَها {dearer}")
    print(f"أكبرُ ثمنٍ {max(costs)} | أصغرُ ثمنٍ {min(costs)} | مجموعُ الأثمان {sum(costs)}")
    print(f"خانةٌ خالفت ٢^(ك−١) {drift}")
    print("التوزيعُ بالعدّ التامّ:")
    for one, many in sorted(widths.items()):
        print(f"  قيمةٌ {one} | مواضيعُ {many} | المنتظَرُ {expected[one]}")
    for one in complaints:
        print(f"شكوى: {one}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
