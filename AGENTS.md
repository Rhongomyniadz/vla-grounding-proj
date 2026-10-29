# Repository Instructions

## Architectural Documentation

- Read `README.md` and the relevant documents in `doc/` before coding.
- For all future coding work, ensure the relevant architectural documentation exists in both English and Simplified Chinese inside the repository-root `doc/` directory.
- Name each pair `<TOPIC>.en.md` and `<TOPIC>.zh-CN.md`. The implementation plan uses `doc/IMPLEMENTATION_PLAN.en.md` and `doc/IMPLEMENTATION_PLAN.zh-CN.md`.
- When adding or changing architecture, interfaces, responsibilities, data flow, or implementation decisions, create or update both language versions in the same change. Keep their meaning, parameters, examples, and completion status synchronized.
- Update the existing document pair for a topic instead of creating duplicate documents or per-change architecture logs. Describe the current design; keep function-level implementation details in code docstrings.
- Add links between the two language versions, and update README links when documents move or new architectural topics are added. Keep architectural documents out of the repository root.
- Chinese documentation does not change the requirement that code comments are written in English.

## Weekly Learning Plans

- Keep detailed learning and execution checklists in `weekly-plan/`, with paired `week-XX.en.md` and `week-XX.zh-CN.md` files and bilingual indexes.
- Every weekly session must include concrete step-by-step instructions, expected evidence, and troubleshooting guidance. Include a week-specific user reading syllabus with exact existing code files/symbols, relevant documentation sections, reading order and concrete understanding goals. Label future code as planned and replace it with real links when implemented. The agent performs all execution tasks, including first implementations; user exercises and review are optional. Preserve existing user attempts without requiring new ones.
- Keep weekly-plan wording focused on implementation tasks, reading, understanding goals and evidence. Do not include human/agent ownership labels or division-of-work explanations. Describe each week's required components, inputs/outputs, error handling, verification and documentation in detail.
- Keep the two language versions synchronized, including task completion status. Mark work complete only when its stated evidence exists.
- Keep architecture and experimental parameters authoritative in the paired documents in `doc/`; reference them from weekly plans instead of duplicating the specification.
- When an implementation change affects a weekly task, update the affected weekly pair alongside any relevant architectural documentation.

## Agent Ownership and Explanations

- The agent owns environment setup, dependency management, all code and experimental logic, data preparation, execution, debugging, validation, analysis, interpretation, reporting and reproduction.
- Do not reserve work for the learner or wait for a first attempt, closed-agent exercise or understanding check. User review and learning exercises are optional.
- Use authorized target access for setup, transfer and execution. If a necessary capability is unavailable, record the exact blocker and prepare the minimal unavoidable user action; continue independent work without claiming target verification.
- Maintain `doc/CODE_GUIDE.en.md` and `doc/CODE_GUIDE.zh-CN.md` with every implementation change. Cover every project-owned module, command, model, class, function and nontrivial control/data-flow structure: responsibility, source location, inputs/outputs, relationships, validation/errors, design rationale, tradeoffs and verification evidence.
- Keep the guide synchronized with actual source; label future components as planned and runtime assumptions as unverified. Keep function details in English docstrings and link to authoritative architecture/setup documents instead of duplicating them.
