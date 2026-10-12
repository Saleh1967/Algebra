import HarfBridge.Satr
import Harf.Azwaj

/-!
# سدُّ `LINE_VS_PAIRWISE_JOIN_UNPROVEN`، والكلمةُ الفارغة في سطر الغانم (ADR ٥)

* **`line_eq_pairwise`**: لكلّ سطرٍ من خانات الغانم كلماتُه غيرُ فارغة، **إن بدأت كلُّ كلمةٍ بعد الأولى بمتحرّك**
  فـ`strictLineB` هو قرانُ أزواجه (`strictJoinB` لكلّ كلمتين متجاورتين؛ و`strictB` للكلمة الواحدة).
* **`pairwise_needs_vowel_start`**: والشرطُ لازم — «قُلِ لْحَمْدُ لِلَّهِ»: السطرُ مرخَّص، وزوجُ «لْحَمْدُ لِلَّهِ»
  مرفوضٌ لأنّ الزوجَ يبتدئ بساكن؛ فالأزواجُ تفترق عن السطر حين تبتدئ كلمةٌ داخليّةٌ بساكن، وهذا هو الافتراقُ
  المسمّى في ADR ٢٧ بعينه.
* **`empty_word_smuggles_straddle`**: في الغانم، كلمةٌ فارغةٌ بين «يَا» و«الشَّافِعِينَ» تُسقط فحصَ الحدّ:
  `strictLineB [يَا، []، شْشَافِعِينَ] = true` و`strictLineB [يَا، شْشَافِعِينَ] = false` — والآلةُ في Algebra لا
  تنخدع (`harf_not_smuggled`).
* **`lineN_eq_strictLineN`**: الحلّ — الكلمةُ الفارغةُ محايدُ السطر فتُحذف قبل الحكم (`lineN`، `strictLineN`)؛
  والتكافؤُ حينئذٍ **لكلّ سطرٍ بلا شرط**.
-/

set_option autoImplicit false

namespace HarfBridge

open A116 A116.Stages A116.Ternary A116.Hadd A116.NizamLine

/-! ## ١. الأزواجُ في الغانم -/

def pairTailA : List Cell → List (List Cell) → Bool
  | _, [] => true
  | v, u :: r => strictJoinB v u && pairTailA u r

def pairA : List (List Cell) → Bool
  | [] => true
  | [w] => strictB w
  | w :: v :: rest => strictJoinB w v && pairTailA v rest

def startsVA : List Cell → Bool
  | x :: _ => x.haraka != .sukun
  | [] => false

/-! ## ٢. النقلُ بين الترتيبين -/

def unprojW (w : List Cell) : List Harf.Khana := w.map unproj

theorem projW_unprojW (w : List Cell) : projW (unprojW w) = w := by
  induction w with
  | nil => rfl
  | cons c t ih =>
    simp only [unprojW, projW, List.map_cons] at ih ⊢
    rw [ih, proj_bijective.2 c (mem_cells c)]

theorem unprojW_ne {w : List Cell} (h : w ≠ []) : unprojW w ≠ [] := by
  cases w <;> simp_all [unprojW]

theorem startsV_unproj_cells : ∀ c ∈ A116.cells, ((unproj c).haal != .sukun) = (c.haraka != .sukun) := by
  decide +kernel

theorem startsV_unprojW (w : List Cell) : Harf.startsV (unprojW w) = startsVA w := by
  cases w with
  | nil => rfl
  | cons c t => simp only [unprojW, List.map_cons, Harf.startsV, startsVA]; exact startsV_unproj_cells c (mem_cells c)

theorem pairTail_eq : ∀ (v : List Harf.Khana) (rest : List (List Harf.Khana)), v ≠ [] →
    (∀ w ∈ rest, w ≠ []) → Harf.pairTail v rest = pairTailA (projW v) (projL rest)
  | _, [], _, _ => rfl
  | v, u :: r, hv, hr => by
    have hu : u ≠ [] := hr u (by simp)
    simp only [Harf.pairTail, pairTailA, projL, List.map_cons]
    rw [join_eq_strictJoinB v u hv hu, pairTail_eq u r hu (fun w hw => hr w (by simp [hw]))]
    rfl

theorem pairB_eq (ws : List (List Harf.Khana)) (hne : ∀ w ∈ ws, w ≠ []) :
    Harf.pairB ws = pairA (projL ws) := by
  match ws with
  | [] => rfl
  | [w] => simp only [Harf.pairB, pairA, projL, List.map_cons, List.map_nil]; exact wasl_eq_strictB w
  | w :: v :: rest =>
    have hw : w ≠ [] := hne w (by simp)
    have hv : v ≠ [] := hne v (by simp)
    simp only [Harf.pairB, pairA, projL, List.map_cons]
    rw [join_eq_strictJoinB w v hw hv, pairTail_eq v rest hv (fun u hu => hne u (by simp [hu]))]
    rfl

