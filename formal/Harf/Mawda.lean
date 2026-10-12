import Harf.Azwaj

/-!
# المودَعُ والسطر: الزوجُ بصورة الابتداء يساوي السطرَ والكلماتِ خامًا (ADR ٦)

مودَعُ السياق في الغانم لا يقرن كلمتي السطر كما هما: يقرن كلَّ كلمةٍ **خامٍ** (`W`) بما قبلها **في صورة الابتداء**
(`S`: الكلمةُ نفسُها إن ابتدأت بمتحرّك، وإلّا متحرّكٌ قبلها — همزةُ الوصل)، بعد إصلاح آخرها على الحدّ (`R`). وهنا
يُبرهَن على آلة Algebra، لكلّ ثلاثيّاتٍ `(R، W، S)` بشروطٍ مسمّاة:

**`dep_eq`**: `depB ps = waslB W₁ && lineB [R₁ … Rₙ] && rawOK ps` — المودَعُ هو **السطرُ** (الكلماتُ مصلَحةً) **وكلُّ كلمةٍ
خامٍ مرخَّصةٌ بعد نواة** (`rawOK`) والكلمةُ الأولى وحدَها.

والسبب: بعد الحدّ وأوّلِ خانةٍ «حرّة» (متحرّكٍ، أو ساكنٍ ليس حرفَ مدّ) تنسى الآلةُ ما قبلها
(`after_hadd_free`)؛ وقراءةُ صورة الابتداء من أوّلها تصل إلى الحال نفسِه (`start_reads_same`، أو `lock` للمتحرّك)؛
وإصلاحُ الآخر لا يُميت كلمةً حيّة (`qabil_drop_last`، `qabil_kasr_last`).
-/

set_option autoImplicit false

namespace Harf

/-- أوّلُ الكلمة حرّ: متحرّكٌ أو ساكنٌ ليس حرفَ مدّ. -/
def freeFirst : List Khana → Bool
  | x :: _ => x.haal != .sukun || jins x.hamil == none
  | [] => false

def can (x : Khana) : Hal := if x.haal = .sukun then .qasir else .nawah x.haal

/-- حالُ الكلمة إن ابتدأت بعد حدٍّ بخانتها الحرّة. -/
def endC : List Khana → Hal
  | [] => .bad'
  | x :: t => run wasl (can x) t

theorem after_hadd_free : ∀ s ∈ Hal.all, s ≠ .bad' → ∀ x ∈ Khana.all,
    (x.haal != .sukun || jins x.hamil == none) = true →
    wasl (hadd s) x = .mayyit ∨ wasl (hadd s) x = can x := by decide +kernel

