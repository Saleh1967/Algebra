import HarfBridge.Mawda
import Harf.Tazamun

/-!
# المودَعُ هو السطرُ بلا قيد الأوّل الحرّ ولا قيد الطول، في خانات الغانم (ADR ٧)

يعمّم `HarfBridge.Mawda` (ADR ٦) فيرفع ثلاثةَ قيود:

* **الكلمةُ الداخليّةُ تبتدئ بحرف مدٍّ ساكن**: تُقبل إن تلاه متحرّك (`ShapeA`: «ايْمُ»)؛ وبعد أوّل متحرّكٍ تنسى
  الآلةُ ما قبلها. والشرطُ لازم: إن تلاه ساكنٌ افترق المودَعُ عن الصيغة (`deposit_needs_vowel_after_madd`).
* **الكلمةُ ذاتُ الخانة الواحدة الساكنة**: لا قيدَ على الطول — إن أُصلحت (كُسرت) فما قبلها مختومٌ بمتحرّكٍ حتمًا،
  لأنّها تبتدئ بساكن، فالحالُ قبلها مفتوح.
* **صورةُ ابتداءٍ تزيد أكثرَ من خانة**: أيُّ سابقةٍ `P` مرخَّصةٍ مختومةٍ بمتحرّك (`StartB`).

**`deposit_eq_line_shape`** (آخرُ السطر وقف، كما يُولَّد المودَع) و**`deposit_eq_line_shape_wasl`**:

`depAQ ((W₁,S₁) :: ps) = strictLinePauseB (repairsL (S₁ :: Wᵢ…)) && strictB S₁ && rawAQ ps`

بشرط كلّ كلمةٍ بعد الأولى: غيرُ فارغة، ومن الأشكال، وصورةُ ابتدائها هي أو مسبوقةٌ بسابقةٍ مرخَّصةٍ مختومةٍ بمتحرّك.
-/

set_option autoImplicit false

namespace HarfBridge

open A116 A116.Stages A116.Ternary A116.Hadd A116.NizamLine A116.Iltiqa A116.Ladder

/-! ## ١. الأشكالُ والسوابقُ في الغانم -/

/-- أوّلُ الكلمة متحرّكٌ، أو ساكنٌ ليس حرفَ مدّ، أو حرفُ مدٍّ ساكنٌ يليه متحرّك. -/
def ShapeA : List Cell → Bool
  | x :: z :: t => freeA (x :: z :: t) ||
      (x.haraka == .sukun && (maddVowel x.carrier).isSome && z.haraka != .sukun)
  | w => freeA w

/-- صورةُ الابتداء: الكلمةُ نفسُها مبتدأةً بمتحرّك، أو مسبوقةٌ بسابقةٍ مرخَّصةٍ مختومةٍ بمتحرّك. -/
def StartB (S W : List Cell) : Prop :=
  (S = W ∧ startsVA W = true) ∨ ∃ P, S = P ++ W ∧ P ≠ [] ∧ strictB P = true ∧ EndsVowel P

def CondB (p : List Cell × List Cell) : Prop := p.1 ≠ [] ∧ ShapeA p.1 = true ∧ StartB p.2 p.1

theorem unproj_maddS : ∀ c ∈ A116.cells,
    Harf.maddS (unproj c) = (c.haraka == .sukun && (maddVowel c.carrier).isSome) := by decide +kernel

theorem unproj_vowel (c : Cell) : ((unproj c).haal != .sukun) = (c.haraka != .sukun) := by
  have := unproj_sukun c (mem_cells c)
  simp only [bne, this]

theorem shape_unprojW (W : List Cell) : Harf.Shape (unprojW W) = ShapeA W := by
  match W with
  | [] => rfl
  | [x] => simp only [unprojW, List.map_cons, List.map_nil, Harf.Shape, ShapeA]; exact freeFirst_unprojW [x]
  | x :: z :: t =>
    simp only [unprojW, List.map_cons, Harf.Shape, ShapeA]
    rw [unproj_maddS x (mem_cells x), unproj_vowel z]
    have := freeFirst_unprojW (x :: z :: t)
    simp only [unprojW, List.map_cons] at this
    rw [this]

/-! ## ٢. الإصلاحُ: أشكالُه، والسابقةُ لا تمسّه -/

theorem kindOne_none_ne_v (x : Cell) : kindOne none x ≠ .v := by
  unfold kindOne; split <;> simp

