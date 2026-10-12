import Harf

/-! جدولُ الثنائيّ `Harf.binB` على كلّ كلمةٍ من خانةٍ أو خانتين، وكلّ كلمةٍ من ثلاثٍ حواملُها من ء ا ب ل (17,668 سطرًا)؛ يطابقه
`tests/test_harf_binary.py` بـ`src/entry.py::licensed` (ADR ٤). -/

open Harf

def markOf : Haal → Char
  | .fath => 'َ'
  | .kasr => 'ِ'
  | .damm => 'ُ'
  | .sukun => 'ْ'

def atomStr (x : Khana) : String := s!"{charOf x.hamil}{markOf x.haal}"

def main : IO Unit := do
  for x in Khana.all do
    IO.println s!"{atomStr x},{binB [x]}"
  for x in Khana.all do
    for y in Khana.all do
      IO.println s!"{atomStr x} {atomStr y},{binB [x, y]}"
  let few := Khana.all.filter fun x => x.hamil = hamza ∨ x.hamil = alif ∨ x.hamil = hamilOf 'ب' ∨ x.hamil = lam
  for x in few do
    for y in few do
      for z in few do
        IO.println s!"{atomStr x} {atomStr y} {atomStr z},{binB [x, y, z]}"
