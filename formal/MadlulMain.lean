import Madlul

/-! جدولُ بوّابة المدلول وحده (ADR ٩) على مودَعٍ صغيرٍ ثابت: كلُّ عقدةٍ من ثلاث، وكلُّ مرجعٍ من صفرٍ إلى ثلاثة
ألفاظٍ من ثلاثة (43 سطرًا)؛ يطابقه `tests/test_madlul.py` بمرآة `src/madlul.py`. -/

open Madlul

def d0 : Mawda Nat Nat Nat where
  naw
    | 0 => some (.kulli .jins, 20)
    | 1 => some (.juzi .damir, 21)
    | _ => none
  isti
    | [0] => some (.mustamal, 10)
    | [1] => some (.muhmal, 11)
    | [0, 1] => some (.mustamal, 12)
    | [1, 1] => some (.muhmal, 13)
    | [0, 1, 2] => some (.muhmal, 14)
    | _ => none

def nawStr : Naw → String
  | n => nawKey n

def istiStr : Isti → String
  | .mustamal => "mustamal"
  | .muhmal => "muhmal"

def wordsStr (ls : List Nat) : String := " ".intercalate (ls.map toString)

def refStr : Ref Nat Nat → String
  | .node n => s!"N:{n}"
  | .lafz ls => s!"L:{wordsStr ls}"

def rafdStr : Rafd → String
  | .emptyLafz => "EMPTY_LAFZ_REF"
  | .noNawWitness => "MAANA_WITHOUT_WITNESS"
  | .noIstiWitness => "ISTI_WITHOUT_WITNESS"

def outStr : Except Rafd (Madlul Nat Nat Nat) → String
  | .error e => s!"rafd:{rafdStr e}"
  | .ok (.maana n k w) => s!"maana:{n}:{nawStr k}:{w}"
  | .ok (.mufrad l i w) => s!"mufrad:{l}:{istiStr i}:{w}"
  | .ok (.murakkab a b r i w) => s!"murakkab:{wordsStr (a :: b :: r)}:{istiStr i}:{w}"

def qismStr : Except Rafd (Madlul Nat Nat Nat) → String
  | .error _ => "-"
  | .ok m => qismKey (qism m)

def lists : Nat → List (List Nat)
  | 0 => [[]]
  | k + 1 => (lists k).flatMap fun ls => [0, 1, 2].map fun x => ls ++ [x]

def refs : List (Ref Nat Nat) :=
  [0, 1, 2].map Ref.node ++ ([0, 1, 2, 3].flatMap lists).map Ref.lafz

def main : IO Unit := do
  for r in refs do
    let o := enter d0 r
    let back := match o with
      | .ok m => if exit m == r then "back" else "LOST"
      | .error _ => "-"
    IO.println s!"{refStr r}\t{outStr o}\t{qismStr o}\t{back}"
