import Madlul.Shawahid

/-!
# بوّابةُ المدلول وحده (ADR ٩): الشخصيّة الإسلاميّة ج3، المختومُ س404–414

«ينقسم اللفظ باعتبار المدلول وحده إلى خمسة أقسام: أحدها أن يكون مدلول اللفظ معنى، والثاني أن يكون لفظاً
مفرداً مستعملاً، والثالث أن يكون لفظاً مفرداً مهملاً، والرابع أن يكون لفظاً مركباً مستعملاً، والخامس أن يكون
لفظاً مركباً مهملاً» (س409). والمعنى «تقدم انقسامه إلى كلي وجزئي» (س410): الكلّيُّ جنسٌ ومشتقّ (س406)،
والجزئيُّ علمٌ وضمير (س407).

**لا يستورد هذا الملفُّ نواةَ الغانم** (على نسق `Harf`، ADR ٣). اللفظُ `L` والعقدةُ `N` والشاهدُ `W` معاملاتٌ
مجرّدة: البوّابةُ لا تقرأ نصًّا، بل مرجعًا إلى ما دخل من بوّابة الغانم (عددُ شهادة) أو إلى عقدةٍ في مودَعٍ مختوم.

* `Madlul`: المدلولُ بأقسامه الخمسة، كلٌّ يحمل شاهدَه؛ والمركّبُ لفظان فأكثر بالبنية.
* `qism_mem_all`، `all_nodup`، `all_length`: الأقسامُ خمسةٌ جامعةٌ مانعة.
* `enter`، `exit`: البوّابةُ على مودَعٍ (`Mawda`) يقول لكلّ مرجعٍ شاهدَه؛ وما لا شاهدَ له رفضٌ باسمه.
* `exit_enter`، `enter_exit`: الدخولُ ثمّ الخروج يعيد المرجعَ بعينه، والخروجُ ثمّ الدخولُ يعيد المدلولَ بعينه
  إذا كان شاهدُه شاهدَ المودَع.
* `absence_refused`، `muhmal_needs_witness`: **المهملُ لا يُستنتج من الغياب** (المادّة ١٦): ما لا شاهدَ له
  يُرفض، وكلُّ مهملٍ يخرج يحمل شاهدَ إهمالٍ من المودَع.
* `mufrad_iff_single`: المفردُ ما مرجعُه لفظٌ واحد، والمركّبُ ما مرجعُه لفظان فأكثر.
* `every_qism_witnessed`، `every_naw_witnessed`: لكلّ قسمٍ ولكلّ نوعٍ من المعنى شاهدٌ من نصّ النبهانيّ بسطره
  (`Madlul.Shawahid`، مولَّدٌ من الحاوية المختومة ومطابَقٌ ببايتاتها).
-/

set_option autoImplicit false

namespace Madlul

/-- الكلّيُّ نوعان (س406): جنسٌ ومشتقّ. -/
inductive Kulli | jins | mushtaq
  deriving DecidableEq, Repr

/-- الجزئيُّ نوعان (س407): علمٌ وضمير. -/
inductive Juzi | alam | damir
  deriving DecidableEq, Repr

/-- نوعُ المعنى: كلّيٌّ أو جزئيّ (س405، س410). -/
inductive Naw | kulli (k : Kulli) | juzi (j : Juzi)
  deriving DecidableEq, Repr

/-- اللفظُ المدلولُ عليه مستعملٌ (موضوع) أو مهمل (س409، س412، س414). -/
inductive Isti | mustamal | muhmal
  deriving DecidableEq, Repr

/-- **المدلولُ وحده** (س409): معنًى، أو لفظٌ مفرد، أو لفظٌ مركّبٌ من لفظين فأكثر؛ كلٌّ بشاهده. -/
inductive Madlul (L N W : Type)
  | maana (n : N) (k : Naw) (w : W)
  | mufrad (l : L) (i : Isti) (w : W)
  | murakkab (a b : L) (rest : List L) (i : Isti) (w : W)
  deriving DecidableEq, Repr

/-- الأقسامُ الخمسة بأسمائها (س409). -/
inductive Qism | maana | mufradMustamal | mufradMuhmal | murakkabMustamal | murakkabMuhmal
  deriving DecidableEq, Repr

def Qism.all : List Qism :=
  [.maana, .mufradMustamal, .mufradMuhmal, .murakkabMustamal, .murakkabMuhmal]

