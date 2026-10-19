# Weekly Learning and Implementation Plans

[English](README.en.md) | [简体中文](README.zh-CN.md)

These twelve weekly checklists translate the [implementation plan](../doc/IMPLEMENTATION_PLAN.en.md) into concrete sessions. They are planned work, not evidence that implementation or experiments have happened. All task checkboxes start unchecked.

## How to use the plans

1. Read the current week's goal, prerequisites, and concept preparation before asking the agent to code.
2. Work through five sessions: 2 + 3 + 3 + 2 + 2 = 12 active hours. Use any remaining time within the agreed 10–15-hour week for diagnosis or deeper understanding.
3. In session 4, close the agent for the first hour and do the stated exercise yourself; use the second hour for review.
4. For learner-owned logic, make the first attempt. For delegated work, use the suggested narrow agent request and define the expected evidence.
5. Mark a task complete only after checking its evidence. Keep completion status and substantive edits synchronized between the English and Chinese files.
6. Explain the understanding questions without the agent and check the handoff conditions before starting dependent work.

The session budgets include reading, coding, running small checks, and review. They do not predict unattended GPU runtime. Use measured throughput to schedule training and evaluation; if a prerequisite overruns a calendar week, carry it forward instead of dropping validation or silently shrinking the experiment.

## Where the authoritative information lives

- Architecture, evaluation definitions, task selection, training parameters, and acceptance criteria: [English implementation plan](../doc/IMPLEMENTATION_PLAN.en.md) / [Chinese implementation plan](../doc/IMPLEMENTATION_PLAN.zh-CN.md).
- Detailed session tasks and independent exercises: the weekly pairs below.
- Current implementation details: source code and docstrings once implemented.
- Observations and conceptual exploration: the existing project notebook once created.
- Experimental evidence: saved manifests, results, traces, and videos once generated.

Keep architectural documentation in `doc/`. These weekly checklists belong in `weekly-plan/` and should link to the specification instead of becoming a second architecture document. If implementation changes an agreed design, update both architectural language versions and the affected weekly pair together.

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
| 11 | [Analyze results and write your own interpretation](week-11.en.md) | [简体中文](week-11.zh-CN.md) |
| 12 | [Reproduce, demonstrate, and verify independent understanding](week-12.en.md) | [简体中文](week-12.zh-CN.md) |

## Learning and experiment boundaries

- Environment and library integration may be delegated; the episode loop, case construction, goal selection, and basic metrics belong to your first attempt.
- Development/debugging uses development initial states and permitted training/validation wording. Keep final states and final-test templates out of tuning.
- Freeze checkpoint selection before final evaluation. Keep development, selection, final, and reproduction runs explicitly labeled.
- Preserve exceptions and missing coverage. Do not invent results, silently change controls, or claim that a partial run completed the study.
- Use one current notebook for learning material rather than adding a separate narrative journal each week.
- Do not add a dashboard, another model family, physical hardware, reinforcement learning, or automatic publishing to this schedule.
- Keep changes uncommitted unless you explicitly request a commit.

## Completion

The project is complete when its software and independent-learning acceptance criteria both pass. A reproducible negative adaptation result is valid; an unexplained or incomplete pipeline is not evidence of that result.