theorem repair_cases (l r : List Cell) :
    (repair l r).1 = l ∨ ∃ a, l.getLast? = some a ∧ a.haraka = .sukun ∧
      (((repair l r).1 = l.dropLast ∧ 2 ≤ l.length) ∨
        (repair l r).1 = l.dropLast ++ [⟨a.carrier, .kasra⟩]) := by
  cases he : endsSukun l
  · left; rw [repair_noop_of_left_vowel l r he]
  · obtain ⟨a, ha, hs⟩ := endsSukun_some he
    rcases repair_eq l r with h0 | ⟨hf, h1⟩ | ⟨hv, h2⟩ | ⟨b, hb, h3⟩
    · left; rw [h0]
    · right; refine ⟨a, ha, hs, Or.inl ⟨by rw [h1], ?_⟩⟩
      simp only [endsFarqAlif, Bool.and_eq_true, beq_iff_eq] at hf
      have hd : l.dropLast ≠ [] := by intro h; rw [h] at hf; simp at hf
      have : l.dropLast.length ≥ 1 := List.length_pos_iff.2 hd
      simp only [List.length_dropLast] at this; omega
    · right; refine ⟨a, ha, hs, Or.inl ⟨by rw [h2], ?_⟩⟩
      match l, ha with
      | [x], _ =>
        simp [lastKind, kindOf, kindGo] at hv
        exact absurd hv (kindOne_none_ne_v x)
      | _ :: _ :: _, _ => simp
    · rw [ha] at hb; cases hb
      right; exact ⟨a, ha, hs, Or.inr (by rw [h3])⟩

theorem repair_ne' (l r : List Cell) (hl : l ≠ []) : (repair l r).1 ≠ [] := by
  rcases repair_cases l r with h | ⟨a, _, _, ⟨h, h2⟩ | h⟩
  · rw [h]; exact hl
  · rw [h]; match l, h2 with
    | _ :: _ :: _, _ => simp
  · rw [h]; simp

theorem shapeA_two (x z : Cell) (t t' : List Cell) : ShapeA (x :: z :: t) = ShapeA (x :: z :: t') := rfl

theorem dropLast_cons2 (x z : Cell) (t : List Cell) (ht : t ≠ []) :
    (x :: z :: t).dropLast = x :: z :: t.dropLast := by
  match t, ht with
  | _ :: _, _ => rfl

theorem shape_repair (W r : List Cell) (hW : ShapeA W = true) : ShapeA (repair W r).1 = true := by
  rcases repair_cases W r with h | ⟨a, ha, hs, ⟨h, h2⟩ | h⟩
  · rw [h]; exact hW
  · rw [h]
    match W, h2, ha with
    | [x, z], _, ha =>
      simp at ha; subst ha
      simp only [ShapeA, Bool.or_eq_true, Bool.and_eq_true, beq_iff_eq, bne_iff_ne, ne_eq] at hW
      rcases hW with hW | ⟨_, hz⟩
      · simpa [ShapeA, freeA] using hW
      · exact absurd hs hz
    | x :: z :: y :: t, _, _ =>
      rw [dropLast_cons2 x z (y :: t) (by simp), shapeA_two x z _ (y :: t)]; exact hW
  · rw [h]
    match W, ha with
    | [x], ha =>
      simp at ha; subst ha
      simp [ShapeA, freeA]
    | [x, z], ha =>
      simp at ha; subst ha
      simp only [ShapeA, Bool.or_eq_true, Bool.and_eq_true, beq_iff_eq, bne_iff_ne, ne_eq] at hW
      rcases hW with hW | ⟨_, hz⟩
      · simp only [List.dropLast, List.cons_append, List.nil_append, ShapeA, Bool.or_eq_true]
        left; simpa [freeA] using hW
      · exact absurd hs hz
    | x :: z :: y :: t, _ =>
      rw [dropLast_cons2 x z (y :: t) (by simp)]
      simp only [List.cons_append]
      rw [shapeA_two x z _ (y :: t)]; exact hW

theorem repairOf_unproj (W r : List Cell) : Harf.RepairOf (unprojW W) (unprojW (repair W r).1) := by
  rcases repair_cases W r with h | ⟨a, ha, hs, ⟨h, _⟩ | h⟩
  · left; rw [h]
  · right
    refine ⟨unprojW W.dropLast, unproj a, ?_, unproj_sukun' a hs, Or.inl (by rw [h])⟩
    conv => lhs; rw [← dropLast_append_of_getLast? ha]
    simp [unprojW]
  · right
    refine ⟨unprojW W.dropLast, unproj a, ?_, unproj_sukun' a hs, Or.inr ?_⟩
    · conv => lhs; rw [← dropLast_append_of_getLast? ha]
      simp [unprojW]
    · rw [h]; simp [unprojW, unproj_kasra a (mem_cells a)]

theorem lastKind_go (p q : Option Haraka) (a b : Cell) (t : List Cell) :
    (kindGo p (a :: b :: t)).getLast? = (kindGo q (a :: b :: t)).getLast? := by
  simp [kindGo]

