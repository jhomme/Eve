# Log

---

## 2026-09-25

Rewrote voice_lab.py from a console CLI to a wxPython GUI. Controls: multiline text field for the test phrase, one list box per parameter (10 total), Speak / Save As New Voice / Install to NVDA / Quit buttons, status bar, close dialog offering to save progress.

Renamed docs/voice-lab.md to docs/Plan.md and rewrote it to describe the GUI. Created bookmarks.md, docs/acceptance.md, docs/deviations.md, docs/log.md, and docs/postMortem.md.

Open question: synthesize_and_play does not include a playback call — audio may be silent. Needs testing.
