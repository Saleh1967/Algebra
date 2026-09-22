# إشعار نقل — هذه الحزمة ليست شجرةً تعمل هنا

`src/alghanem/**` في هذا المستودع **إيداعُ نقلٍ لا حزمةٌ قابلة للاستيراد**.
الوحدات المكتوبة في هذه الجلسة موضوعةٌ بمساراتها في شجرة
[`Saleh1967/Alghanem`](https://github.com/Saleh1967/Alghanem) حتّى يكون نقلُها
نسخًا مباشرًا، لا أكثر.

**لمَ لا تُستورَد هنا؟** لأنّ `alghanem/__init__.py` و`alghanem/arabic/__init__.py`
في الشجرة الأصليّة يستوردان تسعًا وستّين وحدةً وما تحتها، ولم يُنسَخ منها شيء.
ونسخُها كلَّها يصنع **تفريعًا يتباعد عن أصله بصمت**، ثمّ يُستشهَد به بعد
جلساتٍ كأنّه الأصل. وكتابةُ `__init__.py` مختصرٍ هنا تصنع الشيءَ نفسَه بصورةٍ
أهدأ. فتُرِك الأمرُ مكشوفًا بدل أن يُسدَّ بتفريع.

**أين تُفحَص هذه الوحدات فعلًا؟** في نسخةٍ كاملةٍ من `Saleh1967/Alghanem`
تُنسَخ إليها هذه الملفّاتُ بمساراتها، وهناك تمرّ:

- `pytest` على المجموعة كاملة
- `ruff check .` و`ruff format --check .`
- `mypy src` في وضع `strict`

**ما الذي يفحصه CI في هذا المستودع؟** ما يملكه ويُشغّله فعلًا: حزمةَ
`src/hawk_dove` القائمةَ بذاتها واختباراتِها، مع `ruff` على الشجرة كلّها.
ولا يُشغَّل `pytest` ولا `mypy` على `src/alghanem` لأنّ تشغيلَهما عليها
يدّعي فحصًا لا يقع.

**الملفّات المنقولة** (تُنسَخ إلى الشجرة الأصليّة بمساراتها كما هي):

| المسار | ما فيه |
|---|---|
| `src/alghanem/arabic/makhraj_bit_decoder.py` | بتّاتُ المخرج ← حروفُ الخانة ونقاطُها |
| `src/alghanem/arabic/makhraj_haraka_bit_decoder.py` | محورُ الحركة، وكسبُ الفصل مقيسًا صفرًا |
| `src/alghanem/arabic/letter_identity_bit_codec.py` | مِرمازُ الهُويّة: بايتٌ لكلّ وحدة مشكولة |
| `src/alghanem/arabic/sifa_table_deposit.py` | عقدُ إيداع جدول الصفة، وقياسُ قوّة الفصل |
| `src/alghanem/arabic/slgae_deposit.py` | إيداعُ SLGAE الأولى، والتعارضان المُشتَقّان |
| `src/alghanem/arabic/slgae_second_version_deposit.py` | مراتبُ الادّعاء، وتدقيقُ جدول ماركوف |
| `src/alghanem/arabic/slgae_third_version_deposit.py` | تصادمُ معرِّف ٥ك وإغلاقُه بمعرِّفين، وفحوصُ ما نُشر |
| `src/alghanem/arabic/slgae_fourth_version_deposit.py` | جسرٌ بثلاثة مقادير، ونافذةٌ تتّزن |
| `src/alghanem/arabic/pre_articulatory_preregistration.py` | تسجيلٌ مسبقٌ لقاعدةٍ تحت المخرج، ومَسبارا ء/ع، والمانع |
| `src/alghanem/arabic/minimal_complete_slot_comparison.py` | مقابلةُ (C,H,B) بـ(a,g,p,r)، وعدُّ غير المولود بالاتّحاد |
| `src/alghanem/arabic/closure_window_reduction.py` | ردُّ Closure إلى s ≤ 1، وتطابقُ القسمتين |
| `src/alghanem/arabic/closure_identifiability.py` | تنفيذُ شرط الإبطال الرابع: العددُ لا يتعيّن |
| `src/alghanem/arabic/slot_rights_algebra.py` | جبرُ الحقوق بثلاث طبقات، مُشغَّلًا على المقاييس |
| `src/alghanem/arabic/composition_closure_replication.py` | إعادةُ إنتاج سقوط الإغلاق بصفريٍّ يحفظ شرطَيه |
| `src/alghanem/arabic/triangle_licensing_preregistration.py` | تسجيلُ المثلّث B₁₃ — مُسجَّلٌ ولا يُختبَر |
| `src/alghanem/arabic/interaction_complex_lemmas.py` | ل١ و ل٢ و ل٣ مفحوصةً عند كلّ استيراد، وحدٌّ مؤشَّر |
| `src/alghanem/arabic/movement_workbook_crosscheck.py` | فحصُ أرقام مصنَّف الحركة: عددٌ يُخفي سياسةً، وفحوصٌ تعريفيّةٌ لا تسقط |
| `src/alghanem/arabic/word_schema_falsification.py` | اختبارُ «كلمة = جذر + وزن + زوائد» بثلاثة شروطِ إبطالٍ مكتوبةٍ قبل النظر |
| `src/alghanem/arabic/decision_register.py` | القراراتُ الثلاثةُ مُفوَّضةً بفروعها وأثمانها، والوكيلُ مُسمًّى في غير حقل السلطة |

ومعها اختباراتُها في `tests/arabic/` وأمثلتُها في `examples/arabic/`.
