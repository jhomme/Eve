#!/usr/bin/env python3
"""
Voice Lab -- eSpeak NG variant editor for NVDA
wxPython GUI with accessible native controls.
"""
import ctypes
import os
import shutil
import subprocess
import threading
from pathlib import Path

import wx

ESPEAK_EXE = Path(r"C:\Program Files\eSpeak NG\espeak-ng.exe")
DATA_DIR = Path(__file__).parent / "espeak-ng-data"
VARIANTS_DIR = DATA_DIR / "voices" / "!v"
NVDA_VARIANTS = Path(r"C:\Program Files\NVDA\synthDrivers\espeak-ng-data\voices\!v")
NVDA_CONFIG = Path(os.environ["APPDATA"]) / "nvda" / "nvda.ini"
VARIANT_NAME = "_voicelab_temp"
IN_PROGRESS_FILE = Path(__file__).parent / "_voicelab_in_progress"
OUTPUT_WAV = Path(__file__).parent / "test.wav"
TEST_PHRASE = "Hello, this is a test of the custom voice variant. How does it sound?"

PARAMETERS = {
    "klatt": {
        "label": "klatt model",
        "desc": "synthesis engine; higher = more complex",
        "keys": ["klatt"],
        "help": (
            "The Klatt model selects which formant-synthesis algorithm eSpeak uses to generate the voice. "
            "Higher numbers add more synthesis stages, producing a richer but potentially more synthetic sound. "
            "Model 1 is the simplest and cleanest; model 6 is the most elaborate."
        ),
    },
    "voicing": {
        "label": "voicing",
        "desc": "vocal cord vibration; lower = breathier",
        "keys": ["voicing"],
        "help": (
            "Voicing controls how strongly the vocal cords vibrate during speech. "
            "Lower values let more unvoiced air through, creating a breathy or airy quality. "
            "Higher values produce a fuller, more resonant tone."
        ),
    },
    "flutter": {
        "label": "flutter",
        "desc": "natural pitch wavering",
        "keys": ["flutter"],
        "help": (
            "Flutter adds small, random pitch variations over time, mimicking the natural wavering of a real voice. "
            "A value of 0 gives a perfectly steady, robotic tone. "
            "Higher values make the voice sound more organic and human."
        ),
    },
    "roughness": {
        "label": "roughness",
        "desc": "hoarseness / graininess",
        "keys": ["roughness"],
        "help": (
            "Roughness injects irregular noise into the voice signal, simulating hoarseness or graininess. "
            "A value of 0 produces a smooth, clean sound; higher values make the voice increasingly raspy or gravelly. "
            "It is useful for adding texture, age, or grit to a voice."
        ),
    },
    "pitch": {
        "label": "pitch range",
        "desc": "monotone vs. expressive intonation",
        "keys": ["pitch"],
        "help": (
            "Pitch range sets the low and high pitch boundaries eSpeak uses when inflecting speech. "
            "A narrow range produces a flatter, more monotone delivery; a wide range creates expressive, varied intonation. "
            "The two numbers are the bottom and top of the pitch envelope in percent."
        ),
    },
    "consonants": {
        "label": "consonants",
        "desc": "loudness and crispness of consonants",
        "keys": ["consonants"],
        "help": (
            "Consonants controls the amplitude and sharpness of consonant sounds relative to vowels. "
            "The first number sets overall consonant volume; the second controls how crisply they are articulated. "
            "Boosting sharpness improves clarity; reducing it softens the edges of words."
        ),
    },
    "formant1": {
        "label": "formant 1",
        "desc": "vowel darkness/brightness (jaw opening)",
        "keys": ["formant 1"],
        "help": (
            "The first formant is the lowest resonant frequency of the vocal tract, shaped mainly by jaw opening. "
            "Lowering it darkens vowel sounds; raising it brightens them. "
            "It has the strongest single effect on the perceived openness and warmth of the voice."
        ),
    },
    "formant2": {
        "label": "formant 2",
        "desc": "vowel frontness/backness (tongue position)",
        "keys": ["formant 2"],
        "help": (
            "The second formant is shaped by front-to-back tongue position in the mouth. "
            "Lower values push vowels toward the back (darker, rounder); higher values bring them forward (brighter, more nasal). "
            "It most strongly distinguishes vowels like 'ee' from 'oo'."
        ),
    },
    "formant3": {
        "label": "formant 3",
        "desc": "voice timbre and color",
        "keys": ["formant 3"],
        "help": (
            "The third formant contributes to the individual timbre and character of a voice rather than to specific vowel identity. "
            "Adjusting it can make a voice sound warmer, thinner, or more distinctive. "
            "Changes here are subtler than formants 1 and 2 but shape the overall personality of the voice."
        ),
    },
    "formant4": {
        "label": "formant 4",
        "desc": "upper resonance color",
        "keys": ["formant 4"],
        "help": (
            "The fourth formant shapes upper-frequency resonance, adding brightness or ring to the voice. "
            "It contributes to a sense of presence and projection. "
            "Changes are subtle but can make a voice sound more alive or more muffled."
        ),
    },
}

