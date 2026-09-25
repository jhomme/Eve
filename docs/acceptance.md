# Acceptance Criteria

## Audio playback
- Selecting a preset value triggers synthesis and audio plays through the speakers within a second or two.
- The Speak button re-plays with the current phrase and settings.
- No error appears in the status bar on a normal synthesis run.

## Keyboard navigation
- Tab moves through all controls in a logical top-to-bottom order: text field, Speak button, then each list box in parameter order, then the three action buttons.
- Arrow keys move through preset choices inside each list box.
- All buttons can be activated with Space or Enter.

## NVDA announcements
- When focus moves to a list box, NVDA announces the list box label and the currently selected item.
- When an item is selected with arrow keys, NVDA announces the new item.
- When synthesis completes with an error, the status bar text is reachable (NVDA+End reads the status bar).

## Session save and resume
- Closing the window shows a Yes/No/Cancel dialog.
- Pressing Cancel leaves the window open.
- Pressing Yes saves progress and closes. On next launch the resume dialog appears.
- Pressing No closes without saving. On next launch no resume dialog appears.

## Save As New Voice
- Pressing the button opens a dialog with a text field and OK/Cancel.
- A name can be typed and confirmed with Enter or by tabbing to OK.
- After saving, the status bar confirms the name.

## Install to NVDA
- Pressing the button opens a dialog with two fields (display name, file name) and OK/Cancel.
- If not running as Administrator, a UAC prompt appears for the copy step.
- After installing, the status bar confirms. Restarting NVDA and opening Voice Settings shows the new variant in the Voice dropdown.

## Non-destructive
- The original NVDA voice files are never modified during a session.
- The temp variant file is deleted when the session ends without saving.
