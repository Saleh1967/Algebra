"""الرسمُ المهمَل والمصائدُ — **طبقةٌ لها عقدٌ مُعلَن، جامعةٌ مانعة**.

**المسألة**: بايثون تعطي البايتَ والنقطة، **ولا تعطي الرسم**. فلا دالّةَ
في المكتبة المعياريّة تردُّ حرفًا إلى أصله الأعجم، ولا تعرف نوعَ الوصل،
ولا تميّز صورةَ عرضٍ من حرف. **فهذه الطبقةُ تُكتَب أو تبقى في الرؤوس.**

**والعقدُ ثلاثةُ بنود**:

① **`skeleton` تامّةٌ على مدخلها**: كلُّ نقطةٍ إمّا تُردّ إلى أصلها، أو
   تُحذَف لأنّها علامةُ ضبطٍ مُسمّاة، أو **تمرّ كما هي**. ولا نقطةَ تسقط
   صامتة. **ومجالُها مُعلَن**: `0x0600`–`0x06FF`؛ وما خرج عنه يمرُّ
   **ويُسمّيه `traps`** — فالتقسيمُ بين الدالّتين لا في واحدةٍ تفعل
   الأمرين.

② **`traps` تُسمّي ولا تُصلِح**: تردُّ أسماءَ ما وُجِد من ستِّ مصائد،
   **ولا تحذف ولا تُطبِّع**. فالإصلاحُ قرارٌ لصاحب النصّ لا للدالّة.

③ **لا تطبيعَ ههنا ألبتّة**: `NFC` يقلب ترتيبَ الشدّة والتنوين
   (`ccc` ٣٣ مقابل ٢٧–٢٩)، **فيُبطِل كلَّ فحصٍ يقرأ الجوار**. وهذه
   الوحدةُ لا تستدعيه ولا تُوصي به على متنٍ مختوم.

`THE_SKELETON_IS_NOT_A_LETTER_NAME`: **وحدُّها مُعلَن**. الهيكلُ **صورةُ
رسمٍ لا اسمُ حرف**: `skeleton` تجمع ب·ت·ث·ن·ي في أصلٍ واحد لأنّ الرسمَ
يجمعها، **ولا تقول إنّها حرفٌ واحد**. ومن قرأ الهيكلَ حرفًا فقد قرأ غيرَ
ما كُتِب.

`AND_A_TRAP_IS_A_PLACE_TO_LOOK_NOT_A_VERDICT`: و«مصيدةٌ» تعني **موضعًا
يُنظَر فيه**، لا خطأً مقضيًّا. فنصٌّ فارسيٌّ صحيحٌ تُسمّى صورُه، ولا
يُقال إنّه غلط.
"""

from __future__ import annotations

ARABIC = range(0x0600, 0x0700)
"""مجالُ الرسم المُعلَن — وما خرج عنه يمرُّ ويُسمّى."""

MARK: frozenset[int] = frozenset(range(0x064B, 0x0653)) | frozenset(
    {0x0653, 0x0654, 0x0655, 0x0670}
)
"""علاماتُ الضبط التي يحذفها الهيكل — مُسمّاةً بنقاطها لا بأسمائها."""

_FAMILIES: tuple[tuple[int, ...], ...] = (
    (0x0628, 0x062A, 0x062B, 0x0646, 0x064A),  # الأسنان
    (0x062C, 0x062D, 0x062E),
    (0x062F, 0x0630),
    (0x0631, 0x0632),
    (0x0633, 0x0634),
    (0x0635, 0x0636),
    (0x0637, 0x0638),
    (0x0639, 0x063A),
    (0x0641, 0x0642),
    (0x0627, 0x0623, 0x0625, 0x0622, 0x0649, 0x0671),
    (0x0629, 0x0647),
    (0x0624, 0x0626, 0x0621),
)

ARCHETYPE: dict[int, int] = {
    point: family[0] for family in _FAMILIES for point in family
}
"""كلُّ نقطةٍ في عائلةٍ تُردّ إلى أوّلها — والأوّلُ هو الأعجمُ رسمًا."""

TRAP: dict[str, frozenset[int]] = {
    "صور عرض": frozenset(range(0xFB50, 0xFF00)),
    "تطويل": frozenset({0x0640}),
    "محارف خفية": frozenset({0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0xFEFF, 0x00A0}),
    "صور فارسية": frozenset(
        {0x06CC, 0x06A9, 0x06BE, 0x067E, 0x0686, 0x0698, 0x06AF, 0x06C1, 0x06D2}
    ),
    "أرقام شرقية": frozenset(range(0x0660, 0x066A)) | frozenset(range(0x06F0, 0x06FA)),
    "خارج المجال": frozenset(),
}
"""ستُّ مصائدَ مُسمّاةٌ بنقاطها؛ والسادسةُ تُحسَب لا تُسرَد."""


class RasmError(ValueError):
    """مدخلٌ يُرَدّ — ويُسمّى سببُ الردّ."""


def is_mark(point: int) -> bool:
    """أعلامةُ ضبطٍ هي؟ — بالنقطة لا بالفئة، فلا تابعَ خارجيّ."""

    return point in MARK


def archetype(point: int) -> int:
    """أصلُ النقطة الأعجم — وما لا عائلةَ له يردُّ نفسَه."""

    return ARCHETYPE.get(point, point)


def skeleton(text: str) -> str:
    """الرسمُ المهمَل: تُحذَف العلاماتُ وتُردُّ الحروفُ إلى أصولها.

    **تامّةٌ على مدخلها**: ما ليس علامةً يمرُّ إمّا مردودًا أو كما هو،
    ولا نقطةَ تسقط بلا حكم.
    """

    return "".join(chr(archetype(ord(one))) for one in text if not is_mark(ord(one)))


def traps(text: str) -> tuple[str, ...]:
    """أسماءُ ما وُجِد من المصائد، مرتَّبةً — **تُسمّي ولا تُصلِح**."""

    points = {ord(one) for one in text}
    found = {
        name
        for name, members in TRAP.items()
        if name != "خارج المجال" and points & members
    }
    outside = {
        one
        for one in points
        if one not in ARABIC and one not in {0x0020, 0x000A, 0x0009}
    }
    if outside - set().union(*(TRAP[name] for name in TRAP if name != "خارج المجال")):
        found.add("خارج المجال")
    return tuple(sorted(found))


def trapped_points(text: str) -> dict[str, tuple[int, ...]]:
    """نقاطُ كلّ مصيدةٍ بعينها — فما سُمّي يُشار إليه."""

    points = sorted({ord(one) for one in text})
    return {
        name: tuple(one for one in points if one in members)
        for name, members in TRAP.items()
        if name != "خارج المجال" and any(one in members for one in points)
    }


def families() -> tuple[tuple[int, ...], ...]:
    """العائلاتُ كما أُعلِنت — تُقرَأ ولا تُبنى من خارج."""

    return _FAMILIES
