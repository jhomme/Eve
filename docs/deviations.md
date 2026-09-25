# Deviations

Changes from prd.md or Plan.md, with date, reason, and who decided.

---

## 2026-09-25 — GUI instead of CLI

Original prd.md described a console-based CLI tool with a numbered menu system. The implementation was changed to a wxPython GUI with list boxes, a text field, and buttons.

Why: A GUI with native controls gives NVDA better announcements out of the box than a console menu. It also removes the need to type numbers and press Enter for every action.

Decided by: Jim.