theorem qism_mem_all (q : Qism) : q ∈ Qism.all := by
  cases q <;> simp [Qism.all]

theorem all_nodup : Qism.all.Nodup := by decide

theorem all_length : Qism.all.length = 5 := rfl

variable {L N W : Type}

/-- قسمُ المدلول. -/
def qism : Madlul L N W → Qism
  | .maana .. => .maana
  | .mufrad _ .mustamal _ => .mufradMustamal
  | .mufrad _ .muhmal _ => .mufradMuhmal
  | .murakkab _ _ _ .mustamal _ => .murakkabMustamal
  | .murakkab _ _ _ .muhmal _ => .murakkabMuhmal

/-- المرجعُ الذي يدخل البوّابة: ألفاظٌ (أعدادُ شهاداتٍ من بوّابة الغانم) أو عقدةُ معنًى من مودَعٍ مختوم. -/
inductive Ref (L N : Type) | lafz (ls : List L) | node (n : N)
  deriving DecidableEq, Repr

/-- المودَع: لكلّ عقدةٍ نوعُها بشاهده، ولكلّ لفظٍ أو تركيبٍ استعمالُه أو إهمالُه بشاهده. -/
structure Mawda (L N W : Type) where
  naw : N → Option (Naw × W)
  isti : List L → Option (Isti × W)

/-- الرفضُ المسمّى. -/
inductive Rafd
  | emptyLafz      -- EMPTY_LAFZ_REF: مرجعٌ بلا لفظ
  | noNawWitness   -- MAANA_WITHOUT_WITNESS: عقدةٌ لا نوعَ لها في المودَع
  | noIstiWitness  -- ISTI_WITHOUT_WITNESS: لفظٌ لا شاهدَ لاستعماله ولا لإهماله — لا يُحكم بإهماله
  deriving DecidableEq, Repr

/-- **المدخل.** -/
def enter (d : Mawda L N W) : Ref L N → Except Rafd (Madlul L N W)
  | .node n => match d.naw n with
    | some (k, w) => .ok (.maana n k w)
    | none => .error .noNawWitness
  | .lafz [] => .error .emptyLafz
  | .lafz [l] => match d.isti [l] with
    | some (i, w) => .ok (.mufrad l i w)
    | none => .error .noIstiWitness
  | .lafz (a :: b :: r) => match d.isti (a :: b :: r) with
    | some (i, w) => .ok (.murakkab a b r i w)
    | none => .error .noIstiWitness

/-- **المخرج**: المرجعُ بعينه. -/
def exit : Madlul L N W → Ref L N
  | .maana n _ _ => .node n
  | .mufrad l _ _ => .lafz [l]
  | .murakkab a b r _ _ => .lafz (a :: b :: r)

/-- شاهدُ المدلول هو شاهدُ المودَع لمرجعه. -/
def Agrees (d : Mawda L N W) : Madlul L N W → Prop
  | .maana n k w => d.naw n = some (k, w)
  | .mufrad l i w => d.isti [l] = some (i, w)
  | .murakkab a b r i w => d.isti (a :: b :: r) = some (i, w)

/-- **الدخولُ ثمّ الخروج يعيد المرجع.** -/
theorem exit_enter (d : Mawda L N W) {r : Ref L N} {m : Madlul L N W}
    (h : enter d r = .ok m) : exit m = r := by
  cases r with
  | node n =>
    simp only [enter] at h
    split at h <;> simp_all [exit]
    cases h; rfl
  | lafz ls =>
    match ls, h with
    | [], h => simp [enter] at h
    | [l], h =>
      simp only [enter] at h
      split at h <;> simp_all
      cases h; rfl
    | a :: b :: r, h =>
      simp only [enter] at h
      split at h <;> simp_all
      cases h; rfl

/-- ما خرج من البوّابة يوافق المودَع. -/
theorem enter_agrees (d : Mawda L N W) {r : Ref L N} {m : Madlul L N W}
    (h : enter d r = .ok m) : Agrees d m := by
  cases r with
  | node n =>
    simp only [enter] at h
    split at h <;> simp_all
    cases h; simp_all [Agrees]
  | lafz ls =>
    match ls, h with
    | [], h => simp [enter] at h
    | [l], h =>
      simp only [enter] at h
      split at h <;> simp_all
      cases h; simp_all [Agrees]
    | a :: b :: r, h =>
      simp only [enter] at h
      split at h <;> simp_all
      cases h; simp_all [Agrees]

