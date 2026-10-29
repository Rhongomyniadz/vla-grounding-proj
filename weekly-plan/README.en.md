# Weekly Execution and Reading Plans

[English](README.en.md) | [简体中文](README.zh-CN.md)

These twelve checklists translate the [implementation plan](../doc/IMPLEMENTATION_PLAN.en.md) into weekly implementation, execution and reading tasks. Each plan specifies prerequisites, implementation scope, code/document reading paths, understanding goals, procedures, troubleshooting and required evidence.

Checkboxes record verified evidence. Week 1 inspection and Week 2 canonical episode source are available; real target gates, pilot rollouts and experimental results remain unverified. A written implementation alone does not mark a runtime check complete.

## How to use the plans

1. Read the goal, prerequisites and pinned source before implementing the week's scope.
2. Use the five session estimates as planning aids; unattended GPU time must be estimated separately from real measurements.
3. Follow each week's **What to read and understand** section: documentation first, current source, call paths, then the milestone's new code/evidence. Each list names files/symbols and three understanding goals. Replace planned-file descriptions with actual links when implemented.
4. Use Session 4 to audit evidence and explain the findings in the relevant bilingual `doc/` document. Use the review questions to check understanding.
5. Update the [code guide](../doc/CODE_GUIDE.en.md) with design rationale, every implemented structure, interfaces, errors and verification evidence in the same change as the code.
6. Run applicable local checks and real target checks; synchronize English/Chinese completion status only when the stated evidence exists.
7. Continue independent later authoring while target gates are pending. Execute dependent experiments only after their prerequisites pass.

Command blocks identify the intended shell and machine. Install project-local environments and inspect the pinned source before calling an API. Do not assume planned commands already exist. Estimate long jobs from real throughput and carry work forward rather than skipping checks or silently reducing the experiment.

## Working across the two computers

Follow the [execution locations and gate order](../doc/IMPLEMENTATION_PLAN.en.md#two-computer-development-and-execution) and [transfer/evidence procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit).

1. On Windows, implement and check portable work, prepare exact target commands and freeze a reviewed source snapshot including required uncommitted files.
2. With authorized target access, transfer the snapshot, verify hashes, rebuild WSL-local environments and paths, and run the smallest real integration checks before long jobs.
3. Return reports, records, images/videos and traces with their run/source identities, review coverage and errors, and perform portable analysis with declared dependencies.
4. Track **authoring ready**, **target verified** and bilingual documentation separately. Missing runtime evidence stays pending; never invent IDs, hashes, observations or measurements.
5. If target access or an OS-level action is unavailable, record the specific blocker and required setup action, keep dependent runtime checks pending and continue independent preparation.

The twelve weeks describe dependency milestones; target availability may spread one milestone across calendar weeks.

## Where the authoritative information lives

- Architecture, protocol, parameters and acceptance: [English implementation plan](../doc/IMPLEMENTATION_PLAN.en.md) / [中文](../doc/IMPLEMENTATION_PLAN.zh-CN.md).
- Setup, source transfer and evidence return: [English environment guide](../doc/ENVIRONMENT.en.md) / [中文](../doc/ENVIRONMENT.zh-CN.md).
- Every implemented code structure and design rationale: [English code guide](../doc/CODE_GUIDE.en.md) / [中文](../doc/CODE_GUIDE.zh-CN.md); detailed function semantics remain in docstrings.
- Step-by-step execution, evidence and troubleshooting: weekly pairs below.
- Measured findings: the bilingual results report when real results exist, linked to saved manifests, records, traces and videos.

Keep architectural explanations in `doc/` and session checklists in `weekly-plan/`. Update existing topic pairs rather than duplicating specifications or creating weekly narrative logs.

## Weekly index

| Week | English plan | Chinese plan |
| --- | --- | --- |
| 1 | [Environment and the perception-to-action pipeline](week-01.en.md) | [简体中文](week-01.zh-CN.md) |
| 2 | [Write and understand one complete robot episode](week-02.en.md) | [简体中文](week-02.zh-CN.md) |
| 3 | [Reproducible resets and an action-horizon exercise](week-03.en.md) | [简体中文](week-03.zh-CN.md) |
| 4 | [Experiment manifests, reliable execution, and resumption](week-04.en.md) | [简体中文](week-04.zh-CN.md) |
| 5 | [Language cases and correct goal scoring](week-05.en.md) | [简体中文](week-05.zh-CN.md) |
| 6 | [Metrics, uncertainty, and a development baseline](week-06.en.md) | [简体中文](week-06.zh-CN.md) |
| 7 | [Camera and object-layout robustness](week-07.en.md) | [简体中文](week-07.zh-CN.md) |
| 8 | [Demonstration data and a verified LoRA smoke run](week-08.en.md) | [简体中文](week-08.zh-CN.md) |
| 9 | [Run the two controlled fine-tuning arms](week-09.en.md) | [简体中文](week-09.zh-CN.md) |
| 10 | [Select checkpoints and execute the frozen final study](week-10.en.md) | [简体中文](week-10.zh-CN.md) |
| 11 | [Analyze results and document the interpretation](week-11.en.md) | [简体中文](week-11.zh-CN.md) |
| 12 | [Reproduce, demonstrate, and audit the code explanations](week-12.en.md) | [简体中文](week-12.zh-CN.md) |

## Learning and experiment boundaries

- Development/debugging uses development initial states and permitted training/validation wording. Keep final states and final-test templates out of tuning.
- Freeze checkpoint selection before final evaluation. Keep development, selection, final, and reproduction runs explicitly labeled.
- Preserve exceptions and missing coverage. Do not invent results, silently change controls, or claim that a partial run completed the study.
- Maintain current design/code explanations in the paired documents in `doc/`; keep experimental evidence separate from conceptual notes.
- Do not add a dashboard, another model family, physical hardware, reinforcement learning, or automatic publishing to this schedule.
- Keep changes uncommitted unless a commit is explicitly requested.

## Completion

The project is complete when its software, evidence, reproduction and bilingual documentation criteria pass. A reproducible negative adaptation result is valid; an unexplained or incomplete pipeline is not evidence of that result.

