# LRN Man Episode 1 Web Player

Local browser player for the rebuilt Episode 1 animatic.

Files
- `index.html` — self-contained player page
- `start.sh` — launches a loopback-only static server on port 9130

URL
- http://127.0.0.1:9130/

Features
- Embedded HTML5 video player for the final MP4
- Download links for the MP4, subtitles, poster, and thumbnail
- Live scene manifest loaded from `../output/scene_manifest.json`
- Local repo-relative asset paths only; no remote dependencies

Run
- `./start.sh`

Notes
- This is a local utility page, intended for review on this machine.
- The page references artifacts from `../output/` and `../release/`, so keep the current episode-build directory structure intact.
