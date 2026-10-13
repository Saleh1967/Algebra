/-! مولَّدٌ بـ`tools/gen_madlul_shawahid.py` من الحاوية المختومة (بصمتُها
`360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd`)؛ لا يُحرَّر باليد. كلُّ عبارةٍ في سطرها
من النصّ المختوم المعتمد بعينها (ADR ٩). -/

namespace Madlul.Shawahid

/-- مرسًى: الكتاب، والسطر، والعبارةُ بعينها. -/
structure Marsa where
  book : String
  line : Nat
  phrase : String
  deriving DecidableEq, Repr

def containerSha256 : String := "360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd"

/-- شواهدُ الأقسام الخمسة والقسمة (س409–414). -/
def qismShawahid : List (String × Marsa) := [
  ("taqsim", ⟨"shakhsiyya-3", 409, "ينقسم اللفظ باعتبار المدلول وحده إلى خمسة أقسام"⟩),
  ("maana", ⟨"shakhsiyya-3", 410, "أن يكون المدلول معنى، أي شيئاً ليس بلفظ، كالحيوان وكزيد علماً على رجل"⟩),
  ("mufradMustamal", ⟨"shakhsiyya-3", 411, "أن يكون المدلول لفظاً مفرداً مستعملاً، مثل لفظ الكلمة"⟩),
  ("mufradMuhmal", ⟨"shakhsiyya-3", 412, "فحروف ضرب وهي: ضه، وره، وبه، لم توضع لمعنى"⟩),
  ("murakkabMustamal", ⟨"shakhsiyya-3", 413, "فإن مدلوله لفظ مركب موضوع، مثل زيد قائم"⟩),
  ("murakkabMuhmal", ⟨"shakhsiyya-3", 414, "وهو الهذيان"⟩),
  ("murakkabMuhmal", ⟨"shakhsiyya-3", 414, "وهذا القسم غير موضوع، أي لم تضعه العرب"⟩)
]

/-- شواهدُ أنواع المعنى (س406–407). -/
def nawShawahid : List (String × Marsa) := [
  ("jins", ⟨"shakhsiyya-3", 406, "فهو الجنس أي اسم الجنس"⟩),
  ("mushtaq", ⟨"shakhsiyya-3", 406, "فهو المشتق، كالأسود والفارس"⟩),
  ("alam", ⟨"shakhsiyya-3", 407, "فهو العلم، كزيد وكعبد الله"⟩),
  ("damir", ⟨"shakhsiyya-3", 407, "فهو المضمر، مثل هو وهي"⟩)
]

end Madlul.Shawahid
