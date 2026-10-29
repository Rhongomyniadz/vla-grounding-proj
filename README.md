# VLA Grounding Project

Explore how a simulated robot follows language instructions using SmolVLA, LeRobot, and LIBERO. The goal is to learn robotics and embodied AI while building a reproducible evaluation and fine-tuning project.

**Status:** Week 1 source now includes observation inspection, and Week 2's canonical episode loop, chunk/action counters and aligned recording are implemented. Windows authoring and portable evidence smoke checks pass. Real RTX 5080/WSL2 setup, Week 1 runtime gates and Week 2 pilot rollouts remain unverified; no experimental results are claimed.

## Questions

- Does the policy preserve task success when an instruction is paraphrased?
- Does requesting a different object change its behavior in the same scene?
- How do camera and object-layout changes affect performance?
- Does paraphrase-based fine-tuning improve instruction following beyond an equal-budget original-instruction training control?

Language grounding is measured through observable goal selection and execution. High task success alone does not establish that a policy understands or uses language correctly.

## Approach

Start by running the pretrained SmolVLA LIBERO checkpoint, then build controlled language comparisons and a small environmental robustness study. Compare three policies:

1. The pretrained checkpoint.
2. The same checkpoint fine-tuned with original instructions.
3. The same checkpoint fine-tuned with equivalent instruction variations.

The final deliverable is a portfolio containing reproducible code, experiment manifests, machine-readable results, annotated rollout videos, plots with uncertainty estimates, and a report explaining the findings and limitations. A well-supported negative result counts as a successful outcome.

## Agent execution and explanations

The agent owns all work, including environment setup, core implementation, experiment design within the agreed protocol, execution, debugging, validation, analysis, interpretation and reproduction. User review and learning exercises are optional. The [working method](doc/IMPLEMENTATION_PLAN.en.md#1-working-method-and-ownership) defines ownership and evidence requirements.

Read the design and code guide in [English](doc/CODE_GUIDE.en.md) or [简体中文](doc/CODE_GUIDE.zh-CN.md) for the rationale, module/function structure, interfaces, data flow and verification status. The agent updates both versions with every implementation change.

## Planned environment

Write and review code on the current Windows computer. Run simulation, model inference, dataset preparation through LeRobot, and training on the separate RTX 5080 computer in Ubuntu/WSL2, using the `lerobot/smolvla_libero` checkpoint. Review returned evidence and run portable analysis on the coding computer once its required dependencies are declared. Compatibility on the target machine has not been verified yet.

The [two-computer workflow](doc/IMPLEMENTATION_PLAN.en.md#two-computer-development-and-execution) separates implementation progress from target verification. Each weekly plan identifies what can be prepared now, what must run on the target, and which evidence to return. Target-dependent checks remain open while you continue independent implementation work. The [environment guide](doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit) defines how to transfer a reviewed source snapshot, rebuild target-local paths, and bring evidence back.

## Getting started

Read the implementation plan in [English](doc/IMPLEMENTATION_PLAN.en.md) or [简体中文](doc/IMPLEMENTATION_PLAN.zh-CN.md), beginning with the first milestone. Use the environment guide in [English](doc/ENVIRONMENT.en.md) or [简体中文](doc/ENVIRONMENT.zh-CN.md) for authoring checks, transferring work between machines, and the target setup/check sequence. It explicitly distinguishes locally verified behavior from target commands awaiting verification.

Use the [code guide](doc/CODE_GUIDE.en.md#week-1-inspection-and-week-2-episode-implementation) for the implemented inspector and canonical episode loop. The [environment guide](doc/ENVIRONMENT.en.md#week-1-audit-and-week-2-pilot-commands) gives their commands and verification limits. Controlled manifest execution remains later work.

Follow the [twelve-week milestones](doc/IMPLEMENTATION_PLAN.en.md#4-twelve-week-milestones) and [completion criteria](doc/IMPLEMENTATION_PLAN.en.md#5-validation-and-completion-criteria) for the working schedule, scope boundaries, and required portfolio evidence.

## Weekly work

Use the detailed weekly guides in [English](weekly-plan/README.en.md) or [简体中文](weekly-plan/README.zh-CN.md). Each week includes detailed implementation tasks covering components, inputs/outputs, error handling, verification and documentation, followed by five step-by-step sessions. Code/document reading paths, reading order and understanding goals accompany the required evidence and troubleshooting guidance.

## References

- [SmolVLA LIBERO checkpoint](https://huggingface.co/lerobot/smolvla_libero)
- [LeRobot v0.6.1](https://github.com/huggingface/lerobot/releases/tag/v0.6.1)
- [LeRobot LIBERO integration](https://huggingface.co/docs/lerobot/en/libero)
- [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)
- [LIBERO-plus](https://github.com/sylvestf/LIBERO-plus)
- [SmolVLA parameter-efficient fine-tuning](https://huggingface.co/docs/lerobot/en/peft_training)
