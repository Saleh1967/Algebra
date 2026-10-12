import HarfBridge.Azwaj
import Harf.Mawda
import A116.Iltiqa

/-!
# سدُّ `CONTEXT_DEPOSIT_VS_PAIRS_UNPROVEN` في خانات الغانم (ADR ٦)

مودَعُ السياق (`gate/api.py`، `tools/gen_context_certificates.py`): الكلمةُ الأولى في صورة ابتدائها `S₁`
(`strictB`)، وكلُّ كلمةٍ بعدها **خامًا** `Wᵢ` مع صورة ابتداء ما قبلها `Sᵢ₋₁` **مصلَحةً عليها**
(`Iltiqa.strictJoinRepairedB`). هذا `depA`. والسطرُ: الكلماتُ مصلَحةً كلٌّ على تاليتها (`repairsL`)، أوّلُها صورةُ
الابتداء.

**`deposit_eq_line`**: لكلّ سطرٍ كلُّ كلمةٍ بعد الأولى فيه
* غيرُ فارغة، وإن ختمها ساكنٌ فطولُها اثنتان فأكثر (`okLen`)،
* أوّلُها حرٌّ: متحرّكٌ أو ساكنٌ ليس حرفَ مدّ (`freeA`)،
* وصورةُ ابتدائها هي أو متحرّكٌ قبلها (`StartFormA`)،

`depA = strictLineB (repairsL …) && strictB S₁ && كلُّ كلمةٍ خامٍ بعد الأولى مرخَّصةٌ بعد «بَ»`.

فالمودَعُ **هو السطرُ** مع شرطين لا يراهما السطر: صورةُ ابتداء الأولى خامًا، وكلُّ كلمةٍ قبل إصلاح آخرها
(`deposit_needs_raw`: «بِ قَالْ الْحَمْدُ» السطرُ مرخَّصٌ والمودَعُ يرفض).
-/

set_option autoImplicit false

namespace HarfBridge

open A116 A116.Stages A116.Ternary A116.Hadd A116.NizamLine A116.Iltiqa A116.Ladder

/-! ## ١. المودَعُ والسطرُ في الغانم -/

def depTailA : List Cell → List (List Cell × List Cell) → Bool
  | _, [] => true
  | Sp, (W, S) :: rest => strictJoinRepairedB Sp W && depTailA S rest

/-- المودَع: أزواجُ (الكلمةُ خامًا، صورةُ ابتدائها). -/
def depA : List (List Cell × List Cell) → Bool
  | [] => true
  | (_, S) :: rest => strictB S && depTailA S rest

/-- كلُّ كلمةٍ مصلَحةٌ على تاليتها، والأخيرةُ كما هي. -/
def repairsL : List (List Cell) → List (List Cell)
  | [] => []
  | [w] => [w]
  | w :: v :: rest => (repair w v).1 :: repairsL (v :: rest)

def StartFormA (S W : List Cell) : Prop :=
  (startsVA W = true → S = W) ∧ (startsVA W = false → ∃ y : Cell, y.haraka ≠ .sukun ∧ S = y :: W)

def freeA : List Cell → Bool
  | x :: _ => x.haraka != .sukun || maddVowel x.carrier == none
  | [] => false

def okLen (W : List Cell) : Prop := W ≠ [] ∧ (endsSukun W = true → 2 ≤ W.length)

def baA : List Cell := [atom 'ب' .fatha]

/-! ## ٢. النقلُ خانةً خانة -/

theorem unproj_sukun : ∀ c ∈ A116.cells, ((unproj c).haal == .sukun) = (c.haraka == .sukun) := by
  decide +kernel

theorem unproj_kasra : ∀ c ∈ A116.cells,
    unproj ⟨c.carrier, .kasra⟩ = ⟨(unproj c).hamil, .kasr⟩ := by decide +kernel

theorem unproj_free : ∀ c ∈ A116.cells,
    ((unproj c).haal != .sukun || Harf.jins (unproj c).hamil == none) =
      (c.haraka != .sukun || maddVowel c.carrier == none) := by decide +kernel

theorem unproj_ba : unprojW baA = [Harf.k 'ب' .fath] := by decide +kernel

theorem freeFirst_unprojW (W : List Cell) : Harf.freeFirst (unprojW W) = freeA W := by
  cases W with
  | nil => rfl
  | cons c t => simp only [unprojW, List.map_cons, Harf.freeFirst, freeA]; exact unproj_free c (mem_cells c)

theorem unproj_sukun' (c : Cell) (h : c.haraka = .sukun) : (unproj c).haal = .sukun := by
  have := unproj_sukun c (mem_cells c); simp [h] at this; exact this

/-! ## ٣. الإصلاحُ: يمسّ الآخرَ وحدَه، ويُبقي الأوّل، ويَسبق صورةَ الابتداء -/

theorem getLast?_cons_ne (y : Cell) (l : List Cell) (h : l ≠ []) : (y :: l).getLast? = l.getLast? := by
  cases l with
  | nil => exact absurd rfl h
  | cons a t => simp

