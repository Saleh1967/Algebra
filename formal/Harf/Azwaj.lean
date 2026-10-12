import Harf.Satr

/-!
# السطرُ وأزواجُه، والكلمةُ الفارغة (ADR ٥)

**الأزواج.** `pairB ws`: كلُّ كلمتين متجاورتين مرخَّصتان معًا (`joinB`)، والكلمةُ الواحدة وحدَها (`waslB`).
**`line_eq_pairs`**: لكلّ سطرٍ كلماتُه غيرُ فارغة، **إن بدأت كلُّ كلمةٍ بعد الأولى بمتحرّك** فالسطرُ هو أزواجُه.
والسبب: بعد الحدّ وأوّلِ متحرّكٍ تنسى الآلةُ ما قبله (`after_hadd_vowel`: نواةٌ أو موت)، فلا يحمل السطرُ من
الكلمة السابقة إلّا ما يحمله زوجُها؛ وما يزيده الزوجُ حين تبتدئ كلمتُه السطرَ (مدُّ الفرق) لا يغيّر الحدَّ ما دامت
الكلمةُ حيّةً في السطر (`lock_ok`). والشرطُ لازم: `pairs_need_vowel_start` (الشاهدُ في الجسر).

**الكلمةُ الفارغة.** الحدُّ متساوي القوى (`hadd_idem`)، فالكلمةُ الفارغةُ في أوّل السطر أو وسطه لا تغيّر شيئًا
(`lineB_erase_empty`): هي محايدُ السطر.
-/

set_option autoImplicit false

namespace Harf

def startsV : List Khana → Bool
  | x :: _ => x.haal != .sukun
  | [] => false

/-- الحدُّ ثمّ أوّلُ الكلمة التالية لا يموت. -/
def ok (s : Hal) (x : Khana) : Bool := wasl (hadd s) x != .mayyit

/-- حالُ الكلمة إن ابتدأت بعد حدٍّ بنواتها. -/
def endE : List Khana → Hal
  | [] => .bad'
  | x :: t => run wasl (.nawah x.haal) t

def pairTail : List Khana → List (List Khana) → Bool
  | _, [] => true
  | v, u :: r => joinB v u && pairTail u r

def pairB : List (List Khana) → Bool
  | [] => true
  | [w] => waslB w
  | w :: v :: rest => joinB w v && pairTail v rest

/-! ## حقائقُ الآلة المنتهية -/

theorem after_hadd_vowel : ∀ s ∈ Hal.all, s ≠ .bad' → ∀ x ∈ Khana.all, x.haal ≠ .sukun →
    wasl (hadd s) x = .mayyit ∨ wasl (hadd s) x = .nawah x.haal := by decide +kernel

theorem ok_qabil : ∀ s ∈ Hal.all, ∀ x ∈ Khana.all, ok s x = true → qabilWasl s = true := by
  decide +kernel

theorem wasl_ne_bad' : ∀ a ∈ Hal.all, ∀ x ∈ Khana.all, wasl a x ≠ .bad' := by decide +kernel

theorem hadd_idem : ∀ a ∈ Hal.all, hadd (hadd a) = hadd a := by decide

/-- السيرُ متقارنًا: من أوّل الكلمة (`bad'`) ومن نواتها — الحالان واحدٌ، أو الثاني ميّت، أو فرقُ مدّ الفرق. -/
def lock (a b : Hal) : Bool :=
  a == b || b == .mayyit || (a == .hamzaAwwal && b == .nawah .fath) || (a == .farq && b == .madd) ||
    (a == .tawilFarq && b == .tawil lam)

