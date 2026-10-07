"""ميزانُ ترميز الذرّة — مقيسٌ على مدوّنتنا، وفيه تصحيحُ ثابتٍ نقلتُه أنا.

**سجلٌّ مقيسٌ لا ختم**: يُحسَب ههنا ما يلزم البندَ الثامن من تسجيل الذرّة،
ويُشتَقّ من البايتات المختومة `37633090…` عند كلّ تشغيل — فلا رقمَ منقول.

`THE_INDEX_WIDTH_WAS_A_FOREIGN_CONSTANT_AND_I_CARRIED_IT`: وأوّلُ ما يُصحَّح
**خطأٌ منّي**: حسبتُ نقطةَ التعادل ومضاعفَ الفهرسة بعرض مدخلٍ **٢٢ بتًا**،
وهو عرضُ مدوّنتهم لا مدوّنتنا. ومقامُنا ٣٣١٬٢٥٩، و`⌈log₂ 331259⌉` =
**١٩**. فنقلتُ ثابتًا أجنبيًّا في الدفعة نفسِها التي مَنعتُ فيها نقلَ
الثوابت. والمصحَّحُ: `G` للحروف ٢٠٫٨١ وللذرّات **١٠٫٠٢**، ومضاعفُ فهرسة
السكون ٢٫٣٥× و**١٫١٣×**.

`THE_GOVERNING_UNIT_MUST_CARRY_ITS_OWN_CONSTANTS`: والبندُ الثامن يُعلِن
**الذرّةَ حاكمةً والحرفَ معايرًا**، ثمّ يُغلِق التشغيلَ بإنتروبيا **٤٫٠٤٩٣**
ومتوسّطِ طولٍ **٤٫٠٨٦٩** — وهما رقما **الحرف**. ورقما الذرّة **٦٫٠٧٦٢**
و**٦٫١٠٤٠**. فالوحدةُ الحاكمةُ تُحكِم ثوابتَها أيضًا، وإلّا أُغلِق التشغيلُ
ببصمة غير ما يُقاس.

`A_BOUNDARY_ATOM_CHANGES_EVERY_NUMBER_IN_THE_LEDGER`: ونصَّ التسجيلُ أنّ
**حدَّ الكلمة ذرّةٌ داخلُ التيار** — «لا يُخزَّن تيارٌ بلا ذرات حدٍّ» —
ثمّ أعلن الإغلاقَ **٣٣١٬٢٥٩ ذرّةً**، وهو عددُ الحروف بلا حدود. وحدودُ
الكلمات داخلَ الأسطر **٧٦٬٢٩٦**، فالمقامُ بها ٤٠٧٬٥٥٥ — **زيادةُ ٢٣٫٠٣٪**.
وبزيادته تتغيّر الإنتروبيا والوفوراتُ و`G` جميعًا. فإمّا أن يُحذَف شرطُ
ذرّة الحدّ، وإمّا أن يُعاد حسابُ الميزان عليه؛ والجمعُ بينهما تناقض.

`KRAFT_EQUALS_ONE_IS_PREFIX_FREEDOM_NOT_FIDELITY`: ويُشتَقُّ ههنا أنّ
كرافت = ١ في الترميزين. وذلك يبرهن **انعدامَ البادئة** فحسب؛ والوفاءُ
لبايتاتنا شرطُ تشغيلٍ في `verify_against_corpus`، لا خاصّةٌ في الشجرة.
"""

from __future__ import annotations

import heapq
import importlib.util
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

REPOSITORY = Path(__file__).resolve().parents[2]
READER = REPOSITORY / "examples" / "rasm" / "run_marked_contrast.py"

pytestmark = requires_corpus


