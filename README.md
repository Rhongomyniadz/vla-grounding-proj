# VLA Grounding Project

Explore how a simulated robot follows language instructions using SmolVLA, LeRobot, and LIBERO. The goal is to learn robotics and embodied AI while building a reproducible evaluation and fine-tuning project.

**Status:** planning stage. This repository contains the project brief, bilingual implementation plan, and bilingual weekly learning plans. Simulation code, training pipelines, and experimental results are not implemented yet.

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

## Learning and agent assistance

The learner owns the research decisions, core experimental logic, and interpretation. The coding agent supports engineering, explanations, debugging, and review. The [learning workflow](doc/IMPLEMENTATION_PLAN.en.md#1-working-method-and-ownership) defines responsibilities, independent exercises, and understanding checks.

## Planned environment

The target is a separate RTX 5080 machine running Ubuntu through WSL2, using the `lerobot/smolvla_libero` checkpoint. The [system implementation section](doc/IMPLEMENTATION_PLAN.en.md#2-system-implementation) specifies dependency versions, isolated simulator environments, resource requirements, and verification checks. Compatibility on the target machine has not been verified yet.

## Getting started

Read the implementation plan in [English](doc/IMPLEMENTATION_PLAN.en.md) or [简体中文](doc/IMPLEMENTATION_PLAN.zh-CN.md), beginning with the first milestone. The first implementation task is a verified environment check followed by a single-episode rollout. Installation and execution commands will be documented after they work on the target machine.

Follow the [twelve-week milestones](doc/IMPLEMENTATION_PLAN.en.md#4-twelve-week-milestones) and [completion criteria](doc/IMPLEMENTATION_PLAN.en.md#5-validation-and-completion-criteria) for the working schedule, scope boundaries, and required portfolio evidence.

## Weekly work

Use the detailed weekly checklists in [English](weekly-plan/README.en.md) or [简体中文](weekly-plan/README.zh-CN.md). Each week includes five work sessions, your own coding exercises, agent-assisted tasks, deliverables, and understanding checks.

## References

- [SmolVLA LIBERO checkpoint](https://huggingface.co/lerobot/smolvla_libero)
- [LeRobot v0.6.1](https://github.com/huggingface/lerobot/releases/tag/v0.6.1)
- [LeRobot LIBERO integration](https://huggingface.co/docs/lerobot/en/libero)
- [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)
- [LIBERO-plus](https://github.com/sylvestf/LIBERO-plus)
- [SmolVLA parameter-efficient fine-tuning](https://huggingface.co/docs/lerobot/en/peft_training)