theorem lock_start : ∀ x ∈ Khana.all, x.haal ≠ .sukun → lock (wasl .bad' x) (.nawah x.haal) = true := by
  decide +kernel

theorem lock_step : ∀ a ∈ Hal.all, ∀ b ∈ Hal.all, lock a b = true → ∀ y ∈ Khana.all,
    lock (wasl a y) (wasl b y) = true := by decide +kernel

theorem lock_ok : ∀ a ∈ Hal.all, ∀ b ∈ Hal.all, lock a b = true → b ≠ .mayyit → ∀ x ∈ Khana.all,
    ok a x = ok b x := by decide +kernel

theorem lock_run : ∀ (a b : Hal) (t : List Khana), lock a b = true → lock (run wasl a t) (run wasl b t) = true
  | _, _, [], h => h
  | a, b, y :: t, h => lock_run _ _ t (lock_step a (Hal.mem_all a) b (Hal.mem_all b) h y (Khana.mem_all y))

/-! ## السطرُ هو أزواجُه -/

theorem run_ne_bad'' : ∀ (a : Hal) (w : List Khana), w ≠ [] → run wasl a w ≠ .bad'
  | _, [], h => absurd rfl h
  | a, [x], _ => by simpa [run] using wasl_ne_bad' a (Hal.mem_all a) x (Khana.mem_all x)
  | a, x :: y :: t, _ => by simp only [run]; exact run_ne_bad'' _ (y :: t) (by simp)

theorem endE_ne_bad' (v : List Khana) (h : v ≠ []) : endE v ≠ .bad' := by
  match v with
  | [] => exact absurd rfl h
  | [x] => simp [endE, run]
  | x :: y :: t => simp only [endE]; exact run_ne_bad'' _ (y :: t) (by simp)

/-- بعد الحدّ: الكلمةُ التي تبتدئ بمتحرّكٍ إمّا تموت عند أوّلها وإمّا تسير سيرَها من نواتها. -/
theorem run_after_hadd (s : Hal) (hs : s ≠ .bad') (v : List Khana) (hv : startsV v = true) :
    run wasl (hadd s) v = if ok s (v.headD ⟨0, .sukun⟩) then endE v else .mayyit := by
  match v with
  | [] => simp [startsV] at hv
  | x :: t =>
    have hx : x.haal ≠ .sukun := by simpa [startsV] using hv
    simp only [run, endE, ok, List.headD]
    rcases after_hadd_vowel s (Hal.mem_all s) hs x (Khana.mem_all x) hx with h | h
    · simp [h, run_mayyit]
    · simp [h]

theorem runLine_mayyit : ∀ ws : List (List Khana), runLine wasl .mayyit ws = .mayyit
  | [] => rfl
  | [w] => run_mayyit w
  | w :: v :: rest => by
    simp only [runLine, run_mayyit]; exact runLine_mayyit (v :: rest)

theorem hadd_mayyit : hadd .mayyit = .mayyit := rfl

/-- الزوجُ بعد كلمةٍ حيّة. -/
theorem joinB_eq (v u : List Khana) (hv : v ≠ []) (hu : startsV u = true) :
    joinB v u = (ok (run wasl .bad' v) (u.headD ⟨0, .sukun⟩) && qabilWasl (endE u)) := by
  simp only [joinB, lineB, runLine]
  rw [run_after_hadd _ (run_ne_bad'' _ v hv) u hu]
  cases ok (run wasl .bad' v) (u.headD ⟨0, .sukun⟩) <;> simp [qabilWasl]

/-- ما يحمله الزوجُ من كلمته اليسرى يحمله السطر: الحدُّ بعدها واحدٌ إن كانت حيّة. -/
theorem ok_bad'_endE (v : List Khana) (hv : startsV v = true) (x : Khana)
    (hq : qabilWasl (endE v) = true) : ok (run wasl .bad' v) x = ok (endE v) x := by
  match v with
  | [] => simp [startsV] at hv
  | y :: t =>
    have hy : y.haal ≠ .sukun := by simpa [startsV] using hv
    have hl := lock_run (wasl .bad' y) (.nawah y.haal) t (lock_start y (Khana.mem_all y) hy)
    simp only [endE] at hq ⊢
    simp only [run]
    have hne : run wasl (.nawah y.haal) t ≠ .mayyit := by
      intro h; rw [h] at hq; simp [qabilWasl] at hq
    exact lock_ok _ (Hal.mem_all _) _ (Hal.mem_all _) hl hne x (Khana.mem_all x)

theorem line_from (s : Hal) (hs : s ≠ .bad') : ∀ (v : List Khana) (rest : List (List Khana)),
    (∀ u ∈ v :: rest, startsV u = true) →
    qabilWasl (runLine wasl (hadd s) (v :: rest)) =
      (ok s (v.headD ⟨0, .sukun⟩) && qabilWasl (endE v) && pairTail v rest)
  | v, [], hv => by
    simp only [runLine, pairTail, Bool.and_true]
    rw [run_after_hadd s hs v (hv v (by simp))]
    cases ok s (v.headD ⟨0, .sukun⟩) <;> simp [qabilWasl]
  | v, u :: r, hv => by
    have hvv : startsV v = true := hv v (by simp)
    have hvn : v ≠ [] := by intro h; subst h; simp [startsV] at hvv
    have huu : startsV u = true := hv u (by simp)
    simp only [runLine]
    rw [run_after_hadd s hs v hvv]
    cases hok : ok s (v.headD ⟨0, .sukun⟩)
    · simp [hadd_mayyit, runLine_mayyit, qabilWasl]
    · simp only [ite_true, Bool.true_and]
      have ih := line_from (endE v) (endE_ne_bad' v hvn) u r (fun w hw => hv w (by simp_all))
      rw [ih, pairTail, joinB_eq v u hvn huu]
      cases hq : qabilWasl (endE v)
      · -- السطرُ ميّتٌ عند v: الحدُّ بعده لا يمرّ
        have : ok (endE v) (u.headD ⟨0, .sukun⟩) = false := by
          cases h : ok (endE v) (u.headD ⟨0, .sukun⟩)
          · rfl
          · have := ok_qabil _ (Hal.mem_all _) _ (Khana.mem_all _) h; rw [hq] at this; cases this
        rw [this]; simp
      · rw [ok_bad'_endE v hvv _ hq]
        simp [Bool.and_assoc]

/-- **السطرُ هو أزواجُه** إن بدأت كلُّ كلمةٍ بعد الأولى بمتحرّك. -/
theorem line_eq_pairs (ws : List (List Khana)) (hne : ∀ w ∈ ws, w ≠ [])
    (hv : ∀ w ∈ ws.tail, startsV w = true) : lineB ws = pairB ws := by
  match ws with
  | [] => rfl
  | [w] => rfl
  | w :: v :: rest =>
    have hw : w ≠ [] := hne w (by simp)
    have hvv : startsV v = true := hv v (by simp)
    have hvn : v ≠ [] := hne v (by simp)
    simp only [lineB, runLine, pairB]
    rw [line_from _ (run_ne_bad'' _ w hw) v rest (by simpa using hv), joinB_eq w v hw hvv]

/-! ## الكلمةُ الفارغة محايدُ السطر -/

theorem runLine_empty_inner (f : Hal → Khana → Hal) (a : Hal) (w : List Khana) (v : List Khana)
    (rest : List (List Khana)) :
    runLine f a (w :: [] :: v :: rest) = runLine f a (w :: v :: rest) := by
  simp only [runLine, run, hadd_idem _ (Hal.mem_all _)]

theorem runLine_empty_lead (f : Hal → Khana → Hal) (v : List Khana) (rest : List (List Khana)) :
    runLine f .bad' ([] :: v :: rest) = runLine f .bad' (v :: rest) := by
  simp only [runLine, run]; rfl

theorem runLine_erase_empty (f : Hal → Khana → Hal) : ∀ (u : List (List Khana)) (a : Hal)
    (v : List Khana) (rest : List (List Khana)), u ≠ [] →
    runLine f a (u ++ [] :: v :: rest) = runLine f a (u ++ v :: rest)
  | [], _, _, _, h => absurd rfl h
  | [w], a, v, rest, _ => runLine_empty_inner f a w v rest
  | w :: w2 :: u, a, v, rest, _ => by
    simp only [List.cons_append, runLine]
    exact runLine_erase_empty f (w2 :: u) _ v rest (by simp)

/-- **الكلمةُ الفارغةُ في أوّل السطر أو وسطه لا تغيّر ترخيصَه.** -/
theorem lineB_erase_empty (u : List (List Khana)) (v : List Khana) (rest : List (List Khana)) :
    lineB (u ++ [] :: v :: rest) = lineB (u ++ v :: rest) := by
  unfold lineB
  cases u with
  | nil => simp only [List.nil_append]; rw [runLine_empty_lead]
  | cons w u => rw [runLine_erase_empty wasl (w :: u) .bad' v rest (by simp)]

end Harf
