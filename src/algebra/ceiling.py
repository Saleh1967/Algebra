"""سقفُ النسبة: **حدٌّ فوق سقفٍ شرطٌ لا يُختبَر** — والحكمُ حينئذٍ خلوٌّ لا سقوط.

`THE_FLAW_THIS_MODULE_NAMES`: نسبةٌ بسطُها لا يقبل كلَّ ما في مقامها —
لأنّ فيه ما **يمتنع بالبناء** أن يدخل البسط — **سقفُها دون الواحد**. فإن
كُتِب حدُّها فوق ذلك السقف **لم تكن قابلةً للتحقّق من أصلها**، وسقوطُها
**لا يخبر عن المادّة بشيء**: يخبر عن حسابٍ في صياغة الشرط.

`AND_THE_VERDICT_IS_A_VACANCY_NOT_A_FALL`: فالحكمُ الصحيحُ عندها
`Vacancy.IMPOSSIBLE` — **«فحصٌ لا يُمكِن أن يمرَّ»** — لا `FALSIFIED`.
والفرقُ ليس لفظيًّا: `FALSIFIED` يُسجَّل في رصيد ما سقط فيُقرَأ خبرًا عن
المادّة، **وIMPOSSIBLE يُسجَّل في رصيد ما لم يُختبَر**.

`AND_THE_CEILING_IS_ARITHMETIC_NOT_OPINION`: سقفُ النسبة
`(المقامُ − الممتنعُ) ÷ المقام` — حسابٌ تامٌّ متى عُلِم الممتنع. **والعلمُ
به تصريحٌ لا استنباط**: لا تُحسَب الامتناعاتُ آليًّا لكلّ إحصاء، **فيُصرَّح
بها ويُفحَص الحدُّ عليها**. وذلك حدُّ هذه الوحدة، ويُقال.

`AND_A_CEILING_OF_ONE_IS_A_CLAIM_TOO`: ومن قال «سقفي واحد» فقد ادّعى أنّ
**كلَّ ما في المقام يقبل الدخولَ في البسط** — وذلك يُسمّى ويُعلَّل، **ولا
يمرُّ صمتًا** كي لا يصير التصريحُ خاتمًا على بياض.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Final

from .results import Vacancy

WHOLE: Final[Fraction] = Fraction(1)


class CeilingError(ValueError):
    """رُدَّ سقفٌ لا يكون سقفًا، أو مقامٌ لا يحمل ما يُمتنَع منه."""


def attainable_ceiling(whole: int, barred: int) -> Fraction:
    """`(المقامُ − الممتنعُ) ÷ المقام` — كسرٌ تامٌّ لا عائم.

    و`barred` ما **يمتنع بالبناء** أن يدخل البسط، لا ما لم يدخله اتّفاقًا.
    """

    if whole <= 0:
        raise CeilingError("مقامٌ ليس موجبًا لا سقفَ له.")
    if not 0 <= barred <= whole:
        raise CeilingError(f"ممتنعٌ خارجَ المقام: {barred} من {whole}.")
    return Fraction(whole - barred, whole)


def threshold_is_reachable(threshold: Fraction, ceiling: Fraction) -> bool:
    """أَيُمكِن أن يُبلَغ الحدُّ؟ — `الحدُّ ≤ السقف` ولا أكثر."""

    if not 0 <= ceiling <= WHOLE:
        raise CeilingError(f"سقفٌ خارجَ [٠، ١]: {ceiling}.")
    if threshold < 0:
        raise CeilingError(f"حدٌّ سالبٌ لنسبة: {threshold}.")
    return threshold <= ceiling


def verdict_or_vacancy(
    threshold: Fraction, ceiling: Fraction, measured: Fraction
) -> Vacancy | None:
    """`IMPOSSIBLE` إن كان الحدُّ فوق السقف، و`None` إن كان الحكمُ قائمًا.

    **و`None` ليست حكمًا**: تعني أنّ الشرطَ قابلٌ للاختبار فيُحكَم عليه
    بأدواته. وأمّا المقيسُ فيُفحَص أنّه لا يفوق السقفَ — **فإن فاقه فأحدُ
    الرقمين خطأٌ**، ويُردّ.
    """

    if not threshold_is_reachable(threshold, ceiling):
        return Vacancy.IMPOSSIBLE
    if measured > ceiling:
        raise CeilingError(f"مقيسٌ فوق سقفه: {measured} > {ceiling} — فأحدُ الرقمين خطأ.")
    return None
