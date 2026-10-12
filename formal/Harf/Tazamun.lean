import Harf.Mawda

/-!
# التزامن: المودَعُ هو السطرُ بلا قيد الأوّل الحرّ ولا قيد الطول (ADR ٧)

`Harf.Mawda` برهن «المودَع = السطر ∧ الخام» بثلاثة قيود: أوّلُ كلّ كلمةٍ داخليّةٍ حرّ، والكلمةُ المختومةُ بساكنٍ
خانتان فأكثر، وصورةُ الابتداء متحرّكٌ واحدٌ قبل الكلمة. وهنا الحلّ العامّ، في طبقتين:

1. **التزامنُ الدقيق** (`dep_sync`، `dep_sync_waqf`): المودَعُ هو السطرُ وكلُّ كلمةٍ خامٍ **في موضعها من السطر**
   (`rawW`) — بشرطٍ واحدٍ على كلّ حدّ: حالُ صورة الابتداء من أوّلها وحالُ السطر عند آخر الكلمة **سواءٌ** على ما
   بعدهما (`Sync`)، وإصلاحُ الآخر لا يُميت (`Alive`). لا قيدَ على أوّل الكلمة ولا على طولها.
2. **التوطين** (`raw_local`، `raw_local_waqf`): الكلمةُ الخامُ في موضعها هي الكلمةُ الخامُ بعد «بَ»، إن كان أوّلُها
   حرًّا أو حرفَ مدٍّ ساكنًا يليه متحرّك (`Shape`): بعد أوّل متحرّكٍ تنسى الآلةُ ما قبلها.

والعلاقةُ التي تجعل صورةَ الابتداء «سواءً» مع السطر (`rel`): الحالان واحد، أو بينهما مدُّ الفرق وحدَه
(`hamzaAwwal`/`nawah fath`، `farq`/`madd`، `tawilFarq`/`tawil ل`) — مغلقةٌ بالخطوة (`rel_step`)، ولا تفرّق
كلمةً من `Shape` (`same_of_rel`).
-/

set_option autoImplicit false

namespace Harf

/-- السطرُ من حالٍ بعد حدّ. -/
def fwd (s : Hal) (w : List Khana) : Hal := run wasl (hadd s) w
def fwdQ (s : Hal) (w : List Khana) : Hal := run waqf (hadd s) w

/-! ## ١. السطرُ سلسلةُ حالات -/

def lineSt : Hal → List Pos → Hal
  | s, [] => s
  | s, p :: ps => lineSt (fwd s p.R) ps

/-- وآخرُه وقفًا. -/
def lineStQ : Hal → List Pos → Hal
  | s, [] => s
  | s, [p] => fwdQ s p.R
  | s, p :: q :: ps => lineStQ (fwd s p.R) (q :: ps)

theorem runLine_lineSt : ∀ (ps : List Pos) (a : Hal) (w : List Khana),
    runLine wasl a (w :: ps.map Pos.R) = lineSt (run wasl a w) ps
  | [], _, _ => rfl
  | p :: ps, a, w => by
    show runLine wasl a (w :: p.R :: ps.map Pos.R) = _
    rw [show runLine wasl a (w :: p.R :: ps.map Pos.R) =
      runLine wasl (hadd (run wasl a w)) (p.R :: ps.map Pos.R) from rfl, runLine_lineSt ps]
    rfl

