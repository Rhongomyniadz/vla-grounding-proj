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
- Keep the two language versions synchronized, including task completion status. Mark work complete only when its stated evidence exists.
- Keep architecture and experimental parameters authoritative in the paired documents in `doc/`; reference them from weekly plans instead of duplicating the specification.
- When an implementation change affects a weekly task, update the affected weekly pair alongside any relevant architectural documentation.