theorem endsSukun_cons (y : Cell) (l : List Cell) (h : l ≠ []) : endsSukun (y :: l) = endsSukun l := by
  simp only [endsSukun, getLast?_cons_ne y l h]

theorem endsSukun_some {l : List Cell} (h : endsSukun l = true) :
    ∃ a, l.getLast? = some a ∧ a.haraka = .sukun := by
  unfold endsSukun at h
  split at h
  · rename_i a ha; exact ⟨a, ha, by simpa using h⟩
  · simp at h

/-- الإصلاحُ لا شيءَ، أو حذفُ ساكنٍ آخِر، أو كسرُه. -/
theorem repair_shape (l r : List Cell) :
    (repair l r).1 = l ∨ ∃ a, l.getLast? = some a ∧ a.haraka = .sukun ∧
      ((repair l r).1 = l.dropLast ∨ (repair l r).1 = l.dropLast ++ [⟨a.carrier, .kasra⟩]) := by
  cases he : endsSukun l
  · left; rw [repair_noop_of_left_vowel l r he]
  · obtain ⟨a, ha, hs⟩ := endsSukun_some he
    rcases repair_eq l r with h0 | ⟨_, h1⟩ | ⟨_, h2⟩ | ⟨b, hb, h3⟩
    · left; rw [h0]
    · right; exact ⟨a, ha, hs, Or.inl (by rw [h1])⟩
    · right; exact ⟨a, ha, hs, Or.inl (by rw [h2])⟩
    · rw [ha] at hb; cases hb
      right; exact ⟨a, ha, hs, Or.inr (by rw [h3])⟩

theorem length_two_of {l : List Cell} (hl : okLen l) (a : Cell) (ha : l.getLast? = some a)
    (hs : a.haraka = .sukun) : 2 ≤ l.length :=
  hl.2 (by simp [endsSukun, ha, hs])

theorem head?_dropLast (l : List Cell) (h : 2 ≤ l.length) : l.dropLast.head? = l.head? := by
  match l, h with
  | a :: b :: t, _ => simp

theorem dropLast_ne (l : List Cell) (h : 2 ≤ l.length) : l.dropLast ≠ [] := by
  match l, h with
  | a :: b :: t, _ => simp

theorem repair_head (l r : List Cell) (hl : okLen l) : (repair l r).1.head? = l.head? := by
  rcases repair_shape l r with h | ⟨a, ha, hs, h | h⟩
  · rw [h]
  · rw [h, head?_dropLast l (length_two_of hl a ha hs)]
  · rw [h, ← head?_dropLast l (length_two_of hl a ha hs)]
    obtain ⟨z, zs, hz⟩ : ∃ z zs, l.dropLast = z :: zs := by
      cases hd : l.dropLast with
      | nil => exact absurd hd (dropLast_ne l (length_two_of hl a ha hs))
      | cons z zs => exact ⟨z, zs, rfl⟩
    rw [hz]; rfl

theorem repair_ne (l r : List Cell) (hl : okLen l) : (repair l r).1 ≠ [] := by
  intro h
  have := repair_head l r hl
  rw [h] at this
  cases l with
  | nil => exact hl.1 rfl
  | cons _ _ => simp at this

theorem lastKind_cons (y a b : Cell) (t : List Cell) :
    lastKind (y :: a :: b :: t) = lastKind (a :: b :: t) := by
  simp [lastKind, kindOf, kindGo]

theorem endsFarqAlif_cons (y a b : Cell) (t : List Cell) :
    endsFarqAlif (y :: a :: b :: t) = endsFarqAlif (a :: b :: t) := by
  simp [endsFarqAlif]

