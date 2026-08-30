# LRN-Man

The LRN Man Universe — comics, lore, assets, printable/downloadable releases, and animated short experiments.

## Current release status

The portable comic release currently contains:

- HTML reader for Issues #1-6 under `issues/`
- Shared artwork under `art/`
- PDF exports under `pdfs/`
- Windows launcher and installer under `dist/Windows/`
- Linux launcher and installer under `dist/Linux/`
- Browser/direct-open support on Windows, Linux, and macOS through `issues/index.html`
- Rebuilt ZIP and ISO artifacts under `dist/output/`

## Quick start from the repo

```bash
# Open directly in a browser on any desktop OS
xdg-open issues/index.html

# Linux portable launcher
bash dist/Linux/launch-lrn-man.sh

# Windows portable launcher
# Double-click: dist\Windows\Launch-LRN-Man.bat
```

## Rebuild release artifacts

```bash
python3 scripts/rebuild_release.py
python3 scripts/validate_release.py
```

The rebuild script regenerates Issue #6 HTML/PDF and rebuilds the portable email ZIP, full ZIP, and DVD-style ISO.

## Episode build workspace

`episode-build/` is an experimental local workspace for the Episode 1 animatic/web player. It is intentionally not part of the main portable comic release yet. Treat it as a separate workstream until the video workflow is ready for packaging.
