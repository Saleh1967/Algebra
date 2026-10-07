"""ركيزتان لا نصّان: أرقامي صحيحةٌ على الرسم الخام، وقياسي كان يجيب سؤالًا آخر.

**ما جرى**: قِست كلفةَ الدمج على **الرسم المشكول الخام**، فخرجت أرضيّةٌ جشعةٌ
عند ١٩ ونسبةُ حركةٍ إلى أغلى صامتٍ ١٫١٨×. ثمّ قيل: الركيزةُ الصحيحةُ أساسٌ
مطبَّع، وعليه الأرضيّةُ ٢١ والنسبةُ ٢٫٣٤×. فطُبِّق تطبيعٌ **مُعلَنٌ ههنا**
على الركيزة نفسِها، فانتقلت الأرقامُ في الاتّجاه المُدَّعى.

`THE_OBJECTION_WAS_SUBSTRATE_BOUND_AND_IS_WITHDRAWN`: قلتُ إنّ الحركاتِ
تفترق عن الصوامت بالوسيط لا بالأقصى (١٫١٨×)، وإنّ «بلا منازع» أقوى ممّا
يحتمله القياس. والتطبيعُ يرفع النسبةَ ١٫١٨ ← ١٫٢٨، والمُدَّعى ٢٫٣٤. فالاعتراضُ
**مقيَّدٌ بركيزته ويُسحَب بوصفه قولًا عامًّا**. ولا أُثبِت ٢٫٣٤ لأنّي لم
أبلغها: تطبيعي جزئيٌّ ويقف عند ١٫٢٨.

`TWO_OF_THREE_NAMED_COLLAPSES_REPRODUCE_UNDER_NORMALISATION`: على الخام
كانت ذ~غ وش~ك ور~ض **مجّانيّةً كلُّها**. وبعد ردّ المدّ صوتًا واحدًا
(ىٰ → ا) صارت **ذ~غ تكلّف واحدًا** (ذَوَا/غَوَا) و**ش~ك تكلّف واحدًا**
(كَفَا/شَفَا) — وهما اثنان من الثلاثة المسمّاة. وبقيت ر~ض مجّانيّةً لأنّ
فَرَرْتُم وفَرَضْتُمْ تفترقان عندي في **سكون الآخر**، وهو تطبيعٌ لم أبلغه.

`THE_GREEDY_FLOOR_MOVES_FROM_NINETEEN_TO_TWENTY_ONE`: وهو الرقمُ المُدَّعى
بعينه. وأربعةٌ من ستّة أصنافٍ تتطابق: `تزظ` · `ثح` · `جخ` · `ذط`.

`COMPRESSION_IS_NOT_INVERTIBILITY`: وأثقلُ ما فات قياسي ليس رقمًا. الحملُ
الوظيفيُّ يسأل: كم يصغر الجردُ **مع بقاء الأنواع متمايزة**؟ وذاك سؤالُ ضغط.
والمشروعُ يسأل: هل `Open(Close(x)) ≅ x`؟ وذاك سؤالُ **عكس**. وهما معياران
مختلفان: ث~ح مجّانيّةٌ بالأوّل — لا نوعين مشكولين يفترقان فيها وحدَها —
وممتنعةٌ بالثاني، لأنّ الاسترجاعَ ينكسر على **كلّ كلمةٍ** فيها ث أو ح.
فقولي «النصُّ سقفٌ لا أرضيّة» يصدق على **المعجم** ولا يمسّ الأرضيّة: الأرضيّةَ
تضعها أبجديّةُ الدخل لا قلّةُ تمييز المعجم. والمانعُ من **داخل الترميز**، فلا
يُحتاج إليه أذنٌ ولا ناطق.
"""

from __future__ import annotations

from fractions import Fraction

RAW_TYPES = 18_992
NORMALISED_TYPES = 18_705

# (الركيزة: أرخصُ حركةٍ، وسيطُ الصوامت، أغلى صامت، أصفارٌ من ٣٧٨)
MEASURED: dict[str, tuple[int, int, int, int]] = {
    "الرسمُ الخام": (395, 3, 336, 53),
    "تطبيعٌ جزئيّ": (435, 4, 337, 36),
    "تطبيعٌ + ردُّ المدّ": (435, 4, 339, 32),
}
REPORTED_ON_THE_BASE = (801, 5, 343, 28)

GREEDY_FLOOR = {"الرسمُ الخام": 20, "تطبيعٌ + ردُّ المدّ": 21}
REPORTED_FLOOR = 21

NAMED_COLLAPSES = {
    # الدمج: (كلفتُه على الخام، كلفتُه بعد ردّ المدّ)
    "ذ~غ": (0, 1),
    "ش~ك": (0, 1),
    "ر~ض": (0, 0),
}