SUBMENUS = {
    "klatt": [
        ("klatt 1", "cleanest, least complex"),
        ("klatt 2", ""),
        ("klatt 3", ""),
        ("klatt 4", ""),
        ("klatt 5", "used by edward"),
        ("klatt 6", "edward2 default, most complex"),
    ],
    "voicing": [
        ("voicing 60",  "breathy"),
        ("voicing 75",  "airy"),
        ("voicing 90",  "moderate"),
        ("voicing 100", "full (edward2 default)"),
        ("voicing 120", "extra"),
        ("voicing 150", "maximum"),
    ],
    "flutter": [
        ("flutter 0", "none -- perfectly steady"),
        ("flutter 1", "very low"),
        ("flutter 2", "low (current setting)"),
        ("flutter 4", "moderate"),
        ("flutter 6", "natural"),
        ("flutter 8", "high"),
    ],
    "roughness": [
        ("roughness 0", "smooth"),
        ("roughness 1", "very low (current setting)"),
        ("roughness 2", "low"),
        ("roughness 4", "moderate"),
        ("roughness 6", "rough"),
        ("roughness 8", "very rough"),
    ],
    "pitch": [
        ("pitch 75 95",  "very narrow -- almost monotone"),
        ("pitch 70 100", "narrow"),
        ("pitch 65 108", "moderate"),
        ("pitch 60 115", "current setting"),
        ("pitch 55 125", "wide"),
        ("pitch 50 135", "very wide -- very expressive"),
    ],
    "consonants": [
        ("consonants 50 65", "soft amplitude, current sharpness"),
        ("consonants 60 65", "moderate amplitude, current sharpness"),
        ("consonants 70 65", "current amplitude, current sharpness"),
        ("consonants 80 65", "loud amplitude, current sharpness"),
        ("consonants 70 50", "current amplitude, smoother"),
        ("consonants 70 55", "current amplitude, slightly smoother"),
        ("consonants 70 75", "current amplitude, crisper"),
        ("consonants 70 85", "current amplitude, sharp"),
    ],
    "formant1": [
        ("formant 1 80 100 100",  "lower frequency -- darker vowels"),
        ("formant 1 86 100 100",  "slightly dark"),
        ("formant 1 92 100 100",  "current setting"),
        ("formant 1 100 100 100", "neutral frequency"),
        ("formant 1 108 100 100", "higher frequency -- brighter vowels"),
        ("formant 1 92 80 100",   "current freq, quieter"),
        ("formant 1 92 120 100",  "current freq, louder"),
        ("formant 1 92 100 75",   "current freq, narrow width -- tighter"),
        ("formant 1 92 100 130",  "current freq, wide width -- throatier"),
    ],
    "formant2": [
        ("formant 2 90 100 80",  "lower frequency"),
        ("formant 2 96 100 80",  "slightly lower"),
        ("formant 2 103 100 80", "current setting"),
        ("formant 2 110 100 80", "slightly higher"),
        ("formant 2 118 100 80", "higher frequency"),
        ("formant 2 103 80 80",  "current freq, quieter"),
        ("formant 2 103 120 80", "current freq, louder"),
        ("formant 2 103 100 60", "current freq, narrow width"),
        ("formant 2 103 100 100","current freq, wider"),
    ],
    "formant3": [
        ("formant 3 90 100 70",  "lower frequency"),
        ("formant 3 96 100 70",  "slightly lower"),
        ("formant 3 103 100 70", "current setting"),
        ("formant 3 110 100 70", "slightly higher"),
        ("formant 3 118 100 70", "higher frequency"),
        ("formant 3 103 80 70",  "current freq, quieter"),
        ("formant 3 103 120 70", "current freq, louder"),
        ("formant 3 103 100 50", "current freq, narrow width"),
        ("formant 3 103 100 90", "current freq, wider"),
    ],
    "formant4": [
        ("formant 4 100 100 60", "lower frequency"),
        ("formant 4 107 100 60", "slightly lower"),
        ("formant 4 114 100 60", "current setting"),
        ("formant 4 121 100 60", "slightly higher"),
        ("formant 4 128 100 60", "higher frequency"),
        ("formant 4 114 80 60",  "current freq, quieter"),
        ("formant 4 114 120 60", "current freq, louder"),
        ("formant 4 114 100 40", "current freq, narrow width"),
        ("formant 4 114 100 80", "current freq, wider"),
    ],
}

