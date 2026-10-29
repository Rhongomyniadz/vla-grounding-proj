# Week 12: Reproduce, demonstrate, and audit the code explanations

[English](week-12.en.md) | [简体中文](week-12.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Deliver a reviewable, reproducible portfolio with complete bilingual design/code explanations.

**Start authoring when:** The reproduction/portfolio contracts are known; draft instructions early, but final reproduction and documentation checks require Week 11 evidence.

**Run-computer prerequisite:** Week 11 provides an evidence-based report, final figures, annotated examples, and the preserved experiment artifacts.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Prepare the reproduction manifest, documented commands, portfolio links and the complete source-to-guide audit; keep the original frozen study intact.
2. **Execute on the run computer:** Create fresh isolated environments on the same run computer, verify CUDA/cameras/processors and reproduce the representative comparisons; execute any development-only loop change there.
3. **Return for review:** Return the fresh-environment source/lock/backend identities, setup and run logs, reference-versus-reproduction comparisons and videos. Review those alongside the portfolio and documentation audit here.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Environment guide](../doc/ENVIRONMENT.en.md): literal fresh setup/transfer commands. [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#5-validation-and-completion-criteria): software, explanation and portfolio gates. Read the complete [code guide](../doc/CODE_GUIDE.en.md) and final bilingual results report once delivered. |
| 2. Current code | [pyproject.toml](../pyproject.toml), [config.py](../src/vla_grounding/config.py), [assets.py](../src/vla_grounding/assets.py), [bootstrap.py](../src/vla_grounding/bootstrap.py), [runtime.py](../src/vla_grounding/runtime.py): reproduce environment and identities. |
| 3. Follow the calls | All actual episode/case/scoring, runner/resume, metrics, data/training and selection modules, following the code guide rather than an invented file layout. |
| 4. Milestone code/evidence | Reproduction manifest/comparison code and artifact links after implementation; compare original and fresh-environment evidence under documented tolerances. |

Understanding goals:

- Locate each responsibility in source and explain the full instruction-to-action-to-result path.
- Explain why the reproduction panel is representative rather than a new full-suite claim and diagnose its earliest divergence.
- Recover any showcased result from documented inputs and evidence; identify remaining limits and a justified next experiment.

## Prepare and learn

- Read the setup/run instructions as a new contributor and identify assumptions that only exist in your shell or memory.
- Review all delivery acceptance criteria in the implementation plan and choose a small representative reproduction panel.
- Distinguish reproducing a configuration and measured behavior from promising bit-identical GPU results across different runtime environments.

## Reading route and expected understanding

- Read the [software and explanation acceptance criteria](../doc/IMPLEMENTATION_PLAN.en.md#5-validation-and-completion-criteria) as actual exit conditions, not a retrospective celebration.
- Read the README's verified setup/run commands as if you had never used the project. Identify shell, path, environment, and asset assumptions.
- Review case identities, numerical tolerances, and the artifact lineage established earlier so reproduction has a concrete comparison target.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Fresh-environment reproduction procedure.** Complete the documented setup sequence using locked dependencies and immutable source/model/data/assets in fresh isolated environments. Preserve the working environments, checkpoints and final evidence. Record every actual setup command and correct missing path/environment assumptions in the existing environment guide.
2. **Representative reproduction manifest.** Build the declared small original/changed-target and robustness comparison for each policy from preserved identities. Validate source, task/state/variant, instruction, seed, backend, processors and execution settings before starting; keep the reproduction run explicitly separate from the final evaluation.
3. **Reference-to-rerun comparison.** Implement or finish comparison functions for restored states, inputs, predicted/executed actions, goal signals, stop reasons, metadata and summary metrics. Use previously justified tolerances, report the earliest divergence and investigate setup/RNG/cache differences before attributing them to numerical variation.
4. **Portfolio assembly and artifact audit.** Complete the README/report walkthrough using actual figures, annotated videos and reproducible command/evidence links. Verify every showcased result's identity and output recoverability; keep large target-hosted artifacts accessible through recorded locations without committing or publishing automatically.
5. **Complete code/document coverage.** Inventory all implemented modules, commands, records, classes and functions against both code-guide languages. Explain relationships, inputs/outputs, nontrivial control flow, validation/errors, design tradeoffs and verification status. Replace planned-code reading entries with actual source/symbol links wherever implementation exists.
6. **Final acceptance and limitations.** Reconcile software checks, final coverage, reproduction differences, documentation links/translations and weekly status against real evidence. Deliver the representative comparison records and an explicit remaining-gap list where needed. Record a justified future experiment without introducing another core feature or changing frozen claims.

## Work sessions

### 1. Prepare a fresh reproduction environment (2 hours)

**Location:** Coding computer: review/transfer the reproduction snapshot. Run computer: create fresh base/fork environments without deleting working ones and rerun input/environment gates.

**Detailed procedure**

1. Record the original working environment and artifact locations, then create a fresh project environment without removing the working one.

2. Follow the exact verified dependency/configuration procedure from the README; use locked versions and immutable model/data/assets references.

3. Identify every manual step absent from the instructions and correct the relevant existing documentation rather than adding an independent setup diary.

4. Run the environment and input-contract checks again. Confirm the fresh environment resolves the same intended processors and backend resources.

**Expected output:** A fresh environment created from documented inputs, with missing setup assumptions corrected.

**If this does not work:** Do not make reproduction pass by borrowing an undocumented global package or changing versions without recording the difference.

**Session completion checklist**

- [ ] create a fresh project environment without deleting the working setup, datasets, checkpoints, or final artifacts.
- [ ] Use locked dependencies and immutable source/artifact references, then verify CUDA, both cameras, policy inputs, and processor identity again.
- [ ] follow the documented steps literally and identify missing environment variables, paths, assets, or unstated manual steps.

### 2. Reproduce a representative comparison (3 hours)

**Location:** Run computer: execute the representative reproduction panel. Coding computer: compare returned references, actions, states and outcomes.

**Detailed procedure**

1. Build the small declared reproduction manifest with an original/changed-target pair and a robustness case for each policy.

2. Run the selected cases and compare identity, instruction, restored state/variant, policy inputs, decoded actions, end reasons, and metrics against saved references.

3. Locate the earliest divergence before attributing it to numeric nondeterminism; inspect dependency, renderer, device, seeds, queue reset, and state restoration.

4. Report what was reproduced and any remaining differences. A small reproduction check is not another complete final-suite evaluation.

**Expected output:** A concrete reference-to-reproduction comparison with explainable differences.

**If this does not work:** Do not loosen numeric tolerances after seeing outcomes merely to label a reproduction successful.

**Session completion checklist**

- [ ] Run a small explicit panel containing an original/changed-target pair and one robustness case for each of the three policies.
- [ ] Compare restored state/variant identity, actual instruction, predicted/executed actions, scoring, metadata, and outcomes with the preserved records.
- [ ] Investigate differences using documented numerical tolerances and runtime details; report remaining reproducibility limits without claiming full-suite reruns.

### 3. Complete the portfolio walkthrough (3 hours)

**Location:** Coding computer: prepare the walkthrough and audit documentation/artifact links; retain access to target-hosted large evidence.

**Detailed procedure**

1. Prepare a concise documented walkthrough: question, data flow, controlled comparisons, results, limitations, and one future experiment.

2. Choose existing annotated examples that support the quantitative story, including meaningful failure or negative evidence.

3. Verify README/report links, commands, artifact references, and the recoverability of generated outputs.

4. Keep the repository reviewable: inspect `git status --short`, review tracked changes with `git --no-pager diff`, and inspect untracked files directly. Do not publish or commit automatically.

**Expected output:** A portfolio walkthrough another person can follow from the repository to real evidence.

**If this does not work:** A polished video without a recoverable case identity and configuration is a demonstration, not a reproducible result.

**Session completion checklist**

- [ ] prepare a short explanation of the research question, system data flow, comparison design, principal findings, and limitations.
- [ ] help organize existing figures, annotated videos, artifact links, and verified setup/run commands in the README and report.
- [ ] Check that every showcased result is real and labeled, generated outputs are recoverable, and no automatic publishing or commit occurs.

### 4. Audit every code structure and its explanation (2 hours)

**Location:** Coding computer: inventory actual source and both guide languages; obtain missing runtime evidence from the target.

**Detailed procedure**

1. Enumerate all project-owned modules, commands, models, classes and functions in the actual source tree.
2. Match each structure to the bilingual code guide; verify its responsibility, inputs/outputs, relationships, errors, rationale and verification status against source.
3. Trace the episode loop, case/scorer, metrics and training pipeline through one real evidence bundle each. Correct missing explanations and stale links without altering frozen study conditions.
4. Update the weekly reading paths to actual implemented files/symbols, verify translation consistency and list any unresolved runtime questions.

**Expected output:** A complete source-to-guide coverage audit and a reproducible reading path.

**If this does not work:** Missing code or runtime evidence must stay explicitly planned/pending; documentation cannot substitute for implementation or measurements.

**Session completion checklist**

- [ ] match every implemented module, command, record, class and function to both code-guide languages.
- [ ] Verify design rationale, control/data flow, interface/error contracts and real evidence links.
- [ ] Correct missing/stale explanations and weekly reading paths; keep unresolved evidence gates open.

### 5. Perform the final explanation and repository audit (2 hours)

**Location:** Coding computer: perform the final explanation/document audit after reviewing fresh target reproduction evidence.

**Detailed procedure**

1. Document the complete perception-to-action path, paired scoring, metric grouping, training control, and one failure diagnosis.

2. Check every milestone against actual evidence and keep unsupported completion boxes unchecked in both languages.

3. Verify fresh-environment reproduction, result coverage, report claims, translation consistency, and artifact/document links.

4. Record the next justified research question as future work. Preserve the current study's scope and uncommitted review state.

**Expected output:** A completed evidence-based project and complete bilingual explanations, or an explicit list of remaining gaps.

**If this does not work:** A negative adaptation result can be complete; an unexplained broken pipeline or missing final evidence cannot be presented as that result.

**Session completion checklist**

- [ ] document a complete instruction-to-action episode, explain paired goal scoring and the adaptation control, and diagnose one saved failure.
- [ ] Verify document links, paired translations, the weekly checklist status, reproduction evidence, and report consistency; leave unfinished items visibly open.
- [ ] Record a justified next experiment as future work while keeping the current project's scope, evidence, and uncommitted review state intact.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] A fresh environment can execute the documented representative comparison and explain any reproducibility differences.
- [ ] The portfolio links verified setup, real results, uncertainty, annotated examples, and clear limitations.
- [ ] The bilingual guide covers every implemented structure and explains the system, experiments, metrics and conclusions with evidence.

## Optional review questions

1. Can you locate each core responsibility in the source and explain how its inputs become outputs?
2. What evidence would change your main conclusion, and how would you design that next experiment?
3. Can another person reproduce a selected comparison using only the repository and referenced artifacts?

## Delivery summary

> Reproduce the representative panel in fresh environments, assemble the portfolio, audit every code structure against both guide languages and verify evidence and document consistency.

## Ready for the next week

The project is complete when the software, evidence, reproduction and bilingual explanation criteria pass. Leave any unmet criterion open; a reproducible negative adaptation result is still a valid outcome.

