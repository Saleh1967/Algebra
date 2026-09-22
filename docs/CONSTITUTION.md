# Alghanem Kernel Constitution

These are the initial laws of the language-agnostic kernel:

| Law | Status | Kernel v0.1 scope |
| --- | --- | --- |
| Explicit domain | ENFORCED | Anchors require a non-blank domain. When an operation declares a source domain, it must match the source anchor's domain. When an operation declares a target domain, it must match the target anchor's domain. |
| Explicit target anchor | ENFORCED | No successful transition without an explicitly declared target anchor; a default derived from the source anchor never satisfies admission. Identity-preserving transformations require source anchor = target anchor. Branch-birth claims require source anchor != target anchor, and branch provenance must bind the actual source and target anchors. |
| Evidence present | ENFORCED | Successful transitions require at least one evidence record. |
| Evidence-to-claim binding | ENFORCED | Successful-transition evidence is structurally bound by claim id to the transition's own claim. This is not proof sufficiency. |
| G0.C.1 minimal claim constitution | ENFORCED_AT_CONTENT_ENCODER | See **G0.C.1 — Minimal claim constitution** below. |
| Structural admission boundary | ENFORCED | Candidates become `StructurallyAdmissibleTransition`s only through `StructuralAdmissionGate`. The gate is a controlled construction boundary inside the Python API, not a cryptographic or security-grade mechanism, and it certifies structural completeness only — not evidential sufficiency, domain-transition authority, or layer authority. Structural admission must not be conflated with a future `LicensedTransition`: `Representability != Licensability` and `StructuralValidity != EvidentialSufficiency`. |
| Claimed kind vs. certified outcome | ENFORCED | Every candidate declares what it represents via `TransitionKind` (`IDENTITY_PRESERVATION_CLAIM` or `BRANCH_BIRTH_CLAIM`). Candidates do not carry certified outcomes or decision statuses (`Candidate != Decision`); a candidate cannot decide or certify its own outcome. `StructuralAdmissionGate` evaluates the candidate and yields a `StructuralAdmissionDecision` with a status (`ADMITTED`, `BLOCK`, `DEFER`, `UNDEFINED`). `CertifiedOutcome` (`IDENTITY_PRESERVING_TRANSFORMATION`, `CERTIFIED_BRANCH_BIRTH`) is strictly reserved for the final certification stage (`CertifiedTransition`), not asserted by structural admission alone. In particular, `target_anchor == anchor` is a structural check, not proof: `AnchorEquality != ProvenIdentityPreservation`. Declaring a name in `preserved`/`changed` is not proof it was extracted from `before_state`/`after_state`: `DeclaredInvariant != VerifiedInvariant`. |
| Declared invariant presence | ENFORCED | Identity-preserving transformations require a declared invariant. |
| Verified invariant preservation | ENFORCED_AT_INVARIANT_GATE | Structural admission issues an opaque `admission_id`; verification provenance binds that exact transition identity and the sealed registry's `registry_snapshot_id`, in addition to claim, anchors, and trace. `InvariantVerificationGate.assess_all_preserved` and `InvariantVerificationBundle` require exactly one successful verification for every declared preserved component; both `InvariantVerificationDecision` and `InvariantVerificationBundle` are gate-issued only, mirroring each other (`VerificationDecision must be gate-issued`, and `InvariantVerificationBundle` now enforces this with its own private token), so a caller cannot hand-build a `VERIFIED` decision or a bundle, and a later layer that trusts either cannot be fooled by a self-declared result. An `InvariantSpec`'s `extractor_id` is only a claim, never a grant of authority: `InvariantExtractorRegistry.authorize` binds a trusted, registry-owned `RegisteredInvariantDefinition` (`domain`, `component`, `invariant_id` -> exactly one `extractor_id`), and `InvariantVerificationGate.verify` resolves only through `SealedInvariantExtractorRegistry.resolve_authorized`, which raises `UnauthorizedExtractorError` unless that exact extractor id is authorized for that exact scope (`Candidate/Caller does not own verifier selection authority`). `DEFER` is a real, distinct status: epistemic non-answers (unregistered or unauthorized extractor, failing extractor, ambiguous non-`bool` comparison) are `DEFER`, a disproved invariant is `BLOCK`, and internal/programming errors are caught into neither -- they propagate. `assess_all_preserved` evaluates every declared component independently rather than stopping at the first untestable one, and aggregates with strict precedence `BLOCK` (any disproved component) > `DEFER` (else, any untestable component) > `VERIFIED`, recording disproved (`failed_components`) and untestable (`deferred_components`) components as separate, sorted sets so the aggregate judgment never depends on the order components were declared in (`Known falsification dominates epistemic deferral`). Failures remain in an auditable `InvariantVerificationDecision`, and the convenience API raises a typed error carrying that decision. Registration authority, authorization authority, and snapshot resolution authority are three distinct concerns, but none of them is an evidential authority license. `StructurallyAdmissibleTransition.transition_projection_fingerprint` and `SealedInvariantExtractorRegistry.registry_projection_hash` are corroborating, deterministic *projections* of part of the transition/registry content, recorded alongside the opaque `admission_id`/`registry_snapshot_id` (`OccurrenceIdentity != ContentIdentity` for both transitions and registries) -- they are explicitly **not** canonical content identity or reproducibility proofs (each omits significant structurally-relevant content; see their docstrings), and must not be used to promote epistemic status. A full `CanonicalTransitionManifest`/`ExtractorRegistration` content-identity and reproducibility design is deferred to a dedicated follow-up. Verification is not yet wired into `StructuralAdmissionGate` or evidential sufficiency; `No epistemic promotion` remains `DECLARED_DEFERRED`. |
| Preserved/changed separation | ENFORCED | Preserved and changed components are non-blank, unique, and disjoint. |
| Declared change | ENFORCED | Every successful transition has a result and a changed component matching the operation's declared change. |
| Branch birth separation | ENFORCED | A branch-birth claim is distinct from identity preservation and requires origin provenance whose preserved components exactly equal its declared preserved components, plus a distinct branch anchor equal to the target anchor. |
| Non-admitted decisions | ENFORCED | `BLOCK`, `DEFER`, and `UNDEFINED` are external decision statuses (`StructuralDecisionStatus`), never properties of a candidate or `StructurallyAdmissibleTransition`s. |
| Non-success audit | ENFORCED | No non-success decision without reviewable audit information. Every non-success decision preserves its trace, its residuals, and a non-blank structural reason; the assessed candidate is preserved when one exists, and the audit's trace and residuals are then bound to that candidate's own history — no history without provenance from the assessed attempt. Without a candidate, the audit owns its trace and residuals directly. Non-success decision histories must not be erased: `require_admitted` raises `StructuralAdmissionError`, which carries the complete non-admitted decision. An optional `DecisionReasonCode` provides a coarse-grained, machine-auditable classification alongside the human-readable `reason`; it does not replace `reason` or carry additional structural authority. |
| Residual presence | PARTIALLY_ENFORCED | Residual records cannot be blank when present and are preserved in non-success audits, but residual provenance is not defined and residuals are not interpreted or ranked. |
| No epistemic promotion | DECLARED_DEFERRED | Claim/evidence binding is structural only; evidential sufficiency is not implemented. |
| No partial invariant coverage | DECLARED_DEFERRED | No transition may be promoted as preserved from partial invariant coverage; complete invariant verification is available as a separate gate before evidential sufficiency. |
| No higher-layer repair | DECLARED_DEFERRED | Higher layers may not repair invalid lower-layer transitions, but layer authority is not defined. |
| Canonical transition content snapshot | ENFORCED_AT_CONTENT_ENCODER | `CanonicalTransitionEncoder` is the sole issuer of `CanonicalTransitionManifest` and `TransitionContentIdentity`. The manifest preserves immutable canonical bytes for every structural transition field, including branch-origin provenance; occurrence-only `admission_id` and projection fingerprint are explicit exclusions. Its SHA-256 value is a digest reference, not proof of canonical-byte equality. Canonical values accept only exact built-in types, distinguish list from tuple and bytes from bytearray, preserve raw Unicode code points without normalization, encode finite floats as IEEE-754 binary64, and reject unsupported values and cycles. `preserved`, `changed`, and branch provenance components are sets; trace, evidence, and residuals are ordered sequences. Schema coverage rejects unaccounted structural fields. |
| G0.RC.1 certified residual constitution | DECLARED_DEFERRED_CONTRACT_ONLY | `ResidualCertificationCandidate` accepts one existing `BirthAssessmentContentBinding`, not independent definition and content-id values. Its residual definition and content identity are derived from the binding, which verifies byte-exact equality against the sealed registry and frozen pre-evidence experiment. It is not an authority-issued certification: `FrozenFactorRef`/`BornBridgeRef` remain caller-constructible contract references until G0.FA.1, and reconstruction-attempt and comparison authorities are absent. `ResidualDefinitionSpec != ObservedDifference != CertifiedResidual != LegacyResidual` remains a declared distinction only. G0.RC.1 must not be marked enforced until those authorities exist. Residual typing and structural expansion remain deferred to G0.RT.1 and G0.SE.1. |
| G0.FA.1 authority-issued frozen reference | DECLARED_DEFERRED | `FrozenFactorRef` and `BornBridgeRef` validate reference shape and exact membership, but successful construction does not prove that a factor was frozen. A future freeze authority must issue trusted references before residual certification can claim `Freeze(F) -> Residual(F, observation)`. |
| G0.BV.1 authority-issued birth verdict | DECLARED_DEFERRED_CONTRACT_ONLY | `BirthVerdictStatus` remains future vocabulary only. No runtime authority may convert caller-declared assessment status into a verdict. A future assessment authority must first execute authorized evaluators and preserve the `BirthCandidate`/`IndependentClosure` boundary before a verdict authority can issue `BIRTH_IN_SCOPE`, `NO_BIRTH_IN_SCOPE`, or `DEFER_IN_SCOPE`; Freeze and residual certification remain separate later authorities. `BIRTH_IN_SCOPE` and `NO_BIRTH_IN_SCOPE` therefore remain unreachable at runtime; only the deferral branch is now executable, under G0.BV.1a below. |
| G0.BV.1a gate-derived scoped deferral | ENFORCED_AT_VERDICT_GATE | The first executable authority boundary for a `BirthVerdictStatus`, copying the register -> seal -> gate shape already enforced by `EvidenceAcquisitionAuthority`, `InvariantVerificationGate`/`SealedInvariantExtractorRegistry`, and `BirthEvaluatorExecutionGate`. `BirthVerdictScopeRegistry.register` is the sole issuer of an `AuthorizedBirthVerdictScope` and requires a verified `BirthExperimentSpecificationContentBinding`; every scope condition (`experiment_content_id`, `domain`, `experiment_id`, `revision_id`, `revision_sequence`, `evidence_mode`, `test_model`) is derived from that binding, never independently caller-supplied. Only `BirthVerdictScopeRegistry.seal` produces a `SealedBirthVerdictScopeRegistry`, and only `BirthVerdictGate.assess` produces a `BirthVerdictDecision`, which is not caller-constructible. `CallerDoesNotOwnVerdictAuthority` is enforced by the signature, not only by prose: `assess` accepts no status, reason, or closure claim, and derives the status from the request's own frozen projection poset. `DeferredVerdict != Birth`: the gate's codomain is currently the single value `DEFER_IN_SCOPE`, because `BIRTH_IN_SCOPE`/`NO_BIRTH_IN_SCOPE` require a gate-issued `IndependentClosureDecision` that no authority here can issue; the recorded reason distinguishes which obstacle applied (unresolved incomparable competitors, an open prerequisite cone, or the missing closure authority). This stage issues no `Freeze`, no `E0` mapping, and no `TraditionalName`; a `DEFER_IN_SCOPE` decision may not be frozen. `AuthorizedScope != AssessedEvidence`: no evaluator is executed, no residual measured, and no weaker model exhausted here. |
| G0.IC.1a gate-derived comparability closure | ENFORCED_AT_CLOSURE_GATE | Closes exactly one conjunct of the `IndependentClosure` that G0.BV.1a declared missing, and refuses the rest. The same register -> seal -> gate shape applies: `ClosureScopeRegistry.register` is the sole issuer of an `AuthorizedClosureScope` (every condition derived from a verified `BirthExperimentSpecificationContentBinding`), `ClosureScopeRegistry.seal` alone produces a `SealedClosureScopeRegistry`, and `IndependentClosureGate.assess` alone produces an `IndependentClosureAssessment`. `CallerDoesNotOwnClosureAuthority`: `assess` accepts no status, reason, or comparability claim, and reads exactly one thing -- the request's own frozen `ProjectionPoset`. Because comparability over a finite frozen projection set is exhaustively decidable, this status is genuinely two-valued and both `COMPETITION_RESOLVED_IN_POSET` and `COMPETITION_UNRESOLVED_IN_POSET` are reachable. `AbsentRelation != DeclaredIncomparability`: a frozen poset cannot distinguish a declared incomparability from a relation never determined, so both are counted as unresolved competition and `COMPETITION_RESOLVED_IN_POSET` is reachable only when every other projection is strictly related to the test model; ignorance is never read as resolution. `ComparabilityClosure != IndependentClosure` is the boundary this stage does not cross: `NoRicherStructureBeforeLowerOpenResidualClosure` makes an empty competitor set only one conjunct, and the others -- a residual surviving under `NoBirthWithoutResidualOrFormalNecessity` and an exhausted licensed weaker model set under `NoBirthBeforeLicensedWeakerExhaustion` -- have no authority here and cannot be obtained by copying any existing pattern, because both require evaluating evidence content that `G0.BA.1a` explicitly does not evaluate (`InputProvenance = DECLARED_DEFERRED`). `IndependentClosureAssessment.is_independent_closure` is therefore `False` unconditionally, even on the resolved branch. `ComparabilityAssessment != Verdict`: `BirthVerdictGate` is deliberately not wired to consume this assessment, since consuming it would imply the missing conjuncts were satisfied. This stage issues no `BirthVerdict`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.IC.1b evidence-derived weaker-model closure outcome | ENFORCED_AT_CLOSURE_GATE | Closes the first of the two conjuncts AIM-K3 names, and only for one weaker model at a time. Nothing new is invented: `ClosureCriterionSpec.supported_statuses` already declares the closed three-member vocabulary of `Close(W_i, R)`, `BirthExperimentSpecification.frozen_weaker_models` already derives the prerequisite cone from the frozen projection poset before any evidence exists, and `ProvenanceBoundEvaluatorExecutionRecord` (G0.BA.1b) already proves `EvaluatorExecutedOnEvidence`. The single missing step was that nothing related an evaluator's `output_content` -- a plain string -- to a member of that closed vocabulary. `DeclaredClosureOutcomeVocabulary` is that relation, declared as data rather than computed as a judgement: it must cover every `ClosureAssessmentStatus` member exactly once, must not bind one token to two outcomes, and refuses a token carrying surrounding whitespace because matching is exact. The same register -> seal -> gate shape applies: `ClosureOutcomeVocabularyRegistry.register` is the sole issuer of an `AuthorizedClosureOutcomeVocabulary` and requires a verified `BirthAssessmentContentBinding`, so the criterion spoken for is content-frozen in a sealed semantics registry and not merely named; `seal` alone produces a `SealedClosureOutcomeVocabularyRegistry`; and `WeakerModelClosureGate.assess` alone produces a `WeakerModelClosureCertificate`. `CallerDoesNotOwnClosureOutcome`: `assess` accepts no status, reason, or outcome claim, and takes exactly two parameters. `ExactTokenOrRefusal`: the output is matched by exact string equality, with no trimming, case folding, prefix or substring match, nearest match, or default -- an unrecognized output is refused by model id and is never read as `DEFER`, because silently reading ignorance as a declared outcome is precisely the failure this gate exists to prevent. The gate also refuses a record executed under any role other than `WEAKER_MODEL`, and a target outside the derived frozen prerequisite cone. All three declared outcomes are reachable. Four claims remain refused. `LocalClosureOutcome != WeakerModelExhaustion`: a certificate speaks for exactly one model, nothing here aggregates the cone or checks its coverage, and `is_weaker_model_exhaustion` is `False` unconditionally. `WeakerModelClosure != IndependentClosure`: the residual-survival conjunct has no authority here and the comparability conjunct belongs to G0.IC.1a, so `is_independent_closure` is `False` on every branch, `IndependentClosureAssessment` is untouched, and this stage is deliberately wired to neither it nor `BirthVerdictGate`. `DeclaredVocabularyIsNotProvenSemantics`: freezing the token-to-status map before the gate runs prevents a map tailored to an output already seen, and proves nothing about why the evaluator emitted that token. `SealedBeforeAssessmentIsNotSealedBeforeEvidence`: no authority in this repository timestamps a seal against an evidence acquisition run, so the vocabulary is proven frozen relative to the gate, not relative to the evidence. This stage issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.IC.1c derived weaker-model exhaustion | ENFORCED_AT_CLOSURE_GATE | Aggregates G0.IC.1b's per-model certificates into the second conjunct of `IndependentClosure`, and nothing beyond it. The licensed set is not invented here: `BirthExperimentSpecification.frozen_weaker_models` already derives the cone from the frozen projection poset before any evidence exists, so how many models must be answered is fixed in advance and cannot be trimmed to fit the certificates that happen to exist. `MalformedRequestIsNotNonExhaustion`, copied from `InvariantVerificationGate.assess_all_preserved`: certificates that do not exactly cover the cone, that name one model twice, or that name a model the frozen poset never licensed are a malformed request and raise, because an unevaluated model is ignorance and reading ignorance as a failure to close is exactly how a fabricated exhaustion would be manufactured. `OneRequestOnly`: every certificate must be bound to the same `BirthAssessmentRequest` object, since certificates from different requests describe different evidence. `CallerDoesNotOwnExhaustion`: `WeakerModelExhaustionGate.assess` accepts no status and no reason, takes exactly two parameters, reads every certificate rather than stopping at the first, and derives the status under a fixed precedence -- `WEAKER_MODEL_CLOSES_RESIDUAL` > `EXHAUSTION_UNDETERMINED` > `LICENSED_WEAKER_MODELS_EXHAUSTED` -- so a known `CLOSE` is never erased by an unrelated `DEFER` (`False and Unknown == False`) and the aggregate does not depend on certificate order. All three statuses are reachable, and `outcome_counts` is a derived property covering every declared outcome including zeros, never a written field. Claims still refused: `WeakerModelExhaustion != IndependentClosure` -- the surviving-residual conjunct has no authority in this repository and comparability belongs to G0.IC.1a, so `is_independent_closure` is `False` on every branch here too, `IndependentClosureAssessment` is untouched, and this stage is wired to neither it nor `BirthVerdictGate`. `WeakerModelClosesResidual != NoBirthVerdict`: the `CLOSE` branch is the shape of an argument against birth in this scope, not that verdict. `CoverageIsNotCorrectness` and `FrozenConeIsDeclaredNotProven`: the gate proves every licensed model was evaluated on this request's own authorized evidence and reported a declared outcome, not that those outcomes are true or that the poset licensed the right models. `SameRequestIsNotSameEvidenceRun`: sharing one request proves one frozen experiment and one evidence snapshot, not any ordering or co-execution of the evaluators. This stage issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.IC.1d evidence-derived residual survival outcome | ENFORCED_AT_CLOSURE_GATE | Reads the third and last conjunct of `IndependentClosure` for one witness, and stops there. Nothing new is invented: `ResidualDefinitionSpec` already declares the residual whose survival is at stake, its `supported_statuses` declares the closed three-member `ResidualSurvivalStatus` vocabulary exactly as `ClosureCriterionSpec.supported_statuses` declares `Close(W_i, R)`'s, and `ProvenanceBoundEvaluatorExecutionRecord` (G0.BA.1b) already proves `EvaluatorExecutedOnEvidence`. The missing step was the same one G0.IC.1b closed for closure outcomes: nothing related an evaluator's `output_content` -- a plain string -- to a member of that closed vocabulary. `DeclaredResidualSurvivalVocabulary` is that relation, declared as data rather than computed as a judgement: it must cover every `ResidualSurvivalStatus` member exactly once, must not bind one token to two outcomes, and refuses a token carrying surrounding whitespace because matching is exact. The same register -> seal -> gate shape applies: `ResidualSurvivalVocabularyRegistry.register` is the sole issuer of an `AuthorizedResidualSurvivalVocabulary` and requires a verified `BirthAssessmentContentBinding`, so the residual spoken for is content-frozen in a sealed semantics registry and not merely named; `seal` alone produces a `SealedResidualSurvivalVocabularyRegistry`, resolving only by the exact `(domain, residual_id)` scope; and `ResidualSurvivalGate.assess` alone produces a `ResidualSurvivalCertificate`. `CallerDoesNotOwnResidualSurvival`: `assess` accepts no status, reason, or survival claim, and takes exactly two parameters. `ExactTokenOrRefusal`: the output is matched by exact string equality, with no trimming, case folding, prefix or substring match, nearest match, or default -- an unrecognized output is refused by residual id and is never read as `DEFER`. The gate also refuses a record executed under any role other than `RESIDUAL_DEFINITION`, and a target that is not the request's own frozen `residual_definition_id`. `MixedModeNeedsTwoScopedWitnesses`: `evidence_mode` is read from the frozen experiment and never from the caller, and a `MIXED` experiment is refused by name, because that mode is an explicitly typed scoped pair `<(D_emp, S_emp), (D_formal, S_formal)>` and no authority here proves those declared scopes or `NoCrossSubstitution(D_emp, D_formal)`; a named refusal is safer than one certificate a later reader could take as having satisfied both modes. All three declared outcomes are reachable. Claims still refused. `ResidualSurvivalOutcome != IndependentClosure`: the three conjuncts are now each derived on their own -- comparability by G0.IC.1a, exhaustion by G0.IC.1c, survival here -- but composing them is a separate question with no authority in this repository, so `is_independent_closure` is `False` on every branch, `IndependentClosureAssessment` is untouched, and this stage is wired to neither it nor `BirthVerdictGate`. `DoesNotSurvive != NO_BIRTH_IN_SCOPE`: a residual failing to survive is the shape of an argument against birth in this scope, not that verdict. `SurvivalReadIsNotMeasuredReplicatedResidual`: in `EMPIRICAL` mode `NoBirthWithoutResidualOrFormalNecessity` requires a *measured* residual that survives every licensed weaker projection and replicates in a second independent measurement run, and nothing here inspects provenance genus or knows of a second run. `FormalNecessityIsNotProvedHere`: in `FORMAL` mode a declared outcome is read, not an exhaustive proof over the declared closed domain verified. `DeclaredVocabularyIsNotProvenSemantics` and `SealedBeforeAssessmentIsNotSealedBeforeEvidence` are inherited unchanged from G0.IC.1b. `OneWitnessIsNotResidualCertification`: G0.RC.1 remains deferred exactly as written, `ResidualCertificationCandidate` is untouched, and no freeze, reconstruction, or comparison authority is created here. This stage issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.IC.1e composed independent-closure decision | ENFORCED_AT_CLOSURE_GATE | Composes the three conjunct readings G0.IC.1a, G0.IC.1c and G0.IC.1d each derived on their own, and claims nothing beyond what they say. Nothing new is read: the gate opens no evidence, executes no evaluator, and inspects no frozen poset, because every input is already a gate-issued reading (`ThreeReadingsAreNotAFourth` -- a composition that re-derived a conjunct would be a second authority over a question already answered, and the two answers could disagree). `IndependentClosureCompositionGate.assess` alone produces an `IndependentClosureDecision`, and `CallerDoesNotOwnComposition`: it takes exactly three parameters -- the comparability assessment, the exhaustion assessment and the survival certificate -- and no status, reason, or closure claim. `OneRequestOrRefusal`: the three readings must speak for the same `BirthAssessmentRequest` by object identity, exactly as G0.IC.1c requires of its certificates, and the survival reading must carry that request's own authorized evidence snapshot; readings of different requests are refused, never composed. The enumeration was performed before the module was written: comparability is two-valued and exhaustion and survival are three-valued, so there are exactly `2 x 3 x 3 = 18` combinations, and each conjunct falls into exactly one of three roles -- satisfied (`COMPETITION_RESOLVED_IN_POSET`, `LICENSED_WEAKER_MODELS_EXHAUSTED`, `SURVIVES`), refuting (`WEAKER_MODEL_CLOSES_RESIDUAL`, `DOES_NOT_SURVIVE`), or undetermined (`EXHAUSTION_UNDETERMINED`, `DEFER`, `COMPETITION_UNRESOLVED_IN_POSET`). `UnresolvedComparabilityIsIgnoranceNotRefutation`: comparability has no refuting branch at all, because G0.IC.1a already resolves `AbsentRelation != DeclaredIncomparability` conservatively, so reading its unresolved branch as a refutation would manufacture knowledge out of silence. Aggregation follows the precedence already enforced twice in this kernel: `CLOSURE_REFUTED_IN_SCOPE > CLOSURE_UNDETERMINED_IN_SCOPE > CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION`, with refuted and undetermined conjuncts tracked in separate fields, as `InvariantVerificationDecision` tracks `failed_components` and `deferred_components`, and reported in a fixed conjunct order independent of caller order. Of the 18 combinations, 10 are refuted, 7 are undetermined, and exactly 1 -- resolved comparability, exhausted licensed weaker models, and a surviving residual -- reaches the third status. Claims still refused. `SatisfiedConjunctsIsNotIndependentClosure`: even that one combination yields `is_independent_closure == False`, because the three conjuncts hold *as read* and reading is all that happened -- `OneWitnessIsNotResidualCertification` (G0.RC.1 is deferred, so no certified residual exists to close over), `SurvivalReadIsNotMeasuredReplicatedResidual`, and `CoverageIsNotCorrectness` with `FrozenConeIsDeclaredNotProven` each remain open by name. The status name states exactly what was reached and what it is pending on, rather than overstating it, so AIM-K3 is narrowed by name rather than declared met. `CompositionIsNotAVerdict`: this stage is deliberately not wired to `BirthVerdictGate`, the readings it consumes keep their own `False` constants, and `ClosureRefutedInScope != NO_BIRTH_IN_SCOPE`. It issues no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no `TraditionalName`. |
| G0.BC.1a birth-certificate contract and constitutional/executive split | ENFORCED_AT_CERTIFICATION_GATE | Supplies the contract G0.BV.1a and G0.IC.1e both stop short of, and activates neither birth branch. `BirthVerdict != BirthCertificate != Execution`: a verdict decides that the conditions for existence of this genus were met in this scope, a certificate preserves that decision with its scope, necessity readings, evidence references, preventers and trace, and execution uses what was born and may never create it. Two authorities, neither able to perform the other's act: only `ConstitutionalBirthAuthority.assess` may produce a `BirthCertificate` and it exposes no method that runs anything, and only `ExecutiveAdmissionGate.admit` may produce an `ExecutableEntity` and it exposes no method that certifies anything; `ExecutiveAuthorityCannotIssueBirth` and `ConstitutionalBirthAuthorityCannotExecuteTheBornEntity` are enforced by the two classes' public surfaces, asserted by test, not only by prose, so successful execution is never evidence of valid birth. `CallerDoesNotOwnCertification`: `assess` accepts no status, reason, finding or birth claim, and re-derives every finding from two gate-issued decisions. `OneRequestOrRefusal`, copied from G0.IC.1c and G0.IC.1e: the two decisions must speak for the same `BirthAssessmentRequest` by object identity, and a mismatch raises rather than becoming a negative finding, because `MalformedRequestIsNotNonExhaustion` applies unchanged. `APreventerHasAnIdentityNotABoolean`: every member of `BirthPreventer` is derived on every assessment, held or cleared, each with its own reason, and held and cleared findings are tracked separately as `InvariantVerificationDecision` separates `failed_components` from `deferred_components`; the trace records each preventer, its branch and its reason. Necessity is read, never re-derived: `NoBirthWithoutUnclosedResidual` from the closure decision's survival certificate, `NoBirthBeforeLowerLayerExhaustion` and `NoBirthWhenAWeakerReconstructionStillSuffices` from its exhaustion assessment, because a second authority over questions G0.IC.1c and G0.IC.1d already answered could disagree with them (`ThreeReadingsAreNotAFourth`). `NoCertificateIsReachableInThisTree`, declared rather than discovered: three preventers hold on every branch, each naming a different missing authority -- no authority issues the `BirthCandidate` a certificate must name (`AUTHORITY_MISSING`), none proves its identity (`IDENTITY_NOT_PROVED`), and none proves its difference from the origin it branched from (`CANDIDATE_EQUIVALENT_TO_ORIGIN`) -- and a fourth, `VERDICT_NOT_BIRTH_IN_SCOPE`, holds because G0.BV.1a's codomain is still the single value `DEFER_IN_SCOPE`. All `3^5 = 243` reading combinations are enumerated in test and none yields a certificate. `BirthDoesNotMeanFreeze` and `BirthDoesNotMeanTruth`: a certificate issues no `Freeze`, no `E0` mapping and no `TraditionalName`, and claims nothing about the world; the three denials are derived properties rather than prose. `NoGenusLadderIsEncodedHere`: instruction, rule, general rule, universal rule, law and constitution are not encoded as a closed vocabulary, since each such genus would need its own birth certificate and birth specification before entering any ontology, so the ceiling is expressed as denials rather than as a rank. G0.BV.1 remains `DECLARED_DEFERRED_CONTRACT_ONLY` and this stage is wired into no verdict path. |
| A0.CD.1 usuli comprehension-defect vocabulary | DOCUMENTED_CLASSIFICATION_ONLY | An Arabic-layer classification with no authority whatsoever. `ComprehensionDefectCause` is the closed five-value vocabulary the usuliyyun counted as the causes of defective comprehension -- `اشتراك`, `نقل`, `مجاز`, `إضمار`, `تخصيص` -- with the explicit non-member value `لا_ينطبق`; any other text, misspelling or invented term, is rejected rather than folded onto the nearest member. Its priority order at conflict is `تخصيص > مجاز = إضمار > نقل > اشتراك`, and each of the ten pairwise comparisons carries its own textual argument and named source in `PRIORITY_ARGUMENTS`, so no rank rests on estimation; the `مجاز = إضمار` tie adopts the view that counts `إضمار` a `مجاز` by omission and records the competing ordering rather than hiding it. `DeclaredDefectCause != AssessedRelation`: an optional per-reading `سبب_الإخلال_بالفهم` on an external audit card is validated and reported as `تصنيف_أسباب_الإخلال_بالفهم` and nothing else -- it never enters the derived `BirthExperimentSpecification`, never changes `نتيجة_التدقيق_الخارجي`, and neither `IndependentClosureGate` nor `BirthVerdictGate` reads it; removing every classification leaves all other reported fields identical. `FixedTextAmbiguity != ReadingMultiplicity != TransmissionWeakness` is the declared scope limit: the five causes address ambiguity of meaning in a fixed text, not disagreement over the recited wording and not the strength of a report's transmission. Partial applicability is therefore an expected structural result, not an implementation gap: across the four example cards only three of eight competing readings are described by a cause (`تخفيف_إن_وضمير_شأن` as `إضمار`; the `مَن`/`ما` readings of `man_2_255` and `maa_2_197` as `اشتراك`), and the remaining five are declared `لا_ينطبق` rather than forced into a label. |
| A0.PP.1 probe preregistration | ENFORCED_AT_PROBE_PREREGISTRATION | An Arabic documentation-layer boundary with no kernel authority, closing the gap between a *recorded past* probe specification and an *enforced pre-evidence* one: `FrozenProbeSpecification != EnforcedPreEvidenceSpecification`. `FrozenFollowupProbeSpecification` carries no result field at all, checked at import against its own dataclass fields rather than asserted in prose. `PreEvidenceProbeSpecificationRegistry.freeze` is the sole issuer of a `FrozenPreEvidenceProbeManifest` and refuses different content re-frozen under one `(experiment_id, revision_id, revision_sequence)` identity; `FollowupProbeSpecificationContentBinding` re-encodes the live specification and compares canonical bytes, so post-freeze drift cannot be bound. `NoResultWithoutPriorSpecification`: a `ProbeResultAttachment` is unconstructible without that binding, and construction fails -- never warns -- on a feature outside the frozen set, a selection criterion or stopping rule other than the frozen ones, or a `k` outside the frozen range, which is what makes `NoOracleTuningBeforeFreeze` structural instead of remembered. `EvidenceGenus` is deliberately two-valued (`DISTRIBUTIONAL`, `MORPHO_FUNCTIONAL`) with no `MIXED`: mixing genera requires an explicit `(E_D, E_M, CompositionRule)` composition contract that does not exist yet, and `MORPHO_FUNCTIONAL` is declared-but-unconstructible because no frozen morphological feature vocabulary has been born. `ProbeResultAttachment != BirthVerdict` and `FrozenFollowupProbeSpecification != BirthExperimentSpecification`: this registry is a local documentation-layer freeze, not a kernel authority; no `Freeze`, no `E0`, and no kernel gate reads it. |
| A0.PP.1a phase-2 question stays open | DOCUMENTED_OPEN_QUESTION | `Phase2OpenQuestion` records the question the recorded negative result raises, with no answer, verdict, conclusion, resolution, or decision field, checked at import. It requires all three hypotheses rather than a false dichotomy: (A) only the five current features are insufficient; (B) the `اسم`/`فعل`/`حرف` division is not a surface-distributional kind at all, so no enlargement of that evidence genus recovers it; (C) the division becomes distributionally recoverable only after lower structural variables (boundary, position, morphological transformation) are themselves born as licensed carriers, per `Closure_L -> Handoff_L -> Birth_{L+1}`. `RecordedQuestion != Answer`: dropping or repeating a hypothesis is refused, and no authority here may resolve any of the three. |
| A0.PP.1b one canonicalization, no authority transfer | ENFORCED_AT_CANONICAL_PRIMITIVE | `Canonicalization != Authority`. `src/alghanem/canonical_content.py` is the single place canonical bytes and digests are produced, used by both the kernel's content encoders and the Arabic preregistration layer, because two copies of a canonicalization rule are two rules that can silently drift apart. It encodes and hashes and decides nothing: it has no notion of a specification, experiment, freeze, verdict, or birth, so a layer importing it inherits a deterministic byte encoding and no permission from any other importing layer. |
| A0.PP.2 four-rank readiness ladder | ENFORCED_AT_READINESS_RECORD | `RecordedStatusProse != EnforcedReadinessRecord`, one level above `FrozenProbeSpecification != EnforcedPreEvidenceSpecification`: the phase-2 status table lived only as prose in a pull-request body, where it could later be read as an enforced fact while being guarded by nothing. `src/alghanem/arabic/readiness_rank.py` makes it a record that refuses false combinations at construction. Four independent closed vocabularies, deliberately not one enum with four values, because a single ladder implies a false total order in which a higher rank looks entailed by its position rather than by a prior condition: `StructuralReadiness` (`NOT_BUILT`, `BUILT_AND_CHECKED`), `SpecificationFreeze` (`NOT_YET_FROZEN`, `FROZEN`), `MeasurementProgress` (`NOT_STARTED`, `STARTED`, `COMPLETED`), `QuestionStatus` (`OPEN`, `CLOSED_BY_FROZEN_EXPERIMENT`). Four is the minimum sufficient count, not an assumed one: merging structure with freeze would make freezing an automatic promotion of a checked build, though a checked build with no frozen future specification is exactly today's state; merging freeze with measurement would erase the difference between a frozen specification that binds every later measurement and no specification at all; merging measurement with the question would make a completed measurement a settlement, though completion settles nothing without a specification frozen before its evidence. Implication runs one way only, as a prior condition and never its converse: measurement beyond `NOT_STARTED` requires `FROZEN`, `FROZEN` requires `BUILT_AND_CHECKED`, and closure requires `COMPLETED`; a frozen specification with no measurement yet, and a completed measurement with an open question, are both admissible states now. `CLOSED_BY_FROZEN_EXPERIMENT` is declared in the vocabulary rather than omitted, and is unconstructible today under the same discipline as `EvidenceGenus.MORPHO_FUNCTIONAL` -- refused at construction of any record, not only in the module-level one, since no birth gate or verdict authority exists here to issue a closure, and refusing it only in one place would leave every other record free to write it. That refusal is checked before the general implication message, so a refusal grounded in "no issuing authority exists" is not read as the shallower "measurement is not finished". Each rank carries its own non-blank justification, and the single module-level `PHASE2_READINESS` takes its `question_id` from `PHASE2_OPEN_QUESTION` rather than copying the string, with an import-time guard against openness drift between the two. `ReadinessRankRecord != BirthVerdict` and `SpecificationFreeze != Freeze`: the record carries no answer, verdict, or birth field (checked at import against its own dataclass fields), and no kernel gate reads it, which a test enforces by scanning every `kernel/` module. |
| A0.PP.3 cross-project vocabulary import contract | ENFORCED_AT_IMPORT_CONTRACT | `ForeignFrozenExport != LocalFreeze`, one level above `Canonicalization != Authority`: the source project `GFLK-Taaqol-GPT` exports the `OriginType` vocabulary `gflk.origin_type.v1` over the `ORIGIN_LEDGER_AR_v1` ledger with a deterministic content id and a self-declared `FROZEN_LOCAL` scope, and `src/alghanem/arabic/imported_feature_vocabulary.py` is the receiving contract. `ForeignFreezeScope` is a one-valued closed vocabulary read as declared and never promoted: no function converts it into `SpecificationFreeze.FROZEN`, a kernel `Freeze`, an `E0`, or a birth, since promotion would claim a gate this repository does not hold. `ImportedFeatureVocabulary` is bound to `EvidenceGenus.MORPHO_FUNCTIONAL` and refuses any other genus -- the binding named as missing when the import workstream was deferred. `ImportedOriginType` is closed over `EVENT`, `ENTITY`, and `UNRESOLVED`, with `UNRESOLVED` a member rather than a gap, and an unknown value is refused instead of folded into it. The distribution and row count are *derived* by counting the entries; a declared distribution or count that disagrees with the derived one is refused, so no field exists into which the answer may be written directly, and duplicate roots are refused because a duplicate hides one entry under another's identity. `ImportedVocabularyContentVerifier` is the sole issuer of `VerifiedVocabularyImport` and `LocalVocabularyContentIdentity` (private-token issuance), re-deriving an Alghanem-side content id through the shared `alghanem.canonical_content` primitive rather than trusting the declared digest, with schema coverage checked at import against the vocabulary and entry dataclass fields. `assert_matches_recorded_release` pins the recorded release -- 270 rows, 126 `EVENT` / 56 `ENTITY` / 88 `UNRESOLVED`, the source ids, and the declared source digest -- so a mismatched import is refused, not passed through silently. Boundaries: `ImportedVocabulary != BornOntology`, so this is not the deferred born morpho-functional vocabulary and leaves the five distributional features and `RECORDED_PROBE_REPORT` byte-identical; the scope stays narrow to `OriginType` because the weight and structure vocabularies have not been exported; and the module carries no result, verdict, or birth field (checked at import) and no kernel gate reads it, enforced by a test scanning every `kernel/` module. The source digest is recorded as declared and pinned, not independently re-derived: doing so would require the source's byte-precise canonicalization schema and its full payload, neither of which is in this repository, which the module states rather than conceals. What is known of that digest is recorded and enforced rather than assumed: by the export generator's own self-check it covers only each entry's `root` and `origin_type`, so `raw_category` and `batch_note` move without it, while the Alghanem-side identity covers every entry field. `SOURCE_DIGEST_COVERED_FIELDS` is asserted at import to be a *proper* subset of the entry fields, so the local identity is strictly finer than the source's and the two can never be read as attesting the same thing. |
| G0.2a.1 birth semantics content identity | ENFORCED_AT_CONTENT_ENCODER | `NoResidualIdDriftAfterFreeze`/`NoClosureCriterionIdDriftAfterFreeze` (G0.2a's id-equality checks) are label identity, not content identity: `ResidualDefinitionId != ResidualDefinitionContentIdentity`, and the same distinction holds for `ClosureCriterionSpec` and `WeakerModelSpec`. `CanonicalBirthSemanticsEncoder` is the sole issuer of `CanonicalResidualDefinitionManifest`, `CanonicalClosureCriterionManifest`, `CanonicalWeakerModelManifest`, and their `BirthSemanticsContentIdentity` SHA-256 digest references, covering every declared field of each spec. `BirthSemanticsContentRegistry` freezes the *first* canonical content bound to an exact `(domain, role, target_id)` scope; a later attempt to bind different content to that same scope is content drift and is rejected, not silently accepted because the id string still matches. `BirthAssessmentContentBinding` resolves every scope a `BirthAssessmentSemanticsContract` declares against a `SealedBirthSemanticsContentRegistry` and requires `CID(runtime) == CID(frozen)` for the residual definition, the closure criterion, and every weaker model; an unresolvable scope raises rather than passing silently. This closes `NoSemanticDriftAfterFreeze` for content, distinct from and in addition to `NoResidualDefinitionDriftAfterFreeze`/`NoClosureCriterionDriftAfterFreeze` for ids. It performs no evaluation and issues no `BirthVerdict`, `BirthCandidate`, or `Freeze`; `EvaluatorId != EvaluatorImplementationIdentity` and evaluator execution authority remain out of scope. |
| G0.2a.3 evidence acquisition authority | ENFORCED_AT_ACQUISITION_AUTHORITY | Binding evidence to a frozen experiment (G0.2a.2) proves only `FreezePrecedesRequestConstruction`, not that the freeze authorized the evidence's own acquisition; a caller could still select evidence first and attach a freeze afterward. This stage closes the narrower, code-provable `FrozenExperimentPrecedesAuthorizedEvidenceIngestion` instead of an unprovable external-world chronology claim (`AuthorizedCapture != ProofOfExternalAcquisitionChronology`). `EvidenceAcquisitionAuthority.authorize` is the sole issuer of an `EvidenceAcquisitionAuthorization`, requiring a genuine, verified `BirthExperimentSpecificationContentBinding` (`NoEvidenceAcquisitionAuthorizationWithoutFrozenExperiment`); its `experiment_content_id`, `domain`, `evidence_mode`, `evidence_requirements`, `revision_id`, and `revision_sequence` are derived properties of that binding, never independent caller-supplied facts. Only that authorization can issue an `EvidenceAcquisitionRun` (`open_run`), and only that run can issue an `AuthorizedEvidenceSnapshot` (`ingest`), closing `NoAssessableEvidenceSnapshotWithoutAcquisitionAuthorization`; none of the three is caller-constructible. `CanonicalEvidenceContentEncoder` alone issues the ingested payload's `EvidenceContentIdentity`, keeping `EvidenceOccurrenceIdentity != EvidenceContentIdentity` (`snapshot_id`/`run_id`/`authorization_id` name one occurrence; `content_id` is a digest over ingested bytes). `BirthAssessmentRequest` now requires an `AuthorizedEvidenceSnapshot` (rejecting the deprecated, unauthorized `EvidenceSnapshot`) and rejects a snapshot whose `experiment_content_id` does not equal its own experiment binding's `content_id`. `AuthorizedEvidence != SufficientEvidence`: this stage does not imply `ResidualSurvival` or `Birth`, and issues no `ResidualAssessment` or `BirthVerdict`. |
| G0.2a.3.1 issuer-scoped occurrence issuance integrity | ENFORCED_AT_ACQUISITION_AUTHORITY | Before this stage, `authorization_id`/`run_id`/`snapshot_id` were caller-chosen strings with no uniqueness authority: an issuer accepted a repeat of the same id, so `same(id) => same(occurrence)` did not hold and these were `EvidenceOccurrenceCoordinates`, not a proven identity. Each issuer now keeps its own registry of ids it has already issued -- `EvidenceAcquisitionAuthority` for `authorization_id`, one `EvidenceAcquisitionAuthorization` for its own `run_id`s, one `EvidenceAcquisitionRun` for its own `snapshot_id`s -- and `EvidenceAcquisitionAuthorityError` rejects a repeat within that scope, even for a snapshot repeat carrying different content. Each registry's check-and-insert is synchronized with an internal lock so concurrent calls on one instance cannot race past the uniqueness check. This makes issuance injective *within its declared scope* (`IssuerScopedOccurrenceUniqueness = PROVED`): two ids from the same issuer that are equal name the same occurrence, and two ids from the same issuer that differ name different occurrences. `LocalInjectivity != PortableIdentity`: `AuthorizedEvidenceSnapshot` carries no `issuer_scope_id`, so two distinct `EvidenceAcquisitionAuthority` instances are separate, uncoordinated issuance scopes whose ids are not thereby proven to differ from each other, and two snapshots from different authorities can share identical comparable representations despite being genuinely independent occurrences. `PortableEvidenceOccurrenceIdentity` remains `DEFERRED` pending a self-issuing `EvidenceIssuerScopeIdentity` propagated through the chain. `EvidenceAcquisitionRun`/`EvidenceAcquisitionAuthorization` are `ExternallyFrozen, InternallyStatefulAuthority` objects: `frozen=True` fixes their own declared identity fields, but each also holds a private, mutable `_issued_*` registry and lock (excluded from equality, `repr`, and content identity) as operational bookkeeping only. |
| G0.BA.1a authorized evaluator implementation binding | ENFORCED_AT_EXECUTION_GATE | Closes exactly one narrower residual left open by G0.2a: `AuthorizedBirthAssessmentEvaluatorDefinition != AuthorizedEvaluatorImplementation != EvaluatorExecution`. G0.2a's registry authorizes evaluator *declarations* (`domain`, `role`, `target_id`, `evaluator_id`) only, and performs no execution. `AuthorizedBirthEvaluatorImplementationBinding` is unchanged from and does not retroactively grant execution semantics to `AuthorizedBirthAssessmentEvaluatorDefinition`; instead, `BirthEvaluatorImplementationRegistry.register` requires an already-authorized definition plus an `implementation_identity` and an executable callable, and only `BirthEvaluatorImplementationRegistry.seal` freezes those bindings into a `SealedBirthEvaluatorImplementationRegistry`. `BirthEvaluatorExecutionGate.execute` is the sole authority that may resolve a binding by exact `(domain, role, target_id, evaluator_id, implementation_identity)` scope and invoke it, producing a `BirthEvaluatorExecutionRecord` -- a non-caller-constructible audit record preserving the authorized definition, implementation identity, role, target, the exact `BirthAssessmentRequest` and its own bound `AuthorizedEvidenceSnapshot`, input/output content, and trace. This record carries no `ResidualEvaluationResult`, `WeakerModelEvaluationResult`, `ClosureEvaluationResult`, aggregate assessment, residual survival, weaker-model exhaustion, `BirthCandidate`, `IndependentClosure`, `BirthVerdict`, or `Freeze` meaning: `Definition != ImplementationBinding != ExecutionRecord != Assessment`. Composing per-role execution records into any assessment remains a separate, later, still-deferred question. `AuthorizedCallableInvocation`, not `AuthorizedAssessmentEvidenceExecution`: the gate invokes the bound callable on caller-supplied `input_content`; it does not prove that content was derived from, or equals, the attached `AuthorizedEvidenceSnapshot`'s own payload (`EvidenceAttachedToRecord != EvaluatorExecutedOnEvidence`; `InputProvenance = DECLARED_DEFERRED`). Nor does it prove the resolved definition belongs to this request's own frozen `BirthAssessmentContentBinding`/`BirthAssessmentEvaluatorDefinitions` -- only that its `domain` matches (`AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment`). `implementation_identity` is a declared, caller-chosen string with no canonical manifest or digest of its own (`DeclaredImplementationId != ImplementationContentIdentity`; `ImplementationIdentityIsContentAuthenticated = DEFERRED`). |
| G0.BA.1b evidence-derived evaluator input provenance | ENFORCED_AT_DERIVATION_GATE | Closes exactly one of the three claims G0.BA.1a refused to make: `InputProvenance = DECLARED_DEFERRED`. The fix is structural, not a comparison added to the old gate. An `EvaluatorInputDerivation` receives exactly one argument -- the `canonical_bytes` of the request's own `AuthorizedEvidenceSnapshot` manifest -- and `EvaluatorInputDerivationGate.derive` accepts no `input_content` and no domain parameter at all (`CallerDoesNotOwnInputContent`): the caller chooses which authorized derivation runs, never what the evaluator sees, and the domain is read from the request's own frozen experiment. The same register -> seal -> gate shape applies: `EvaluatorInputDerivationRegistry.register` is the sole issuer of an `AuthorizedEvaluatorInputDerivationBinding`, `seal` alone produces a `SealedEvaluatorInputDerivationRegistry` resolving only by the exact three-part scope `(domain, derivation_id, implementation_identity)`, and only `EvaluatorInputDerivationGate.derive` issues an `EvidenceDerivedEvaluatorInput`. The gate re-verifies that the snapshot's bytes hash to the snapshot's own `EvidenceContentIdentity` before deriving, and rejects a derivation that returns non-text, blank content, or a different result for the same authorized bytes (`ObservedDeterminism != ProvenPurity`: this rejects observed nondeterminism, it does not prove purity). `CanonicalEvaluatorInputDerivationEncoder` digests the source evidence identity, the derivation id, the implementation identity, and the produced content together under length-prefixed canonical bytes, so the issued `EvaluatorInputContentIdentity` binds what was produced, from which exact evidence, and by which declared derivation (`OutputDigest != DerivationIdentity`). `ProvenanceBoundEvaluatorExecutionGate.execute` delegates the invocation itself to the unchanged `BirthEvaluatorExecutionGate` and then binds the issued record to the derivation that produced its input, requiring the same request object, the same evidence snapshot object, and exactly the derived content. G0.BA.1a is preserved completely unchanged and still accepts unrelated caller-supplied input by design: provenance is proven only for records issued by this stage. Three claims remain refused. `DerivationIdIsContentAuthenticated = DEFERRED`: `derivation_id` and `implementation_identity` are plain, caller-chosen strings with no manifest or digest of the derivation code (`DeclaredDerivationId != DerivationContentIdentity`), and `declared_transformation` is carried for audit and never verified against the callable (`DeclaredTransformation != VerifiedTransformation`). `AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment` is inherited unchanged: the execution boundary still matches only `domain`. `ProvenInputProvenance != AssessedEvidence`: `is_assessment` is `False` unconditionally, and the record carries no residual survival, weaker-model exhaustion, closure, `BirthCandidate`, `IndependentClosure`, `BirthVerdict`, or `Freeze` meaning -- `Derivation != ExecutionRecord != Assessment`. |
| AIM.1 declared programme aims, stage two record | ENFORCED_AT_AIM_RECORD | `DeclaredAim != LicensedProgramme`, `Aim != Achievement`, `AimsDocument != Authority`. [`docs/AIMS.md`](AIMS.md) names the programme's aims, each with its question, what would count as reaching it, what would not count even though it resembles it, and its citation in this record; aims are *extracted* from the existing record rather than dictated from outside it. Indicators of progress are declared epistemic and never engineering, and the reason is named rather than left implicit: an engineering indicator answers "does the code run?", while this programme's indicators answer "is the judgment the code issues earned by its evidence?" — two independent questions, since an empty function that always returns `PASS` can hold full test coverage and a green CI, so merging the two axes reproduces that defect at the scale of the whole programme instead of one unit. `TestPassIsNotUniversalTruth` (Encyclopedia Self-Observation, below) is the same refusal stated from inside this constitution. Aims that have not started are kept distinct from aims blocked by a *named* obstacle (`NamedObstacle != SilentAbsence`), and two foreign aims imported from the `A0.PP.3` source project are recorded as declared only (`DeclaredForeignAim != AlghanemRecord`): nothing here verifies them, and they enter no indicator. Stage two has begun and is enforced at `alghanem.program.aims`, one milestone at a time: `AimRecord` carries each aim's question, both boundaries, and its citation, across two independent vocabularies (`AimEngagement`, `AttainmentStanding`) rather than one ordinal scale, with each refused merge justified in writing. `AttainmentStanding.REACHED` is declared and refused at construction itself, exactly like `QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT`: no authority here may issue an aim's attainment. Absence of classification is a vocabulary member (`UNCLASSIFIED_IN_RECORD`), never a silent blank read later as progress, and `DeclaredForeignAim != AlghanemRecord` is a type boundary (`ForeignDeclaredAim`) rather than a field value, so exclusion from every later derivation is structural rather than disciplined. The module cites the open audit question `DeclaredVersusDerivedRecurrenceNotExplained` as its direct design source, as §5 of that document requires, and a test enforces the citation rather than trusting prose. The next milestone adds exactly the two derivation readers §4 names and nothing more, at `alghanem.program.constitution_ledger`: the law-table rows of this document and its open and resolved audit questions are read into two separate ledgers whose counts are derived properties rather than written fields, so no recorded number can disagree with this document. A status outside the closed `DeclaredLawStatus` vocabulary halts the read with a named refusal rather than skipping the row, because a silently short count is read later as a complete table; a missing section or an unreadable document is a named refusal too, never an empty ledger. An open question whose status this record does not declare carries `NO_STATUS_DECLARED_IN_RECORD` instead of a blank, and a resolved one keeps its previous audit label and closure law. That reader binds to no aim and imports neither `AimId` nor `AimRecord`, and a test enforces it. The third and last reader §4 names follows at `alghanem.program.deferred_value_ledger`, and only it: the declared-but-unbuildable values that still hold an aim open (`BIRTH_IN_SCOPE`, `MORPHO_FUNCTIONAL`, `CLOSED_BY_FROZEN_EXPERIMENT`). Its source is the `src/` tree rather than a document: each member is imported live so a rename is a named refusal rather than a value read as released, and the holding module's own text is parsed so the hold's site and shape are *derived*. Coding it showed that "unbuildable" is not one shape but three, kept in a three-valued `DeferredValueShape` rather than merged: a guard that names the value and raises; a guard that names it nowhere at all and merely admits its only sibling in a two-valued vocabulary; and a value no guard refuses because its sole authority never writes it, so the authority's derived codomain does not reach it. Each row carries both its declared shape and the shape derived from the code, and a disagreement is refused at construction — the `DeclaredVersusDerivedRecurrenceNotExplained` form doing real work here, where the previous reader had no declared total to compare against. The refusal rule rises one more layer, from the table to the guard: every guard over a tracked vocabulary is recorded in a derived `GuardCensus`, and a declared site with no witness in its module's text halts the read by name instead of being skipped. What remains is named rather than hidden: `REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY` (nothing in this record obliges a hold to take one of the three observed shapes), `SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE` (that hold is written nowhere and follows from an allow-list over a two-valued vocabulary, whose size is checked live), `CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY` (a codomain read from literal writes is *no reaching write was found*, not *no execution reaches it*), and `SECTION_4_NAMES_THREE_VALUES_ONLY` (other held values exist, and widening the list is a judgment this milestone does not hold). That reader binds to no aim either, importing neither `AimId` nor `AimRecord` nor `AttainmentStanding`, which a test enforces. The fourth milestone follows at `alghanem.program.aims_document_ledger`, and only it: the aims layer is subjected to the very rule it imposed on others. The three earlier readers checked declared against derived in *this* document and in the `src/` tree, while the aim record itself stayed a hand copy of `docs/AIMS.md` prose that nothing checked, so the layer exempted itself from its own law. Coding it showed that the record's prose is a paraphrase rather than a transcription — markup dropped, citations normalised — so verbatim comparison would have rejected the standing record or forced a shape the document never declared; what is derived instead is the structure the document does declare: aim identity and order, bullet labels, the §3 classification, and the partial-attainment remainder, with the untested remainder named (`RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION`). The bullet vocabulary is six labels rather than four, because one aim carries two variant labels; dropping them would have silently dropped that aim, and merging them would have erased the partial-attainment distinction the record itself derives. The field-presence laws of `AimRecord` are now enforced against the document that is their source, not only against the record. `AimRecordCorrespondence` carries no pass/fail field: its construction *is* the correspondence, and disagreement is a named refusal rather than a recorded verdict. Importing `AimId` here is not the indicator, and the distinction is structural rather than promised: the indicator binds a derived *count* to an aim, while this reader binds an aim to its own source text, imports none of the three readers, and a test parses its imports to enforce that. Transcription fidelity is not an aim's truth (`TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH`): a false aim faithfully copied passes this reader entirely. Still deferred and not present here: no indicator value is derived, and no field carries one — joining a derived count to a particular aim is the indicator itself and belongs to a later milestone under §4's conditions. The layer remains authority-inert: `AimRecord != BirthVerdict`, it issues no `Freeze`, no `E0`, no birth, and no verdict, it orders nothing by priority, and an automated scan asserts that no `kernel/` module reads it. |
| G0.MA.0 no predetermined pattern architecture (law only) | DECLARED_LAW_ONLY | See **G0.MA — Meta-architecture law** below. No runtime type or gate exists yet; this is a constitutional constraint on all future pattern-discovery, factorization-search, or architecture-selection work, including any future G0.BA/G0.F stage. |
| G0.LEX-0 necessary relation is not generative authority (law only) | DECLARED_LAW_ONLY | See **G0.LEX-0 — `NecessaryRelationIsNotGenerativeAuthority`** below. Constitutional scope is GENERAL; runtime enforcement scope is `G0.LEX-0` only (`src/alghanem/arabic/lexical_evidence_specification.py`); global runtime status is `NOT_YET_ESTABLISHED`. No kernel type or gate reads it, and none is added here. |


### G0.C.1 — Minimal claim constitution

- `ClaimCandidate` is a reviewable occurrence of
  `ClaimContentManifest(ClaimCore, qualifications)`, not truth, evidence,
  knowledge, or a license.
- For the declared structured-claim distinction target, no-weaker projection
  collisions prove `anchor`, opaque `PredicateRef`, `polarity`, and `scope` are
  necessary in `ClaimCore`; broader semantic minimality remains
  `DECLARED_DEFERRED`.
- Predicate rendering and semantics are deferred; text is not claim input or
  primary identity.
- `CanonicalClaimContentEncoder` is the sole public issuer of
  `ClaimContentIdentity` through the controlled canonical-encoder API. Coverage
  guards fail closed for every field of `ClaimContentManifest`, `ClaimCore`,
  `Anchor`, `PredicateRef`, `ClaimScopeRef`, and `ClaimQualification`.
- Qualification tuple order is content-significant
  (`NoUnlicensedQualificationCommutation`); scope and polarity are encoded
  content.
- `ClaimOccurrenceRef != ClaimOccurrenceIdentity`: it is a reusable local
  reference; portable occurrence identity is `DECLARED_DEFERRED`.
- Legacy `Claim(claim_id, statement)`/`ClaimEvidenceBinding` remains separate;
  its claim-id equality is not G0.EB.1 evidence binding.
- `ClaimCandidate` has no evidence or evidence-binding field; claim-specific
  evidence binding is deferred to G0.EB.1.

### G0.OB.1 — Authenticated-observation bridge

- `AuthenticationIdentifier != AuthenticationCertificate`: strings naming an
  observation and its authentication never constitute an authenticated
  observation.
- `AuthenticatedObservationBinding` is issued only through a private,
  source-agnostic kernel bridge. A source-specific authority must invoke that
  internal bridge only after issuing its own authenticated
  observation. The G0.SO.1 repository adapter is
  `RepositoryObservationRun.bridge_authenticated_fragment`, which accepts only
  its own authority-issued `AuthenticatedRepositoryFragment`.
- The bridge is absent from the public kernel API. This establishes
  `NoPublicCallerIssuancePath` as a controlled Python API boundary, not
  cryptographic impossibility of forgery.
- The kernel imports no source-layer type. Repository-source coordinates use
  canonical JSON over every declared field, so delimiter-bearing values cannot
  collapse distinct provenance tuples. A binding is a
  `SourceBoundAuthenticatedCoordinate`, not a portable identity:
  `PortableAuthenticatedObservationIdentity = DECLARED_DEFERRED` until an
  issuer-scope identity is explicitly propagated.

### G0.EB.1 — Claim-relative evidence-role constitution

- `EvidenceRoleCandidate(AuthenticatedObservationBinding, ClaimCandidate,
  EvidenceRoleRef)` is a proposed evidence role. `EvidenceRoleRef` is opaque:
  `EvidenceRoleRef != EvidenceRoleSemantics != EvidenceApplicability`.
- Projection collisions prove the three coordinates are necessary for the
  declared distinction target: deleting observation, claim, or role collapses
  distinct candidates. This is
  `EvidenceRoleCandidateCoreMinimality`, not a claim of semantic minimality.
- `EvidenceRoleCandidate != EvidenceApplicability`: it does not assert that
  the observation is evidence or that the proposed role applies.
- `LegacyEvidence != EvidenceRoleCandidate`: legacy `Evidence(claim_id, basis)`
  and `ClaimEvidenceBinding` remain a separate claim-id system and never issue
  or substitute for a G0.EB.1 candidate.
- `EvidenceApplicability != EvidenceSufficiency`,
  `EvidenceSufficiency != Truth`, and `TruthAssessment != Knowledge` remain
  outside this milestone. `EvidenceRoleCandidate` has no fields for any of
  those judgments.

### G0.EA.1 — Evidence applicability assessment

- `ApplicabilityAssessmentGate` consumes an existing
  `EvidenceRoleCandidate`; it does not create or alter an observation, claim,
  or role.
- `EvidenceApplicabilityAssessment` is limited to `PASS`, `BLOCK`, or `DEFER`
  for the candidate's claim scope, and preserves a reason, trace, and
  residuals, plus the content identity of its specification and the snapshot
  identity of its sealed evaluator registry. `PASS` carries no unresolved
  residuals; `DEFER` carries at least one.
- Applicability models are content-bound to authority-issued evaluator
  bindings, including evaluator implementation identity, candidate role, and
  claim scope. A caller-supplied callable is not a frozen applicability
  semantics. The gate validates that the weakening graph is well-formed and
  acyclic.
- Models are competing closure models ordered by their declared weaker-model
  relation. The result is `PASS` when the weakest declared model that closes
  applicability passes; a stronger unresolved model cannot override it. If no
  model closes, a licensed block yields `BLOCK`, otherwise unresolved residuals
  yield `DEFER`.
- No anchor, scope, role, or provenance checklist is born as a primitive
  without a declared, authorized model and its residual boundary.
- The assessment does not assert evidence sufficiency, truth, licensed-claim
  status, or knowledge. A `DEFER` result is an unresolved applicability
  boundary, not a negative truth judgment.

Invariant assessment request semantics are closed at the gate: `BLOCK` means an
authorized verifier observed at least one invariant as false; `DEFER` means no
invariant was false but at least one could not be checked; and `VERIFIED` means
every declared component was checked and preserved. Missing, extra, or duplicate
specifications are malformed requests and raise
`InvariantAssessmentSpecificationError`; they produce no epistemic decision and
must not be recorded as failed components.

At Kernel v0.1, an operation's target domain is declared structural metadata
only; it does not grant transition or domain-transition authority. Source and
target domains may differ; whether they must coincide is a licensing question
deferred beyond Kernel v0.1.

Structural admission is not full licensing. `StructuralAdmissionGate` proves
only that a transition is well-formed under the laws above; it does not prove
evidential sufficiency, cross-domain authority, or inter-layer authority.
Those remain declared-deferred laws, and a future `LicensedTransition` — issued
only once those gates exist — must not be assumed to already exist because a
transition is structurally admissible.

Kernel v0.1's epistemic ladder, current rung marked with `*`:

```
Representable (TransitionCandidate) -> *StructurallyAdmissible* (StructurallyAdmissibleTransition) -> EvidentiallySupported -> AuthorityLicensed -> Certified (CertifiedTransition)
```

`TransitionKind` names the claim a candidate makes (what it is *representing*);
`StructurallyAdmissibleTransition` certifies only that the claim is
well-formed under structural laws. `StructuralAdmissionGate` evaluates candidates
to produce `StructuralAdmissionDecision`s (`ADMITTED`, `BLOCK`, `DEFER`, `UNDEFINED`).
Evidential sufficiency (`EvidentiallySupportedTransition`), authority to license a
transition (`AuthorityLicensedTransition`), and final certification
(`CertifiedTransition` carrying `CertifiedOutcome`) are later rungs, deferred
beyond Kernel v0.1. A linguistic layer (for example, a future Carrier/J
adapter) must be built as a client that produces evidence and invariant
claims for this kernel to structurally admit; it must not be granted
certification the kernel itself does not yet issue.

Kernel dataclasses are shallowly immutable: field reassignment is blocked, but
payload objects stored in `State.value` and `OperationResult.value` are not
deep-frozen by the kernel.

Canonical manifests are independent snapshots: mutation of a shallow payload
after encoding cannot alter existing canonical bytes, but a later encoding may
produce a different content digest for the same admission occurrence.

The kernel does not assume reversibility, global composition, path
independence, a group, or a groupoid. Those questions are intentionally
deferred until later milestones.

## G−1 — Pre-Algebraic Conditions of Intelligibility (law-only)

This milestone declares one constitutional boundary question:

```
What must be true before the first algebraic representation is even possible?
```

Intelligibility here carries no post-algebraic licensing, evidence, rank,
truth, or authority semantics.

It is law-only and boundary-only. It introduces no runtime, class, enum, gate,
evidence machinery, residual machinery, algebra primitive, or learning
architecture.

| Law | Status | Scope |
| --- | --- | --- |
| `NoTotalAlgebraicSelfBootstrap` | DECLARED_DEFERRED | The first algebraic representation may not be the complete ground of its own possibility. `NoTotalSelfBootstrap` is required; `RecursiveSelfExtensionAllowed` is explicitly preserved for later stages (`A_n -> A_{n+1}` is allowed). |
| `PreAlgebraicEnablingConditionIsNotOrganizedPriorContent` | DECLARED_DEFERRED | `E_-1 != P_0`. Pre-algebraic enabling conditions are not the same object as organized prior content. `ConditionOfPossibility != OrganizedPriorContent`. |
| `PriorAvailabilityIsNotPriorAuthority` | DECLARED_DEFERRED | `PriorAvailability != PriorAuthority` and `PriorInformation != PriorJudgment`. Availability for possible binding does not license truth, correctness, or judgment authority. |
| `PreAlgebraicIntelligibilityIsNotPostAlgebraicLicense` | DECLARED_DEFERRED | Any first differentiation/binding step at this boundary is an intelligibility/usability candidate only, not a post-algebraic licensing-authority act. |
| `FirstAlgebraRepresentabilityIsNotG0Birth` | DECLARED_DEFERRED | `FirstAlgebraRepresentability != G0Birth`. The representability boundary question must not be collapsed into post-algebraic birth authority semantics. |
| `NoHiddenEncyclopediaInFoundation` | DECLARED_DEFERRED | Foundation cannot be treated as a hidden finished inventory of truths. Availability of prior structure does not imply pre-certified knowledge. |
| `DifferenceCandidateIsNotCertifiedResidual` | DECLARED_DEFERRED | `DifferenceCandidate != CertifiedResidual`. A certified residual requires reconstruction/comparison capacity and explicit scope; before that, only candidates exist. |
| `NoResidualBeforeReconstructionCapacity` | DECLARED_DEFERRED | `Observed + Reconstructed + Comparator + Scope -> ResidualCandidate`. Therefore no residual is licensed before reconstruction capacity exists. |
| `NoPrematureGMinus1PrimitivePromotion` | DECLARED_DEFERRED | Evidence, Rank, Closure, and Residual are not G−1 primitives and must not be installed as foundational atoms at this stage. |
| `GenesisIsNotRetrospectiveReconstruction` | DECLARED_DEFERRED | `Genesis != RetrospectiveReconstruction` and `RetrospectiveFormalization != HistoricalGeneration`. Later formal reconstruction can describe prior conditions but does not historically generate them. |
| `ConditionOfPossibilityIsNotTruthGuarantee` | DECLARED_DEFERRED | `ConditionOfPossibility != TruthGuarantee`. Being necessary for intelligible start does not certify truth-status of the content. |
| `FoundationalInventoryOpen` | DECLARED_DEFERRED | `FoundationalInventory = OPEN` at the level of exact internal factorization. `NecessityOfUsablePriorInformationRelatedToReality = FOUNDATIONAL_GIVEN`, but no exact or partially closed three-factor ontology is frozen at G−1. `RetrospectiveMinimalityAudit != FoundationalGeneration`. |
| `NoPreAlgebraicUseOfPostAlgebraicProofMachinery` | DECLARED_DEFERRED | Later algebra may retrospectively audit G−1 boundary commitments, but post-algebraic proof machinery may not be used to retroactively generate G−1 itself. |
| `EpistemicPrecedenceIsNotFileOrderOrImplementationChronology` | DECLARED_DEFERRED | `EpistemicPrecedence != FileOrder != ImplementationChronology`. Existing G0+ laws/runtime are not invalidated or rewritten; G−1 states prior conditions they presuppose, not historical implementation order. |
| `NoClosedOPI0TupleAtGMinus1` | DECLARED_DEFERRED | If `OPI_0` is referenced, it is only a provisional analytical name. It must not be frozen here as a closed tuple, ontology identity, birth-certified object, rank, or evidence-certified status. |

The declared epistemic ordering is:

```
E_-1 -> P_0^{given} -> Encounter -> FirstIntelligibleDifferentiationOrBindingCandidate
    -> StableRepeatableRegularityCandidate
    -> CaseBoundDescriptionInsufficientCandidate
    -> ParticularInstanceIdentityInsufficientCandidate
    -> RepresentativeIndependentStructuralDeterminationCandidate
    -> ?

? = FirstAlgebraRepresentabilityCriterionNotYetDerived
```

PR47 is an open-audit boundary update only: it records falsifiable pressure
toward first algebra representability while leaving
`FirstAlgebraRepresentabilityCriterionNotYetDerived` explicitly unresolved.

Only after representational birth, recurrence is evidence-mode typed:

```
P_n + Q_{n+1} + EvidenceMode_{n+1} -> DemandAssessment

D_{n+1} =
  EMPIRICAL -> Demand(EMPIRICAL), as defined by G0.MA
  FORMAL    -> Demand(FORMAL), as defined by G0.MA
  MIXED     -> Demand(MIXED), as defined by G0.MA

D_{n+1} -> MinimalSatisfyingExtension? -> Birth? -> Freeze -> P_{n+1}
```

Mode-specific demand routes:

```
EMPIRICAL: Observation -> Reconstruction -> Difference -> CertifiedResidualGeometry
FORMAL:    FormalQuestion -> ExhaustiveNecessityProof -> CertifiedFormalNecessityWitness
MIXED:     EMPIRICAL and FORMAL tracks both required; neither substitutes for the other
```

### ClosedClaims

- G−1 is declared as pre-algebraic boundary law only.
- `ClosedClaims` at G−1 means constitutionally fixed boundary commitments for
  this milestone only; it is not runtime proof or runtime enforcement status.
- `ClosedAtConstitutionalBoundary != PROVED != ENFORCED`.
- Total algebraic self-bootstrap is disallowed, while later recursive
  self-extension is allowed.
- `E_-1 != P_0`, and `ConditionOfPossibility != TruthGuarantee`.
- `DifferenceCandidate != CertifiedResidual`; no residual before reconstruction
  capacity.
- `AlgebraRepresentability != AlgebraNecessity`.
- `FirstAlgebraRepresentability != G0Birth`.
- `RepresentabilityCandidate != LicensedAlgebraBirth`.
- `RepresentabilityPressure != RepresentabilityProof`.
- `OpenAuditUpdate != CriterionClosure`.
- Post-algebraic recurrence remains mode-typed (`EMPIRICAL/FORMAL/MIXED`) and
  is not reduced to residual-only flow.
- G0+ remains valid in implementation; G−1 asserts epistemic precedence only.

### UnprovedClaims

- Exact functional/internal factorization of `P_0`.
- Final foundational inventory membership and cardinality.
- Any proof that a particular candidate foundational dimension is strictly
  necessary.
- Historical generation path of pre-algebraic conditions.

### SourceAttestedPriorDimensions

- `NecessityOfUsablePriorInformationRelatedToReality = FOUNDATIONAL_GIVEN`.
- `SourceAttestedPriorDimensions ⊇ {ThingDirectedInformation,
  RealityOrWhatTheThingIsDirectedInformation, PropertyDirectedInformation}`.
- `ExactFactorization(P_0) = OPEN`.
- `PriorAvailability != PriorAuthority`.
- `PriorInformation != PriorJudgment`.
- `ConditionOfPossibility != TruthGuarantee`.
- `NoHiddenEncyclopediaInFoundation`.

These are boundary commitments, not a frozen ontology or closed primitive tuple.

### ResolvedAuditQuestions (lineage preserved)

- `PreAlgebraicLicensingVocabularyUnresolved`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: `PreAlgebraicIntelligibilityIsNotPostAlgebraicLicense`
- `GMinus1PostAlgebraicRecurrenceEvidenceModeMismatch`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: evidence-mode typed recurrence with
    `Demand(EvidenceMode) as defined by G0.MA`.
- `ClosedClaimsStatusSemanticsAmbiguous`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: `ClosedAtConstitutionalBoundary != PROVED != ENFORCED`.
- `PostAlgebraicAuditMustNotBecomeFoundationalGenerator`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: `NoPreAlgebraicUseOfPostAlgebraicProofMachinery`.

### OpenAuditQuestions

- `OrganizedPriorContentBoundaryNotDerived`: exact boundary between `E_-1` and
  organized prior content is not yet fully derived.
- `FirstAlgebraRepresentabilityCriterionNotDerived`: the criterion that upgrades
  stable repeatable regularity to first algebra representability remains open.
- `P0FunctionalMinimalityNotAudited`
  - Status: `DEFERRED_UNTIL_POSTALGEBRAIC_RETROSPECTIVE_AUDIT`
  - Note: prior-information necessity is given; minimal internal/functional
    factorization remains open.
- `ThirdTransmittedEvidenceModeNotDecided`
  - Status: `OPEN`
  - Question: is there a third, transmission-based evidence path independent of
    `EMPIRICAL` and `FORMAL`, in which a claim rests on *what was transmitted or
    reported* rather than on a measured residual or an exhaustive formal proof?
  - Standing evidence: the only concrete support currently in this repository is
    empirical, not theoretical, and it is named card by card rather than by any
    "two of three" generality. `maa_2_197.yaml` declares "خلاف نحوي مُسجَّل"
    and `imran_3_33.yaml` declares "تنازع مُسجَّل": both are records of a
    *disagreement between sources*, not derivations from a text, and they fit
    neither `EMPIRICAL` (no measurement run) nor `FORMAL` (no exhaustive proof
    over a closed domain). `man_2_255.yaml` is explicitly *not* of that kind:
    its witness ("وجود (ذا) بعد (من) قرينة نحوية تقليدية على الاستفهام") is a
    traditional grammatical clue about the text itself, not a transmitted
    disagreement. `hadhan_20_63.yaml` (طه:63) declares five witnesses, each
    naming its own grammarian (الطبري نقلًا عن لغة بلحارث بن كعب، أبو عمرو بن
    العلاء ورفض الزجّاج له، قراءة عاصم والخليل، مذهب كنانة، والشاذ الآحاد عن
    أُبَيّ بن كعب والخليل); these too are records of transmitted disagreement.
    Only those cards, named individually, stand behind this question.
  - Measured standing: `عدد_الشواهد` is no longer uniform. It is `1` on
    `man_2_255.yaml`, `maa_2_197.yaml`, and `imran_3_33.yaml`, and `5` on
    `hadhan_20_63.yaml`. This records a change in measurement only; it is not
    an upgrade of this question, which stays `OPEN`. A larger count is still a
    count of declared text: `DeclaredWitness != AssessedEvidence` still holds,
    the auditor does not read the *kind* of a witness's source, classifying
    witnesses remains out of scope, and multiplicity of named transmitters is
    not itself evidence that a third transmission-based `EvidenceMode` exists.
    The richer card also defers exactly like the other three, so nothing in the
    reported outcome distinguishes it.
  - Not decided here: this question is recorded, not answered. Status remains
    `OPEN`. `EvidenceMode` is unchanged, and `evidence_requirements` is part of
    frozen experiment content identity, so no mode may be added without a
    dedicated milestone that addresses that content-identity impact.
- `DeclaredVersusDerivedRecurrenceNotExplained`
  - Status: `OBSERVED_NOT_EXPLAINED`
  - Observation: the shape "a caller/card *declares* something; an authority
    *derives* or *verifies* it independently; the declaration never becomes the
    verified thing" recurs across this repository well beyond the four sites it
    was first noticed at. Located by search, not by recollection:
    `DeclaredInvariant != VerifiedInvariant`
    (`kernel/transition.py:86`, `kernel/invariant.py:4`),
    `ClaimedInvariant != VerifiedInvariant` (`kernel/invariant.py:313`),
    an `InvariantSpec.extractor_id` as "only a claim, not a grant of authority"
    with `Candidate/Caller does not own verifier selection authority`
    (`kernel/invariant.py:148`, `kernel/invariant.py:183`,
    `kernel/invariant.py:861`), gate-issued-only verification decisions and
    bundles that a caller cannot hand-build, `Candidate != Decision` and
    `AnchorEquality != ProvenIdentityPreservation`
    (`kernel/transition.py:83`), `DeclaredEvaluatorId != AuthorizedEvaluator`
    with `CallerDoesNotOwnEvaluatorAuthority`,
    `AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment` and
    `EvidenceAttachedToRecord != EvaluatorExecutedOnEvidence`
    (`kernel/evaluator_execution.py:41`, `kernel/evaluator_execution.py:257`),
    `DeclaredImplementationId != ImplementationContentIdentity`,
    `AuthorizedCapture != ProofOfExternalAcquisitionChronology` and
    `AuthorizedEvidence != SufficientEvidence`
    (`kernel/evidence_acquisition.py:19-22`),
    `ConstructibleContract != IssuedByAuthority` /
    `WellFormedFrozenFactorRef != AuthorityIssuedFrozenFactorRef`
    (`kernel/fractal.py:31-32`), `SameId != SameSemantics` /
    `ResidualDefinitionId != ResidualDefinitionContentIdentity`
    (`kernel/birth_content_identity.py:1`,
    `kernel/birth_content_identity.py:11`), the refusal of a caller-declared
    weaker cone (`arabic/external_audit.py:231`), and
    `DeclaredWitness != AssessedEvidence` (`arabic/external_audit.py:194`).
  - Two distinct sub-shapes, not one: in some sites the declaration is *checked
    against* the derived value and a mismatch is rejected outright (unauthorized
    `extractor_id`, caller-declared weaker cone, content drift under
    `SameId != SameSemantics`); in others the declaration is merely *carried and
    reported* with no authority ever attached to it (`DeclaredWitness`,
    `DeclaredImplementationId`, `AuthorizedEvidence != SufficientEvidence`).
    Whether these are one structure or two is not decided here.
  - Not a law and not named: this entry records a recurrence, nothing more. No
    law, type, base class, shared abstraction, or general name is created for
    it, and none may be introduced on the strength of this observation alone.
    A recurrence of phrasing is not proof of a shared underlying structure; the
    recurrence itself is what has yet to be explained.
- `NisbahSortBelongsToSchemaOrSpecificationNotDecided`
  - Status: `OPEN`
  - Question: the text deposited at `G0.NSB-0` proposes that `TermAnchor`,
    `Predicate`, `Operator`, `ArgumentSlot`, `Nisbah`, `Constraint` and
    `RelationalClosure` become sorts of the meta-algebra alongside `Layer`,
    `Transition` and `Realization`. Are they sorts of `Σ_M` — part of what it
    *means* to be a linguistic structure — or structures of a particular `Σ_A`
    written in that language?
  - Two distinct sub-shapes, not one: the deposit answers neither branch and
    refuses the pair as a false dichotomy, opening a third level `Σ_L` between
    them under `ThreeLevelsAreNotTwo`. So two questions are folded here under
    one name: the original either/or, which the deposit declines, and the third
    level's own warrant, which is untested. `Σ_L` earns its place only if the
    registered negative controls, once run on a named held-out corpus, are not
    tied by a weaker representation.
  - Note: `A_SCHEMA_IS_NOT_A_SPECIFICATION`
    forbids a particular theory inside the language of the algebra, and a
    schema carrying one instance is a schema that has turned into a theory whose
    shape then constrains every theory written after it. Admitting these sorts
    on the strength of a text nobody has tested would do exactly that, so the
    question cannot be settled by preference.
  - Standing evidence: none either way. `Carrier/State` is a sort-level
    commitment that survived a preregistered negative control in `G0.FLT-1.Q`
    and produced a mixed first reading; the nisbah nucleus has produced no
    reading at all. Its negative controls are now registered and frozen, and
    every one of them is held unrunnable until a held-out corpus is named, so
    the registration adds no evidence on either branch.
  - Not decided here: this question is recorded, not answered.
    `META_ALGEBRA_SCHEMA` keeps its four sorts and its digest, no sort is added,
    and no authority in this repository may add one on the strength of this
    entry. `Σ_L` is a separate nucleus built on the digest of `Σ_M` and sharing
    no sort name with it; standing beside the meta-algebra is not entering it.

### TheoreticalProgramBeforePostAlgebraicAudit

This section freezes the *question form* for the next theoretical stage. It
does not claim completion of derivation, minimality, or closure.

- `NecessityOfUsablePriorInformationRelatedToReality = FOUNDATIONAL_GIVEN`.
- `ExactFactorization(P_0) = OPEN`.
- `FirstAlgebraRepresentabilityCriterionNotDerived` remains open.

The immediate target is to separate three layers that must not be conflated:

- `PriorContent`: what is already present in prior information.
- `PriorAvailability`: what makes that prior content retrievable and usable.
- `RealityBindingCapacity`: what makes usable prior content connectable to new
  encountered reality.

Boundary law for this stage:

- `PriorContent != PriorAvailability`.
- `PriorAvailability != RealityBindingCapacity`.
- No item is declared primitive only because it appears early in explanation.

Central open question (theoretical, not yet a derived criterion):

- What is the minimal set of preconditions under which first intelligibility is
  possible at all?

Audit-position clarification:

- Philosophical/theoretical analysis of candidate preconditions is allowed now.
- Proof that a candidate set is minimal and irreducible remains
  `DEFERRED_UNTIL_POSTALGEBRAIC_RETROSPECTIVE_AUDIT`.

### First Algebra Representability — Falsifiable Boundary Candidate

This subsection stays inside G−1 and remains boundary-law only.

It does not claim that algebra is born, nor that a fully unified regularity or algebraic
element has already been derived.

Target form for this stage:

```
StableRepeatableRegularityCandidate
  -> CaseBoundDescriptionInsufficientCandidate
  -> ParticularInstanceIdentityInsufficientCandidate
  -> RepresentativeIndependentStructuralDeterminationCandidate
  -> FirstAlgebraRepresentabilityCriterionNotYetDerived
```

Interpretive boundary for this target form:

- Re-identifiable regularity across differentiated cases can pressure a
  representation demand.
- `CaseBoundDescriptionInsufficientCandidate != FirstAlgebraRepresentability`.
- `ParticularInstanceIdentityInsufficientCandidate != FirstAlgebraRepresentability`.
- `RepresentativeIndependentStructuralDeterminationCandidate != FirstAlgebraRepresentability`.
- Pressure toward representation is not completed representation.
- The candidate pressure is: identity of the revealing instance is insufficient
  to determine the result; structural determination must survive across
  independently differentiated representatives.

Conservative non-equivalence guards:

- `Repetition != FirstAlgebraicRepresentation`.
- `Similarity != ProvenSingleRegularity`.
- `RepeatableRegularity != IndependentRepresentationOfThatRegularity`.
- `CrossCaseReIdentification != ProvenUnifiedRegularity`.
- `CaseBoundDescription != RepresentativeIndependentStructuralDetermination`.
- `DependenceOnParticularInstanceIdentity != FirstAlgebraRepresentability`.
- `TrivialOneExampleAbstraction != FirstAlgebraRepresentability`.
- `NeedForHigherRepresentation != AchievedHigherRepresentation`.
- `AlgebraRepresentability != AlgebraNecessity`.
- `FirstAlgebraRepresentability != G0Birth`.
- `RepresentabilityCandidate != LicensedAlgebraBirth`.

Refutation-question matrix (questioning only; no final derivation here):

Rows for prior persistence, binding capacity, and linguistic-carrier analysis
belong to first-intelligibility/language sections, not this algebra
representability boundary subsection.

| Explanatory candidate | Piercing question |
| --- | --- |
| Repetition-only candidate | Can mere repetition, with no unified regularity claim, explain the observed invariance? |
| Similarity-only candidate | Can loose similarity explain the observations without one structurally unified regularity? |
| Case-bound description candidate | Can a strictly case-bound description preserve what repeats across differentiated cases? |
| Particular-instance-identity dependence candidate | If representative identity is changed while structural role-pattern is preserved, does determination collapse? |
| Structural nondeterminacy candidate | Can the same role-pattern map to incompatible determinations without violating the candidate boundary? |
| Trivial one-example abstraction candidate | Can a one-example or one-representative abstraction stand without independent differentiated support? |

Matrix output constraint:

- Failure of a weaker explanatory model yields only
  `CandidateNecessityForFurtherAudit`.
- It does not yield a necessity certificate at G−1.
- Minimality and irreducibility remain
  `DEFERRED_UNTIL_POSTALGEBRAIC_RETROSPECTIVE_AUDIT`.
- No-weaker closure, independent validation, reconstruction, and birth authority
  remain later/post-algebraic audit questions.

### ForbiddenNextJumps

- Do not introduce runtime/classes/enums/gates/evaluator machinery under G−1.
- Do not treat Evidence, Rank, Closure, or Residual as G−1 primitives.
- Do not close `OPI_0` into a fixed tuple or ontology identity.
- Do not reinterpret retrospective formalization as historical generation.
- Do not claim G−1 rewrites or invalidates existing G0/G0.MA/G0.F/BA/BV/RC law.

## G0.N — Knot ontology of the carrier (law-only)

This milestone declares one ontological commitment about what a carrier *is*,
ahead of any runtime that could issue one:

```
Carrier != DiscoveredEssence
Carrier  = KnotTiedOnAFiberOfRegularity
```

A carrier is not an essence that was latent in the material and finally
found. It is a knot tied, by convention and justified statistically or
formally, at a point on a continuous fiber of regularity — the one point that
survived every weaker model licensed and frozen for that experiment. Nothing
below promotes that convention into a discovery, and nothing below weakens it
into an arbitrary choice: a knot is licensed exactly by what it survived.

The structural consequence is about `Freeze`, and it is stated here rather
than left to be noticed later. Freezing does not fix a final essence; it
fixes a knot *at one version of the fiber* — one tool, one corpus, one
moment. Reopening when the fiber changes is therefore not a contradiction of
the earlier freeze but the condition of the knot's continuity, which is why
this section binds itself to the existing `G0.F.1` reopen protocol instead of
forking a parallel one.

| Law | Status | Scope |
| --- | --- | --- |
| `KnotNotEssence` | DECLARED_DEFERRED | A carrier is a conventional knot tied at a point that survived every licensed, frozen weaker model for its own experiment, never an essence that pre-existed the experiment and was uncovered by it. `SurvivedEveryLicensedWeakerModel` is the whole warrant for the knot; no separate act of recognition, intuition, or traditional naming adds anything to it, and `TraditionalName` remains strictly posterior per `NamingIsPosterior` below in G0. |
| `FreezeIsFiberVersionScoped` | DECLARED_DEFERRED | `Freeze(K)` fixes a knot at one declared version of the fiber (tool identity, corpus, normalization policy, Unicode database version), never an essence independent of that version. Consequently reopening `K` when the fiber version changes is required rather than merely permitted, and is not a defect of the earlier freeze. This composes `G0.F.1`'s `ReopenDoesNotRebirth` and `RevisionDoesNotEraseHistoricalFreeze` and forks neither: a fiber-version change opens a new revision on `K` itself and leaves the historical frozen record intact. |
| `NodeContinuityIsContentNotOccurrence` | DECLARED_DEFERRED | Two results separated in time or tool version may be read as *the same carrier* only if their content identity matches. Name equality is never sufficient, and occurrence identity is never sufficient: `admission_id` fingerprints that an execution happened, not which phenomenon it was about. `TransitionContentIdentity` and `OCCURRENCE_ONLY_EXCLUSIONS` (`src/alghanem/kernel/content_identity.py`) already enforce the exclusion half of this law — an occurrence field cannot enter a content identity — but the comparison half, deciding that two content identities produced under two tool versions name one knot, is issued by no authority in this repository and is not implied by digest equality alone. |
| `NoIntentProjection` | DECLARED_DEFERRED | No candidate's meaning may be settled by (a) the intent of whoever originally laid down the phenomenon, or (b) the intent of the researcher running the experiment. The only admissible meaning is what a surviving residual forces after every weaker model licensed and frozen *for that experiment* has been exhausted. `NoLabelLeak` (case a) and `NoOracleTuningBeforeFreeze` (case b) are two applications of this one origin, not two independent prohibitions, and neither is weakened by the other's satisfaction. |
| `ExistenceIsBinaryRankIsGraded` | DECLARED_DEFERRED | Two different questions may not share one verdict type. Whether a thing exists at all is binary and ungraded, and corresponds to `StructuralDecisionStatus` as a purely logical judgement. How well a judgement about a thing's attributes matches reality is graded by strength of evidence, and corresponds to whatever lower-confidence-bound, z-score, or p-value machinery a later measurement layer supplies. No such rank machinery exists in this repository today, so this law is declared over a codomain that is not yet constructible here. |
| `RankNeverCertifiesEssence` | DECLARED_DEFERRED | A rank may reach any height and still remain a measurement of the strength of presumptive evidence about an attribute. It never converts into the binary existence judgement, and never certifies an essence. Retractions of high-rank results are therefore structural rather than accidental: those results answered attribute questions, which stay presumptive at every rank. |
| `CompleteInductionIsCorpusBounded` | DECLARED_DEFERRED | Exhaustive enumeration over a closed finite set yields certainty *inside that set only*. A `PASS` over a complete corpus must be stated as established within that corpus and presumptive beyond it until a second independent corpus is enumerated. Direct generalization from one closed corpus to the open language it is drawn from is refused by name, not softened by hedging prose. |
| `NoBedrockWithoutRecurringDirayaSurvival` | DECLARED_DEFERRED | Ontological and epistemological scrutiny is a continuing process, not a gate passed once. Every independent new application — another corpus, another tool, another scope — is a fresh occasion to fail. Repeated survivals never fix the framework as bedrock; they license only the reading that it has not been defeated yet. |
| `TawaturRequiresDiachronicSuccession` | DECLARED_DEFERRED | `متواتر` presupposes succession *through time*: independent witnesses arriving in successive, temporally separated cycles. A closed corpus is a frozen synchronic section — one fixed text that neither grows nor renews — and therefore carries no temporal dimension in which succession could occur at all. Asking whether a finding over such a corpus is `متواتر` is therefore a category mismatch, ill-posed in the manner of asking whether the number five is univocal or equivocal, and not a question left unanswered until some future measuring authority arrives. The consequence is stated in this precise form and no wider: the obstacle to *earning* `متواتر` inside this repository is the structure of the evidence base, not the absence of a tool, so no future authority over closed corpora removes it — while the obstacle to *verifying* a genuinely diachronic transmission remains ordinary missing authority, held under `NoReachingWrite != ProvenUnreachable` like any other hold. The temporal structure a hold is derived *from* is itself derived, never passed in: a base is a frozen synchronic section only when its closure binding is re-derived by byte-exact rematch of its own full enumeration through the authority-free canonical content primitive, so an unenumerable base proves no closure. That derivation is necessarily asymmetric and partial: `DIACHRONIC_INDEPENDENT_SUCCESSION` is never derived from any descriptor, because proving succession is precisely the temporal authority this repository lacks, and deriving it would invert `NoReachingWrite != ProvenUnreachable` under the appearance of repair. Nor may its absence be inferred: "not a proven frozen closure" does not entail "therefore a genuine succession", so a failed closure proof yields `TEMPORAL_STRUCTURE_NOT_SETTLED` and an unsettled genus, never the nearer of the two. One level of the regress is removed and no more: the enumeration itself remains caller-declared, and what changed is that the declaration is now a structural claim rematched byte for byte rather than a temporal verdict nothing could check. This law neither grants nor withholds any exemption resting on recurrence; `FIRST_ORGANIZED_INFORMATION_QUESTION` stays open with all three of its hypotheses. |

This section is law-only and boundary-only, in the manner of `G−1` above. It
introduces no runtime, class, enum, gate, rank primitive, or continuity
authority, and it neither invalidates nor rewrites any existing G0, G0.MA,
G0.F, G0.BA, G0.BV, or G0.IC law. In particular it issues no
`CarrierNodeContinuityReading`: deciding that two frozen results name one knot
across two tool versions is exactly the authority this repository does not
have, and declaring the law is not exercising it.

## G0.W — The decision chain: wad, umum/khusus, and the chain ledger

This milestone builds three Arabic-layer modules for the fourth, tenth, and
framing positions of the decision chain that runs from an identity-free
codepoint to a concept grounded in sense. It adds no kernel authority: none of
the three imports anything from `kernel/`, none is read by anything in it, and
none issues a birth, a `Freeze`, or an `E0`.

The founding correction is stated as law rather than left in prose. Language is
laid down by human beings and not by God: neither revelation (a vicious circle,
since revelation is itself understood only through a language prior to it) nor
necessary knowledge (which would entail necessary knowledge of God, contrary to
observed fact) is a path to it. `وعلَّم آدم الأسماء` is therefore the teaching
of the *realities and properties of things* — a direct concept in the sense of
`ContentStanding.مفهوم` — not the teaching of lexemes. The consequence is the
one that matters structurally: because the laying-down is a purely human,
historically contingent event, it is knowable only by transmission — not
because it is sacred, but because nothing else reaches a past convention.

| Law | Status | Scope |
| --- | --- | --- |
| `WadIsHumanNotDivine` | ENFORCED_AT_WAD_NAQL | `WadOrigin` is a closed two-member vocabulary and `وضع_بشري` is **derived from an exhausted two-part refutation, never declared in a field**: a `TawqifRefutation` must carry both `لا_طريق_بالوحي` and `لا_طريق_بعلم_ضروري`, each with an excerpt quoted verbatim from the one named source and checked by containment (`src/alghanem/arabic/wad_naql.py`). One ground alone leaves the other possibility standing, so a single-ground refutation fails at construction rather than producing a warning. The rejected reading of `وعلَّم آدم الأسماء` as lexemes is a named member of `AdamTeachingReading` refused by the source's own words, not a silent absence. `HumanWad != ArbitraryChoice`: a human convention is a collective settlement that actually occurred, transmitted as it occurred and not invented as one wishes. |
| `WadKnownOnlyByNaql` | ENFORCED_AT_WAD_NAQL | A `WadRecord` — the pairing of one `لفظ` with one `مدلول` — carries its path of knowledge only as a `TransmissionStanding` (متواتر/آحاد/فرض), imported rather than copied, and `known_only_by_naql` is structural rather than optional. The two refused paths are refused by name and by construction: `refuse_derivation` always raises for `استنباط_من_التحليل_التوزيعي` and `استنباط_من_تحليل_المدلول`, because link 3a knows only relations among carriers and states and link 3b knows no particular lexeme at all. `Naql != Sanctity`. |
| `DistributionalTraceIsNotWadPath` | ENFORCED_AT_WAD_NAQL | The trace of a convention is not the path to knowing it, and neither statement corrects the other. `ONLY_LEGITIMATE_TARGET_NOTE` in `maluma_mafhum` describes a real distributional regularity left by a settled convention and stands unchanged; what it may not do is yield *which* lexeme was paired with *which* meaning, since an equivalent regularity can arise from incidental repetition or sample bias. `DistributionalCorroboration` is therefore constructible only over an already transmitted `WadRecord`, its `function` is fixed at `يرفع_دراية`, and `transmission_after_corroboration` returns the prior standing unchanged: statistics raise diraya and never manufacture riwaya. |
| `TakhsisIsNotIhmal` | ENFORCED_AT_UMUM_KHUSUS | Specialization is the operation of *both* evidences, never the dropping of one: the specializer operates at its locus and the general remains authoritative beyond it. `TakhsisRegistration` (`src/alghanem/arabic/umum_khusus.py`) holds exactly the general evidence, the specializer, and a named conflict locus; there is no field into which a dropped or outweighed evidence could be written, and an import-time sweep refuses one. The channel of specialization is **derived** from the specializer's own `DalalaChannel` — imported from `mantuq_mafhum_ifada` rather than duplicated — so specializing a general by a `مفهوم` is read off the evidence rather than asserted. A general specializing a general, a specializer that is itself general, an evidence specializing itself, or a specialization with no named locus each fail at construction, the last because the default is difference rather than contradiction (`DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE`). `TakhsisChannel.لا_تخصيص` is a declared member that no derivation from a standing specializer can ever produce. |
| `TafriPathsAreNotMixed` | ENFORCED_AT_UMUM_KHUSUS | A general rule branches onto its individuals and a universal rule branches onto its particulars; the two are distinct paths, not synonyms. `TafriRegistration` derives its path from a closed `RuleGenus` and refuses a declared path that disagrees. `RuleGenus` is deliberately *not* `Universality` from `kulli_juzi_formal`: that vocabulary classifies a single word as كلّي or جزئي on attested evidence, and mapping its `جزئي` onto a general rule would be the very genus confusion this row forbids — a foreign value passed to `tafri_path_of` is refused rather than coerced. |
| `TypeSignificationIsAlwaysMantuq` | ENFORCED_AT_MANTUQ_MAFHUM_IFADA | The eighth link divides signification exhaustively — مطابقة and تضمن are منطوق, التزام is مفهوم, and there is no third — but one thing never falls on the مفهوم side: **the type of the ruling itself**. It is منطوق always, and is never derived by مفهوم موافقة or مخالفة from an accompanying descriptor; only the side qualifications of a ruling are read that way. `SignifiedAspect` (`src/alghanem/arabic/mantuq_mafhum_ifada.py`) names what a reading falls upon — `نوع_الحكم` or `قيد_جانبي` — and `RulingAspectReading` refuses exactly one combination at construction: `نوع_الحكم` read through `DalalaChannel.مفهوم`. The aspect is not a rung in the channel and does not rank منطوق above مفهوم: reading a side qualification by مفهوم stays open. The channel is not rewritten here but read off the held `DalalaRecord`, so it remains derived in one place; and the accompanying descriptor a مفهوم was read from must be named, while a منطوق may carry none, so no مفهوم is attributed to an unnamed وصف. |
| `ChainReachIsDerivedNotCoded` | ENFORCED_AT_DECISION_CHAIN | `decision_chain` reads the fifteen positions of the chain off the tree, and reach is derived by succession rather than from coding alone: each link conditions the next, so a coded link preceded by an unreached one reads `مسبوقة_بحلقة_غير_بالغة` and never `بالغة`. This is what keeps the chain from reading as complete while links 1 and 2 (the carrier, and the (carrier, state) derivative) stay deferred under `KnotNotEssence`. Deferral by law is **declared, not inferred from absence**: a link with no module at all names the constitutional law that defers it, while a link naming a module has its coding read from the tree like any other. The two governing constraints — the idea/method/means test and the seriousness/benefit test — are recorded as the chain's *frame* rather than positions in it, both `مُصرَّح_غير_مُرمَّز`, and no `GoverningConstraint` declaring itself coded is constructible today: constraint (أ) awaits a written universal idea for GFLK, which this repository does not have and which this milestone deliberately does not invent, and constraint (ب) admits only one acceptable test — a complete application to a real word or verse. That test has been run rather than argued: `examples/external_audit/malik_114_2.yaml` (مَلِك، الناس:٢, chosen because the spelling there is undisputed, with the مالك/مَلِك *reading* contest of الفاتحة:٤ excluded by name in the card itself) is driven through links ٤–١٣ by `tests/arabic/test_malik_114_2_card.py`, and the stop is derived from the card's own declared lexical path rather than written into the test: the fourth link, الوضع بالنقل, because `card_transmission_standing` derives no standing at all from a card whose lexical citation structure is `عنوان_واحد_مسطح` — a named title and entry, with no transmitted internal attribution to succeed anything. The stop is no longer read as the textual absence of a `TransmissionStanding` word from a manat-shaped card, which was the earlier reading: the word could be present and the link would still stop, and it can be absent while the link stands up, because the standing is derived from the path and never read off the card's prose. Link ١٢ still stops for its own absent declarations, and the shared root — a card that names its sources without describing how they arrived — is what the two have in common. Links ٥, ٦ and ٧ stand up and are still not read as reached, by the succession rule. The consequence is recorded in the constraint itself rather than in prose: (ب) keeps `مُصرَّح_غير_مُرمَّز` but its gap note now names the blocking link (`APPLICATION_STOPS_AT_THE_FOURTH_LINK_NOTE`), so the two absences are no longer one genus described twice — (أ) lacks a theory nobody has written, (ب) lacks only a traversal that stopped at a named position. No `jiddiya_ifada.py` is created, since a module measuring an incomplete application is the *further stage of the measuring apparatus* that (ب) itself forbids, and no third `GoverningConstraintStanding` member is opened, because a distinction is admitted here only when one side can be derived. The ledger is a reading of the tree and not an authority over it. |
| `FourthLinkAsksForADerivedStandingNotANamedOne` | ENFORCED_AT_WAD_NAQL | **The fourth link does not require `متواتر` by name; it requires that *some* member of `TransmissionStanding` be derivable from the card's own path of transmission.** `WadRecord` accepts any member of the imported vocabulary (متواتر/آحاد/فرض) and `card_traversal.link_four` stands the link up exactly when `card_transmission_standing` returns a member rather than `None`. Requiring `متواتر` by name would make the link unreachable in principle rather than unreached in fact: `متواتر` is a member with no entry on every path in this repository — `derive_standing` yields it only under `SourceIndependence.COLLUSION_IMPOSSIBLE`, `derive_lexical_carriers` fixes independence at `NOT_ESTABLISHED` structurally because transmission from a book is the very thing that defeats impossibility of collusion, and `TransmissionStandingRecord` refuses it outright (`MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE`, `MUTAWATIR_HAS_NO_ENTRY_ON_THIS_PATH_NOTE`). The distinction is load-bearing for what the three cards of PR#97 established: their stop is `REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH` on *their own flat citations*, a card-specific structural category error, and it must not be confused with the separate, general unreachability of `متواتر`. Otherwise the recorded result would be right by coincidence rather than for its stated reason. That the tool itself can pass the fourth link is not asserted but demonstrated by a negative control: `tests/arabic/test_fourth_link_negative_control.py` drives a synthetic, explicitly `test_only` card — no production standing, and deliberately kept out of `examples/external_audit/` so it never enters the audited corpus — whose lexical path carries two named internal attributions, and the link stands up with a derived `آحاد`. Remove one attribution and the same link stops again, so both standing-up and stopping are derived from structure and neither is frozen into the harness. |

## G0 — Birth Protocol (declared law, no runtime gate yet)

The kernel and Arabic layer never introduce a new named object, cardinality,
or ontology term because it is convenient, expected, or traditional. A
candidate object is only permitted to be *born* — closed independently and
eventually handed a traditional name — through the following declared chain.
At Kernel v0.1 this chain is **law only** except for its deferral branch: no
`BirthGate` that can birth anything, no rank/complexity class, and no
Arabic-specific carrier/state/relation ontology type exists yet. G0.BV.1a's
`BirthVerdictGate` executes only the `DEFER_IN_SCOPE` outcome of this chain
and can never advance it. A
non-linguistic intervention-operation runtime does already exist (see
`InterventionOperationIsNotOntology` below); it is a declared experimental
tool, not one of these ontology types, and does not itself satisfy this
chain. Those ontology types are separate, later milestones that must
themselves be structurally admitted like any other change, and must not be
named in advance of the residual that would force them (`G0.F` below); this
section only freezes the constraints they will have to satisfy if and when
they are born.

```
BirthQuery -> Evidence -> Residual -> LicensedWeakerExhaustion
-> NecessaryInvariantCandidate -> BirthCandidate -> IndependentClosure
-> BirthVerdict -> Freeze -> E0 -> TraditionalName
```

`BirthCandidate != BirthVerdict`: a candidate remains only a proposal until
`IndependentClosure` produces `BIRTH_IN_SCOPE` through a future gate. `Freeze`
is the separate, later act of fixing only that successful scoped verdict;
`E0` consumes that frozen result in a subsequent stage. `NO_BIRTH_IN_SCOPE`
and `DEFER_IN_SCOPE` cannot be frozen. Naming never occurs before birth
verdict, freeze, and `E0` have happened.

| Law | Status | Scope |
| --- | --- | --- |
| `NoBirthWithoutResidualOrFormalNecessity` | DECLARED_DEFERRED | No candidate object, factor, or axis may be born without one of two independent evidence modes. In `EMPIRICAL` mode, a *measured* residual (from real observations, not synthetic interventions alone) must remain unexplained after every licensed weaker projection has been applied. In `FORMAL` mode, over a declared `FrozenFormalDomain` with `card(Ω) < ∞` (or another exhaustively decidable closed domain), an exhaustive proof over every element of that domain, with no weaker formal model sufficing, may license birth without any measurement run. A `MIXED` mode combines both and must satisfy each mode's own condition on its own part of the claim. `FormalProof ⇏ EmpiricalReality` and `EmpiricalPattern ⇏ MathematicalNecessity`: neither mode substitutes for the other, and every birth must declare which mode(s) it relies on. |
| `NoBirthBeforeLicensedWeakerExhaustion` | DECLARED_DEFERRED | Before any `BirthCandidate` may be proposed, every weaker projection or formal model *licensed and frozen for that experiment* (`W_E = {W_1, ..., W_n}`), not an unbounded or open-ended "every weaker model conceivable," must first be tried and shown insufficient. A birth proposal that skips a licensed weaker model is malformed, not merely unproven. Discovering a new weaker model `W_{n+1}` afterward opens a new, separately recorded revision; it does not erase the historical closure in its original scope. |
| `NoRicherStructureBeforeLowerOpenResidualClosure` | DECLARED_DEFERRED | For a queried structure `q`, its prerequisite cone is exactly `Down_E(q) = {p ∈ P_E : p ≺_E q}`, derived from the experiment's frozen projection poset, never selected independently by the caller. If any `p ∈ Down_E(q)` has an open residual, examination of `q` is blocked. This is a partial-order constraint, not a linear "rank `r+1`" constraint. An incomparable projection (`p ∥ q`) does not block examination; however, if it offers a complete competing explanation of the residual, `BIRTH_IN_SCOPE(q)` is blocked until discriminating evidence resolves the competition. |
| `ScopedBirthIsNotGlobalOntologyClaim` | DECLARED_DEFERRED | Every verdict is scoped to the exact `(experiment, revision, domain, licensed weaker-model set, evidence mode, measurement run or formal domain, evidence snapshot)` tuple that produced it: `BIRTH_IN_SCOPE(...)`, `NO_BIRTH_IN_SCOPE(...)`, or `DEFER_IN_SCOPE(...)`. A malformed specification produces no verdict; `DEFER_IN_SCOPE` is reserved for a structurally valid but epistemically unresolved assessment. A later revision may become the active epistemic assessment, but cannot erase a prior verdict's historical scoped record. No scoped verdict generalizes into a global ontology claim. |
| `ProjectionIsNotOntology` | DECLARED_DEFERRED | Weaker-model projections (for example count, set, multiset, ordered-tuple) are analysis tools for deciding whether a residual survives, not born objects and not linguistic claims. Projections form a partial order, not a total order: `P_count` and `P_set` are incomparable (`P_count ∥ P_set`), while both are recoverable from `P_multiset`, and `P_multiset` is recoverable from `P_seq` (`P_count ⪯ P_multi`, `P_set ⪯ P_multi`, `P_multi ⪯ P_seq`). No total-order complexity vector may be assumed across projections or coordinates that have not themselves been born. |
| `InterventionOperationIsNotOntology` | DECLARED_DEFERRED | A declared basis of experimental interventions (for example an "ExperimentalInterventionBasisV0" of delete/insert/substitute/repeat/swap) is an explicit, named, non-exhaustive experimental tool. It must never be asserted to be the complete set of primitive operations, and its members are not linguistic or structural objects. |
| `CounterfactualResultIsNotObservation` | DECLARED_DEFERRED | The output of a synthetic/counterfactual intervention applied to a previously observed occurrence is not itself a `RawSurfaceObservation` or any other measured observation. This is a type/authority separation, not an implementation detail: a counterfactual result must belong to a distinct type that cannot be admitted into the observation or normalization ledgers, regardless of how any particular field on it is named or valued. Partially enforced for the two artifact kinds that exist in the Arabic encoding layer (`src/alghanem/arabic/encoding/provenance_genus.py`): `EvidenceProvenanceGate` is the sole issuer of an `EvidenceProvenanceClassification`, and derives its genus from the artifact's own type (`NormalizationAudit` bound to a manifest is `MEASURED`, `SurfaceInterventionAuditRow` is `SYNTHETIC`), so no caller may write a genus anywhere — `DeclaredProvenanceLabel != DerivedProvenanceGenus`. A synthetic classification is refused at construction by `MeasuredContrastSet`. The law remains `DECLARED_DEFERRED` in general because only these two artifact kinds are covered, and nothing yet prevents a future artifact kind from bypassing the gate. |
| `SyntheticInterventionMayGenerateHypothesisOnly` | DECLARED_DEFERRED | A residual discovered only through synthetic/counterfactual interventions (`R_synthetic`) may license nothing beyond a hypothesis (recorded as a `HypothesisResidual`, not a `FactorCandidate`). It cannot by itself satisfy `NoBirthWithoutResidualOrFormalNecessity`. A hypothesis becomes birth-eligible only after an independently measured contrast (`R_measured`), drawn from real observations under a measurement run, is found to match the hypothesis and itself survives every licensed weaker projection, with replication in a second, independent measurement run. For example, a `swap` intervention showing `(a, b) != (b, a)` at the codepoint-sequence level proves only `CodepointSequenceIsOrderSensitive` within the synthetic domain; it does not by itself birth any order-related linguistic or structural candidate. The 'hypothesis only' half is enforced in the Arabic encoding layer: `HypothesisResidual` is the only thing constructible from synthetic classifications, it refuses measured evidence, it is checked at import to declare no candidate, verdict, birth, or rank field, and its `is_birth_eligible` is structurally `False` with no method able to raise it. The promotion half remains `DECLARED_DEFERRED`: no authority in that layer assesses residual survival under licensed weaker projections or replication in a second independent measurement run, so no rank, count of measured sources, or freeze exists there — a rank ladder ascending on a count would be precisely the caller-owned freeze authority this constitution refuses. |
| `DerivedFootprint != DeclaredFootprint` | ENFORCED_AT_INTERVENTION_FOOTPRINT | The ReadSet, WriteSet, and coordinate shift of an intervention are derived from the intervention itself and are never accepted from a caller. `InterventionFootprint` (`src/alghanem/arabic/encoding/intervention_footprint.py`) holds exactly one field — the intervention — and exposes `read_set`, `write_set`, `shift`, and `touched` as computed properties, so a footprint contradicting its own intervention is unconstructible rather than merely unverified. Shift is modelled explicitly (`delete` and `repeat` from `i + 1`, `insert` from `i`) instead of being folded into overlap, so disjoint write sets still conflict when one operand sits at or past the other's shift origin. |
| `PredictedVerdict != ObservedVerdict` | ENFORCED_AT_INTERVENTION_FOOTPRINT | A commutation verdict predicted from footprints alone is a distinct object from the verdict observed by applying both orders through the real application path (`observe_commutation`), and the two are never conflated. A disagreement is named `PREDICTION_ORACLE_MISMATCH(τᵢ,τⱼ)`, retained in the reported pair list, and drops the derived `law_status()` to `PARTIAL_WITH_NAMED_RESIDUALS`; the status is derived from the matrix rather than written into it, the mismatched pair may not be dropped, and the footprint definition may not be retrofitted to match what was observed. This is `NoLabelLeak` raised to the level of a verdict. |
| `NamedCriticalPairs != GeneralizedLaw` | ENFORCED_AT_INTERVENTION_FOOTPRINT | The product of the footprint module is an enumerated list of named pairs with their verdicts and reasons (`overlap`, `shift`, `out_of_range`) over named coordinate configurations, not a generalized confluence or commutation law over the whole intervention algebra. `reference_matrix` covers the five intervention types pairwise across nine declared configurations on a distinct-atom sequence, excluding identical interventions by declaration; its scope and its limits are recorded in `DERIVED_LAW_SCOPE_NOTE`, `IDENTICAL_PAIR_EXCLUSION_NOTE`, `PAYLOAD_INDEPENDENCE_NOTE`, `ORDERED_TRIPLES_ABSENCE_NOTE`, and `VALUE_COINCIDENCE_NOTE`. The measured domain is ordered pairs only: a three-way critical-pair set is not derivable from pairwise verdicts, so it is recorded as absent rather than assumed. Because the model reads coordinates and not values, agreement produced by repeated atoms is value coincidence, not structural commutation, and is demonstrated by an explicit test instead of absorbed by widening the definition. Nothing beyond the measured configurations is claimed. |
| `AgreedVerdict != GrantedAuthority` | ENFORCED_AT_INTERVENTION_FOOTPRINT | Agreement between the predicted and the observed verdict disciplines a model of non-linguistic surface interventions and grants no authority whatsoever. No kernel type, gate, `Freeze`, or `E0` reads anything from the footprint module, and exporting it from `alghanem.arabic.encoding` is availability, not consumption; the absence is recorded in `NO_KERNEL_MODULE_CONSUMES_INTERVENTION_FOOTPRINT_NOTE` and enforced by an import-tree sweep test rather than asserted in prose. Subject to `InterventionOperationIsNotOntology` and `SyntheticInterventionMayGenerateHypothesisOnly`, a confirmed derived law here remains non-authoritative: it licenses at most a hypothesis and never a birth verdict. |
| `TraditionalNamingOnlyAfterFreezeAndE0` | DECLARED_DEFERRED | A traditional name (linguistic, grammatical, or morphological) may only be attached after the full chain `BirthCandidate -> IndependentClosure -> BIRTH_IN_SCOPE -> Freeze -> E0` has completed. The name is never part of the birth proof, never influences whether birth, closure, or freeze occurs, and the kernel itself must never define or reference `TraditionalName`; any such naming step belongs strictly to a downstream, kernel-independent evaluation/oracle layer. |

These laws are declared now, ahead of any experiment, precisely so that the
question being asked cannot be quietly reshaped by the answer an experiment
later produces. Implementing `BirthGate`, a rank/complexity representation,
or any Arabic-specific carrier/state/relation ontology type is out of scope
for this section and must occur in later, separately reviewed milestones
that are held to these same laws. No such type -- including any general
linguistic "binding" relation -- is to be named or scaffolded before a
residual is shown to force it: see `G0.F`'s `DerivedRelationDoesNotBirth` and
`NoTraditionalSchemaBeforeFactorization` below. (`kernel/binding.py`'s
`ClaimEvidenceBinding` is an unrelated kernel-level evidence/claim binding,
not an Arabic linguistic relation, and is out of scope of this paragraph.)

#### Recorded external-source conflict (not a law, not a relaxation)

An external jurisprudential source consulted while reviewing this protocol
licenses answering a question with *more* than was asked ("الجواب بأكثر مما
سُئل"): a valid answer may legitimately settle matters beyond the question's
own subject. This directly conflicts with
`NoRicherStructureBeforeLowerOpenResidualClosure` above, which blocks
examination of a richer structure `q` while any `p ∈ Down_E(q)` has an open
residual, and with `TraditionalNamingOnlyAfterFreezeAndE0`, which forbids
naming anything a residual has not forced.

The conflict is recorded, not resolved, and neither side is weakened to fit
the other. In this repository the constitutional laws govern: an audit or
experiment may not answer beyond the structure its own query and prerequisite
cone license, regardless of that external precedent. This paragraph exists so
that the conflict cannot later be presented as agreement, and so that the
external precedent cannot be cited as grounds for relaxing either law.

### G0.1 — Birth experiment contract

`BirthExperimentSpecification` is a language-agnostic, frozen pre-evidence
contract. It contains an experiment identity, revision identity and monotonic
revision sequence, evidence mode, domain, frozen projection poset,
`BirthQuery`, stable residual-definition identity, residual-definition text,
stable closure-criterion identity, closure-criterion text, and evidence
requirements. The stable identities are the freeze boundary; descriptive text
alone cannot identify a later executable contract. It does not contain an
evidence snapshot, a candidate, a verdict, or caller-selected weaker models.
Its frozen weaker-model set and `PrerequisiteCone` are both derived as
`Down_E(q)` from the poset and query: they share values in G0.1, but name the
distinct frozen-model-set and query-relative order roles. Its incomparable
projections are recorded as possible competing explanations.

`BirthAssessmentRequest = AuthorizedFrozenExperimentBinding +
AuthorizedEvidenceSnapshot`; the request refuses a raw
`BirthExperimentSpecification` and refuses the legacy, unauthorized
`EvidenceSnapshot` (deprecated: it carries no acquisition provenance). This
ordering enforces `NoAssessmentRequestWithoutAuthorizedPreEvidenceFreeze` and
`EvidenceMayBeAttachedOnlyToAnAuthorizedFrozenExperiment`, preventing evidence
from redesigning the question or its closure criterion. The contract validates
malformed bindings before any request can enter a future runtime. G0.1 stops at
`BirthAssessmentRequest`: it has no
executable verdict, revision-history, competing-explanation assessment, or
freeze authority. G0.BV.1's birth branch remains deferred: no runtime authority may issue
`BIRTH_IN_SCOPE` or `NO_BIRTH_IN_SCOPE` until an assessment authority,
BirthCandidate, and IndependentClosure exist. Its deferral branch is now
executable at G0.BV.1a (`kernel/birth_verdict.py`): `BirthVerdictGate.assess`
derives `DEFER_IN_SCOPE` itself from the request's own frozen projection poset,
for a frozen experiment authorized in a sealed `BirthVerdictScopeRegistry`. A
gate that can only defer still refuses every unlicensed birth, which is the
boundary G0.BV.1 exists to protect; it issues no `Freeze` and no `E0`.
G0.IC.1a (`kernel/independent_closure.py`) then closes exactly one conjunct of
the missing `IndependentClosure` and openly refuses the rest:
`IndependentClosureGate.assess` derives, from the frozen projection poset
alone, whether any projection is left incomparable with the test model. Over a
finite frozen projection set that question is exhaustively decidable, so unlike
the verdict gate both of its statuses are reachable. It remains far from
closure: `IndependentClosureAssessment.is_independent_closure` is `False`
unconditionally, and `BirthVerdictGate` is deliberately not wired to consume
it.

The current repository-level Arabic card auditor
(`src/alghanem/arabic/external_audit.py`) is intentionally outside kernel
verdict authority. It may parse an external card and emit an external audit
result (`نتيجة_التدقيق_الخارجي`) for communication/audit traceability, but it
must not be interpreted as issuing `BirthVerdict` or freeze authority. Its
weaker-prerequisite cone is derived from the experiment's frozen projection
poset, not caller-declared, and it may defer when competing-relation typing or
`Down_E` closure documentation is unresolved. Competing-relation typing draws
on a closed vocabulary (`غير_متعينة`, `أضعف_صوريًّا`, `مكافئ_صوريًّا`,
`غير_قابل_للمقارنة`); an unrecognized value is rejected rather than treated as
a resolved relation, and, per
`NoRicherStructureBeforeLowerOpenResidualClosure`, a `غير_قابل_للمقارنة`
reading stops blocking only when the card explicitly denies that it offers a
complete competing explanation. Because a surface spelling is not
an epistemic distinction, every card comparison runs over an
orthography-insensitive key rather than raw text: optional diacritics,
invisible formatting characters, `TATWEEL`, and equivalent `ALEF`/`ALEF
MAQSURA`/`TEH MARBUTA` forms may not decide whether a relation counts as
determined or a `Down_E` prerequisite counts as closed. The key governs
comparison only; reported fields keep the card's own spelling.

### G0.2a.3 — Evidence acquisition authority

Binding evidence to a frozen experiment is not enough: a caller could still
select or construct evidence before designing an experiment, then attach it
to a `BirthExperimentSpecificationContentBinding` produced afterward. This
proves only `FreezePrecedesRequestConstruction`, not that the freeze
authorized the evidence's own acquisition. G0.2a.3 closes the narrower,
code-provable claim `FrozenExperimentPrecedesAuthorizedEvidenceIngestion`
instead of an unprovable external-world chronology claim.

The chain is
`BirthExperimentSpecification -> FrozenPreEvidenceExperimentManifest ->
BirthExperimentSpecificationContentBinding -> EvidenceAcquisitionAuthorization
-> EvidenceAcquisitionRun -> AuthorizedEvidenceSnapshot`.
`EvidenceAcquisitionAuthority.authorize` is the sole issuer of an
`EvidenceAcquisitionAuthorization`, and requires a genuine, already-verified
`BirthExperimentSpecificationContentBinding`
(`NoEvidenceAcquisitionAuthorizationWithoutFrozenExperiment`). The
authorization does not accept caller-supplied `experiment_content_id`,
`domain`, `evidence_mode`, `evidence_requirements`, `revision_id`, or
`revision_sequence`: every one of these is a derived property read from the
verified binding, so an authorization can never assert a condition the frozen
experiment did not itself freeze.

An `EvidenceAcquisitionAuthorization` is also the sole issuer of an
`EvidenceAcquisitionRun` (`authorization.open_run(...)`), and an
`EvidenceAcquisitionRun` is the sole issuer of an `AuthorizedEvidenceSnapshot`
(`run.ingest(...)`), closing
`NoAssessableEvidenceSnapshotWithoutAcquisitionAuthorization`: no caller can
construct any of the three objects directly, each raising
`EvidenceAcquisitionAuthorityError` when its authority token is missing.
`CanonicalEvidenceContentEncoder` is the sole issuer of the ingested payload's
`EvidenceContentIdentity`; a snapshot never accepts a caller-supplied content
identity. This keeps `EvidenceOccurrenceIdentity != EvidenceContentIdentity`:
`snapshot_id`, `run_id`, and `authorization_id` name one acquisition
occurrence, while `content_id` is a digest over the ingested bytes, shared by
any two occurrences that ingest byte-identical content.
`BirthAssessmentRequest` further checks that its evidence snapshot's
`experiment_content_id` equals its own experiment binding's `content_id`,
rejecting a snapshot authorized under a different frozen experiment.

`AuthorizedCapture != ProofOfExternalAcquisitionChronology`: this stage does
not prove when or how evidence was first observed or produced outside this
process, and pre-existing evidence could still be ingested through an
authorized run. It also does not claim anything about evidence quality:
`AuthorizedEvidence != SufficientEvidence`, and authorized evidence does not
imply `ResidualSurvival` or `Birth`. G0.2a.3 issues no `ResidualAssessment`
and no `BirthVerdict`.

### G0.2a.3.1 — Issuer-scoped occurrence issuance integrity

G0.2a.3 alone let `authorization_id`, `run_id`, and `snapshot_id` be any
non-empty, caller-chosen string: nothing stopped
`EvidenceAcquisitionAuthority.authorize` from issuing two authorizations for
the same `authorization_id`, an authorization from opening the same `run_id`
twice, or a run from ingesting two different payloads under the same
`snapshot_id`. These strings were therefore `EvidenceOccurrenceCoordinates`
with real provenance, but not yet a proven `EvidenceOccurrenceIdentity`:
`same(id)` did not imply `same(occurrence)`, since an issuer would accept the
id again.

Each issuer now keeps its own registry of the ids it has already issued and
rejects a repeat with `EvidenceAcquisitionAuthorityError`: an
`EvidenceAcquisitionAuthority` instance tracks its issued `authorization_id`s,
one `EvidenceAcquisitionAuthorization` tracks its own issued `run_id`s, and
one `EvidenceAcquisitionRun` tracks its own issued `snapshot_id`s (rejecting a
repeat even when the later `ingest` call carries different content). Each
registry's check-and-insert is synchronized with an internal lock, so
concurrent calls on the same authority, authorization, or run instance cannot
race past the uniqueness check. This makes issuance injective within its
declared scope: two ids issued by the same issuer are equal only if they name
the same occurrence, and distinct ids issued by the same issuer always name
distinct occurrences. This is `IssuerScopedOccurrenceUniqueness`, precisely:

```
forall issuer, id:
    Issued_issuer(o1) = id and Issued_issuer(o2) = id => o1 = o2
```

This is deliberately **not** named `EvidenceOccurrenceIdentity`, because
`LocalInjectivity != PortableIdentity`: proving an id is never repeated
*within one issuer's own registry* does not prove it is never repeated
*across issuers*. Nothing in `AuthorizedEvidenceSnapshot` carries an
`issuer_scope_id`, so two distinct `EvidenceAcquisitionAuthority` instances
remain two distinct, uncoordinated issuance scopes: each is free to issue
`authorization_id="a1"`, whose `open_run("r1")` issues `run_id="r1"`, whose
`ingest(snapshot_id="s1", ...)` issues `snapshot_id="s1"`, and nothing in the
resulting snapshot's comparable fields (`snapshot_id`, `run_id`,
`authorization_id`, `experiment_content_id`, `domain`, `evidence_mode`,
`trace`) distinguishes which authority issued it. If both authorities also
share the same frozen experiment binding, payload, and trace, the two
snapshots' comparable representations coincide even though the two
acquisition occurrences are genuinely independent
(`Occurrence_A != Occurrence_B` yet
`Representation(Occurrence_A) == Representation(Occurrence_B)`). A portable
identity would require an issuer-scope identity of its own -- one that
carries its own issuance authority rather than being another caller-chosen
string -- propagated through `Authorization -> Run -> Snapshot`; that is not
built here. So the accurate judgment is:

```
IssuerScopedOccurrenceUniqueness = PROVED
PortableEvidenceOccurrenceIdentity = DEFERRED
```

`BirthAssessmentRequest` does not hold an authority or issuer-scope object
either: it only checks `snapshot.experiment_content_id ==
binding.content_id`, so it cannot and does not distinguish which authority
scope produced an otherwise-matching snapshot. This is an accepted, narrower
surface than a caller might assume from the name "occurrence identity" alone,
and is the reason this stage's claim is `IssuerScopedOccurrenceUniqueness`,
not `EvidenceOccurrenceIdentity`.

This closes `IssuerScopedOccurrenceUniqueness` only within each issuer's own
scope, not globally: two different `EvidenceAcquisitionAuthority` instances
are two different issuance scopes, and nothing proves their respective
`authorization_id`s differ from one another. `EvidenceAcquisitionAuthority()`
remains a construction boundary, not a permission or security authority --
identical to how `StructuralAdmissionGate` construction is not itself a claim
of external authorization.

`EvidenceAcquisitionRun` and `EvidenceAcquisitionAuthorization` are
`ExternallyFrozen, InternallyStatefulAuthority` objects, not plain immutable
value objects: their dataclass is `frozen=True` so their *own* declared
identity fields (`run_id`, `authorization_id`, `binding`, etc.) can never be
reassigned after construction, but each also holds a private, mutable
`_issued_*` registry `set` and a `threading.Lock` (both `compare=False`,
`repr=False`, `init=False`) as internal operational bookkeeping state. This
bookkeeping is deliberately excluded from equality, `repr`, and from any
content-identity computation (it is never hashed or serialized into
`EvidenceContentIdentity` or any experiment content identity): it exists only
to enforce this stage's issuance uniqueness, not to describe the object's own
identity or content.


### G0.BA.1a — Authorized evaluator implementation binding

G0.2a's `BirthAssessmentEvaluatorRegistry` authorizes evaluator
*declarations* for an exact `(domain, role, target_id, evaluator_id)` scope
and explicitly performs no assessment. That leaves a narrower residual than
"birth assessment execution is missing": `AuthorizedBirthAssessmentEvaluatorDefinition`
does not, and must not, imply `AuthorizedEvaluatorImplementation`, and neither
implies `EvaluatorExecution`. This stage closes exactly that one narrower
question: can an already registry-authorized definition be bound to an exact
implementation identity and executed through an authority boundary that
produces a non-caller-constructible record?

`AuthorizedBirthAssessmentEvaluatorDefinition` is preserved completely
unchanged; it gains no execution semantics here. A separate
`AuthorizedBirthEvaluatorImplementationBinding` binds one such definition to
one `implementation_identity` and one executable callable.
`BirthEvaluatorImplementationRegistry.register` is the only way to construct
one, and it requires the caller to already hold a genuine, registry-issued
`AuthorizedBirthAssessmentEvaluatorDefinition` -- a bare evaluator id string
cannot substitute for it. `BirthEvaluatorImplementationRegistry.seal` freezes
the registered bindings into a `SealedBirthEvaluatorImplementationRegistry`,
which resolves only by the exact five-part scope
`(domain, role, target_id, evaluator_id, implementation_identity)`; an
unregistered implementation identity, or a definition mismatched on domain,
role, target, or evaluator id, is rejected rather than silently resolved.

`BirthEvaluatorExecutionGate.execute` is the sole authority that may invoke a
bound implementation. It resolves the exact binding, re-checks that the
resolved binding's own definition equals the caller-supplied definition,
requires the request's frozen experiment domain to match the definition's
domain, and calls the bound implementation with the caller-supplied input
content. The bound implementation must return `(output_content, trace)`; any
other shape is rejected. Only the gate can construct the resulting
`BirthEvaluatorExecutionRecord`, which preserves the exact authorized
definition, implementation identity, role, target, the exact
`BirthAssessmentRequest`, that request's own bound `AuthorizedEvidenceSnapshot`
(not a caller-substituted one), input content, output content, and trace.

This record answers only "did a specific, registry-bound implementation run
within the context of a specific, authorized assessment request, while
preserving that request and its attached evidence reference?"
(`ExecutedInContextOfAuthorizedRequest + AttachedEvidenceReference`, not
`ExecutedAgainstAuthorizedEvidence`): `EvidenceAttachedToRecord !=
EvaluatorExecutedOnEvidence`, and `InputProvenance = DECLARED_DEFERRED`. It
carries no
`ResidualEvaluationResult`, `WeakerModelEvaluationResult`,
`ClosureEvaluationResult`, aggregate execution status, residual survival,
weaker-model exhaustion, `BirthCandidate`, `IndependentClosure`,
`BirthVerdict`, or `Freeze` meaning:

```
Definition != ImplementationBinding != ExecutionRecord != Assessment
```

Composing per-role execution records (residual, weaker-model, closure) into
any assessment, and any question of whether the frozen weaker-model family as
a whole has been exhausted (`WeakerFamilyExhausted <=> forall W_i in
FrozenWeakerSet: AuthorizedExecution(W_i)`, distinct from
`Executed(W_i)` for any single model), remain separate, later, and still
undecided questions. This stage does not assume they will be closed next, or
in this shape; it closes only the one question stated above.


G0.2 is split into smaller authority-preserving stages. G0.2a defines only
executable assessment contracts: `ResidualDefinitionSpec` identifies the
residual domain, input projection, output schema, evaluator-id declaration,
invariants, and failure semantics; each `WeakerModelSpec` binds a frozen weaker
model to its evaluator, information loss, result schema, and exact poset
relations; and `ClosureCriterionSpec` defines the local
`Close(W_i, R) ∈ {CLOSE, FAIL_TO_CLOSE, DEFER}` vocabulary for weaker-model
closure. `BirthAssessmentSemanticsContract` validates that these executable
contracts match the frozen residual-definition and closure-criterion
identities, experiment, domain, queried projection, prerequisite cone, schemas,
and poset relations. Matching only domain or schema is insufficient:
`NoResidualDefinitionDriftAfterFreeze` and
`NoClosureCriterionDriftAfterFreeze` require exact identity equality.

Evaluator ids in these contracts are declarations only:
`DeclaredEvaluatorId != AuthorizedEvaluator`. `CallerDoesNotOwnEvaluatorAuthority`
requires registry-issued definitions before those ids can become authorized for
an exact `(domain, role, target_id, evaluator_id)` scope.
`BirthAssessmentEvaluatorRegistry` and
`SealedBirthAssessmentEvaluatorRegistry` provide that sealed definition
boundary while executing no assessment. G0.2a obeys `NoVerdictYet`: it issues
no `ResidualAssessment`, `BirthCandidate`, `BirthVerdict`, `Freeze`, or E0
result.

G0.2a's id-equality checks close *label* identity, not *content* identity:
`SameId` does not imply `SameSemantics`. G0.2a.1 closes that separately.
`ResidualDefinitionId != ResidualDefinitionContentIdentity`, and the same
distinction holds for `ClosureCriterionSpec` and `WeakerModelSpec`.
`CanonicalBirthSemanticsEncoder` issues immutable canonical manifests and
`BirthSemanticsContentIdentity` digests for each; `BirthSemanticsContentRegistry`
freezes the canonical bytes of the first canonical content bound to an exact
`(domain, role, target_id)` scope, rejecting later content drift under the
same id; and `BirthAssessmentContentBinding` proves
exact canonical-byte equality for the residual definition, the closure
criterion, and every weaker model bound to a `BirthAssessmentSemanticsContract`.
This closes `NoDeclaredSemanticDigestDriftAfterFreeze`; the registry retains
the canonical bytes and binding compares those bytes directly, so it also
enforces `ExactCanonicalContentFreeze` rather than treating digest equality as
content equality. G0.2a.2 separately gives every complete
`BirthExperimentSpecification` an encoder-issued canonical manifest and
content identity, covering its revision, evidence mode, domain, poset, query
and hypothesis, residual/closure declarations, and evidence requirements.
`PreEvidenceSpecificationRegistry` alone issues a
`FrozenPreEvidenceExperimentManifest`; semantic-registry sealing requires that
manifest, so a semantic snapshot cannot float independently of its frozen
experiment specification. All canonical encoders enforce schema coverage:
every declared field is either encoded or listed as an explicit derived
exclusion, including `ProjectionPoset`, `BirthQuery`, and
`StructureHypothesis`; adding an unaccounted field rejects encoding. It still
performs no evaluation and
issues no birth authority. `EvaluatorId != EvaluatorImplementationIdentity`
remains open: this stage authorizes evaluator *declarations*, not evaluator
*implementations*. `G0.BA.1a` already provides a runtime invocation boundary
that resolves evaluator execution through a registry-owned implementation,
never a caller-supplied callable, but proves only registry-bound invocation:
`ImplementationIdentityIsContentAuthenticated = DEFERRED`. Any later runtime
that claims reproducible or content-authenticated evaluator implementation
identity must instead bind that implementation to independently
authenticated content; `G0.BA.1a` does not yet close that requirement
(`AuthorizedCallableInvocation != ReproducibleImplementationIdentity`).

Later G0.2 stages alone may implement the complete authority chain:
`BirthAssessmentRequest -> ResidualAssessment ->
LicensedWeakerExhaustion -> NecessaryInvariantCandidate -> BirthCandidate ->
IndependentClosureDecision -> gate-issued BirthVerdict -> Freeze -> E0`.
That gate must assess every relevant incomparable model itself; callers cannot
omit a competitor or promote string placeholders as discriminating evidence.
It must keep `Freeze` distinct from the subsequent `E0` assessment. No
Arabic-specific type is part of G0.1 or this deferred G0.2 design.

### G0.BA.1b — Evidence-derived evaluator input provenance

G0.BA.1a states three claims it refuses to make. This stage closes exactly
one of them, `InputProvenance = DECLARED_DEFERRED`, and leaves the other two
standing.

The refused claim is precise. `BirthEvaluatorExecutionGate` invokes a
registry-bound implementation on *caller-supplied* `input_content` and
attaches the request's own `AuthorizedEvidenceSnapshot` for audit, but
nothing there relates the two. A `BirthEvaluatorExecutionRecord` therefore
proves that an implementation ran on *some* content alongside *some*
authorized evidence -- never that the one came from the other
(`EvidenceAttachedToRecord != EvaluatorExecutedOnEvidence`). Passing the real
measured numbers rather than invented ones was, at that boundary, a caller's
discipline and not a kernel guarantee.

The correction is structural rather than a comparison bolted onto the old
gate. An `EvaluatorInputDerivation` receives exactly one argument: the
`canonical_bytes` of the request's own authorized evidence manifest. It is
handed nothing else, so it cannot source content from outside that snapshot
except by ignoring its input, which the recorded derivation identity then
exposes. `EvaluatorInputDerivationGate.derive` accepts no `input_content`
parameter and no domain parameter at all (`CallerDoesNotOwnInputContent`):
the caller chooses *which* authorized derivation runs, never what the
evaluator sees, and the domain is read from the request's own frozen
experiment specification.

The authority shape is the one used throughout this repository.
`EvaluatorInputDerivationRegistry.register` is the sole issuer of an
`AuthorizedEvaluatorInputDerivationBinding`; `seal` alone produces a
`SealedEvaluatorInputDerivationRegistry`, which resolves only by the exact
three-part scope `(domain, derivation_id, implementation_identity)`; and only
`EvaluatorInputDerivationGate.derive` may issue an
`EvidenceDerivedEvaluatorInput`. Before deriving, the gate re-verifies that
the snapshot's own bytes hash to the snapshot's own `EvidenceContentIdentity`.
A derivation that returns non-text, returns blank content, or returns a
different result for the same authorized bytes is rejected. That last check
rejects *observed* nondeterminism only: `ObservedDeterminism != ProvenPurity`.

Identity binds the whole triple, not the output alone.
`CanonicalEvaluatorInputDerivationEncoder` digests the source evidence
content identity, the derivation id, the implementation identity, and the
produced content together under length-prefixed canonical bytes, so no two
distinct tuples share an encoding by concatenation. The issued
`EvaluatorInputContentIdentity` therefore records what was produced, from
which exact evidence, and by which declared derivation:

```
OutputDigest != DerivationIdentity
```

Execution stays layered, not rewritten.
`ProvenanceBoundEvaluatorExecutionGate.execute` delegates the invocation
itself to the completely unchanged `BirthEvaluatorExecutionGate`, then binds
the issued record to the derivation that produced its input: the same
request object, the same evidence snapshot object, and exactly the derived
content. G0.BA.1a keeps `InputProvenance = DECLARED_DEFERRED` and still
accepts unrelated caller-supplied input by design; provenance is proven only
for records this stage issues.

Three claims remain refused here, and must not be read into a
`ProvenanceBoundEvaluatorExecutionRecord`:

* `DerivationIdIsContentAuthenticated = DEFERRED`. `derivation_id` and
  `implementation_identity` are plain, caller-chosen strings, exactly as in
  G0.BA.1a, with no canonical manifest or digest of the derivation code
  (`DeclaredDerivationId != DerivationContentIdentity`). The
  `declared_transformation` text is carried for audit and never verified
  against the callable (`DeclaredTransformation != VerifiedTransformation`).
  What is proven is that this record's input came from this evidence through
  *the* callable registered under that name -- not that the name describes
  the callable truthfully.
* `AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment`,
  inherited unchanged from G0.BA.1a: the execution boundary still matches
  only `domain`.
* `ProvenInputProvenance != AssessedEvidence`. `is_assessment` is `False`
  unconditionally. Knowing that an evaluator truly ran on the authorized
  evidence says nothing about what its output means, so the record carries
  no residual survival, weaker-model exhaustion, closure, `BirthCandidate`,
  `IndependentClosure`, `BirthVerdict`, or `Freeze` meaning:

```
Derivation != ExecutionRecord != Assessment
```

This stage does not move `IndependentClosureAssessment.is_independent_closure`
off `False`. It removes a necessary-but-insufficient obstacle beneath the two
conjuncts AIM-K3 still lacks: an authority that evaluates residual survival
and licensed weaker exhaustion. Such an authority would previously have been
built on input no gate could relate to the authorized evidence; it now has a
boundary to build on, and nothing more.

## G0.IC.1b — Evidence-derived weaker-model closure outcome

`ClosureCriterionSpec` already declared the closed outcome vocabulary of
`Close(W_i, R)`, the frozen projection poset already derived which weaker
models must be closed, and G0.BA.1b already proved that an evaluator ran on
this request's own authorized evidence. What no authority did was relate an
evaluator's output string to a member of that closed vocabulary.

`DeclaredClosureOutcomeVocabulary` is that relation, declared as data by the
closure criterion's owner and frozen in a sealed registry before any gate
reads it. It must cover every `ClosureAssessmentStatus` member exactly once,
so no declared outcome is unreachable by construction and none is silently
dropped:

```
DeclaredToken -> ClosureAssessmentStatus, exact match or refusal
```

The gate reads, and does not decide:

* `CallerDoesNotOwnClosureOutcome`. `WeakerModelClosureGate.assess` accepts
  no status, no reason, and no outcome claim.
* `ExactTokenOrRefusal`. An output outside the declared vocabulary is refused
  by model id. It is never mapped to `DEFER` as a convenience, because reading
  ignorance as a declared outcome is the exact failure this gate prevents.
* `VocabularyIsBoundToFrozenCriterionContent`. Authorization requires a
  verified `BirthAssessmentContentBinding`, and the gate additionally requires
  the resolved vocabulary's contract to carry this request's own frozen
  experiment specification.

What this stage does not reach:

```
LocalClosureOutcome != WeakerModelExhaustion != IndependentClosure
```

A certificate speaks for one model in the cone. Nothing here aggregates the
cone, and `IndependentClosureAssessment.is_independent_closure` is untouched
and still `False`. `DeclaredVocabularyIsNotProvenSemantics` and
`SealedBeforeAssessmentIsNotSealedBeforeEvidence` remain open by name: a
frozen map cannot be tailored to an output already seen, but it proves nothing
about why the evaluator emitted that token, and no authority here timestamps a
seal against an evidence acquisition run.

## G0.IC.1c — Derived weaker-model exhaustion

G0.IC.1b answers one weaker model and says so: its certificate's
`is_weaker_model_exhaustion` is `False` unconditionally, because one model is
not the set. This stage is the set, and nothing more.

The set was already derived rather than written, so the question has a
decidable shape -- exact coverage of a frozen finite cone -- and this gate
answers only that shape:

```
coverage of frozen_weaker_models, exactly once, then aggregation
```

Coverage before judgement, copied from `assess_all_preserved`:

* A missing model is refused, never read as exhaustion-so-far
  (`MissingModelIsNotFailureToClose`).
* A model named twice is refused, because two outcomes for one model would let
  ordering choose the result.
* A model outside the frozen cone is refused, because the poset never licensed
  it (`FrozenPosetIsTheLicensedSet`).

Then the declared precedence, mirroring `BLOCK > DEFER > VERIFIED`:

```
WEAKER_MODEL_CLOSES_RESIDUAL
  > EXHAUSTION_UNDETERMINED
  > LICENSED_WEAKER_MODELS_EXHAUSTED
```

A single `CLOSE` outranks every deferral, because knowing that some weaker
model *does* close the residual is knowledge an unrelated `DEFER` must not
erase.

What this stage does not reach:

```
WeakerModelExhaustion != IndependentClosure
```

Two of three conjuncts are now derived -- comparability by G0.IC.1a and
exhaustion here. The third, a residual surviving under
`NoBirthWithoutResidualOrFormalNecessity`, is certified by no authority in this
repository, so `is_independent_closure` remains `False` and
`IndependentClosureAssessment` is untouched. `WeakerModelClosesResidual !=
NoBirthVerdict`, `CoverageIsNotCorrectness`, and
`SameRequestIsNotSameEvidenceRun` remain open by name.

## G0.IC.1d — Evidence-derived residual survival outcome

G0.IC.1a and G0.IC.1c each said the same thing about the conjunct they did not
reach: a residual surviving under `NoBirthWithoutResidualOrFormalNecessity` is
certified by no authority in this repository. This stage is that reading, for
one witness, and nothing more.

Nothing new is invented. The residual whose survival is at stake is already
declared by `ResidualDefinitionSpec`, and the closed three-member vocabulary of
a survival reading is declared on that same frozen contract
(`supported_statuses`), exactly as `ClosureCriterionSpec` declares the
vocabulary of `Close(W_i, R)`. The single missing relation is the one G0.IC.1b
supplied for closure outcomes:

```
evaluator output_content --(frozen declared vocabulary)--> ResidualSurvivalStatus
```

`ExactTokenOrRefusal` is inherited verbatim: exact string equality, no
trimming, no case folding, no prefix match, no default, and an unrecognized
output refused by residual id rather than read as `DEFER`. A record under any
role other than `RESIDUAL_DEFINITION`, or naming a target that is not the
request's own frozen `residual_definition_id`, is refused too.

The one mode refused by name:

```
MixedModeNeedsTwoScopedWitnesses
```

`evidence_mode` is read from the frozen experiment, never from the caller. A
`MIXED` experiment declares the explicitly typed scoped pair
`<(D_emp, S_emp), (D_formal, S_formal)>`, and no authority here proves those
declared scopes or `NoCrossSubstitution(D_emp, D_formal)`. One certificate that
a later reader could take as having satisfied both modes is exactly the
fabricated closure this constitution refuses, so the gate refuses the mode
instead.

What this stage does not reach:

```
ResidualSurvivalOutcome != IndependentClosure
```

The three conjuncts are now each derived on their own — comparability by
G0.IC.1a, weaker-model exhaustion by G0.IC.1c, and residual survival here — but
**composing** them is a separate question with no authority in this repository.
`is_independent_closure` is therefore still `False` on every branch,
`IndependentClosureAssessment` is untouched, and this stage is wired to neither
it nor `BirthVerdictGate`. `DoesNotSurvive != NO_BIRTH_IN_SCOPE`,
`SurvivalReadIsNotMeasuredReplicatedResidual`, `FormalNecessityIsNotProvedHere`,
`DeclaredVocabularyIsNotProvenSemantics`,
`SealedBeforeAssessmentIsNotSealedBeforeEvidence`, and
`OneWitnessIsNotResidualCertification` remain open by name.

## G0.IC.1e — Composed independent-closure decision

G0.IC.1a, G0.IC.1c and G0.IC.1d each closed one conjunct of
`IndependentClosure`, and each said the same thing in the same words: composing
them is a separate question with no authority in this repository. This stage is
that composition, and nothing more.

Nothing new is read:

```
ThreeReadingsAreNotAFourth
```

The gate opens no evidence, executes no evaluator, and inspects no frozen poset.
Every input is already a gate-issued reading, and a composition that re-derived
any conjunct would be a second authority over a question already answered — two
authorities whose answers could disagree.

`CallerDoesNotOwnComposition`: `IndependentClosureCompositionGate.assess` takes
exactly three parameters — the comparability assessment, the exhaustion
assessment and the survival certificate — and no status, no reason, and no
closure claim. `OneRequestOrRefusal`: the three readings must speak for the same
`BirthAssessmentRequest`, compared by object identity exactly as G0.IC.1c
requires of its certificates, and the survival reading must carry that request's
own authorized evidence snapshot. A comparability result for one frozen
experiment composed with a survival reading of another would be a closure claim
no single experiment ever supported.

The enumeration performed before the module was written. Comparability is
two-valued and exhaustion and survival are three-valued, so there are exactly
`2 x 3 x 3 = 18` combinations. Each conjunct falls into exactly one of three
roles:

* *satisfied* — `COMPETITION_RESOLVED_IN_POSET`,
  `LICENSED_WEAKER_MODELS_EXHAUSTED`, `SURVIVES`.
* *refuting* — `WEAKER_MODEL_CLOSES_RESIDUAL`, `DOES_NOT_SURVIVE`.
* *undetermined* — `EXHAUSTION_UNDETERMINED`, `DEFER`,
  `COMPETITION_UNRESOLVED_IN_POSET`.

```
UnresolvedComparabilityIsIgnoranceNotRefutation
```

Comparability has no refuting branch at all. G0.IC.1a already resolves
`AbsentRelation != DeclaredIncomparability` conservatively, so its unresolved
branch means the frozen poset did not settle the relation — not that a competing
explanation was established. Reading it as a refutation would manufacture
knowledge out of silence, the mirror image of the fabricated closure this chain
forbids.

Aggregation follows the precedence already enforced twice in this kernel
(`BLOCK > DEFER > VERIFIED`, and `WEAKER_MODEL_CLOSES_RESIDUAL >
EXHAUSTION_UNDETERMINED > LICENSED_WEAKER_MODELS_EXHAUSTED`):

```
CLOSURE_REFUTED_IN_SCOPE
  > CLOSURE_UNDETERMINED_IN_SCOPE
  > CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION
```

A single refuting conjunct outranks every deferral (`False and Unknown ==
False`), and refuted and undetermined conjuncts are tracked in separate fields,
as `InvariantVerificationDecision` tracks `failed_components` and
`deferred_components`, reported in a fixed conjunct order independent of caller
order. Of the 18 combinations, 10 are refuted, 7 are undetermined, and exactly 1
— resolved comparability, exhausted licensed weaker models, and a surviving
residual — reaches the third status.

What this stage does not reach:

```
SatisfiedConjunctsIsNotIndependentClosure
```

Even that one reachable combination yields `is_independent_closure == False`.
The three conjuncts hold *as read*, and reading is all that happened. Three
barriers already declared by the stages that produced these very inputs stand
between that and closure: `OneWitnessIsNotResidualCertification` (G0.RC.1 is
deferred, so no certified residual exists to be closed over),
`SurvivalReadIsNotMeasuredReplicatedResidual`, and `CoverageIsNotCorrectness`
with `FrozenConeIsDeclaredNotProven`. The status name states exactly what was
reached and what it is pending on, rather than overstating it; AIM-K3 is thereby
narrowed by name, not declared met.

`CompositionIsNotAVerdict`. This stage is deliberately not wired to
`BirthVerdictGate`, and the readings it consumes are untouched: their own
`is_independent_closure` properties remain `False` constants.
`ClosureRefutedInScope != NO_BIRTH_IN_SCOPE` — a refuted conjunct is the shape
of an argument against birth in this scope, not that verdict. This stage issues
no `BirthVerdict`, no `BirthCandidate`, no `Freeze`, no `E0` mapping, and no
`TraditionalName`.

## G0.EX — Experimental authority (the third path)

Two authorities existed before this section: a constitutional one that may
certify a birth and run nothing, and an executive one that may use what was
born and certify nothing. Between them there was no place to *try* anything. A
candidate could be argued about but never exercised, and the only way to
exercise it would have been to let execution stand in for birth -- precisely
what `ExecutiveAuthorityCannotIssueBirth` forbids.

G0.EX opens a third path, deliberately weak, whose whole purpose is to run what
has not been born without letting the run prove that it was:

```
DeclaredExperimentalCandidate -> ExperimentalRunRequest
-> CanonicalExperimentalRunRequestEncoder (content id, before the run)
-> ExperimentalRunBindingAuthority (bound to one frozen experiment's content id)
-> ExperimentalAuthority -> ExperimentalRun (operations reached only through an
   authority-issued capability)
-> ObservedExperimentalResult (trace + observed unaccounted cases + failures)
-> ExperimentalEvidenceOffer (canonical manifest of everything observed)
-> [G0.2a.3 acquisition chain]
-> BirthAssessmentRequest -> ... -> BirthVerdictGate -> BirthCertificate
```

A run closes exactly one question, and its answer has exactly one shape:

> this declared candidate, under these declared conditions, on these declared
> inputs, produced this output -- or this failure.

It does not answer whether a genus was born, whether the candidate's identity
is independent, whether it differs from the origin it claims to branch from,
whether it is necessary, whether a weaker model would have sufficed, or whether
anything holds outside the run's own declared scope.

What this buys is a laboratory in which the question *is a new genus necessary*
can be attacked from the negative side cheaply. Two declared models are run
over one case set frozen before either ran: if the model with fewer declared
parts accounts for every case, there is nothing for a richer candidate to be
necessary for, and the matter ends there. If cases survive the first model and
not the second, that is a contrast between two opaque model references over one
declared case set -- which is a reason to open a birth experiment, never a
birth. The kernel names no genus in this section, so no contrast decided here
can say which genus won.

G0.EX.1a (`kernel/experimental.py`) declares the candidate, the frozen case
set, the frozen per-case outcome vocabulary, the capability through which a run
reaches a permitted operation, and the run authority that issues
`ExperimentalRunRecord`. G0.EX.1b (`kernel/experimental_comparison.py`) reads
two runs against each other, and one candidate's repeated runs against
themselves. G0.EX.1c (`kernel/experimental_evidence_gate.py`) is the single
door out: it issues a payload that the existing G0.2a.3 acquisition chain must
still ingest, and it issues no `AuthorizedEvidenceSnapshot` of its own.
G0.EX.1d (`kernel/experimental_request_content_identity.py`) is the one rule by
which two experimental artifacts are the same artifact, and G0.EX.1e
(`kernel/experimental_run_binding.py`) binds one request to one frozen
experiment's content id *before* it runs.

What that binding closes is a provenance leak rather than a naming
inconvenience. A domain holds many frozen experiments; an experiment id holds
many revisions. A gate that reads only the domain would accept a record
produced under one experiment against another experiment's binding, and would
then write that other experiment's name into the offer's own trace. Hence
`SameDomain != SameExperiment` and `SameExperimentName != SameFrozenContent`,
and hence the short form of what an offer now is:

```
ExperimentalEvidenceOffer
  = BoundRun + FrozenExperimentContentIdentity + CanonicalObservedPayload
```

| Law | Status | Scope |
| --- | --- | --- |
| `ExperimentalSuccessIsNotBirth` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | A completed run records observed facts and confers nothing. `ExperimentalRunRecord` exposes `confers_birth`, `confers_validity`, `confers_constitutional_evidence`, `confers_identity_proof`, `confers_difference_from_origin` and `confers_necessity` as structurally `False` derived properties, so the ceiling is read from the object rather than from this table. |
| `ExperimentalFailureIsNotNoBirth` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | A failed or aborted run is recorded, never discarded: `ExperimentalAuthority.run` captures the exception rather than propagating it, and stores an `ExperimentalFailureRecord` naming the failure kind, the case, the message, and the trace up to that point. A failure is not `NO_BIRTH_IN_SCOPE`, and `ExperimentalOutcomeStatus` is about how the run ended, never about whether its result was valid. |
| `ExperimentalCandidateIsNotBirthCandidate` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | No type in G0.EX is, subclasses, or is accepted by anything on the birth path, and `ExperimentalAuthorityError` is a plain `ValueError` rather than a `BirthExperimentSpecificationError`, so an experimental refusal cannot be caught as a birth-protocol refusal. An import sweep asserts that `experimental` and `experimental_comparison` import nothing from the birth, verdict, certificate, closure, survival, exhaustion or acquisition modules, and that no kernel module outside the G0.EX gate imports them. |
| `NoValidityFieldOnAnExperimentalArtifact` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | No experimental type may declare a field named for birth, validity, correctness, certification, rank or verdict. `sweep_forbidden_fields` runs at import over every dataclass in the three modules, so a field added later fails the import rather than quietly conferring a status -- the technique already used to keep `HypothesisResidual` free of a candidate or verdict field. |
| `ObservedUnexplainedCasesIsNotCertifiedResidual` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | `observed_unexplained_cases` is derived by reading each per-case output through a two-token vocabulary frozen in the run request *before* the run, so what counts as "not accounted for" cannot be chosen after seeing the output. An output matching neither token fails the run rather than being reinterpreted. The reading is an observation, never a `ResidualCertificationCandidate`, and it satisfies no condition of `NoBirthWithoutResidualOrFormalNecessity`. |
| `BetterExperimentalFitIsNotNecessity` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | `ModelContrastObservation` derives all four of its case tuples and its status from two authority-issued records over one case set compared by canonical content digest; it accepts no status and no claim. All four statuses, including `B_CLOSES_STRICT_SUPERSET`, expose `confers_necessity`, `confers_birth` and `confers_residual_certification` as structurally `False`. Two runs of the same declared model, or over two separately declared case sets, are refused rather than contrasted. |
| `ObservedDeterminismInThisProcessIsNotReproducibility` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | `ReplayObservation` derives whether repeated runs of one request agreed on output, trace and outcome status. `proves_reproducibility` and `proves_independent_replication` are structurally `False`: agreement inside one process is not determinism, portability, or the independent second measurement run that `SyntheticInterventionMayGenerateHypothesisOnly` requires. One record read twice is refused as a replay, and runs belong to one replay when their requests share one canonical content digest, never because two request objects happened to compare equal. |
| `ExperimentalResultIsNotConstitutionalEvidence` | ENFORCED_AT_EXPERIMENTAL_EVIDENCE_GATE | `ExperimentalEvidenceGate.offer` is the only path out of the experimental path, and it derives every admission condition: the bound request the record was produced from, an offered binding whose content id is the very one that request was bound to, the record's own request content digest, scope equal to the frozen experiment's own domain read from the binding, a replay covering this very record whose outputs, traces and statuses agreed, an authority-issued trace, and a canonical manifest encoded from the record itself. The gate issues no `AuthorizedEvidenceSnapshot` and imports no acquisition type: `OfferedExperimentalEvidence != AuthorizedEvidence != SufficientEvidence != Residual != Birth`, and `FrozenExperimentPrecedesAuthorizedEvidenceIngestion` is preserved unchanged because the G0.2a.3 chain must still ingest the payload. |
| `UnpermittedOperationCannotExecute` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | An operation is reachable only through `ExperimentalRunContext`, the capability `ExperimentalAuthority.run` issues for the case being run: an unpermitted id is refused *before* the action is invoked, the run aborts with `OPERATION_NOT_PERMITTED`, and the refusal is raised as a `BaseException` so an implementation's own `except Exception` cannot swallow it. The authority alone writes the run's `operation:` events and builds `operations_used`; an implementation that writes one into its own trace fails the run under `OPERATION_EVENT_NOT_AUTHORITY_ISSUED` rather than being believed. The capability is revoked when its case ends, so it cannot be stored and used later. This replaces the audited-if-reported reading that preceded it. |
| `NoRunWithoutABoundRequest` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | `ExperimentalAuthority.run` accepts a `BoundExperimentalRunRequest` and refuses a bare request, and it stamps the bound request's canonical content digest onto the record rather than recomputing or accepting one. A run that was never bound therefore cannot be produced, cannot be replayed, and cannot be offered. |
| `SameDomainIsNotSameExperiment` | ENFORCED_AT_EXPERIMENTAL_RUN_BINDING | `ExperimentalRunBindingAuthority.bind` binds one request to one frozen experiment's own `content_id`, and the gate compares that content id with the binding it is offered. Equal domains remain a necessary condition of binding and are never a sufficient one, so a record produced under one experiment cannot be offered against another frozen in the same domain. |
| `SameExperimentNameIsNotSameFrozenContent` | ENFORCED_AT_EXPERIMENTAL_RUN_BINDING | Two revisions of one experiment id freeze two different questions -- a different `BirthQuery`, residual definition, closure criterion, or evidence requirement -- and `BirthExperimentSpecificationContentBinding.content_id` separates them. A binding to one revision authorises no offer against another. |
| `OneRequestIsBoundOnce` | ENFORCED_AT_EXPERIMENTAL_RUN_BINDING | Within one binding authority, one request content identity is bound to one frozen experiment content id; a second binding of the same request to a different experiment is refused rather than recorded, so a single run cannot be attributed two provenances. As elsewhere, `LocalInjectivity != PortableIdentity`. |
| `BindingIsNotEvidenceAndNotBirth` | ENFORCED_AT_EXPERIMENTAL_RUN_BINDING | `ExperimentalRunBindingAuthority` exposes `bind` and its own id, imports no acquisition type, and issues no snapshot, verdict or certificate. `BoundExperimentalRunRequest` exposes `confers_authorized_evidence`, `confers_birth` and `confers_necessity` as structurally `False`: a binding makes a run attributable, never admissible. |
| `OneContentIdentityLawForSameness` | ENFORCED_AT_EXPERIMENTAL_CONTENT_ENCODER | Sameness of an experimental artifact is decided in exactly one place, by exactly one rule: the canonical content digest issued by `CanonicalExperimentalRunRequestEncoder` over `alghanem.canonical_content`. The earlier split -- object identity for a contrast's case set, dataclass equality for a replay's request -- is closed, so two artifacts cannot be the same for one authority and different for another. |
| `NothingEncodedIsSummarised` | ENFORCED_AT_EXPERIMENTAL_CONTENT_ENCODER | Every declared field of a request, including each case's own input content in declared order, the permitted operations and the outcome vocabulary, is encoded structurally rather than joined into one string with a separator. Coverage sweeps run at import over every encoded dataclass in G0.EX, so a field added later fails the import rather than dropping silently out of the identity of the thing it was added to. |
| `NothingObservedIsOmittedFromTheManifest` | ENFORCED_AT_EXPERIMENTAL_EVIDENCE_GATE | The offered payload is the canonical manifest of the request content identity, the candidate declaration, the case set, every case input, the permitted operations, the outcome vocabulary, the outcome status, the output or the failure, the operations the authority recorded, the trace, the replay reading, the contrast reading if present, and the frozen experiment's content id. `CallerDoesNotWriteTheOfferedPayload` therefore now means that two different observations cannot encode to one payload, which delimiter-joined text could not guarantee. |
| `AFailedRunIsStillOffered` | ENFORCED_AT_EXPERIMENTAL_EVIDENCE_GATE | A failed or aborted run may be offered and is marked by the offer's own derived `records_failure`. Dropping failures at the gate would make the record of an experiment better than the experiment was; keeping them changes no verdict, because `ExperimentalFailureIsNotNoBirth` still holds. |
| `ExperimentalAuthorityCannotCertifyOrExecute` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | `ExperimentalAuthority` exposes `run` and its own id and nothing else; `ExperimentalEvidenceGate` exposes `offer` and its own id and nothing else. Both surfaces are checked at import and asserted by test, alongside the unchanged surfaces of `ConstitutionalBirthAuthority`, `ExecutiveAdmissionGate` and `BirthVerdictGate`, which gain nothing from this milestone. |
| `NoBornEntityIsRequiredToRunAnExperiment` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | A run requires no certificate, no `ExecutableEntity`, and no verdict. That is the point of the third path: the laboratory may try what the constitution has not admitted. |
| `ExperimentalRunIsNotExecutionOfABornEntity` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | An `ExperimentalRunRecord` is not an `ExecutableEntity`, cannot be produced from one, and cannot produce one; neither type is a subclass of the other. Running in the laboratory and using what was born remain two acts under two authorities. |
| `PermissionToExperimentAndCertificationAreIndependent` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | A derivation of the four laws above, not a fifth authority and not a gate. Read in one direction, permitting a run does not entail certifying what was run; read in the other, withholding certification does not entail forbidding the run. The witness is the three authority signatures: `ExperimentalAuthority.run` takes no certificate and no verdict and so cannot require one, `ExecutiveAdmissionGate.admit` requires a `BirthCertificate` and so cannot waive one, and `ConstitutionalBirthAuthority.assess` takes no run record and so cannot be reached by a successful run. It does not claim a run is inert afterwards: an `ExperimentalEvidenceOffer` may still travel G0.EX.1c and the G0.2a.3 acquisition chain into a *new* licensed assessment, whose readings are re-derived there rather than carried over from the run. |
| `DeclaredOriginIsNotProvedBranchRelation` | DECLARED_DEFERRED | `declared_origin_ref` is the origin a caller *claims* the candidate branched from, and `ExperimentalCandidateDeclaration.proves_origin_branch_relation` is structurally `False`. Nothing here checks that the origin exists, that a `BranchOriginProvenance` could be derived for the pair, or that the candidate differs from it; `DeclaredCandidateId != ProvedIdentity` likewise. |
| `ExperimentalIsolationIsProcessLocal` | DECLARED_DEFERRED | The authority's isolation is authority isolation and capability mediation: an implementation's exception is captured into a record instead of escaping into the caller's control flow, and an operation reached through the capability is refused before it runs unless the request permitted it. Mediation is not confinement: nothing restricts filesystem, network, memory, or time, and an ambient effect taken without asking the capability is not seen at all. `CapturedFailure != SandboxedExecution`, and a genuine sandbox is a separate, later milestone. |
| `ExperimentalOutputIsSyntheticUnlessItsInputsWereMeasured` | DECLARED_DEFERRED | `CounterfactualResultIsNotObservation` and `SyntheticInterventionMayGenerateHypothesisOnly` apply to experimental output unchanged. Case inputs here are caller-supplied strings with no measurement provenance, so an offered result carries at most hypothesis force; no authority in this section assesses residual survival, weaker-model exhaustion, or replication in a second independent measurement run. |
| `NoGenusNameIsIntroducedHere` | ENFORCED_AT_EXPERIMENTAL_AUTHORITY | Candidate, origin and model references are opaque caller strings, and the kernel defines no genus vocabulary in this section. The instruction-versus-rule question is expressible as a contrast between two opaque model references and in no other way, so `TraditionalNamingOnlyAfterFreezeAndE0` cannot be circumvented by an experiment that names its own winner. |

These laws exist so that a repository which can now run things does not
gradually begin to treat running them as evidence that they deserved to exist.
The formulae are short: `ExperimentalSuccess != Birth`,
`ExperimentalFailure != NoBirth`, `BetterExperimentalFit != Birth`, and
`ExperimentalResult != ConstitutionalEvidence` until one gate, one acquisition
chain, and one constitutional assessment have each done their own work.

## G0.MA — Meta-architecture law (declared law, no runtime yet)

This law governs every future stage that searches for, selects, or names a
pattern, factorization, or architecture -- including any future extension of
G0.BA beyond G0.BA.1a, and any future stage of G0.F. It is declared now, as
law only, with no accompanying type or gate, precisely so that it constrains
those future stages before their first line of runtime code is written.

The recurring risk this law closes: an agent (human or automated) with
foreknowledge of common pattern-discovery techniques -- bigrams, trigrams,
graphs, hypergraphs, transformers, or any other named architecture -- reaches
for one of them because it is familiar, not because the system's own frozen
residuals have forced it. That is exactly the same failure mode `G0.BV.1` and
`G0.BA.1a` were written to refuse for birth verdicts and evaluator execution:
naming or licensing a structure before the evidence that would force it.

The following are declared, law-only constraints; none has a runtime
enforcement mechanism yet:

* `NoPredeterminedPatternArchitecture` -- no future stage may fix, in
  advance, which family of pattern-recognition architecture (bigram,
  trigram, graph, hypergraph, transformer, or any other) will be used to
  discover structure in residuals. The choice must be an output of the
  process, never an input to it.
* `PatternType ∉ PriorOntology` -- the vocabulary of pattern types available
  to a future discovery stage is not fixed by this constitution, this
  codebase, or any prior stage's ontology. A pattern type is only real once
  something forces its birth; it cannot be pre-declared "just in case."
* `NoPatternNameBeforeIndependentBirth` -- a pattern may not be named,
  typed, or exposed as an API surface before an independent birth process
  (mirroring G0.1-G0.BV.1's own chain) has forced it into existence. A name
  is not a license: naming ahead of birth is exactly the failure this law
  refuses.
* `LicensedStructuralDemandConstrainsArchitectureSearch` -- whatever
  architecture search a future stage performs must be constrained by the
  actual licensed structural demand on hand, not by a convenient or popular
  prior architecture. Licensed structural demand is evidence-mode-sensitive
  (`LicensedStructuralDemand_n = Demand(EvidenceMode_n)`), because
  `NoBirthWithoutResidualOrFormalNecessity` already declares three
  independent evidence modes and architecture search must not contradict
  them:
  `Demand(EMPIRICAL) = CertifiedResidualGeometry`,
  `Demand(FORMAL) = CertifiedFormalNecessityWitness`, and
  `Demand(MIXED) = <(D_emp, S_emp), (D_formal, S_formal)>` -- an explicitly
  typed *scoped* pair, not a sum: `S_emp` and `S_formal` are independently
  declared scopes of the claim, with no prior assumption that they are
  disjoint, equal, or exhaustive (the same part of a claim may need both
  formal necessity and empirical support), and
  `NoCrossSubstitution(D_emp, D_formal)` -- neither component may compensate
  for the other on the part of the claim that belongs to it
  (`FormalProof ⇏ EmpiricalReality`,
  `EmpiricalPattern ⇏ MathematicalNecessity`). Licensed demand is not
  claimed to be the only thing constraining search overall: frozen prior
  structure, admissibility, licensed operations, and prior invariants also
  constrain every future search, alongside the licensed demand:
  `Search_{n+1} = ConstrainedBy(FrozenPrior_n, LicensedOperations_n,
  LicensedStructuralDemand_n)`. What licensed structural demand alone
  licenses is new structural complexity:
  `NewStructuralComplexity must be demanded by LicensedStructuralDemand_n`,
  not by `rho_n` alone.
* `NoFixedComplexityOrder` -- no future stage may assume, in advance, an
  ordering of model complexity (for example, "try bigrams before trigrams
  before graphs") as a structural law. Any such ordering, if it appears,
  must itself be derived from evidence, not declared upfront.
* `FuturePossibility != CurrentImplementationLicense` -- that a future
  architecture is conceivable, discussed, or even likely, does not license
  building it now, or building scaffolding for it now. This mirrors
  `RoadmapKnowledge != ExecutionAuthority` below at the level of technical
  architecture rather than agent process.
* `AgentRoadmapKnowledge != ExecutionAuthority` -- an agent's own knowledge
  of where a roadmap is likely headed is not, by itself, authority to
  implement the next stage in the same session that closed the current one.
  What licenses the next stage is the next session's fresh audit of the
  frozen parent's own residuals, not carried-over foresight.

These combine into one governing law for any future architecture search:

```
Architecture_{n+1} = Min_ (relation)
    { A : Preserve(A_n) and SatisfyLicensedDemand(A, D_n)
          and Validation_n(A) }
```

where `D_n = LicensedStructuralDemand_n`. That is: the next architecture is
the *minimal* structure (under whatever partial order the future stage
defines and justifies) that preserves the previous architecture's proven
guarantees, satisfies the licensed structural demand that forced this step,
and passes the evidence-mode-sensitive validation of its own claim.
Satisfaction is itself mode-relative
(`Demand != Residual`: a residual is only the EMPIRICAL special case of
licensed demand, so the satisfaction relation is named neutrally rather than
borrowed from residual logic): in `EMPIRICAL` mode,
`SatisfyLicensedDemand(A, D)` specializes to residual closure
(`Close(A, CertifiedResidualGeometry)`); in `FORMAL` mode, it means that `A`
realizes -- fulfills and instantiates -- the structural necessity that the
`CertifiedFormalNecessityWitness` proved within its frozen formal domain,
not that it "closes a residual" (a necessity witness is not a residual to be
closed); in `MIXED` mode, each component of the typed scoped pair
`<(D_emp, S_emp), (D_formal, S_formal)>` is satisfied by its own mode's
relation within its own declared scope.
Validation is mode-relative
(`Validation_n(A) = Validation(EvidenceMode_n, A)`), matching
`NoBirthWithoutResidualOrFormalNecessity`'s three modes:
`Validation(EMPIRICAL, A) = HeldOutStable(A)` -- the architecture remains
stable under held-out evidence it was not fitted to;
`Validation(FORMAL, A) = ExhaustivelyProvedClosure(A)` -- exhaustive formal
closure over the declared closed domain, with no held-out measurement
required, since a formal birth needs no measurement run; and
`Validation(MIXED, A) = Validation_emp(A | S_emp) and
Validation_formal(A | S_formal)` -- each mode's validation applies to `A`
restricted to its own declared scope, with no assumption here about whether
the two scopes overlap, are disjoint, or are exhaustive, and with neither
substituting for the other. No future stage may skip the
minimality requirement by asserting that a richer, named architecture is
"obviously" going to be needed eventually --
`FuturePossibility != CurrentImplementationLicense` applies here exactly as
everywhere else in this constitution.

One deferred residual is exposed by this reconciliation and recorded here
without being closed: G0.F's stated *general* factorization law below
(`K_L -> Residual(O_L | K_L) -> candidate factorizations`) is still
residual-only and has not yet been reconciled with the `FORMAL`/`MIXED`
birth paths that `NoBirthWithoutResidualOrFormalNecessity` declares
(`G0.F EvidenceModeConsistencyNotAudited`). Auditing and, if needed,
reconciling G0.F's general law is a separate future frozen-parent question;
this section neither modifies G0.F nor licenses doing so now.


G0's chain as written above reads as *one* candidate object, closed
independently and frozen. That phrasing is a special case, not the general
law: a domain `L`'s residual over everything frozen prior to experiment
(`K_L`) does not name in advance how many candidate objects, or which ones,
would close it. Requiring `Residual(O_L | K_L) = 0` may force a single
factor, several jointly-necessary factors, or none at all
(`NO_BIRTH_IN_SCOPE`). This section restates G0's chain, for any domain `L`,
as closing a **minimal sufficient irreducible factorization** rather than a
single named object, and it is held to the same discipline as G0: **law
only**, ahead of any runtime, ahead of any Arabic-specific folder structure,
and ahead of any decision about how many factors traditional grammar expects.

```
K_L -> Residual(O_L | K_L) -> candidate factorizations F (poset-ordered)
    -> Sufficiency(F) & FamilyMinimality(F) & ComponentIrreducibility(F)
    -> IndependentClosure -> BirthVerdict -> Freeze(F*) -> Bridge stage -> E0
```

`Bridge stage`: once (and only once) two factors are each independently
frozen, a *separate* birth protocol -- not automatic adjacency -- decides
whether any relation between them is itself born or merely derived. `E0`
here names a mapping graph from the frozen factor/bridge network to external
(traditional) terminology, not a single rename step. Neither the
factorization runtime nor the bridge runtime nor the E0-mapping runtime is
implemented by this section; as with G0, only the constraints they must
satisfy are frozen now.

| Law | Status | Scope |
| --- | --- | --- |
| `NoTraditionalSchemaBeforeFactorization` | DECLARED_DEFERRED | A domain `L`'s factorization is discovered from `Residual(O_L \| K_L)`, never assumed from a traditional grammatical schema (for example, a presumed phonology/morphology/syntax/semantics split) before that residual is examined. A traditional category name may describe a result after `E0`; it must never seed or constrain the search for one. |
| `NoPredeterminedFactorCount` | DECLARED_DEFERRED | No experiment, spec, or runtime may fix in advance how many factors a domain's minimal factorization contains. `Residual(O_L \| K_L) = 0` licenses `NO_BIRTH_IN_SCOPE` for the whole domain; a nonzero residual licenses exactly the factor family the closure proof produces, whether that is one factor, several, or (pending further evidence) none yet decidable. |
| `FactorizationMinimalityIsPartialOrderRelative` | DECLARED_DEFERRED | The set of admissible minimal factorizations for `L` is `M_L = Min_{≺_L}{F : Sufficient_L(F) and Closed_L(F)}`, where `≺_L` is the domain's frozen partial order over candidate factor families and `Min` selects its minimal elements. `M_L` is never computed as `argmin` of a linear/scalar complexity measure: `ProjectionIsNotOntology`'s ban on assuming a total-order complexity vector across projections applies equally here to factor families. |
| `MultipleIncomparableMinimalFactorizationsDefer` | DECLARED_DEFERRED | If `\|M_L\| > 1` and two members of `M_L` are pairwise incomparable under `≺_L` (neither is derivable from, nor a refinement of, the other under currently licensed weaker models), no verdict may pick one: the assessment is `DEFER_IN_SCOPE`, mirroring `NoRicherStructureBeforeLowerOpenResidualClosure`'s treatment of an incomparable competing explanation, until discriminating evidence resolves the competition. |
| `DerivedRelationDoesNotBirth` | DECLARED_DEFERRED | A relation between two already-frozen factors `F_i`, `F_j` is not itself a candidate for birth merely because both endpoints exist. If the relation's value is fully reconstructible from `F_i`, `F_j`, and shared already-frozen context (`ReconstructibleRelation => Derived, not Born`), it is recorded as a derived relationship (`D*`), not promoted to an ontology object, regardless of how useful or traditionally named that relationship is. |
| `NoBridgeBeforeIndependentEndpointFreeze` | DECLARED_DEFERRED | A `BridgeResidualExperiment(F_i, F_j)` may only be opened after both `F_i` and `F_j` have each already completed their own independent `Freeze`. Endpoint existence as an in-progress candidate, hypothesis, or unclosed factor never licenses opening a bridge experiment between them. |
| `NoBridgeBirthIfReconstructible` | DECLARED_DEFERRED | Given frozen `F_i`, `F_j`, and shared context, if every licensed weaker reconstruction model accounts for the coupling between them (residual `R_ij = 0`), the relation is `DERIVED`, not a `BridgeCandidate`. Only a coupling residual that survives every licensed weaker reconstruction model (`R_ij != 0` after exhaustion) may proceed to `BridgeCandidate -> IndependentClosure -> Freeze`, mirroring `NoBirthBeforeLicensedWeakerExhaustion` for bridges. |
| `FrozenFactorReopeningRequiresNewRevision` | DECLARED_DEFERRED | A frozen factor's content is fixed at freeze time and is never silently mutated by later evidence. New evidence bearing on an already-frozen factor opens a new, separately recorded revision (mirroring `NoBirthBeforeLicensedWeakerExhaustion`'s treatment of a newly discovered weaker model); it does not erase, edit in place, or retroactively rewrite the original frozen verdict's historical scoped record. |
| `LayerIsDiscoveryJurisdictionNotOntology` | DECLARED_DEFERRED | A domain `L` (however named -- "encoding," "phonology," "morphology," or otherwise) denotes only the scope of experiment, evidence, and residual under examination: a `DiscoveryJurisdiction`, not a promise that factorization will reproduce any traditional layer boundary. A single born factor may cut across what tradition calls two layers, or one traditional layer may fracture into several independently born factors; neither outcome is a failure of this law. |
| `E0IsExternalAuditOnly` | DECLARED_DEFERRED | `E0` maps the frozen factor/bridge network to external (traditional or reference) terminology for audit and communication only. `E0` certifies no birth, closure, or freeze decision, and a factor's or bridge's epistemic status never depends on whether, or how, `E0` maps it to an external name. |
| `E0MappingMayBePartialAndManyToMany` | DECLARED_DEFERRED | The `E0` mapping `Π^E0 : FrozenDiscoveryGraph ⇀ ExternalConceptGraph` is a partial relation, not a total function: an entry may be one-to-one, one-to-many, many-to-one, or absent entirely (a frozen factor with no traditional counterpart, or a traditional term matching no single frozen factor). An unmapped frozen factor, or a traditional term left unmatched, is not itself evidence against either side. |
| `RuleTableIsDerivedArtifact` | DECLARED_DEFERRED | Any future "Arabic rule table" is a compiled, read-only projection of the frozen factor set, frozen bridge set, derived-relation set, and `E0` mapping (`ArabicRuleTable = Compile(F*, B*, D*, Π^E0)`), produced strictly after those inputs are frozen. It is never hand-authored ahead of, or independently of, that frozen network. |
| `NoRuleTableFeedbackIntoDiscovery` | DECLARED_DEFERRED | A compiled rule table, or any traditional inventory or category count it reflects, may never feed back into an open experiment, residual criterion, weaker-model set, or factorization search (`ArabicRuleTable ↛ Discovery`, `TraditionalInventory ↛ FactorCount`, `TraditionalCategory ↛ ResidualCriterion`). Discovery in progress must not be steered toward reproducing a table that has not yet been compiled from it. |
| `NoOracleLabelCriterionOrFunctionLeakBeforeFreeze` | DECLARED_DEFERRED | No caller-supplied oracle label, closure criterion, or evaluator function/callable may be substituted for, or silently override, the frozen residual definition, closure criterion, or weaker-model specifications bound at G0.1/G0.2a, for any stage of factorization, bridge, or `E0` assessment. This extends `EvaluatorId != EvaluatorImplementationIdentity` and `CallerDoesNotOwnEvaluatorAuthority` (G0.2a) to the factorization and bridge stages: a caller may declare which evaluator it expects, but never supply, swap, or leak the executing implementation itself ahead of a sealed registry's authorization. |

These fourteen laws are declared now, before any factorization runtime,
`EvaluatorImplementationIdentity`/execution-authority stage (itself still
open per `EvaluatorId != EvaluatorImplementationIdentity` above), typed
residual/provenance stage, bridge-assessment stage, or `E0`-mapping-audit
stage exists. As with G0, no Arabic-specific `phonology`/`morphology`/
`syntax`/`semantics` (or similarly pre-committed) module or folder is created
by this section, and none should be created merely to anticipate a
factorization that has not yet been discovered
(`LayerIsDiscoveryJurisdictionNotOntology`). This section governs, but does
not implement, the milestones that must be built to close it.

### G0.F.1 — Fractal reopen protocol (declared law, contracts only)

G0.F above closes one experiment's factorization question. Fractality is not
a folder layout; it is the same execution law applied recursively: a frozen
result from one experiment must be capable of being read, unmodified, inside
a *later, higher* experiment, without being reborn, copied, or having its
identity re-decided:

```
Birth -> Freeze -> Reopen -> Residual -> MinimalFactorization
-> Freeze -> Reopen -> ...
```

Formally, for a jurisdiction (domain) `L` at level `n`, given the already
frozen set `F_n = {F_1, ..., F_m}` opened in a new jurisdiction `J_{n+1}`:

```
W_0 = Reopen(F_n) + KnownDerivedRelations
R_{n+1} = Residual(O_{n+1} | W_0)
```

`R_{n+1} = 0` licenses `NoBirthAtReopen`: reopening never forces a new layer
to appear. Otherwise the next frozen layer is exactly:

```
F_{n+1} = Freeze(MinimalFactorization(Residual(O_{n+1} | Reopen(F_{<=n}))))
```

which is itself immediately reopenable, making the recurrence indefinite.
Every higher-layer result is exactly one of three kinds, and the three are
never conflated: a `BornFactor` (irreducible under every licensed weaker
reconstruction), a `DerivedRelation` (reconstructible from already-frozen
factors and shared context; `DERIVED_NO_BIRTH`, per `DerivedRelationDoesNotBirth`
above), or a `BornBridge` (a coupling between two independently frozen
factors that survives every licensed weaker reconstruction model). So:

```
FractalGraph = FrozenFactors + DerivedRelations + BornBridges
```

| Law | Status | Scope |
| --- | --- | --- |
| `BirthOnceFreezeOnceReopenMany` | DECLARED_DEFERRED | A factor is born and frozen exactly once; after that, every later experiment that needs it must `Reopen` that one frozen result rather than re-run its birth. Nothing licenses a second, independent birth of what is content-identically the same factor inside the same scope. |
| `ReopenDoesNotRebirth` | DECLARED_DEFERRED | `Reopen(FrozenFactorRef, E_{n+1})` opens a read-only, licensed window onto an already-frozen factor for use in a new experiment; it is not a second construction of that factor and issues no new `BirthVerdict` for it. Formally `Reopen(F) != Rebirth(F)` and `Id_after(F) == Id_before(F)`: reopening a factor can never change the factor's own declared identity, only license a new question about it. |
| `NoBridgeForSequentialInquiry` | PROVED (at contract level) | A later question about a frozen factor is represented only by `ReopenExperimentSpecification` and, once its result is frozen, `ProofLineageEdge`. A proof-lineage edge records discovery history and is not accepted as a `BornBridgeRef` or `DerivedRelationSpec`. |
| `ParentageIsNotOntologicalRelation` | PROVED (at contract level) | `FractalSnapshot` keeps `proof_lineage_edges` separate from `born_bridges` and `derived_relations`: parentage belongs exclusively to the provenance graph and cannot populate the born ontology or derived-relation graphs. |
| `ProofLineageGraphIsAcyclic` | PROVED (at contract level) | `FractalSnapshot` rejects any cycle in `proof_lineage_edges`, including indirect cycles; reopening an ancestor remains valid because it does not add a reverse ancestor edge. |
| `LineageEdgeBindsExactReopenSpecification` | PROVED (at contract level) | Every `ProofLineageEdge` carries one exact `ReopenExperimentSpecification`; the child birth experiment and declared parent are checked against that specification, with no duplicated lineage identity strings. |
| `FrozenOntologyRefIncludesBornBridge` | PROVED (at contract level) | Reopen and proof-lineage parent references may be either `FrozenFactorRef` or `BornBridgeRef`; `DerivedRelationRef` is not an ontology reference and cannot become a lineage parent. |
| `DistinctBridgeExperimentFromEndpointExperiments` | PROVED (at contract level) | `BornBridgeRef` requires a bridge birth experiment identifier distinct from every endpoint birth experiment identifier. This is identifier-level contract evidence only; independent endpoint birth remains deferred until freeze authority exists. |
| `BridgeRequiresIndependentEndpointBirth` | DECLARED_DEFERRED | Independent endpoint birth requires authority to prove the ordering `Freeze(F_i) < BridgeExperiment`; caller-constructible references and distinct identifiers cannot establish that authority claim. |
| `BridgeRequiresResidualBeyondEndpointReconstruction` | DECLARED_DEFERRED | A future bridge gate may freeze a `BornBridgeRef` only after its own G0 experiment shows a coupling residual beyond both endpoints and shared frozen context; a zero residual produces `DerivedRelationSpec`, never a bridge. |
| `NoUpstreamIdentityMutation` | DECLARED_DEFERRED | If `F_i` is frozen, no later result `G` computed from a `Reopen` of `F_i` may modify `F_i`, rename it, reinterpret its identity, merge it with another frozen factor, or change its rank. `G` may only carry `ParentRef(G, F_i)`; new evidence that bears on `F_i` opens a new revision on `F_i` itself (`NewEvidence => NewRevision != HistoricalOverwrite`, consistent with `BirthExperimentSpecification.revision_id`/`revision_sequence`), never a retroactive edit performed by `G`. |
| `HigherExperimentHoldsRefsNotCopies` | DECLARED_DEFERRED | A higher-level experiment or result holds a `FrozenFactorRef` (`factor_id`, `factor_content_id`, `freeze_certificate_id`, `domain`, `birth_experiment_id`, `birth_revision_id`) to a parent factor, never a reconstructed or mutable copy of the parent's own content. `HigherLayerOwnsReference != HigherLayerOwnsIdentity`: owning the reference grants no authority over the referenced factor's identity. |
| `NoTraditionalLayerEnum` | DECLARED_DEFERRED | No fixed enumeration of traditional layers (for example `ORTHOGRAPHY`/`PHONOLOGY`/`MORPHOLOGY`/`SYNTAX`/`SEMANTICS`) may be declared as a closed type in the kernel or Arabic runtime. A domain `L` is identified only by its own frozen experiment/jurisdiction scope (`Layer = FrozenExperimentJurisdiction`); two jurisdictions may later be shown to share a factor without that implying either was ever a case of the other. |
| `FractalParentageDoesNotDefineIdentity` | DECLARED_DEFERRED | A `FractalProvenancePath` records which frozen factors, bridges, derived relations, and reopen experiments produced a later result, strictly for audit and reconstruction of the proof path. `Parentage != Identity`: this path is never part of the later result's own declared identity or content identity, and two results with identical content but different provenance paths remain distinct occurrences, exactly as `EvidenceOccurrenceIdentity != EvidenceContentIdentity` already separates occurrence from content elsewhere in this kernel. |
| `RevisionDoesNotEraseHistoricalFreeze` | DECLARED_DEFERRED | Restates `FrozenFactorReopeningRequiresNewRevision` (G0.F above) at the fractal-reopen level: new evidence discovered through a `Reopen` never edits, deletes, or silently supersedes a parent's historical frozen record. `ContentIdentity_new(F) == ContentIdentity_old(F)` is required for any claim that a later step merely *reopened* `F`; a change in `F`'s own content identity is not a reopen at all -- it is a new revision or a new birth, recorded separately. |
| `ExactFrozenReferencePreservation` | PROVED (at contract level) | `FractalSnapshot` checks a derived relation's or bridge's referenced factor against the *exact* `FrozenFactorRef` recorded in the snapshot -- every declared field (`factor_id`, `factor_content_id`, `freeze_certificate_id`, `domain`, `birth_experiment_id`, `birth_revision_id`), never against a bare `factor_id` string. A reference sharing a `factor_id` but differing in content id, domain, birth experiment/revision, or freeze certificate names a different, unrecognized occurrence and is rejected. `factor_id` equality alone is never sufficient membership proof. |
| `ReopenComposesG0DoesNotForkG0` | PROVED (at contract level) | `ReopenExperimentSpecification` embeds one ordinary, complete `BirthExperimentSpecification` (`experiment`) rather than redeclaring its own `new_question`/`residual_definition`/`closure_criterion` fields. This preserves G0's own revision identity, `EvidenceMode`, `ProjectionPoset`, `BirthQuery`, residual/closure identities, and derived prerequisite cone verbatim, so reopen semantics cannot drift from G0 semantics over time (`G0SemanticsDriftBetweenBirthAndReopen` is closed, not merely avoided by convention). Reopen uses G0; Reopen does not fork G0. |
| `DerivedRelationProvenanceIsContentBound` | PROVED (at contract level) | `FractalProvenancePath.derived_relation_refs` holds `DerivedRelationRef` values (`relation_id` plus `derivation_content_id`), never bare `relation_id` strings. `SameRelationId != SameDerivationSemantics`: two derivations that happen to reuse the same `relation_id` but disagree on `derivation_content_id` are distinguishable, so drift in a derived relation's own recorded content is detectable from its provenance rather than silently trusted by id alone. |

`FrozenFactorRef`, `BornBridgeRef`, `DerivedRelationSpec`,
`DerivedRelationRef`, `ReopenExperimentSpecification`,
`FractalProvenancePath`, `ProofLineageEdge`, and `FractalSnapshot`
(`src/alghanem/kernel/fractal.py`) are contract *skeletons* only: their
constructors validate internal well-formedness (non-blank identities,
non-empty/non-duplicate parent or endpoint sets, exact-reference membership,
and so on), exactly as `BirthExperimentSpecification` and its G0.2a siblings
do ahead of any executable assessment runtime. None of them is issued by a
freeze or reopen authority yet, because no such authority exists: a caller
can construct a syntactically valid `FrozenFactorRef` by hand today, which
proves only that the contract is well-formed, never that a factor was
actually born, closed, and frozen (`ConstructibleContract != IssuedByAuthority`,
equivalently `WellFormedFrozenFactorRef != AuthorityIssuedFrozenFactorRef`).
No code anywhere in the kernel may treat successful construction, or a
passing `isinstance(x, FrozenFactorRef)` check, as proof that a genuine
freeze occurred. A future `FreezeAuthority`/`ReopenAuthority` -- analogous to
`EvidenceAcquisitionAuthority`'s sole-issuer pattern -- is a separate, later
milestone; only that authority may make an issued `FrozenFactorRef`
trustworthy. `FractalSnapshot` contains no `ArabicRuleTable` and no other
compiled artifact; per `RuleTableIsDerivedArtifact` above, any such table
remains a strictly later, derived projection of a frozen snapshot like this
one.

## G0.L2.D — Discriminating the level-two stop (registration-only)

This milestone is registration and derivation only: it issues no birth, no
verdict, no freeze, and no `E0`, and nothing in `kernel/` reads its outputs.

```
ArityArtifact       != LinguisticStructure
RiwayaStopMatch     != DirayaStopMatch
UnfalsifiableStop   != DerivedNegativeResult
TransmittedConflict != MalformedInput
```

`derive_lexical_citation_structure` recognises a chain only at or above
`LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS` (two). A citation carrying one genuinely
transmitted attribution therefore derives the same flat-title structure, and the
same `REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH`, as a card that transmitted
nothing at all — so the level-two stop recorded for «سائمة الغنم» was not
falsifiable by a single real attribution. That is the same shape as the earlier
demand for `متواتر` by name, which made link four permanently impossible rather
than contingently stopped, and the recurrence is now recorded as a pattern with
a prospective question every new gate must answer before it is built: *which
real input falsifies this stop?* A stop no real input can falsify is a tool
limit, not a finding.

| Law | Status | Scope |
| --- | --- | --- |
| `ArityIsNotALinguisticStructure` | DECLARED_DEFERRED | Identical unconstructibility genera derived on either side of a declared arity threshold are an artifact of that threshold, never evidence that one linguistic structure recurred. A stop at one transmitted attribution licenses exactly one reading — the threshold was not reached — and neither refutes nor supports any claim about the composition itself. |
| `IdenticalStopGenusIsNotFractalEvidenceWhileDataIsAbsent` | DECLARED_DEFERRED | Matching stop genera across levels, or across any number of cases, may be read as a candidate structural recurrence (`تطابق_دراية_مرشح`) only when every side transmitted a real chain at or above the threshold. While any side is still empty the match is `تطابق_رواية` — nothing has been written yet — and while any side sits at a single attribution the match stays unsettled. No fractal (Φ) verdict rests on any of the three. |
| `StructurallyUnfalsifiableNegativeIsARecurringPattern` | DECLARED_DEFERRED | Before a gate is built, the input that would falsify its stop must be named. Where no constructible real input can falsify it, the stop reports a limit of the tool and may not be recorded as a derived negative result about the world. |
| `TransmittedConflictIsACaseNotACrash` | DECLARED_DEFERRED | A real transmission path carrying both a specifying and a طردي reading is a case to be read by a named member and a named stop genus, never an exception that halts the mechanism, and never to be resolved silently onto either side. |

The discriminating experiment itself is registered in
`src/alghanem/arabic/level_two_discrimination.py` before any text is
transmitted: one movable variable (the `الإسنادات` enumeration of the
composition card), its fixed elements, and six named branches each stating what
it licenses and what it refuses. Its scope is the (الغنم)/(سائمة) pair alone;
only the match guard is general. As of this milestone no source text has been
supplied, the enumeration is empty, and the registered reading of the standing
branch is that the experiment has not been run.

## G0.FLT-0 — The fractal licensed-transition calibration (invalid preregistration)

This milestone froze a hypothesis text supplied from outside this tree, *verbatim
and including its mathematical notation*, registered the ten pre-run items the
text itself demands, and only then built a readout and ran it. It issues no
birth, no verdict about Arabic, no freeze and no `E0`, and nothing in `kernel/`
reads its outputs.

```
FrozenHypothesisText != EstablishedLaw
StructureMatch       != SurfaceSimilarity
PostHocSimilarity    != FractalEvidence
WeakerReconstruction >= StructureMatch  -> WEAKER_MODEL_RECONSTRUCTS
```

The claim under test is that one transition structure
`K = (Carrier, Gate, Operation, Identity, Evidence, Residual, Trace, Closure)`
survives a change of linguistic scale `S`, i.e. `S ∘ K_n ≅ K_m ∘ S`, restricted
to six fields — Carrier, Gate, Identity, Trace, Residual, Closure — and
explicitly *not* to frequency, entropy, α, number of states, surface form or
magnitude. Four jurisdictions are declared (مقطع، كلمة، تركيب، جملة); only the
first two have a coded carrier in this tree, so exactly one of the three
declared pairs was measurable and the other two were declared `UNDERPOWERED`
before the run, not after it.

**This milestone is a calibration, not a test of the hypothesis.** Direct
inspection of the deposited text found that it diverges from the text that was
supplied: at the site that decides the success condition the requested text
carries an explicit order relation between `StructureMatch` and
`BestWeakerReconstruction`, and the deposited text carries no relation there at
all, while the module simultaneously declares `NotationIsPartOfTheFrozenText`.
So `H_frozen != H_requested`, the digest attests a different text, and the
standing of the run is `INVALID_PREREGISTRATION` — whatever verdict it produced
is a correct reading of *this* code on *these* surfaces and is not attributable
to the hypothesis that was asked for. The divergence is derived from the
deposited text by `fractal_transition_calibration`, not asserted in prose, and
the frozen text is left exactly as it is, because repairing it would erase the
only evidence of the defect.

Three further limits were derived rather than described. The comparison
actually performed is agreement between two boolean predicates on the same
surface across two encoders, not a test of `S ∘ K_n ≅ K_m ∘ S`: no independent
scale-transport contract exists in the kernel, so the finding that some fields
are true by construction diagnoses a weak signature rather than refuting
fractality. `SUPPORTED` is unreachable in this registration by construction,
since every ladder name occurs in the frozen text and no declared pair can
serve as a holdout — an instrument that can refute and cannot support is a
refutation instrument, not a balanced test. And the `Identity` field is a
boolean read from an encoder that never passes the invariant verification gate,
so `DeclaredInvariant != VerifiedInvariant` applies to it directly.

The first run's reading is recorded as it came out, carried whole rather than
erased, with only its attribution withheld. On `syllable-to-word` the
transported structure agreed with the upper layer in 24 of 30 field/case
comparisons, while the weaker `constant-admission` model — which predicts
admission everywhere and reads nothing — agreed in 28. Under the text's own
precedence that is `WEAKER_MODEL_RECONSTRUCTS`, and the run also showed *why*:
in the present codecs Trace and Closure are true by construction, and Gate and
Residual are the same predicate under two names, so four of the six compared
fields cannot discriminate any hypothesis at all. That is a statement about
this tree's encoders, not about Arabic. Because all four ladder names occur in
the frozen text, no declared pair is a holdout, and `SUPPORTED` is unreachable
here by construction rather than by result.

The successor experiment is declared by name and not executed. `G0.FLT-1`
requires a newly frozen verbatim text checked site by site against the supplied
one, an independent `S` contract defined outside the extractors whose
commutation is tested rather than assumed, scales that were not used in
formulating `K` and whose names do not occur in the frozen text, a signature
whose fields can read false on a real input, an `Identity` that is verified or
else yields `UNDERPOWERED`, and surfaces and pairs that were not read in
`G0.FLT-0`. Repairing this criterion and re-running it on the five surfaces
whose results are now known would not produce prospective evidence.

| Law | Status | Scope |
| --- | --- | --- |
| `HypothesisTextFrozenBeforeAnyLayerRun` | ENFORCED_AT_PROBE_PREREGISTRATION | The hypothesis text and the ten preregistered items are content-digested and sealed, and the readout gate re-derives both digests and refuses to read on any drift. The preregistration was committed while no readout module existed, so the ordering is a fact of the history and not a claim in prose. |
| `StructureMatchIsFieldRestricted` | ENFORCED_AT_PROBE_PREREGISTRATION | Correspondence is asserted over the six compared fields only. Frequency, entropy, α, state counts, surface form and magnitude are excluded by name, and a readout that reaches for an excluded field is refused rather than reported. |
| `NoPairIsHoldoutUnderTheFrozenLadder` | DECLARED_DEFERRED | A layer whose ladder name occurs in the frozen hypothesis text cannot serve as a holdout for it. All four declared layers are named there, so no verdict of `SUPPORTED` may be issued from them however well they match; lifting the stop requires a coded pair whose names are absent from the frozen text. |
| `WeakerReconstructionOutranksStructureMatch` | ENFORCED_AT_PROBE_PREREGISTRATION | If any weaker model reconstructs the readings at least as well as the transported structure, the verdict is `WEAKER_MODEL_RECONSTRUCTS` regardless of how high the structure's own agreement was. Agreement is never reported as support while a cheaper model matches it. |
| `AConstructionallyTrueFieldIsNotACorrespondence` | DECLARED_DEFERRED | A compared field that is true by construction at both layers, or that duplicates another field's predicate, agrees trivially and carries no evidential weight. Such fields are named in the readout as non-discriminating rather than counted as matches. |
| `AbsentCodedCarrierYieldsUnderpowered` | ENFORCED_AT_PROBE_PREREGISTRATION | A declared layer with no coded carrier in this tree yields `UNDERPOWERED` for every pair it enters. Absence of a measurement is never reported as agreement, as refutation, or as a reason to substitute a hand-made carrier. |
| `FractalLawProvedIsNotAnOutput` | ENFORCED_AT_PROBE_PREREGISTRATION | The permitted outputs are exactly `SUPPORTED`, `REFUTED`, `UNDERPOWERED` and `WEAKER_MODEL_RECONSTRUCTS`. No run, corpus or aggregate may emit `FRACTAL_LAW_PROVED`, and the frozen text says so in its own words. |
| `ADivergentFrozenTextIsAnInvalidPreregistration` | ENFORCED_AT_PROBE_PREREGISTRATION | A digest taken over a text that diverges from the supplied one at a site deciding the success condition attests a different hypothesis, even when the divergence is a transcription error rather than an intent. The run's standing becomes `INVALID_PREREGISTRATION` and its verdict is withheld from attribution to the requested hypothesis, while the divergent text itself is left unrepaired as the evidence of the defect. |
| `AnUnreachableVerdictIsDeclaredNotDiscovered` | ENFORCED_AT_PROBE_PREREGISTRATION | Which verdicts a registration can and cannot reach is derived and declared with the registration, not learned after the result. An instrument that can reach `REFUTED` but not `SUPPORTED` is named a refutation instrument and may not be presented as a balanced test of the claim. |
| `BooleanAgreementIsNotScaleTransport` | DECLARED_DEFERRED | Agreement between two boolean predicates on one surface across two encoders is not a test of `S ∘ K_n ≅ K_m ∘ S`. Until an independent scale-transport contract exists outside the extractors and its commutation is tested rather than assumed, a degenerate signature is a diagnosis of the instrument and never a refutation of the claim. |
| `DeclaredInvariantIsNotAVerifiedOne` | DECLARED_DEFERRED | An `Identity` field read as a boolean from an encoder is a declaration. Identity preservation counts as evidence only when it passes the invariant verification gate; where it cannot, the pair is `UNDERPOWERED` rather than a hit. |
| `ARepairedRunOnSeenCasesIsNotProspective` | ENFORCED_AT_PROBE_PREREGISTRATION | Once surfaces and pairs have been read, no repair of the criterion makes a re-run on them prospective. A successor experiment requires a newly frozen text and inputs that were not read, registered before it is run. |

The frozen text lives in
`src/alghanem/arabic/fractal_transition_hypothesis.py`, the ten pre-run items in
`src/alghanem/arabic/fractal_transition_preregistration.py`, and the sealed
gate in `src/alghanem/arabic/fractal_transition_readout.py`. The calibration that names this
milestone's own defects, withholds its verdict and derives its capability
envelope is `src/alghanem/arabic/fractal_transition_calibration.py`, and it is
the only sanctioned reader of the run. Neither the text nor the preregistration
may be edited now that the run has happened; a different reading requires a new,
separately frozen preregistration.

## G0.FLT-1 — The licensed Carrier/State centre (preregistration only)

`G0.FLT-0` failed as a test and succeeded as an instrument: it found the defects
of its own experiment before it could find anything about Arabic. What it forced
into view is where fractality could actually be tested — the birth of a higher
centre from lower ones — and this milestone freezes that question **and stops
there**. It issues no reading, no birth, no verdict, no freeze and no `E0`, and
no module in `kernel/` reads it. There is deliberately no readout module in this
deposit: the one thing `G0.FLT-0` got right was the ordering of its commits, and
that is kept.

The law under test is a chain, frozen with its notation:

```
Carrier -> Carrier/State Center -> Licensed Join -> Closure -> Higher Center
```

It is registered as six hypotheses that fail separately rather than one large
claim, so that the success of the easiest cannot cover the failure of the
hardest: `C_0` and `V_0` as quotients whose cardinalities are then tested, `M_0`
as their predicted product, birth under an opening vowel with its negative
control, closure under sukūn, and `M_1` as the closure of a join. `28 × 4` is a
prediction, never an input — the equivalence relation is declared first, the
quotient derived from it, and only then counted; whoever puts the number into
the relation has tested a definition.

The decisive correction over `G0.FLT-0` is that verbatim fidelity is now
*checked* rather than promised. Fourteen decisive notation sites are named one
by one, their presence in the deposited text is derived at import, and the
report can be inspected before any reading exists. `G0.FLT-0` was lost precisely
because a digest was taken over a text nobody had compared against the request.

The negative controls are the point of the experiment, not its footnote. Three
weaker representations — the carrier alone, the state alone, and the unordered
pair — are run on the same surfaces, and a *tie* is enough to defeat the claim
that a licensed Carrier/State pair is the lower centre; superiority of the
weaker model is not required. The name "higher centre" is earned only by
Reconstruction, Minimality, NoBypass and Closure together. Identity preservation
counts only if it passes the invariant verification gate; otherwise the pair is
`UNDERPOWERED`. The seven frozen surfaces are disjoint from the five read in
`G0.FLT-0`, and the disjointness is checked at import rather than entrusted to
attention.

| Law | Status | Scope |
| --- | --- | --- |
| `VerbatimFidelityIsCheckedNotPromised` | ENFORCED_AT_PROBE_PREREGISTRATION | Decisive notation sites are enumerated, their presence derived from the deposited text at import, and the fidelity report made inspectable before any readout exists. A missing site makes the registration unfit to run rather than a formatting matter. |
| `SeparateHypothesesFailSeparately` | ENFORCED_AT_PROBE_PREREGISTRATION | The law is registered as six independently falsifiable hypotheses, each naming what would falsify it, what would make it underpowered, and what would lift that. A single aggregate claim is refused because it lets the easiest component mask the hardest. |
| `TheCountIsTestedAfterTheQuotient` | ENFORCED_AT_PROBE_PREREGISTRATION | The equivalence relation is declared before the run, the quotient derived from it, and only then counted. A predicted cardinality may never appear in the relation that produces it, or the experiment tests its own definition. |
| `AWeakerRepresentationThatTiesDefeatsTheClaim` | ENFORCED_AT_PROBE_PREREGISTRATION | The three weaker representations are registered before the run and evaluated on the same surfaces. Equal performance by any of them defeats the claim that the licensed pair is the lower centre; the weaker model need not win. |
| `FourConditionsOrNoHigherCenter` | DECLARED_DEFERRED | Reconstruction, Minimality, NoBypass and Closure must hold together before anything may be named a higher centre. A failure of one withholds the name rather than weakening it. |
| `NoReadoutExistsForFLT1Yet` | ENFORCED_AT_PROBE_PREREGISTRATION | The registration deposit contains the frozen text and the registration only. A reading built in the same deposit could not testify to its own ordering, so the readout belongs to a later commit. This law was discharged, not repealed: `G0.FLT-1.Q` below repeats the same ordering for its own text, and the test that once asserted the absence of a readout module was restated against repository history rather than deleted. |

The frozen text is `src/alghanem/arabic/flt1_hypothesis.py` and the ten
registered items are `src/alghanem/arabic/flt1_preregistration.py`. `G0.FLT-2` —
syllable to prosodic centre — is named here and not registered; it must reuse
this law rather than redefine it.

## G0.FLT-1.Q — Continuity under an origin, and the birth of an independent branch

`G0.FLT-1` froze the chain `Carrier -> Carrier/State Center -> Licensed Join ->
Closure -> Higher Center` and stopped. That chain treated every transition as a
move *upward*. The reformulation frozen here corrects it: a transition must also
pass a **licensed qiyās between an origin and a candidate branch**, and the
*qādiḥ* difference is something to be **tested**, never something required.

```
Q(O,F) = Sh ∧ Sb ∧ ¬Mn ∧ I ∧ w* ∧ μ(O,F) ∧ ¬Δq(O,F)
```

There are two paths that may not be mixed. `μ ∧ ¬Δq` yields *continuity* under
the origin (`F ⪯_O O`); `μ_base ∧ Δq*` — a qādiḥ difference whose *effect* is
shown, not a merely formal one — opens an independent-branch candidate, and even
then nothing is born until `J ∧ I ∧ Cl` also pass. A third position is forced by
the text and named explicitly rather than smuggled into either path: a
difference that exists but whose effect is unshown is `FORMAL_DIFFERENCE_ONLY`.

The text was superseded, not edited. `flt1_hypothesis.py` keeps its letter and
its digest; the new statement is a second, independent text with its own digest
and an explicit `SupersessionRecord` saying why the exchange was licensed — the
first text had never been read, no readout had run and no number had come out,
so this is a change of hypothesis *before* the test rather than retro-fitting
*after* a result. Had a single result been seen first, the same exchange would
have been the exact offence that sank `G0.FLT-0`.

The first run is recorded as it came out, and it is mixed:

- Of eighteen branches across the seven frozen surfaces, nine read
  `CONTINUITY_UNDER_ORIGIN` and nine `INDEPENDENT_BRANCH_CANDIDATE`.
- No surface earned the name "higher centre". `فَتَحَ` lost `NoBypass` outright —
  the no-join path reproduces `CV-CV-CV` exactly, so for that surface the join is
  ornament. `بَابٌ` lost `Reconstruction` and `Closure` together, because the madd
  seat at position 1 enters no syllable.
- The remaining five surfaces are `UNDERPOWERED`, not successful, because
  `Minimality` is underpowered by construction.
- `w*` and `μ` held everywhere and are reported as **analytic in this deposit**:
  they are true by the template function itself, not by the corpus, so they are
  read and explicitly not counted as evidence.
- Five of the machine's registered outcomes never fired and are listed as
  untested rather than silently passed.

| Law | Status | Scope |
| --- | --- | --- |
| `SupersessionIsNotEditing` | ENFORCED_AT_PROBE_PREREGISTRATION | A superseding statement is a second text with its own digest; the superseded text keeps its letter and digest untouched. Supersession is licensed only while no result has been read from the superseded text, and the record must name what would have made it illegitimate. |
| `TheQadihDifferenceIsTestedNotRequired` | ENFORCED_AT_PROBE_PREREGISTRATION | `Δq` is neither a precondition of success nor of failure; it is asked. Its absence yields continuity under the origin, its presence without shown effect yields a formal difference only, and only a difference whose effect is shown opens an independent branch. |
| `ContinuityIsNotBirth` | ENFORCED_AT_PROBE_PREREGISTRATION | `CONTINUITY_UNDER_ORIGIN` is a verdict in a different register, not a lower grade of `INDEPENDENT_BRANCH_CANDIDATE`. Counting continuity as a failed birth mixes the two paths the law separates. |
| `PrecedenceIsPartOfTheMachine` | ENFORCED_AT_PROBE_PREREGISTRATION | The decision machine's rules are deposited in an explicit, gap-free precedence that is checked at import. Reading one line before another changes the verdict, so ordering is law rather than presentation. |
| `TheTargetIsFrozenBeforeTheScore` | ENFORCED_AT_PROBE_PREREGISTRATION | The reconstruction target is declared before any score and is the same for the licensed and the weaker models. Scoring a weaker model against the licensed model's own output would make the licensed model correct by definition. |
| `AnalyticGatesCarryNoDiscriminatingWeight` | ENFORCED_AT_PROBE_PREREGISTRATION | A gate that holds by the structure of the reader rather than by the corpus is marked analytic in the readout and excluded from evidence, instead of being counted as a passing field. This is the `G0.FLT-0` signature-degeneracy lesson applied to the successor experiment. |
| `AnUnfiredRuleIsAnUntestedRule` | ENFORCED_AT_PROBE_PREREGISTRATION | Registered outcomes that the frozen corpus never triggered are enumerated in the run output. Silence from a branch of the decision machine is not evidence that the branch is sound. |
| `MinimalityIsAsymmetricWhenTheTargetIsNotIndependent` | ENFORCED_AT_PROBE_PREREGISTRATION | Where the reconstruction target is produced by the same reader that embodies the licensed model, the licensed model's advantage is guaranteed by construction. A tie by any weaker representation therefore refutes the claim, while a win by the licensed model leaves `Minimality` `UNDERPOWERED` rather than satisfied. |

The frozen text is `src/alghanem/arabic/flt1_qiyas_law.py`, the machine is
`src/alghanem/arabic/flt1_qiyas_preregistration.py`, and the reading —
committed after both — is `src/alghanem/arabic/flt1_qiyas_readout.py`. Lifting
`Minimality` out of `UNDERPOWERED` requires a reconstruction target that does
not come from the syllabifier; that, and not a larger corpus, is what `G0.FLT-2`
must obtain first.

## G0.NSB-0 — `Σ_L`, the general linguistic nucleus (deposit and registration only)

`G0.FLT-1` and `G0.FLT-1.Q` both treat a licensed `Carrier/State` pair as the
lower centre. The hypothesis deposited here disputes that pair's *rank* rather
than its content: `Representation(x) = (Carrier, State)` answers *how an entity
exists in the system*, and the text argues that a second, independent question —
*what does this entity do as language?* — is not answerable from it. Its own
summary keeps both: `LinguisticObject(x) = Representation(x) + RelationalRole(x)`.

The question "is the nisbah a sort of `Σ_M` or a structure of some `Σ_A`?" is
refused here as a false dichotomy rather than answered. The claim "language is a
system for establishing nisab" is more general than Arabic and more specific
than a law of representation, so it fits neither end. The deposit therefore
opens a third level between them:

```
Σ_M (representation)  ->  Σ_L (relation)  ->  Σ_AR (Arabic instantiation)
```

and the three fail independently: a refuted nisbah claim does not refute the law
of representation, and a refuted Arabic instantiation does not refute `Σ_L`.

The dependency runs one way and is checked rather than described:
`metaalgebra -> linguistic -> arabic`. No module under `src/alghanem/linguistic/`
imports `arabic/`, `kernel/` or the generated tree, and `metaalgebra/` imports
nothing from `linguistic/`; `src/alghanem/arabic/nisbah_relativization.py` is the
single site where the two levels meet, and it is the Arabic layer that reaches
up, never the nucleus that reaches down.

No result is read here. `Σ_L` declares no Arabic term, no `Agent` and no
`Patient`, carries no corpus, computes no score, and no module in `kernel/` reads
it. The negative controls that would make the claim falsifiable are registered
and deliberately not run: the run awaits a held-out corpus that entered neither
the hypothesis nor the earlier `G0.FLT` experiments.

| Law | Status | Scope |
| --- | --- | --- |
| `ThreeLevelsAreNotTwo` | ENFORCED_AT_LINGUISTIC_NUCLEUS | `Σ_M`, `Σ_L` and `Σ_AR` are three independently falsifiable levels, not two with a disputed boundary. `Σ_L` is built on the *digest* of `Σ_M` rather than its name, so a nucleus pointing at any other language of the algebra is refused at construction, and `LinguisticSortsAreNotMetaSorts` refuses at import any sort name shared between the two levels — a shared name would restore the very merge this level exists to prevent. |
| `RelativizationIsNotCompetition` | ENFORCED_AT_LINGUISTIC_NUCLEUS | Ranking a standing result is not refuting it. `G0.FLT-1.Q` keeps its letter, its digest and its read result; there is no `SupersessionRecord` here — a result has been read, and `SupersessionIsNotEditing` licenses an exchange only before that — and no competing-statement record either. `OnlyADemonstratedContradictionCompetes`: while the two answer different questions there is no conflict, and a relativization record that declares a contradiction is refused at construction, because a demonstrated contradiction demands a record of a different kind that no authority in this tree issues. |
| `RelationIsNotRepresentation` | ENFORCED_AT_LINGUISTIC_NUCLEUS | The counterpart of `CarrierIsNotState` one level up, enforced on field *types* rather than field names: `RepresentationRef` and `RelationalRoleRef` are disjoint types, neither may hold a field of the other's type, and the separation is checked at import. Burying a role inside a representation is therefore unsayable rather than refused after the fact, since a name can be changed while the structure stays merged. `RelationalRole.UNREAD` is a declared member, so an unread role is never read as an absent one. |
| `TermAnchorIsWiderThanGenus` | ENFORCED_AT_LINGUISTIC_NUCLEUS | `زيد`, `هذا`, `أنا`, `خمسة رجال` are identity-preserving terms without being genera in the strict logical sense, so the general primitive is `TermAnchor` and genus is one of its branches. The five named branches are `CandidateBranchIsNotABornKind`: declared candidates awaiting a test, never patterns named before the experiment that would birth them. |
| `ArityMustBeLicensedBeforeUse` | ENFORCED_AT_LINGUISTIC_NUCLEUS | A predicate's arity may come from a prior specification, a lexical source, a prior proof, or an independent pre-frozen derivation. Exactly one path is refused by name and at construction: reading the arity off the *target case* after seeing it and then using it to establish that case. The refused path is a declared member of the vocabulary rather than an unwritten assumption, so it fails loudly instead of passing under a general name. |
| `ArgumentRolesAreDeferredToTheirOwnLayer` | DECLARED_DEFERRED | `ArgumentSlot` is a primitive position with no semantic name. No `Agent`, `Patient`, `Cause` or `Result` exists in this nucleus, and naming a slot with one is refused at construction. This keeps `NoPatternNameBeforeIndependentBirth`, and it keeps faith with the standing deferral of `CompoundStage.قيم_النسبة`, which is held open for want of a source text. |
| `ArgumentFillingIsNotClosure` | ENFORCED_AT_LINGUISTIC_NUCLEUS | Relational closure is five components together — arguments closed, operators scoped, constraints licensed, references resolved, no residual active across the boundary. Filling every argument slot is one fifth of the condition, not the condition. Coverage is exact or refused, on the pattern of the kernel's invariant gate: all five are assessed, a missing or duplicated component is refused, and assessment never stops at the first failure, so every failing component is named. |
| `RelationalClosureIsNotIfadah` | ENFORCED_AT_LINGUISTIC_NUCLEUS | Closure yields `PreIfadahClosure` and nothing more; ifādah additionally needs a licensed force and the context it requires, which is why `هل قام زيد؟` has a complete nisbah and asserts nothing. `IfadaVocabularyIsNotDuplicated`: the existing `IfadaStanding` in the Arabic layer stays the only such vocabulary, and the one-way derivation from closure to standing belongs to `Σ_AR`, since building it here would both invert the dependency and create a second copy of one list. |
| `NoConcreteNisbahInTheNucleus` | ENFORCED_AT_LINGUISTIC_NUCLEUS | `Σ_L` says what it *means* to be a term, a predicate or a nisbah, and carries no particular one. A nucleus holding a single instance is a nucleus that has turned into a theory whose shape then constrains every theory written after it — the same refusal `A_SCHEMA_IS_NOT_A_SPECIFICATION` makes one level down. |
| `RegistrationIsNotARun` | ENFORCED_AT_LINGUISTIC_NUCLEUS | The weaker representations that must defeat the claim, and the independence conditions a corpus must meet, are frozen now; no corpus is named, no score computed, no reading emitted. `TheCorpusIsNamedBeforeTheResult` holds the run open until a held-out set is named that entered neither this hypothesis nor the earlier `G0.FLT` experiments, and `AWeakerRepresentationThatTiesDefeatsTheClaim` is reused rather than reinvented: a tie by the carrier alone, the state alone, or an unordered pair defeats the claim, and superiority of the weaker model is not required. |
| `VerbatimFidelityIsCheckedNotPromisedForTheNisbahText` | ENFORCED_AT_LINGUISTIC_NUCLEUS | `VerbatimFidelityIsCheckedNotPromised` (G0.FLT-1) is reused rather than restated, and this row records only that it was discharged here: the decisive notation sites of the deposited text are enumerated one by one, their presence derived from the text at import, and the fidelity report is inspectable before any reader exists. A missing site makes the deposit unfit to be read rather than a formatting matter. The text is also marked an internal hypothesis rather than a transmitted source, so nothing here may be cited as naql. |
| `NoReadoutExistsForNSB0Yet` | ENFORCED_AT_LINGUISTIC_NUCLEUS | The deposit carries the frozen text, the nucleus, the relativization record and the registration of negative controls only. It issues no birth, no verdict, no freeze and no `E0`, and a test asserts that no `kernel/` module reads it. |

The nucleus is `src/alghanem/linguistic/` (`hypothesis`, `role`, `nisbah`,
`closure`, `schema`, `relativization`, `null_model`) and its single Arabic
meeting point is `src/alghanem/arabic/nisbah_relativization.py`. Until the
registered negative controls run on a named held-out corpus, nothing in this
repository prefers the nisbah nucleus to the pair it ranks.

## G0.PK-0 / G0.ONT-0 — The earlier origin: prior organized information, then ontology (deposit and registration only)

`G0.NSB-0` remains standing, unedited and unrefuted. What this section adds is a
level *beneath* it. The nisbah deposit answered "where does the relation sit
between the general algebra and Arabic?" and opened `Σ_L`. A second question
turned out to precede it: *what exists at all that could serve as a genus, an
individual, an attribute, an event, a relation, a quantity or a reference — and
by what criterion is its identity preserved?* That question is not answerable
inside `Σ_L`, because `Σ_L`'s own `TermAnchorKind` already names `GENUS`,
`INDIVIDUAL`, `REFERENCE`, `EVENT_ANCHOR` and `QUANTITY_ANCHOR` as branches of a
linguistic primitive. Those are not purely linguistic sorts; they are
ontological candidates that language *uses* after some earlier layer has fixed
them.

The correction is therefore not a deletion but an insertion, and it splits one
chain into two axes. The existence axis:

```
PK₀ (prior organized information) → O₀ (general ontology)
    → O_L (linguistic ontology) → O_AR (Arabic ontology, deferred)
```

and the algebra axis that operates *on* those objects:

```
Σ_M (representation) ⇝ Σ_L (relation) ⇝ Σ_AR (Arabic instantiation)
```

`Σ_M` is not promoted to an ontological layer here; its job is different. It is
the language of representation, transition, closure, trace and residual in which
these structures are described and checked. The load-bearing consequence is that
`Σ_L` does not *create* `O_L`: it operates on objects that `O_L` has licensed.

`PK₀` is deliberately narrower and stronger than a store of ready-made facts. It
does not say "this thing is a genus"; it records the conditions under which it
is legitimate for a kind called "genus" to be born at all — domain, unit
criterion, identity criterion, attribute possibility, relation possibility,
transformation conditions, conditions and preventers, preserved trace, and the
remainder that blocks closure. Nine places, exact coverage, each naming what it
forbids and the genus of its own license.

This is a deposit, a testbed, and nothing more. It issues no birth, no verdict,
no freeze and no `E0`; no `kernel/` module reads it; and — decisively — it does
not touch `src/alghanem/linguistic/`. The `Σ_L` schema version, its digest, its
frozen hypothesis text and its Arabic meeting point are byte-identical to what
`G0.NSB-0` left. Re-anchoring `Σ_L` to `O_L`, and migrating `TermAnchorKind`
into a licensing reference, are declared next steps, not steps taken here.

| Law | Status | Scope |
| --- | --- | --- |
| `TheAlgebraDoesNotCreateItsObjects` | ENFORCED_AT_EXISTENCE_AXIS | `Σ_L` operates on objects licensed by `O_L`; it does not generate them. An algebra that births its own sorts proves what it assumed. Enforced structurally rather than by prose: `prior/` imports only `canonical_content`, `ontology/` imports only `prior/` and `canonical_content`, neither reads `metaalgebra/`, `linguistic/`, `arabic/`, `kernel/` or the generated tree, and an import-sweep witness checks every direction in both packages. |
| `PriorInformationOrdersPossibilityNotResult` | ENFORCED_AT_EXISTENCE_AXIS | `PK₀` orders the field of possibility and never selects the result in place of the proof. It records the conditions that make the birth of a kind legitimate, not the kind itself. Enforced on field *names* at import: no field in this level may carry a ready-made fact (`genus`, `individual`, `event`, `quantity`, `reference`, `term`, `predicate`, `nisbah`, `arabic`, `root`, `fact`), so depositing the answer where the argument belongs is unsayable rather than refused afterwards. |
| `PriorCoverageIsExactNotBestEffort` | ENFORCED_AT_EXISTENCE_AXIS | The nine places are covered exactly: a missing place is refused with the absent place named, and a duplicated one is refused rather than folded. This reuses the discipline of the kernel's invariant gate and of `ClosureCoverageIsExactNotBestEffort` one axis over: an incompletely covered base would read as complete by inattention. |
| `AConditionNamesWhatItForbids` | ENFORCED_AT_EXISTENCE_AXIS | A condition that forbids nothing constrains no possibility; it is a description read as a constraint by inattention. Every `PriorCondition` names what it forbids and the genus of its license, and `AnUnreadConditionIsNotASatisfiedOne` keeps `UNREAD` a declared member: an unread condition is recorded as unread and never read as met. A condition licensed by the very ontology it licenses is a declared, refused member, so circular licensing fails loudly instead of passing under a general name. |
| `NecessityAndIrreducibilityAreBothRequired` | ENFORCED_AT_EXISTENCE_AXIS | Every `OntologicalCandidate` carries both a necessity claim (why it cannot be dispensed with) and an irreducibility claim (what it cannot be reduced to). Either alone is refused at construction: necessity without irreducibility admits a candidate something else already covers, irreducibility without necessity admits one nothing needs. |
| `AnOntologicalCandidateIsNotABornKind` | DECLARED_LAW_ONLY | Thing, identity, attribute, state, event, relation, role, quantity, reference, transformation, condition, preventer, trace and remainder are *declared candidates awaiting a test*, on the pattern of `CandidateBranchIsNotABornKind` one axis over. Naming them registers what is to be examined; it births nothing and issues no verdict. `UNREAD` is a declared member of the vocabulary. |
| `AnOntologyIsFoundedOnADigestNotAName` | ENFORCED_AT_EXISTENCE_AXIS | `O₀` is bound to the *digest* of the `PK₀` base that licensed it, exactly as `Σ_L` is bound to the digest of `Σ_M`. A base carrying any unlicensed condition cannot found an ontology, and a candidate naming a prior place absent from that base is refused rather than read charitably — an ontology pointing at prior information that no longer stands is an ontology of some other base. |
| `OntologicalKindIsNotLinguisticRole` | ENFORCED_AT_EXISTENCE_AXIS | The counterpart of `RelationIsNotRepresentation` one level down, and enforced the same way — on field *types*, not field names. `OntologicalCandidateRef` and `LinguisticFunctionRef` are disjoint types, neither may hold a field of the other's type, and the separation is checked at import. `AnEventIsAKindAnEventAnchorIsARole` is the concrete case the current `TermAnchorKind` merges: "event" is an ontological kind, "event anchor inside a nisbah" is a linguistic role of that object, and no name may belong to both vocabularies except the declared `unread`. |
| `LicensingIsADirectionNotAContainment` | ENFORCED_AT_EXISTENCE_AXIS | `Genus → TermAnchorRole` is a reasoned license; `Genus ⊆ TermAnchor` asserted as a primitive truth is not. A `FunctionalLicense` carries the registered candidate, the function licensed, the `PK₀` place that licenses it and a non-blank condition statement; `ALicenseWithoutAConditionIsAContainmentClaim` refuses the blank one at construction, because a license that nothing can defeat is containment under another name. A license naming a candidate absent from `O₀`, or disagreeing with that candidate's registered kind, is refused. |
| `FreeTextConditionIsNotALicensedCondition` | DECLARED_DEFERRED | `TermAnchorSignature.identity_condition` and `ArgumentSlot.admissibility_condition` remain free text in `Σ_L`. That is an accepted recording stage, and it is not enough once an ontological proof is claimed, since the system can check neither the truth of free prose nor its relation to prior information. Their migration into references to born, licensed conditions is deferred by declaration, not by neglect. |
| `ALayerThatFoundALayerBeneathItIsNotARefutedLayer` | ENFORCED_AT_EXISTENCE_AXIS | `G0.NSB-0` is a correct layer under which a missing layer was found. Its text, its digest, its schema version and its Arabic meeting point are untouched by this deposit, and a witness asserts that no module under `src/alghanem/linguistic/` imports `prior/` or `ontology/`. Preserving the earlier text preserves the history of the argument, which is worth more than demolishing it. |
| `NoReadoutExistsForPK0Yet` | ENFORCED_AT_EXISTENCE_AXIS | Frozen text, formal structure and registration only. The registered negative controls of `G0.NSB-0` stay unrun and no held-out corpus is named — that question is now premature, because testing kinds born in a layer that is no longer the earliest would test something other than what is claimed. The deposit issues no birth, no verdict, no freeze and no `E0`, and no `kernel/` module reads it. |

The existence axis is `src/alghanem/prior/` (`hypothesis`, `conditions`) and
`src/alghanem/ontology/` (`general`, `linguistic`). It is a testbed: if it holds
under experiment and witness, its adoption as a proof subordinate to the algebra
is a separate, later question that this section does not settle.

## G0.ONT-1 — `Σ_L` re-anchored to `O_L` (deposit and registration only)

`G0.ONT-0` opened the existence axis and stopped there: it said `Σ_L` operates on
objects `O_L` licenses, but `Σ_L` itself still named its own sorts. This section
closes that gap on the algebra side, and it does so *beside* `v1`, not over it.

The migration is structural, and it is deliberately **decoupled from any
empirical threshold**. No measurement can correct a confusion of an object's
nature with its function in language; that correction is carried by the types.
Accordingly, nothing here names a corpus, computes a score, or registers an
acceptance criterion, and the negative controls of `G0.NSB-0` remain suspended.

Three things change in the anchored layer. A term anchor no longer *writes* its
kind: it carries a `LicensedRoleRef` derived from a license in a standing `O_L`,
so `GENUS`, `INDIVIDUAL`, `REFERENCE`, `EVENT_ANCHOR` and `QUANTITY_ANCHOR` stop
being branches of a linguistic primitive and become ontological candidates
licensed for a linguistic function. An identity condition and an admissibility
condition are no longer free prose: each is a `LicensedConditionRef` bound to a
born, licensed `PK₀` condition and to the digest of its base. And the whole
nisbah is bound to a single `O_L` digest, so licenses from two ontologies cannot
be mixed into one structure.

| Law | Status | Scope |
| --- | --- | --- |
| `AnAnchorRoleIsALicenseNotAPrimitive` | ENFORCED_AT_ANCHORED_NUCLEUS | An anchor carries a reference to a license, never a written kind. Enforced on field *types* at import, like `OntologicalKindIsNotLinguisticRole` one axis over: no field in the anchored layer may be typed `TermAnchorKind`, so writing the nature where the license belongs is unsayable rather than refused afterwards. A license granted for one function and read as another, and a license whose function is `UNREAD`, are both refused at construction — an unread license is recorded unread and never read as operative. |
| `FreeTextConditionIsDischargedInV2Only` | ENFORCED_AT_ANCHORED_NUCLEUS | `FreeTextConditionIsNotALicensedCondition` (G0.ONT-0) is discharged here and only here. Every condition field in the anchored layer is typed `LicensedConditionRef` and derived from a standing base, and a condition whose own license genus does not permit use founds no anchor and no slot. `v1` keeps its free text and its `DECLARED_DEFERRED` row unchanged: that row is a true statement about `v1`, and editing it would hide what the earlier stage actually was. |
| `ALicenseOfAnotherOntologyIsNotALicense` | ENFORCED_AT_ANCHORED_NUCLEUS | An anchored nisbah is bound to one `O_L` digest, and every role reference it holds — the predicate's included — must carry that same digest. Mixing licenses from two ontologies builds on a foundation that no longer stands, and identifier equality would let it pass unnoticed. |
| `V2StandsBesideV1NotOverIt` | ENFORCED_AT_ANCHORED_NUCLEUS | `linguistic-nisbah.schema.v2` is built on the *digest* of `v1`, is refused if it reuses `v1`'s version name, and is refused if `v1`'s digest has moved. `v1` is a text that was read, and overwriting a text that was read erases the history of the argument instead of correcting it. An anchored schema that is not bound to an ontology is refused too: it would be `v1` under a new name. |
| `TheAlgebraReadsTheExistenceAxisFromOnePlace` | ENFORCED_AT_ANCHORED_NUCLEUS | Exactly one module of `src/alghanem/linguistic/` reads `prior/` and `ontology/`, and a witness asserts that the reader set is exactly `anchored.py`. The seven `v1` modules stay as they were left. `ontology/` still reads no algebra at all, so the licensing layer is never born from what it licenses. |
| `ArityLicensingIsReusedNotReinvented` | ENFORCED_AT_ANCHORED_NUCLEUS | The anchored predicate reuses `ArityLicenseGenus` and `DEFERRED_ARGUMENT_ROLE_NAMES` from `v1` rather than copying them. An arity read off the target state still licenses nothing, and a slot named for a deferred semantic role is still refused — one vocabulary, not two that drift apart. |
| `NoReadoutExistsForONT1Either` | ENFORCED_AT_ANCHORED_NUCLEUS | Structure only. No corpus is named, no score computed, no acceptance threshold registered, no birth, verdict, freeze or `E0` issued, and no `kernel/` module reads the layer. The question of a threshold is open and unregistered: a figure is not derivable until the unit of count, the reference it is measured against, and the ruling on unread units are named. |
| `AnAbsoluteThresholdIsNotAMargin` | DOCUMENTED_OPEN_QUESTION | Recorded so the open question is not lost. An absolute match level cannot on its own license an adoption, because `AWeakerRepresentationThatTiesDefeatsTheClaim` (G0.NSB-0) already holds: a weaker model that *ties* defeats the claim, so a high level reached alongside a tying null model is a defeat, and a lower level reached against four beaten null models is not. Any future criterion must carry both an absolute floor and a margin over each of the four registered null models separately — not over their best, and not over their mean. |

The anchored layer is `src/alghanem/linguistic/anchored.py`. `§G0.NSB-0` and
`§G0.PK-0 / G0.ONT-0` both remain standing and unedited.

## G0.ONT-2 — the origin chain closed (registration only)

`G0.ONT-1` removed free prose from the conditions the algebra reads, but left
two remainders. First, the prose did not disappear from the chain; it moved one
step back, into `FunctionalLicense.condition_statement`, so a license could
still be founded on an interpretive sentence rather than on a standing
condition. Second, a nisbah bound its role references to one `O_L` digest, yet
nothing forbade its *conditions* from coming out of a different prior base than
the one that `O_L` was founded on. Digest unity inside the nisbah is not origin
unity along the chain.

This section closes both remainders, and it closes them **beside** `v2`, never
inside it. Four modules are added — `prior/references.py`,
`ontology/linguistic_v2.py`, `ontology/lineage.py`,
`linguistic/anchored_v3.py` — and not one historical file is edited. Nothing
here names a corpus, computes a score, or registers a threshold; the negative
controls of `G0.NSB-0` remain suspended.

The chain that becomes readable is `PK₀ → PriorConditionRef → O₀ → O_L² →
ExistenceLineageRef → Nisbah_v3`, and every arrow in it answers two questions:
by whom was it licensed, and what is the identity of the origin it was licensed
from.

| Law | Status | Scope |
| --- | --- | --- |
| `AHistoricalLayerKeepsItsDependencySemantics` | ENFORCED_AT_ORIGIN_CHAIN | Preserving a layer is preserving its own bytes *and* the identity of everything it depends on. A file left untouched whose imports moved beneath it no longer means what it meant, and its preserved bytes then testify to something that is no longer there. A witness freezes the digest of every module in `anchored.py`'s transitive internal import closure, asserts the closure gained no new member, and asserts `v1` and `v2` schema digests did not move. This is why `ontology/linguistic.py` is not edited: `anchored.py` imports it, so editing it would silently rewrite what `v2` says. |
| `AConditionReferenceBelongsToThePriorBase` | ENFORCED_AT_ORIGIN_CHAIN | The type that references a prior condition lives in `prior/`, not in the ontology that consumes it. Prior information is a condition of the mental operation, not a product of the layer built on it; a reference minted by the consumer would let the consumer decide what it is allowed to depend on. |
| `ALicenseIsFoundedOnAStandingLicensedConditionNotOnProse` | ENFORCED_AT_ORIGIN_CHAIN | `ReferencedFunctionalLicense` has no `condition_statement` and no `licensing_condition`: it carries a `PriorConditionRef` naming the very condition that licensed it, its place, its base, and that base's digest. Every license can therefore answer *which condition licensed me, from which base, with what digest*. A condition whose own license genus does not permit use founds no license. |
| `AReferenceIsDerivedNotConstructed` | ENFORCED_AT_ORIGIN_CHAIN | Authority is a condition of a reference coming into being, not a property attached to it afterwards. `PriorConditionRef`, `ExistenceLineageRef` and `BaseSchemaRefV3` are issuable only through their `of(...)` derivation; direct construction raises rather than yielding a structurally valid but non-standing reference. Permitting a forgeable twin of an authoritative type would make the type itself mean less. |
| `ALicenseAndItsConditionShareOneBase` | ENFORCED_AT_ORIGIN_CHAIN | `LinguisticOntologyV2` carries the prior-base reference of its general ontology, and refuses any license whose condition reference names a different base id or a different base digest. A base of the same name and another digest is another base. All offending licenses are named, not only the first. |
| `OriginUnityIsNotOntologyUnity` | ENFORCED_AT_ORIGIN_CHAIN | `ExistenceLineageRef` records the three levels the chain passed through — prior base, general ontology, linguistic ontology — with the id and digest of each, and is derivable only from a linguistic ontology actually founded on the given general ontology. `AnchoredNisbahSignatureV3` then refuses any role reference from another ontology *and* any condition reference from another base, naming every offender. `v2` admits the mixed case; `v3` refuses it, and a paired witness shows exactly that. |
| `ALineageIsNotEditedItIsExtended` | ENFORCED_AT_ORIGIN_CHAIN | The lineage is a separate object standing beside the ontologies, not a field added inside them. A chain that can be extended in place by a later stage stops being evidence of what it was when it was read; a further level is a new type carrying this one, never a mutation of it. |
| `V3StandsBesideV2NotOverIt` | ENFORCED_AT_ORIGIN_CHAIN | `linguistic-nisbah.schema.v3` is built on the *identity* of `ANCHORED_NISBAH_SCHEMA` read from the living parent, is refused if it reuses `v2`'s version name, and is refused if the parent's digest has moved. Reading the parent's identity is not using the parent's implementation: `anchored_v3.py` imports exactly one name from `anchored.py`, and builds nothing with `v2`'s constructors. |
| `TheAlgebraReadsTheExistenceAxisFromNamedPlacesOnly` | ENFORCED_AT_ORIGIN_CHAIN | The reader set of the existence axis inside `src/alghanem/linguistic/` is now exactly `anchored.py` and `anchored_v3.py`, and a witness asserts that set literally. The seven `v1` modules stay as they were left, and `ontology/` still reads no algebra at all. |
| `NoBirthLanguageAtThisStage` | ENFORCED_AT_ORIGIN_CHAIN | A `PK₀` condition is *registered*, *standing*, *usable*, *licensed* — never *born*. No birth gate exists at this stage, so calling a condition born would grant it a rank that nothing has yet conferred. The new modules and this section use the registration vocabulary only. |
| `NoReadoutExistsForONT2Either` | ENFORCED_AT_ORIGIN_CHAIN | Structure only. No corpus, score, threshold, birth, verdict, freeze or `E0`, and no `kernel/` module reads the layer. Whether `O_M` can be founded above `O_L²` — and what minimum it must add before positing, parthood, externality and entailment can arise rather than be assumed — is open and unregistered. |

`§G0.NSB-0`, `§G0.PK-0 / G0.ONT-0` and `§G0.ONT-1` all remain standing and
unedited, including `G0.ONT-1`'s own description of `v2`.

## Encyclopedia Nucleus — Constitution

The encyclopedia is an application consumer of the kernel, never a replacement
for it. Its minimal state is:

```
EncyclopediaNucleusSnapshot = FractalSnapshot + GrowthFrontier
GrowthFrontier = RootInquiries + ReopenInquiries
```

`FractalSnapshot` remains a discovery graph, not a knowledge graph. It holds
only frozen discovery contracts, whose construction remains non-authoritative
until the future birth and freeze authorities exist. The frontier holds open
questions. Frontier immutability is a contract property; preserving an inquiry
after a `DEFER` verdict is deferred until a growth transition mechanism exists.

| Law | Status | Scope |
| --- | --- | --- |
| `NoDedicatedTraditionalSchemaFields` | PROVED (at contract level) | The encyclopedia namespace has no dedicated domain, ontology, or human-science label fields. |
| `NoSemanticLabelLeakThroughIdentifiers` | DECLARED_DEFERRED | Identifiers are opaque keys, not semantic evidence; a future registry and evaluator authority must ensure their values cannot influence discovery. |
| `QuestionGenerationIsNotAuthorization` | PROVED (at contract level) | `QuestionProposal` has no experiment or execution field. `RootInquiry` requires a `BirthExperimentSpecificationContentBinding`, which proves its complete G0 specification exactly matches registry-frozen pre-evidence content. |
| `QuestionGrowthUsesReopen` | PROVED (at contract level) | Later questions around frozen results are represented by kernel `ReopenExperimentSpecification`; sequential inquiry is not an ontological bridge. |
| `FrontierReopenParentMustExistInSnapshot` | PROVED (at contract level) | Every reopen parent in the frontier must exactly equal a frozen factor or born bridge reference present in the paired `FractalSnapshot`; identifier equality alone is insufficient. |
| `FrontierImmutability` | PROVED (at contract level) | The frozen frontier contract cannot be mutated after construction. |
| `DeferPreservesOpenQuestion` | DECLARED_DEFERRED | A future `EncyclopediaGrowthTransition` must retain an inquiry after a `DEFER` result; no verdict-to-frontier transition exists yet. |
| `NoKnowledgeBeforeLicensedClaim` | PROVED (at contract level) | The nucleus contains no claim or knowledge fields. Frozen factors are not knowledge states. |
| `NoTextBeforeKnowledgeProjection` | PROVED (at contract level) | The nucleus contains no article or text fields; rendering is a later projection and cannot create knowledge. |
| `NoIndexFeedbackIntoDiscovery` | DECLARED_DEFERRED | A future index or renderer may project licensed knowledge but may not authorize or alter discovery. |

`src/alghanem/encyclopedia/inquiry.py`,
`src/alghanem/encyclopedia/frontier.py`, and
`src/alghanem/encyclopedia/snapshot.py` intentionally define no growth engine,
domain taxonomy, knowledge graph, article store, or evaluator authority.
`EncyclopediaGrowthTransition` is the deferred future boundary for applying
authorized kernel outcomes to a nucleus snapshot.

## Encyclopedia Self-Observation — Constitution

`Alghanem` is not exempt from its own encyclopedia's discipline: the
repository the encyclopedia is implemented in is itself a legitimate future
`ObjectOfInquiry`. But a four-way separation must hold before any claim
about the repository can be licensed as knowledge:

```
System != RepositoryRepresentation != SelfModel != KnowledgeAboutSystem
```

A GitHub repository is a `SourceArtifact` carrying traces of the system; a
commit is one exact `SourceVersion`; a file is a `SourceFragmentCarrier`;
a line, node, or function is an `EvidenceCandidate`
(`CodeFragment != Evidence` until a future claim-specific
`EvidenceBinding` exists). This module intentionally goes no further than
naming these carriers:

```
RepositorySnapshot -> Evidence -> Claim -> EpistemicLicensing -> SelfKnowledge
```

`src/alghanem/encyclopedia/self_observation/` defines only the first link,
`RepositorySnapshotRef` plus the artifact/fragment/transition refs anchored
to it. It defines no `Claim`, `EvidenceBinding`, or `SelfEpistemicState`
runtime; those remain a later, separate `SelfKnowledgeBridgeExperiment`
milestone, built only once a claim/evidence constitution exists.

| Law | Status | Scope |
| --- | --- | --- |
| `RepositorySnapshotIsNotKnowledge` | PROVED (at contract level) | `RepositorySnapshotRef` has no claim, evidence, or knowledge field; it names one explicitly-addressed repository state and nothing else. |
| `RepositoryArtifactIsNotEvidenceByItself` | PROVED (at contract level) | `RepositoryArtifactRef` and `RepositoryFragmentRef` name a file or fragment carrier only; naming a fragment proves nothing about any claim until a future `EvidenceBinding` exists. |
| `DocumentationIsNotImplementation` | DECLARED_DEFERRED | A future claim constitution must keep `DeclaredSelfModel` (from `docs/CONSTITUTION.md` and other prose) distinct from `ImplementedSelfModel` (from source); this module records neither yet. |
| `TestPassIsNotUniversalTruth` | DECLARED_DEFERRED | A future evidence constitution must keep `TestedSelfModel` (from passing tests/CI at one commit) distinct from `FormalProofEvidence` and from universal correctness; no test-evidence field exists yet. |
| `SelfModelIsNotSystem` | PROVED (at contract level) | `RepositorySnapshotRef`, `RepositoryArtifactRef`, `RepositoryFragmentRef`, and `RepositoryTransitionRef` are all references anchored to a commit; none of them is, contains, or executes the repository itself. |
| `SelfDescriptionDoesNotGrantAuthority` | PROVED (at contract level) | This module defines no freeze, reopen, or mutation authority; constructing or observing any of its refs grants no permission to alter the kernel or encyclopedia they describe. |
| `RepositoryVersionMustBeContentBound` | CONSTITUTIONAL REQUIREMENT | Every ref in this module is anchored to an explicit `commit_sha` (never a branch name); `RepositoryArtifactRef` and `RepositoryFragmentRef` are anchored to their exact snapshot, and `RepositoryTransitionRef` requires distinct `from_snapshot`/`to_snapshot` commit shas. This requirement is only *proved* at the weaker `RepositoryVersionIsExplicitlyAddressed` level below; full content authentication remains `RepositoryVersionIsContentAuthenticated` (DECLARED_DEFERRED). |
| `RepositoryVersionIsExplicitlyAddressed` | PROVED (at contract level) | `RepositorySnapshotRef` and `RepositoryArtifactRef` require non-blank `commit_sha`/`tree_sha`/`blob_sha` fields, each anchored to an explicit version, never a bare identifier without context. |
| `RepositoryVersionIsContentAuthenticated` | PROVED (within provider scope) | `RepositoryObservationAuthority` opens an authority-issued `RepositoryObservationRun`; the run verifies repository→commit→tree and tree/path→blob, and issues authenticated snapshots/artifacts only after those checks. This remains scoped to the provider's returned observations, not universal repository truth. |
| `SameRepositoryIdentity` | PROVED (at contract level) | `RepositoryTransitionRef` requires `from_snapshot.repository_identity == to_snapshot.repository_identity`; a pair naming two different repositories is rejected, not silently accepted as a transition. |
| `DifferentCommitsIsNotHistoricalTransition` | PROVED (within provider scope) | `RepositoryTransitionRef` remains address-only; an `AuthenticatedRepositoryTransition` requires two authenticated snapshots from the same observation run and a provider ancestry witness. Distinct commit shas alone remain insufficient. |
| `AuthenticatedObservationIsNotEvidence` | PROVED (at contract level) | Authenticated snapshots, artifacts, fragments, and transitions contain no claim or evidence binding; authentication of repository structure does not make an observation evidence or knowledge. |
| `ProviderDeclaredImplementationIdIsNotExecutionIdentity` | DECLARED_DEFERRED | `implementation_identity` is provider-declared provenance metadata. This milestone does not independently bind that string to the implementation that executed the run. |
| `ArtifactChangeRecordsBothSides` | PROVED (at contract level) | `RepositoryArtifactChangeRef` requires both a `before` (anchored to `from_snapshot`) and an `after` (anchored to `to_snapshot`) `RepositoryArtifactRef`, sharing the same `artifact_path` with distinct `blob_sha`s, so a delta can be reconstructed instead of only naming the post-change file. It also independently requires `before.snapshot.repository_identity == after.snapshot.repository_identity` and distinct `commit_sha`s, so a well-formed change pair is coherent even when constructed outside a `RepositoryTransitionRef`. |

`RepositoryTransitionRef` records `changed_artifacts` (as
`RepositoryArtifactChangeRef` before/after pairs), `added_artifacts`, and
`removed_artifacts` between two explicitly-addressed snapshots of the *same*
repository, but `Change != Improvement`: it makes no claim that a later
commit is better, safer, or more correct than an earlier one.
`RevisionDoesNotEraseHistoricalFreeze` follows directly from
`RepositoryVersionMustBeContentBound`: a later snapshot never invalidates
what a licensed claim once said about an earlier one, because the two are
distinct, equally addressable versions. A path renamed or moved between
`from_snapshot` and `to_snapshot` (`SameContent+DifferentPath`) is
deliberately out of scope for `RepositoryArtifactChangeRef`, which requires
an identical `artifact_path` on both sides; a future
`RepositoryArtifactMoveCandidate` would carry that separate identity
question.

## G0.ST — Two standing axes: structural and empirical (declared law, no runtime yet)

This law separates two questions that this repository has so far allowed to
share one answer slot: *is a claim proved relative to a frozen specification?*
and *has a claim been checked against something measured outside that
specification?* They are independent axes, and neither is a weaker or stronger
version of the other.

```
StructuralStanding          != EmpiricalStanding
SpecificationIndependence   != EmpiricalTargetIndependence
TheoremValidity             != InstantiationCoverage
```

The recurring failure this law closes is visible in the VV experiment already
registered in `src/alghanem/arabic/vv_birth_hypothesis.py`: a missing
independent *empirical* target (`INDEPENDENT_TARGET_MISSING`) was read as a
ceiling on the whole claim, including the part of it that is a statement about
a frozen algebra and owes nothing to any corpus, microphone, or articulatory
measurement. `G0.MA` already declares the one direction
(`FormalProof ⇏ EmpiricalReality`); the converse was never written down, and
its absence is what let an empirical gap silently lower a structural claim.

What a structural standing requires instead is that the *obligation* be
independent of the function claiming to discharge it. A transition's contract
— its domain condition, licensing gate, preserved invariants, trace obligation
and residual policy — must be frozen, with its own content identity, before the
transformation that claims to satisfy it exists. A contract written after its
function is not a contract, in exactly the sense in which a rival model written
after the result is not a rival (`A_RIVAL_WRITTEN_AFTER_THE_RESULT_IS_NOT_A_RIVAL`).

A structural standing is therefore never absolute. It is always relative to a
named, content-identified specification set `Σ` and a declared scope, and the
vocabulary carries that relativity in the name of the value itself rather than
in a footnote beside it.

| Law | Status | Scope |
| --- | --- | --- |
| `MissingEmpiricalEvidenceIsNotMissingStructuralProof` | DECLARED_LAW_ONLY | The absence, unavailability, or circularity of an independent *empirical* target caps the empirical axis alone. It may not lower, block, defer, or qualify a standing on the structural axis. `INDEPENDENT_TARGET_MISSING` on the empirical axis is consistent with `STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA` on the structural axis, and a reader who treats that pair as a contradiction has merged two axes this law keeps apart. The converse direction — `FormalProof ⇏ EmpiricalReality`, declared in `G0.MA` — remains in force unchanged; this law adds only the direction that was missing. |
| `SpecificationIndependenceIsTheStructuralIndependence` | DECLARED_LAW_ONLY | The independence a structural claim requires is that its obligation was fixed independently of the function asserted to satisfy it: the contract `(Pre, Post, Inv, Cl, Trace)` frozen, with content identity, before that function existed. An external measured target is not required, and supplying one does not substitute for a frozen contract. A contract derived from, fitted to, or edited after its own implementation establishes nothing (`A_CONTRACT_WRITTEN_AFTER_ITS_FUNCTION_IS_NOT_A_CONTRACT`). |
| `EmpiricalTargetIndependenceIsEmpiricalOnly` | DECLARED_LAW_ONLY | Independence of a reconstruction target from the candidate model's own rules remains a condition on the empirical axis, where it was introduced. It constrains nothing on the structural axis and may not be imported there under another name. |
| `NoStructuralStandingWithoutItsFrozenSigma` | DECLARED_LAW_ONLY | No structural standing may be recorded without naming the frozen specification set it is relative to, together with that set's content identity and declared scope. There is no unrelativized structural `PROVED` in this repository; a value whose name omits its `Σ` is refused rather than interpreted generously. |
| `NoAxisCollapse` | DECLARED_LAW_ONLY | The two standings may not be stored in one field, summed, ordered against one another, or derived one from the other in either direction. A type carrying a single combined verdict over both axes is refused at construction, not corrected at read time. |
| `TheoremValidityIsNotInstantiationCoverage` | DECLARED_LAW_ONLY | That a theorem is stated and proved symbolically for all `n` is one fact; that the repository currently instantiates it for some particular number of layers or transitions is a second, independent fact. Low coverage is not a defect in the theorem, and high coverage is not a substitute for proving it. Both must be reported, separately named, and neither may stand in for the other. |
| `SpecificationIndependenceGradeIsHistoricalNotRetrofittable` | DECLARED_LAW_ONLY | The strongest grade, prospective specification independence, is available only where the frozen contract demonstrably predates the implementation. An implementation that already existed when its contract was frozen may reach at most `RETROSPECTIVE_CONFORMANCE` — it conforms to the contract, and that is all that was shown. Recording the stronger grade for such an implementation would make preregistration retroactive, which is the failure preregistration exists to prevent. |

`G0.ST` declares law only. It installs no gate, promotes no existing claim, and
re-labels no row in any table above; the vocabulary that carries these axes in
code (`src/alghanem/metaalgebra/standing.py`) is registration-only and issues no
judgment of its own.

## G0.T.0 — Intended theorem for the pure derivational core (DRAFT — NOT LAW)

**Status: DRAFT_TEXT_ONLY.** This section is a text experiment, not a law and
not a merged constitutional clause. It adds no row to any law table, changes
no gate, authorizes nothing, and grants no epistemic promotion. Its only
purpose is to find out whether the intended theorem can be *stated* at all in
current kernel terms. Nothing here is proved; where this text asserts, it
asserts as a declared assumption.

### Scope of the draft statement

The kernel divides, for provability purposes, into two halves that must not
be conflated:

- a **pure derivational core** — `BirthVerdictGate.assess` and
  `IndependentClosureGate.assess`, which read no evidence payload and compute
  their status from frozen specification fields alone; and
- an **opaque oracle edge** — registry-bound invariant extractors, evaluator
  input derivations, and evaluator implementations, which are arbitrary
  callables with no declared denotation (`ObservedDeterminism != ProvenPurity`).

This draft states a theorem about the first half only. The second half enters
only as explicitly assumed axioms (§ *Assumed oracle axioms*), never as
proved content.

### T-1 (intended, unproved) — Verdict derivation is specification-local

> For every `BirthAssessmentRequest` `r` that is successfully constructed, and
> every `SealedBirthVerdictScopeRegistry` `R` that resolves a scope `s` for
> `r`'s own `(domain, experiment_content_id)`, the `BirthVerdictDecision`
> issued by `BirthVerdictGate.assess(registry=R, request=r)` is a total
> function of `r.specification.competing_projections` and
> `r.specification.frozen_weaker_models` alone — both of which are derived by
> `BirthExperimentSpecification` from its own frozen `projection_poset` and
> `birth_query`. In particular the decision's `status` and `reason` are
> independent of `r.evidence_snapshot`'s payload, of every evaluator, every
> derivation, and every extractor, and of `R`'s other scopes.

**T-1′ (companion, same shape).** The same statement holds for
`IndependentClosureGate.assess` with `ComparabilityClosureStatus` in place of
`BirthVerdictStatus`.

**Intended corollary (weak).** Because the codomain reachable by the current
gate is the single value `DEFER_IN_SCOPE`, T-1 currently entails no claim
about any birth. The theorem is stated now so that its *shape* is fixed before
`BIRTH_IN_SCOPE` becomes reachable; today its subject matter is deferral.

**What T-1 does not say.** It does not say the verdict is *correct*, *sound*,
*justified by the evidence*, or *consistent with its inputs* in any sense
richer than "computed from these frozen fields". `SpecificationLocality !=
EvidentialConsistency`. It is a non-interference/locality statement, not a
soundness statement.

### Assumed oracle axioms (declared, not proved)

Any future statement that reaches past the pure core must discharge or assume
these. They are recorded here as assumptions precisely because the kernel
cannot establish them:

This list is written as prose, not as a table: the document's table grammar
is a closed vocabulary of declared headers, and inventing a new header shape
for a draft would either be refused outright or silently widen that grammar.

- `OracleTotality` — *assumed*: a registry-bound extractor, derivation, or
  implementation returns a value for every input it is invoked on. *Not proved
  here*: bound callables are arbitrary Python and may raise or diverge. The
  kernel converts raising into `DEFER`, which records an epistemic non-answer
  rather than establishing totality.
- `OracleDeterminism` — *assumed*: a bound callable returns equal output for
  equal input, across invocations and processes. *Not proved here*:
  `EvaluatorInputDerivationGate` observes one repeat invocation only and
  explicitly records `ObservedDeterminism != ProvenPurity`; nothing excludes
  hidden state, clock, or environment dependence.
- `OraclePurity` — *assumed*: a bound callable has no effect on kernel or
  external state. *Not proved here*: Python imposes no effect discipline and
  the kernel performs no static analysis of bound callables.
- `OracleIdentityFaithfulness` — *assumed*: a declared
  `implementation_identity` names the code that actually ran. *Not proved
  here*: declared identity is caller/provider metadata; the kernel compares
  strings, it does not attest the executing artifact.
- `SchemaDenotation` — *assumed*: declared schema strings (`result_schema`,
  `residual_schema`, `model_result_schema`, `output_schema`) denote sets of
  values, and a returned value lies in the denoted set. *Not proved here*:
  these fields are opaque text compared only by equality; no interpretation
  function from schema text to a value set exists anywhere in the kernel.
- `FailureSemanticsDenotation` — *assumed*: `failure_semantics` and
  `declared_information_loss` denote something a judgment could be checked
  against. *Not proved here*: same — declarative text, never interpreted.

An oracle-touching theorem is therefore, at best, of the form
"assuming `OracleTotality ∧ OracleDeterminism ∧ …`, then …". None of these
assumptions is currently testable inside the kernel, and asserting them is not
weaker than asserting the conclusion by inspection.

### Where the intended statement is not expressible (the actual finding)

Writing T-1 exposed that the *originally intended* theorem — "every
successfully constructed request yields a judgment consistent with its
inputs" — cannot be written down in current kernel terms. The following
phrases have no referent here, and each needs a different remedy:

- **"consistent with its inputs"** — there is no relation in the kernel
  between an evidence payload and a verdict. The gate never reads the payload,
  and no predicate `Consistent(evidence, verdict)` is definable because
  evidence bytes are deliberately uninterpreted. *Remedy*: an interpretation of
  evidence content — a genuine denotational layer — which G0 deliberately does
  not have.
- **"a judgment" as a semantic object** — `BirthVerdictStatus` is an enum
  label carrying no truth condition; `DEFER_IN_SCOPE` is defined by its issuing
  procedure, not by a condition on the world. *Remedy*: semantics for statuses,
  stated independently of the procedure that emits them.
- **"for every request" as a quantifier** — quantification over all
  constructible `BirthAssessmentRequest`s is not expressible in Python or in
  mypy-strict types; construction validity lives in `__post_init__` raises,
  which are a procedure, not a predicate. *Remedy*: an external proof object
  (dependent types / a proof assistant), or at minimum an explicit predicate
  mirroring every `__post_init__` check.
- **"successfully constructed" as a predicate** — success is defined
  operationally as "no exception was raised by some constructor", and the set
  of raises is distributed across many `__post_init__` bodies in several
  modules. There is no single, quotable well-formedness predicate to appear as
  the theorem's hypothesis. *Remedy*: a consolidated, auditable statement of the
  admission predicate, derived from — and kept in step with — the constructors.
- **"the same request" across runs** — request identity is partly occurrence
  identity (`uuid4`, `admission_id`) and only partly content identity;
  `OccurrenceIdentity != ContentIdentity` is declared law. A theorem
  quantifying over requests-up-to-content cannot yet name its own equivalence
  relation. *Remedy*: total content identity coverage for requests, not only for
  experiment specifications, residuals, criteria, and weaker models.
- **"necessarily" / "must"** — the kernel's modality is runtime refusal: a
  violation raises. Refusal establishes that *this* execution did not proceed,
  never that no execution could. *Remedy*: a proof-carrying notion of
  impossibility, which runtime raises cannot supply.

`BirthAssessmentSemanticsContract` is **not** this theorem and does not
approach it: it is a per-instance referential well-formedness predicate
(matching ids, domains, schemas, exact prerequisite-cone coverage, poset
agreement) evaluated in `__post_init__`. It quantifies over nothing and issues
no verdict. In the shape above it belongs in T-1's *hypothesis*, not its
conclusion; `ReferentialConsistencyContract != DenotationalSemantics`, and the
name "semantics contract" overstates what it establishes.

### Reconsideration condition (tracked, not scheduled)

This draft is not to be promoted to law, and the "prove once vs. re-verify per
instance" question is not to be reopened, until **both** hold: `BIRTH_IN_SCOPE`
is actually reachable through a real closure authority, **and** the law tables
above have stopped moving. Until then any theorem proved here has `DEFER` as
its only subject.

## G0.T.1 — Global licensed composition and backward auditability (DRAFT — NOT LAW)

**Status: DRAFT_TEXT_ONLY.** Like `G0.T.0`, this section adds no row to any law
table, opens no gate, and promotes nothing. Unlike `G0.T.0`, its subject is not
the kernel's verdict gates but the domain-neutral meta-algebra registered in
`src/alghanem/metaalgebra/`: layer signatures, transition signatures, and the
conditions under which transitions compose. Two theorems are stated, proved
separately, and must not be merged — failure of the second does not weaken the
first, and success of the first does not establish the second.

### Objects

A layer signature is the eight-tuple

```
A_i = (C_i, S_i, Omega_i, Rel_i, Inv_i, Cl_i, Tr_i, R_i)
```

— carrier, state space, partial operations, licensing relations, invariant
components, closure law, auditable trace, residuals. The state space is a
component in its own right and is never folded into the carrier, because
`Carrier != State` is a finding this repository already paid for, not a
presentational choice.

A transition signature is the six-tuple

```
T_i = (D_i, G_i, T_i, P_i, tau_i, rho_i)
```

— domain condition, licensing gate, transformation, preserved-invariant
obligation, trace obligation, residual/rank policy — together with an
independent handoff condition `Handoff_i`.

Neither definition names a layer, fixes a number of layers, or orders them.
`GenericLayerType != PredeclaredLayerArchitecture`: defining `Graph = (V, E)`
is not a claim about how many vertices exist, and `G0.MA`'s
`NoPatternNameBeforeIndependentBirth` bears on the second, never the first.

### The two step laws

**NoJump.**

```
D_i(x) and G_i(x)  =>  T_i(x) in C_{i+1}
not G_i(x)         =>  T_i(x) is undefined, or BLOCK/DEFER,
                       and no successful-transition certificate is issued
```

The second clause deliberately does **not** say that the value fails to belong
to `C_{i+1}`. The same object may be a perfectly good member of the next
carrier by another licensed route; what is refused is *this* transition and the
authority it would have carried. NoJump constrains the path and its licence,
not membership in the target carrier
(`NoJumpConstrainsThePathNotTheTargetMembership`).

**Handoff.**

```
Cl_i(y) and Handoff_i(y)  =>  y in Dom(T_{i+1})
```

Closure alone does not entitle exit. An object may be closed inside its own
layer and still not be qualified for the relation the next layer imposes;
`ClosureIsNotARightOfExit`. The condition is separate, separately named, and
must declare what it adds beyond closure — a handoff condition that restates
the closure law is closure under a second name, and is refused at construction.
The distinction is not decorative: it is exactly where `Weight -> Derivation`
and `Word -> SyntacticSlot` will need something closure cannot supply.

### Theorem 1 (intended, proved by induction in this text) — Global licensed composition

> Let `A_0, ..., A_n` be layer signatures and `T_0, ..., T_{n-1}` transition
> signatures with `T_i` from `A_i` to `A_{i+1}`. Suppose for every `i`:
> `Typed_i`, `Licensed_i`, `InvariantPreserving_i` (on the named subset `P_i`,
> with every component of `P_i` declared in both `Inv_i` and `Inv_{i+1}`),
> `Traceable_i`, `ResidualSafe_i`, and the handoff law above. Then
> `T^(n) = T_{n-1} o ... o T_0` is defined on every `x` that passes every gate,
> and the path `x_0 -> x_1 -> ... -> x_n` is licensed at every step, with no
> unlicensed jump.

*Proof sketch (induction on n).* Base `n = 0`: the empty composition is the
identity on `Dom(T_0)` and licenses nothing, so the claim holds vacuously.
Step: assume `T^(k)` is defined and licensed on every `x` passing the first `k`
gates, producing `x_k in C_k`. `ResidualSafe_k` and `Cl_k` give `Cl_k(x_k)`;
`Handoff_k(x_k)` gives `x_k in Dom(T_k)` by the handoff law; `D_k(x_k)` and
`G_k(x_k)` then give `T_k(x_k) in C_{k+1}` by NoJump's first clause, and the
step carries a licence by construction of `G_k`. If any gate fails, NoJump's
second clause yields undefined/`BLOCK`/`DEFER` and no certificate, so no
unlicensed element enters the composition. Hence `T^(k+1)` is defined and
licensed wherever all `k+1` gates pass. ∎

The theorem is about *paths and licences*, not about correctness of content. It
does not say the composite output is true, faithful, or linguistically right;
`LicensedPath != CorrectResult`.

### Theorem 2 (intended, independent) — Backward auditability

> For every step there exists `Audit_i(x_{i+1}, Trace_i)` returning a
> certificate `(source_class, operation, license, preserved_invariants,
> residuals)`.

No inverse `T_i^{-1}` is demanded, because layers compress and a compressing
step has no inverse. What must be recoverable is *the reason the step was
licensed*, not the original object. The theorem therefore does not weaken as
layers compress, and the five certificate fields are required jointly — none
substitutes for another (`REQUIRED_AUDIT_CERTIFICATE_FACTS`). Theorem 2 is
stated separately from Theorem 1 on purpose: a chain may compose licensedly and
still fail to be auditable, and an auditable step may sit in a chain that does
not compose.

### Validity is not coverage

```
TheoremValidity != InstantiationCoverage
```

Both theorems are stated and argued for arbitrary `n`. How many Arabic layers
and transitions this repository has actually built is a second, independent
figure, derived rather than written (`CompositionChain.instantiation_coverage`).
As of this section no Arabic instantiation exists at all: the meta-theory is
frozen first, deliberately, so that the first instantiation is tested against a
specification that historically precedes it. Low coverage is not a defect in
the theorem, and high coverage would not substitute for proving it. An earlier
draft of this work described the theorem as "nearly empty" because only one
adjacent pair was in view; that description conflated the two figures and is
withdrawn.

### What this text does not establish

- **The proof lives in this document, not in the type system.** Python and
  mypy-strict cannot quantify over all well-formed inputs; well-formedness is
  distributed across `__post_init__` raises. What the code contributes is
  construction-time refusal of chains whose adjacency hypotheses fail — the
  theorem's *hypothesis*, never its conclusion
  (`AdjacencyIsAHypothesisNotAConclusion`).
- **No transformation is executed anywhere in `metaalgebra/`.** `Typed_i`,
  `Licensed_i`, and the rest are declared obligations of a step, not measured
  properties of a run. A registered chain is a frozen structure, not a result.
- **Any step implemented by a registry-bound callable inherits `G0.T.0`'s
  oracle axioms** — `OracleTotality`, `OracleDeterminism`, `OraclePurity`,
  `OracleIdentityFaithfulness`, `SchemaDenotation`,
  `FailureSemanticsDenotation` — by citation, not by discharge.
- **Nothing here touches the empirical axis.** Under `G0.ST`, a chain proved
  relative to its frozen `Σ` may simultaneously carry
  `EmpiricalStanding = NOT_TESTED`, and that pair is consistent.

### Reconsideration condition (tracked, not scheduled)

Promotion of `G0.T.1` beyond `DRAFT_TEXT_ONLY` requires both: at least two
independently registered adjacent pairs whose contracts were frozen *before*
their implementations (`PROSPECTIVE_SPECIFICATION_INDEPENDENT`, not merely
`RETROSPECTIVE_CONFORMANCE`), and a discharged backward-audit certificate for
at least one of them.

## G0.R — Realization law: one origin, parallel realizations (DRAFT — NOT LAW)

**Status: `DRAFT_TEXT_ONLY`.** This section records a structure that now exists
in code. It does not promote that structure to law, and nothing in it licenses
any linguistic or empirical claim.

### The three levels

```
Σ_M  =  MetaAlgebraSchema            the language: what a layer, a transition,
                                     an audit certificate and a realization are

Σ_A  =  AbstractSystemSpecification  a particular theory written in Σ_M:
                                     named layers, named transitions

R    =  Realization(Σ_A, D)          Σ_A carried into a domain D
```

and, in parallel, never in series:

```
Σ_A  ⟶  R_arabic(Σ_A)          Σ_A  ⟶  R_python(Σ_A)
```

not `Arabic → Python` and not `Python → Arabic`.

### Declared laws

- **`SchemaIsNotSpecification`.** `Σ_M` carries no concrete layer. A language
  that already contains the theory written in it cannot be a language.
- **`SigmaIsTheOrigin`.** `Σ_A`'s digest excludes its realizations. Changing a
  realization does not change the theory; this is the structural witness that
  `Σ_A` is an origin rather than a description of one of its images.
- **`RealizationCoverageIsExact`.** A realization's realized and deferred
  members must exactly partition `Σ_A`'s members. Partial coverage presented as
  coverage is the failure mode this forbids.
- **`ARenamingIsNotARealization`.** Every component realization carries a
  falsifier distinct from the name it realizes. A binding with no way to be
  wrong is a translation table, not a realization.
- **`NoSemanticsFromProse`.** Executable meaning is generated only from
  `ExecutableClause`; a `DeclarativeClause` yields an explicit refusal that
  fails loudly when called. Inventing a predicate from a human sentence
  manufactures agreement.
- **`CommutationIsPerTransition`.** The square is
  `R_{i+1}^D ∘ T_i = T_i^D ∘ R_i^D`, with distinct source and target carrier
  realizations. A single `R^D` on both sides hides the layer change.
- **`GenerationIsRelativeToTheGeneratorDigest`.** Determinism is a property of
  `(digest Σ_A, digest g)`, never of `Σ_A` alone, and every manifest carries
  `sigma_digest`, `generator_digest` and `backend_id`.
- **`AResidualMayIndictTheDomain`.** A residual may be dispositioned `CLOSE`,
  `REFINE`, `REVISE_DOMAIN` or `DEFER`. Without `REVISE_DOMAIN` every residual
  becomes evidence against the theory and never against the binding.

### What this does not establish

- **Two domains prove coverage, not representation independence.** Realizing
  `Σ_A` in two domains shows the law does not require either domain's
  vocabulary. Independence requires discharged commutative squares, and those
  are recorded as obligations, not results.
- **The Arabic realization is structural, not linguistic.** It binds `Σ_A`'s
  components to named places in the Arabic domain. It does not bind
  `CarrierState` to a syllable, a vowel or a weight, and it asserts nothing
  about Arabic being true under any transition.
- **The Python realization is structural, not semantic.** Every generated
  predicate today is an explicit refusal, because `Σ_A` carries no executable
  clause yet. `G_py` is demonstrated to be a deterministic function; it is not
  demonstrated to produce working semantics.
- **A matching manifest is a proof of derivation, not of truth.** Code
  generated from a false specification is faithfully derived false code.
- **The core is handwritten and stays handwritten.** `metaalgebra/` is a trusted
  bootstrap. `G_py(Σ_core) ≅ Implementation_core` is a deferred fixed-point
  claim, not a milestone reached here, and the generation package must never be
  imported by the core.

### Reconsideration condition (tracked, not scheduled)

Promotion of `G0.R` beyond `DRAFT_TEXT_ONLY` requires both: two realizations in
independently motivated domains whose bindings were frozen *before* their
implementations (`PROSPECTIVE_SPECIFICATION_INDEPENDENT`, not merely
`RETROSPECTIVE_CONFORMANCE`), and at least one discharged commutative square
`R_{i+1}^D ∘ T_i = T_i^D ∘ R_i^D`.

## G0.GEN — The generalization blocker: local closure is not global closure (declared law, no runtime gate)

This law closes a failure that has recurred in this tree often enough to stop
being an accident: a claim measured, closed, or exhaustively covered on a
subdomain was carried, without any further step, to the whole domain. The
carrier-state work is the latest instance. A state vocabulary that closed over
one probe's carriers was read as the state vocabulary; a coverage result on a
short deposited text was read as capacity over Arabic.

```
LocalClosure         ⇏ GlobalClosure
CoverageOnSubdomain  ⇏ UniversalCapacity
```

The step that is blocked is precisely this one:

```
∀x ∈ D₀, P(x)      ⊬      ∀x ∈ D, P(x)
```

Two warrants, and only two, license that step: a *proved* identity `D₀ = D`,
carrying its own named, citable evidence; or a *named* generalization law with
a statement and a precondition that a reader can check. Any third route —
"obviously", "in practice", "every example so far" — is refused at
construction, because enumeration is not a generalization law and a finite
corpus does not close an open language.

Refusal here is refusal of *promotion*, never of *record*. A claim without a
warrant stays readable exactly as it was measured, bounded by its subdomain.
The blocker deletes nothing; it forbids the widening.

| Law | Status | Scope |
| --- | --- | --- |
| `LocalClosureIsNotGlobalClosure` | DECLARED_LAW_ONLY | That a claim is closed, exhaustive, or fully covered over a measured subdomain `D₀` establishes nothing about the domain `D ⊋ D₀`. The extension is a separate step requiring its own warrant, not a consequence that follows from the local result. A reader who treats local closure as global closure has performed an unlicensed extension, whatever the local result's strength. |
| `CoverageOnSubdomainIsNotUniversalCapacity` | DECLARED_LAW_ONLY | That a vocabulary, model, or state schema accounts for everything observed within a subdomain is a coverage fact about that subdomain. It is not a capacity claim about the domain, and it may not be recorded, cited, or promoted as one. Capacity asserted over what was never measured is the exact step this law blocks. |
| `DomainIdentityIsAClaimNotAConvenience` | DECLARED_LAW_ONLY | `D₀ = D` is a claim requiring named evidence that cites where it is argued and states what it argues. Asserting domain identity in passing smuggles the conclusion into an unexamined premise. Evidence naming two domains other than the two in the extension request is not evidence in that request and is refused rather than read charitably. |
| `EnumerationIsNotAGeneralizationLaw` | DECLARED_LAW_ONLY | More examples are not a generalization law. A warrant of this kind must carry an identifier, a statement, and the precondition under which it applies, all three readable and reviewable. Closure over a finite corpus does not extend to an open language, and the absence of a counterexample within a subdomain is not a law about the domain. |
| `AnUnwarrantedClaimMayBeRecordedInItsSubdomain` | DECLARED_LAW_ONLY | The absence of a warrant blocks promotion, not registration. A claim stays recorded, readable, and citable within the subdomain over which it was measured; only its extension is refused. This law forbids reading the blocker as a deletion rule or as a judgment against the local measurement. |
| `OneWarrantIsDeclaredNotTwo` | DECLARED_LAW_ONLY | An extension request declares exactly one warrant and carries exactly the evidence that warrant requires. Supplying a domain-identity witness and a generalization law together is refused, because a request carrying both conceals which of them actually bore the extension, and an unattributable warrant cannot be reviewed. |

`G0.GEN` declares law only. It installs no gate, promotes and demotes no
existing claim, and re-labels no row in any table above; the vocabulary that
carries the blocker in code (`src/alghanem/metaalgebra/generalization.py`) is
registration-only, refuses unwarranted extensions at construction, and issues
no judgment on any claim already standing in this repository.

## G0.RUN-0 — Minimal licensed execution: the first runnable vertical slice

Everything above this heading either constitutes a level or refuses a shortcut.
Nothing above it *runs*. `G0.RUN-0` closes that gap with the smallest slice that
is still non-trivial: a fully declared case is carried through the real
licensing chain and emits an auditable, replayable verdict.

```
PK₀ → O₀ → O_L² → ExistenceLineage → Nisbah_v3 → PASS | BLOCK | DEFER
```

The product of this milestone is a **licensing and audit engine**, not a model
of language. No Arabic material, no `O_M`, no significations, no parser. The
question it answers is exactly one: *is this whole nisbah traceable to a single
licensed origin?*

### Five epistemic standings, not three

A verdict is aggregated only from standings that bear on it. The separation
below is constitutional, not a rendering detail:

```
proved true ≠ proved violated ≠ evidence incomplete
            ≠ check blocked by a prior law ≠ no claim was ever made
```

- `SATISFIED` — bears on the verdict. The law was evaluated and held.
- `VIOLATED` — bears on the verdict. The law was evaluated and failed; produces
  `BLOCK`.
- `UNRESOLVED` — bears on the verdict. A checkable claim lacked evidence;
  produces `DEFER` and a named residual.
- `NOT_EVALUATED_BY_PREREQUISITE` — does not bear on the verdict. A claim existed
  and was checkable, but a prior law blocked the material it needed. It names its
  blocker and is never a residual.
- `NOT_APPLICABLE_NO_CLAIM` — does not bear on the verdict. No claim was declared,
  so there was nothing to compare. Never a residual, and never an agreement.

### Stages, and what may exist at each

```
Declaration → Validation → PartialDerivation → LawEvaluation
                   ↘ INVALID_INPUT (not a verdict)
BLOCK | DEFER
PASS → Materialization → MaterializedIdentity
```

Identities verifiable *before* judgment (`PK₀`, `O₀`) are recomputed in
`Validation`; a false claim there is `INVALID_INPUT`, never `BLOCK`. Identities
of objects that exist only *after* a licensing act (`O_L²`, the nisbah) are
checked in the law layer, because demanding them earlier would reinstate the
circularity this separation exists to break.

| Law | Status | Scope |
| --- | --- | --- |
| `ADeclarationIsNotAnAuthority` | ENFORCED_AT_EXECUTION_GATE | The input document is an inert candidate declaration. It may name identifiers, digests, and vocabulary members, but may not carry a derived reference, a licensed role, a lineage, or a verdict. Authority is re-derived from the declaration through the existing doors; it is never read out of the document. |
| `InvalidInputIsNotABlock` | ENFORCED_AT_EXECUTION_GATE | A document from which no case can be constituted yields an `InputValidation`, not a verdict. `ExecutionOutcome` has no member for malformed input, so the confusion cannot be expressed. A false pre-judgment digest is `INVALID_INPUT`; a welded two-origin chain is `BLOCK`. |
| `UnresolvedEvidenceIsNotInvalidInput` | ENFORCED_AT_EXECUTION_GATE | Missing evidence is declared as a closed, non-authoritative `UnresolvedRequirement` naming the authority and its subject. A missing field is a fault; a declared unresolved requirement is a residual. An absent site without a matching declared requirement is `UNDECLARED_ABSENT_SITE`, and a declared requirement for a site that is present is a contradiction. |
| `JudgmentPrecedesConstruction` | ENFORCED_AT_EXECUTION_GATE | `AnchoredNisbahSignatureV3` is constructed only after a provisional `PASS`. Its constructor refuses origin mixture; building it earlier would let the constructor, not the engine, issue the verdict, and no readable trace would survive. |
| `EveryLawIsEvaluated` | ENFORCED_AT_EXECUTION_GATE | Evaluation never short-circuits and never drops a law from the trace. A dependent law whose material a prior law blocked is recorded `NOT_EVALUATED_BY_PREREQUISITE` naming its blocker, so a blocked case is never displayed as an incomplete one. |
| `NoClaimIsNotAnAgreement` | ENFORCED_AT_EXECUTION_GATE | An undeclared identity is not proof that the identity agrees. The absence of a claim is `NOT_APPLICABLE_NO_CLAIM`, a standing of its own, causally distinct from a check that a prior law blocked. |
| `ADigestDoesNotContainItself` | ENFORCED_AT_EXECUTION_GATE | `ExecutionResultCore` is pure content and carries no digest of itself; `execution_digest` lives in the envelope and is recomputed from the core on construction. |
| `AReplayNeedsTheDeclarationNotItsDigest` | ENFORCED_AT_EXECUTION_GATE | A digest cannot be inverted, so the envelope carries the full declaration document, bound by `Digest(declaration_document) == core.input_digest`. Replay runs from the stored declaration, never from the earlier verdict. |
| `ALawSetIsNotReinterpretedByALaterOne` | ENFORCED_AT_EXECUTION_GATE | `law_set_digest` is derived from the frozen ordered law list. Changing, removing, or reordering a law changes the identity of every result judged under it, so an old verdict is never silently re-read under a newer set. |
| `SameInputSameLawsSameResult` | ENFORCED_AT_EXECUTION_GATE | No clock, randomness, environment, or filesystem path enters the result content. The same declaration under the same law set reproduces the same verdict, the same trace, and the same `execution_digest`, byte for byte. |

`G0.RUN-0` deposits `src/alghanem/execution/`, which sits above the existence
axis and is imported by nothing below it. It reads the algebra at two named
places only (`linguistic/anchored_v3.py`, `linguistic/nisbah.py`), canonicalizes
solely through `canonical_content.py`, and issues no birth, no birth verdict,
and no `E0` freeze.

Deferred here by name, not by omission: the golden-case corpus, the command
line interface, packaging, `O_M`, significations, and any Arabic material.

### G0.RUN-0H — Hardening the sealed verdict

`G0.RUN-0H` adds no theory and no linguistic law. It closes three gaps between
the stated meaning of a verdict and what the engine actually did, and corrects
the standing of one dependent law.

The two invariants below are **invariants of the execution engine, not members
of `ExecutionLaw`**. They are never evaluated against a case, never recorded as
a line in a trace, and never enter `LAW_SET_DIGEST`; they live in
`src/alghanem/execution/invariant.py` and are enforced at construction time.
`LAW_SET`, `LAW_SET_ID` and `LAW_SET_DIGEST` are therefore unchanged by this
milestone, and no earlier verdict is re-read under a different law set.

| Law | Status | Scope |
| --- | --- | --- |
| `AMaterializationFailureIsNotABlock` | ENFORCED_AT_EXECUTION_GATE | An engine invariant, not an `ExecutionLaw`. `BLOCK` is issued only because a declared law was evaluated and proved violated. If a case passes every pre-construction law and materialization then fails — the `v3` door refuses it, or a derived site the laws admitted is absent — the law set failed to cover a condition `v3` imposes, or the engine is defective. That is `ExecutionInvariantError`, outside `PASS`/`BLOCK`/`DEFER`; no envelope is sealed and the failure is never charged to the case. |
| `PassIffMaterializedIdentity` | ENFORCED_AT_EXECUTION_GATE | An engine invariant, not an `ExecutionLaw`. The relation is biconditional: `PASS` requires a `materialized_identity`, and `BLOCK`/`DEFER` forbid one. Only success reaches authoritative material, and success is never without it. |
| `AnEnvelopeHoldsAnUnalterableDeclaration` | ENFORCED_AT_EXECUTION_GATE | Freezing a dataclass does not freeze a dictionary it carries, nor the dictionaries nested inside it. The envelope therefore holds the frozen `CaseDeclaration` itself, and `declaration_document` is a read-only projection recomputed on every read, so the stored input cannot be altered after sealing while `input_digest` and `execution_digest` stay as they were. |

Under `DEFER`, `MATERIALIZED_IDENTITY_AGREES` is recorded
`NOT_EVALUATED_BY_PREREQUISITE` naming the first `UNRESOLVED` law as its
blocker, not `UNRESOLVED`: the identity law's own evidence is not missing; the
nisbah was never constructed because an earlier law lacked evidence. The
distinction is the one `ABlockedDependentIsNotMissingEvidence` already draws, so
the dependent law no longer contributes a residual of its own.

This correction changes `execution_digest` for `DEFER` cases that claim a nisbah
identity. That is admissible **now and not later**: the digests produced by
`G0.RUN-0` are not a frozen historical contract over cases, and hardening
precedes the freezing of golden data. After `G0.CASE-0` freezes the corpus, a
digest change requires a new law set and new cases, never a silent edit.

### G0.CASE-0.MATRIX — The constitution of the cases, before the cases

`G0.CASE-0.MATRIX` freezes *what must be covered* before a single golden case
exists. It contains no case, no JSON input, no expected verdict of any concrete
case, and no `execution_digest`. Its own digest, `COVERAGE_MATRIX_DIGEST`, is a
digest of the requirement — not of an execution.

The order it establishes is historical, not merely stylistic:

    Specification  ≺  Cases  ≺  Readout

`MATRIX` states the requirement; `G0.CASE-0.DATA` freezes inputs and
expectations **without running the engine against them**; `G0.CASE-0.READOUT`
runs the engine for the first time and exposes agreement or failure. Were the
cases written, run and adjusted inside one change, success would prove only that
the expectations were edited after seeing the result.

| Law | Status | Scope |
| --- | --- | --- |
| `CoverageRequirementIsFrozenBeforeCaseSelection` | ENFORCED_AT_COVERAGE_GATE | A requirement engine invariant, not an `ExecutionLaw`. Every `CoverageRequirement` carries `case_id = None`, enforced at construction. Thirty cases must be a consequence of the legal structure, never an arbitrary count that the matrix is later written to describe. |
| `CaseExpectationIsFrozenBeforeFirstEngineReadout` | ENFORCED_AT_COVERAGE_GATE | A requirement engine invariant, not an `ExecutionLaw`. The matrix names what a requirement expects, not what was observed; no engine call may occur in the same stage that fixes an expectation. |
| `AnUnreachableCellIsJustifiedNotInvented` | ENFORCED_AT_COVERAGE_GATE | A requirement engine invariant, not an `ExecutionLaw`. A standing the constitution forbids is recorded `reachable = False`, `required = False`, with a named justification, no verdict effect, no case disposition, no prerequisites and no forbidden co-standings. The absence is read from the fields themselves rather than from a member inside a vocabulary, so no enumeration carries a value that is not a state of anything. No case is fabricated to fill a table. |
| `AMatrixNamesNoCaseAndNoDigest` | ENFORCED_AT_COVERAGE_GATE | A requirement engine invariant, not an `ExecutionLaw`. The matrix is unreadable by any engine module — a test asserts no execution module imports it — so a coverage requirement can never influence a verdict. |
| `ALawStandingIsNotACaseVerdict` | ENFORCED_AT_COVERAGE_GATE | A requirement engine invariant, not an `ExecutionLaw`. A first-axis cell speaks of one law on one subject, so it may not carry a whole-case expectation at all: it carries `verdict_effect` only — `VIOLATED → FORCES_BLOCK`, `UNRESOLVED → FORCES_DEFER_UNLESS_BLOCKED`, and `SATISFIED`, `NOT_EVALUATED_BY_PREREQUISITE` and `NOT_APPLICABLE_NO_CLAIM` → `NO_VERDICT_EFFECT`. A satisfied law never forces `PASS`, because another law in the same case may be violated and `aggregate_outcome` reads `BLOCK > DEFER > PASS`. The three layers are separately typed: `CheckStanding → VerdictEffect → CaseDisposition`. `VerdictEffect` has exactly three members; a fourth effect would enter a new matrix with evidence, never as a reserved place. |
| `AProhibitionIsReadInItsEvaluationScope` | ENFORCED_AT_COVERAGE_GATE | A requirement engine invariant, not an `ExecutionLaw`. Every law carries a frozen `EvaluationScope` — `SUBJECT` where the judgement is borne by a named licence, site, slot or ontology, `CASE` where it is borne by the structure itself, such as predicate shape or the materialized identity. The scope is the bearer of the judgement, not a count of sites, so it does not move when a case happens to have one site or ten. `forbidden_co_standings` is read in that scope: on a `SUBJECT` law the prohibition binds `(law, subject)` alone, so `SATISFIED(L, A)` and `VIOLATED(L, B)` may stand together while `SATISFIED(L, A)` and `VIOLATED(L, A)` may not. A cell may not redefine its law's scope, and `G0.CASE-0.DATA` must name `witness_subject_id` for every `SUBJECT`-scoped law even where only one subject exists. |
| `AMatrixMeasuresTheEngineAsFrozen` | ENFORCED_AT_COVERAGE_GATE | A requirement engine invariant, not an `ExecutionLaw`. The matrix measures `PK₀ → O₀ → O_L² → Nisbah` as frozen. Any deeper ontological founding — redefining `PK₀` as a network of fibered nodes with existence, reality, properties, attributes, relations, conditions, causes and preventers — is a new layer above this contract with its own matrix and its own cases; it never alters this one retroactively. `G0.CASE-0` is thereby a historical witness of correct behaviour *before* that redesign. |

The matrix has three independent axes; none substitutes for another.

**1. Law-standing coverage.** Every `ExecutionLaw` × every `CheckStanding`: 18 ×
5 = 90 cells, each present exactly once. 56 are reachable and required; 34 are
refused with a named reason. The refusals are themselves claims about the
engine's meaning, and the sharpest are: `VIOLATED` is unreachable for
`NoUnreadConditionInTheFoundingBase`, because an unread condition is missing
evidence and never a proved breach; and `UNRESOLVED` is unreachable for
`MaterializedIdentityAgrees`, because a nisbah identity is not itself missing
evidence — either the nisbah is constructed and its identity compared, or an
earlier law prevented its construction and the block is recorded under the name
of its blocker.

No first-axis cell carries a case disposition at all; each reachable one carries
the effect of its standing on the aggregate, under `ALawStandingIsNotACaseVerdict`.

Each reachable cell also carries `forbidden_co_standings`: proving that a law
*can* reach `VIOLATED` does not prove that it cannot simultaneously be read
`SATISFIED` or `UNRESOLVED`. The prohibition is read in the law's frozen
`EvaluationScope`: on a `SUBJECT`-scoped law it binds `(law, subject)` alone,
because such a law legitimately holds at one site and fails at another.

**2. Outcome reachability.** Independent witnesses for the five case
dispositions: `PASS`, `BLOCK`, `DEFER`, `INVALID_INPUT` and `INVARIANT_ERROR`.
The last two are not members of `ExecutionOutcome` — invalid input yields no
verdict and an `ExecutionInvariantError` is an internal defect — but both are
states the case as a whole can end in, so both belong in `CaseDisposition` and
both require a reachability witness. The matrix states explicitly that the
invariant error is reached at the engine seam — by handing the engine incomplete
derived material after a provisional pass — never by a document a case author
could write.

**3. Cross-stage separation.** Seven boundaries between stages: invalid input
produces no envelope; `BLOCK` produces no materialized identity; `DEFER`
produces no materialized identity; `PASS` is never without one; an
`ExecutionInvariantError` produces neither verdict nor envelope;
`NOT_EVALUATED_BY_PREREQUISITE` produces no residual; and
`NOT_APPLICABLE_NO_CLAIM` is never read as `SATISFIED`. The last two constrain
no case disposition and carry `None`: a blocked dependent or an absent claim can
appear under `BLOCK` and under `DEFER` alike, and the requirement is exactly the
separation it names, read on its own subject.

`G0.CASE-0.MATRIX-H` corrected this specification before any golden case was
written, and `COVERAGE_MATRIX_DIGEST` moved accordingly. The move is required,
not incidental: it records that the requirement was repaired while it was still
only a requirement. Once `G0.CASE-0.DATA` freezes the corpus, a change of this
kind needs a new matrix, never a silent edit.

Deferred here by name, not by omission: the golden cases themselves, their
inputs, their expected verdicts, and every execution digest.

### G0.CASE-0.DATA — The written cases, before the first readout

`G0.CASE-0.DATA` derives an independent corpus from the frozen matrix. The
governing order is now four stages long:

    MATRIX  ≺  DATA  ≺  READOUT  ≺  DIGEST LEDGER

`DATA` says, before the engine has run once: *this is the case, and this is what
we expect of it*. `READOUT` runs the engine for the first time and compares.
Only if the reading matches the frozen expectation is an execution digest
recorded, in a ledger of its own that never flows back into `DATA`; from the
second reading onward that digest is a witness of drift.

| Law | Status | Scope |
| --- | --- | --- |
| `ACaseIsAuthoredNotGenerated` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. The golden cases are reviewed `JSON` files under `case_data/`, never the output of Python builders: a program that constructs the evidence cannot be held to account by it. `case_data.py` carries the specification datatypes and the internal-consistency checker only — it opens no file, builds no document, and imports no engine module. Reading the files is the test layer's business, so no file path enters the specification. |
| `AnExpectationCarriesNoExecutionDigest` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. `execution_digest` is born of the readout; admitting it into `DATA` — even as `None` — merges two stages. The field is absent from every type, and any key born of the readout is refused wherever it hides in the expectation tree, at any depth. |
| `ACounterCaseIsOneDeclaredPerturbation` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. In `DATA`: `AuthoredCounterCase = ExpectedPassBaseline + OneDeclaredPerturbation`, for `UNRESOLVED` as much as for `VIOLATED`. The unit of the experiment is the perturbation, not the structural difference: one authored change of meaning may need more than one surface operation for the case to remain constitutionally well formed, so `Perturbation = 1..n StructuralDiff × atomicity_kind × reason`. The kind is one of exactly three. `SINGLE_OPERATION` admits one operation and carries no reason. `COMPOUND_CONSTITUTION_PRESERVATION_CLAIM` admits several operations that serve a single epistemic transition, and is an *author's claim* in `DATA`: the gate can prove `|StructuralDiff| = 2` but cannot prove by itself that the two operations preserved well-formedness — only the input gate at `READOUT` can. `MULTIPLICITY_IS_THE_PROOF` is reserved for the different case where the multiplicity is itself the subject of the proof — a single law satisfied on one subject and violated on another — and is not a second name for a compound. |
| `ADeclaredPerturbationIsNotALicensedOne` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. A name may not carry a rank higher than its evidence. `DATA: AuthoredCounterCase = ExpectedPassBaseline + OneDeclaredPerturbation`; `READOUT: VerifiedCounterCase = VerifiedPassBaseline + OneLicensedPerturbation`. So `DeclaredPerturbation_DATA ≠ LicensedPerturbation_READOUT`, exactly as `Citation_DATA ≠ ProvenCoverage`: a case whose expectation is `PASS` is an *expected-pass* baseline, never a verified one, and licensing is a rank the readout alone confers. The refined order is `MATRIX ≺ Authored DATA ≺ DeclaredPerturbation ≺ ExpectedPassParent ≺ READOUT ≺ VerifiedPassParent ≺ LicensedPerturbation ≺ DIGEST LEDGER`. |
| `ABaselineIsTheImmediateStructuralParent` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. `baseline_case_id = ImmediateStructuralParent`, not necessarily the root baseline: each case is measured exactly one hop against the case it names, and that parent may itself be a derived, expected-pass case. This is what makes a clean violation possible — `B₀ →ADD anchor.second→ B₁ (expected PASS) →ADD anchor.third→ C (expected BLOCK)` isolates `3 > 2` with no second cause mixed in. The chain remains a tree: no case is its own parent, directly or through intermediaries. And the gate enforces the parent's rank, not merely its existence: `baseline_case_id ⇒ ExpectedDisposition(baseline) = PASS`, so no branch grows out of a case the author already expects to be blocked or deferred. What this proves is bounded — `ExpectedPASS_DATA ≠ VerifiedPASS_READOUT`: the gate establishes only that the author froze an expectation of success for the parent, never that the parent succeeded. |
| `ACitationIsAClaimUntilTheReadout` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. A `CoverageCitation` in `DATA` is a *claim* of coverage. The `DATA` checker proves only that the citation is legitimate — that it names a required, reachable cell, that its law and standing are that cell's own, that a `SUBJECT`-scoped cell names its witness subject and a `CASE`-scoped cell names none, and that the case's own frozen expectation contains the row cited. `READOUT` alone proves that the case actually reached the cell, by matching the citation against a line of the real trace. This is what prevents paper coverage. |
| `AnInvariantErrorIsNotInTheUserCaseSpace` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. `INVARIANT_ERROR ∉ UserCaseSpace`, so it is not a golden case and is given no document: it is an `EngineSeamWitness` on an internal seam reached by handing the engine incomplete derived material after a provisional pass. Giving it a document would make an engine defect something a case author can request. Invalid input is likewise a separate identity — `InvalidInputWitness ≠ GoldenExecutionCase` — with no trace, no envelope and no verdict. |

Four independent types carry the corpus. `GoldenExecutionCase` carries the
document alone, with its baseline and its declared differences, and no verdict.
`GoldenExpectation` carries what was expected before any reading: the
disposition, the trace, the residuals, the materialized identity and the
citations. `InvalidInputWitness` carries a document from which no case is
constituted, with its expected input faults only. `EngineSeamWitness` carries no
document at all. Both witnesses may cite the second- and third-axis cells that
constrain their own disposition, and neither may claim a law-standing cell: a
cell about a law in a standing is reached by a case that stood, not by a witness
to something short of one.

The expectation is checked for internal coherence without running the engine:
any `VIOLATED` row forces `BLOCK`, `UNRESOLVED` defers only when no violation is
present, `PASS` and a materialized identity imply each other, the declared
violations are exactly the violated rows in their order, no law contradicts
itself on one subject in one reading, and both `COVERAGE_MATRIX_DIGEST` and
`LAW_SET_DIGEST` are pinned to the frozen values. A mis-authored expectation is
therefore not caught here; it is caught at the readout, which is the point.

What the corpus does not yet cover is named in `case_data/MANIFEST.json`, and
the checker refuses any drift between that declared residual and the residual
derived from the citations. Coverage is closed by adding cases, never by
narrowing the list.

Deferred here by name, not by omission: the counter-cases for the requirements
listed in the manifest; the `JSON → CaseDeclaration` reader, which belongs to
`G0.CASE-0.READOUT` as its first obligation; the readout itself; and the digest
ledger that only a matching first reading may open.

### G0.CASE-0.DATA-H — Immutable data, and a difference that is proved

`G0.CASE-0.DATA-H` closes two structural gaps in the corpus layer before the
remaining cases are written, so the order gains a stage of its own:

    MATRIX  ≺  Immutable DATA  ≺  Verified Typed Structural Difference
            ≺  READOUT  ≺  DIGEST LEDGER

| Law | Status | Scope |
| --- | --- | --- |
| `AFrozenDocumentIsDeeplyImmutable` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. Freezing a dataclass never froze the dictionary inside it, so a golden case and an invalid-input witness hold their document as *transitively* frozen content — read-only mappings and tuples, with every value inside the `JSON` contract — and project a fresh tree on every read, exactly as the sealed envelope does with its declaration. `FrozenData ≺ Readout` would otherwise be nominal: a readout holding a reference into a "frozen" case could rewrite the evidence it is being measured against. |
| `ADifferenceIsAnOperationNotAPath` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. A structural difference is `operation ∈ {ADD, REMOVE, REPLACE}` at a named path, with the content before and the content after. Adding an anchor is `ADD nisbah.anchors[1]`, dropping one is `REMOVE nisbah.anchors[1]`, and changing one that stands is `REPLACE` at the place that changed; a list never reports a bare change of length, and an element changed beside an element added is two differences, not one. An added subtree is one difference at its own root, not one per leaf. |
| `ADeclaredDifferenceIsTheActualDifference` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. `Diff(BaselineDocument, CounterDocument) = DeclaredDifferences`, operation, path, before and after alike — not merely `DeclaredPath = ActualPath`. The comparison is between two authored texts only: no engine is run, no digest is born, and `DATA ≺ READOUT` is untouched. `GoldenCounterCase = ValidBaseline + OneDeclaredDifference` is thereby an enforced invariant rather than an author's assertion: without a stated reason the actual difference must be exactly one, and where multiplicity is itself the proof it must be at least two. A counter-case that does not differ from its baseline at any place is refused. |
| `ABaselineChainDoesNotTurnBackOnItself` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. The difference is measured one hop only, against the named baseline, and is never flattened to the root of a chain. Refusing a case that names itself as its baseline is not enough once a counter-case may itself be a baseline, so the whole baseline graph is walked and any cycle is refused: in a cycle every case is its own baseline by an intermediary, and no case is measured against anything. |

`expected_fault_kinds` is read as `InputFaultKind`, the closed vocabulary that
already existed, so a misspelt fault name is refused at `DATA` instead of
surviving until the readout. And the Arabic constitutional register now keeps
the distinction the structure requires: `INVALID_INPUT` is *constitutional
invalidity* — the case never came into being, so nothing stands to be judged —
while `BLOCK` belongs to the other side, where a case did stand and then broke a
law. The public enum members are unchanged; only the register and the prose
move, before the word settles into dozens of places.

Deferred here by name, not by omission: the remaining counter-cases, which are
written only after these gates are closed, so that no case is authored under a
difference claim that was never verified.

### G0.CASE-0.DATA-HH — The contract binds the class, and the diff stays strict

`G0.CASE-0.DATA-HH` closes the three ways the previous gates could still be
walked around, and records one piece of frozen legacy wording, before the
remaining cases are authored.

| Law | Status | Scope |
| --- | --- | --- |
| `AContractBindsTheClassNotItsFactory` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. Freezing inside the `of(...)` reader is not enough: the general constructor is an equally lawful road in Python, so a caller could hand a live dictionary to `GoldenExecutionCase(...)`, `InvalidInputWitness(...)` or `DeclaredDifference(...)` and rewrite it afterwards. The document, and a declared difference's *before* and *after*, are therefore re-frozen inside `__post_init__` itself. `FrozenGoldenCase ⇒ DeeplyImmutableDocument` holds for every road into the class, not only for the one the author is expected to take. |
| `AFrozenNumberIsAJsonNumber` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. `NaN`, `Infinity` and `-Infinity` are not `JSON` numbers, and Python's reader admits them by default, so they could enter from a file that looks like `JSON`. A non-finite float is refused at the freeze, which is where the written law "what falls outside the `JSON` contract is returned" is actually kept — a value that is not equal to itself would otherwise sit inside a corpus whose whole method is comparison. |
| `ASequenceEditWaitsForItsIdentityPolicy` | ENFORCED_AT_CASE_DATA_GATE | A corpus invariant, not an `ExecutionLaw`. The structural difference is positional and knows nothing of element identity, so an insertion or a removal in the middle of a list reads as a run of replacements followed by an addition or a removal — which is not the edit the author made. The open question is constitutional, not algorithmic: `ListIdentity = ElementIdentity` or `PositionIdentity`? In this project a position inside a list may itself be meaningful, so no `LCS` or edit distance is introduced to guess. Until an explicit `SequenceIdentityPolicy` is frozen, a list may either change its tail (`ADD`/`REMOVE`) or change a standing position (`REPLACE`) — never both at once — and anything else is refused. A diff that is less clever is safer than one that invents an identity the constitution has not granted. |

The two occurrences of «فساد الإدخال» inside the `COVERAGE_MATRIX` content are
**legacy frozen wording**. They are not corrected, because the matrix content
enters `COVERAGE_MATRIX_DIGEST` and every expectation pins that digest; editing
historical language by moving a frozen specification would breach
`MATRIX ≺ DATA`. The later constitutional term for that state is «بطلان تكوين
القضية» — *constitutional invalidity of the case*, recorded outside the matrix
content as `INPUT_CONSTITUTION_FAILURE` — and the reader should take the matrix
phrases in that sense.

Deferred here by name, not by omission: `SequenceIdentityPolicy`, which must
decide whether a list position is an identity or an order before mid-list edits
are admitted into the corpus.

### G0.CASE-0.DATA-1 — The first tranche of counter-cases

With the immutability and difference gates closed, the corpus grows for the
first time. Five counter-cases are authored against the single baseline, each
one an input that stands as a case and is then judged, and each one measured one
hop against `case0.baseline.pass` with its difference proved from the two texts
rather than asserted:

- `case0.counter.duplicate_anchor.block` — `ADD nisbah.anchors[1]`, a second
  anchor carrying the first anchor's own id. Claims
  `LS.anchors_do_not_exceed_arity.violated`, `OR.block` and
  `XS.block_has_no_materialized_identity`. *(Withdrawn at `DATA-1H`; see
  below.)*
- `case0.counter.arity_exceeds_slots.block` — `REPLACE nisbah.predicate.arity`,
  three declared and two written. Claims
  `LS.predicate_arity_matches_its_slots.violated`.
- `case0.counter.slot_names_a_deferred_role.block` —
  `REPLACE nisbah.predicate.slots[1].slot_id`, an argument place named after a
  deferred role. Claims
  `LS.argument_slot_ids_are_not_deferred_role_names.violated`.
- `case0.counter.absent_condition_site.defer` —
  `REPLACE nisbah.predicate.slots[0].condition_site` together with
  `ADD unresolved_requirements[0]`. Claims
  `LS.condition_sites_share_the_lineage_base.unresolved`,
  `LS.condition_sites_are_licensed_for_use.unresolved`, `OR.defer` and
  `XS.defer_has_no_materialized_identity`.
- `case0.counter.role_license_is_absent.block` —
  `REPLACE nisbah.anchors[0].role_site.license_id`, a licence that is not in the
  ontology. Claims `LS.role_license_granted_for_the_function_read.violated`,
  `LS.role_license_is_operative.not_evaluated_by_prerequisite` and
  `XS.blocked_dependent_has_no_residual`.

The fourth case is the first in the corpus carried by two structural operations,
and it is so for a constitutional reason rather than a convenience: an absent
site that is not declared as a standing requirement is *constitutional
invalidity*, not a deferral, so the removal of the site and the declaration of
its unresolved requirement do not stand apart. Two structural operations, one
authored change of meaning. At `DATA-1` this was recorded under
`multiplicity_is_the_proof`; `DATA-1H` corrects that name.

The written corpus now reaches all three verdicts a standing case can reach.
Every expected trace here is **authored from the frozen law set, not derived**:
no engine was run to produce a row, and `A CitationIsAClaimUntilTheReadout`
still holds of every cell claimed above. The residual falls from forty-three
requirements to thirty-one, and `case_data/MANIFEST.json` names each remaining
one.

Deferred here by name, not by omission: the thirty-one remaining cells, and the
readout that will either confirm or refute every row written in this tranche.

### G0.CASE-0.DATA-1H — The witness is purified and the rank is named

Three corrections are made before the corpus grows further. None of them moves
`COVERAGE_MATRIX_DIGEST` or `LAW_SET_DIGEST`: `RUN-0` is not re-run.

**The golden witness for `ANCHORS_DO_NOT_EXCEED_ARITY` was impure.** The frozen
implementation of that law computes
`len(anchor_ids) <= arity and len(set(anchor_ids)) == len(anchor_ids)`, so it
carries two clauses under one name. `case0.counter.duplicate_anchor.block` never
exceeded the arity at all — two anchors against `arity: 2` — and was blocked by
the hidden uniqueness clause, proving the unnamed half of the law rather than
the half the name states. Worse, its trace carried two distinct *occurrences*
both reporting `subject_id = anchor.first`, collapsing occurrence identity into
declared identity. It is withdrawn from the corpus and replaced by a one-hop
chain with unique ids throughout:

    B₀  →ADD anchor.second→  B₁ (expected PASS)  →ADD anchor.third→  C (expected BLOCK)

`case0.baseline.two_anchors.pass` stays inside the bound and is expected to
pass; `case0.counter.anchors_exceed_arity.block` violates it cleanly at `3 > 2`,
and inherits the three cells the withdrawn case claimed. The residual is
unchanged: the expected-pass link claims no cell of its own, so
`case_data/MANIFEST.json` still names the same thirty-one requirements.

**`RES.RUN0.AnchorArityConflatesIdentityUniqueness`** — an *architectural*
residual, of a different layer than the uncovered matrix cells, and therefore
recorded here by name rather than in `MANIFEST.json`, which is reserved for
`UncoveredMatrixRequirements`. Statement:
`ANCHORS_DO_NOT_EXCEED_ARITY = CountBound ∧ IdentityUniqueness` in the currently
frozen implementation. Separating the two clauses is deferred to a later
law-set revision; `LAW_SET` is not touched now. The withdrawn document is kept
outside the golden corpus, at
`tests/execution/fixtures/duplicate_anchor_exposes_arity_uniqueness_conflation.json`,
so that the evidence for this residual is not lost. A single residual does not
justify a ledger of its own; one will be opened when several become mechanically
traceable.

**The unit of the experiment is the perturbation, not the structural
difference.** `absent_condition_site.defer` exposed this: its two operations are
not a multiplicity being proved, they are two means of representing one
epistemic transition — `ResolvedAuthority → DeclaredUnresolvedAuthority`. So

    OneSemanticPerturbation  ≠  OneStructuralDiff

and every counter-case now carries a nested `perturbation` object with an
`atomicity_kind` drawn from a closed vocabulary of three, and a `reason` required
of the compound kinds and refused of the single one.
`COMPOUND_CONSTITUTION_PRESERVATION_CLAIM` is reserved for several operations
serving one transition, and `MULTIPLICITY_IS_THE_PROOF` for the genuinely
different case where the multiplicity is the subject of the proof. The latter is
admitted by the gate but cited by no case in the corpus yet.

**And the name may not outrank its evidence.** `DATA` may not call a
perturbation *licensed*, nor a case a *valid* baseline, because neither
licensing nor validity has been read yet:

    DATA:     AuthoredCounterCase  =  ExpectedPassBaseline  +  OneDeclaredPerturbation
    READOUT:  VerifiedCounterCase  =  VerifiedPassBaseline  +  OneLicensedPerturbation

`COMPOUND_CONSTITUTION_PRESERVATION_CLAIM` is named a *claim* for the same
reason: the author *declares* several structural differences *intending* to
preserve the constitution of the case, and `DATA` does not prove that the
preservation occurred —

    ClaimedConstitutionPreservation  ≠  VerifiedConstitutionPreservation

`DATA` can prove `|StructuralDiff| = 2`; only the input gate at `READOUT` can
prove that those two operations left the case well formed. For the same reason
`GoldenExecutionCase` no longer describes itself as a case *whose input stands*:
it is an authored document, and whether its input stands is a judgment reserved
for `READOUT` —

    Authored  ⇏  Valid          (as  Declared  ⇏  Licensed)

**And the parent's rank is enforced, not merely assumed.** The written law said
`ExpectedPassBaseline`, but the gate checked only that the named parent existed,
that it was not the case itself, and that the chain did not turn back. A case
expected to be blocked or deferred could therefore have served as a baseline,
contradicting the law it was written under. A separate gate now enforces

    baseline_case_id  ⇒  ExpectedDisposition(baseline) = PASS

and it runs before the difference and atomicity checks, so an illicit parent is
refused before its diff is even measured. What it establishes is bounded:

    ExpectedPASS_DATA  ≠  VerifiedPASS_READOUT

the author's frozen expectation of success, never success itself. The refined
order of the whole layer is therefore

    MATRIX ≺ Authored DATA ≺ DeclaredPerturbation ≺ ExpectedPassParent
           ≺ READOUT ≺ VerifiedPassParent ≺ LicensedPerturbation
           ≺ DIGEST LEDGER

and `baseline_case_id = ImmediateStructuralParent`, not the root baseline, so a
derived expected-pass case may itself be the parent of the next hop. Even the
parent-child relation inside the corpus now carries an epistemic rank: the
parent in `DATA` is not a *valid* origin but an *expected-pass* one, and it is
not a licensed origin until the readout.

Finally, the one surviving use of «إدخال فاسد» outside the frozen matrix — in
`ExecutionReport.__post_init__` — is corrected to «إدخال باطل التكوين», in
agreement with the constitution's own wording. The two historical phrases inside
`coverage.py` are deliberately left alone: they enter
`COVERAGE_MATRIX_DIGEST`, and `MATRIX ≺ DATA` forbids rewriting a frozen
specification to improve its language.

Deferred here by name, not by omission: the separation of the arity bound from
identity uniqueness, the first genuine `MULTIPLICITY_IS_THE_PROOF` case, and the
readout that alone can turn a declared perturbation into a licensed one.

## G0.GEN-0 — Minimal licensed Arabic production (specification only)

Every layer until now read a surface and asked what licensed it. This one turns
the arrow around, and the first thing the constitution must forbid is the
assumption that turning the arrow is free:

    Analysis  ≠  Generation⁻¹

Generation is not the inverse of the analyser; it is a *licensed* transformation
from a closed internal structure into an Arabic signifier:

    Generation :  LicensedStructure  →  SurfaceCandidate

**The source of a production is a passed execution, not a structure.** An
`AnchoredNisbahSignatureV3` merely *exists*; existence is not judgment. So the
only admissible entry point is a reference minted from an execution envelope
that actually carried a verdict:

    Outcome = PASS  ∧  MaterializedIdentity ≠ ∅   ⇒   PassedNisbahSourceRef

and nothing else may construct that reference. Generation does not run the
engine; it reads a certificate the engine already issued, and carries its
`input_digest`, `execution_digest` and `law_set_digest` forward so that the
authority of any produced word can be traced back to the judgment that licensed
its structure. This is the layer's highest law:

    NoGenerationAuthorityBeyondItsSource

**The specification is thin, and it does not restate its source.** Relation
kind, predicate anchor and argument anchors live in the licensed source; copying
them into the request would open a drift between `SourceStructure` and
`ProductionSpecification`, and drift is exactly what a content identity is meant
to close. For the same reason the caller may not write a rank or a residual:

    CallerDoesNotOwnGenerationRank
    ResidualsAreObservedNotAuthored

A rank is issued by a gate; a residual is read off the trace of the step that
failed to close. Evidence enters as closed references, never as free text, and
no identifier field may contain a single Arabic character — a specification that
carries its own answer has stopped being a specification.

**A position is not a semantic role.** The first family needs a subject and an
object *slot*, and it is tempting to reach for `Agent` and `Patient`. The
constitution refuses, permanently:

    فاعل  ≠  Agent          مفعول به  ≠  Patient

so generation opens its own closed vocabulary — `FAA_IL_POSITION`,
`MAF_UL_BIH_POSITION`, and `PREDICATE_POSITION` for the verb, which would
otherwise be a surface without a licensed slot — and binds an anchor *identity*
to a position without ever redescribing that anchor semantically:

    AnchorIdentity → SyntacticRealizationTarget      not      Anchor = Agent

**The unrealized layers branch, they do not block.** The earlier sketch made
orthography a child of phonology, which would have made the whole axis
unreachable, since this project has measured no phonological layer. After
composition the projections are siblings:

    Composition  →  { PhonologicalProjection , OrthographicProjection }

In `GEN-0` the phonological projection is withheld, and the orthographic one may
still be produced — but only from a frozen lexical form, never claimed as
derived from a sound layer nobody measured:

    OrthographyNeedNotClaimPhonologicalDerivation

**And withheld is a type, not a flag.** A field reading `GENERATED | WITHHELD`
puts both states in one shape and lets a consumer read a withheld stage as
though it held a value. The separation is structural:

    StageReadout  =  GeneratedStage[T]  |  WithheldStage

so `Generated ≠ Withheld` by construction, not by an enum comparison a caller
may forget to make.

**No morphology is claimed.** `فَعَلَ` is not derived from `ك ت ب` here; that
would announce the closure of the pattern system before it is built. The only
licensed operation is

    LEXICALLY_ATTESTED_FORM_SELECTION       not      DERIVED_FROM_ROOT

and the refusal is enforced, not merely documented; real derivation is deferred
to `GEN-MORPH-1`.

**Three ranks, and the third is unreachable.** Not every output is «correct
Arabic»:

    SurfaceCandidate ≺ SpecificationConformantSurface ≺ CertifiedGeneratedUtterance

The second is issued by a gate that checks every token against its specification
— anchor, position, case effect, order, trace — and it is named for exactly that
and no more (see `G0.GEN-0.SPEC-H` below). The third requires a round trip:

    G(S) = U  ∧  A(U) = S′  ∧  S′ ≃ S       over  { relation, anchors, roles,
                                                    tense, voice, case relations }

and the analyser that would compute `A` does not exist, because the corpus tags
case, not function (`ACCUSATIVE_IS_NOT_OBJECTHOOD`). So `RoundTripGate` has
exactly one outcome — a named deferral — and `RoundTripCertificate` cannot be
constructed at all:

    RoundTripIsSpecifiedNotIssuable
    NoCertifiedGenerationWithoutRoundTrip

**And the generator invents nothing.** It never asks what the speaker wishes to
say:

    IntentCreation  ≠  LanguageRealization
    GenerationDoesNotInventIntent

What is being built here is a language realizer, not a mind that authors
purposes. Python, the lexicon, the rules and the search are means; none of them
is the source of a sentence's correctness.

The frozen first family is

    PastActiveTransitiveVSO

a past active verb in a lexically attested form, one explicit singular subject,
one explicit singular object, `VSO` order only — no pronoun, no ellipsis, no
fronting, no passive, no augmentation, no dual or plural.

The order of the axis is

    SPEC ≺ DATA ≺ READOUT ≺ RT

and this milestone is `SPEC` alone: primitives, laws and gates with synthetic
tests only. No frozen lexicon and no golden specification enter here — a
reviewed Arabic datum inside `SPEC` would conflate the milestone that *names*
the shape with the one that *fills* it. Deferred here by name: the frozen
minimal lexicon (`G0.GEN-0.DATA`), the orchestrating readout
(`G0.GEN-0.READOUT`), the function-recovering analyser and the certificate it
alone can license (`G0.GEN-0.RT`), and morphological derivation
(`GEN-MORPH-1`).

## G0.GEN-0.SPEC-H — Lowering every claim to its own rank

`SPEC` was reviewed after it was merged, and the review found three places where
the implementation claimed more authority than it held. Nothing in the shape
above is withdrawn — `Analysis ≠ Generation⁻¹`, the withheld phonological layer,
the sibling projections, the refusal of `DERIVED_FROM_ROOT`, the single deferral
of `RoundTripGate`, and the separation of the first rank from the highest
certificate all stand. `SPEC-H` changes no goal; it lowers three claims to the
rank the evidence actually supports, and names what remains unproved.

**A contract binds the type, not the road that builds it.** `SPEC` wrote
`Outcome = PASS ⇒ PassedNisbahSourceRef` in this document, but left
`PassedNisbahSourceRef` freely constructible: only the optional `from_envelope`
factory ever saw an envelope. A caller could therefore write the digests by
hand, so in fact

    PassedNisbahSourceRef  ⇏  ActuallyPassedExecution

The same hole ran one level up: `ProductionSpecification` checked its internal
consistency in `__post_init__`, but checked *membership of its elements in the
source* only inside `for_passed_execution` — so a direct construction, or a
`dataclasses.replace`, could anchor a production on an element the source never
carried. Both types are now closed by an issuance token on the pattern already
used by `_IssuanceToken` in the certificate layer, and every source check is
moved into the constructor, where it also covers the lexical choices and the
realization constraints, which the factory never examined. The reference now
carries a frozen inventory of its source's elements and their kinds, so the same
check can be re-measured later without the envelope. The law:

    ContractMustBindClassNotFactory

An enforceable factory that can be walked around is not an enforceable contract.

**Conformance is not licensing.** The second rank was called
`StructurallyLicensedSurface`, and its gate `StructuralLicensingGate`. But the
gate reads the realization targets *out of the specification the caller wrote*
and then verifies that the produced tokens honour them. What it proves is that
the product matches its author's own claim:

    CallerClaim → ConformsToCallerClaim  ⇏  Licensed

That is circular, and a claim is not evidence of itself. The rank, the gate, the
decision, the status and the verdict member are renamed to say what is actually
proved:

    StructurallyLicensedSurface → SpecificationConformantSurface
    StructuralLicensingGate     → SpecificationConformanceGate
    LICENSED                    → CONFORMANT

The name `StructurallyLicensedSurface` is reserved by text and defined by no
type; it is not opened until an independent `SyntacticBindingCertificate`
exists. The law:

    ConformanceIsNotLicensing

**An architectural authority gap is not a runtime residual.** A
`GenerationResidual` is *observed*: a transition ran and named what it could not
settle — `Transition → ObservedResidual`. What is missing here is known before
anything runs, because the structure of the layer does not hold the authority at
all. Conflating the two would let a gap be read as though some step had reported
it. So they are separated by type, in `generation/authority_gaps.py`:

    RuntimeResidual  ≠  ArchitecturalAuthorityGap

    GenerationAuthorityGap = gap_id + claim + missing_authority
                                    + discharge_condition

Each gap names the claim that falls inside it, the authority that is absent, and
— so that it is a door and not an open wound — the condition that discharges it.
Two are frozen now.

**`RES.GEN0.NoIndependentAnchorToSyntacticFunctionAuthority`** — recorded by name
in the manner of `RES.RUN0.AnchorArityConflatesIdentityUniqueness`, and outside
both law sets, since it is a gap and not a rule. Statement: nothing in the source
establishes

    anchor.first = فاعل        anchor.second = مفعول به

`AnchoredNisbahSignatureV3` carries anchors and `predicate.slots` with no
filling relation between them at all, and `ArgumentSlot` refuses role names
outright. So the mapping is the caller's choice, and the gate grants conformance
to an inverted assignment exactly as readily as to the intended one — a test
witnesses this rather than assuming it. Its discharge condition: a
`SyntacticBindingCertificate` proving

    Anchor  —evidence→  LicensedSyntacticPosition

and only then may the word «licensed» be used. `Agent`/`Patient` are not opened,
and `linguistic/nisbah.py` is not touched.

**`RES.GEN0.NoVerifiedLexicalAttestation`** — `LexicalChoiceRef` carries
`entry_id`, `entry_content_id` and `lexical_source_digest`, but `SPEC` has no
frozen lexicon to measure them against; in the tests they are synthetic strings.
Nor can this layer prove that a token's `surface` is the form of an attested
entry rather than a well-formed Arabic fabrication. So:

    LexicalChoiceRef_SPEC  ≠  VerifiedLexicalChoice_READOUT
    LexicalChoiceRefIsAClaimUntilTheReadout

Its discharge condition: `GEN-0.DATA` freezes the lexicon, then `GEN-0.READOUT`
proves that `entry_id + entry_content_id + lexical_source_digest + surface`
agree.

**A success is read no wider than its mandate.** Every conformant decision
carries `open_authority_gaps` — both of the above — explicitly. They are not
called residuals, because nothing observed them; they are the boundary of the
rank, carried with it:

    ConformantSurface = ProvedConformance + ExplicitAuthorityBoundary

**Metadata conformance is not generation provenance**, and what can be proved
structurally is proved by structure, not by a repeated check. A
`GeneratedArabicUtterance` used to carry `orthographic_content_id` and `tokens`
as two independent claims, which permits `orthographic_content_id ≠
Digest(tokens)` in principle. It now carries the `OrthographicProjection`
itself, and both are read from it:

    DoNotStoreDerivableIdentityAsASecondClaim

and its construction requires that the trace begin at the specification's own
content id and end at an orthographic-projection step whose output is that
projection's digest. The gate is left with one connection the object cannot
enforce for itself: that each token's own trace is the utterance's chain rather
than an adjacent one. What cannot be proved at all here — that `surface` is an
attested entry's form — is the second frozen gap, not an omission.

**The historical law set is not edited.** `G0.GEN-0` froze
`GENERATION_LAW_SET_DIGEST`, and preserving the record is worth more than a
single unified name. The revision is therefore a *second* law set, with its own
identifier and its own digest, containing the original laws verbatim plus
`ContractMustBindClassNotFactory`, `ConformanceIsNotLicensing` and
`LexicalChoiceRefIsAClaimUntilTheReadout`:

    LawSet_GEN0  ≠  LawSet_GEN0.SPEC-H

Anything after `SPEC-H` refers to the revision; the original stays a document
that can still be rebuilt exactly.

With this, the order of the axis is stated more exactly than `SPEC ≺ DATA ≺
READOUT ≺ RT`:

    GEN-SPEC ≺ GEN-DATA ≺ LexicalVerification ≺ GenerationReadout
             ≺ SpecificationConformance ≺ SyntacticLicensing
             ≺ RoundTripCertification

and this does not push the first real Arabic sentence far away: `GEN-0.READOUT`
may produce one, at the rank `VerifiedGeneratedSurface` /
`SpecificationConformantSurface` — never «syntactically licensed».

**And here the linear line stops being extended.** With `SPEC-H` closed, `GEN-0`
witnesses six things in order —

    SourceAuthority → Specification → Candidate → Provenance
                    → Conformance → AuthorityGaps

— and that is enough from one line. No large `GEN-0` corpus is built next.
The next milestone is `G0.FGEN-0.SPEC`, which re-states this experience in more
general primitives — seed, node, pattern, expansion, branch, closure, authority
gap, trace, scale transition — so that `PastActiveTransitiveVSO` becomes *one
pattern* inside a pattern space rather than the engine itself, and `GEN-0`
becomes the base case of an inductive proof rather than a thing to enlarge. The
law fixed from now:

    LinearGeneration  ⊂  FractalGeneration

and **not** `FractalGeneration = RepeatedLinearGeneration`, because the fractal
adds what a repeated line cannot: branching multiplicity, change of scale, the
requirement that a level be closed before the next may rise, preservation of the
origin's identity, the birth of a branch or a transformation of the carrier, and
horizontal alternatives at each node:

    N_{i+1}  =  Close( Gate( Expand( N_i , P_i ) ) )

with `Closure(N_i)` a condition of ascent. `GEN-0.DATA` is not opened before
that.

## `G0.FGEN-EX-0` — temporary fractal experimental authority

The core `G0.FGEN-0` is deliberately sealed at the top: `ScaleNecessityCertificate`
cannot be issued, so `NextScaleSeed` is unreachable and no run may ascend a scale.
That seal is correct for licensing and wrong as a precondition for *trying*.
`G0.FGEN-EX-0` therefore does not open it. It opens a parallel authority beside
it:

    ExperimentalAuthority  ≠  LicensingAuthority

under one highest law, `ExperimentBeforeLicense`, and one pipeline:

    FrozenPreregistration → TemporaryExperimentalPermit → ExperimentalRun
                          → ExperimentalWitness → WitnessBundle

and there this stage stops. `WitnessBundle → SufficiencyAssessment →
LicensingCandidate → License` belongs to a later, independent authority that is
not written here.

The layer lives in `src/alghanem/fractal_experiment/` and imports only
`canonical_content` and `fractal_generation`; the core imports it never, and a
test guards both directions. Its authority gaps are a distinct type with a
distinct prefix, `RES.FGENEX0.`, so the core's `RES.FGEN0.` ledger is neither
extended nor edited.

Four separations are frozen as law texts, with their own law-set digest:

    ExperimentalPermission      ≠  License
    ExperimentalTransition      ≠  LicensedTransition
    ExperimentalNextScaleSeed   ≠  NextScaleSeed
    Witness                     ≠  Judgment

The permit is scoped to its own `run_id`, names the frozen binding it was issued
upon, enumerates the patterns, operations, source scales and target scales it
allows, and moves `ISSUED → ACTIVE → REVOKED` with no reuse after revocation.
Validity is a function of run identity and operational state, never of a clock:
`ExperimentalAuthorityExpiresWithItsRun`.

Experimental ascent is permitted and certification is not. A `ClosedFractalNode`
plus an `ExperimentalLiftPermit` yields an `ExperimentalNextScaleSeed`, which is
not a `FractalSeed`, inherits from nothing permanent, and carries no method that
converts it into `NextScaleSeed`. The necessity claim travels with it as a claim
*under test*: `ExperimentalLiftTestsNecessity; ItDoesNotCertifyNecessity`.

A result is not a witness's rank. `ExperimentalPASS → Witness`, and refutation,
underpoweredness and run failure are witnesses too — four standings, no licence —
and a witness refuses the vocabulary of rank in its observation texts. Witnesses
gather into a `WitnessBundle` that partitions by observation and carries no
verdict, no rank and no score, and `SufficientWitnessesOpenLicensingCandidateNotLicense`
is why the bundle names its own missing authority,
`RES.FGENEX0.NoSufficiencyAssessmentAuthority`. `WitnessSufficiencyContract` is
declared now and measured never here, because
`SufficiencyCriterionMustPrecedeItsMeasurement`.

Input is frozen before the run and split before it is read:

    FrozenInput        ≠  ProvenStructure
    FrozenExpectation  ≠  GenerativeInput

`FrozenExperimentBinding` names the fields the generator may see and the fields
held out for readout, and refuses any generator projection that carries a
held-out or undeclared field. This is what makes the MASAQ run meaningful: the
corpus already carries `Morph_Tag`, `Syntactic_Role` and `Case_Mood`, and letting
them into the generator would make the engine recite its own answer. The Arabic
adapter (`src/alghanem/arabic/masaq_fractal_experiment.py`) resolves the bytes
through `ALGHANEM_MASAQ_PATH`, verifies their length and digest, shows the
generator only positions and stripped segment surfaces, runs the core per word,
lifts experimentally from `masaq.segment` toward `masaq.word`, and reads the tags
afterwards as observations in the witness.

The whole stage claims one thing and no more: **we can experimentally run what is
not yet licensed, under a temporary scoped authority, and turn the run into
auditable witnesses.**

## `G0.FGEN-EX-1` — hardening the MASAQ witness

`G0.FGEN-EX-0` proved the stage, not the theory. Its first pattern,
`segment_accretion`, reaches a word by joining its segments in order, and its own
preregistration declares a weaker model that reaches the same surface by plain
textual concatenation. A run that merely rebuilds `"".join(segments)` therefore
demonstrates a correct output and not a necessary architecture:

    CorrectOutput  ≠  NecessityOfArchitecture

`G0.FGEN-EX-1` opens nothing. `fractal_generation/` is untouched, no
`SufficiencyAssessment`, no `LicensingCandidate` and no `License` is written, no
permanent `NextScaleSeed` appears, and `ExperimentalLift` stays open. It corrects
what the witness of `G0.FGEN-EX-0` is allowed to mean, before more of them
accumulate. Five laws are added, all of them restrictions:

    WeakerModelTieBlocksDistinctiveStructuralSupport
    TaskOutcome     ≠  ComparativeStanding
    RawOccurrence   ≠  NormalizedProjection
    SourceWordNo    ≠  DerivedLocalPosition
    HeldOut         ≠  Dropped

The tie law blocks the claim of *distinctive* support, not the success of the
work. Those are two axes, and `G0.FGEN-EX-1` records both per word. A
`MasaqWordReading`, bound to `word.input_id`, carries an
`ExperimentalTaskOutcome` — did the algebra reach the target on this input? —
alongside a `ComparativeStanding` — where does it stand against the weaker
model? — and the `ExperimentalStanding` that governs only the distinctiveness
claim. A word whose fractal run reconstructs correctly and whose concatenation
ties reads `SUCCESS`, `BOTH_SUCCEED` and `UNDERPOWERED` at once, with no
contradiction. Two correct methods covering the same region are two witnesses,
not a problem; the only error would be to credit one with what it has not shown.
`MasaqExperimentReport.coverage_tally` therefore counts task outcomes and
comparative standings separately, so a full MASAQ run can answer *how much of the
corpus the algebra closes* independently of *whether the fractal was distinctive*.

Standing is no longer read off closure and reconstruction alone. It is derived
from the preregistered conditions together — run failure, reconstruction,
closure, negative controls behaving as preregistered, absence of a blocking
residual, and absence of a weaker-model tie — in `derive_standing`. A tie yields
`UNDERPOWERED` and a named residual, `WEAKER_MODEL_TIES_FRACTAL_MODEL`, never
`OBSERVED_REFUTATION`: a tie does not falsify the reconstruction, it forbids the
claim that the fractal added distinctive structure.

The adapter no longer authors `IRREDUCIBLE_AT_CURRENT_SCALE` for every word with
more than one segment. That was a strong claim asserted before measurement, and
contradicted by the weaker model, which does reach the word from the segment
scale. What is recorded instead is disciplined ignorance: an
`UNRESOLVED_DIFFERENCE` stating that the necessity of the higher scale is under
test and irreducibility at the current scale has not been established. The
experimental lift still issues while standing is `UNDERPOWERED`, and its witness
says it ran to *test* the target scale, not to certify it.

Provenance is preserved rather than reinvented. Each `MasaqSegmentOccurrence`
keeps its raw MASAQ surface, the original `Word_No` verbatim, a separately named
derived `LocalSegmentPosition`, a `NormalizationTrace` naming the transformation
and every character it removed with its position, and a
`HeldOutMASAQAnnotation` freezing all five held-out columns — not `Morph_Tag`
alone — with column absence distinguished from an empty value. The generator
projection still shows only the declared visible fields, and a leaked held-out
field is still refused.

Negative controls are runs. Reversed order and dropped segment pass through the
same accretion gates and the same readout as the primary branch, and each
`NegativeControlObservation` records control input identity, transformation,
output and comparison against the preregistered expectation. A control that
makes no difference is recorded as a failure to discriminate and drives the
standing to `UNDERPOWERED`.

The stage claims one thing and no more: **a witness may not be called structural
support while a weaker model reaches the same result.** The question it leaves
open is the real one — which transformation genuinely requires the fractal
algebra, and cannot be reproduced by concatenation.

## G0.LEX-0 — `NecessaryRelationIsNotGenerativeAuthority` (declared law, runtime scope is one milestone)

`ConditionIsNotMujib`. That a relation *must hold* wherever the thing holds does
not make that relation a licence to *produce* the thing. A condition rules out
the cases in which the claim is false; it does not, by itself, generate a single
true case. Reading a necessary relation as a generative authority is the general
shape of which several separately named refusals in this document are instances:
`FrozenExpectationIsNotGenerativeInput`, `IltizamConditionIsNotItsCause`,
`StatisticsRaiseDirayaNeverMakeRiwaya`, and `TestPassIsNotUniversalTruth`.

Two literal instances are enforced at `G0.LEX-0`:

- `LazimIsConditionNotMujib` — a mental concomitant is a *condition* of an
  `iltizam` signification, never its efficient cause; the concomitant alone
  licenses no `iltizam` candidate.
- `PartOfMeaningIsConditionNotGenerativeAuthority` — that something is part of a
  meaning is a *condition* of a `tadammun` signification, never an authority
  that generates one.

**Three scopes, kept apart deliberately.** Its *constitutional scope* is
GENERAL: it is stated here over the whole programme, not over one module. Its
*runtime enforcement scope* is `G0.LEX-0` alone, declared in
`GENERAL_TRANSITION_LAW_SCOPE` in
`src/alghanem/arabic/lexical_evidence_specification.py`. Its *global runtime
status* is `NOT_YET_ESTABLISHED`: no kernel gate enforces it, and no kernel
module is touched by this milestone — a test scans every `kernel/` module to
keep that true. Merging the three would itself be an instance of the law being
declared: a general statement here would be read as a general enforcement in
code, which is exactly the move from a necessary relation to an authority that
this law refuses.

## G0.LEX-0.APPLY — The layer applied to a root-indexed lexicon (registration only)

`SurfaceIsNotRoot`. `Maqāyīs al-Lugha` is indexed by root; an occurrence is a
surface. A lookup that matches a surface form directly against a root index has
silently dropped the morphological layer and then reports the drop as a match.
`src/alghanem/arabic/maqayis_lexical_evidence.py` therefore routes every match
through a `DerivedMorphologicalCandidate` carrying a proposed root and a written
`derivation_basis`, and refuses anything else at the boundary. The same
asymmetry is why this lexicon compared against a surface-indexed comparator
returns `NOT_COMPARABLE`: two different indexing units are not two competing
results, and `NotComparableIsNotFailure` is what keeps the refusal from being
scored as a loss.

`QuotedNumberIsNotDerivedMeasure`. The `axes_count` column is a number the
source wrote. It is kept as the source's own text and never parsed, summed, or
compared, because a number this layer converts is a number this layer is
afterwards read as having measured — the same move the candidate field guard
refuses everywhere else. `ReportedRecordIsNotCoreCandidate` follows from it:
`MaqayisRootEvidence` is deliberately *refused* by `refuse_numeric_or_verdict_fields`,
and a test asserts that refusal, so its exclusion from the fifteen-member core
ceiling is a declared boundary rather than an oversight. Its fields carry the
`_as_reported` suffix because transmission is part of the field's name, not a
comment on it.

`OneDoorToFingerprintedBytes`. The adapter opens no file. It reads through
`maqayis_root_table_deposit`, which verifies the declared length and SHA-256
before yielding a row, and a test enforces that the adapter contains no reader
of its own — a second reader would create a second door to bytes that are only
assumed to be the fingerprinted ones. Every raised `LexicalEvidenceCandidate`
carries that digest in its `source_trace`, so a witness can never be read later
as coming from a different edition.

`ThePriceIsNamedNotCounted`. Each hamza branch keeps a separate index, and each
publishes the roots it fuses by name rather than as a total: `حدأ`/`حدا`,
`دفأ`/`دفا` and `لمأ`/`لما` fuse under the bare-alif rule and nothing fuses
under the carried-alif rule. Cross-branch matching is refused outright, since
matching a signifier normalized by one rule against an index built by another
attributes one rule's effect to the other. An ambiguity produced by a rule is
recorded and never resolved.

Boundaries unchanged: this is an *adapter*, not part of the core — the core
imports nothing from it, which a test enforces — the ladder still stops at
`LexicalEvidenceCandidate`, no meaning or signified is issued, and no `kernel/`
module reads it.

## `G0.EVAL-0` — the blind evaluation boundary

`FrozenContractBeforeReaders`. A contract describes a domain and an exam; it
never carries the identity of whoever will read it. `FiberContractBody` has no
reader field, so an exam can be frozen before its opponent exists, and the
binding of readers to an exam belongs to `EvaluationBinding` alone. An exam that
waits for its second system is an exam designed after seeing one of them.

`DigestOnly != CryptographicallyHiddenGold`. Storing a digest of the answer
prevents shipping it; over a domain of five members and five sections it does not
hide it, because the combinations can be enumerated and hashed. The commitment is
therefore `H(canonical_gold ‖ nonce ‖ contract_body_digest ‖ scheme)` with a
nonce of at least 256 bits that the core never generates, never derives and never
stores. In the current madlul domain the claim is explicitly
`blind-by-boundary + commitment binding`, because the answer key is still a file
in this repository; the interface takes gold and nonce as arguments so that an
external hidden gold can replace it without changing the law.

`ASystemNameIsNotASystemIdentity`. `reading_systems = ("fractal_system_one", ...)`
is a pair of strings, and a different program can adopt the same string. A reader
identity is `implementation_digest + configuration_digest +
dependency_boundary_digest + contract_interface_version`, and carries no name at
all, so a reader cannot change after seeing the exam and keep its identity.

`ASerializedContractIsWhatTheReaderReceives`. The reader is handed canonical
bytes, never a Python object, never an adapter and never a module path. The
payload refuses to carry the commitment, the author or the node trace.

`StaticImportAudit != ProcessIsolation`. Refusing `importlib`, `__import__` and
dynamic file access in a reader's declared source strengthens the boundary and is
measured, not asserted. It does not prove the program cannot reach the repository
by other means. This phase therefore names its boundary a *declared*,
source-isolated reader boundary and records process confinement as
`DECLARED_DEFERRED` rather than claiming a sandbox it has not built.

`AFirstRunHappensOnce`. The first frozen report under a given system identity and
request is the reference. A byte-identical repeat is admissible only as a
determinism witness and never replaces the first; a differing repeat, or a second
report claiming to be the first, is refused and recorded as a violation. Any
recorded violation blocks the reveal.

`NoEvaluationVerdictBefore(FrozenContract ∧ FrozenSystemIdentity ∧
FrozenProtocol ∧ BoundRequest ∧ FrozenFirstRunReports ∧ ValidGoldReveal)`. The
reveal authority holds neither gold nor nonce: both arrive at reveal time, are
checked against the commitment, and produce a `GoldRevealRecord` that carries
neither of them. `AGoldRevealRecordIsNotAVerdict`: no comparison, no dominance
and no `Ω_M` exists in this phase, and the ceiling of any later reading remains
`ObservedDominanceWithinFrozenDomain`.

## `G0.EXEC-0` — bound reader execution

`NoRunReportWithoutBoundExecution`. A report that carries a system identity is a
claim about a system; it becomes a proof only when the identity was re-measured
at execution time, the frozen bytes themselves received the frozen payload, and
the bytes that came out were captured by the authority that ran them. The chain
is `FrozenSystemIdentity → BoundEvaluationRequest → BlindPayload(bytes) →
ExecutionAuthority → BoundExecutionReceipt → FrozenRunReport → RunLedger →
GoldRevealRecord`, and there is no parallel road to a `FrozenRunReport`.

`OnlyExecutionAuthorityIssuesExecutionReceipts` and
`AHarnessIsNotAnExecutionAuthority`. Immutability after construction is not
unforgeability of construction. A receipt exists only when the execution
authority seals it, and a report exists only when it is derived from such a
receipt, field by field, with nothing supplied by the caller. The seal closes the
public construction path; it is not a cryptographic barrier, and the qualified
claim is stated under `G0.EXEC-0.HARDEN`.

`ExecutedReaderIdentity == FrozenReaderIdentity`. The four identity components
are re-measured from the real source bytes, the real configuration and a fresh
import audit before anything runs, and recomposed with the same primitive that
froze them. A mismatch, or any boundary violation found at execution time, means
no execution is attributed to that identity.

`MeasuredBytesAreExecutedBytes`. Measuring a file and then running its path
leaves a gap between the measurement and the run. The measured bytes are
materialized into a temporary workspace outside the tree and that copy is
executed, with the workspace alone on the import path.

`ImplementationChangedDuringExecution -> NoReferenceRunReport`. The source is
re-measured after the process exits; if it moved, the event is receipted and
named, and never promoted to a reference run.

`FailureIsReceiptedButNotPromotedToReferenceRun`. Once execution is attempted,
the outcome is recorded under a closed status vocabulary rather than raised away.
A receipt is a witness to what happened, not a certificate of success; only a
`COMPLETED` receipt can become a reference run report.

`AResidualIsNamedNotStringly`. A residual is `member_id`, a code from a closed
vocabulary, a blocking flag, a reason and an evidence reference. A blocking
residual is recorded and carried into the next phase; it does not block the
reveal, because the reveal is not a verdict.

`SeparateProcess != Sandbox`. Running the reader in another interpreter process
with a pruned environment, a temporary workspace and bytes on `stdin` is a
declared execution mechanism, recorded as `SEPARATE_PROCESS_DECLARED` and not
proven confinement: there is no seccomp, no network isolation and no filesystem
sandbox in this phase.

`EvaluationBoundary != ExecutionMechanism`. The evaluation layer stays pure and
non-operational and never imports the execution layer; the execution layer
declares every operational access it takes under its own import policy.

`NoComparisonBeforeBoundExecution`. No second system, no comparison, no Pareto
dominance, no `Ω_M` and no verdict is built in this phase. The ceiling remains a
`GoldRevealRecord` conditioned on receipt-derived first run reports.

## `G0.EXEC-0.HARDEN` — execution provenance and operational configuration

`ReceiptIssuanceIsKeyedNotMerelySealed` and
`AnInProcessSealIsNotUnforgeableProvenance`. A module-private seal closes the
public API; it does not close the process. Every execution authority therefore
holds its own issuance key and signs each receipt over that receipt's canonical
content, so a receipt answers *which* authority issued it and not merely *that*
some authority did. The key's secret is never a field, never rendered and never
serialized. The standing is declared, not proven: this distinguishes issuers
inside one process and establishes neither trust across sessions nor resistance
to code already executing within the process. An isolated signing authority and a
verifiable authority-owned issuance record are deferred and are not claimed here.

`ConfigurationIsExecutedNotOnlyIdentified`. A configuration that enters the
system identity but never reaches the run proves a configuration identity, not
the execution of that configuration. The declared configuration is therefore
carried into the run inside the same measured envelope as the payload, the entry
point receives it as a second argument, and the reader returns the envelope
digest it parsed. A reader that does not accept the declared signature is refused
under its own status, and a configuration that did not arrive as written is named
a delivery mismatch rather than folded into a successful run.

`AWireValueIsRefusedNotCoerced`. A closed wire format that converts a wrong type
into an acceptable one is not closed. Every value crossing the boundary is
checked against its declared type and refused when it does not match; no value is
stringified, truthiness-tested or widened into validity.

`ATimeoutIsNamedNotFoldedIntoANonzeroExit`. A run that never exited has no exit
code, and inventing a sentinel for it both hides the event and collides with
processes killed by a signal. A run stopped at its declared ceiling is named a
timeout, a process killed by a signal is named as such, and neither is reported
as a nonzero exit.

## `G0.METRIC-0` — the fractal Arabic capability map

`ADenominatorDerivedFromTheImplementationIsNotAMeasure`. A denominator read off
the built tree measures the build against itself and reaches its own completion
the moment it finishes representing whatever it chose to represent. The
denominator of this phase is therefore declared outside the implementation, in a
package whose import policy forbids it from reading `arabic/`, `kernel/`,
`evaluation/`, `program/` or any other implementation module.

`ADeclaredDenominatorIsNotTheCompleteOntologyOfArabic`. One hundred percent here
is one hundred percent of what has been declared, not one hundred percent of
Arabic. `DeclaredArabicCapabilityUniverseV1` is an extensible declaration with a
frozen digest and a version identity; reading it as a finished ontology
attributes to the measure a claim it does not make.

`MissingImplementationDoesNotRemoveACapabilityFromTheDenominator` and
`UnimplementedCapabilityMustRemainVisible`. A capability nobody built stays in
the tree and lowers coverage truthfully. A leaf without evidence is not a
construction error but a **measured absence**, carried as a row with its stage,
its blocking reason and its next gate. Dropping it from the count would improve a
figure by deleting its question.

`TheDenominatorIsCitedNotInvented`. Every node in the declared universe carries a
named classical source and a locus within it. A node without a citation is an
opinion, not a denominator.

`StandingsAreGatesNotEpistemicMagnitudes`. The ten stages `S0_ABSENT` through
`S9_REPRODUCED` are licensing gates ordered by permission, not epistemic
magnitudes that may be summed or averaged as quantities. A stage is attained only
through the contiguous gates below it; an attested gate reached over a missing
one is recorded as a jump and does not raise the stage.

`Breadth != Readiness`. Coverage is how much of the declared domain was built;
readiness is how far the built part qualifies to carry the next layer. A parent
never exceeds the readiness of its weakest `REQUIRED` child, and the two figures
are never merged into one.

`EvidenceMustHaveAnAuthorityPath`. Every piece of evidence names a typed
authority path that issued it, and that path need not be an execution receipt: a
bound execution receipt, a measurement run manifest, a frozen formal proof, a
corpus witness, a preregistered measurement, a gold contract result, a blind
evaluation report, a transfer result and a reproduced historical experiment are
distinct genera. Forcing a census or a proof through a reader process to make it
admissible falsifies its genus instead of strengthening it. Each path licenses
only the gates proper to it; `IN_PROCESS_MEASUREMENT_REPLAY` never licenses gold,
blind, transfer or reproduction.

`RepeatedReference != IndependentEvidence`. Evidence is canonicalized on
capability, scope digest, experiment content digest, gold contract digest and
protocol digest. Citing the same experiment twice is one piece of evidence, and
the duplicate is recorded as a refusal rather than silently dropped.

`TheMetricMustBeAllowedToGoDown`. Expanding the denominator, withdrawing
evidence, or failing to reproduce a historical experiment lowers the figure. A
measure that can only rise is an announcement, not a measure. Negative evidence
therefore revokes a gate rather than being filed beside it.

`ARatioCarriesItsDenominator`. No ratio is rendered apart from its numerator, its
denominator and the source that froze that denominator. A ratio over an empty
denominator is undefined, neither zero nor complete.

`NoKernelModuleConsumesTheCapabilityMap`. No gate in `kernel/` reads this
package. It births nothing, freezes nothing and issues no verdict; it measures
what has already happened and names what has not.

## `G0.METRIC-0.HARDEN` — measurement semantics, citation provenance, denominator geometry

`NoOrdinalGateArithmeticWithoutDeclaredWeights`. A gate index is a rank of
permission, not a magnitude. Summing, averaging or dividing `gate_index` turns
nine qualitative licences into nine equal quantities and contradicts
`StandingsAreGatesNotEpistemicMagnitudes` inside the very figure that cites it. A
composite number is licensed only by a declared, frozen weight protocol that
weighs every attestable gate exactly once and justifies each weight. Absent such
a protocol the number is **undefined with a named reason**, never zero, never an
estimate, and never a default of equal weights.

`EqualDomainWeightingIsStillAWeightingProtocol`. Choosing to weigh the domains
equally is a choice of measurement geometry, not an escape from choosing. It may
not be presented as the neutral or derived figure.

`TaxonomyGranularity != CapabilityImportance`. Under leaf counting, how finely a
domain was subdivided becomes its weight. A domain split into fifteen leaves
moves the ratio nearly four times as much as one split into four, for reasons of
drafting rather than of evidence. Every coverage figure therefore names the
geometry that produced it, and domain figures are published as a profile of
separate rows rather than collapsed into one number.

`DeclaredCoverage != SystemCapability`. That every declared question is present
is a statement about the question list, not about the system. A full declaration
coverage means the denominator is complete as declared; it licenses no claim that
anything linguistic has been built.

`CitationName != VerifiedSourceLocus`. Naming a source and naming the capability
inside that source's field is not a verified locus. Every citation declares the
standing of its link — exact textual locus, section-level locus, conceptual
correspondence, modern formal extension or unverified locus — and the locators
proper to that standing are required for it and forbidden above it. A modern
formalisation may carry no page or chapter, so that it can never be read as a
quotation from a classical text. A source and an edition are distinct
declarations, and no edition identifier is issued before that edition is
verified.

`OurConceptualMapping != SourceTextAnchor`. A digest of our own formalisation is
evidence of what we wrote, not an anchor into a source text. The two are separate
fields, and a citation in which they coincide is rejected.

`KeepingAQuestionDoesNotLicenseAFalseCitation`. A question whose classical
provenance is unproven stays in the denominator — removing it would improve the
figure by deleting the question — but it is labelled for what it is. Retention
and honest labelling are one obligation, not two alternatives.

`SourceCitationDoesNotLicenseSystemCapability`. Documenting a source establishes
where the question came from. It raises no maturity gate, because nothing about
the system has been shown by it.

`UniformReadinessGate != DerivedReadinessRequirement`. A single readiness gate
declared uniformly across every node is a convention of the first version, not a
requirement derived from each capability's role. The origin of every readiness
gate is declared, and the share derived from capability role is reported
separately so the convention cannot be read as an analysis.

`DifferentMeasurementSemanticsAreNotComparableCertificates`. A certificate
carries its schema version in its own content. When the semantics of measurement
change, the digest changes as a change of contract, and figures from two schema
versions are not compared as if they measured the same thing.

## `G0.PROJ-0` — projection identity before probabilistic closure

`NoMarkovStateWithoutAProjectionIdentityCertificate`. A probabilistic state
space may not be raised over a projection whose identity has not been deposited.
The certificate names its source identity, its fold rule by digest, its boundary
rule, its fibers, its loss, its residue, its trace and its scope. Numbers
computed over an undeposited projection are arithmetic without a referent.

`TheOrderIsBoundaryThenFoldThenAdjacency`. The deposited order is

```
RawText --B--> WrittenWords --Π_F--> CarrierWords --A--> Adjacency --P--> Probability
```

and no step may be jumped. `P` in particular is not reached before `B`, `Π_F`
and `A` are deposited, each with its own published cost.

`StreamFoldingAndWordFoldingAreTwoOperationsUntilTheyAreMeasuredEqual`. Where an
implementation folds a character stream and also folds a written word, their
agreement `B(F_s(T)) = map(F_w, B(T))` is measured per deposit and per boundary
rule, never assumed. It holds only where the boundary rule consumes every
whitespace character the fold discards, and it demonstrably fails on a deposit
whose ayah separator is a newline under a space-only rule. No certificate is
issued where the two orders disagree.

`NoCertificateUnderAnUnorderedComposition`. Commutation is a requirement of
*this contract*, not a property demanded of every legitimate projection. A future
projection whose stream fold and word boundary do not commute may still be
legitimate if its composition order is explicitly deposited and argued. What is
refused here is a composition whose order is ambiguous and undeclared. The
ordering algebra itself — classifying a composition as commuting, order-required,
or unresolved — is not deposited yet, so this section issues only the refusal of
ambiguity.

`TheCollapseIsAFiberNotAPair`. Preservation and loss are read off the
equivalence classes `[w]_Π = {w' : Π(w') = Π(w)}`. A fiber of size one is a
preserved distinction; a larger fiber is a collapse group. The published figures
are derived — `N_written = Σ|f|`, `N_skeleton = |Fibers|`,
`Loss = Σ(|f| − 1)` — so that a fiber holding four written words is counted
correctly without amending the rule.

`DeclaredFold != LicensedCollapse`. That a fold rule is written establishes that
the transformation is *declared*; it does not establish that the loss of a
distinction is *permitted*. The mechanism of a collapse (declared fold,
discarded residue, or both) is descriptive and never promotes a standing. A
collapse is licensed only by an explicit written license register entry bound to
that deposit and those written forms. An empty register means nothing is
licensed.

`NoDestructiveCollapseWithoutAnOccurrenceAlignedWitness`. A collapse is called
destructive only on an independent deposited witness bound to the same source
identity and the same occurrence, showing a distinction the tree was able to
keep and the projection erased. The mere existence of another layer in the tree
is not such a witness. Absent one, the standing stays `unresolved distinction`,
and an empty destructive class is a statement about our evidence, not about
Arabic.

`APropertyThatDoesNotTransportIsNotCertifiedAsACarrierInvariant`. Failure to
transport across the deposited fonts, positions or contexts withholds a
certificate; it does not locate the property. Formally
`¬Transport(x) ⇒ ¬CertifiedCarrierInvariant(x)`, and **not**
`¬Transport(x) ⇒ PositionProperty(x) ∨ FontProperty(x)`, since the failure may
lie in the measurement, in an interaction, or in the poverty of the witness. The
output of this step is typed: each affected class is returned with the standing
`NOT_CERTIFIED_AS_CARRIER_INVARIANT`, and no name in the unit may read as
falsification (`FALSE_`, `REFUTED`, `DISPROVED`, `INVALID`), which an import
guard enforces. Withholding a certificate is not falsifying an identity.

`NoStatisticalInvarianceClaimFromAnInvarianceTheProjectionItselfMade`. Where the
projection increases repetition — three written repeats becoming five projected
repeats, fifty distinct written words becoming forty-seven skeletons — any
regularity measured downstream may be an artifact of the projection. Such a
regularity licenses no invariance claim about the text.

`ObservedAdjacency != LinguisticRelation != ProbabilisticTransition`. An edge
deposited under an explicit fold and boundary is an observed adjacency. It is
not thereby a linguistic unit, it carries no causal force, and it is not a state
transition in the probabilistic sense. The three are named apart and never
substituted for one another.

`ContractCorrectnessIsNotPopulationWidening`. The scope of this section is the
two deposits holding eighty-three words between them, and its rank is a local
declared scope name, connected to no readiness rank and to no kernel authority.
Widening the population is separate work, so that the correctness of the
contract is never read as the size of the evidence.

### What this section does not establish

It does not establish that the current folding is the correct projection for
Arabic, nor that any-whitespace is the final definition of an Arabic word, nor
that the three unresolved collapses are permitted. It re-legitimises no figure
computed over MASAQ, whose bytes remain outside the tree and whose chain
therefore stays unread.

## `G0.STATE-0` — the state space before the chain

This section governs what may enter a state space at all. It adds no statistic,
issues no transition matrix, and computes no probability. It closes one
evidential branch, constrains the survivor, deposits the ordering algebra that
`G0.PROJ-0` deferred, splits one column into two states, and leaves the two
state-space licences standing exactly where the deposited evidence leaves them.
Its units are `lexical_artifact_closure`, `suppression_expectation_floor`,
`projection_composition_order`, `sukun_state_contract` and
`markov_readiness_gate`.

`AClosedArtifactIsNotAFigureBelowAThreshold`. An excluded claim has two distinct
standings. `BELOW_THRESHOLD` falls short of a declared bar and stays a candidate
for a larger sample. `CLOSED_AS_LEXICAL_ARTIFACT` has had its corruption
mechanism diagnosed, and a larger sample strengthens that mechanism rather than
weakening it. The raw token-count "sukūn-overlap" claim is closed under
`TOKEN_REPETITION_INFLATION`: a presence claim counted token by token lets a
single high-frequency word testify repeatedly on its own behalf. The mechanism
is not asserted; its witness is the deposited distributional probe, whose best
partition was `k=2` rather than `3`, split 2,159 against 34, and whose smaller
cluster mixed genuine function words with high-frequency content words. Numbers
from a closed claim do not re-enter a freeze, and `refuse_to_freeze` always
refuses.

`APartialClosureClosesItsMeasuredShareAndNoMore`. "Fatḥa-only" shares the
mechanism only to the extent measured, so only its exposed share
`(tokens − types) / tokens` is closed. What remains is not admitted; it is *not
closed by this mechanism*, which is the difference between what has not been
shown and what has been shown false. The share is derived at read time from the
deposit bytes, never transcribed.

`AZeroWithATinyExpectationIsAnEmptyCellNotASuppression`. Absence is immune to
token-repetition inflation but not to emptiness. `obs = 0` reads as suppression
only under three deposits together: a declared null hypothesis the expectation
is computed against, a declared minimum expectation floor, and a published
distribution of zero-cell contributors counted as **types**, not tokens.
Lacking any of the three, the reading is withheld, not relaxed. Every reading
publishes its largest contributor share, so that a cell held up by one repeated
type is never read as a population. The contract register is empty here, and
the filtered CVC test is named and refused by name rather than silently unknown.

`AFailureToCommuteDoesNotItselfDepositAnOrder`. `G0.PROJ-0` made commutation a
condition of its own certificate and deferred the ordering algebra. That algebra
is deposited here as three standings: `COMMUTES`, which is measured;
`ORDER_REQUIRED`, which is *deposited* — a written record naming which side of
the composition is legal and on what ground; and `UNRESOLVED`, which is the
remainder. A composition is usable when its order is **known**, either because
it does not matter or because it is written; what is refused is ambiguity, not
non-commutation. The order register is empty on this evidence, so the single
broken cell — the Fātiḥa under the space-only rule — stands `UNRESOLVED`. That
is a statement about our deposit, not about Arabic. Its cause, a line break the
fold projects and the boundary does not eat, is live in every multi-line text,
and the Qurʾānic corpus is one; each text is classified on its own measurement
and never by generalisation.

`TheWrittenAndTheInferredAreNotOneState`. A census names sources; it does not
partition a state space. Sukūn enters as **two** states, never one: written
sukūn, whose witness is in the ink, and inferred sukūn, whose witness is a rule
of ours. Merging them turns our decision into evidence from the text, which is
the same confusion for which the lexical branch was closed. The first half of a
geminate is neither: it is evicted from the column into its own category rather
than subclassed within it. On the two deposits the split is written 21 and 27,
inferred 40 and 61, evicted 14 and 16, against raw columns of 75 and 104. No
single "sukūn total" is issued from a three-way column, and the request is
always refused with its three parts named.

`AGateThatNamesItsFirstUnmetPrerequisiteIsNotAFailure`. The prerequisites of a
state space are **ordered**, not a set: the first unmet one is the door, and
what follows it is not examined, since a later condition cannot compensate for
an earlier one. The order is lexical closure, sukūn column split, corpus bytes,
corpus projection certificate, composition order. The first two are met by the
deposits in this tree; the third is not, since the corpus bytes are neither
vendored nor declared, so every Qurʾānic figure today is a computation without a
referent. Depositing them would not open the gate, only move the standing to the
next condition.

`ANegativeProbeSuspendsTheFunctionalSplitUntilItIsDeposited`. The two
state-space licences are not one. Token Markov is `BLOCKED` at a named
prerequisite whose path is known. Functional Markov is `SUSPENDED`, which is a
different standing: it awaits a licensed functional/lexical partition that does
not exist, and the single distributional attempt at measuring one returned a
recorded negative result. Satisfying all five prerequisites does not lift the
suspension, and an import guard makes any other value for that chain impossible.

`NoTokenFigureIsIssuedWithoutItsDominanceReading`. Every figure drawn from
tokens is issued together with the leading type's share and the repeated mass;
a `TokenFigure` cannot be constructed without a dominance reading. Absent that,
the closed lexical artifact would return at a larger scale wearing a larger
number.

`AnInvarianceTheProjectionMadeIsNotAStatisticalFinding`. The statistical gate of
`G0.PROJ-0` remains in force and is now measurable per deposit: three repeated
written types become five repeated projected types on the Fatḥ āyah and remain
three on the Fātiḥa. The surplus was made by the fold, not by the text, and is
subtracted from any regularity claimed.

### What this section does not establish

It does not establish any Markov figure over the Qurʾān, functional or token,
since no such figure is computed here. It does not establish that the Fātiḥa
composition is unorderable — only that no order for it has been deposited. It
does not establish that the filtered CVC suppression result is wrong — only that
its cells, contributors, null hypothesis and expectation floor are not in this
tree, so it is refused by name rather than read. It does not re-legitimise MASAQ
or any figure computed over it, and it establishes nothing about the phonology
of Arabic; its entire subject is what may be admitted as evidence, and in what
order.
