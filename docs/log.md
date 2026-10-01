# Log

---

## 2026-09-28

Created tests/test_voice_lab.py with 31 pytest tests covering Variant, get_leading_key, read_nvda_config, and PARAMETERS/SUBMENUS data consistency. wx is stubbed at import time so tests run headlessly. All 31 pass. Added .venv/ to .gitignore. VoiceLabFrame, synthesize_and_play, and the install path are not tested (require a running wx app or eSpeak binary).

---

## 2026-09-27

Created GitHub repo jhomme/Eve and pushed all commits. Cut release 0.1.0: added requirements.txt, added `__version__ = "0.1.0"` to voice_lab.py, rewrote README for a semi-technical audience with plain-English install steps, download instructions, eSpeak NG and Python links, feedback/issues section, and credits. Tagged v0.1.0 and published GitHub release with matching release notes.

---

## 2026-09-25

Rewrote voice_lab.py from a console CLI to a wxPython GUI. Controls: multiline text field for the test phrase, one list box per parameter (10 total), Speak / Save As New Voice / Install to NVDA / Quit buttons, status bar, close dialog offering to save progress.

Renamed docs/voice-lab.md to docs/Plan.md and rewrote it to describe the GUI. Created bookmarks.md, docs/acceptance.md, docs/deviations.md, docs/log.md, and docs/postMortem.md.

Open question: synthesize_and_play does not include a playback call — audio may be silent. Needs testing.
