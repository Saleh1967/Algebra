#!/usr/bin/env bash
# البوّابةُ الوحيدةُ المُعتمَدة — ولا يُوصَل مخرجُها بأنبوب.
#
# العطلُ الذي عالجه هذا الملفّ: كنتُ أكتب `pytest -q | tail -2 && git push`.
# ورمزُ خروجِ الأنبوب رمزُ آخرِ حلقةٍ فيه — `tail` — وهو صفرٌ دائمًا.
# فمرّ `&&` إلى الدفع والفحصُ ساقط. **ومن وصل الفحصَ بأنبوبٍ أبطل شرطَه.**
#
# فهذا الملفُّ يجمع البوّابات، و`set -e` يوقفه عند أوّل سقوط، ورمزُ خروجه
# رمزُ ما سقط. ويُستدعى وحدَه قبل كلّ دفعة.

set -euo pipefail

PY="${PY:-/tmp/claude-0/py310/bin/python}"

echo "— ruff check"
"$PY" -m ruff check .

echo "— ruff format --check"
"$PY" -m ruff format --check .

echo "— mypy --strict"
"$PY" -m mypy --strict src tools

echo "— pytest"
"$PY" -m pytest -q

echo "== البوّاباتُ كلُّها مرّت =="