def _stream() -> list[tuple[str, str]]:
    spec = importlib.util.spec_from_file_location("run_marked_contrast", READER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return list(module.read_stream(CORPUS.read_text(encoding="utf-8")))


def _code_lengths(counts: Counter[str]) -> dict[str, int]:
    """أطوالُ هافمان مبنيّةً بالأشجار، لا مقدَّرةً بالإنتروبيا."""

    lengths = {one: 0 for one in counts}
    nodes: list[tuple[int, int, tuple[str, ...]]] = [
        (number, index, (one,)) for index, (one, number) in enumerate(counts.items())
    ]
    heapq.heapify(nodes)
    step = len(nodes)
    while len(nodes) > 1:
        first = heapq.heappop(nodes)
        second = heapq.heappop(nodes)
        for one in first[2] + second[2]:
            lengths[one] += 1
        heapq.heappush(nodes, (first[0] + second[0], step, first[2] + second[2]))
        step += 1
    return lengths


class Ledger:
    """ميزانُ أبجديّةٍ واحدة: ثابتُها وهافمانُها وأرضيّتُها."""

    def __init__(self, symbols: list[str]) -> None:
        self.counts = Counter(symbols)
        self.places = len(symbols)
        self.width = math.ceil(math.log2(len(self.counts)))
        self.lengths = _code_lengths(self.counts)
        self.huffman = sum(self.counts[one] * self.lengths[one] for one in self.counts)
        self.fixed = self.places * self.width
        self.entropy = -sum(
            number / self.places * math.log2(number / self.places)
            for number in self.counts.values()
        )
        self.kraft = sum(2.0 ** -self.lengths[one] for one in self.counts)

    @property
    def savings(self) -> int:
        return self.fixed - self.huffman

    @property
    def mean_length(self) -> float:
        return self.huffman / self.places


STREAM = _stream()
LETTERS = Ledger([one for one, _ in STREAM])
ATOMS = Ledger([f"{one}|{kind}" for one, kind in STREAM])
SUKUN_MARKS = sum(1 for _, kind in STREAM if kind == "سكون")
INDEX_WIDTH = math.ceil(math.log2(len(STREAM)))
FOREIGN_WIDTH = 22
BOUNDARIES = 76_296


def test_the_index_width_is_nineteen_here_not_the_twenty_two_i_carried() -> None:
    """عرضُ المدخل دالّةٌ في المقام؛ ومقامُنا يعطي ١٩، ونقلتُ ٢٢."""

    assert len(STREAM) == 331_259
    assert INDEX_WIDTH == 19
    assert 2**18 < len(STREAM) <= 2**INDEX_WIDTH
    assert INDEX_WIDTH != FOREIGN_WIDTH
    assert math.ceil(math.log2(872_334)) == 20 != FOREIGN_WIDTH


def test_the_break_even_and_the_index_multiple_move_with_the_corrected_width() -> None:
    """بـ١٩: G للذرّات ١٠٫٠٢ ومضاعفُ الفهرسة ١٫١٣× — لا ١١٫٦٠ و١٫٣١×."""

    for ledger, expected_g, expected_multiple in (
        (LETTERS, 20.81, 2.35),
        (ATOMS, 10.02, 1.13),
    ):
        gap = INDEX_WIDTH * len(STREAM) / ledger.savings
        multiple = INDEX_WIDTH * SUKUN_MARKS / ledger.savings
        assert abs(gap - expected_g) < 0.05
        assert abs(multiple - expected_multiple) < 0.01
    # وبالعرض الأجنبيّ كانت ١١٫٦٠ و١٫٣١× — فالفرقُ من الثابت لا من المادّة
    assert abs(FOREIGN_WIDTH * len(STREAM) / ATOMS.savings - 11.60) < 0.05


def test_the_two_alphabets_carry_two_different_pairs_of_constants() -> None:
    """الحرفُ ٤٫٠٤٩٣/٤٫٠٨٦٩ والذرّةُ ٦٫٠٧٦٢/٦٫١٠٤٠ — ولا تُخلَطان."""

    assert abs(LETTERS.entropy - 4.0493) < 0.0001
    assert abs(LETTERS.mean_length - 4.0869) < 0.0001
    assert abs(ATOMS.entropy - 6.0762) < 0.0001
    assert abs(ATOMS.mean_length - 6.1040) < 0.0001
    # ومتوسّطُ الطول فوق الإنتروبيا دائمًا، وبأقلَّ من بتٍّ واحد
    for ledger in (LETTERS, ATOMS):
        assert 0 < ledger.mean_length - ledger.entropy < 1


def test_the_savings_are_measured_on_our_corpus_not_transferred() -> None:
    """١٨٫٢٦٪ حروفًا و٢٣٫٧٠٪ ذرّاتٍ — و١٦٫٩٪ رقمُ مدوّنةٍ أخرى."""

    letters_share = Fraction(LETTERS.savings, LETTERS.fixed)
    atoms_share = Fraction(ATOMS.savings, ATOMS.fixed)
    assert abs(float(letters_share) - 0.1826) < 0.0001
    assert abs(float(atoms_share) - 0.2370) < 0.0001
    assert atoms_share > letters_share
    assert LETTERS.width == 5 and ATOMS.width == 8
    assert len(ATOMS.counts) == 194 and len(LETTERS.counts) == 28


def test_both_codes_are_prefix_free_and_that_is_not_fidelity() -> None:
    """كرافت = ١ في الترميزين؛ والوفاءُ يُفحَص بالبصمة لا بكرافت."""

    for ledger in (LETTERS, ATOMS):
        assert abs(ledger.kraft - 1.0) < 1e-9
    digest_gate = "verify_against_corpus"
    assert digest_gate not in ("kraft", "prefix")


def test_a_boundary_atom_would_move_the_denominator_by_a_quarter() -> None:
    """٧٦٬٢٩٦ حدًّا داخلَ الأسطر: المقامُ ٤٠٧٬٥٥٥ — زيادةُ ٢٣٪ لا حاشية."""

    text = CORPUS.read_text(encoding="utf-8")
    boundaries = len(text.split()) - len(text.splitlines())
    assert boundaries == BOUNDARIES
    with_boundaries = len(STREAM) + boundaries
    assert with_boundaries == 407_555
    assert Fraction(22, 100) < Fraction(boundaries, len(STREAM)) < Fraction(24, 100)
