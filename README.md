# Eve

Eve is a Windows tool for tuning eSpeak NG voice settings and hearing the results instantly through NVDA. You adjust parameters like pitch, breathiness, and roughness, and Eve plays the new voice immediately so you can decide whether you like it. When you find a voice you want to keep, Eve saves it and can install it directly into NVDA.

Eve is Windows-only. It requires NVDA and eSpeak NG.

---

## What you need before installing

- Windows 10 or 11
- NVDA, with eSpeak NG set as your synthesizer in NVDA's Voice Settings
- eSpeak NG installed at its default location. Download the `.msi` installer for Windows from the [eSpeak NG releases page](https://github.com/espeak-ng/espeak-ng/releases) and run it, accepting the default install location.
- Python 3.11 or later. Download it from [python.org](https://www.python.org/downloads/). During install, check the box that says **Add Python to PATH**.

---

## How to install

Do these steps once, the first time you set up Eve.

1. Download Eve. Go to the [Eve releases page](https://github.com/jhomme/Eve/releases) and click the **Source code (zip)** link under the latest release. Save the zip file somewhere you can find it, then unzip it. You will get a folder called `Eve-0.1.0` or similar. You can move that folder wherever you like.

2. Open Command Prompt. Press the Windows key, type `cmd`, and press Enter.

3. Go to the Eve folder. Type the command below, replacing the path with wherever you put the Eve folder on your computer:

   ```
   cd C:\path\to\Eve
   ```

4. Create a virtual environment. This is a private copy of Python used only by Eve, so it does not affect anything else on your computer:

   ```
   python -m venv .venv
   ```

5. Install the required library:

   ```
   .venv\Scripts\pip install -r requirements.txt
   ```

6. Run Eve:

   ```
   .venv\Scripts\python voice_lab.py
   ```

---

## How to run Eve after the first install

Open Command Prompt, go to the Eve folder, and run:

```
.venv\Scripts\python voice_lab.py
```

---

## Feedback and bug reports

If something does not work, or you have a suggestion, please open an issue on GitHub.

Go to the [Eve issues page](https://github.com/jhomme/Eve/issues) and click **New issue**. Give it a short title describing the problem, then describe what happened and what you expected to happen. Click **Submit new issue** when you are done.

If you have never filed a GitHub issue before, GitHub has a short guide: [Creating an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue).

---

## Credits

The code was written by Claude (Anthropic's AI) and tested by Jim Homme.

---

## License

MIT — see [LICENSE](LICENSE).
