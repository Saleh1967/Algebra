"""**ختمٌ قبل النظر**: الترخيصُ الجبريُّ — ابتلاعٌ بلا بقيّة، وتوفيرٌ بالبتّ.

**لم يُشغَّل شيءٌ بعد.**

**الرخصةُ تُشدَّد**: رخصةُ `73cc5b24…` قبلت **التخشين** — طبقةً تُسقِط بتّاتٍ
وتُعلنها. وهذه **لا تقبله**. فالصعودُ الجبريُّ **إعادةُ تدوير**: الأعلى
**يبتلع** الأدنى فلا يبقى منه شيءٌ خارجَه، **ويوفّر** بتّاتٍ تُعَدّ. وما
لا يوفّر **ليس صعودًا بل إعادةَ تسمية**.

**ثلاثةُ بنودٍ مجتمعة**:

1. **الدالّيةُ الكلّيّة**: كلُّ وحدةٍ في L_k تدخل وحدةً من L_{k+1}، ولا
   وحدةَ تُترَك؛ وغيرُ الداخلِ **يُعَدّ باسمه**.
2. **الابتلاع (Δ = ٠)**: L_k **يُستعاد من L_{k+1} بلا بقيّةٍ ألبتّة** —
   لا قناةَ جانبيّةً ولا راية. وأيُّ فقدٍ **يُسقِط الرخصة**، ولو أُعلن.
3. **الاقتصاد**: `تكلفة(L_{k+1}) < تكلفة(L_k)` بالبتّ، والتكلفةُ **ذات
   شطرين** لئلّا تنحلّ: **معجمٌ + بيان**. فمعجمُ الطبقة يُهجّى بحروف
   الطبقة التي تحتها، وبيانُها إنتروبيتها في عدد وحداتها. وبلا شطر المعجم
   تصير «الكلمةُ الواحدةُ للمدوّنة كلِّها» صفرَ بتٍّ — وهو انحلالٌ لا علم.

**وقاعدةُ المقطع تُصلَح بما شخّصه `b8aa21e`**، وتُعلَن هنا قبل النظر:

- **ألفُ الوصل تُحذَف**: وحدةُ (ا، سكون) في مبتدأ كلمةٍ ليست مبتدأَ الآية
  **تُحذَف قبل التقطيع** — وهو ما تفعله العربيّةُ وصلًا.
- **ومبتدأُ الآية يُفتَح**: (ا، سكون) في أوّل الآية تُقرأ (ا، فتحة) فتفتح
  مقطعًا.
- **والتقطيعُ على الآية لا على الكلمة**: فالمقطعُ يعبر الوصلَ.

**والقياسُ محجوز**، والإنتروبيا تُقاس بقسمة الآيات الزوجيّة/الفرديّة.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="الصعودُ الجبريُّ المُرخَّص: ابتلاعٌ وتوفير",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "من L₀ (١١٢ وحدةً، `c5a1e18`) يُصعَد بطبقاتٍ كلُّ واحدةٍ تجميعٌ "
        "لما تحتها؛ وتُفحَص على ثلاثة: الدالّيةُ الكلّيّة، والابتلاعُ "
        "باستعادةٍ مطابقةٍ بلا قناةٍ جانبيّة، والاقتصادُ بتكلفةٍ ذات "
        "شطرين (معجمٌ مهجًّى بحروف الطبقة الأدنى + بيانٌ إنتروبيا في عدد)؛ "
        "وقاعدةُ المقطع بحذف ألف الوصل وفتحِ مبتدأ الآية والتقطيعِ على "
        "الآية؛ والإنتروبيا محجوزةٌ بقسمة الآيات الزوجيّة/الفرديّة"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ي١",
        statistic="نصيبُ وحدات L₀ غيرِ الداخلةِ في مقطعٍ بعد الإصلاح",
        threshold=Fraction(1, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "إصلاحي للقاعدة: إن بقي فوقَ واحدٍ من مئةٍ بعد حذف ألف الوصل "
            "والتقطيعِ على الآية، فتشخيصي في `b8aa21e` كان ناقصًا، "
            "ويُوقَف الصعودُ ثانيةً عند L₁"
        ),
    ),
    Prediction(
        identifier="ي٢",
        statistic="عددُ الوحدات التي لا تُستعاد مطابقةً من الطبقة الأعلى",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "بندَ الابتلاع: فقدٌ واحدٌ يكفي، ولا يُنقَذ بإعلانٍ ولا براية — "
            "فالطبقةُ حينئذٍ ظلٌّ لا مستوى"
        ),
    ),
    Prediction(
        identifier="ي٣",
        statistic="تكلفةُ L₁ مقسومةً على تكلفة L₀ (معجمًا وبيانًا)",
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "بندَ الاقتصاد عند أوّل صعود: إن لم يوفّر المقطعُ بتًّا واحدًا "
            "فهو إعادةُ تسميةٍ لا تجريد، ولا يُرخَّص"
        ),
    ),
    Prediction(
        identifier="ي٤",
        statistic="عددُ الصعودات المُرخَّصةِ فوق L₀ بالبنود الثلاثة",
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "تقديري أنا: إن رُخِّص أقلُّ من صعودين فالهرمُ طابقان لا أكثرُ، "
            "ويُنشَر سقفُه كذلك بلا تجميل"
        ),
    ),
    Prediction(
        identifier="ي٥",
        statistic="أدنى (الإنتروبيا المحجوزة − الملحَقة) على الطبقات (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies="اتّجاهَ الانتحال؛ وهو الدرسُ الذي سقطت به نتيجتي في `ca8fd2c`",
    ),
    Prediction(
        identifier="ي٦",
        statistic="عددُ الطبقات التي وُقِفَ عندها بسبب الاقتصاد وحدَه",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى أنّ للهرم سقفًا **يُحدّده العدُّ لا رأيي**: إن لم توقفه "
            "التكلفةُ عند طبقةٍ ما فالسقفُ لم يُبلَغ، ولا يُدَّعى بلوغُه"
        ),
    ),
)

DIGEST = "0021350c1d0f4b0a73a9d53613d65112352fec36947c518e2b1be4c8c4e16423"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_absorption_clause_admits_no_declared_loss() -> None:
    """ي٢ حدُّه صفرٌ — فالإعلانُ لا يُنقِذ فقدًا ههنا، بخلاف رخصة 73cc5b24."""

    absorb = next(one for one in PREDICTIONS if one.identifier == "ي٢")
    assert absorb.threshold == Fraction(0)
    assert absorb.direction is Direction.AT_MOST
    assert "ولا براية" in absorb.falsifies


def test_the_cost_has_two_parts_so_it_cannot_degenerate() -> None:
    """المعجمُ شطرٌ لازم — وبدونه تصير المدوّنةُ رمزًا واحدًا بصفر بتّ."""

    assert "معجمٌ + بيان" in __doc__ or "معجم" in ORACLE.extraction
    thrift = next(one for one in PREDICTIONS if one.identifier == "ي٣")
    assert thrift.threshold == Fraction(1)
    assert "إعادةُ تسميةٍ لا تجريد" in thrift.falsifies


def test_two_conditions_are_aimed_at_my_own_forecasts() -> None:
    """ي٤ وي٦ يُعرّضان تقديري لعدد الطبقات ولوجود سقفٍ يحدّده العدّ."""

    mine = [one for one in PREDICTIONS if one.identifier in {"ي٤", "ي٦"}]
    assert len(mine) == 2
    assert any("تقديري أنا" in one.falsifies for one in mine)
    assert any("يُحدّده العدُّ لا رأيي" in one.falsifies for one in mine)
