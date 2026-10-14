# Algebra — مستودعُ «المدلول وحده»

هذا المستودعُ **المرحلةُ الثانية** من ثلاث مراحل قرّرها صاحبُ المستودع (2026-10-14). والمراحلُ على قسمة النبهانيّ
للّفظ في «الشخصيّة الإسلاميّة» ج3:

| المرحلة | القسمة | المستودع |
|---|---|---|
| ١ | الدالُّ وحده | [`Saleh1967/Alghanem`](https://github.com/Saleh1967/Alghanem) — البوّابة `gate.enter`/`gate.exit` وبرهانُها `formal/a116` |
| **٢** | **المدلولُ وحده** (س409) | **هنا** — `formal/Madlul.lean` (ADR ٩) |
| ٣ | الدالُّ والمدلول معًا (ف418)، وسجلُّ القرار، وطبقةُ الحكم | [`Saleh1967/dal-madlul-constitution`](https://github.com/Saleh1967/dal-madlul-constitution) (ADR ١٠ هنا، ADR ٧ هناك) |

## القانونُ الواحد

**لا يدخل نصٌّ هذا المستودعَ ولا يخرج منه إلّا من بوّابة الغانم.** وبوّابةُ المدلول هنا لا تقرأ نصًّا أبدًا: مدخلُها مرجعٌ
إلى ما دخل من الغانم (ألفاظٌ بأعداد شهاداتها) أو إلى عقدةِ معنًى في مودَعٍ مختوم. ودستورُها المعلن
[`docs/MADLUL_CONSTITUTION.md`](docs/MADLUL_CONSTITUTION.md)، والتعليماتُ الملزِمة لكلّ وكيل في [`CLAUDE.md`](CLAUDE.md).

## ما في الشجرة الحيّة

| الموضع | ما هو | وسمُه |
|---|---|---|
| `src/entry.py` | المدخلُ الوحيد: ذرّاتُ شهادة الغانم ← خانات، وعكسُها | مفحوص (`tests/test_harf_binary.py`) |
| `formal/Harf.lean`، `formal/Harf/` | آلةُ الحرف والمقاطع بتعريفات Algebra، **بلا استيرادٍ من نواة الغانم** (ADR ٣) | مبرهن (`Audit.lean`) |
| `formal/HarfBridge.lean`، `formal/HarfBridge/` | التكافؤُ مع قيد الحدّ في الغانم: الكلمة والكلمتان والسطرُ ومودَعُ السياق والقطعة (ADR ٣–٨) | مبرهن (`Audit.lean`) |
| `formal/Madlul.lean`، `formal/Madlul/Shawahid.lean` | **بوّابةُ المدلول وحده**: الأقسامُ الخمسة، والمعنى كلّيٌّ أو جزئيّ، و`enter`/`exit` بشاهد، والرفضُ المسمّى؛ بلا استيرادٍ من النواة ولا من `Harf` (ADR ٩، ١٠) | مبرهن (`Audit.lean`)؛ الشواهدُ مطابَقةٌ بالبايت على الحاوية المختومة |
| `src/madlul.py`، `formal/madlul.csv` | مرآةُ البوّابة وجدولُها الذي يطبعه Lean | مفحوص (`tests/test_madlul.py`، بأربع طفرات) |
| `formal/binary.csv` | جدولُ الثنائيّ الذي يطبعه Lean | مطابَق (`tests/test_harf_binary.py`) |
| `tools/guard.py`، `tools/gen_registry.py`، `tools/gen_tree_index.py`، `tools/gen_madlul_shawahid.py` | الحارس، وسجلُّ المعلَّق، والشجرةُ المرخَّصة (ADR ٢)، ومولِّدُ الشواهد | مفحوص في CI |
| `docs/adr/` | القرارات (ADR ١–١٠) | معلن |

ونواةُ الغانم مثبَّتةٌ بإيداعٍ بعينه في `formal/lakefile.toml`، ولا يقرؤها إلّا `HarfBridge`.

## ما ليس حيًّا

* **`suspended/`**: كلُّ ما كان يقرأ النصَّ أو يكتبه أو يطبّعه أو يقيس عليه مباشرة، نُقل إليه في 2026-10-07 (ADR ١)، نقلًا لا
  حذفًا، وسجلُّه المولَّد [`SUSPENDED_REGISTRY.json`](SUSPENDED_REGISTRY.json): لكلّ وحدةٍ مسارُها القديم وسببُها وشرطُ عودتها.
  لا يُستورد منه شيءٌ ولا يُشغَّل.
* **الوثائقُ العربيّةُ الأسماء في `docs/`** (مثل `مدخل.md`، `السلّم-المجمَّد.md`): كتبتها أدواتٌ صارت معلَّقة، وأرقامُها أرقامُ ما
  قبل البوّابة. هي سجلٌّ تاريخيّ لا دعوى قائمة.
* **الجذرُ السابق** و«الاعتمادُ بالوكالة» (2026-09-26): محفوظان بعينهما في
  [`docs/history/README-2026-09.md`](docs/history/README-2026-09.md).

## الفحص

```sh
python3 tools/gen_registry.py --check && python3 tools/guard.py && python3 tools/gen_tree_index.py --check && python3 -m pytest tests -q
(cd formal && lake build && lake env lean Audit.lean && lake exe harf-table > binary.csv && git diff --exit-code binary.csv)
(cd formal && lake exe madlul-table > madlul.csv && git diff --exit-code madlul.csv) && python3 tools/gen_madlul_shawahid.py --check
```

وهي ما يشغّله CI (`.github/workflows/ci.yml`)، ومعه رفضُ أيّ `sorry` أو `native_decide` أو مسلَّمةٍ غيرِ
`propext`/`Classical.choice`/`Quot.sound`، وأسماءُ المبرهنات المدقَّقة. و`tools/gen_madlul_shawahid.py` يقرأ حاويةَ ج3 من
نسخة الغانم التي يجلبها `lake build`، فلا يُشغَّل قبله.

## الوسوم

«مبرهن» لما في Lean باسمه مدقَّقَ المسلّمات، و«مفحوص» لما له اختبارٌ باسمه بتوقّعاتٍ مستقلّة وطفرة، و«مطابَق» لجدولٍ يطبعه
Lean ويطابقه اختبار، و«مقيس» لرقمٍ على مرجعٍ محجوب — ولا مقيسَ في هذا المستودع بعد. وما سوى ذلك «معلن».