MAIN_MENU_ORDER = [
    "klatt", "voicing", "flutter", "roughness",
    "pitch", "consonants",
    "formant1", "formant2", "formant3", "formant4",
]

_current_voice = "en-us"


class Variant:
    def __init__(self, path: Path):
        self.path = path
        self.lines: list[str] = path.read_text(encoding="utf-8").splitlines()

    def _find(self, key: str) -> int:
        for i, line in enumerate(self.lines):
            if line.startswith(key + " ") or line.startswith(key + "\t") or line == key:
                return i
        return -1

    def get_raw(self, key: str) -> str:
        i = self._find(key)
        return self.lines[i].strip() if i >= 0 else "(not set)"

    def set_line(self, key: str, full_line: str):
        i = self._find(key)
        if i >= 0:
            self.lines[i] = full_line
        else:
            self.lines.append(full_line)

    def reload(self):
        self.lines = self.path.read_text(encoding="utf-8").splitlines()

    def save(self):
        self.path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")

    def show(self):
        print("\n--- Current variant ---")
        for line in self.lines:
            if line.strip():
                print(f"  {line}")
        print()


def get_leading_key(line: str) -> str:
    parts = line.split()
    if len(parts) >= 2 and parts[0] == "formant":
        return f"formant {parts[1]}"
    return parts[0] if parts else ""


def read_nvda_config():
    """Return (synth, voice, variant) from NVDA's config. variant may be None."""
    if not NVDA_CONFIG.exists():
        return None, None, None
    synth = voice = variant = None
    in_speech = in_espeak = False
    for line in NVDA_CONFIG.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s == "[speech]":
            in_speech, in_espeak = True, False
        elif s.startswith("[") and not s.startswith("[["):
            in_speech, in_espeak = False, False
        elif in_speech:
            if s == "[[espeak]]":
                in_espeak = True
            elif s.startswith("[["):
                in_espeak = False
            elif "=" in s:
                k, _, v = s.partition("=")
                k, v = k.strip(), v.strip()
                if not in_espeak and k == "synth":
                    synth = v
                elif in_espeak and k == "voice":
                    voice = v
                elif in_espeak and k == "variant":
                    variant = v
    return synth, voice, variant


