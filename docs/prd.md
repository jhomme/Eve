# PRD: Voice Lab

## What we are building

Voice Lab is a Windows desktop tool for tuning eSpeak NG voice variant files and hearing each change through NVDA in real time. It presents a menu of tunable parameters (klatt model, voicing, flutter, roughness, pitch range, consonants, formants 1-4), lets the user pick preset values, and plays each result immediately so they can hear it before committing.

## Who it is for

Jim (the developer and sole user). Jim is blind, uses NVDA with the eSpeak NG synthesizer, and wants a keyboard-only way to craft a custom voice without hand-editing variant files.

## Why we are building it

NVDA's eSpeak NG variant files use an undocumented numeric format. There is no accessible GUI for experimenting with parameters. Voice Lab removes the trial-and-error of editing files by hand and restarting NVDA.

## Key constraints

- Must run on Windows with NVDA running.
- All interaction must be keyboard-only and NVDA-accessible.
- Changes are non-destructive: work on a temp copy, never touch the user's live NVDA voice files.
- Install step copies the finished variant into NVDA's voice data folder (requires admin rights for that step only).
- The app is a single Python script; no server, no web UI.

## Out of scope

- Non-Windows platforms.
- Synthesizers other than eSpeak NG.
- Automated voice optimization or machine-learning tuning.
