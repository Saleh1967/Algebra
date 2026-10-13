# ADR ٩ — بوّابةُ المدلول وحده: Algebra مقرُّها، مستقلّةً عن نواة الغانم (قرارُ المالك، 2026-10-14)

**القرار.** «نترك الغانم كما هو وفق بوّابةٍ دستوريّةٍ للدالّ وحده، ونختبر مستودعَ المدلول وحده بوّابةً موازيةً
للغانم ولها دستورٌ معلن… وبعدها نبني بوّابةً للدالّ والمدلول معًا بعد انتهاء المدلول وحده»؛ ثمّ: «Algebra هو
المقرّ للمدلول وحده» ومعه `QARAR_SEAT`.

**السند** (ج3 المختوم المعتمد، ADR ٦٠ في SLGE؛ والعباراتُ مولَّدةٌ ومطابَقةٌ بالبايت في `Madlul.Shawahid`):
* س409: «ينقسم اللفظ باعتبار المدلول وحده إلى خمسة أقسام»، والمدلولُ «قد يكون معنى، وقد يكون لفظاً».
* س410–414: شاهدُ كلّ قسم؛ والمهملُ بشاهدٍ موجِب («ضه، وره، وبه، لم توضع لمعنى»؛ الهذيانُ «غير موضوع»).
* س406–407: الكلّيُّ جنسٌ ومشتقّ، والجزئيُّ علمٌ وضمير.

**ما يترتّب.** أربعةٌ من الأقسام الخمسة مدلولُها لفظ، واللفظُ لا يدخل إلّا من الغانم؛ فالبوّابةُ لا تقرأ نصًّا
أبدًا، والقانونُ الواحد في `CLAUDE.md` قائمٌ بلا تعديل. ودستورُها المعلن: `docs/MADLUL_CONSTITUTION.md`.

**ما كُتب.**
* `formal/Madlul.lean` (لا يستورد إلّا `Madlul.Shawahid`):
  * `Madlul L N W`: المدلولُ بأقسامه الخمسة كلٌّ بشاهده، والمركّبُ لفظان فأكثر بالبنية.
  * `enter`/`exit` على مودَعٍ `Mawda`، والرفضُ المسمّى: `EMPTY_LAFZ_REF`، `MAANA_WITHOUT_WITNESS`،
    `ISTI_WITHOUT_WITNESS`.
  * مبرهنٌ لكلّ مودَعٍ ومرجع: `exit_enter`، `enter_agrees`، `enter_exit`، `absence_refused`،
    `muhmal_needs_witness`، `mufrad_iff_single`، `maana_iff_node`؛ و`qism_mem_all`، `all_nodup`.
  * مبرهنٌ على الشاهد: `every_qism_witnessed`، `every_naw_witnessed`.
* `formal/Madlul/Shawahid.lean`: يولّده `tools/gen_madlul_shawahid.py` من الحاوية f0025 ببصمتها (`360f7653…`)
  بباب SLGE المعتمد؛ كلُّ عبارةٍ في سطرها وإلّا `ANCHOR_NOT_IN_LINE`. وهذا هو «شاهدُ المهمل المودَع»: س412
  للمفرد وس414 للمركّب (`MUHMAL_WITNESS_NOT_DEPOSITED` مسدود).
* `formal/MadlulMain.lean` → `formal/madlul.csv` (43 سطرًا على مودَعٍ صغيرٍ ثابت)، ومرآتُه `src/madlul.py`.
* `tests/test_madlul.py`: الاستقلال، والجدولُ مرآةً، وصفوفٌ باليد، وأربعُ طفرات: `MUTANT_MADLUL_IMPORTS_A116`،
  `MUTANT_MUHMAL_FROM_ABSENCE`، `MUTANT_ONE_WORD_MURAKKAB`، `MUTANT_EXIT_REVERSES`.
* `docs/madlul/PREREG-juzi.md`: تسجيلٌ مسبق لمرجع الجزئيّ (QAC: PN، PRON) قبل أيّ رقم
  (`JUZI_REFERENCE_NOT_PREREGISTERED` مسدود).
* **رفعُ نواة الغانم المثبَّتة** `df76f39 → 2c7f18d` (فيها `Wad`، `Qarina`، `Qarar`، `Manhaj`) لمرحلة الجسر؛
  و`Harf`/`HarfBridge` يُبنيان ويُدقَّقان عليها كما كانا (`A116_PIN_PREDATES_WAD` مسدود).

**المرحلةُ الثانية (لم تبدأ).** `formal/DalMadlul.lean` يستورد `A116` و`Madlul`: علاقةُ الوضع (ف418 السبعة) بين
شهادة الغانم وشهادة المدلول؛ ومنها `A116.Wad` و`A116.Qarina` يُستهلكان من النواة المثبَّتة هنا، ولا يُحذفان من
الغانم («نترك الغانم كما هو»)، فيصير مقرُّهما الدلاليُّ الجسرَ ونسختُهما في الغانم مجمَّدة.

**ما بقي باسمه.**
* `WAD_SEAT_IN_DAL_REPO`: يُسدّ في المرحلة الثانية بالجسر هنا؛ لم يُنقل شيءٌ بعد.
* `MANHAJ_REGISTRY_NOT_WRITTEN`: سجلُّ قرارات المنهج مقرُّه هنا (`QARAR_SEAT`) ولم يُكتب.
* `MAANA_DEPOSIT_NOT_NAMED`: مودَعُ عُقَد المعنى (المرشَّح: «المخصَّص» في الغانم، ADR ٤٨) لم يُسمَّ بقرار.
* `HAMIL_SEAT_NOTE`: `hamil-constitution/README.md` يقول «مستودع المدلول وحده»؛ يُكتب هناك سطرٌ يحيل إلى هذا
  القرار.
