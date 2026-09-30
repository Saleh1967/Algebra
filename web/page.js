// وصلُ الصفحةِ بالوحدة. ولا حسابَ ههنا: الحسابُ كلُّه في `fold.js`،
// **فموضعٌ واحدٌ للعقدِ لا موضعان** (المادّةُ ٤٠).

import { Guarded, fold, unfold, foldAny, unfoldAny, bitsExactly, FoldingError } from "./fold.js";

const at = (id) => document.getElementById(id);
const whole = (id) => {
  const value = Number(at(id).value.trim());
  if (!Number.isInteger(value)) throw new FoldingError(`ليس صحيحًا: ${at(id).value}`);
  return value;
};

function show(where, text, bad = false) {
  const box = at(where);
  box.textContent = text;
  box.classList.toggle("bad", bad);
}

function guarded(run, where) {
  try {
    run();
  } catch (slip) {
    show(where, slip instanceof Error ? slip.message : String(slip), true);
  }
}

// `T(n)` على `Number` — للمقابلةِ لا للاستعمال
function looseCount(free, blocked, length) {
  let open = 1;
  let shut = 1;
  for (let m = 0; m < length; m += 1) {
    const nextOpen = free * open + blocked * shut;
    const nextShut = free * open;
    open = nextOpen;
    shut = nextShut;
  }
  return open;
}

at("do-count").addEventListener("click", () => guarded(() => {
  const free = whole("free");
  const blocked = whole("blocked");
  const length = whole("length");
  const shape = new Guarded(free, blocked);
  const exact = shape.count(length);
  const loose = looseCount(free, blocked, length);
  const same = exact.toString() === String(loose);
  show("out-count", [
    `T(${length}) = ${exact}`,
    `البتّاتُ المضبوطة = ${bitsExactly(shape, length)}`,
    `off(${length}) = ${shape.offset(length)}`,
    "",
    `Number   = ${loose}`,
    same ? "متطابقان ههنا — وهذا لا يدوم." : "**فارقَ Number، صامتًا.**",
  ].join("\n"), !same);
}, "out-count"));

at("do-fold").addEventListener("click", () => guarded(() => {
  const shape = new Guarded(whole("free"), whole("blocked"));
  const word = at("word").value.trim() === ""
    ? []
    : at("word").value.split(",").map((one) => {
        const value = Number(one.trim());
        if (!Number.isInteger(value)) throw new FoldingError(`رمزٌ ليس صحيحًا: ${one}`);
        return value;
      });
  const here = fold(shape, word);
  const anywhere = foldAny(shape, word);
  const back = unfold(shape, here, word.length).join(",");
  const whole_back = unfoldAny(shape, anywhere).join(",");
  const exact = back === word.join(",") && whole_back === word.join(",");
  show("out-fold", [
    `fold      = ${here}   من T(${word.length}) = ${shape.count(word.length)}`,
    `unfold    = ${back}`,
    `fold_any  = ${anywhere}`,
    `unfold_any= ${whole_back}`,
    "",
    exact ? "التقابلُ تامٌّ في الاتّجاهين." : "**اختلف الفكُّ عن الأصل — وهذا عطل.**",
  ].join("\n"), !exact);
}, "out-fold"));

at("do-unfold").addEventListener("click", () => guarded(() => {
  const shape = new Guarded(whole("free"), whole("blocked"));
  const index = BigInt(at("index").value.trim());
  const word = unfoldAny(shape, index);
  const again = foldAny(shape, word);
  show("out-unfold", [
    `الطول    = ${word.length}`,
    `الكلمة   = ${word.join(",")}`,
    `fold_any = ${again}`,
    "",
    again === index ? "عادَ العددُ بعينه." : "**لم يعُد العددُ — وهذا عطل.**",
  ].join("\n"), again !== index);
}, "out-unfold"));

// جدولُ الفراق، محسوبٌ عند التحميل
for (const [free, blocked] of [[5, 3], [2, 1], [10, 9]]) {
  const shape = new Guarded(free, blocked);
  let row = null;
  for (let length = 1; length < 60 && row === null; length += 1) {
    const exact = shape.count(length).toString();
    const loose = String(looseCount(free, blocked, length));
    if (exact !== loose) row = [length, exact, loose];
  }
  const line = document.createElement("tr");
  const cells = [`(${free}، ${blocked})`, row ? row[0] : "—", row ? row[1] : "—", row ? row[2] : "—"];
  cells.forEach((text, i) => {
    const cell = document.createElement("td");
    if (i > 1) cell.className = "n";
    cell.textContent = String(text);
    line.appendChild(cell);
  });
  document.querySelector("#divergence tbody").appendChild(line);
}
