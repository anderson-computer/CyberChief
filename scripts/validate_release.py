#!/usr/bin/env python3
"""Static QA checks for CyberChief release content."""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "issues/index.html",
    "issues/issue-01.html",
    "issues/issue-02.html",
    "issues/issue-03.html",
    "issues/issue-04.html",
    "issues/issue-05.html",
    "issues/issue-06.html",
    "issues/comic.css",
    "dist/Windows/Launch-CyberChief.bat",
    "dist/Windows/Install-CyberChief.bat",
    "dist/Linux/launch-cyberchief.sh",
    "dist/Linux/install-cyberchief.sh",
    "dist/README.txt",
    "dist/output/cyberchief-comic-email.zip",
    "dist/output/cyberchief-comic-full.zip",
    "dist/output/cyberchief-dvd.iso",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def check_required() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def check_html_refs() -> None:
    broken = []
    for p in list((ROOT / "issues").glob("*.html")) + list((ROOT / "dist").glob("*.html")):
        s = p.read_text(errors="replace")
        for url in re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", s):
            if url.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            path = url.split("#")[0].split("?")[0]
            if not path:
                continue
            target = (p.parent / path).resolve()
            if not target.exists():
                broken.append(f"{p.relative_to(ROOT)} -> {url}")
    if broken:
        fail("broken HTML references:\n" + "\n".join(broken))


def check_index() -> None:
    idx = (ROOT / "issues/index.html").read_text(errors="replace")
    for n in range(1, 7):
        if f"issue-{n:02d}.html" not in idx:
            fail(f"index missing issue-{n:02d}.html")
    if "</h1>THE BLIZZARD" in idx:
        fail("index has malformed header tag")


def check_release_zips() -> None:
    expected = ["issues/index.html", "issues/issue-06.html", "Windows/Launch-CyberChief.bat", "Linux/launch-cyberchief.sh", "README.txt"]
    for name in ["cyberchief-comic-email.zip", "cyberchief-comic-full.zip"]:
        zp = ROOT / "dist" / "output" / name
        if not zipfile.is_zipfile(zp):
            fail(f"{name} is not a valid zip")
        with zipfile.ZipFile(zp) as z:
            names = set(z.namelist())
            missing = [e for e in expected if e not in names]
            if missing:
                fail(f"{name} missing {missing}")
            if name.endswith("full.zip") and "pdfs/cyberchief-issue-06.pdf" not in names:
                fail("full zip missing issue 6 PDF")


def check_lfs_pointer_artifacts() -> None:
    suspect = []
    for p in list((ROOT / "pdfs").glob("*.pdf")) + list((ROOT / "dist/output").glob("*.zip")) + list((ROOT / "dist/output").glob("*.iso")):
        head = p.read_bytes()[:80]
        if head.startswith(b"version https://git-lfs.github.com/spec"):
            suspect.append(str(p.relative_to(ROOT)))
    if suspect:
        fail("Git LFS pointer files remain instead of real artifacts: " + ", ".join(suspect))


def main() -> int:
    check_required()
    check_lfs_pointer_artifacts()
    check_html_refs()
    check_index()
    check_release_zips()
    print("CyberChief release validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