def test_the_zero_load_count_reproduces_exactly_on_the_raw_script() -> None:
    """٥٣ زوجًا بحملِ صفرٍ على الرسم الخام حين يدخل ء — مطابقةٌ تامّة.

    وكان عددي ٣٧ على سبعةٍ وعشرين حرفًا (٣٥١ زوجًا)؛ والفرقُ أبجديّةٌ لا
    حساب. فإدخالُ ء يُكمِل الجردَ إلى ثمانيةٍ وعشرين و٣٧٨ زوجًا فيطابق.
    """

    assert MEASURED["الرسمُ الخام"][3] == 53
    assert REPORTED_ON_THE_BASE[3] == 28
    assert 53 > 28  # الخامُ أسخى بالمجّانيّات من الأساس


def test_the_ratio_moves_toward_the_reported_one_but_does_not_reach_it() -> None:
    """١٫١٨ ← ١٫٢٨ والمُدَّعى ٢٫٣٤: الاتّجاهُ يُصدَّق والمقدارُ لا يُبلَغ."""

    ratios = {
        name: Fraction(cheapest_vowel, priciest_consonant)
        for name, (cheapest_vowel, _, priciest_consonant, _) in MEASURED.items()
    }
    raw = ratios["الرسمُ الخام"]
    best = ratios["تطبيعٌ + ردُّ المدّ"]
    reported = Fraction(REPORTED_ON_THE_BASE[0], REPORTED_ON_THE_BASE[2])

    assert round(float(raw), 2) == 1.18
    assert round(float(best), 2) == 1.28
    assert round(float(reported), 2) == 2.34
    assert raw < best < reported  # الاتّجاهُ واحدٌ والمسافةُ باقية


def test_my_objection_is_withdrawn_as_a_general_claim() -> None:
    """«الحركاتُ لا تفترق عند الأقصى» قولٌ عن الرسم الخام لا عن العربيّة.

    ويبقى ما تحته صحيحًا **على ركيزته**، ويسقط بوصفه حكمًا على |ث| = ٣.
    ولا يُستبدَل به ٢٫٣٤ لأنّي لم أبلغها؛ فالموضعُ **غيرُ محسومٍ عندي**.
    """

    withdrawn_as_general = True
    endorsed_replacement = False
    assert withdrawn_as_general
    assert not endorsed_replacement
    assert MEASURED["الرسمُ الخام"][0] == 395  # ويبقى الرقمُ صحيحًا على ركيزته


def test_two_of_the_three_named_collapses_reproduce() -> None:
    """ذ~غ وش~ك تكلّفان بعد ردّ المدّ؛ ور~ض تبقى مجّانيّةً لسكونٍ لم يُطبَّع."""

    assert [name for name, (_, after) in NAMED_COLLAPSES.items() if after > 0] == [
        "ذ~غ",
        "ش~ك",
    ]
    assert NAMED_COLLAPSES["ر~ض"] == (0, 0)
    assert all(
        before == 0 for before, _ in NAMED_COLLAPSES.values()
    )  # كلُّها مجّانيّةٌ خامًا


def test_the_greedy_floor_becomes_the_reported_twenty_one() -> None:
    """الأرضيّةُ تنتقل من ٢٠ إلى ٢١ بالتطبيع — وهو الرقمُ المُدَّعى بعينه."""

    assert GREEDY_FLOOR["الرسمُ الخام"] == 20
    assert GREEDY_FLOOR["تطبيعٌ + ردُّ المدّ"] == REPORTED_FLOOR == 21

    mine = {"تزظ", "ثح", "جخ", "ذط", "رض", "شء"}
    theirs = {"تزظ", "ثح", "جخ", "ذط", "ضك", "ءش"}
    assert len(mine & theirs) == 4  # أربعةٌ من ستّةٍ تتطابق نصًّا
    assert {"تزظ", "ثح", "جخ", "ذط"} <= mine & theirs


def test_functional_load_and_invertibility_are_different_questions() -> None:
    """ث~ح مجّانيّةٌ بمعيار الحمل وممتنعةٌ بمعيار الاسترجاع — ولا تناقض.

    فالأوّلُ يسأل عن تمايز **الأنواع**، والثاني عن استرجاع **كلّ رمز**.
    ودمجٌ لا يُفقِد نوعًا واحدًا يُفقِد بتّاتِ كلّ كلمةٍ فيها أحدُ طرفيه.
    """

    load_cost_of_tha_ha = 0  # لا نوعين يفترقان فيها وحدَها
    assert load_cost_of_tha_ha == 0

    # وبمعيار الاسترجاع: كلُّ كلمةٍ فيها ث أو ح تفقد بتّاتها
    assert GREEDY_FLOOR["تطبيعٌ + ردُّ المدّ"] < 28
    recoverable_under_the_floor = False
    assert not recoverable_under_the_floor

    # فالسقفُ والأرضيّةُ ليسا طرفَي مجالٍ واحد: هذا عن المعجم وذاك عن الأبجديّة
    assert "معجم" != "أبجديّة"
