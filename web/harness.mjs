// مِرقاةُ القياس: تقرأ متّجهاتٍ بـJSON من المَدخَل وتكتب نتائجَها بـJSON.
//
// وغرضُها أن يُقاسَ التطابقُ بين التنفيذَين على **المُدخَلاتِ نفسِها**،
// فلا يُقال «نقلٌ حرفيّ» بلا قياس. ولا تطبع شيئًا سوى JSON واحدًا،
// **فمخرجٌ مُختلَطٌ لا يُفكّ**.
//
// والأعدادُ تُنقَل **نصًّا** لا أرقامًا: فـ`JSON.stringify` يكتب
// `BigInt` خطأً، و`JSON.parse` في بايثون يقرأ العددَ الكبيرَ صحيحًا
// بلا حدٍّ — أمّا في JavaScript فالعددُ الكبيرُ في JSON **يمرُّ على
// `Number` فيُقرَّب**. فالنصُّ هو المعبرُ الوحيدُ الذي لا يكذب.

import { Guarded, fold, unfold, foldAny, unfoldAny, bitsExactly } from "./fold.js";

const input = JSON.parse(await new Promise((done) => {
  let all = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (part) => { all += part; });
  process.stdin.on("end", () => done(all));
}));

const out = [];
for (const one of input) {
  const shape = new Guarded(one.free, one.blocked);
  if (one.kind === "count") {
    out.push({ value: shape.count(one.length).toString() });
  } else if (one.kind === "offset") {
    out.push({ value: shape.offset(one.length).toString() });
  } else if (one.kind === "bits") {
    out.push({ value: String(bitsExactly(shape, one.length)) });
  } else if (one.kind === "fold") {
    out.push({ value: fold(shape, one.word).toString() });
  } else if (one.kind === "unfold") {
    out.push({ value: unfold(shape, BigInt(one.index), one.length).join(",") });
  } else if (one.kind === "fold_any") {
    out.push({ value: foldAny(shape, one.word).toString() });
  } else if (one.kind === "unfold_any") {
    out.push({ value: unfoldAny(shape, BigInt(one.index)).join(",") });
  } else if (one.kind === "count_as_number") {
    // **الحالةُ المُكذِّبة**: العدُّ نفسُه على `Number` لا على `BigInt`.
    // فمتى فارق نصُّه نصَّ `BigInt` ثبت أنّ `BigInt` ضرورةٌ لا زينة.
    // `A(m) = f·A(m−1) + b·B(m−1)` و`B(m) = f·A(m−1)` — التكرارُ عينُه
    let open = 1;
    let shut = 1;
    for (let m = 0; m < one.length; m += 1) {
      const nextOpen = one.free * open + one.blocked * shut;
      const nextShut = one.free * open;
      open = nextOpen;
      shut = nextShut;
    }
    out.push({ value: String(open) });
  } else if (one.kind === "types") {
    // **حارسُ النوعِ نفسِه**: لو أُبدِل `BigInt` بـ`Number` يومًا صار
    // هذا `"number"` فسقط الفحص. فالحارسُ يقيس النوعَ لا يقرأ النصّ.
    out.push({
      value: [
        typeof shape.count(one.length),
        typeof shape.offset(one.length),
        typeof fold(shape, one.word),
        typeof foldAny(shape, one.word),
      ].join(","),
    });
  } else {
    out.push({ error: `نوعٌ غيرُ معروف: ${one.kind}` });
  }
}
process.stdout.write(JSON.stringify(out));