def synthesize_and_play(variant: Variant, voice: str, phrase: str = TEST_PHRASE,
                        cancel_event: threading.Event | None = None):
    variant.save()
    voice_arg = f"{voice}+{VARIANT_NAME}" if voice else VARIANT_NAME
    cmd = [
        str(ESPEAK_EXE),
        f"--path={DATA_DIR}",
        "-v", voice_arg,
        phrase,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    while proc.poll() is None:
        if cancel_event and cancel_event.is_set():
            proc.kill()
            proc.wait()
            return None
    if proc.returncode not in (0, -9):
        return f"Synthesis error: {proc.stderr.read().decode(errors='replace').strip()}"
    return None



class _InstallDialog(wx.Dialog):
    def __init__(self, parent, default_display="", default_file=""):
        super().__init__(parent, title="Install to NVDA")
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        lbl1 = wx.StaticText(panel, label="Display name (shown in NVDA Voice Settings):")
        self.display_ctrl = wx.TextCtrl(panel, value=default_display or VARIANT_NAME)
        lbl2 = wx.StaticText(panel, label="File name (one word, no spaces):")
        self.file_ctrl = wx.TextCtrl(panel, value=default_file or VARIANT_NAME)

        for w in (lbl1, self.display_ctrl, lbl2, self.file_ctrl):
            sizer.Add(w, 0, wx.EXPAND | wx.ALL, 5)

        btn_sizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        panel.SetSizer(sizer)
        sizer.Fit(self)
        self.display_ctrl.SetFocus()

    def get_values(self):
        return self.display_ctrl.GetValue().strip(), self.file_ctrl.GetValue().strip()


class VoiceLabFrame(wx.Frame):
    def __init__(self, variant: "Variant", voice: str, defer_init: bool = False):
        super().__init__(None, title="Voice Lab — eSpeak NG Variant Editor")
        self._variant = variant
        self._voice = voice
        self._saved_display = ""
        self._saved_file = ""
        self._synth_timer = None
        self._synth_lock = threading.Lock()
        self._cancel_event = threading.Event()

        self.CreateStatusBar()
        self.SetStatusText("Ready.")
        self._build_ui()
        self.Show()
        self._phrase_ctrl.SetFocus()
        if not defer_init:
            self._preselect_all()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        outer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)

        # Text-to-speak area
        phrase_label = wx.StaticText(panel, label="Text to speak:")
        self._phrase_ctrl = wx.TextCtrl(
            panel, value=TEST_PHRASE,
            style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER,
        )
        self._phrase_ctrl.SetMinSize((-1, 60))
        speak_btn = wx.Button(panel, label="&Speak")
        speak_btn.Bind(wx.EVT_BUTTON, self._on_speak)

        outer.Add(phrase_label, 0, wx.ALL, 6)
        outer.Add(self._phrase_ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 6)
        outer.Add(speak_btn, 0, wx.ALL, 6)

        # Parameter list boxes
        self._listboxes: dict[str, wx.ListBox] = {}
        self._last_selection: dict[str, int] = {}
        for key in MAIN_MENU_ORDER:
            param = PARAMETERS[key]
            box_label = f"{param['label']} — {param['desc']}"
            lbl = wx.StaticText(panel, label=box_label)
            lbl.SetWindowStyleFlag(wx.ST_NO_AUTORESIZE)
            outer.Add(lbl, 0, wx.LEFT | wx.TOP | wx.RIGHT, 6)

            items = [desc if desc else full_line for full_line, desc in SUBMENUS[key]]
            lb = wx.ListBox(panel, choices=items, style=wx.LB_SINGLE)
            lb.Bind(wx.EVT_LISTBOX, self._make_listbox_handler(key))
            self._listboxes[key] = lb
            outer.Add(lb, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 6)

        # Action buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_btn = wx.Button(panel, label="Save As &New Voice")
        open_btn = wx.Button(panel, label="&Open Voice")
        install_btn = wx.Button(panel, label="&Install to NVDA")
        quit_btn = wx.Button(panel, label="&Quit")
        save_btn.Bind(wx.EVT_BUTTON, self._on_save)
        open_btn.Bind(wx.EVT_BUTTON, self._on_open)
        install_btn.Bind(wx.EVT_BUTTON, self._on_install)
        quit_btn.Bind(wx.EVT_BUTTON, self._on_quit)
        for b in (save_btn, open_btn, install_btn, quit_btn):
            btn_sizer.Add(b, 0, wx.ALL, 6)
        outer.Add(btn_sizer, 0, wx.ALL, 4)

        panel.SetSizer(outer)
        outer.Fit(panel)
        self.SetClientSize(panel.GetBestSize())
        self.Bind(wx.EVT_CLOSE, self._on_close)

    # ------------------------------------------------------------------
    # Startup: pre-select current settings in each listbox
    # ------------------------------------------------------------------

    def _preselect_all(self):
        for key in MAIN_MENU_ORDER:
            lb = self._listboxes[key]
            lookup_keys = PARAMETERS[key]["keys"]
            current_raw = " / ".join(self._variant.get_raw(k) for k in lookup_keys)
            for idx, (full_line, _) in enumerate(SUBMENUS[key]):
                if full_line == current_raw:
                    lb.SetSelection(idx)
                    self._last_selection[key] = idx
                    break

    # ------------------------------------------------------------------
    # Synthesis helpers
    # ------------------------------------------------------------------

    def _make_listbox_handler(self, param_key: str):
        def handler(evt):
            idx = evt.GetSelection()
            if idx == wx.NOT_FOUND or idx == self._last_selection.get(param_key):
                return
            self._last_selection[param_key] = idx
            full_line, _ = SUBMENUS[param_key][idx]
            key = get_leading_key(full_line)
            self._variant.set_line(key, full_line)
            self._schedule_synthesis()
        return handler

    def _schedule_synthesis(self):
        if self._synth_timer is not None:
            self._synth_timer.Stop()
        self._cancel_event.set()
        self._synth_timer = wx.CallLater(300, self._fire_synthesis)

    def _fire_synthesis(self):
        self._cancel_event.clear()
        phrase = self._phrase_ctrl.GetValue() or TEST_PHRASE
        cancel = self._cancel_event
        variant = self._variant
        voice = self._voice

        def run():
            err = synthesize_and_play(variant, voice, phrase, cancel)
            if not cancel.is_set():
                wx.CallAfter(self._on_synthesis_done, err)

        threading.Thread(target=run, daemon=True).start()

    def _on_synthesis_done(self, err):
        if err:
            self.SetStatusText(err)

    def _on_speak(self, evt):
        self._fire_synthesis()

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _on_save(self, evt):
        default = self._saved_file if self._saved_file else ""
        dlg = wx.FileDialog(
            self, message="Save voice as",
            defaultDir=str(VARIANTS_DIR),
            defaultFile=default,
            wildcard="All files (*.*)|*.*",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return
        dest = Path(dlg.GetPath())
        dlg.Destroy()
        self._variant.set_line("name", f"name {dest.name}")
        self._variant.save()
        try:
            shutil.copy2(self._variant.path, dest)
            self._saved_file = dest.name
            self.SetStatusText(f"Saved as '{dest.name}'.")
        except Exception as e:
            wx.MessageDialog(self, str(e), "Save failed", wx.OK | wx.ICON_ERROR).ShowModal()

    def _on_open(self, evt):
        dlg = wx.FileDialog(
            self, message="Open voice file",
            defaultDir=str(VARIANTS_DIR),
            wildcard="All files (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return
        path = Path(dlg.GetPath())
        dlg.Destroy()
        try:
            shutil.copy2(path, self._variant.path)
            self._variant.reload()
            self._preselect_all()
            self.SetStatusText(f"Opened '{path.name}'.")
            self._fire_synthesis()
        except Exception as e:
            wx.MessageDialog(self, str(e), "Open failed", wx.OK | wx.ICON_ERROR).ShowModal()

    def _on_install(self, evt):
        dlg = _InstallDialog(self, default_display=self._saved_display, default_file=self._saved_file)
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return
        display, file_name = dlg.get_values()
        dlg.Destroy()
        if not display or not file_name:
            return
        self._saved_display = display
        self._saved_file = file_name
        self._variant.set_line("name", f"name {display}")
        self._variant.save()
        dest = NVDA_VARIANTS / file_name
        if ctypes.windll.shell32.IsUserAnAdmin():
            try:
                shutil.copy2(self._variant.path, dest)
                self.SetStatusText(f"Installed as '{file_name}'. Restart NVDA to see it.")
            except Exception as e:
                wx.MessageDialog(self, str(e), "Install failed", wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            # Re-launch only the copy step elevated via UAC
            import tempfile, sys
            script = tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            )
            script.write(
                f"import shutil\n"
                f"shutil.copy2({str(self._variant.path)!r}, {str(dest)!r})\n"
            )
            script.close()
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script.name}"', None, 1
            )
            self.SetStatusText(f"Install requested. Restart NVDA to see '{display}'.")

    def _on_quit(self, evt):
        self.Close()

    def _on_close(self, evt):
        variant_path = self._variant.path
        if variant_path.exists():
            dlg = wx.MessageDialog(
                self,
                "Save progress so you can continue later?",
                "Quit Voice Lab",
                wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION,
            )
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_CANCEL:
                return  # don't close
            if result == wx.ID_YES:
                shutil.copy2(variant_path, IN_PROGRESS_FILE)
            variant_path.unlink(missing_ok=True)
        evt.Skip()  # allow the close


