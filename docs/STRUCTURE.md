# البنية (Structure) — منسوخة من Saleh1967/Alghanem

> المصدر: `https://github.com/Saleh1967/Alghanem` عند الالتقاط `2e73e04` بتاريخ 2026-09-21.
> هذا الملف يصف **الهيكل** فقط. الدستور الكامل منسوخ حرفيًا في [`docs/CONSTITUTION.md`](CONSTITUTION.md).

## 1. ترتيب القراءة المعتمد في المصدر

`docs/VISION.md` → `docs/AIMS.md` → `docs/CONSTITUTION.md` → المصدر (`src/`) → الاختبارات (`tests/`) → كتلة الحالة المشتقة.

> المنسوخ هنا: `docs/CONSTITUTION.md` + الهيكل. ملفا `VISION.md` و`AIMS.md` لم يُنقلا (لم يُطلبا).

## 2. الشجرة العليا

```
.github
.gitignore
LICENSE
README.md
case_data
corpora
docs
examples
fonts
gloss_data
maqayis_by_root_csv_999.csv
pyproject.toml
src
tests
```

## 3. حزم المصدر (`src/alghanem/`)

| الحزمة | عدد وحدات `.py` |
|---|---|
| `src/alghanem` | 3 |
| `src/alghanem/arabic` | 194 |
| `src/alghanem/arabic/encoding` | 13 |
| `src/alghanem/arabic/fiber_contracts` | 2 |
| `src/alghanem/capability` | 16 |
| `src/alghanem/encyclopedia` | 4 |
| `src/alghanem/encyclopedia/self_observation` | 14 |
| `src/alghanem/evaluation` | 12 |
| `src/alghanem/evaluation_execution` | 7 |
| `src/alghanem/execution` | 18 |
| `src/alghanem/fractal_experiment` | 9 |
| `src/alghanem/fractal_generation` | 11 |
| `src/alghanem/generation` | 7 |
| `src/alghanem/kernel` | 32 |
| `src/alghanem/kernel/_internal` | 3 |
| `src/alghanem/linguistic` | 10 |
| `src/alghanem/metaalgebra` | 11 |
| `src/alghanem/ontology` | 5 |
| `src/alghanem/prior` | 4 |
| `src/alghanem/prior_fiber` | 7 |
| `src/alghanem/program` | 15 |
| `src/alghanem/realization` | 8 |
| `src/alghanem/realization/generated` | 1 |
| `src/alghanem/structural_bridge` | 2 |
| `src/alghanem/structural_dal` | 9 |

## 4. شجرة الاختبارات (`tests/`)

```
tests
tests/arabic
tests/capability
tests/encyclopedia
tests/encyclopedia/self_observation
tests/evaluation
tests/evaluation/readers
tests/evaluation_execution
tests/execution
tests/execution/fixtures
tests/fractal_experiment
tests/fractal_generation
tests/generation
tests/kernel
tests/linguistic
tests/metaalgebra
tests/ontology
tests/prior
tests/prior_fiber
tests/program
tests/realization
tests/structural_bridge
tests/structural_dal
```

## 5. الأمثلة (`examples/`)

```
examples
examples/arabic
examples/capability
examples/compression
examples/evaluation
examples/external_audit
examples/irab
examples/kernel
examples/letter_fingerprint
examples/level_two_manat
examples/prior_fiber
examples/reference
examples/sentence_card
examples/state_evidence
examples/structural_dal
```

## 6. بيانات ومراجع

```
case_data
case_data/cases
case_data/expectations
case_data/invalid
case_data/seam
corpora
docs
docs/reference
fonts
gloss_data
```

| المرجع في `docs/reference/` | الحجم |
|---|---|
| `arabic_identity_confusion_catalog.md` | 13147 بايت |
| `classical_makharij_ordering.md` | 9811 بايت |
| `gflk_arabic_letter_specification.md` | 38241 بايت |
| `lisan345_cluster_adjacency.md` | 9499 بايت |
| `phonetic_standing_closure.md` | 9319 بايت |
| `word_hierarchy_rebuild.md` | 26024 بايت |

## 7. سلسلة الأدوات (منسوخة حرفيًا)

- `pyproject.toml` — setuptools، تخطيط `src/`، Python ≥ 3.10، أدوات التطوير: `mypy==1.10.0`, `pytest==8.2.2`, `ruff==0.6.9`؛ `mypy` في وضع `strict`؛ `ruff` بطول سطر 88 وقواعد `E,F,I,UP`.
- `.github/workflows/ci.yml` — على `push` إلى `main` و`pull_request`: `pytest` ثم `ruff check .` ثم `ruff format --check .` ثم `mypy src`.

> تنبيه: سير عمل CI منسوخ كما هو. سيفشل ما دام `src/` و`tests/` هيكلًا فارغًا (`pytest` يخرج برمز 5 عند انعدام الاختبارات). احذفه أو عطّله حتى يُملأ الهيكل.

## 8. كيف نُسخ الهيكل هنا

- كل مجلد من مجلدات المصدر (76 مجلدًا) أُنشئ فارغًا ويحمل `.gitkeep` — لأن git لا يتتبّع المجلدات الفارغة.
- لم يُنسخ أي ملف مصدر `.py` ولا أي بيانات: المنقول هو **الهيكل + الدستور + إعدادات البناء** فقط.
- `docs/CONSTITUTION.md` منسوخ بايتًا ببايت (تطابق `md5`: `0499624968e0b1bac76862170c90e6ce`).
