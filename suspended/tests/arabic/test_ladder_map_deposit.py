"""الخريطةُ أُودِعت — وهي **إيداعٌ حقيقيّ**، ولكنّها ليست ما يقوله عنوانُها.

**الفضلُ أوّلًا**: ما غاب عن خ٢ حتّى أبطله — جدولٌ حرفًا حرفًا بتوقيع راويه —
أُودِع ههنا. وذلك فعلٌ لا يملكه إلّا صاحبُه، وقد فعله. وما دونَه في هذا
الملفّ تدقيقٌ للمُودَع، لا ردٌّ لإيداعه.

`THE_MAP_CARRIES_TWENTY_NINE_LETTERS_WHILE_THE_UNIT_DECLARES_TWENTY_EIGHT`:
عنوانُها «خريطة ٢٨ ← ١٧»، وصفوفُها **تسعةٌ وعشرون**: الهمزةُ المفردةُ «ء»
صفٌّ مستقلٌّ في الموضع ٢ مع الألف. ووحدةُ العدّ (و٢) تقول «٢٨ حرفًا بتطبيع
phon، **الهمزة مدموجة في الألف**». فإمّا أن تُدمَج فيسقط صفُّها، وإمّا أن
تُفرَد فيصير العدُّ ٢٩ وتنتقض و٢ وكلُّ رقمٍ بُني على ٢٨.

`SEVENTEEN_IS_THE_TITLE_AND_THIRTEEN_IS_THE_LADDER`: والمواضعُ المستعملةُ
**ثلاثةَ عشرَ** (٢…١٤)، والخالياتُ ١ و١٥ و١٦ و١٧. وهذا **متّسقٌ مع
الإسقاطين المُعلَنين** (الجوفُ صفةُ مدّ، والخيشومُ غنّة) — فلا اعتراضَ على
الخلوّ. والاعتراضُ أنّ السلّمَ الفاعلَ ثلاثةَ عشرَ موضعًا، فيُسمّى بعدده
لا بعدد المرجع، وإلّا حُسِبت سعةُ الحقل على ١٨ وهي ١٤.

`THE_REFERENCE_DIVISION_IN_THE_HEADER_IS_NOT_THE_RECEIVED_SEVENTEEN`:
ورأسُ الملفّ يقسم السبعةَ عشرَ: الجوفُ ١ · الحلقُ ٢‑٤ · اللسانُ ٥‑١٢ ·
الشفتانِ ١٣‑١٤ · الخيشومُ ١٥‑١٧. والمجموعُ سبعةَ عشرَ صحيحًا، **والقسمةُ
ليست قسمةَ الجزريّ**: اللسانُ عنده **عشرةُ مواضع** والخيشومُ **واحد**.
فنُقِل من اللسان موضعان إلى الخيشوم، ووقع في المُودَع دمجان يفرّقهما
المرويّ: **ض مع ج ش ي** (حافةُ اللسان مع وسطه)، و**ل مع ن** (وهما موضعان
متمايزان عنده). فالمُودَعُ **إعادةُ بناءٍ** لا روايةً، ويُعلَن كذلك أو
يُصحَّح — إذ «ص ٥٧‑٥٨» في صفّ الضاد وحدَها شاهدٌ على أنّ مصدرَها غيرُ
مصدر الثلاثة التي جُمِعت معها.

`FOUR_ROWS_CARRY_NO_PAGE_AT_ALL`: ودعوى «إسنادِ صفحةٍ لكلّ حرف» **لا تصدق
على أربعة**: ف وب وم وو حقلُ صفحتها «ص (باطن الشفة)» و«ص (الشفتان)» —
وصفُ موضعٍ لا رقمُ صفحة. وأربعةٌ من تسعةٍ وعشرين ليست حاشية.
"""

from __future__ import annotations

from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
DEPOSIT = REPOSITORY / "deposits" / "ladder_map.tsv"

BASE = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
DECLARED_LETTERS = 28
DECLARED_LADDER = 17
RECEIVED_TONGUE_PLACES = 10  # الجزريّ: ١ جوف + ٣ حلق + ١٠ لسان + ٢ شفتان + ١ خيشوم
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩0123456789"


def _rows() -> list[tuple[str, int, str]]:
    out: list[tuple[str, int, str]] = []
    for line in DEPOSIT.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith(("#", "letter")):
            continue
        parts = line.split("\t")
        out.append((parts[0].strip(), int(parts[1]), parts[2].strip()))
    return out


ROWS = _rows()


def test_the_deposit_exists_and_names_every_letter_of_the_alphabet() -> None:
    """الإيداعُ واقعٌ، ويغطّي الأبجديّةَ كلَّها — وهذا ما غاب عن خ٢."""

    assert DEPOSIT.is_file()
    assert set(one for one, _, _ in ROWS) >= set(BASE)
    assert all(1 <= place <= DECLARED_LADDER for _, place, _ in ROWS)


def test_the_map_has_twenty_nine_rows_against_a_unit_that_declares_twenty_eight() -> (
    None
):
    """«ء» صفٌّ مستقلٌّ مع أنّ و٢ تدمجها في الألف — عدّان لا عدّ."""

    letters = [one for one, _, _ in ROWS]
    assert len(letters) == len(set(letters)) == 29
    assert len(set(letters) - set(BASE)) == 1
    assert set(letters) - set(BASE) == {"ء"}
    assert not set(BASE) - set(letters)
    assert len(BASE) == DECLARED_LETTERS


def test_the_working_ladder_is_thirteen_places_not_seventeen() -> None:
    """المستعملُ ٢…١٤، والخالي ١ و١٥‑١٧ — وهو متّسقٌ مع الإسقاطين."""

    used = sorted({place for _, place, _ in ROWS})
    assert used == list(range(2, 15))
    assert len(used) == 13
    assert [one for one in range(1, 18) if one not in used] == [1, 15, 16, 17]
    # وسعةُ حقل الحاجز تُحسَب على ١٣ + حدُّ الكلمة = ١٤، لا على ١٨
    assert len(used) + 1 == 14 < 18


def test_two_merges_depart_from_the_received_division() -> None:
    """ض مع ج ش ي، ول مع ن — والمرويُّ يفرّقهما؛ فالمُودَعُ إعادةُ بناء."""

    groups: dict[int, str] = {}
    for one, place, _ in ROWS:
        groups[place] = groups.get(place, "") + one
    assert groups[7] == "جشيض"  # وسطُ اللسان وحافتُه في موضعٍ واحد
    assert groups[12] == "لن"  # واللامُ والنونُ كذلك

    tongue = [place for place in groups if 5 <= place <= 12]
    assert len(tongue) == 8 < RECEIVED_TONGUE_PLACES
    # والضادُ وحدَها تحمل صفحةً غيرَ صفحة من جُمِعت معهم
    pages = {one: page for one, place, page in ROWS if place == 7}
    assert pages["ض"] != pages["ج"] == pages["ش"] == pages["ي"]


def test_four_rows_carry_a_place_description_instead_of_a_page() -> None:
    """ف ب م و: «ص (الشفتان)» وصفُ موضعٍ لا رقمُ صفحة — وأربعةٌ ليست حاشية."""

    without = [
        (one, page)
        for one, _, page in ROWS
        if not any(digit in page for digit in ARABIC_DIGITS)
    ]
    assert [one for one, _ in without] == ["ف", "ب", "م", "و"]
    assert len(without) == 4
    assert all("ص" in page for _, page in without)
    # وسائرُ الصفوف تحمل رقمًا، فالنقصُ في هذه الأربعة لا في الصيغة
    assert len(ROWS) - len(without) == 25