/-- **الإصلاحُ يَسبق صورةَ الابتداء**: إصلاحُ `y :: l` هو `y ::` إصلاحِ `l`. -/
theorem repair_cons (y : Cell) (l r : List Cell) (hl : okLen l) :
    (repair (y :: l) r).1 = y :: (repair l r).1 := by
  cases he : endsSukun l
  · have he' : endsSukun (y :: l) = false := by rw [endsSukun_cons y l hl.1, he]
    rw [repair_noop_of_left_vowel _ _ he', repair_noop_of_left_vowel _ _ he]
  · obtain ⟨a, ha, hs⟩ := endsSukun_some he
    have h2 := length_two_of hl a ha hs
    match l, h2 with
    | a0 :: b0 :: t, _ =>
      unfold repair
      rw [endsSukun_cons y _ (by simp), endsFarqAlif_cons, lastKind_cons, getLast?_cons_ne y _ (by simp)]
      split
      · rfl
      · split
        · simp
        · split
          · simp
          · split <;> simp

/-! ## ٤. الحياة: إصلاحُ الآخر لا يُميت كلمةً حيّة -/

theorem unprojW_dropLast (l : List Cell) : unprojW l.dropLast = (unprojW l).dropLast := by
  simp [unprojW, List.map_dropLast]

theorem alive_repair (l r : List Cell) (hl : okLen l)
    (h : Harf.qabilWasl (Harf.endC (unprojW l)) = true) :
    Harf.qabilWasl (Harf.endC (unprojW (repair l r).1)) = true := by
  rcases repair_shape l r with he | ⟨a, ha, hs, he | he⟩
  · rw [he]; exact h
  · have h2 := length_two_of hl a ha hs
    have hsplit : unprojW l = unprojW l.dropLast ++ [unproj a] := by
      conv => lhs; rw [← dropLast_append_of_getLast? ha]
      simp [unprojW]
    rw [he]; rw [hsplit] at h
    exact Harf.alive_drop _ (unprojW_ne (dropLast_ne l h2)) _ (unproj_sukun' a hs) h
  · have h2 := length_two_of hl a ha hs
    have hsplit : unprojW l = unprojW l.dropLast ++ [unproj a] := by
      conv => lhs; rw [← dropLast_append_of_getLast? ha]
      simp [unprojW]
    have hk : unprojW (l.dropLast ++ [⟨a.carrier, .kasra⟩]) =
        unprojW l.dropLast ++ [⟨(unproj a).hamil, .kasr⟩] := by
      simp [unprojW, unproj_kasra a (mem_cells a)]
    rw [he, hk]; rw [hsplit] at h
    exact Harf.alive_kasr _ (unprojW_ne (dropLast_ne l h2)) _ (unproj_sukun' a hs) h

/-! ## ٥. المواضع -/

def posOf (W S : List Cell) : Option (List Cell) → Harf.Pos
  | none => ⟨unprojW W, unprojW W, unprojW S⟩
  | some n => ⟨unprojW (repair W n).1, unprojW W, unprojW (repair S n).1⟩

def build : List (List Cell × List Cell) → List Harf.Pos
  | [] => []
  | [(W, S)] => [posOf W S none]
  | (W, S) :: (W', S') :: rest => posOf W S (some W') :: build ((W', S') :: rest)

/-- شروطُ الكلمة بعد الأولى. -/
def CondA (p : List Cell × List Cell) : Prop := okLen p.1 ∧ freeA p.1 = true ∧ StartFormA p.2 p.1

theorem startsVA_repair (l r : List Cell) (hl : okLen l) : startsVA (repair l r).1 = startsVA l := by
  have h := repair_head l r hl
  cases hr : (repair l r).1 with
  | nil => exact absurd hr (repair_ne l r hl)
  | cons x t =>
    rw [hr] at h
    cases l with
    | nil => simp at h
    | cons y u => simp at h; rw [h.symm]; rfl

theorem freeA_repair (l r : List Cell) (hl : okLen l) : freeA (repair l r).1 = freeA l := by
  have h := repair_head l r hl
  cases hr : (repair l r).1 with
  | nil => exact absurd hr (repair_ne l r hl)
  | cons x t =>
    rw [hr] at h
    cases l with
    | nil => simp at h
    | cons y u => simp at h; rw [h.symm]; rfl

theorem startsV_unprojW' (w : List Cell) : Harf.startsV (unprojW w) = startsVA w := startsV_unprojW w

theorem startForm_repair (S W r : List Cell) (hW : okLen W) (hS : StartFormA S W) :
    Harf.StartForm (unprojW (repair S r).1) (unprojW (repair W r).1) := by
  constructor
  · intro hv
    rw [startsV_unprojW', startsVA_repair W r hW] at hv
    rw [hS.1 hv]
  · intro hv
    rw [startsV_unprojW', startsVA_repair W r hW] at hv
    obtain ⟨y, hy, rfl⟩ := hS.2 hv
    refine ⟨unproj y, ?_, ?_⟩
    · intro h0
      have := unproj_sukun y (mem_cells y)
      rw [h0] at this; simp at this; exact hy this
    · rw [repair_cons y W r hW]; simp [unprojW]

theorem startForm_unproj (S W : List Cell) (hS : StartFormA S W) :
    Harf.StartForm (unprojW S) (unprojW W) := by
  constructor
  · intro hv; rw [startsV_unprojW'] at hv; rw [hS.1 hv]
  · intro hv
    rw [startsV_unprojW'] at hv
    obtain ⟨y, hy, rfl⟩ := hS.2 hv
    refine ⟨unproj y, ?_, by simp [unprojW]⟩
    intro h0
    have := unproj_sukun y (mem_cells y)
    rw [h0] at this; simp at this; exact hy this

theorem head_unprojW (l : List Cell) : (unprojW l).headD ⟨0, .sukun⟩ =
    match l.head? with | some c => unproj c | none => ⟨0, .sukun⟩ := by
  cases l <;> rfl

theorem posOK_of (W S : List Cell) (n : Option (List Cell)) (h : CondA (W, S)) :
    Harf.PosOK (posOf W S n) := by
  obtain ⟨hl, hf, hS⟩ := h
  have hW : unprojW W ≠ [] := unprojW_ne hl.1
  have hfW : Harf.freeFirst (unprojW W) = true := by rw [freeFirst_unprojW]; exact hf
  cases n with
  | none =>
    exact ⟨hW, hW, hfW, hfW, rfl, startForm_unproj S W hS, id⟩
  | some r =>
    refine ⟨unprojW_ne (repair_ne W r hl), hW, ?_, hfW, ?_, startForm_repair S W r hl hS,
      alive_repair W r hl⟩
    · show Harf.freeFirst (unprojW (repair W r).1) = true
      rw [freeFirst_unprojW, freeA_repair W r hl]; exact hf
    · simp only [posOf]; rw [head_unprojW, head_unprojW, repair_head W r hl]

theorem build_posOK : ∀ (ps : List (List Cell × List Cell)), (∀ p ∈ ps, CondA p) →
    ∀ q ∈ build ps, Harf.PosOK q
  | [], _ => by simp [build]
  | [(W, S)], h => by
    intro q hq; simp only [build, List.mem_singleton] at hq; subst hq
    exact posOK_of W S none (h _ (by simp))
  | (W, S) :: (W', S') :: rest, h => by
    intro q hq
    simp only [build, List.mem_cons] at hq
    rcases hq with rfl | hq
    · exact posOK_of W S _ (h _ (by simp))
    · exact build_posOK ((W', S') :: rest) (fun p hp => h p (by simp_all)) q (by simpa using hq)

theorem build_R : ∀ (ps : List (List Cell × List Cell)),
    (build ps).map Harf.Pos.R = (repairsL (ps.map Prod.fst)).map unprojW
  | [] => rfl
  | [(W, S)] => rfl
  | (W, S) :: (W', S') :: rest => by
    simp only [build, List.map_cons, repairsL, posOf]
    congr 1
    simpa using build_R ((W', S') :: rest)

theorem build_last' : ∀ (ps : List (List Cell × List Cell)), ps ≠ [] →
    ∃ W S, (build ps).getLast? = some (posOf W S none)
  | [], h => absurd rfl h
  | [(W, S)], _ => ⟨W, S, rfl⟩
  | (W, S) :: (W', S') :: rest, _ => by
    obtain ⟨W0, S0, h0⟩ := build_last' ((W', S') :: rest) (by simp)
    refine ⟨W0, S0, ?_⟩
    have e : build ((W, S) :: (W', S') :: rest) = posOf W S (some W') :: build ((W', S') :: rest) := rfl
    rw [e, List.getLast?_cons, h0]; rfl

theorem build_last (ps : List (List Cell × List Cell)) :
    ((build ps).getLast?.map fun p => p.R) = ((build ps).getLast?.map fun p => p.W) := by
  cases ps with
  | nil => rfl
  | cons q rest =>
    obtain ⟨W0, S0, h0⟩ := build_last' (q :: rest) (by simp)
    rw [h0]; rfl

theorem build_W : ∀ (ps : List (List Cell × List Cell)),
    (build ps).map Harf.Pos.W = ps.map fun p => unprojW p.1
  | [] => rfl
  | [(W, S)] => rfl
  | (W, S) :: (W', S') :: rest => by
    simp only [build, List.map_cons, posOf]
    congr 1
    simpa using build_W ((W', S') :: rest)

/-! ## ٦. المودَعُ على المواضع -/

theorem depT_build : ∀ (rest : List (List Cell × List Cell)) (L W S : List Cell), L ≠ [] →
    (∀ p ∈ (W, S) :: rest, CondA p) →
    Harf.depT (unprojW L) (build ((W, S) :: rest)) = (strictJoinB L W && depTailA S rest)
  | [], L, W, S, hL, h => by
    have hW : W ≠ [] := (h (W, S) (by simp)).1.1
    simp only [build, posOf, Harf.depT, Bool.and_true, depTailA]
    rw [join_eq_strictJoinB _ _ (unprojW_ne hL) (unprojW_ne hW),
      projW_unprojW, projW_unprojW]
  | (W', S') :: rest, L, W, S, hL, h => by
    have hW := (h (W, S) (by simp)).1
    have hS : okLen S ∨ True := Or.inr trivial
    have e : build ((W, S) :: (W', S') :: rest) = posOf W S (some W') :: build ((W', S') :: rest) := rfl
    have hSne : (repair S W').1 ≠ [] := by
      have hSF := (h (W, S) (by simp)).2.2
      have := startForm_repair S W W' hW hSF
      intro he
      have hR := unprojW_ne (repair_ne W W' hW)
      cases hv : Harf.startsV (unprojW (repair W W').1)
      · obtain ⟨y, _, hy⟩ := this.2 hv; rw [he] at hy; simp [unprojW] at hy
      · have := this.1 hv; rw [he] at this; exact hR this.symm
    rw [e]
    simp only [Harf.depT, posOf]
    rw [depT_build rest (repair S W').1 W' S' hSne (fun p hp => h p (by simp_all)),
      join_eq_strictJoinB _ _ (unprojW_ne hL) (unprojW_ne hW.1), projW_unprojW, projW_unprojW]
    rfl

theorem depB_build (S1 : List Cell) (W1 : List Cell) (rest : List (List Cell × List Cell))
    (h1 : okLen S1) (h : ∀ p ∈ rest, CondA p) :
    Harf.depB (build ((S1, S1) :: rest)) = depA ((W1, S1) :: rest) := by
  cases rest with
  | nil => simp [build, posOf, Harf.depB, Harf.depT, depA, depTailA, wasl_eq_strictB, projW_unprojW]
  | cons q rest =>
    obtain ⟨W2, S2⟩ := q
    have e : build ((S1, S1) :: (W2, S2) :: rest) = posOf S1 S1 (some W2) :: build ((W2, S2) :: rest) := rfl
    rw [e]
    simp only [Harf.depB, posOf, depA, depTailA]
    rw [wasl_eq_strictB, projW_unprojW, depT_build rest _ W2 S2 (repair_ne S1 W2 h1) h]
    rfl

/-! ## ٧. المبرهنة -/

theorem repairsL_ne : ∀ (ws : List (List Cell)), (∀ w ∈ ws, okLen w) → ∀ w ∈ repairsL ws, w ≠ []
  | [], _ => by simp [repairsL]
  | [w], h => by
    intro u hu
    simp only [repairsL, List.mem_singleton] at hu
    subst hu; exact (h u (by simp)).1
  | w :: v :: rest, h => by
    intro u hu
    simp only [repairsL, List.mem_cons] at hu
    rcases hu with rfl | hu
    · exact repair_ne w v (h w (by simp))
    · exact repairsL_ne (v :: rest) (fun x hx => h x (by simp_all)) u (by simpa using hu)

/-- **سدُّ `CONTEXT_DEPOSIT_VS_PAIRS_UNPROVEN`**: المودَعُ هو السطرُ المصلَح، وصورةُ ابتداء الأولى خامًا،
وكلُّ كلمةٍ بعدها خامًا مرخَّصةٌ بعد «بَ». -/
theorem deposit_eq_line (W1 S1 : List Cell) (rest : List (List Cell × List Cell))
    (h1 : okLen S1) (h : ∀ p ∈ rest, CondA p) :
    depA ((W1, S1) :: rest) =
      (strictLineB (repairsL (S1 :: rest.map Prod.fst)) && strictB S1 &&
        rest.all fun p => strictJoinB baA p.1) := by
  rw [← depB_build S1 W1 rest h1 h]
  have hb : build ((S1, S1) :: rest) = posOf S1 S1 (rest.head?.map Prod.fst) :: build rest := by
    cases rest with
    | nil => rfl
    | cons q rest => obtain ⟨W2, S2⟩ := q; rfl
  have hall : ∀ p ∈ build rest, Harf.PosOK p := build_posOK rest h
  have hlast := build_last ((S1, S1) :: rest)
  rw [hb] at hlast ⊢
  have hR1 : (posOf S1 S1 (rest.head?.map Prod.fst)).R ≠ [] := by
    cases rest.head?.map Prod.fst with
    | none => exact unprojW_ne h1.1
    | some r => exact unprojW_ne (repair_ne S1 r h1)
  have hS1 : (posOf S1 S1 (rest.head?.map Prod.fst)).S = (posOf S1 S1 (rest.head?.map Prod.fst)).R := by
    cases rest.head?.map Prod.fst <;> rfl
  rw [Harf.dep_eq _ _ hR1 hS1 hall hlast]
  -- السطر
  have hRs : (posOf S1 S1 (rest.head?.map Prod.fst) :: build rest).map Harf.Pos.R =
      (repairsL (S1 :: rest.map Prod.fst)).map unprojW := by
    rw [← hb, build_R]; rfl
  have hne : ∀ w ∈ repairsL (S1 :: rest.map Prod.fst), w ≠ [] :=
    repairsL_ne _ (by
      intro w hw
      simp only [List.mem_cons, List.mem_map] at hw
      rcases hw with rfl | ⟨p, hp, rfl⟩
      · exact h1
      · exact (h p hp).1)
  have hline : Harf.lineB ((repairsL (S1 :: rest.map Prod.fst)).map unprojW) =
      strictLineB (repairsL (S1 :: rest.map Prod.fst)) := by
    rw [line_eq_strictLineB _ (by
      intro w hw; simp only [List.mem_map] at hw; obtain ⟨u, hu, rfl⟩ := hw; exact unprojW_ne (hne u hu))]
    congr 1
    simp only [projL, List.map_map]
    conv => rhs; rw [← List.map_id (repairsL _)]
    exact List.map_congr_left (fun w _ => projW_unprojW w)
  -- الأولى
  have hW1 : Harf.waslB (posOf S1 S1 (rest.head?.map Prod.fst)).W = strictB S1 := by
    cases rest.head?.map Prod.fst <;> simp only [posOf] <;> rw [wasl_eq_strictB, projW_unprojW]
  -- الخام
  have hraw : Harf.rawOK (build rest) = rest.all fun p => strictJoinB baA p.1 := by
    have e1 : Harf.rawOK (build rest) =
        ((build rest).map Harf.Pos.W).all fun w => Harf.qabilWasl (Harf.endC w) := by
      simp [Harf.rawOK, List.all_map, Function.comp_def]
    have e : ∀ p ∈ rest, Harf.qabilWasl (Harf.endC (unprojW p.1)) = strictJoinB baA p.1 := by
      intro p hp
      rw [Harf.raw_eq_ba _ (by rw [freeFirst_unprojW]; exact (h p hp).2.1), ← unproj_ba,
        join_eq_strictJoinB _ _ (by decide +kernel) (unprojW_ne (h p hp).1.1), projW_unprojW, projW_unprojW]
    rw [e1, build_W, List.all_map, Bool.eq_iff_iff]
    simp only [List.all_eq_true, Function.comp_def]
    constructor
    · intro H p hp; rw [← e p hp]; exact H p hp
    · intro H p hp; rw [e p hp]; exact H p hp
  rw [hRs, hline, hW1, hraw]
  cases strictB S1 <;> cases strictLineB (repairsL (S1 :: rest.map Prod.fst)) <;> simp

/-! ## ٩. الوقفُ آخرَ السطر (`exit = pause`) -/

def depTailAQ : List Cell → List (List Cell × List Cell) → Bool
  | _, [] => true
  | Sp, [(W, _)] => strictJoinPauseRepairedB Sp W
  | Sp, (W, S) :: q :: rest => strictJoinRepairedB Sp W && depTailAQ S (q :: rest)

/-- المودَعُ كما يُولَّد: آخرُ السطر وقف، والكلمةُ الواحدةُ ابتداءٌ ووقف. -/
def depAQ : List (List Cell × List Cell) → Bool
  | [] => true
  | [(_, S)] => strictPauseB S
  | (_, S) :: q :: rest => strictB S && depTailAQ S (q :: rest)

/-- كلُّ كلمةٍ خامٍ بعد الأولى مرخَّصةٌ بعد «بَ»، والأخيرةُ وقفًا. -/
def rawAQ : List (List Cell × List Cell) → Bool
  | [] => true
  | [(W, _)] => strictJoinPauseB baA W
  | (W, _) :: q :: rest => strictJoinB baA W && rawAQ (q :: rest)

theorem sukunTail_of_okLen (W : List Cell) (h : okLen W) : Harf.sukunTail (unprojW W) = true := by
  match W with
  | [] => exact absurd rfl h.1
  | x :: [] =>
    have hx : x.haraka ≠ .sukun := by
      intro hs
      have := h.2 (by simp [endsSukun, hs])
      simp at this
    have := unproj_sukun x (mem_cells x)
    have hb : (x.haraka == .sukun) = false := by simpa using hx
    rw [hb] at this
    have hu : (unproj x).haal ≠ .sukun := by simpa using this
    simp [unprojW, Harf.sukunTail, hu]
  | x :: y :: t => simp [unprojW, Harf.sukunTail]

/-- الزوجُ الأوّلُ بعد يسارٍ مصلَح، وقفًا إن كان الأخير. -/
def dq (L : List Cell) : List (List Cell × List Cell) → Bool
  | [] => true
  | [(W, _)] => strictJoinPauseB L W
  | (W, S) :: q :: rest => strictJoinB L W && depTailAQ S (q :: rest)

theorem depTQ_build : ∀ (rest : List (List Cell × List Cell)) (L W S : List Cell), L ≠ [] →
    (∀ p ∈ (W, S) :: rest, CondA p) →
    Harf.depTQ (unprojW L) (build ((W, S) :: rest)) = dq L ((W, S) :: rest)
  | [], L, W, S, hL, h => by
    have hW : W ≠ [] := (h (W, S) (by simp)).1.1
    simp only [build, posOf, Harf.depTQ, dq]
    rw [joinWaqf_eq_strictJoinPauseB _ _ (unprojW_ne hL) (unprojW_ne hW), projW_unprojW, projW_unprojW]
  | (W', S') :: rest, L, W, S, hL, h => by
    have hW := (h (W, S) (by simp)).1
    have e : build ((W, S) :: (W', S') :: rest) = posOf W S (some W') :: build ((W', S') :: rest) := rfl
    have hSne : (repair S W').1 ≠ [] := by
      have := startForm_repair S W W' hW (h (W, S) (by simp)).2.2
      intro he
      have hR := unprojW_ne (repair_ne W W' hW)
      cases hv : Harf.startsV (unprojW (repair W W').1)
      · obtain ⟨y, _, hy⟩ := this.2 hv; rw [he] at hy; simp [unprojW] at hy
      · have := this.1 hv; rw [he] at this; exact hR this.symm
    obtain ⟨b, bs, hb⟩ : ∃ b bs, build ((W', S') :: rest) = b :: bs := by
      cases rest with
      | nil => exact ⟨_, _, rfl⟩
      | cons q r => exact ⟨_, _, rfl⟩
    have ih := depTQ_build rest (repair S W').1 W' S' hSne (fun p hp => h p (by simp_all))
    rw [e, hb]
    rw [hb] at ih
    simp only [Harf.depTQ, posOf]
    rw [ih, join_eq_strictJoinB _ _ (unprojW_ne hL) (unprojW_ne hW.1), projW_unprojW, projW_unprojW]
    cases rest with
    | nil => rfl
    | cons q r => rfl

theorem rawQ_build : ∀ (ps : List (List Cell × List Cell)), (∀ p ∈ ps, CondA p) →
    Harf.rawQ (build ps) = rawAQ ps
  | [], _ => rfl
  | [(W, S)], h => by
    have hc := h (W, S) (by simp)
    simp only [build, posOf, Harf.rawQ, rawAQ]
    rw [Harf.raw_eq_ba_waqf _ (by rw [freeFirst_unprojW]; exact hc.2.1) (sukunTail_of_okLen W hc.1),
      ← unproj_ba, joinWaqf_eq_strictJoinPauseB _ _ (by decide +kernel) (unprojW_ne hc.1.1),
      projW_unprojW, projW_unprojW]
  | (W, S) :: (W', S') :: rest, h => by
    have hc := h (W, S) (by simp)
    have e : build ((W, S) :: (W', S') :: rest) = posOf W S (some W') :: build ((W', S') :: rest) := rfl
    obtain ⟨b, bs, hb⟩ : ∃ b bs, build ((W', S') :: rest) = b :: bs := by
      cases rest with
      | nil => exact ⟨_, _, rfl⟩
      | cons q r => exact ⟨_, _, rfl⟩
    have ih := rawQ_build ((W', S') :: rest) (fun p hp => h p (by simp_all))
    rw [e, hb]; rw [hb] at ih
    simp only [Harf.rawQ, posOf, rawAQ]
    rw [ih, Harf.raw_eq_ba _ (by rw [freeFirst_unprojW]; exact hc.2.1), ← unproj_ba,
      join_eq_strictJoinB _ _ (by decide +kernel) (unprojW_ne hc.1.1), projW_unprojW, projW_unprojW]

theorem build_mem_W (ps : List (List Cell × List Cell)) (x : Harf.Pos) (hx : x ∈ build ps) :
    ∃ p ∈ ps, x.W = unprojW p.1 := by
  have h1 : x.W ∈ (build ps).map Harf.Pos.W := List.mem_map.2 ⟨x, hx, rfl⟩
  rw [build_W] at h1
  obtain ⟨p, hp, he⟩ := List.mem_map.1 h1
  exact ⟨p, hp, he.symm⟩

/-- **سدُّ `CONTEXT_DEPOSIT_VS_PAIRS_UNPROVEN` كما يُولَّد المودَع**: آخرُ السطر وقف — المودَعُ هو السطرُ المصلَحُ
وقفًا (`strictLinePauseB`)، وصورةُ ابتداء الأولى، وكلُّ كلمةٍ بعدها خامًا بعد «بَ» (والأخيرةُ وقفًا). -/
theorem deposit_eq_line_pause (W1 S1 : List Cell) (q : List Cell × List Cell)
    (rest : List (List Cell × List Cell)) (h1 : okLen S1) (h : ∀ p ∈ q :: rest, CondA p) :
    depAQ ((W1, S1) :: q :: rest) =
      (strictLinePauseB (repairsL (S1 :: (q :: rest).map Prod.fst)) && strictB S1 && rawAQ (q :: rest)) := by
  obtain ⟨W2, S2⟩ := q
  -- المودَعُ على المواضع
  have hdep : depAQ ((W1, S1) :: (W2, S2) :: rest) = Harf.depBQ (build ((S1, S1) :: (W2, S2) :: rest)) := by
    have e : build ((S1, S1) :: (W2, S2) :: rest) =
        posOf S1 S1 (some W2) :: build ((W2, S2) :: rest) := rfl
    obtain ⟨b, bs, hb⟩ : ∃ b bs, build ((W2, S2) :: rest) = b :: bs := by
      cases rest with
      | nil => exact ⟨_, _, rfl⟩
      | cons q r => exact ⟨_, _, rfl⟩
    have ht := depTQ_build rest (repair S1 W2).1 W2 S2 (repair_ne S1 W2 h1) h
    rw [hb] at ht
    rw [e, hb]
    simp only [Harf.depBQ, posOf, depAQ]
    rw [ht, wasl_eq_strictB, projW_unprojW]
    cases rest with
    | nil => rfl
    | cons q r => rfl
  rw [hdep]
  have e : build ((S1, S1) :: (W2, S2) :: rest) = posOf S1 S1 (some W2) :: build ((W2, S2) :: rest) := rfl
  obtain ⟨b, bs, hb⟩ : ∃ b bs, build ((W2, S2) :: rest) = b :: bs := by
    cases rest with
    | nil => exact ⟨_, _, rfl⟩
    | cons q r => exact ⟨_, _, rfl⟩
  have hall : ∀ x ∈ b :: bs, Harf.PosOK x := by rw [← hb]; exact build_posOK _ h
  have htl : ∀ x ∈ b :: bs, Harf.sukunTail x.W = true := by
    intro x hx; rw [← hb] at hx
    obtain ⟨p, hp, he⟩ := build_mem_W _ x hx
    rw [he]; exact sukunTail_of_okLen _ (h p hp).1
  have hlast := build_last ((W2, S2) :: rest)
  rw [hb] at hlast
  rw [e, hb, Harf.dep_eq_waqf _ _ _ (unprojW_ne (repair_ne S1 W2 h1)) rfl hall htl hlast]
  -- السطر
  have hRs : (posOf S1 S1 (some W2) :: b :: bs).map Harf.Pos.R =
      (repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst)).map unprojW := by
    rw [← hb, ← e, build_R]; rfl
  have hne : ∀ w ∈ repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst), w ≠ [] :=
    repairsL_ne _ (by
      intro w hw
      rcases List.mem_cons.1 hw with rfl | hw
      · exact h1
      · obtain ⟨p, hp, rfl⟩ := List.mem_map.1 hw; exact (h p hp).1)
  have hline : Harf.lineWaqfB ((repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst)).map unprojW) =
      strictLinePauseB (repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst)) := by
    rw [lineWaqf_eq_strictLinePauseB _ (by
      intro w hw; simp only [List.mem_map] at hw; obtain ⟨u, hu, rfl⟩ := hw; exact unprojW_ne (hne u hu))]
    congr 1
    simp only [projL, List.map_map]
    conv => rhs; rw [← List.map_id (repairsL _)]
    exact List.map_congr_left (fun w _ => projW_unprojW w)
  have hraw : Harf.rawQ (b :: bs) = rawAQ ((W2, S2) :: rest) := by rw [← hb]; exact rawQ_build _ h
  rw [hRs, hline, hraw]
  simp only [posOf]
  rw [wasl_eq_strictB, projW_unprojW]
  cases strictB S1 <;> simp

/-- والكلمةُ وحدَها في سطرها: صورةُ ابتدائها وقفًا. -/
theorem deposit_one (W1 S1 : List Cell) : depAQ [(W1, S1)] = strictPauseB S1 := rfl

/-! ## ٨. الشاهدان -/

def biA : List Cell := [atom 'ب' .kasra]
def qaalA : List Cell := [atom 'ق' .fatha, atom 'ا' .sukun, atom 'ل' .sukun]
def hamduStart : List Cell := atom 'ء' .fatha :: A116.Iltiqa.lhamdu

/-- «بِ قَالْ الْحَمْدُ». -/
def biQaalHamdA : List (List Cell × List Cell) :=
  [(biA, biA), (qaalA, qaalA), (A116.Iltiqa.lhamdu, hamduStart)]

/-- **الخامُ لازم**: السطرُ المصلَح («بِ قَالِ لْحَمْدُ») مرخَّص، والمودَعُ يرفض لأنّ «قَالْ» خامًا لا تُرخَّص بعد «بَ». -/
theorem deposit_needs_raw :
    depA biQaalHamdA = false ∧
    strictLineB (repairsL (biA :: (biQaalHamdA.tail.map Prod.fst))) = true ∧ strictB biA = true ∧
    strictJoinB baA qaalA = false ∧
    repairsL [qaalA, A116.Iltiqa.lhamdu] =
      [[atom 'ق' .fatha, atom 'ا' .sukun, atom 'ل' .kasra], A116.Iltiqa.lhamdu] := by
  decide +kernel

/-- والوقفُ كذلك: «بِ قَالْ الْحَمْدُ» آخرُها وقف — السطرُ وقفًا مرخَّص والمودَعُ يرفض. -/
theorem deposit_needs_raw_pause :
    depAQ biQaalHamdA = false ∧
    strictLinePauseB (repairsL (biA :: (biQaalHamdA.tail.map Prod.fst))) = true ∧ strictB biA = true ∧
    rawAQ biQaalHamdA.tail = false := by
  decide +kernel

theorem biQaalHamdA_cond : ∀ p ∈ biQaalHamdA.tail, CondA p := by
  simp only [biQaalHamdA, List.tail_cons, List.mem_cons, List.not_mem_nil, or_false]
  rintro p (rfl | rfl)
  · refine ⟨⟨by decide, fun _ => by decide⟩, by decide +kernel, fun _ => rfl, fun h => ?_⟩
    exact absurd h (by decide +kernel)
  · refine ⟨⟨by decide, fun _ => by decide⟩, by decide +kernel, fun h => ?_, fun _ => ⟨_, by decide, rfl⟩⟩
    exact absurd h (by decide +kernel)

/-- **الأوّلُ الحرّ لازم**: «ءَ» ثمّ «اْلْ» (أوّلُها حرفُ مدٍّ ساكن) — المودَعُ غيرُ الصيغة. -/
theorem deposit_needs_free :
    let W : List Cell := [atom 'ا' .sukun, atom 'ل' .sukun]
    let S : List Cell := atom 'ء' .fatha :: W
    freeA W = false ∧
    depA [([atom 'ء' .fatha], [atom 'ء' .fatha]), (W, S)] ≠
      (strictLineB (repairsL [[atom 'ء' .fatha], W]) && strictB [atom 'ء' .fatha] && strictJoinB baA W) := by
  decide +kernel

end HarfBridge