def main():
    global _current_voice

    synth, voice, source_variant = read_nvda_config()

    if synth != "espeak":
        app = wx.App()
        wx.MessageDialog(
            None,
            "NVDA is not currently using the eSpeak NG synthesizer.\n\n"
            "Open NVDA's Voice Settings, switch the synthesizer to eSpeak NG, "
            "then run Voice Lab again.",
            "Voice Lab",
            wx.OK | wx.ICON_INFORMATION,
        ).ShowModal()
        return

    _current_voice = voice
    variant_path = VARIANTS_DIR / VARIANT_NAME

    app = wx.App()

    has_session = IN_PROGRESS_FILE.exists()
    if has_session:
        shutil.copy2(IN_PROGRESS_FILE, variant_path)
    else:
        _seed_from_nvda(variant_path, voice, source_variant)

    variant = Variant(variant_path)
    frame = VoiceLabFrame(variant, voice, defer_init=has_session)

    if has_session:
        def _ask_resume():
            dlg = wx.MessageDialog(
                frame,
                "An in-progress session was found. Continue where you left off?",
                "Voice Lab",
                wx.YES_NO | wx.ICON_QUESTION,
            )
            if dlg.ShowModal() == wx.ID_YES:
                variant.reload()
                frame._preselect_all()
            else:
                IN_PROGRESS_FILE.unlink()
                _seed_from_nvda(variant_path, voice, source_variant)
                variant.reload()
                frame._preselect_all()
            dlg.Destroy()
            frame._fire_synthesis()

        wx.CallAfter(_ask_resume)

    app.MainLoop()


def _seed_from_nvda(variant_path: Path, voice: str, source_variant: str | None):
    if source_variant:
        nvda_source = NVDA_VARIANTS / source_variant
        local_source = VARIANTS_DIR / source_variant
        src = nvda_source if nvda_source.exists() else local_source
        shutil.copy2(src, variant_path)
    else:
        variant_path.write_text("language variant\nname _voicelab_temp\n", encoding="utf-8")


if __name__ == "__main__":
    main()
