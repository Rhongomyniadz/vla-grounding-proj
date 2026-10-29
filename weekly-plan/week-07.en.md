# Week 7: Camera and object-layout robustness

[English](week-07.en.md) | [简体中文](week-07.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Build an isolated LIBERO-plus evaluation panel and understand what changes in each perturbation.

**Start authoring when:** The base connector contract and robustness protocol are available; prepare fork integration before access, keeping base runtime validation pending.

**Run-computer prerequisite:** The base-language development pipeline and metrics work, and the base environment's dependencies and assets are recorded.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Prepare the isolated fork dependency/configuration specification, metadata mapping and variant/anchor manifest builder; review pinned source.
2. **Execute on the run computer:** After the base pipeline/metrics gates, install the fork separately, verify both backends, resolve/freeze actual variants and run development pilots and anchors.
3. **Return for review:** Return both interpreter/import/path inventories, pinned backend/assets identities, frozen variant/anchor manifests, state comparisons, pilot results/images/videos and a base recheck.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#c-evaluate-environmental-robustness): variant/anchor selection and comparison limits. [Environment guide](../doc/ENVIRONMENT.en.md): dependency/path isolation. [Code guide](../doc/CODE_GUIDE.en.md): bootstrap and planned robustness. |
| 2. Current code | [bootstrap.py](../src/vla_grounding/bootstrap.py): project-local config/assets; [simulator.py](../src/vla_grounding/simulator.py): `environment_config` and base-backend choice. |
| 3. Follow the calls | [assets.py](../src/vla_grounding/assets.py): snapshot identity and local path validation; compare fork/base import and asset reports. |
| 4. Milestone code/evidence | Fork connector/setup, metadata-to-runtime mapping, variant sampling and clean-anchor builder: planned; read actual implementation and the pinned fork code it wraps. |

Understanding goals:

- Explain why separate environments alone do not prove config/assets isolation when packages share a namespace.
- Distinguish camera-only changes, physical layout changes and unintended backend differences.
- Reconstruct frozen sampling and anchor pairing from identities; explain why selecting variants by success would bias evaluation.

## Prepare and learn

- Read the implementation plan's robustness protocol and the pinned LIBERO-plus installation, task mapping, and asset-loading code.
- Distinguish camera-only changes, changed physical layouts, and differences introduced by a separate simulator backend.
- Inspect how each environment resolves package imports, configuration, and assets so installing the fork cannot redirect the base setup.

## Reading route and expected understanding

- Read the [LIBERO-plus setup and evaluation guide](https://huggingface.co/docs/lerobot/en/libero_plus) for the fork, asset installation, and observation/control compatibility. Resolve the actual source revisions used by your environment.
- Inspect [LIBERO configuration resolution](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/__init__.py) and the corresponding code in the installed fork. Find import-time configuration behavior and verify any supported path-isolation setting.
- Use the [robustness protocol](../doc/IMPLEMENTATION_PLAN.en.md#c-evaluate-environmental-robustness) to distinguish the final panel from the small development pilots you will inspect.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Isolated robustness setup.** Declare and build a separate project environment for the pinned LIBERO-plus code/assets without replacing the base environment. Configure independent runtime/asset paths through supported interfaces, record interpreter/import/configuration locations, and rerun the base smoke after setup.
2. **Robustness connector.** Adapt the established observation, preprocessing, relative-control and requested-goal contracts to the fork. Validate actual cameras/state/action features and preserve backend/revision identity in every case/result. Fail clearly on missing assets or unsupported interfaces; do not substitute another backend.
3. **Metadata resolution and panel construction.** Read the installed task/category definitions and map each variant to its verified primary task. Resolve runtime indices by actual suite membership, validate object/goal/state references, and implement the protocol's deterministic sampling without using policy outcomes to choose variants.
4. **Clean-anchor construction.** Build clean reference cases within the same robustness backend from pinned original definitions/states. Preserve explicit links between task, variant, clean anchor and policy sampling controls. Verify unchanged physical components for camera comparisons; describe altered layout states without claiming exact matching when unsupported.
5. **Development pilots and coverage.** Execute separate development camera/layout pilots with aligned initial images, physical-state records, actions, predicates and videos. Produce a frozen final-panel coverage inventory and preserve it for later evaluation; keep pilot results separate from final-panel evidence.
6. **Isolation audit and explanations.** Verify both environments still resolve their own code/config/assets after all setup changes. Document the fork connector, metadata-to-index mapping, sampling functions, reference relationships and comparison limitations in the code guide, linking actual import/state/render diagnostics.

## Work sessions

### 1. Specify backend isolation and comparison rules (2 hours)

**Location:** Coding computer: specify isolation and supported path settings. Run computer: create the separate fork environment and verify imports/assets plus the base recheck.

**Detailed procedure**

1. Keep the working base environment intact and create a distinct project environment for the fork; record the interpreter, imported package location, and revisions for both.

2. Inspect how each installation resolves configuration and asset paths. Upstream LIBERO exposes `LIBERO_CONFIG_PATH`; verify the selected fork's implementation before relying on that setting.

3. Configure separate runtime paths through the supported mechanism, then print the resolved task, asset, and initial-state locations before rendering.

4. Run a base smoke case again after fork setup. Confirm configuring the fork has not redirected the base environment's resources.

**Expected output:** Two independently verified import/configuration/asset resolutions and a still-working base smoke case.

**If this does not work:** Separate Python environments alone do not prove that a shared user configuration file is isolated.

**Session completion checklist**

- [ ] prepare a separate LIBERO-plus environment with pinned dependencies, code, and assets, using supported configuration mechanisms.
- [ ] verify each environment imports the intended package and resolves the intended assets and initial-state files.
- [ ] Write down which camera cases can share physical states and why layout comparisons require their own explicit variant states.

### 2. Create and inspect the variant manifest (3 hours)

**Location:** Coding computer: implement mapping/sampling code. Run computer: resolve installed metadata/state identities and freeze the performance-independent manifest.

**Detailed procedure**

1. Load the fork's actual category and task metadata, then map each candidate variant back to a primary task by verified definition/name association.

2. Resolve runtime indices from the installed suite. Check one resolved entry against its task definition, category, goal, and initial-state asset.

3. Use the plan's fixed sampling rule to generate the final panel without running candidates to choose easy examples.

4. Store variant names, categories, code/assets revision, state reference, sampling seed, and mapping to the base task so the exact panel can be reconstructed.

**Expected output:** A performance-independent final variant manifest with verified task-to-variant mapping.

**If this does not work:** Missing variants or assets require a clear setup error and investigation, not silent substitution of another task or category.

**Session completion checklist**

- [ ] expose category/task metadata and resolve runtime IDs by actual suite names rather than assuming metadata IDs equal indices.
- [ ] inspect representative camera and layout cases and verify their intended target and destination.
- [ ] Freeze ten variants per task per dimension with seed 42 and explicit state/seed references, without selecting by observed policy success.

### 3. Verify clean anchors and development pilots (3 hours)

**Location:** Run computer: render clean anchors and development pilots, execute the policy and compare actual state/control/scoring.

**Detailed procedure**

1. Construct clean references within the robustness backend using the pinned original task definitions and states; do not compare against an unlabeled base-backend run.

2. Choose separate development pilots for each perturbation dimension and inspect camera images before policy execution.

3. For camera pilots, compare physical state and the parts of the task definition that should remain unchanged. For layout pilots, identify the intended object/state changes explicitly.

4. Run the same policy/processor/control contract and verify requested-goal scoring. Keep unexpected backend differences visible rather than mixing them into a camera effect.

**Expected output:** Inspectable pilot/reference pairs with a clear account of intended versus unintended changes.

**If this does not work:** If a clean reference fails to load in the fork, resolve the task/asset integration before reporting a perturbation performance drop.

**Session completion checklist**

- [ ] Construct the planned clean anchors inside the robustness backend from pinned original task definitions and states.
- [ ] Run separate development pilots for both perturbation dimensions; keep these pilot cases outside the final held-out panel.
- [ ] Compare camera images, physical state, observation mapping, scoring, and control settings; investigate unexpected backend differences before pooling anything.

### 4. Diagnose a perturbation and document the findings (2 hours)

**Location:** Coding computer: diagnose returned pilot/reference artifacts; run any controlled follow-up on the target.

**Detailed procedure**

1. Choose one development camera or layout failure.

2. Compare the reference and perturbation at initial state, image, first predicted action, subsequent executed actions, and native predicates.

3. Write a concrete hypothesis: visual target localization, physical reach/grasp difficulty, or pipeline/backend mismatch. Identify evidence that distinguishes them.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** An evidence-based perturbation diagnosis, not just a label that the model is fragile.

**If this does not work:** Do not call a changed camera crop an object displacement unless the physical state actually changed.

**Session completion checklist**

- [ ] compare one development perturbation against its appropriate clean reference using states, images, actions, and video.
- [ ] Propose why it changes behavior and identify any alternative explanation caused by the backend or scorer.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Audit the final robustness panel (2 hours)

**Location:** Coding computer: audit returned final counts and backend labels. Run computer: confirm the base environment still works.

**Detailed procedure**

1. Count final cases by primary task and dimension and check unique variant/state identities against the intended panel.

2. Audit clean anchors separately and verify all three policies will use the exact same case definitions later.

3. Check every result path and summary retains backend/category identity, even when task names match base LIBERO.

4. Save the development evidence and keep final-panel results unused until Week 10; recheck the base environment after all path changes.

**Expected output:** A frozen, complete robustness manifest and verified isolation from base evaluation.

**If this does not work:** If task counts are wrong, fix metadata resolution rather than trimming expected coverage after the fact.

**Session completion checklist**

- [ ] Verify the frozen panel contains eighty perturbed cases and eighty clean-anchor cases per policy, with recoverable mappings and no duplicates.
- [ ] Confirm base-LIBERO development still works after setting up the fork and that labels preserve backend identity.
- [ ] Prepare coverage and per-dimension summaries without reporting the development pilot as the complete LIBERO-plus benchmark.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] Base and robustness environments resolve their intended code, configuration, and assets independently.
- [ ] Camera and layout pilots have valid observations and goal scoring; backend differences are explainable.
- [ ] The final variant and anchor manifest is frozen independently of performance and has not been used for tuning.

## Optional review questions

1. Why does a layout perturbation not automatically support an exactly matched clean-state comparison?
2. What could go wrong if the two Python environments resolve the same unintended asset configuration?
3. Why must the robustness panel include clean anchors within its own backend?

## Delivery summary

> Set up the isolated LIBERO-plus environment and connector, construct and freeze variants/anchors, run development pilots and document isolation and perturbation comparisons.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Proceed when both backends are reliable, final robustness cases are frozen, and the code guide identifies the physical and visual changes in pilot examples.