/-! ## ٣. السطرُ هو أزواجُه -/

/-- **سدُّ `LINE_VS_PAIRWISE_JOIN_UNPROVEN`**: إن بدأت كلُّ كلمةٍ بعد الأولى بمتحرّك فالسطرُ قرانُ أزواجه. -/
theorem line_eq_pairwise (ws : List (List Cell)) (hne : ∀ w ∈ ws, w ≠ [])
    (hv : ∀ w ∈ ws.tail, startsVA w = true) : strictLineB ws = pairA ws := by
  have hws : projL (ws.map unprojW) = ws := by
    simp only [projL, List.map_map]
    conv => rhs; rw [← List.map_id ws]
    exact List.map_congr_left (fun w _ => projW_unprojW w)
  have hne' : ∀ w ∈ ws.map unprojW, w ≠ [] := by
    intro w hw; simp only [List.mem_map] at hw; obtain ⟨u, hu, rfl⟩ := hw; exact unprojW_ne (hne u hu)
  have hv' : ∀ w ∈ (ws.map unprojW).tail, Harf.startsV w = true := by
    intro w hw
    rw [← List.map_tail] at hw
    simp only [List.mem_map] at hw
    obtain ⟨u, hu, rfl⟩ := hw
    rw [startsV_unprojW]; exact hv u hu
  rw [← hws, ← line_eq_strictLineB _ hne', Harf.line_eq_pairs _ hne' hv', pairB_eq _ hne']

def lillahi : List Harf.Khana :=
  [Harf.k 'ل' .kasr, Harf.k 'ل' .sukun, Harf.k 'ل' .fath, Harf.k 'ه' .kasr]

/-- **والشرطُ لازم**: كلمةٌ داخليّةٌ تبتدئ بساكن تفرّق السطرَ عن أزواجه. -/
theorem pairwise_needs_vowel_start :
    strictLineB (projL [Harf.quli, Harf.lhamdu, lillahi]) = true ∧
    pairA (projL [Harf.quli, Harf.lhamdu, lillahi]) = false ∧
    startsVA (projW Harf.lhamdu) = false := by
  decide +kernel

/-! ## ٤. الكلمةُ الفارغة -/

/-- **في الغانم**: كلمةٌ فارغةٌ تُسقط فحصَ الحدّ بين جارتيها. -/
theorem empty_word_smuggles_straddle :
    strictLineB (projL [Harf.yaa, [], Harf.shshafiina]) = true ∧
    strictLineB (projL [Harf.yaa, Harf.shshafiina]) = false := by
  decide +kernel

/-- **وفي Algebra لا**: الحدُّ متساوي القوى، فالكلمةُ الفارغةُ لا تُسقط شيئًا. -/
theorem harf_not_smuggled : Harf.lineB [Harf.yaa, [], Harf.shshafiina] = false := by decide

def nonEmpty {β : Type} (ws : List (List β)) : List (List β) := ws.filter fun w => !w.isEmpty

/-- السطرُ بعد حذف الكلمات الفارغة (محايدِ السطر). -/
def lineN (ws : List (List Harf.Khana)) : Bool := Harf.lineB (nonEmpty ws)

def strictLineN (ws : List (List Cell)) : Bool := strictLineB (nonEmpty ws)

theorem nonEmpty_ne {β : Type} (ws : List (List β)) : ∀ w ∈ nonEmpty ws, w ≠ [] := by
  intro w hw
  simp only [nonEmpty, List.mem_filter, Bool.not_eq_true', List.isEmpty_eq_false_iff] at hw
  exact hw.2

theorem projL_nonEmpty (ws : List (List Harf.Khana)) : projL (nonEmpty ws) = nonEmpty (projL ws) := by
  induction ws with
  | nil => rfl
  | cons w ws ih =>
    simp only [projL, nonEmpty, List.map_cons, List.filter_cons] at ih ⊢
    cases w with
    | nil => simpa [projW] using ih
    | cons x t => simp [projW, ih]

/-- **الحلّ**: الكلمةُ الفارغةُ محايدٌ يُحذف، فالتكافؤُ لكلّ سطرٍ بلا شرط. -/
theorem lineN_eq_strictLineN (ws : List (List Harf.Khana)) : lineN ws = strictLineN (projL ws) := by
  unfold lineN strictLineN
  rw [← projL_nonEmpty]
  exact line_eq_strictLineB _ (nonEmpty_ne ws)

theorem strictLineN_nonempty (ws : List (List Cell)) (hne : ∀ w ∈ ws, w ≠ []) :
    strictLineN ws = strictLineB ws := by
  unfold strictLineN nonEmpty
  rw [List.filter_eq_self.mpr]
  intro w hw; cases w with
  | nil => exact absurd rfl (hne [] hw)
  | cons _ _ => rfl

end HarfBridge
