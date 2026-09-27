"""شُغِّل ختمُ `51bd90a4…`: **ثلاثةٌ من ثلاثة — والإعرابُ أوسعُ ما تفرّق به الحال**.

`THE_PAIRS`: الأزواجُ الدنيا **٢٬٣٣١**، منها في المقام (خمسُ وحداتٍ فأكثر)
**١٬٤٠٧**.

`THE_EDGES_HOLD`: م١ **صمد بفارقٍ ضيّق**: الأطرافُ الثلاثة ٠٫٧٧١٩ — والحدّ
٠٫٧٥، وكنتُ توقّعتُ قرابةَ ٠٫٨٥. م٢ **صمد**: ما يعطيه التساوي ٠٫٥١٨٠،
والزيادةُ ٠٫٢٥٣٨. م٣ **صمد**: الأخيرةُ ٠٫٧٢٢١ وحدها، وتسبق كلَّ موضعٍ غيرها
بـ٠٫٦٢٧٦.

`BUT_THE_VERB_SHAPE_IS_SMALL_AT_THE_SURFACE`: الأولى ٠٫٠٣٢٧ والثانية ٠٫٠١٧١
فقط. فالدعوى صمدت **بالإعراب لا بهيئة الفعل**؛ وما في الأوليين أكثرُه هيئةُ
حرفٍ أو فعل: «إِنَّ/أَنَّ»، و«آتَيْنَا/أَتَيْنَا» (أفعل وفعل)، و«آمَنُوا/
آمِنُوا» (ماضٍ وأمر).

`THE_MIDDLE_IS_THE_CASE_PUSHED_INWARD` — **تشخيصٌ بعد التشغيل، لا حكم**: من
أزواج الوسط **٣٢١**، **٢٤٩** يقع اختلافُها في الوحدة التي تسبق ضميرًا متّصلًا
(«قُلُوبُهُمْ/قُلُوبَهُمْ»، «رَبُّكُمْ/رَبِّكُمْ») — أي الإعراب نفسُه، دفعه
الضميرُ عن آخر اللفظ إلى آخر الكلمة. و**٤** بعد سابقةٍ مفتوحة («وَآمِنُوا/
وَآمَنُوا»). والباقي **٦٨** أكثرُه هيئةُ فعلٍ في داخله: المعلوم والمجهول
(«تُخْرِجُونَ/تُخْرَجُونَ»)، والماضي والأمر («اتَّبَعُوا/اتَّبِعُوا»).

فالسطحُ يعدّ مواضعَ **اللفظ**، والإعرابُ والهيئةُ يقعان على حدود **الكلمة**
داخلَه. وبحدود الكلمة تصير الأطرافُ **١٬٣٣٩ من ١٬٤٠٧** — وهذا تشخيصٌ لم يُختَم،
يحتاج ختمًا يعرّف حدَّ الكلمة قبل العدّ.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import combinations
from pathlib import Path
from types import ModuleType

from frozen_corpus import CORPUS, requires_corpus
from test_minimal_pairs_seal import DIGEST, ORACLE, PREDICTIONS

from algebra.signified import Verdict, seal

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_minimal_pairs.py"

pytestmark = requires_corpus

PAIRS = 2_331
SCOPE = 1_407
EDGES = 0.7719
UNIFORM = 0.5180
ABOVE_UNIFORM = 0.2538
LAST_LEAD = 0.6276
SHARES = {"الأخيرة": 0.7221, "الأولى": 0.0327, "الثانية": 0.0171, "الوسط": 0.2281}
FORECAST = 0.85
MIDDLE = 321
BEFORE_A_PRONOUN = 249
AFTER_A_PREFIX = 4
REST = 68
WORD_EDGES = 1_339
SUFFIXES = {"ه", "ها", "هم", "هن", "هما", "ك", "كم", "كن", "كما", "ي", "ني", "نا"}
PREFIXES = "وفبلك"


def _reader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_minimal_pairs", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@cache
def _types() -> dict[tuple[tuple[str, str], ...], str]:
    text = CORPUS.read_text(encoding="utf-8").rstrip("\n")
    return _reader().types(text)  # type: ignore[no-any-return]


@cache
def _verdicts() -> dict[str, Fraction]:
    reader = _reader()
    return reader.verdicts(reader.pairs(_types()))  # type: ignore[no-any-return]


def test_the_seal_was_deposited_before_the_run() -> None:
    """البصمةُ تُشتَقّ ثانيةً — ولم يُمَسّ شرطٌ بعد النظر."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST
    assert DIGEST.startswith("51bd90a4")