theorem lastKind_append (P W : List Cell) (hW : W ≠ []) (hs : ShapeA W = true) :
    lastKind (P ++ W) = lastKind W := by
  unfold lastKind kindOf
  rw [kindGo_append, List.getLast?_append]
  match W, hW with
  | [x], _ =>
    have hf : (x.haraka != .sukun || maddVowel x.carrier == none) = true := by
      simpa [ShapeA, freeA] using hs
    have h1 : ∀ p : Option Haraka, kindOne p x = kindOne none x := by
      intro p
      unfold kindOne
      by_cases hx : x.haraka ≠ .sukun
      · simp [hx]
      · have hm : maddVowel x.carrier = none := by simpa [hx] using hf
        simp [hx, hm]
    simp [kindGo, h1]
  | a :: b :: t, _ =>
    rw [lastKind_go (lastH none P) none a b t]
    cases h : (kindGo none (a :: b :: t)).getLast? with
    | none => simp [kindGo] at h
    | some k => simp

theorem endsFarqAlif_append (P W : List Cell) (hW : W ≠ []) (hs : ShapeA W = true) :
    endsFarqAlif (P ++ W) = endsFarqAlif W := by
  match W, hW with
  | [x], _ =>
    have hx : x ≠ atom 'ا' .sukun := by
      intro h; subst h; simp [ShapeA, freeA] at hs
      revert hs; decide
    simp [endsFarqAlif, List.getLast?_append, hx]
  | a :: b :: t, _ =>
    unfold endsFarqAlif
    rw [List.getLast?_append, List.dropLast_append_of_ne_nil (by simp), List.getLast?_append]
    obtain ⟨c, hc⟩ : ∃ c, (a :: b :: t).getLast? = some c := by
      cases h : (a :: b :: t).getLast? with
      | none => simp at h
      | some c => exact ⟨c, rfl⟩
    obtain ⟨d, hd⟩ : ∃ d, (a :: b :: t).dropLast.getLast? = some d := by
      cases h : (a :: b :: t).dropLast.getLast? with
      | none => simp [List.dropLast] at h
      | some d => exact ⟨d, rfl⟩
    rw [hc, hd]; rfl

/-- **السابقةُ لا تمسّ الإصلاح**: إصلاحُ `P ++ W` هو `P ++` إصلاحِ `W`. -/
theorem repair_append (P W r : List Cell) (hW : W ≠ []) (hs : ShapeA W = true) :
    (repair (P ++ W) r).1 = P ++ (repair W r).1 := by
  have he : endsSukun (P ++ W) = endsSukun W := by
    simp only [endsSukun, List.getLast?_append]
    cases h : W.getLast? with
    | none => simp at h; exact absurd h hW
    | some a => simp
  have hg : (P ++ W).getLast? = W.getLast? := by
    rw [List.getLast?_append]
    cases h : W.getLast? with
    | none => simp at h; exact absurd h hW
    | some a => simp
  unfold repair
  rw [he, endsFarqAlif_append P W hW hs, lastKind_append P W hW hs, hg,
    List.dropLast_append_of_ne_nil hW]
  split
  · rfl
  · split
    · simp
    · split
      · simp
      · split <;> simp

/-! ## ٣. الحالُ قبل الكلمة الساكنة الأوّل مفتوح -/

theorem repair_some (l r : List Cell) (hl : endsSukun l = true) (hr : startsSukun r = true) :
    ∃ t, (repair l r).2 = some t := by
  obtain ⟨a, ha, _⟩ := endsSukun_some hl
  unfold repair
  simp only [hr, hl, Bool.and_self, Bool.not_true, Bool.false_eq_true, ↓reduceIte]
  split
  · exact ⟨_, rfl⟩
  · split
    · exact ⟨_, rfl⟩
    · rw [ha]; exact ⟨_, rfl⟩

theorem endsV_unprojW (l : List Cell) (h : EndsVowel l) : Harf.endsV (unprojW l) = true := by
  obtain ⟨p, hp, hv⟩ := h
  unfold Harf.endsV
  rw [show (unprojW l).getLast? = l.getLast?.map unproj by simp [unprojW, List.getLast?_map], hp]
  simp only [Option.map_some]
  rw [unproj_vowel]; simpa using hv

theorem endsVowel_repair (l r : List Cell) (hl : l ≠ []) (hr : startsSukun r = true) :
    EndsVowel (repair l r).1 := by
  cases he : endsSukun l
  · rw [repair_noop_of_left_vowel l r he]
    cases h : l.getLast? with
    | none => simp at h; exact absurd h hl
    | some a =>
      refine ⟨a, h, ?_⟩
      intro hs; simp [endsSukun, h, hs] at he
  · obtain ⟨t, ht⟩ := repair_some l r he hr
    exact repaired_endsVowel l r t ht

theorem head_or_sukun (W r : List Cell) :
    (repair W r).1.head? = W.head? ∨ startsSukun W = true := by
  rcases repair_cases W r with h | ⟨a, ha, hs, ⟨h, h2⟩ | h⟩
  · left; rw [h]
  · left; rw [h, head?_dropLast W h2]
  · match W, ha with
    | [x], ha =>
      simp at ha; subst ha
      right; simp [startsSukun, hs]
    | x :: y :: t, _ =>
      left; rw [h, List.head?_append, head?_dropLast _ (by simp)]; simp

