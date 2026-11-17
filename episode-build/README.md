# CyberChief Episode Build Workspace

This directory is an experimental video/animatic workstream for CyberChief Episode 1. It is intentionally separated from the main portable comic release.

Tracked source/control files:

- `generate_episode1_animatic.py` — local animatic generator
- `narration_episode1.txt` — narration source text
- `web/` — loopback-only review player
- `null-protocol-package/` — prompts, continuity checklist, scene plan, and asset manifest
- `release/README.md` — release notes for generated episode artifacts

Ignored generated artifacts:

- `output/`
- `assets/`
- generated poster/thumbnail/subtitle artifacts under `release/`

Run the local review player:

```bash
cd episode-build/web
./start.sh
# open http://127.0.0.1:9130/
```

The web player expects generated assets to exist locally under `episode-build/output/` and `episode-build/release/`.