def test_the_edges_hold_narrowly() -> None:
    """م١ صمد: ٠٫٧٧١٩ فوق ٠٫٧٥ — ودون ما توقّعتُه."""

    found = _verdicts()
    assert (found["الأزواج"], found["المقام"]) == (PAIRS, SCOPE)
    first = next(one for one in PREDICTIONS if one.identifier == "م١")
    assert abs(float(found["م١"]) - EDGES) < 5e-5
    assert float(found["م١"]) < FORECAST
    assert first.verdict(found["م١"]) is Verdict.MET


def test_the_edges_beat_the_uniform_expectation() -> None:
    """م٢ صمد: فوق التساوي بـ٠٫٢٥٣٨."""

    found = _verdicts()
    second = next(one for one in PREDICTIONS if one.identifier == "م٢")
    assert abs(float(found["التساوي"]) - UNIFORM) < 5e-5
    assert abs(float(found["م٢"]) - ABOVE_UNIFORM) < 5e-5
    assert second.verdict(found["م٢"]) is Verdict.MET


def test_the_last_unit_leads_every_other_position() -> None:
    """م٣ صمد: الأخيرةُ وحدها ٠٫٧٢٢١."""

    found = _verdicts()
    third = next(one for one in PREDICTIONS if one.identifier == "م٣")
    assert abs(float(found["م٣"]) - LAST_LEAD) < 5e-5
    for name, value in SHARES.items():
        assert abs(float(found[name]) - value) < 5e-5
    assert third.verdict(found["م٣"]) is Verdict.MET


def test_the_middle_is_mostly_the_case_pushed_inward() -> None:
    """تشخيصًا: ٢٤٩ من ٣٢١ قبل ضميرٍ متّصل، و٤ بعد سابقة، و٦٨ غيرُهما."""

    groups: dict[tuple[str, ...], list[tuple[tuple[str, str], ...]]] = {}
    for kept in _types():
        groups.setdefault(tuple(letter for letter, _ in kept), []).append(kept)
    kinds: Counter[str] = Counter()
    for members in groups.values():
        for one, two in combinations(members, 2):
            where = [i for i, (a, b) in enumerate(zip(one, two, strict=True)) if a != b]
            if len(where) != 1 or len(one) < 5 or where[0] in (0, 1, len(one) - 1):
                continue
            index = where[0]
            tail = "".join(letter for letter, _ in one[index + 1 :])
            if tail in SUFFIXES:
                kinds["ضمير"] += 1
            elif one[0][0] in PREFIXES and index in (1, 2) and one[0][1] == "َ":
                kinds["سابقة"] += 1
            else:
                kinds["غيرهما"] += 1
    assert sum(kinds.values()) == MIDDLE
    assert (kinds["ضمير"], kinds["سابقة"], kinds["غيرهما"]) == (
        BEFORE_A_PRONOUN,
        AFTER_A_PREFIX,
        REST,
    )
    assert SCOPE - MIDDLE + BEFORE_A_PRONOUN + AFTER_A_PREFIX == WORD_EDGES


THE_BOUND_BINDS_BOTH_ARMS = False
"""أيَعَضُّ الحدُّ المُعلَنُ (خمسُ وحداتٍ فأكثر) الموضعين المقارَنين **بالسواء**؟ — لا.

الختمُ يقول إنّ الزوجَ الأدنى «يعزل» ما تفيده الحال. لكنّ حدَّ الطول يُدخل
الألفاظَ الطويلة، وأكثرُ طولها ضميرٌ متّصلٌ في آخرها، فيدفع الإعرابَ من
«الأخيرة» إلى «الوسط». فالحدُّ واحدٌ في قيمته، **يُنقص الأخيرةَ ويزيد الوسطَ**
— أي يعمل ضدّ م٣ لا معه؛ وم٣ صمد مع ذلك.
"""

THE_BOUND_EVIDENCE = (
    "من أزواج الوسط ٣٢١ في المقام، ٢٤٩ اختلافُها في الوحدة التي تسبق ضميرًا "
    "متّصلًا، أي إعرابٌ دفعه الضميرُ عن آخر اللفظ؛ فحدُّ الطول يميل على الأخيرة"
)

REASONING_NOT_SUPPORTED: tuple[str, ...] = ("م١",)
"""م١ مرّ وتعليلُه — «الإعرابُ وهيئةُ الفعل» — **لم يُؤيَّد في شطره الثاني**.

الأطرافُ صمدت بالأخيرة وحدها (٠٫٧٢٢١)؛ والأوليان معًا دون ٠٫٠٥. فهيئةُ الفعل
لا تظهر في أوّل **اللفظ** لأنّ السوابقَ تسبقها، ولا يُعرف موضعُها إلّا بحدّ
الكلمة. فالشطرُ الثاني من الدعوى يحتاج ختمًا آخر بعد تعريف ذلك الحدّ.
"""
