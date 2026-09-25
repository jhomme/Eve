# Voice Lab

A wxPython GUI for editing eSpeak NG voice variant files and previewing them through NVDA in real time.

---

## Requirements

- eSpeak NG installed at `C:\Program Files\eSpeak NG\espeak-ng.exe`
- NVDA installed at `C:\Program Files\NVDA\` and currently running
- NVDA must be configured to use the eSpeak NG synthesizer (set in NVDA's Voice Settings)
- Python with wxPython installed in the project's .venv

---

## How to Run

```
.venv\Scripts\python voice_lab.py
```

On startup Voice Lab reads your current eSpeak voice from `%APPDATA%\nvda\nvda.ini`. If NVDA is not using eSpeak NG, a dialog box appears with instructions and the app exits.

If a saved session is found, a dialog asks whether to continue from where you left off or start fresh from your current NVDA voice.

---

## Workflow

1. The app opens showing all parameters at once in a single scrollable window.
2. Move between controls with Tab and Shift+Tab. Use arrow keys inside a list box to select a preset value.
3. Each time you select a preset, Voice Lab updates the working variant file and synthesizes audio immediately.
4. Edit the text in the "Text to speak" field to test specific words or phrases, then press the Speak button or Enter.
5. When the voice sounds right, use Save As New Voice to keep a named copy, or Install to NVDA to put it in NVDA's voice data folder.
6. When you close the window, a dialog asks whether to save progress so you can resume later.

Changes are non-destructive: the tool works on a temporary copy (`_voicelab_temp`) and never modifies your original NVDA voice files.

---

## Controls

### Text to speak
A multiline text field pre-filled with a test phrase. Edit it to try specific words. Press Enter or Tab to the Speak button and activate it.

### Parameter list boxes (one per parameter)
Ten list boxes, one for each tunable parameter. Arrow up and down to move through preset values. Selecting a value triggers synthesis immediately.

### Speak button
Re-synthesizes and plays the current phrase with the current settings.

### Save As New Voice button
Saves the working variant as a named file inside the local espeak-ng-data folder. Prompts for a voice name.

### Install to NVDA button
Copies the variant into NVDA's voice data folder. Prompts for a display name (shown in NVDA's Voice list) and a file name (one word, no spaces). If the app is not running as Administrator, it triggers a UAC prompt for that copy step only.

After installing, restart NVDA and open Preferences > Speech to select the new variant from the Voice dropdown.

### Quit button
Closes the window. Equivalent to pressing Alt+F4.

---

## Parameters

### 1. Klatt Model

Selects which formant-synthesis algorithm eSpeak uses to generate the voice. Higher numbers add more synthesis stages, producing a richer but potentially more synthetic sound. Model 1 is the simplest and cleanest; model 6 is the most elaborate.

- klatt 1 — Cleanest, least complex
- klatt 2–4 — Intermediate
- klatt 5 — Used by the built-in "edward" variant
- klatt 6 — edward2 default; most complex

---

### 2. Voicing

Controls how strongly the vocal cords vibrate during speech. Lower values let more unvoiced air through, creating a breathy or airy quality. Higher values produce a fuller, more resonant tone.

- voicing 60 — Breathy
- voicing 75 — Airy
- voicing 90 — Moderate
- voicing 100 — Full (edward2 default)
- voicing 120 — Extra
- voicing 150 — Maximum

---

### 3. Flutter

Adds small, random pitch variations over time, mimicking the natural wavering of a real voice. A value of 0 gives a perfectly steady, robotic tone. Higher values make the voice sound more organic and human.

- flutter 0 — None — perfectly steady
- flutter 1 — Very low
- flutter 2 — Low
- flutter 4 — Moderate
- flutter 6 — Natural
- flutter 8 — High

---

### 4. Roughness

Injects irregular noise into the voice signal, simulating hoarseness or graininess. A value of 0 produces a smooth, clean sound; higher values make the voice increasingly raspy or gravelly. Useful for adding texture, age, or grit to a voice.

- roughness 0 — Smooth
- roughness 1 — Very low
- roughness 2 — Low
- roughness 4 — Moderate
- roughness 6 — Rough
- roughness 8 — Very rough

---

### 5. Pitch Range

Sets the low and high pitch boundaries eSpeak uses when inflecting speech. A narrow range produces a flatter, more monotone delivery; a wide range creates expressive, varied intonation. The two numbers are the bottom and top of the pitch envelope in percent.

- pitch 75 95 — Very narrow — almost monotone
- pitch 70 100 — Narrow
- pitch 65 108 — Moderate
- pitch 60 115 — Wide setting
- pitch 55 125 — Wide
- pitch 50 135 — Very wide — very expressive

---

### 6. Consonants

Controls the amplitude and sharpness of consonant sounds relative to vowels. The first number sets overall consonant volume; the second controls how crisply they are articulated. Boosting sharpness improves clarity; reducing it softens the edges of words.

Format: `consonants <amplitude> <sharpness>`

---

### 7–10. Formants 1–4

Formants are the resonant frequencies of the vocal tract. Each is set with three numbers: `formant <n> <frequency%> <amplitude%> <width%>`.

- Formant 1 — Vowel darkness/brightness, shaped by jaw opening. Lower = darker; higher = brighter.
- Formant 2 — Vowel frontness/backness, shaped by tongue position. Lower = back/round; higher = front/bright.
- Formant 3 — Voice timbre and individual character. Subtler than F1/F2; shapes the overall personality of the voice.
- Formant 4 — Upper resonance color. Affects presence and projection; changes are subtle.

---

## Session Files

- `espeak-ng-data/voices/!v/_voicelab_temp` — Working copy of the variant (deleted on exit)
- `_voicelab_in_progress` — Saved session state for resuming later

---

## Work remaining

- [ ] Confirm audio playback works (synthesize_and_play may be silent — needs testing)
- [ ] Test tab order and NVDA announcements for all controls
- [ ] Test the close/save-progress dialog with keyboard
- [ ] Test Install to NVDA and the UAC elevation path
- [ ] Decide whether "current setting" labels in list boxes should reflect the actual loaded values dynamically
