"""شُغِّل ختمُ `248f10df…`: **تسعةٌ من تسعة — والسلّمُ يقف عند الثانية**.

`THE_IN_SAMPLE_COST_FALLS_ALL_THE_WAY_AND_THE_HELD_OUT_TURNS`: ي٤ وي٥
صمدا معًا وهما متقابلان. الملحَقُ للوحدة ينزل بلا انقطاع
**٥٫٦٠٤٨ ⟶ ٣٫٦١٥٥ ⟶ ٢٫٤٩٢٦ ⟶ ٠٫٢١٥٤**؛ والمحجوزُ ينزل **ثمّ ينقلب**:
**٥٫٦٠٥٩ ⟶ ٣٫٦٥٤٩ ⟶ ٤٫٢١١٨ ⟶ ٦٫٩٣٦٩**.

`SO_THE_LADDER_PAYS_TO_THE_LICENSED_SYMBOL_AND_NO_FURTHER`: **أرخصُ
مستوًى محجوزًا هو `م١`** — الرمزُ المُرخَّصُ بقيدِ الفاصل — لا اللفظُ ولا
السطر. **فالتصعيدُ الجشع يربح إلى ما دون اللفظ، ويخسر عنده وفوقه.**

`AND_THE_TOKEN_STILL_BEATS_THE_BARE_UNIT_THOUGH_NOT_THE_SYMBOL`: وي٧
صمد: اللفظُ **٤٫٢١١٨** دون الوحدة **٥٫٦٠٥٩** — فهو يربح على القاع
ويخسر على `م١`. **والانقلابُ يقع بين `م١` و`م٢`، لا عند القاع.**

`AND_THE_LINE_IS_THE_WORST_OF_THE_FOUR`: وي٦ صمد: السطرُ **+١٫٣٣١٠**
فوق الوحدة. ومرتدُّه **٠٫٩٦٩٩** — فكلُّ سطرٍ يكاد يُهجّى من أوّله.

`AND_I_RISES_BUT_AS_OVERFITTING_NOT_AS_STRUCTURE`: وي٨ صمد: `I` ترتفع
**١٫٢٨٧٤ ⟶ ٤٫٣٧٩٨ ⟶ ٨٫١٢٥٥ ⟶ ١٢٫٤٤٧٥**. **وارتفاعُها عند السطر
انتحالٌ**: كلُّ سطرٍ فريدٌ فيعيّن تاليَه في العيّنة، والمرتدُّ ٠٫٩٦٩٩.

`AND_THE_THREE_PROVEN_BOUNDS_HELD_AT_EVERY_LEVEL`: ي١ وي٢ وي٣:
`L − H` في `[+٠٫٠٢٣٠، +٠٫٠٧٩١]`، و`N·H − log₂ تباديل` أدناه **+٧١٨٫٣**.

`AND_FOUR_LEVELS_ARE_CLASSIFIED_NOT_INVENTED`: وي٩ صمد: الكلمةُ المفردة،
والتركيبُ الإسناديّ، والتركيبُ المزجيّ، والجملة — **أربعةٌ**، كلُّها
`UNCLASSIFIED` بسببٍ مكتوب. **ولم يُسمَّ السطرُ جملةً ولا اللفظُ كلمة.**
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from test_markov_ladder_seal import DIGEST, ORACLE, PREDICTIONS, VACANT

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
LOG = REPOSITORY / "deposits" / "markov_ladder_run.log"
FLAWS = REPOSITORY / "docs" / "سجل-الأعطال.md"

INSIDE = (5.6048, 3.6155, 2.4926, 0.2154)
OUTSIDE = (5.6059, 3.6549, 4.2118, 6.9369)
FLOW = (1.2874, 4.3798, 8.1255, 12.4475)
MISSING = (0.0000, 0.0020, 0.1972, 0.9699)
COUNTS = (364_747, 135_603, 78_245, 6_236)


def _one(identifier: str) -> object:
    return next(one for one in PREDICTIONS if one.identifier == identifier)


def _exact(measured: float) -> Fraction:
    return Fraction(measured).limit_denominator(10**9)


def _rows() -> list[tuple[float, ...]]:
    found: list[tuple[float, ...]] = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        hit = re.match(
            r"^  م\d [^|]+\| (\d+) \| (\d+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) "
            r"\| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| \+([\d.]+) ",
            line,
        )
        if hit:
            found.append(tuple(float(one) for one in hit.groups()))
    return found


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("248f10df")


def test_the_four_levels_are_the_ones_the_bytes_license() -> None:
    """أربعةُ مستوياتٍ بأعدادها — والأبجديّةُ تنمو والمجرى ينكمش."""

    rows = _rows()
    assert len(rows) == 4
    assert tuple(int(one[0]) for one in rows) == COUNTS
    assert [one[0] for one in rows] == sorted(
        (one[0] for one in rows), reverse=True
    )  # المجرى ينكمش صعودًا
    alphabets = [int(one[1]) for one in rows]
    assert alphabets[:3] == sorted(alphabets[:3])  # وتنمو الأبجديّةُ إلى اللفظ
    assert alphabets[3] < alphabets[2]  # ثمّ تنكمش: الأسطرُ أقلُّ من ألفاظها
    assert alphabets[3] / COUNTS[3] > 0.97  # وكلُّ سطرٍ يكاد يكون فريدًا
    assert alphabets == [112, 2_952, 17_909, 6_057]


def test_the_three_proven_bounds_held_at_every_level() -> None:
    """ي١ وي٢ وي٣ — شانون وهوفمان وستيرلنغ، عند المستويات كلِّها."""

    text = LOG.read_text(encoding="utf-8")
    low = float(re.findall(r"أدنى L−H \+([\d.]+)", text)[0])
    high = float(re.findall(r"أقصى L−H \+([\d.]+)", text)[0])
    thin = float(re.findall(r"أدنى \(N·H − تباديل\): \+([\d.]+)", text)[0])
    assert _one("ي١").verdict(_exact(low)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ي٢").verdict(_exact(high)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ي٣").verdict(_exact(thin)) is Verdict.MET  # type: ignore[attr-defined]
    assert low > 0 and high < 1


def test_the_in_sample_falls_and_the_held_out_turns() -> None:
    """ي٤ وي٥ متقابلان، وصمدا معًا — فالانقلابُ انتحالٌ لا مادّة."""

    text = LOG.read_text(encoding="utf-8")
    inside = float(re.findall(r"أقصى ارتفاعٍ للملحَق صعودًا: (-?[\d.+]+)", text)[0])
    outside = float(re.findall(r"أقصى ارتفاعٍ للمحجوز صعودًا: \+([\d.]+)", text)[0])
    assert _one("ي٤").verdict(_exact(inside)) is Verdict.MET  # type: ignore[attr-defined]
    assert _one("ي٥").verdict(_exact(outside)) is Verdict.MET  # type: ignore[attr-defined]
    assert inside < 0 and outside > 0
    rows = _rows()
    assert [one[7] for one in rows] == sorted((one[7] for one in rows), reverse=True)


def test_the_cheapest_level_held_out_is_the_licensed_symbol() -> None:
    """أرخصُ مستوًى محجوزًا `م١` — لا اللفظُ ولا السطر."""

    rows = _rows()
    held = [one[8] for one in rows]
    assert held.index(min(held)) == 1
    for index, value in enumerate(OUTSIDE):
        assert abs(held[index] - value) < 5e-5, index
    assert held[2] > held[1] and held[3] > held[2]


def test_the_token_beats_the_unit_but_not_the_symbol() -> None:
    """ي٧: ٤٫٢١١٨ دون ٥٫٦٠٥٩ — والانقلابُ بين `م١` و`م٢`."""

    apart = OUTSIDE[2] - OUTSIDE[0]
    assert _one("ي٧").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    assert apart < 0
    assert OUTSIDE[2] > OUTSIDE[1]


def test_the_line_is_the_worst_and_its_escape_share_says_why() -> None:
    """ي٦: +١٫٣٣١٠ فوق الوحدة، ومرتدُّه ٠٫٩٦٩٩."""

    apart = OUTSIDE[3] - OUTSIDE[0]
    assert _one("ي٦").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    rows = _rows()
    assert abs(rows[3][5] - MISSING[3]) < 5e-5
    assert rows[3][5] > 0.96


def test_the_flow_rises_but_as_overfitting() -> None:
    """ي٨: `I` ترتفع ١١٫١٦٠١ — وارتفاعُها عند السطر انتحال."""

    text = LOG.read_text(encoding="utf-8")
    apart = float(re.findall(r"I في القمّة − في القاع: \+([\d.]+)", text)[0])
    assert _one("ي٨").verdict(_exact(apart)) is Verdict.MET  # type: ignore[attr-defined]
    rows = _rows()
    for index, value in enumerate(FLOW):
        assert abs(rows[index][6] - value) < 5e-5, index
    assert "انتحالٌ لا بنية" in _one("ي٨").falsifies  # type: ignore[attr-defined]


def test_four_levels_above_the_bytes_are_classified_not_invented() -> None:
    """ي٩: أربعةٌ `UNCLASSIFIED` بأسبابها — ولا يُسمّى السطرُ جملةً."""

    text = LOG.read_text(encoding="utf-8")
    named = re.findall(r"^  (\S[^:]*): UNCLASSIFIED — (.+)$", text, re.MULTILINE)
    assert len(named) == VACANT == 4
    assert _one("ي٩").verdict(Fraction(abs(len(named) - VACANT))) is Verdict.MET  # type: ignore[attr-defined]
    for _name, why in named:
        assert len(why) > 25
    assert "جملتُها: 4" in text


def test_the_conflation_is_recorded_in_the_flaw_ledger() -> None:
    """اللفظُ سُمّي كلمةً — والعدُّ صحيحٌ والاسمُ خطأ."""

    written = FLAWS.read_text(encoding="utf-8")
    assert "اللفظُ سُمّي كلمةً — خلطُ مستويين" in written
    assert "والعدُّ صحيحٌ والاسمُ خطأ" in written
    assert "شحنُ المرتدّ بما لا يُفَكّ" in written


def test_nine_of_nine() -> None:
    """أوّلُ ختمٍ يصمد تامًّا منذ `34133d54…`."""

    met = {one.identifier for one in PREDICTIONS}  # type: ignore[attr-defined]
    assert len(met) == 9