theorem startsVA_repair' (W r : List Cell) (hv : startsVA W = true) : startsVA (repair W r).1 = true := by
  rcases head_or_sukun W r with h | h
  · cases hr : (repair W r).1 with
    | nil => exact absurd hr (repair_ne' W r (by intro e; subst e; simp [startsVA] at hv))
    | cons x t =>
      rw [hr] at h
      cases W with
      | nil => simp [startsVA] at hv
      | cons y u => simp at h; subst h; simpa [startsVA] using hv
  · cases W with
    | nil => simp [startsVA] at hv
    | cons y u => simp [startsSukun, startsVA] at h hv; exact absurd h hv

/-! ## ٤. المواضعُ أشكالٌ في Harf -/

theorem startShape_of (S W : List Cell) (n : Option (List Cell)) (hW : W ≠ []) (hs : ShapeA W = true)
    (hS : StartB S W) :
    Harf.StartShape (unprojW (match n with | none => S | some r => (repair S r).1))
      (unprojW (match n with | none => W | some r => (repair W r).1)) := by
  rcases hS with ⟨he, hv⟩ | ⟨P, rfl, hP, hPl, hPe⟩
  · left; rw [he]; refine ⟨rfl, ?_⟩
    cases n with
    | none => rw [startsV_unprojW']; exact hv
    | some r => rw [startsV_unprojW']; exact startsVA_repair' W r hv
  · right
    refine ⟨unprojW P, ?_, ?_⟩
    · cases n with
      | none => simp [unprojW]
      | some r => simp only; rw [repair_append P W r hW hs]; simp [unprojW]
    · apply Harf.opn_of_endsV .bad' (unprojW P) (endsV_unprojW P hPe)
      have := wasl_eq_strictB (unprojW P)
      rw [projW_unprojW, hPl] at this
      exact this

theorem posShape_of (W S : List Cell) (n : Option (List Cell)) (h : CondB (W, S)) :
    Harf.PosShape (posOf W S n) := by
  obtain ⟨hW, hs, hS⟩ : W ≠ [] ∧ ShapeA W = true ∧ StartB S W := h
  have hst := startShape_of S W n hW hs hS
  have hSne : S ≠ [] := by
    rcases hS with ⟨he, _⟩ | ⟨P, rfl, hP, _, _⟩
    · rw [he]; exact hW
    · simp [hP]
  cases n with
  | none =>
    exact ⟨unprojW_ne hW, unprojW_ne hW, unprojW_ne hSne,
      show Harf.Shape (unprojW W) = true by rw [shape_unprojW]; exact hs,
      show Harf.Shape (unprojW W) = true by rw [shape_unprojW]; exact hs, Or.inl rfl, hst⟩
  | some r =>
    exact ⟨unprojW_ne hW, unprojW_ne (repair_ne' W r hW), unprojW_ne (repair_ne' S r hSne),
      show Harf.Shape (unprojW W) = true by rw [shape_unprojW]; exact hs,
      show Harf.Shape (unprojW (repair W r).1) = true by rw [shape_unprojW]; exact shape_repair W r hs,
      repairOf_unproj W r, hst⟩

theorem build_posShape : ∀ (ps : List (List Cell × List Cell)), (∀ p ∈ ps, CondB p) →
    ∀ q ∈ build ps, Harf.PosShape q
  | [], _ => by simp [build]
  | [(W, S)], h => by
    intro q hq; simp only [build, List.mem_singleton] at hq; subst hq
    exact posShape_of W S none (h _ (by simp))
  | (W, S) :: (W', S') :: rest, h => by
    intro q hq
    simp only [build, List.mem_cons] at hq
    rcases hq with rfl | hq
    · exact posShape_of W S _ (h _ (by simp))
    · exact build_posShape ((W', S') :: rest) (fun p hp => h p (List.mem_cons_of_mem _ hp)) q
        (by simpa using hq)

theorem head_unprojW' (l : List Cell) : (unprojW l).head? = l.head?.map unproj := by
  simp [unprojW, List.head?_map]

/-- السلسلةُ: ما قبل كلّ كلمةٍ هو `X` مصلَحًا عليها. -/
theorem headChain_build : ∀ (rest : List (List Cell × List Cell)) (X : List Cell), X ≠ [] →
    (∀ p ∈ rest, CondB p) →
    Harf.HeadChain (unprojW (match rest with | [] => X | (W, _) :: _ => (repair X W).1)) (build rest)
  | [], _, _, _ => trivial
  | [(W, S)], X, hX, h => ⟨Or.inl rfl, trivial⟩
  | (W, S) :: (W', S') :: rest, X, hX, h => by
    have hW := (h (W, S) (by simp)).1
    refine ⟨?_, ?_⟩
    · simp only [posOf]
      rcases head_or_sukun W W' with he | he
      · left; rw [head_unprojW', head_unprojW', he]
      · right; exact endsV_unprojW _ (endsVowel_repair X W hX he)
    · exact headChain_build ((W', S') :: rest) W hW (fun p hp => h p (List.mem_cons_of_mem _ hp))

/-! ## ٥. المودَعُ على المواضع، بلا قيدٍ سوى ألّا تفرغ -/

theorem depT_build' : ∀ (rest : List (List Cell × List Cell)) (L W S : List Cell), L ≠ [] →
    (∀ p ∈ (W, S) :: rest, p.1 ≠ [] ∧ p.2 ≠ []) →
    Harf.depT (unprojW L) (build ((W, S) :: rest)) = (strictJoinB L W && depTailA S rest)
  | [], L, W, S, hL, h => by
    have hW : W ≠ [] := (h (W, S) (by simp)).1
    simp only [build, posOf, Harf.depT, Bool.and_true, depTailA]
    rw [join_eq_strictJoinB _ _ (unprojW_ne hL) (unprojW_ne hW), projW_unprojW, projW_unprojW]
  | (W', S') :: rest, L, W, S, hL, h => by
    have hW := h (W, S) (by simp)
    have e : build ((W, S) :: (W', S') :: rest) = posOf W S (some W') :: build ((W', S') :: rest) := rfl
    rw [e]
    simp only [Harf.depT, posOf]
    rw [depT_build' rest (repair S W').1 W' S' (repair_ne' S W' hW.2)
      (fun p hp => h p (List.mem_cons_of_mem _ hp)),
      join_eq_strictJoinB _ _ (unprojW_ne hL) (unprojW_ne hW.1), projW_unprojW, projW_unprojW]
    rfl

theorem depTQ_build' : ∀ (rest : List (List Cell × List Cell)) (L W S : List Cell), L ≠ [] →
    (∀ p ∈ (W, S) :: rest, p.1 ≠ [] ∧ p.2 ≠ []) →
    Harf.depTQ (unprojW L) (build ((W, S) :: rest)) = dq L ((W, S) :: rest)
  | [], L, W, S, hL, h => by
    have hW : W ≠ [] := (h (W, S) (by simp)).1
    simp only [build, posOf, Harf.depTQ, dq]
    rw [joinWaqf_eq_strictJoinPauseB _ _ (unprojW_ne hL) (unprojW_ne hW), projW_unprojW, projW_unprojW]
  | (W', S') :: rest, L, W, S, hL, h => by
    have hW := h (W, S) (by simp)
    have e : build ((W, S) :: (W', S') :: rest) = posOf W S (some W') :: build ((W', S') :: rest) := rfl
    obtain ⟨b, bs, hb⟩ : ∃ b bs, build ((W', S') :: rest) = b :: bs := by
      cases rest with
      | nil => exact ⟨_, _, rfl⟩
      | cons q r => exact ⟨_, _, rfl⟩
    have ih := depTQ_build' rest (repair S W').1 W' S' (repair_ne' S W' hW.2)
      (fun p hp => h p (List.mem_cons_of_mem _ hp))
    rw [e, hb]
    rw [hb] at ih
    simp only [Harf.depTQ, posOf]
    rw [ih, join_eq_strictJoinB _ _ (unprojW_ne hL) (unprojW_ne hW.1), projW_unprojW, projW_unprojW]
    cases rest with
    | nil => rfl
    | cons q r => rfl

theorem localQ_build : ∀ (ps : List (List Cell × List Cell)), (∀ p ∈ ps, p.1 ≠ []) →
    Harf.localQ (build ps) = rawAQ ps
  | [], _ => rfl
  | [(W, S)], h => by
    have hW : W ≠ [] := h (W, S) (by simp)
    simp only [build, posOf, Harf.localQ, rawAQ]
    rw [← unproj_ba, joinWaqf_eq_strictJoinPauseB _ _ (by decide +kernel) (unprojW_ne hW),
      projW_unprojW, projW_unprojW]
  | (W, S) :: (W', S') :: rest, h => by
    have e : build ((W, S) :: (W', S') :: rest) = posOf W S (some W') :: build ((W', S') :: rest) := rfl
    obtain ⟨b, bs, hb⟩ : ∃ b bs, build ((W', S') :: rest) = b :: bs := by
      cases rest with
      | nil => exact ⟨_, _, rfl⟩
      | cons q r => exact ⟨_, _, rfl⟩
    have ih := localQ_build ((W', S') :: rest) (fun p hp => h p (List.mem_cons_of_mem _ hp))
    have hW : W ≠ [] := h (W, S) (by simp)
    rw [e, hb]; rw [hb] at ih
    simp only [Harf.localQ, posOf, rawAQ]
    rw [ih, ← unproj_ba, join_eq_strictJoinB _ _ (by decide +kernel) (unprojW_ne hW),
      projW_unprojW, projW_unprojW]

/-! ## ٦. المبرهنتان -/

theorem cond_ne (p : List Cell × List Cell) (h : CondB p) : p.1 ≠ [] ∧ p.2 ≠ [] := by
  refine ⟨h.1, ?_⟩
  rcases h.2.2 with ⟨he, _⟩ | ⟨P, he, hP, _, _⟩
  · rw [he]; exact h.1
  · rw [he]; simp [hP]

theorem repairsL_ne' : ∀ (ws : List (List Cell)), (∀ w ∈ ws, w ≠ []) → ∀ w ∈ repairsL ws, w ≠ []
  | [], _ => by simp [repairsL]
  | [w], h => by
    intro u hu
    simp only [repairsL, List.mem_singleton] at hu
    subst hu; exact h u (by simp)
  | w :: v :: rest, h => by
    intro u hu
    simp only [repairsL, List.mem_cons] at hu
    rcases hu with rfl | hu
    · exact repair_ne' w v (h w (by simp))
    · exact repairsL_ne' (v :: rest) (fun x hx => h x (List.mem_cons_of_mem _ hx)) u (by simpa using hu)

/-- **المودَعُ هو السطرُ، كما يُولَّد** (آخرُه وقف): بلا قيد الأوّل الحرّ ولا قيد الطول ولا قيد خانة الابتداء. -/
theorem deposit_eq_line_shape (W1 S1 : List Cell) (q : List Cell × List Cell)
    (rest : List (List Cell × List Cell)) (h1 : S1 ≠ []) (h : ∀ p ∈ q :: rest, CondB p) :
    depAQ ((W1, S1) :: q :: rest) =
      (strictLinePauseB (repairsL (S1 :: (q :: rest).map Prod.fst)) && strictB S1 && rawAQ (q :: rest)) := by
  obtain ⟨W2, S2⟩ := q
  have hne := fun p (hp : p ∈ (W2, S2) :: rest) => cond_ne p (h p hp)
  have e : build ((S1, S1) :: (W2, S2) :: rest) = posOf S1 S1 (some W2) :: build ((W2, S2) :: rest) := rfl
  obtain ⟨b, bs, hb⟩ : ∃ b bs, build ((W2, S2) :: rest) = b :: bs := by
    cases rest with
    | nil => exact ⟨_, _, rfl⟩
    | cons q r => exact ⟨_, _, rfl⟩
  have hdep : depAQ ((W1, S1) :: (W2, S2) :: rest) = Harf.depBQ (build ((S1, S1) :: (W2, S2) :: rest)) := by
    have ht := depTQ_build' rest (repair S1 W2).1 W2 S2 (repair_ne' S1 W2 h1) hne
    rw [hb] at ht
    rw [e, hb]
    simp only [Harf.depBQ, posOf, depAQ]
    rw [ht, wasl_eq_strictB, projW_unprojW]
    cases rest with
    | nil => rfl
    | cons q r => rfl
  rw [hdep, e, hb]
  have hs : ∀ x ∈ b :: bs, Harf.PosShape x := by rw [← hb]; exact build_posShape _ h
  have hh : Harf.HeadChain (posOf S1 S1 (some W2)).R (b :: bs) := by
    rw [← hb]; exact headChain_build ((W2, S2) :: rest) S1 h1 h
  have hlast := build_last ((W2, S2) :: rest)
  rw [hb] at hlast
  rw [Harf.dep_shape_waqf _ _ (by simp) rfl (unprojW_ne (repair_ne' S1 W2 h1)) (repairOf_unproj S1 W2)
    hs hh hlast]
  have hRs : (posOf S1 S1 (some W2) :: b :: bs).map Harf.Pos.R =
      (repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst)).map unprojW := by
    rw [← hb, ← e, build_R]; rfl
  have hne' : ∀ w ∈ repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst), w ≠ [] :=
    repairsL_ne' _ (by
      intro w hw
      rcases List.mem_cons.1 hw with rfl | hw
      · exact h1
      · obtain ⟨p, hp, rfl⟩ := List.mem_map.1 hw; exact (hne p hp).1)
  have hline : Harf.lineWaqfB ((repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst)).map unprojW) =
      strictLinePauseB (repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst)) := by
    rw [lineWaqf_eq_strictLinePauseB _ (by
      intro w hw; simp only [List.mem_map] at hw; obtain ⟨u, hu, rfl⟩ := hw; exact unprojW_ne (hne' u hu))]
    congr 1
    simp only [projL, List.map_map]
    conv => rhs; rw [← List.map_id (repairsL _)]
    exact List.map_congr_left (fun w _ => projW_unprojW w)
  have hraw : Harf.localQ (b :: bs) = rawAQ ((W2, S2) :: rest) := by
    rw [← hb]; exact localQ_build _ (fun p hp => (hne p hp).1)
  rw [hRs, hline, hraw]
  simp only [posOf]
  rw [wasl_eq_strictB, projW_unprojW]
  cases strictB S1 <;> cases strictLinePauseB (repairsL (S1 :: ((W2, S2) :: rest).map Prod.fst)) <;> simp

/-- **وصلًا** (السطرُ كلُّه وصل). -/
theorem deposit_eq_line_shape_wasl (W1 S1 : List Cell) (rest : List (List Cell × List Cell))
    (h1 : S1 ≠ []) (h : ∀ p ∈ rest, CondB p) :
    depA ((W1, S1) :: rest) =
      (strictLineB (repairsL (S1 :: rest.map Prod.fst)) && strictB S1 &&
        rest.all fun p => strictJoinB baA p.1) := by
  have hne := fun p (hp : p ∈ rest) => cond_ne p (h p hp)
  have hb : build ((S1, S1) :: rest) = posOf S1 S1 (rest.head?.map Prod.fst) :: build rest := by
    cases rest with
    | nil => rfl
    | cons q rest => obtain ⟨W2, S2⟩ := q; rfl
  have hdep : depA ((W1, S1) :: rest) = Harf.depB (build ((S1, S1) :: rest)) := by
    cases rest with
    | nil => simp [build, posOf, Harf.depB, Harf.depT, depA, depTailA, wasl_eq_strictB, projW_unprojW]
    | cons q rest =>
      obtain ⟨W2, S2⟩ := q
      have e : build ((S1, S1) :: (W2, S2) :: rest) = posOf S1 S1 (some W2) :: build ((W2, S2) :: rest) := rfl
      rw [e]
      simp only [Harf.depB, posOf, depA, depTailA]
      rw [wasl_eq_strictB, projW_unprojW, depT_build' rest _ W2 S2 (repair_ne' S1 W2 h1) hne]
      rfl
  rw [hdep, hb]
  have hR1 : (posOf S1 S1 (rest.head?.map Prod.fst)).R ≠ [] := by
    cases rest.head?.map Prod.fst with
    | none => exact unprojW_ne h1
    | some r => exact unprojW_ne (repair_ne' S1 r h1)
  have hS1 : (posOf S1 S1 (rest.head?.map Prod.fst)).S = (posOf S1 S1 (rest.head?.map Prod.fst)).R := by
    cases rest.head?.map Prod.fst <;> rfl
  have h1A : Harf.RepairOf (posOf S1 S1 (rest.head?.map Prod.fst)).W (posOf S1 S1 (rest.head?.map Prod.fst)).R := by
    cases rest.head?.map Prod.fst with
    | none => exact Or.inl rfl
    | some r => exact repairOf_unproj S1 r
  have hs : ∀ x ∈ build rest, Harf.PosShape x := build_posShape rest h
  have hh : Harf.HeadChain (posOf S1 S1 (rest.head?.map Prod.fst)).R (build rest) := by
    have := headChain_build rest S1 h1 h
    cases rest with
    | nil => trivial
    | cons q r => obtain ⟨W2, S2⟩ := q; simpa [posOf] using this
  rw [Harf.dep_shape _ _ hS1 hR1 h1A hs hh]
  have hRs : (posOf S1 S1 (rest.head?.map Prod.fst) :: build rest).map Harf.Pos.R =
      (repairsL (S1 :: rest.map Prod.fst)).map unprojW := by
    rw [← hb, build_R]; rfl
  have hne' : ∀ w ∈ repairsL (S1 :: rest.map Prod.fst), w ≠ [] :=
    repairsL_ne' _ (by
      intro w hw
      rcases List.mem_cons.1 hw with rfl | hw
      · exact h1
      · obtain ⟨p, hp, rfl⟩ := List.mem_map.1 hw; exact (hne p hp).1)
  have hline : Harf.lineB ((repairsL (S1 :: rest.map Prod.fst)).map unprojW) =
      strictLineB (repairsL (S1 :: rest.map Prod.fst)) := by
    rw [line_eq_strictLineB _ (by
      intro w hw; simp only [List.mem_map] at hw; obtain ⟨u, hu, rfl⟩ := hw; exact unprojW_ne (hne' u hu))]
    congr 1
    simp only [projL, List.map_map]
    conv => rhs; rw [← List.map_id (repairsL _)]
    exact List.map_congr_left (fun w _ => projW_unprojW w)
  have hW1 : Harf.waslB (posOf S1 S1 (rest.head?.map Prod.fst)).W = strictB S1 := by
    cases rest.head?.map Prod.fst <;> simp only [posOf] <;> rw [wasl_eq_strictB, projW_unprojW]
  have hraw : ((build rest).all fun p => Harf.joinB [Harf.k 'ب' .fath] p.W) =
      rest.all fun p => strictJoinB baA p.1 := by
    have e1 : ((build rest).all fun p => Harf.joinB [Harf.k 'ب' .fath] p.W) =
        ((build rest).map Harf.Pos.W).all fun w => Harf.joinB [Harf.k 'ب' .fath] w := by
      simp [List.all_map, Function.comp_def]
    rw [e1, build_W, List.all_map, Bool.eq_iff_iff]
    simp only [List.all_eq_true, Function.comp_def]
    have e : ∀ p ∈ rest, Harf.joinB [Harf.k 'ب' .fath] (unprojW p.1) = strictJoinB baA p.1 := by
      intro p hp
      rw [← unproj_ba, join_eq_strictJoinB _ _ (by decide +kernel) (unprojW_ne (hne p hp).1),
        projW_unprojW, projW_unprojW]
    constructor
    · intro H p hp; rw [← e p hp]; exact H p hp
    · intro H p hp; rw [e p hp]; exact H p hp
  rw [hRs, hline, hW1, hraw]
  cases strictB S1 <;> cases strictLineB (repairsL (S1 :: rest.map Prod.fst)) <;> simp

/-! ## ٧. الشاهد: الشرطُ لازم -/

def abbaA : List Cell := [atom 'ا' .sukun, atom 'ب' .sukun, atom 'ب' .fatha]

/-- «بَ اْبْبَ وَ»، وصورةُ ابتداء الثانية «ءِاْبْبَ»: حرفُ مدٍّ ساكنٌ يليه ساكن. في السطر الألفُ بعد فتحةٍ مدٌّ يُغلقه
أوّلُ مثلين (حَاجَّ)، وفي صورة الابتداء بعد كسرةٍ فهي ساكنٌ يليه ساكن؛ فالمودَعُ يرفض والصيغةُ تقبل، وصلًا ووقفًا. -/
theorem deposit_needs_vowel_after_madd :
    ShapeA abbaA = false ∧
    depAQ [([atom 'ب' .fatha], [atom 'ب' .fatha]), (abbaA, atom 'ء' .kasra :: abbaA),
      ([atom 'و' .fatha], [atom 'و' .fatha])] = false ∧
    (strictLinePauseB (repairsL [[atom 'ب' .fatha], abbaA, [atom 'و' .fatha]]) && strictB [atom 'ب' .fatha] &&
      rawAQ [(abbaA, atom 'ء' .kasra :: abbaA), ([atom 'و' .fatha], [atom 'و' .fatha])]) = true ∧
    depA [([atom 'ب' .fatha], [atom 'ب' .fatha]), (abbaA, atom 'ء' .kasra :: abbaA),
      ([atom 'و' .fatha], [atom 'و' .fatha])] = false ∧
    (strictLineB (repairsL [[atom 'ب' .fatha], abbaA, [atom 'و' .fatha]]) && strictB [atom 'ب' .fatha] &&
      strictJoinB baA abbaA && strictJoinB baA [atom 'و' .fatha]) = true := by
  decide +kernel

/-- وما سوى الشكل من شروط المبرهنة قائمٌ في الشاهد. -/
theorem abbaA_start : StartB (atom 'ء' .kasra :: abbaA) abbaA ∧ abbaA ≠ [] := by
  refine ⟨Or.inr ⟨[atom 'ء' .kasra], rfl, by simp, by decide +kernel, ⟨atom 'ء' .kasra, rfl, by decide⟩⟩, by simp [abbaA]⟩

/-- **ما رُفع من القيود مشمول**: «ايْمُ» (حرفُ مدٍّ ساكنٌ يليه متحرّك) و«بْ» (خانةٌ واحدةٌ ساكنة) من الأشكال، وصورةُ
ابتداءٍ بسابقةٍ من خانتين («بَءَ» قبل «لْ…») صورةٌ مقبولة. -/
theorem lifted_examples :
    ShapeA [atom 'ي' .sukun, atom 'م' .damma] = true ∧ ShapeA [atom 'ب' .sukun] = true ∧
    StartB ([atom 'ب' .fatha, atom 'ء' .fatha] ++ [atom 'ل' .sukun, atom 'ه' .fatha])
      [atom 'ل' .sukun, atom 'ه' .fatha] := by
  refine ⟨by decide +kernel, by decide +kernel, Or.inr ⟨[atom 'ب' .fatha, atom 'ء' .fatha], rfl, by simp,
    by decide +kernel, ⟨atom 'ء' .fatha, rfl, by decide⟩⟩⟩

/-- وهمزةُ الوصل بحركاتها الثلاث سابقةٌ مرخَّصةٌ مختومةٌ بمتحرّك: فصورةُ ابتداء كلّ كلمةٍ تُسبق بها من `StartB`. -/
theorem hamza_prefix (v : Haraka) (hv : v ∈ [Haraka.fatha, .kasra, .damma]) (W : List Cell) :
    StartB (atom 'ء' v :: W) W := by
  refine Or.inr ⟨[atom 'ء' v], rfl, by simp, ?_, ⟨atom 'ء' v, rfl, ?_⟩⟩
  · simp only [List.mem_cons, List.not_mem_nil, or_false] at hv
    rcases hv with rfl | rfl | rfl <;> decide +kernel
  · simp only [List.mem_cons, List.not_mem_nil, or_false] at hv
    rcases hv with rfl | rfl | rfl <;> decide

end HarfBridge
