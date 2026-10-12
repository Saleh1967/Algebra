import Harf.Maqta

/-!
# الألفُ عنصرًا محايدًا: أين يصدق وأين لا يصدق

اعتقادُ المالك (2026-10-12): «الألفُ عنصرٌ محايد». يُبرهَن هنا على تعريفات Algebra وحدَها:

* **يصدق في الكلمة حرّةً**: محوُ الألف (`mahw`) تشاكلُ مونويدات يرسل كلَّ خانةِ ألفٍ إلى المحايد
  (`mahw_append`، `mahw_alif`)، وكلُّ تشاكلٍ يرسل خاناتِ الألف إلى المحايد يمرّ به
  (`factor_through_mahw` — القسمةُ الكلّيّة). وسلسلةُ الحركات القصيرة لا تتغيّر بزيادة ألفٍ ساكنة
  (`harakat_alif`).
* **ويصدق في الحركة**: الألفُ الساكنةُ بعد فتحٍ مدٌّ لها، وبعد غيره مُغلِق (`alif_baad_nawah`) — فهي
  لا تأتي بحركةٍ من عندها.
* **ولا يصدق في الترخيص**: «قَلْتُ» و«قَالْتُ» صورةٌ واحدةٌ بعد المحو، والأولى مرخَّصةٌ وصلًا والثانية لا
  (`alif_not_neutral_for_licence`)؛ فالترخيصُ لا يمرّ بالمحو (`licence_not_through_mahw`): الألفُ تزيد
  وزنَ المقطع (CVC ← CVVC) فتُدخل شرطَ المثل.
-/

set_option autoImplicit false

namespace Harf

/-- مونويدٌ بأقلّ ما يلزم هنا (لا Mathlib): ضربٌ ومحايدٌ يساريّ. -/
class Monoid' (M : Type) where
  mul : M → M → M
  one : M
  one_mul : ∀ a, mul one a = a

def isAlif (x : Khana) : Bool := x.hamil == alif

/-- محوُ الألف. -/
def mahw (w : List Khana) : List Khana := w.filter fun x => !isAlif x

theorem mahw_append (u v : List Khana) : mahw (u ++ v) = mahw u ++ mahw v := by
  simp [mahw, List.filter_append]

theorem mahw_alif (s : Haal) : mahw [⟨alif, s⟩] = [] := by
  simp [mahw, isAlif]

theorem mahw_nil : mahw [] = [] := rfl

/-- **القسمةُ الكلّيّة**: كلُّ تشاكلٍ من مونويد الكلمات يرسل خاناتِ الألف إلى المحايد يمرّ بالمحو. -/
theorem factor_through_mahw {M : Type} [Monoid' M] (f : List Khana → M)
    (happ : ∀ u v, f (u ++ v) = Monoid'.mul (f u) (f v))
    (halif : ∀ s : Haal, f [⟨alif, s⟩] = Monoid'.one) (w : List Khana) : f w = f (mahw w) := by
  induction w with
  | nil => rfl
  | cons x t ih =>
    have hx : f (x :: t) = Monoid'.mul (f [x]) (f t) := happ [x] t
    by_cases ha : isAlif x = true
    · have hxa : x = ⟨alif, x.haal⟩ := by
        rcases x with ⟨h, s⟩; simp [isAlif] at ha; subst ha; rfl
      have : mahw (x :: t) = mahw t := by simp [mahw, ha]
      rw [hx, this, ih, hxa, halif, Monoid'.one_mul]
    · have : mahw (x :: t) = x :: mahw t := by simp [mahw, ha]
      rw [hx, this, show x :: mahw t = [x] ++ mahw t from rfl, happ [x] (mahw t), ih]

/-- سلسلةُ الحركات القصيرة. -/
def harakat (w : List Khana) : List Haal := (w.filter fun x => x.haal != .sukun).map Khana.haal

theorem harakat_alif (u v : List Khana) :
    harakat (u ++ ⟨alif, .sukun⟩ :: v) = harakat (u ++ v) := by
  simp [harakat, List.filter_append]

/-- الألفُ الساكنةُ بعد نواةٍ: مدٌّ بعد الفتح، ومُغلِقٌ بعد غيره. -/
theorem alif_baad_nawah (q : Haal) (hq : q ≠ .sukun) :
    baadNawah q ⟨alif, .sukun⟩ = if q = .fath then .madd else .qasir := by
  cases q <;> simp_all [baadNawah, jins] <;> decide

theorem mahw_qaltu_qaaltu : mahw qaltu = mahw qaaltu := by decide

/-- **ولا يصدق في الترخيص**: صورةٌ واحدةٌ بعد المحو، وترخيصان مختلفان. -/
theorem alif_not_neutral_for_licence :
    mahw qaltu = mahw qaaltu ∧ waslB qaltu = true ∧ waslB qaaltu = false := by decide

theorem licence_not_through_mahw : ¬ ∃ g : List Khana → Bool, ∀ w, waslB w = g (mahw w) := by
  rintro ⟨g, hg⟩
  have h1 := hg qaltu
  have h2 := hg qaaltu
  rw [mahw_qaltu_qaaltu] at h1
  have := alif_not_neutral_for_licence
  rw [h1, h2] at this
  simp at this

end Harf
