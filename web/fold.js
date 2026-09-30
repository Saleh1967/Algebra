// الطيُّ والفكُّ في JavaScript — **بـ`BigInt` لا بـ`Number`**.
//
// العطلُ الذي يتجنّبه هذا الملفّ: `Number` في JavaScript هو `float64`
// بعينه، فمضبوطٌ على الصحاحِ إلى ٢⁵³ ثمّ يكذب صامتًا. وقد قِيس الحدُّ
// ثلاثَ مرّاتٍ في هذه الشجرة: `T(n)` للسلّمِ `G` يكسر الضبطَ عند `G8`
// = ١٦٨٦١٦٨٠٩٨٧٧٣٤٠١٦، ودليلُ سطرٍ من المدوّنةِ ٥٢٦٨ بتًّا — نحوَ
// ١٥٨٦ رقمًا عشريًّا. **فـ`Number` ههنا ليس تقريبًا بل سقوطٌ صامت.**
//
// ولهذا: كلُّ عددٍ ههنا `BigInt`، والمواضعُ والأطوالُ وحدَها `Number`
// لأنّها صغيرةٌ بطبعها ولا تُجمَع.
//
// وهذا الملفُّ **نقلٌ حرفيٌّ** لـ`src/algebra/folding.py`، ومطابقتُه
// مقيسةٌ في `tests/algebra/test_javascript_fold.py` بتشغيلِ التنفيذَين
// على المتّجهات نفسِها — **فلا يُقال «مطابق» بلا قياس**.

export class FoldingError extends Error {}

export class Guarded {
  constructor(free, blocked) {
    if (free < 1) throw new FoldingError("أبجديّةٌ بلا حرٍّ واحد — فلا كلمةَ جائزة.");
    if (blocked < 0) throw new FoldingError("عددُ المحجورين سالب.");
    this.free = free;
    this.blocked = blocked;
    this._memo = new Map();
  }

  get size() {
    return this.free + this.blocked;
  }

  isFree(symbol) {
    if (!(0 <= symbol && symbol < this.size))
      throw new FoldingError(`رمزٌ خارجَ الأبجديّة: ${symbol}`);
    return symbol < this.free;
  }

  admits(symbol, afterBlocked) {
    return afterBlocked ? this.isFree(symbol) : true;
  }

  // `S(m, …)` — صحيحٌ تامٌّ بـ`BigInt`، مع تذكيرٍ فالحلقةُ لا تُعاد.
  completions(length, openStart) {
    if (length < 0) throw new FoldingError(`طولٌ سالب: ${length}`);
    if (length === 0) return 1n;
    const key = `${length}:${openStart ? 1 : 0}`;
    const kept = this._memo.get(key);
    if (kept !== undefined) return kept;
    const free = BigInt(this.free) * this.completions(length - 1, true);
    const found = openStart
      ? free + BigInt(this.blocked) * this.completions(length - 1, false)
      : free;
    this._memo.set(key, found);
    return found;
  }

  // `T(n)`
  count(length) {
    return this.completions(length, true);
  }

  // `off(n) = Σ_{m<n} T(m)`
  offset(length) {
    if (length < 0) throw new FoldingError(`طولٌ سالب: ${length}`);
    let total = 0n;
    for (let m = 0; m < length; m += 1) total += this.count(m);
    return total;
  }
}

// الطيُّ: كلمةٌ جائزةٌ ← دليلٌ في `{0, …, T(n)−1}`
export function fold(shape, word) {
  const length = word.length;
  let index = 0n;
  let afterBlocked = false;
  for (let place = 0; place < length; place += 1) {
    const symbol = word[place];
    if (!shape.admits(symbol, afterBlocked))
      throw new FoldingError(`محجورٌ بعد محجورٍ في الموضع ${place}`);
    const rest = length - place - 1;
    // المجموعُ مُغلَقٌ لا حلقة — كما في النصِّ المُبرهَن
    index += BigInt(Math.min(symbol, shape.free)) * shape.completions(rest, true);
    if (!afterBlocked && symbol > shape.free)
      index += BigInt(symbol - shape.free) * shape.completions(rest, false);
    afterBlocked = !shape.isFree(symbol);
  }
  return index;
}

// الفكُّ: دليلٌ ← الكلمةُ بعينها. معكوسُ `fold` تمامًا.
export function unfold(shape, index, length) {
  if (length < 0) throw new FoldingError(`طولٌ سالب: ${length}`);
  const whole = shape.count(length);
  if (!(0n <= index && index < whole))
    throw new FoldingError(`دليلٌ خارجَ المدى: ${index} من ${whole}`);
  let left = index;
  let afterBlocked = false;
  const built = [];
  for (let place = 0; place < length; place += 1) {
    const rest = length - built.length - 1;
    const freeEach = shape.completions(rest, true);
    const freeBlock = BigInt(shape.free) * freeEach;
    let symbol;
    if (left < freeBlock) {
      symbol = Number(left / freeEach);
      left -= BigInt(symbol) * freeEach;
    } else {
      if (afterBlocked) throw new FoldingError("باقٍ فوق كتلةِ الأحرار بعد محجور");
      left -= freeBlock;
      const blockedEach = shape.completions(rest, false);
      symbol = shape.free + Number(left / blockedEach);
      left -= BigInt(symbol - shape.free) * blockedEach;
    }
    built.push(symbol);
    afterBlocked = !shape.isFree(symbol);
  }
  return built;
}

export function foldAny(shape, word) {
  return shape.offset(word.length) + fold(shape, word);
}

export function unfoldAny(shape, index) {
  if (index < 0n) throw new FoldingError(`دليلٌ سالب: ${index}`);
  let length = 0;
  let left = index;
  for (;;) {
    const here = shape.count(length);
    if (left < here) return unfold(shape, left, length);
    left -= here;
    length += 1;
  }
}

// عددُ البتّاتِ المضبوط: أصغرُ `k` بحيث `2^k ≥ T(n)` — **بلا لوغاريتم**،
// فاللوغاريتمُ على `float64` يكذب حيث يكذب `Number`.
export function bitsExactly(shape, length) {
  const whole = shape.count(length);
  let bits = 0;
  let reach = 1n;
  while (reach < whole) {
    reach *= 2n;
    bits += 1;
  }
  return bits;
}