theorem lineB_lineSt (R1 : List Khana) (ps : List Pos) :
    lineB (R1 :: ps.map Pos.R) = qabilWasl (lineSt (run wasl .bad' R1) ps) := by
  rw [lineB, runLine_lineSt]

theorem runMix_lineStQ : ∀ (ps : List Pos) (a : Hal) (w : List Khana), ps ≠ [] →
    runMix a (w :: ps.map Pos.R) = lineStQ (run wasl a w) ps
  | [], _, _, h => absurd rfl h
  | [p], _, _, _ => rfl
  | p :: q :: ps, a, w, _ => by
    show runMix a (w :: p.R :: q.R :: ps.map Pos.R) = _
    rw [show runMix a (w :: p.R :: q.R :: ps.map Pos.R) =
      runMix (hadd (run wasl a w)) (p.R :: (q :: ps).map Pos.R) from rfl,
      runMix_lineStQ (q :: ps) _ _ (by simp)]
    rfl

theorem lineWaqfB_lineStQ (R1 : List Khana) (ps : List Pos) (hps : ps ≠ [])
    (hne : ∀ w ∈ R1 :: ps.map Pos.R, w ≠ []) :
    lineWaqfB (R1 :: ps.map Pos.R) = qabilWaqf (lineStQ (run wasl .bad' R1) ps) := by
  rw [lineWaqfB, line_mix _ _ hne, runMix_lineStQ ps _ _ hps]

theorem joinB_fwd (S W : List Khana) : joinB S W = qabilWasl (fwd (run wasl .bad' S) W) := rfl

theorem joinWaqfB_fwdQ (S W : List Khana) (hS : S ≠ []) (hW : W ≠ []) :
    joinWaqfB S W = qabilWaqf (fwdQ (run wasl .bad' S) W) := by
  rw [joinWaqfB, lineWaqfB, line_mix [S, W] .bad' (by
    intro w hw; simp only [List.mem_cons, List.not_mem_nil, or_false] at hw
    rcases hw with rfl | rfl
    · exact hS
    · exact hW)]
  rfl

/-! ## ٢. الطبقةُ الأولى: التزامن -/

/-- الحالان سواءٌ على الكلمة وصلًا ووقفًا. -/
def Same (a b : Hal) (w : List Khana) : Prop := fwd a w = fwd b w ∧ fwdQ a w = fwdQ b w

/-- الإصلاحُ لا يُميت كلمةً حيّة، من أيّ حال. -/
def Alive (p : Pos) : Prop :=
  ∀ a, qabilWasl (run wasl a p.W) = true → qabilWasl (run wasl a p.R) = true

/-- التزامنُ على الحدّ بين `p` و`q`: صورةُ ابتداء `p` من أوّلها سواءٌ مع السطر عند آخرها، على كلمتَي `q`. -/
def Sync (p q : Pos) : Prop :=
  ∀ s, s ≠ .bad' → qabilWasl (fwd s p.R) = true →
    Same (run wasl .bad' p.S) (fwd s p.R) q.W ∧ Same (run wasl .bad' p.S) (fwd s p.R) q.R

def SyncL : List Pos → Prop
  | p :: q :: r => Sync p q ∧ SyncL (q :: r)
  | _ => True

/-- الكلمةُ الخامُ في موضعها من السطر. -/
def rawW : Hal → List Pos → Bool
  | _, [] => true
  | s, p :: ps => qabilWasl (fwd s p.W) && rawW (fwd s p.R) ps

def rawWQ : Hal → List Pos → Bool
  | _, [] => true
  | s, [p] => qabilWaqf (fwdQ s p.W)
  | s, p :: q :: ps => qabilWasl (fwd s p.W) && rawWQ (fwd s p.R) (q :: ps)

def SameHead (μ σ : Hal) : List Pos → Prop
  | [] => True
  | p :: _ => Same μ σ p.W ∧ Same μ σ p.R

theorem run_ne_bad_any (a : Hal) (w : List Khana) (hw : w ≠ []) : run wasl a w ≠ .bad' :=
  run_ne_bad'' a w hw

theorem dep_syncT : ∀ (ps : List Pos) (Sp : List Khana) (s : Hal), s ≠ .bad' → qabilWasl s = true →
    SameHead (run wasl .bad' Sp) s ps → SyncL ps → (∀ p ∈ ps, Alive p) → (∀ p ∈ ps, p.R ≠ []) →
    depT Sp ps = (qabilWasl (lineSt s ps) && rawW s ps)
  | [], _, s, _, hs, _, _, _, _ => by simp [depT, lineSt, rawW, hs]
  | p :: ps, Sp, s, hsb, _, hsame, hsync, hal, hne => by
    have e1 : depT Sp (p :: ps) = (joinB Sp p.W && depT p.S ps) := rfl
    rw [e1, joinB_fwd, hsame.1.1]
    simp only [lineSt, rawW]
    cases hW : qabilWasl (fwd s p.W)
    · simp
    · have hR : qabilWasl (fwd s p.R) = true := hal p (by simp) _ hW
      have hsame' : SameHead (run wasl .bad' p.S) (fwd s p.R) ps := by
        cases ps with
        | nil => trivial
        | cons q r => exact hsync.1 s hsb hR
      have hsync' : SyncL ps := by
        cases ps with
        | nil => trivial
        | cons q r => exact hsync.2
      rw [dep_syncT ps p.S (fwd s p.R) (run_ne_bad_any _ _ (hne p (by simp))) hR hsame' hsync'
        (fun u hu => hal u (List.mem_cons_of_mem _ hu)) (fun u hu => hne u (List.mem_cons_of_mem _ hu))]
      simp

/-- **الطبقةُ الأولى، وصلًا**: المودَعُ هو السطرُ والكلماتُ خامًا في مواضعها. -/
theorem dep_sync (p1 : Pos) (ps : List Pos) (h1S : p1.S = p1.R) (h1 : Alive p1) (h1ne : p1.R ≠ [])
    (hsync : SyncL ps) (hal : ∀ p ∈ ps, Alive p) (hne : ∀ p ∈ ps, p.R ≠ []) :
    depB (p1 :: ps) = (waslB p1.W && lineB ((p1 :: ps).map Pos.R) &&
      rawW (run wasl .bad' p1.R) ps) := by
  have e1 : depB (p1 :: ps) = (waslB p1.W && depT p1.S ps) := rfl
  rw [e1, List.map_cons, lineB_lineSt]
  cases hW : waslB p1.W
  · simp
  · have hR : qabilWasl (run wasl .bad' p1.R) = true := h1 .bad' hW
    rw [dep_syncT ps p1.S _ (run_ne_bad_any _ _ h1ne) hR (by
      rw [h1S]
      cases ps with
      | nil => trivial
      | cons q r => exact ⟨⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩) hsync hal hne]
    simp

theorem dep_syncTQ : ∀ (ps : List Pos) (Sp : List Khana) (s : Hal), ps ≠ [] → Sp ≠ [] → s ≠ .bad' →
    qabilWasl s = true → SameHead (run wasl .bad' Sp) s ps → SyncL ps → (∀ p ∈ ps, Alive p) →
    (∀ p ∈ ps, p.R ≠ [] ∧ p.W ≠ [] ∧ p.S ≠ []) →
    ((ps.getLast?.map fun p => p.R) = (ps.getLast?.map fun p => p.W)) →
    depTQ Sp ps = (qabilWaqf (lineStQ s ps) && rawWQ s ps)
  | [], _, _, h, _, _, _, _, _, _, _, _ => absurd rfl h
  | [p], Sp, s, _, hSp, _, _, hsame, _, _, hne, hlast => by
    simp only [List.getLast?_singleton, Option.map_some, Option.some.injEq] at hlast
    simp only [depTQ, lineStQ, rawWQ]
    rw [joinWaqfB_fwdQ _ _ hSp (hne p (by simp)).2.1, hsame.1.2, hlast]
    simp
  | p :: q :: ps, Sp, s, _, _, hsb, _, hsame, hsync, hal, hne, hlast => by
    have e1 : depTQ Sp (p :: q :: ps) = (joinB Sp p.W && depTQ p.S (q :: ps)) := rfl
    rw [e1, joinB_fwd, hsame.1.1]
    simp only [lineStQ, rawWQ]
    cases hW : qabilWasl (fwd s p.W)
    · simp
    · have hR : qabilWasl (fwd s p.R) = true := hal p (by simp) _ hW
      rw [dep_syncTQ (q :: ps) p.S (fwd s p.R) (by simp) (hne p (by simp)).2.2
        (run_ne_bad_any _ _ (hne p (by simp)).1) hR (hsync.1 s hsb hR)
        hsync.2 (fun u hu => hal u (List.mem_cons_of_mem _ hu))
        (fun u hu => hne u (List.mem_cons_of_mem _ hu)) (by simpa using hlast)]
      simp

/-- **الطبقةُ الأولى، وآخرُ السطر وقف**. -/
theorem dep_sync_waqf (p1 : Pos) (ps : List Pos) (hps : ps ≠ []) (h1S : p1.S = p1.R) (h1 : Alive p1)
    (h1ne : p1.R ≠ []) (hsync : SyncL ps) (hal : ∀ p ∈ ps, Alive p)
    (hne : ∀ p ∈ ps, p.R ≠ [] ∧ p.W ≠ [] ∧ p.S ≠ [])
    (hlast : (ps.getLast?.map fun p => p.R) = (ps.getLast?.map fun p => p.W)) :
    depBQ (p1 :: ps) = (waslB p1.W && lineWaqfB ((p1 :: ps).map Pos.R) &&
      rawWQ (run wasl .bad' p1.R) ps) := by
  obtain ⟨q, r, rfl⟩ : ∃ q r, ps = q :: r := by
    cases ps with
    | nil => exact absurd rfl hps
    | cons q r => exact ⟨q, r, rfl⟩
  have e1 : depBQ (p1 :: q :: r) = (waslB p1.W && depTQ p1.S (q :: r)) := rfl
  rw [e1, List.map_cons, lineWaqfB_lineStQ _ _ hps (by
    intro w hw
    rcases List.mem_cons.1 hw with rfl | hw
    · exact h1ne
    · obtain ⟨u, hu, rfl⟩ := List.mem_map.1 hw; exact (hne u hu).1)]
  cases hW : waslB p1.W
  · simp
  · have hR : qabilWasl (run wasl .bad' p1.R) = true := h1 .bad' hW
    rw [dep_syncTQ (q :: r) p1.S _ hps (by rw [h1S]; exact h1ne) (run_ne_bad_any _ _ h1ne) hR (by
      rw [h1S]; exact ⟨⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩) hsync hal hne hlast]
    simp

/-! ## ٣. الطبقةُ الثانية: التوطين -/

/-- الكلمةُ في موضعها هي الكلمةُ بعد «بَ»، ما دام السطرُ حيًّا عندها. -/
def LocalAt (σ : Hal) (q : Pos) : Prop :=
  qabilWasl (fwd σ q.R) = true → qabilWasl (fwd σ q.W) = joinB [k 'ب' .fath] q.W

def LocalAtQ (σ : Hal) (q : Pos) : Prop :=
  qabilWaqf (fwdQ σ q.R) = true → qabilWaqf (fwdQ σ q.W) = joinWaqfB [k 'ب' .fath] q.W

/-- التوطينُ على سلسلة حالات السطر. -/
def LocAll : Hal → List Pos → Prop
  | _, [] => True
  | σ, q :: ps => LocalAt σ q ∧ LocAll (fwd σ q.R) ps

def LocAllQ : Hal → List Pos → Prop
  | _, [] => True
  | σ, [q] => LocalAtQ σ q
  | σ, q :: q' :: ps => LocalAt σ q ∧ LocAllQ (fwd σ q.R) (q' :: ps)

def localQ : List Pos → Bool
  | [] => true
  | [p] => joinWaqfB [k 'ب' .fath] p.W
  | p :: q :: ps => joinB [k 'ب' .fath] p.W && localQ (q :: ps)

theorem doom_wasl_line (s : Hal) (hs : qabilWasl s = false) :
    ∀ (ps : List Pos), (∀ p ∈ ps, p.R ≠ []) → ps ≠ [] → qabilWasl (lineSt s ps) = false
  | [], _, h => absurd rfl h
  | p :: ps, hne, _ => by
    simp only [lineSt]
    have hd : fwd s p.R = .mayyit := by
      rcases hadd_doom s (Hal.mem_all s) hs with h | h
      · unfold fwd; rw [h, run_mayyit]
      · obtain ⟨x, t, hx⟩ : ∃ x t, p.R = x :: t := by
          cases h' : p.R with
          | nil => exact absurd h' (hne p (by simp))
          | cons x t => exact ⟨x, t, rfl⟩
        unfold fwd; rw [h, hx]; simp only [run]
        rw [(doom_step x (Khana.mem_all x)).1, run_mayyit]
    rw [hd]
    cases ps with
    | nil => rfl
    | cons q r => exact doom_wasl_line .mayyit rfl (q :: r) (fun u hu => hne u (by simp [hu])) (by simp)

theorem fwd_doom (s : Hal) (hs : qabilWasl s = false) (w : List Khana) (hw : w ≠ []) :
    fwd s w = .mayyit ∧ fwdQ s w = .mayyit := by
  obtain ⟨x, t, rfl⟩ : ∃ x t, w = x :: t := by
    cases w with
    | nil => exact absurd rfl hw
    | cons x t => exact ⟨x, t, rfl⟩
  rcases hadd_doom s (Hal.mem_all s) hs with h | h
  · unfold fwd fwdQ; rw [h]; simp only [run]
    rw [(doom_step x (Khana.mem_all x)).2.2]
    exact ⟨by simp [wasl, run_mayyit], run_waqf_mayyit t⟩
  · unfold fwd fwdQ; rw [h]; simp only [run]
    rw [(doom_step x (Khana.mem_all x)).1, (doom_step x (Khana.mem_all x)).2.1]
    exact ⟨run_mayyit t, run_waqf_mayyit t⟩

theorem doom_waqf_line (s : Hal) (hs : qabilWasl s = false) :
    ∀ (ps : List Pos), (∀ p ∈ ps, p.R ≠ []) → ps ≠ [] → qabilWaqf (lineStQ s ps) = false
  | [], _, h => absurd rfl h
  | [p], hne, _ => by
    simp only [lineStQ]; rw [(fwd_doom s hs p.R (hne p (by simp))).2]; rfl
  | p :: q :: ps, hne, _ => by
    simp only [lineStQ]
    rw [(fwd_doom s hs p.R (hne p (by simp))).1]
    exact doom_waqf_line .mayyit rfl (q :: ps) (fun u hu => hne u (by simp [hu])) (by simp)

/-- **التوطين، وصلًا**. -/
theorem raw_local : ∀ (ps : List Pos) (σ : Hal), (∀ p ∈ ps, p.R ≠ []) → LocAll σ ps →
    (qabilWasl (lineSt σ ps) && rawW σ ps) =
      (qabilWasl (lineSt σ ps) && ps.all fun p => joinB [k 'ب' .fath] p.W)
  | [], _, _, _ => rfl
  | q :: ps, σ, hne, hL => by
    simp only [lineSt, rawW, List.all_cons]
    cases hR : qabilWasl (fwd σ q.R)
    · cases ps with
      | nil => simp [lineSt, hR]
      | cons q' r =>
        rw [doom_wasl_line _ hR (q' :: r) (fun u hu => hne u (List.mem_cons_of_mem _ hu)) (by simp)]
        simp
    · rw [hL.1 hR]
      have ih := raw_local ps (fwd σ q.R) (fun u hu => hne u (by simp [hu])) hL.2
      cases ha : joinB [k 'ب' .fath] q.W <;> cases hl : qabilWasl (lineSt (fwd σ q.R) ps) <;>
        simp_all

/-- **التوطين، وآخرُ السطر وقف**. -/
theorem raw_local_waqf : ∀ (ps : List Pos) (σ : Hal), (∀ p ∈ ps, p.R ≠ []) → LocAllQ σ ps →
    (qabilWaqf (lineStQ σ ps) && rawWQ σ ps) = (qabilWaqf (lineStQ σ ps) && localQ ps)
  | [], _, _, _ => rfl
  | [q], σ, _, hL => by
    simp only [lineStQ, rawWQ, localQ]
    cases hR : qabilWaqf (fwdQ σ q.R)
    · simp
    · rw [hL hR]
  | q :: q' :: ps, σ, hne, hL => by
    simp only [lineStQ, rawWQ, localQ]
    cases hR : qabilWasl (fwd σ q.R)
    · rw [doom_waqf_line _ hR (q' :: ps) (fun u hu => hne u (by simp [hu])) (by simp)]
      simp
    · rw [hL.1 hR]
      have ih := raw_local_waqf (q' :: ps) (fwd σ q.R) (fun u hu => hne u (by simp [hu])) hL.2
      cases ha : joinB [k 'ب' .fath] q.W <;> cases hl : qabilWaqf (lineStQ (fwd σ q.R) (q' :: ps)) <;>
        simp_all

/-! ## ٤. الأشكال: متى يتزامن الحدّ ويتوطّن -/

/-- حرفُ مدٍّ ساكن. -/
def maddS (x : Khana) : Bool := x.haal == .sukun && jins x.hamil != none

/-- أوّلُ الكلمة حرّ، أو حرفُ مدٍّ ساكنٌ يليه متحرّك. -/
def Shape : List Khana → Bool
  | x :: z :: t => freeFirst (x :: z :: t) || (maddS x && z.haal != .sukun)
  | w => freeFirst w

/-- حالٌ مفتوح: نواةٌ قصيرة، أو همزةٌ مفتوحةٌ أوّلًا. -/
def opn : Hal → Bool
  | .nawah _ => true
  | .hamzaAwwal => true
  | _ => false

def maddList : List Khana := Khana.all.filter maddS

theorem mem_maddList (x : Khana) (h : maddS x = true) : x ∈ maddList :=
  List.mem_filter.2 ⟨Khana.mem_all x, h⟩

theorem free_cell (x : Khana) (h : freeFirst [x] = true) :
    (x.haal != .sukun || jins x.hamil == none) = true := by simpa [freeFirst] using h

/-- من حالٍ مفتوحٍ تُقرأ الخانةُ الحرّةُ قراءتَها بعد الحدّ. -/
theorem opn_free : ∀ a ∈ Hal.all, opn a = true → ∀ x ∈ Khana.all,
    (x.haal != .sukun || jins x.hamil == none) = true → wasl a x = can x := by decide +kernel

theorem opn_waqf_free : ∀ a ∈ Hal.all, opn a = true → ∀ x ∈ Khana.all,
    (x.haal != .sukun || jins x.hamil == none) = true → waqf a x = can x := by decide +kernel

/-- وحرفُ المدّ الساكن ثمّ متحرّكٌ: نواةٌ بحركته، من حالٍ مفتوح. -/
theorem opn_madd : ∀ a ∈ Hal.all, opn a = true → ∀ x ∈ maddList, ∀ z ∈ Khana.all, z.haal ≠ .sukun →
    wasl (wasl a x) z = .nawah z.haal ∧ waqf (waqf a x) z = .nawah z.haal := by decide +kernel

/-- وبعد الحدّ: نواةٌ بحركته أو موت. -/
theorem hadd_madd : ∀ s ∈ Hal.all, ∀ x ∈ maddList, ∀ z ∈ Khana.all, z.haal ≠ .sukun →
    wasl (hadd s) x ≠ .mayyit → wasl (wasl (hadd s) x) z = .nawah z.haal := by decide +kernel

theorem hadd_madd_waqf : ∀ s ∈ Hal.all, ∀ x ∈ maddList, ∀ z ∈ Khana.all, z.haal ≠ .sukun →
    waqf (waqf (hadd s) x) z = .nawah z.haal ∨ waqf (waqf (hadd s) x) z = .mayyit := by decide +kernel

theorem hadd_opn : ∀ a ∈ Hal.all, opn a = true → hadd a = a := by decide

/-- بعد متحرّكٍ: نواةٌ بحركته، أو همزةٌ أوّلًا، أو موت. -/
theorem after_vowel : ∀ a ∈ Hal.all, ∀ x ∈ Khana.all, x.haal ≠ .sukun →
    opn (wasl a x) = true ∨ wasl a x = .mayyit := by decide +kernel

/-- علاقةُ مدّ الفرق: الحالان واحد، أو بينهما مدُّ الفرق وحدَه، أو مات السطر. -/
def rel (μ ν : Hal) : Bool :=
  μ == ν || (μ == .hamzaAwwal && ν == .nawah .fath) || (μ == .farq && ν == .madd) ||
    (μ == .tawilFarq && ν == .tawil lam) || ν == .mayyit

theorem rel_step : ∀ μ ∈ Hal.all, ∀ ν ∈ Hal.all, rel μ ν = true → ∀ x ∈ Khana.all,
    rel (wasl μ x) (wasl ν x) = true := by decide +kernel

theorem rel_start : ∀ s ∈ Hal.all, s ≠ .bad' → ∀ x ∈ Khana.all, x.haal ≠ .sukun →
    rel (wasl .bad' x) (wasl (hadd s) x) = true := by decide +kernel

theorem rel_run : ∀ (t : List Khana) (μ ν : Hal), rel μ ν = true → rel (run wasl μ t) (run wasl ν t) = true
  | [], _, _, h => h
  | x :: t, μ, ν, h => rel_run t _ _ (rel_step μ (Hal.mem_all μ) ν (Hal.mem_all ν) h x (Khana.mem_all x))

/-- همزةُ الفرق والنواةُ المفتوحة سواءٌ على كلّ كلمةٍ من الأشكال. -/
theorem hamza_first_free : ∀ x ∈ Khana.all, (x.haal != .sukun || jins x.hamil == none) = true →
    wasl .hamzaAwwal x = wasl (.nawah .fath) x ∧ waqf .hamzaAwwal x = waqf (.nawah .fath) x := by
  decide +kernel

theorem hamza_first_madd : ∀ x ∈ maddList, ∀ z ∈ Khana.all, z.haal ≠ .sukun →
    wasl (wasl .hamzaAwwal x) z = wasl (wasl (.nawah .fath) x) z ∧
    waqf (waqf .hamzaAwwal x) z = waqf (waqf (.nawah .fath) x) z := by decide +kernel

theorem hadd_farq_madd : hadd .farq = hadd .madd := rfl

theorem shape_cases (w : List Khana) (h : Shape w = true) :
    (∃ x t, w = x :: t ∧ (x.haal != .sukun || jins x.hamil == none) = true) ∨
    (∃ x z t, w = x :: z :: t ∧ maddS x = true ∧ z.haal ≠ .sukun) := by
  match w, h with
  | [], h => simp [Shape, freeFirst] at h
  | [x], h => left; exact ⟨x, [], rfl, by simpa [Shape, freeFirst] using h⟩
  | x :: z :: t, h =>
    simp only [Shape, Bool.or_eq_true] at h
    rcases h with h | h
    · left; exact ⟨x, z :: t, rfl, by simpa [freeFirst] using h⟩
    · right
      simp only [Bool.and_eq_true, bne_iff_ne, ne_eq] at h
      exact ⟨x, z, t, rfl, h.1, h.2⟩

theorem same_hamza (w : List Khana) (hw : Shape w = true) : Same .hamzaAwwal (.nawah .fath) w := by
  unfold Same fwd fwdQ
  rw [hadd_opn _ (Hal.mem_all _) rfl, hadd_opn (.nawah .fath) (Hal.mem_all _) rfl]
  rcases shape_cases w hw with ⟨x, t, rfl, hx⟩ | ⟨x, z, t, rfl, hx, hz⟩
  · obtain ⟨h1, h2⟩ := hamza_first_free x (Khana.mem_all x) hx
    simp only [run]; rw [h1, h2]; exact ⟨rfl, rfl⟩
  · obtain ⟨h1, h2⟩ := hamza_first_madd x (mem_maddList x hx) z (Khana.mem_all z) hz
    simp only [run]; rw [h1, h2]; exact ⟨rfl, rfl⟩

/-- **العلاقةُ لا تفرّق كلمةً من الأشكال** إن كان السطرُ حيًّا. -/
theorem same_of_rel (μ ν : Hal) (h : rel μ ν = true) (hν : qabilWasl ν = true) (w : List Khana)
    (hw : Shape w = true) : Same μ ν w := by
  unfold rel at h
  simp only [Bool.or_eq_true, Bool.and_eq_true, beq_iff_eq] at h
  rcases h with (((h | ⟨rfl, rfl⟩) | ⟨rfl, rfl⟩) | ⟨rfl, rfl⟩) | rfl
  · subst h; exact ⟨rfl, rfl⟩
  · exact same_hamza w hw
  · exact ⟨rfl, rfl⟩
  · simp [qabilWasl] at hν
  · simp [qabilWasl] at hν

theorem run_append (f : Hal → Khana → Hal) : ∀ (a : Hal) (l m : List Khana), run f a (l ++ m) = run f (run f a l) m
  | _, [], _ => rfl
  | a, x :: t, m => run_append f (f a x) t m

theorem opn_madd_alive : ∀ a ∈ Hal.all, opn a = true → ∀ x ∈ maddList, wasl a x ≠ .mayyit := by decide +kernel

theorem run_dead (t : List Khana) (h : run wasl .mayyit t = .mayyit := run_mayyit t) : run wasl .mayyit t = .mayyit := h

/-- الصورةُ المسبوقة بحالٍ مفتوح تقرأ ما يقرؤه السطر بعينه. -/
theorem sync_prefix (P R : List Khana) (hP : opn (run wasl .bad' P) = true) (hR : Shape R = true)
    (s : Hal) (hs : s ≠ .bad') (hq : qabilWasl (fwd s R) = true) : run wasl .bad' (P ++ R) = fwd s R := by
  rw [run_append]
  have hπ := Hal.mem_all (run wasl .bad' P)
  rcases shape_cases R hR with ⟨x, t, rfl, hx⟩ | ⟨x, z, t, rfl, hx, hz⟩
  · unfold fwd at hq ⊢
    simp only [run] at hq ⊢
    rw [opn_free _ hπ hP x (Khana.mem_all x) hx]
    rcases after_hadd_free s (Hal.mem_all s) hs x (Khana.mem_all x) hx with h | h
    · rw [h, run_mayyit] at hq; simp [qabilWasl] at hq
    · rw [h]
  · unfold fwd at hq ⊢
    simp only [run] at hq ⊢
    rw [(opn_madd _ hπ hP x (mem_maddList x hx) z (Khana.mem_all z) hz).1]
    by_cases hm : wasl (hadd s) x = .mayyit
    · rw [hm] at hq; simp only [wasl] at hq; rw [run_mayyit] at hq; simp [qabilWasl] at hq
    · rw [hadd_madd s (Hal.mem_all s) x (mem_maddList x hx) z (Khana.mem_all z) hz hm]

/-- والكلمةُ صورةُ نفسها: بينهما مدُّ الفرق وحدَه. -/
theorem sync_self (R : List Khana) (hv : startsV R = true) (s : Hal) (hs : s ≠ .bad') :
    rel (run wasl .bad' R) (fwd s R) = true := by
  match R, hv with
  | x :: t, hv =>
    have hx : x.haal ≠ .sukun := by simpa [startsV] using hv
    unfold fwd; simp only [run]
    exact rel_run t _ _ (rel_start s (Hal.mem_all s) hs x (Khana.mem_all x) hx)

def StartShape (S R : List Khana) : Prop :=
  (S = R ∧ startsV R = true) ∨ ∃ P, S = P ++ R ∧ opn (run wasl .bad' P) = true

def RepairOf (W R : List Khana) : Prop :=
  R = W ∨ ∃ l x, W = l ++ [x] ∧ x.haal = .sukun ∧ (R = l ∨ R = l ++ [⟨x.hamil, .kasr⟩])

def PosShape (q : Pos) : Prop :=
  q.W ≠ [] ∧ q.R ≠ [] ∧ q.S ≠ [] ∧ Shape q.W = true ∧ Shape q.R = true ∧ RepairOf q.W q.R ∧
    StartShape q.S q.R

theorem sync_of (p q : Pos) (hp : PosShape p) (hq : PosShape q) : Sync p q := by
  intro s hs hR
  obtain ⟨_, _, _, _, hRs, _, hS⟩ := hp
  obtain ⟨_, _, _, hW', hR', _, _⟩ := hq
  rcases hS with ⟨he, hv⟩ | ⟨P, he, hP⟩
  · have hr : rel (run wasl .bad' p.S) (fwd s p.R) = true := by rw [he]; exact sync_self p.R hv s hs
    exact ⟨same_of_rel _ _ hr hR _ hW', same_of_rel _ _ hr hR _ hR'⟩
  · rw [he, sync_prefix P p.R hP hRs s hs hR]
    exact ⟨⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩

theorem syncL_of : ∀ (ps : List Pos), (∀ q ∈ ps, PosShape q) → SyncL ps
  | [], _ => trivial
  | [_], _ => trivial
  | p :: q :: r, h => ⟨sync_of p q (h p (by simp)) (h q (by simp)),
      syncL_of (q :: r) (fun u hu => h u (List.mem_cons_of_mem _ hu))⟩

theorem alive_of (W R : List Khana) (h : RepairOf W R) (a : Hal) (hq : qabilWasl (run wasl a W) = true) :
    qabilWasl (run wasl a R) = true := by
  rcases h with rfl | ⟨l, x, rfl, hx, rfl | rfl⟩
  · exact hq
  · rw [run_snoc] at hq
    exact qabil_drop_last _ (Hal.mem_all _) x (Khana.mem_all x) hx hq
  · rw [run_snoc] at hq ⊢
    exact qabil_kasr_last _ (Hal.mem_all _) x (Khana.mem_all x) hx hq

theorem dropLast_snoc : ∀ (l : List Khana) (a : Khana), l.getLast? = some a → l.dropLast ++ [a] = l
  | [], _, h => by simp at h
  | [x], a, h => by simp at h; simp [h]
  | x :: y :: t, a, h => by
    have ih := dropLast_snoc (y :: t) a (by simpa using h)
    simpa [List.dropLast] using ih

/-- آخرُ الكلمة متحرّك. -/
def endsV (l : List Khana) : Bool :=
  match l.getLast? with
  | some x => x.haal != .sukun
  | none => false

theorem opn_of_endsV (a : Hal) (l : List Khana) (hl : endsV l = true) (hq : qabilWasl (run wasl a l) = true) :
    opn (run wasl a l) = true := by
  unfold endsV at hl
  split at hl
  · rename_i x hx
    have hsplit : l = l.dropLast ++ [x] := (dropLast_snoc l x hx).symm
    rw [hsplit, run_snoc] at hq ⊢
    have hxv : x.haal ≠ .sukun := by simpa using hl
    rcases after_vowel _ (Hal.mem_all _) x (Khana.mem_all x) hxv with h | h
    · exact h
    · rw [h] at hq; simp [qabilWasl] at hq
  · simp at hl

def HeadChain : List Khana → List Pos → Prop
  | _, [] => True
  | Rp, q :: ps => (q.R.head? = q.W.head? ∨ endsV Rp = true) ∧ HeadChain q.R ps

theorem ba_state : run wasl .bad' [k 'ب' .fath] = .nawah .fath := by decide

theorem first_alive (σ : Hal) (W R : List Khana) (hRW : R.head? = W.head? ∨ (qabilWasl σ = true → opn σ = true))
    (hW : Shape W = true) (hR : R ≠ []) (hq : qabilWasl (fwd σ R) = true) :
    ∀ x t, W = x :: t → wasl (hadd σ) x ≠ .mayyit := by
  intro x t hWe
  rcases hRW with he | ho
  · obtain ⟨y, u, hRe⟩ : ∃ y u, R = y :: u := by
      cases R with
      | nil => exact absurd rfl hR
      | cons y u => exact ⟨y, u, rfl⟩
    rw [hRe, hWe] at he; simp only [List.head?_cons, Option.some.injEq] at he
    intro hm
    rw [hRe, he] at hq; unfold fwd at hq; simp only [run] at hq; rw [hm, run_mayyit] at hq
    simp [qabilWasl] at hq
  · have hσ : qabilWasl σ = true := by
      cases hc : qabilWasl σ
      · rw [(fwd_doom σ hc R hR).1] at hq; simp [qabilWasl] at hq
      · rfl
    have ho' := ho hσ
    rw [hadd_opn _ (Hal.mem_all _) ho']
    rcases shape_cases W hW with ⟨x', t', hW', hx⟩ | ⟨x', z, t', hW', hx, _⟩
    · rw [hWe] at hW'; cases hW'
      rw [opn_free _ (Hal.mem_all _) ho' x (Khana.mem_all x) hx]
      unfold can; split <;> simp
    · rw [hWe] at hW'; cases hW'
      exact opn_madd_alive _ (Hal.mem_all _) ho' x (mem_maddList x hx)

theorem localAt_of (σ : Hal) (hσ : σ ≠ .bad') (q : Pos) (hW : Shape q.W = true) (hR : q.R ≠ [])
    (hRW : q.R.head? = q.W.head? ∨ (qabilWasl σ = true → opn σ = true)) : LocalAt σ q := by
  intro hq
  have hfa := first_alive σ q.W q.R hRW hW hR hq
  rw [joinB_fwd, ba_state]
  unfold fwd
  rw [hadd_opn (.nawah .fath) (Hal.mem_all _) rfl]
  rcases shape_cases q.W hW with ⟨x, t, hWe, hx⟩ | ⟨x, z, t, hWe, hx, hz⟩
  · rw [hWe]; simp only [run]
    rw [opn_free (.nawah .fath) (Hal.mem_all _) rfl x (Khana.mem_all x) hx]
    rcases after_hadd_free σ (Hal.mem_all σ) hσ x (Khana.mem_all x) hx with h | h
    · exact absurd h (hfa x t hWe)
    · rw [h]
  · rw [hWe]; simp only [run]
    rw [(opn_madd (.nawah .fath) (Hal.mem_all _) rfl x (mem_maddList x hx) z (Khana.mem_all z) hz).1,
      hadd_madd σ (Hal.mem_all σ) x (mem_maddList x hx) z (Khana.mem_all z) hz (hfa x (z :: t) hWe)]

theorem localAtQ_of (σ : Hal) (hσ : σ ≠ .bad') (q : Pos) (hW : Shape q.W = true) (hWne : q.W ≠ []) (hRW : q.R = q.W) :
    LocalAtQ σ q := by
  intro hq
  rw [hRW] at hq
  rw [joinWaqfB_fwdQ _ _ (by simp) hWne, ba_state]
  unfold fwdQ at hq ⊢
  rw [hadd_opn (.nawah .fath) (Hal.mem_all _) rfl]
  rcases shape_cases q.W hW with ⟨x, t, hWe, hx⟩ | ⟨x, z, t, hWe, hx, hz⟩
  · rw [hWe] at hq ⊢; simp only [run] at hq ⊢
    rw [opn_waqf_free (.nawah .fath) (Hal.mem_all _) rfl x (Khana.mem_all x) hx]
    by_cases hm : wasl (hadd σ) x = .mayyit
    · rcases waqf_dead_step _ (Hal.mem_all _) x (Khana.mem_all x) hm with h1 | ⟨h1, hxs⟩
      · rw [h1, run_waqf_mayyit] at hq; simp [qabilWaqf] at hq
      · rw [h1] at hq ⊢
        cases t with
        | nil => simp [run, can, hxs, qabilWaqf]
        | cons y u => rw [run_waqf_khatm _ (by simp)] at hq; simp [qabilWaqf] at hq
    · rw [wasl_waqf_step _ (Hal.mem_all _) x (Khana.mem_all x) hm]
      rcases after_hadd_free σ (Hal.mem_all σ) hσ x (Khana.mem_all x) hx with h | h
      · exact absurd h hm
      · rw [h]
  · rw [hWe] at hq ⊢; simp only [run] at hq ⊢
    rw [(opn_madd (.nawah .fath) (Hal.mem_all _) rfl x (mem_maddList x hx) z (Khana.mem_all z) hz).2]
    rcases hadd_madd_waqf σ (Hal.mem_all σ) x (mem_maddList x hx) z (Khana.mem_all z) hz with h | h
    · rw [h]
    · rw [h, run_waqf_mayyit] at hq; simp [qabilWaqf] at hq

theorem locAll_of : ∀ (ps : List Pos) (a : Hal) (Rp : List Khana), Rp ≠ [] →
    (∀ q ∈ ps, PosShape q) → HeadChain Rp ps → LocAll (run wasl a Rp) ps
  | [], _, _, _, _, _ => trivial
  | q :: ps, a, Rp, hRp, hs, hh => by
    obtain ⟨_, hR, _, hW, _, _, _⟩ := hs q (by simp)
    refine ⟨localAt_of _ (run_ne_bad_any _ _ hRp) q hW hR ?_, ?_⟩
    · rcases hh.1 with h | h
      · exact Or.inl h
      · exact Or.inr (opn_of_endsV a Rp h)
    · exact locAll_of ps (hadd (run wasl a Rp)) q.R hR (fun u hu => hs u (List.mem_cons_of_mem _ hu)) hh.2

theorem locAllQ_of : ∀ (ps : List Pos) (a : Hal) (Rp : List Khana), Rp ≠ [] →
    (∀ q ∈ ps, PosShape q) → HeadChain Rp ps →
    ((ps.getLast?.map fun p => p.R) = (ps.getLast?.map fun p => p.W)) → LocAllQ (run wasl a Rp) ps
  | [], _, _, _, _, _, _ => trivial
  | [q], a, Rp, hRp, hs, _, hlast => by
    simp only [List.getLast?_singleton, Option.map_some, Option.some.injEq] at hlast
    obtain ⟨hWne, _, _, hW, _, _, _⟩ := hs q (by simp)
    exact localAtQ_of _ (run_ne_bad_any _ _ hRp) q hW hWne hlast
  | q :: q' :: ps, a, Rp, hRp, hs, hh, hlast => by
    obtain ⟨_, hR, _, hW, _, _, _⟩ := hs q (by simp)
    refine ⟨localAt_of _ (run_ne_bad_any _ _ hRp) q hW hR ?_, ?_⟩
    · rcases hh.1 with h | h
      · exact Or.inl h
      · exact Or.inr (opn_of_endsV a Rp h)
    · exact locAllQ_of (q' :: ps) (hadd (run wasl a Rp)) q.R hR
        (fun u hu => hs u (List.mem_cons_of_mem _ hu)) hh.2 (by simpa using hlast)

/-! ## ٥. المبرهنتان -/

/-- **المودَعُ هو السطرُ والكلماتُ خامًا بعد «بَ»، وصلًا** — لكلّ سطرٍ كلُّ كلمةٍ بعد الأولى فيه من الأشكال:
أوّلُها حرٌّ أو حرفُ مدٍّ ساكنٌ يليه متحرّك، وإصلاحُها في الآخر وحدَه، وصورةُ ابتدائها هي أو مسبوقةٌ بحالٍ مفتوح؛
وأوّلُ المصلَحة أوّلُ الخام أو ما قبلها مختومٌ بمتحرّك. لا قيدَ على الطول. -/
theorem dep_shape (p1 : Pos) (ps : List Pos) (h1S : p1.S = p1.R) (h1ne : p1.R ≠ [])
    (h1 : RepairOf p1.W p1.R) (hs : ∀ q ∈ ps, PosShape q) (hh : HeadChain p1.R ps) :
    depB (p1 :: ps) = (waslB p1.W && lineB ((p1 :: ps).map Pos.R) &&
      ps.all fun p => joinB [k 'ب' .fath] p.W) := by
  rw [dep_sync p1 ps h1S (alive_of _ _ h1) h1ne (syncL_of ps hs)
    (fun q hq => alive_of _ _ (hs q hq).2.2.2.2.2.1) (fun q hq => (hs q hq).2.1),
    List.map_cons, lineB_lineSt, Bool.and_assoc,
    raw_local ps _ (fun q hq => (hs q hq).2.1) (locAll_of ps .bad' p1.R h1ne hs hh), ← Bool.and_assoc]

/-- **وآخرُ السطر وقف** (كما يُولَّد المودَع). -/
theorem dep_shape_waqf (p1 : Pos) (ps : List Pos) (hps : ps ≠ []) (h1S : p1.S = p1.R) (h1ne : p1.R ≠ [])
    (h1 : RepairOf p1.W p1.R) (hs : ∀ q ∈ ps, PosShape q) (hh : HeadChain p1.R ps)
    (hlast : (ps.getLast?.map fun p => p.R) = (ps.getLast?.map fun p => p.W)) :
    depBQ (p1 :: ps) = (waslB p1.W && lineWaqfB ((p1 :: ps).map Pos.R) && localQ ps) := by
  have hne : ∀ w ∈ p1.R :: ps.map Pos.R, w ≠ [] := by
    intro w hw
    rcases List.mem_cons.1 hw with rfl | hw
    · exact h1ne
    · obtain ⟨u, hu, rfl⟩ := List.mem_map.1 hw; exact (hs u hu).2.1
  rw [dep_sync_waqf p1 ps hps h1S (alive_of _ _ h1) h1ne (syncL_of ps hs)
    (fun q hq => alive_of _ _ (hs q hq).2.2.2.2.2.1)
    (fun q hq => ⟨(hs q hq).2.1, (hs q hq).1, (hs q hq).2.2.1⟩) hlast,
    List.map_cons, lineWaqfB_lineStQ _ _ hps hne, Bool.and_assoc,
    raw_local_waqf ps _ (fun q hq => (hs q hq).2.1) (locAllQ_of ps .bad' p1.R h1ne hs hh hlast),
    ← Bool.and_assoc]

end Harf