/-- **الخروجُ ثمّ الدخول يعيد المدلول** إذا وافق شاهدُه المودَع. -/
theorem enter_exit (d : Mawda L N W) (m : Madlul L N W) (h : Agrees d m) :
    enter d (exit m) = .ok m := by
  cases m <;> simp_all [Agrees, exit, enter]

/-- **لا مهملَ من الغياب**: لفظٌ أو تركيبٌ بلا شاهدٍ في المودَع يُرفض، ولا يُحكم بإهماله. -/
theorem absence_refused (d : Mawda L N W) {ls : List L} (hne : ls ≠ []) (h : d.isti ls = none) :
    enter d (.lafz ls) = .error .noIstiWitness := by
  match ls, hne with
  | [l], _ => simp [enter, h]
  | a :: b :: r, _ => simp [enter, h]

/-- كلُّ مهملٍ يخرج يحمل شاهدَ إهمالٍ من المودَع. -/
theorem muhmal_needs_witness (d : Mawda L N W) {r : Ref L N} {m : Madlul L N W}
    (h : enter d r = .ok m) (hq : qism m = .mufradMuhmal ∨ qism m = .murakkabMuhmal) :
    ∃ ls w, r = .lafz ls ∧ d.isti ls = some (.muhmal, w) := by
  have ha := enter_agrees d h
  have he := exit_enter d h
  cases m with
  | maana n k w => simp [qism] at hq
  | mufrad l i w =>
    cases i <;> simp [qism] at hq
    exact ⟨[l], w, he.symm, ha⟩
  | murakkab a b rest i w =>
    cases i <;> simp [qism] at hq
    exact ⟨a :: b :: rest, w, he.symm, ha⟩

/-- المفردُ ما مرجعُه لفظٌ واحد، والمركّبُ ما مرجعُه لفظان فأكثر. -/
theorem mufrad_iff_single (d : Mawda L N W) {ls : List L} {m : Madlul L N W}
    (h : enter d (.lafz ls) = .ok m) :
    (qism m = .mufradMustamal ∨ qism m = .mufradMuhmal) ↔ ls.length = 1 := by
  have he := exit_enter d h
  cases m with
  | maana n k w => simp [exit] at he
  | mufrad l i w =>
    simp [exit] at he; subst he
    cases i <;> simp [qism]
  | murakkab a b rest i w =>
    simp [exit] at he; subst he
    cases i <;> simp [qism]

/-- المعنى لا يدخل إلّا عقدةً، واللفظُ لا يدخل إلّا ألفاظًا: الدالُّ لا يُخلط بالمعنى. -/
theorem maana_iff_node (d : Mawda L N W) {r : Ref L N} {m : Madlul L N W}
    (h : enter d r = .ok m) : qism m = .maana ↔ ∃ n, r = .node n := by
  have he := exit_enter d h
  subst he
  cases m with
  | maana n k w => simp [qism, exit]
  | mufrad l i w => cases i <;> simp [qism, exit]
  | murakkab a b rest i w => cases i <;> simp [qism, exit]

/-! ## الشواهدُ من نصّ النبهانيّ (مولَّدةٌ في `Madlul.Shawahid`) -/

/-- مفتاحُ القسم في جدول الشواهد. -/
def qismKey : Qism → String
  | .maana => "maana"
  | .mufradMustamal => "mufradMustamal"
  | .mufradMuhmal => "mufradMuhmal"
  | .murakkabMustamal => "murakkabMustamal"
  | .murakkabMuhmal => "murakkabMuhmal"

/-- مفتاحُ نوع المعنى في جدول الشواهد. -/
def nawKey : Naw → String
  | .kulli .jins => "jins"
  | .kulli .mushtaq => "mushtaq"
  | .juzi .alam => "alam"
  | .juzi .damir => "damir"

open Shawahid in
/-- لكلّ قسمٍ من الخمسة شاهدٌ من نصّه بسطره. -/
theorem every_qism_witnessed :
    Qism.all.all (fun q => qismShawahid.any (·.1 == qismKey q)) = true := by
  decide

open Shawahid in
/-- ولكلّ نوعٍ من أنواع المعنى الأربعة شاهد. -/
theorem every_naw_witnessed :
    [Naw.kulli .jins, .kulli .mushtaq, .juzi .alam, .juzi .damir].all
      (fun k => nawShawahid.any (·.1 == nawKey k)) = true := by
  decide

end Madlul