theorem start_reads_same : ∀ y ∈ Khana.all, y.haal ≠ .sukun → ∀ x ∈ Khana.all, x.haal = .sukun →
    jins x.hamil = none → wasl (wasl .bad' y) x = .qasir := by decide +kernel

theorem qabil_drop_last : ∀ s ∈ Hal.all, ∀ x ∈ Khana.all, x.haal = .sukun →
    qabilWasl (wasl s x) = true → qabilWasl s = true := by decide +kernel

theorem qabil_kasr_last : ∀ s ∈ Hal.all, ∀ x ∈ Khana.all, x.haal = .sukun →
    qabilWasl (wasl s x) = true → qabilWasl (wasl s ⟨x.hamil, .kasr⟩) = true := by decide +kernel

theorem endC_ne_bad' (v : List Khana) (h : v ≠ []) : endC v ≠ .bad' := by
  match v with
  | [] => exact absurd rfl h
  | [x] => simp only [endC, run, can]; split <;> simp
  | x :: y :: t => simp only [endC]; exact run_ne_bad'' _ (y :: t) (by simp)

theorem endC_of_startsV (v : List Khana) (h : startsV v = true) : endC v = endE v := by
  match v with
  | [] => simp [startsV] at h
  | x :: t =>
    have hx : x.haal ≠ .sukun := by simpa [startsV] using h
    simp [endC, endE, can, hx]

theorem freeFirst_cases (v : List Khana) (h : freeFirst v = true) :
    startsV v = true ∨ ∃ x t, v = x :: t ∧ x.haal = .sukun ∧ jins x.hamil = none := by
  match v with
  | [] => simp [freeFirst] at h
  | x :: t =>
    by_cases hx : x.haal = .sukun
    · right; refine ⟨x, t, rfl, hx, ?_⟩; simpa [freeFirst, hx] using h
    · left; simp [startsV, hx]

/-- بعد الحدّ: الكلمةُ الحرّةُ الأوّل تموت عند أوّلها أو تسير من حالها القانونيّ. -/
theorem run_after_hadd_free (s : Hal) (hs : s ≠ .bad') (v : List Khana) (hv : freeFirst v = true) :
    run wasl (hadd s) v = if ok s (v.headD ⟨0, .sukun⟩) then endC v else .mayyit := by
  match v with
  | [] => simp [freeFirst] at hv
  | x :: t =>
    simp only [run, endC, ok, List.headD]
    rcases after_hadd_free s (Hal.mem_all s) hs x (Khana.mem_all x) (by simpa [freeFirst] using hv)
      with h | h
    · simp [h, run_mayyit]
    · have hc : can x ≠ .mayyit := by unfold can; split <;> simp
      simp [h, hc]

/-- صورةُ الابتداء: الكلمةُ نفسُها إن ابتدأت بمتحرّك، وإلّا متحرّكٌ قبلها. -/
def StartForm (S R : List Khana) : Prop :=
  (startsV R = true → S = R) ∧ (startsV R = false → ∃ y, y.haal ≠ .sukun ∧ S = y :: R)

/-- قراءةُ صورة الابتداء من أوّلها تعطي الحدَّ نفسَه إن كانت الكلمةُ حيّةً بعد حدّ. -/
theorem ok_start (S R : List Khana) (hS : StartForm S R) (hR : freeFirst R = true)
    (hq : qabilWasl (endC R) = true) (x : Khana) : ok (run wasl .bad' S) x = ok (endC R) x := by
  rcases freeFirst_cases R hR with hv | ⟨x0, t, rfl, hx0, hj⟩
  · rw [hS.1 hv, endC_of_startsV R hv]
    rw [endC_of_startsV R hv] at hq
    exact ok_bad'_endE R hv x hq
  · have hsv : startsV (x0 :: t) = false := by simp [startsV, hx0]
    obtain ⟨y, hy, rfl⟩ := hS.2 hsv
    simp only [run, endC, can, hx0, ite_true]
    rw [start_reads_same y (Khana.mem_all y) hy x0 (Khana.mem_all x0) hx0 hj]

/-- الزوجُ: صورةُ الابتداء يسارًا والكلمةُ خامًا يمينًا. -/
theorem joinB_free (S W : List Khana) (hS : S ≠ []) (hW : freeFirst W = true) :
    joinB S W = (ok (run wasl .bad' S) (W.headD ⟨0, .sukun⟩) && qabilWasl (endC W)) := by
  simp only [joinB, lineB, runLine]
  rw [run_after_hadd_free _ (run_ne_bad'' _ S hS) W hW]
  cases ok (run wasl .bad' S) (W.headD ⟨0, .sukun⟩) <;> simp [qabilWasl]

/-! ## المودَع -/

/-- موضعٌ في السطر: الكلمةُ في السطر (مصلَحةَ الآخر) `R`، وخامًا `W`، وصورةُ ابتدائها `S`. -/
structure Pos where
  R : List Khana
  W : List Khana
  S : List Khana

/-- شروطُ موضعٍ بعد الأوّل: غيرُ فارغ، أوّلُه حرٌّ ومشتركٌ بين `R` و`W`، وصورةُ ابتدائه، وحياةُ الخام تُحيي المصلَح. -/
def PosOK (p : Pos) : Prop :=
  p.R ≠ [] ∧ p.W ≠ [] ∧ freeFirst p.R = true ∧ freeFirst p.W = true ∧
  p.R.headD ⟨0, .sukun⟩ = p.W.headD ⟨0, .sukun⟩ ∧ StartForm p.S p.R ∧
  (qabilWasl (endC p.W) = true → qabilWasl (endC p.R) = true)

def depT : List Khana → List Pos → Bool
  | _, [] => true
  | Sprev, p :: rest => joinB Sprev p.W && depT p.S rest

/-- المودَع: الكلمةُ الأولى وحدَها (ابتداءً)، وكلُّ كلمةٍ خامٍ مع صورة ابتداء ما قبلها. -/
def depB : List Pos → Bool
  | [] => true
  | p :: rest => waslB p.W && depT p.S rest

def rawOK (ps : List Pos) : Bool := ps.all fun p => qabilWasl (endC p.W)

/-- السطرُ بعد الحدّ من حال `s`. -/
def lineAfter (s : Hal) (rs : List (List Khana)) : Bool := qabilWasl (runLine wasl (hadd s) rs)

theorem lineAfter_cons (s : Hal) (hs : s ≠ .bad') (r : List Khana) (hr : freeFirst r = true)
    (rest : List (List Khana)) :
    lineAfter s (r :: rest) =
      (ok s (r.headD ⟨0, .sukun⟩) && match rest with
        | [] => qabilWasl (endC r)
        | _ :: _ => lineAfter (endC r) rest) := by
  unfold lineAfter
  cases rest with
  | nil =>
    simp only [runLine]
    rw [run_after_hadd_free s hs r hr]
    cases ok s (r.headD ⟨0, .sukun⟩) <;> simp [qabilWasl]
  | cons v rest =>
    simp only [runLine]
    rw [run_after_hadd_free s hs r hr]
    cases ok s (r.headD ⟨0, .sukun⟩)
    · simp [hadd_mayyit, runLine_mayyit, qabilWasl]
    · simp

theorem startForm_ne (S R : List Khana) (hS : StartForm S R) (hR : R ≠ []) : S ≠ [] := by
  cases hv : startsV R
  · obtain ⟨y, _, rfl⟩ := hS.2 hv; simp
  · rw [hS.1 hv]; exact hR

/-- ما بعد الأوّل: إن قرأت صورةُ ابتداء ما قبلُ كما يقرأ الحالُ `s` فالمودَعُ هو السطرُ من `s` والخام. -/
theorem low : ∀ (rest : List Pos) (s : Hal) (Sp : List Khana), s ≠ .bad' → Sp ≠ [] →
    (∀ x, ok (run wasl .bad' Sp) x = ok s x) → (∀ p ∈ rest, PosOK p) → rest ≠ [] →
    (rest.getLast?.map fun p => p.R) = (rest.getLast?.map fun p => p.W) →
    depT Sp rest = (lineAfter s (rest.map Pos.R) && rawOK rest)
  | [], _, _, _, _, _, _, h, _ => absurd rfl h
  | [p], s, Sp, hs, hSp, hok, hall, _, hlast => by
    obtain ⟨hR, _, hfR, hfW, hhead, _, _⟩ := hall p (by simp)
    simp only [List.getLast?_singleton, Option.map_some, Option.some.injEq] at hlast
    have e1 : depT Sp [p] = joinB Sp p.W := by simp [depT]
    rw [e1, List.map_cons, List.map_nil, lineAfter_cons s hs p.R hfR [], joinB_free Sp p.W hSp hfW,
      hok, hhead, hlast]
    simp [rawOK]
  | p :: q :: rest, s, Sp, hs, hSp, hok, hall, _, hlast => by
    obtain ⟨hR, _, hfR, hfW, hhead, hS, hRW⟩ := hall p (by simp)
    have e1 : depT Sp (p :: q :: rest) = (joinB Sp p.W && depT p.S (q :: rest)) := rfl
    have e2 : rawOK (p :: q :: rest) = (qabilWasl (endC p.W) && rawOK (q :: rest)) := rfl
    rw [e1, e2, List.map_cons, lineAfter_cons s hs p.R hfR _, joinB_free Sp p.W hSp hfW, hok, hhead]
    cases hqW : qabilWasl (endC p.W)
    · simp
    · have hqR := hRW hqW
      have ih := low (q :: rest) (endC p.R) p.S (endC_ne_bad' _ hR) (startForm_ne _ _ hS hR)
        (ok_start p.S p.R hS hfR hqR) (fun u hu => hall u (by simp [hu])) (by simp)
        (by simpa using hlast)
      rw [ih]
      simp only [List.map_cons, Bool.true_and, Bool.and_true, Bool.and_assoc]

/-- **المودَعُ هو السطرُ والكلماتُ خامًا**: لكلّ سطرٍ كلُّ موضعٍ بعد الأوّل بشروطه، وآخرُه بلا إصلاح. -/
theorem dep_eq (p1 : Pos) (rest : List Pos) (h1R : p1.R ≠ []) (h1S : p1.S = p1.R)
    (hall : ∀ p ∈ rest, PosOK p)
    (hlast : ((p1 :: rest).getLast?.map fun p => p.R) = ((p1 :: rest).getLast?.map fun p => p.W)) :
    depB (p1 :: rest) = (waslB p1.W && lineB ((p1 :: rest).map Pos.R) && rawOK rest) := by
  cases rest with
  | nil =>
    simp only [List.getLast?_singleton, Option.map_some, Option.some.injEq] at hlast
    simp [depB, depT, lineB, runLine, rawOK, waslB, hlast]
  | cons p rest =>
    have e1 : depB (p1 :: p :: rest) = (waslB p1.W && depT p1.S (p :: rest)) := rfl
    have e2 : lineB ((p1 :: p :: rest).map Pos.R) =
        lineAfter (run wasl .bad' p1.R) ((p :: rest).map Pos.R) := by
      simp only [List.map_cons, lineB, runLine, lineAfter]
    rw [e1, e2, h1S, low (p :: rest) (run wasl .bad' p1.R) p1.R (run_ne_bad'' _ _ h1R) h1R
      (fun _ => rfl) hall (by simp) (by simpa using hlast)]
    simp only [Bool.and_assoc]

/-! ## إصلاحُ الآخر لا يُميت كلمةً حيّة، وحياةُ الخام هي ترخيصُ صورة ابتدائه -/

theorem run_snoc (f : Hal → Khana → Hal) : ∀ (a : Hal) (l : List Khana) (x : Khana),
    run f a (l ++ [x]) = f (run f a l) x
  | _, [], _ => rfl
  | a, y :: t, x => run_snoc f (f a y) t x

theorem endC_snoc (l : List Khana) (hl : l ≠ []) (x : Khana) : endC (l ++ [x]) = wasl (endC l) x := by
  match l with
  | [] => exact absurd rfl hl
  | y :: t => simp only [List.cons_append, endC]; exact run_snoc wasl _ t x

theorem alive_drop (l : List Khana) (hl : l ≠ []) (x : Khana) (hx : x.haal = .sukun)
    (h : qabilWasl (endC (l ++ [x])) = true) : qabilWasl (endC l) = true := by
  rw [endC_snoc l hl] at h
  exact qabil_drop_last _ (Hal.mem_all _) x (Khana.mem_all x) hx h

theorem alive_kasr (l : List Khana) (hl : l ≠ []) (x : Khana) (hx : x.haal = .sukun)
    (h : qabilWasl (endC (l ++ [x])) = true) : qabilWasl (endC (l ++ [⟨x.hamil, .kasr⟩])) = true := by
  rw [endC_snoc l hl] at h ⊢
  exact qabil_kasr_last _ (Hal.mem_all _) x (Khana.mem_all x) hx h

/-- بعد «بَ» كلُّ خانةٍ حرّةٍ مقبولة: المقطعُ المفتوحُ القصير محايدُ ما قبل الحدّ. -/
theorem ok_ba : ∀ x ∈ Khana.all, (x.haal != .sukun || jins x.hamil == none) = true →
    ok (run wasl .bad' [k 'ب' .fath]) x = true := by decide +kernel

/-- **حياةُ الكلمة الخام بعد حدٍّ هي ترخيصُها موصولةً بعد «بَ»**. -/
theorem raw_eq_ba (W : List Khana) (hW : freeFirst W = true) :
    qabilWasl (endC W) = joinB [k 'ب' .fath] W := by
  rw [joinB_free _ _ (by simp) hW]
  match W, hW with
  | x :: _, hW => rw [List.headD_cons, ok_ba x (Khana.mem_all x) (by simpa [freeFirst] using hW)]; simp

/-! ## الوقف: آخرُ السطر وقفٌ وما قبله وصل -/

/-- السطرُ وصلًا إلّا آخرَه وقفًا. -/
def runMix : Hal → List (List Khana) → Hal
  | a, [] => a
  | a, [w] => run waqf a w
  | a, w :: v :: rest => runMix (hadd (run wasl a w)) (v :: rest)

theorem hadd_doom : ∀ a ∈ Hal.all, qabilWasl a = false → hadd a = .mayyit ∨ hadd a = .khatm := by
  decide +kernel

theorem doom_step : ∀ x ∈ Khana.all,
    wasl .khatm x = .mayyit ∧ waqf .khatm x = .mayyit ∧ waqf .mayyit x = .mayyit := by decide +kernel

theorem waqf_dead_step : ∀ a ∈ Hal.all, ∀ x ∈ Khana.all, wasl a x = .mayyit →
    waqf a x = .mayyit ∨ (waqf a x = .khatm ∧ x.haal = .sukun) := by decide +kernel

theorem run_waqf_mayyit : ∀ t : List Khana, run waqf .mayyit t = .mayyit
  | [] => rfl
  | x :: t => by
    simp only [run]; rw [(doom_step x (Khana.mem_all x)).2.2]; exact run_waqf_mayyit t

theorem run_waqf_khatm (t : List Khana) (ht : t ≠ []) : run waqf .khatm t = .mayyit := by
  match t with
  | [] => exact absurd rfl ht
  | x :: t => simp only [run]; rw [(doom_step x (Khana.mem_all x)).2.1]; exact run_waqf_mayyit t

theorem runLine_waqf_mayyit : ∀ ws : List (List Khana), runLine waqf .mayyit ws = .mayyit
  | [] => rfl
  | [w] => run_waqf_mayyit w
  | w :: v :: rest => by
    simp only [runLine]; rw [run_waqf_mayyit, hadd_mayyit]; exact runLine_waqf_mayyit (v :: rest)

theorem runMix_mayyit : ∀ ws : List (List Khana), runMix .mayyit ws = .mayyit
  | [] => rfl
  | [w] => run_waqf_mayyit w
  | w :: v :: rest => by
    simp only [runMix]; rw [run_mayyit, hadd_mayyit]; exact runMix_mayyit (v :: rest)

/-- ما مات وصلًا لا يحيا وقفًا داخلَ السطر: يموت أو يُختم. -/
theorem run_waqf_doom : ∀ (a : Hal) (w : List Khana),
    qabilWasl (run wasl a w) = false → qabilWasl (run waqf a w) = false
  | _, [], h => h
  | a, x :: t, h => by
    simp only [run] at h ⊢
    by_cases hm : wasl a x = .mayyit
    · rcases waqf_dead_step a (Hal.mem_all a) x (Khana.mem_all x) hm with h1 | ⟨h1, _⟩
      · rw [h1, run_waqf_mayyit]; rfl
      · rw [h1]
        cases t with
        | nil => rfl
        | cons y t => rw [run_waqf_khatm _ (by simp)]; rfl
    · rw [wasl_waqf_step a (Hal.mem_all a) x (Khana.mem_all x) hm]
      exact run_waqf_doom _ t h

theorem doom_line (b : Hal) (hb : b = .mayyit ∨ b = .khatm) (v : List Khana) (hv : v ≠ [])
    (rest : List (List Khana)) :
    runLine waqf b (v :: rest) = .mayyit ∧ runMix b (v :: rest) = .mayyit := by
  match v with
  | [] => exact absurd rfl hv
  | x :: t =>
    have hw : waqf b x = .mayyit := by
      rcases hb with rfl | rfl
      · exact (doom_step x (Khana.mem_all x)).2.2
      · exact (doom_step x (Khana.mem_all x)).2.1
    have hl : wasl b x = .mayyit := by
      rcases hb with rfl | rfl
      · rfl
      · exact (doom_step x (Khana.mem_all x)).1
    have e1 : run waqf b (x :: t) = .mayyit := by simp only [run]; rw [hw, run_waqf_mayyit]
    have e2 : run wasl b (x :: t) = .mayyit := by simp only [run]; rw [hl, run_mayyit]
    cases rest with
    | nil => exact ⟨e1, e1⟩
    | cons u r =>
      simp only [runLine, runMix]
      rw [e1, e2, hadd_mayyit]
      exact ⟨runLine_waqf_mayyit _, runMix_mayyit _⟩

/-- **السطرُ وقفًا هو السطرُ وصلًا وآخرُه وقفًا** (لكلّ سطرٍ كلماتُه غيرُ فارغة). -/
theorem line_mix : ∀ (ws : List (List Khana)) (a : Hal), (∀ w ∈ ws, w ≠ []) →
    qabilWaqf (runLine waqf a ws) = qabilWaqf (runMix a ws)
  | [], _, _ => rfl
  | [_], _, _ => rfl
  | w :: v :: rest, a, hne => by
    simp only [runLine, runMix]
    cases hq : qabilWasl (run wasl a w)
    · have hv : v ≠ [] := hne v (by simp)
      obtain ⟨h1, _⟩ := doom_line _ (hadd_doom _ (Hal.mem_all _) (run_waqf_doom a w hq)) v hv rest
      obtain ⟨_, h2⟩ := doom_line _ (hadd_doom _ (Hal.mem_all _) hq) v hv rest
      rw [h1, h2]
    · rw [run_wasl_waqf a w hq]
      exact line_mix (v :: rest) _ (fun u hu => hne u (by simp_all))

/-- حالُ الكلمة الأخيرة بعد حدٍّ بخانتها الحرّة، وقفًا. -/
def endCQ : List Khana → Hal
  | [] => .bad'
  | x :: t => run waqf (can x) t

/-- الساكنُ وحدَه لا يكون كلمة: إن ابتدأت بساكنٍ فلها ما بعده. -/
def sukunTail : List Khana → Bool
  | x :: t => x.haal != .sukun || !t.isEmpty
  | [] => false

theorem run_after_hadd_free_waqf (s : Hal) (hs : s ≠ .bad') (v : List Khana) (hv : freeFirst v = true)
    (ht : sukunTail v = true) :
    qabilWaqf (run waqf (hadd s) v) = (ok s (v.headD ⟨0, .sukun⟩) && qabilWaqf (endCQ v)) := by
  match v with
  | [] => simp [freeFirst] at hv
  | x :: t =>
    simp only [run, endCQ, ok, List.headD]
    by_cases hm : wasl (hadd s) x = .mayyit
    · rw [hm]
      rcases waqf_dead_step _ (Hal.mem_all _) x (Khana.mem_all x) hm with h1 | ⟨h1, hx⟩
      · rw [h1, run_waqf_mayyit]; rfl
      · have : t ≠ [] := by
          intro he; subst he; simp [sukunTail, hx] at ht
        rw [h1, run_waqf_khatm t this]; rfl
    · rw [wasl_waqf_step _ (Hal.mem_all _) x (Khana.mem_all x) hm]
      rcases after_hadd_free s (Hal.mem_all s) hs x (Khana.mem_all x) (by simpa [freeFirst] using hv)
        with h | h
      · exact absurd h hm
      · rw [h]
        have hc : can x ≠ .mayyit := by unfold can; split <;> simp
        simp [hc]

/-- الزوجُ الأخيرُ وقفًا: صورةُ ابتداء ما قبلها والكلمةُ خامًا. -/
theorem joinWaqfB_free (S W : List Khana) (hS : S ≠ []) (hW : freeFirst W = true) (ht : sukunTail W = true) :
    joinWaqfB S W = (ok (run wasl .bad' S) (W.headD ⟨0, .sukun⟩) && qabilWaqf (endCQ W)) := by
  rw [joinWaqfB, lineWaqfB, line_mix [S, W] .bad' (by
    intro w hw; simp only [List.mem_cons, List.not_mem_nil, or_false] at hw
    rcases hw with rfl | rfl
    · exact hS
    · intro he; subst he; simp [freeFirst] at hW)]
  exact run_after_hadd_free_waqf _ (run_ne_bad'' _ S hS) W hW ht

theorem raw_eq_ba_waqf (W : List Khana) (hW : freeFirst W = true) (ht : sukunTail W = true) :
    qabilWaqf (endCQ W) = joinWaqfB [k 'ب' .fath] W := by
  rw [joinWaqfB_free _ _ (by simp) hW ht]
  match W, hW with
  | x :: _, hW => rw [List.headD_cons, ok_ba x (Khana.mem_all x) (by simpa [freeFirst] using hW)]; simp

def depTQ : List Khana → List Pos → Bool
  | _, [] => true
  | Sprev, [p] => joinWaqfB Sprev p.W
  | Sprev, p :: q :: rest => joinB Sprev p.W && depTQ p.S (q :: rest)

/-- المودَعُ وقفًا آخرَ السطر: الأولى وحدَها (ابتداءً، ووقفًا إن كانت وحدَها). -/
def depBQ : List Pos → Bool
  | [] => true
  | [p] => waqfB p.W
  | p :: q :: rest => waslB p.W && depTQ p.S (q :: rest)

def rawQ : List Pos → Bool
  | [] => true
  | [p] => qabilWaqf (endCQ p.W)
  | p :: q :: rest => qabilWasl (endC p.W) && rawQ (q :: rest)

def lineAfterQ (s : Hal) (rs : List (List Khana)) : Bool := qabilWaqf (runMix (hadd s) rs)

theorem lineAfterQ_one (s : Hal) (hs : s ≠ .bad') (r : List Khana) (hr : freeFirst r = true)
    (ht : sukunTail r = true) :
    lineAfterQ s [r] = (ok s (r.headD ⟨0, .sukun⟩) && qabilWaqf (endCQ r)) :=
  run_after_hadd_free_waqf s hs r hr ht

theorem lineAfterQ_cons (s : Hal) (hs : s ≠ .bad') (r : List Khana) (hr : freeFirst r = true)
    (v : List Khana) (rest : List (List Khana)) :
    lineAfterQ s (r :: v :: rest) = (ok s (r.headD ⟨0, .sukun⟩) && lineAfterQ (endC r) (v :: rest)) := by
  unfold lineAfterQ
  simp only [runMix]
  rw [run_after_hadd_free s hs r hr]
  cases ok s (r.headD ⟨0, .sukun⟩)
  · simp [hadd_mayyit, runMix_mayyit, qabilWaqf]
  · simp

theorem lowQ : ∀ (rest : List Pos) (s : Hal) (Sp : List Khana), s ≠ .bad' → Sp ≠ [] →
    (∀ x, ok (run wasl .bad' Sp) x = ok s x) → (∀ p ∈ rest, PosOK p) →
    (∀ p ∈ rest, sukunTail p.W = true) → rest ≠ [] →
    (rest.getLast?.map fun p => p.R) = (rest.getLast?.map fun p => p.W) →
    depTQ Sp rest = (lineAfterQ s (rest.map Pos.R) && rawQ rest)
  | [], _, _, _, _, _, _, _, h, _ => absurd rfl h
  | [p], s, Sp, hs, hSp, hok, hall, htl, _, hlast => by
    obtain ⟨_, _, _, hfW, _, _, _⟩ := hall p (by simp)
    simp only [List.getLast?_singleton, Option.map_some, Option.some.injEq] at hlast
    have ht := htl p (by simp)
    simp only [depTQ, List.map_cons, List.map_nil, rawQ]
    rw [hlast, lineAfterQ_one s hs p.W hfW ht, joinWaqfB_free Sp p.W hSp hfW ht, hok]
    simp
  | p :: q :: rest, s, Sp, hs, hSp, hok, hall, htl, _, hlast => by
    obtain ⟨hR, _, hfR, hfW, hhead, hS, hRW⟩ := hall p (by simp)
    have e1 : depTQ Sp (p :: q :: rest) = (joinB Sp p.W && depTQ p.S (q :: rest)) := rfl
    have e2 : rawQ (p :: q :: rest) = (qabilWasl (endC p.W) && rawQ (q :: rest)) := rfl
    rw [e1, e2, List.map_cons, List.map_cons, lineAfterQ_cons s hs p.R hfR, joinB_free Sp p.W hSp hfW,
      hok, hhead]
    cases hqW : qabilWasl (endC p.W)
    · simp
    · have hqR := hRW hqW
      have ih := lowQ (q :: rest) (endC p.R) p.S (endC_ne_bad' _ hR) (startForm_ne _ _ hS hR)
        (ok_start p.S p.R hS hfR hqR) (fun u hu => hall u (by simp [hu]))
        (fun u hu => htl u (by simp [hu])) (by simp) (by simpa using hlast)
      rw [← List.map_cons, ih]
      simp only [Bool.true_and, Bool.and_true, Bool.and_assoc]

/-- **المودَعُ وقفًا هو السطرُ وقفًا والكلماتُ خامًا** (سطرٌ من كلمتين فأكثر). -/
theorem dep_eq_waqf (p1 p : Pos) (rest : List Pos) (h1R : p1.R ≠ []) (h1S : p1.S = p1.R)
    (hall : ∀ q ∈ p :: rest, PosOK q) (htl : ∀ q ∈ p :: rest, sukunTail q.W = true)
    (hlast : ((p :: rest).getLast?.map fun q => q.R) = ((p :: rest).getLast?.map fun q => q.W)) :
    depBQ (p1 :: p :: rest) = (waslB p1.W && lineWaqfB ((p1 :: p :: rest).map Pos.R) && rawQ (p :: rest)) := by
  have e1 : depBQ (p1 :: p :: rest) = (waslB p1.W && depTQ p1.S (p :: rest)) := rfl
  have hne : ∀ w ∈ (p1 :: p :: rest).map Pos.R, w ≠ [] := by
    intro w hw
    simp only [List.map_cons, List.mem_cons, List.mem_map] at hw
    rcases hw with rfl | rfl | ⟨q, hq, rfl⟩
    · exact h1R
    · exact (hall p (by simp)).1
    · exact (hall q (by simp [hq])).1
  have e2 : lineWaqfB ((p1 :: p :: rest).map Pos.R) =
      lineAfterQ (run wasl .bad' p1.R) ((p :: rest).map Pos.R) := by
    rw [lineWaqfB, line_mix _ _ hne]
    simp only [List.map_cons, runMix, lineAfterQ]
  rw [e1, e2, h1S, lowQ (p :: rest) (run wasl .bad' p1.R) p1.R (run_ne_bad'' _ _ h1R) h1R
    (fun _ => rfl) hall htl (by simp) hlast]
  simp only [Bool.and_assoc]

/-- والكلمةُ وحدَها في السطر: ابتداءٌ ووقف. -/
theorem dep_eq_waqf_one (p1 : Pos) : depBQ [p1] = waqfB p1.W := rfl

/-! ## الشاهدان -/

def biM : List Khana := [k 'ب' .kasr]
def qaalSakin : List Khana := [k 'ق' .fath, k 'ا' .sukun, k 'ل' .sukun]
def qaalKasr : List Khana := [k 'ق' .fath, k 'ا' .sukun, k 'ل' .kasr]

/-- بِ قَالْ الْحَمْدُ: في السطر «قَالِ» (الساكنُ يُكسَر)، وفي المودَع «قَالْ» خامًا. -/
def biQaalHamd : List Pos :=
  [⟨biM, biM, biM⟩, ⟨qaalKasr, qaalSakin, qaalKasr⟩, ⟨lhamdu, lhamdu, k 'ا' .kasr :: lhamdu⟩]

/-- **`rawOK` لازم**: السطرُ المصلَحُ مرخَّصٌ والمودَعُ يرفض، لأنّ «قَالْ» خامًا قافيةُ مدٍّ مغلقة. -/
theorem rawOK_needed :
    depB biQaalHamd = false ∧ (waslB biM && lineB (biQaalHamd.map Pos.R)) = true ∧
    rawOK biQaalHamd.tail = false := by decide

theorem biQaalHamd_posOK : ∀ p ∈ biQaalHamd.tail, PosOK p := by
  simp only [biQaalHamd, List.tail_cons, List.mem_cons, List.not_mem_nil, or_false]
  rintro p (rfl | rfl) <;> refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    first | decide | (constructor <;> intro h <;> first | rfl | (exact absurd h (by decide)) | exact ⟨k 'ا' .kasr, by decide, rfl⟩)

/-- **أوّلٌ حرٌّ لازمٌ للصيغة**: كلمةٌ أوّلُها حرفُ مدٍّ ساكن (اْلْ بعد ءَ) تُفسد `endC` فتفترق الصيغةُ عن المودَع. -/
theorem freeFirst_needed :
    freeFirst [k 'ا' .sukun, k 'ل' .sukun] = false ∧
    depB [⟨[k 'ء' .fath], [k 'ء' .fath], [k 'ء' .fath]⟩,
          ⟨[k 'ا' .sukun, k 'ل' .sukun], [k 'ا' .sukun, k 'ل' .sukun], [k 'ا' .sukun, k 'ل' .sukun]⟩] ≠
      (waslB [k 'ء' .fath] && lineB [[k 'ء' .fath], [k 'ا' .sukun, k 'ل' .sukun]] &&
        rawOK [⟨[k 'ا' .sukun, k 'ل' .sukun], [k 'ا' .sukun, k 'ل' .sukun], [k 'ا' .sukun, k 'ل' .sukun]⟩]) := by
  decide

end Harf
