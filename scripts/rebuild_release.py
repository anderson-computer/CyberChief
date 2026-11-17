#!/usr/bin/env python3
"""Rebuild CyberChief portable release artifacts.

Creates:
- issues/issue-06.html from CyberChief-Issue-6-The-Signal-from-Maytag.md
- pdfs/cyberchief-issue-06.pdf via Chrome headless when available
- dist/output/cyberchief-comic-email.zip
- dist/output/cyberchief-comic-full.zip
- dist/output/cyberchief-dvd.iso
"""
from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUT = DIST / "output"
STAGING = ROOT / "build" / "release-staging"
ISSUE6_MD = ROOT / "CyberChief-Issue-6-The-Signal-from-Maytag.md"
ISSUE6_HTML = ROOT / "issues" / "issue-06.html"
ISSUE6_PDF = ROOT / "pdfs" / "cyberchief-issue-06.pdf"


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(map(str, cmd)))
    return subprocess.run(cmd, text=True, check=True, **kwargs)


def convert_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def md_table_to_html(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [convert_inline(c.strip()) for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in line.strip().strip("|").split("|")):
            continue
        rows.append(cells)
    if not rows:
        return ""
    head, body = rows[0], rows[1:]
    out = ["<table class=\"tools-table\"><thead><tr>"]
    out.extend(f"<th>{c}</th>" for c in head)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def md_to_issue_html(md: str) -> str:
    body: list[str] = []
    lines = md.splitlines()
    i = 0
    in_ul = False
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            if in_ul:
                body.append("</ul>")
                in_ul = False
            i += 1
            continue
        if line.strip() == "---":
            if in_ul:
                body.append("</ul>")
                in_ul = False
            body.append("<hr class=\"universe-divider\">")
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and lines[i + 1].startswith("|"):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            body.append(md_table_to_html(table_lines))
            continue
        if line.startswith("# "):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            title = convert_inline(line[2:].strip())
            body.append(f"<section class=\"chapter\"><div class=\"chapter-header\"><div class=\"chapter-title\">{title}</div></div>")
            i += 1
            continue
        if line.startswith("## "):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            body.append(f"<h2>{convert_inline(line[3:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("### "):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            body.append(f"<h3>{convert_inline(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.startswith(">"):
            if in_ul:
                body.append("</ul>")
                in_ul = False
            q = line.lstrip("> ").strip()
            cls = "narration"
            upper = q.upper()
            if upper.startswith("CYBERCHIEF:"):
                cls = "lrn"
            elif "GREEN TECH BOX" in upper:
                cls = "tech"
            body.append(f"<div class=\"bubble {cls}\">{convert_inline(q)}</div>")
            i += 1
            continue
        if line.startswith("- "):
            if not in_ul:
                body.append("<ul class=\"issue-list\">")
                in_ul = True
            body.append(f"<li>{convert_inline(line[2:].strip())}</li>")
            i += 1
            continue
        if in_ul:
            body.append("</ul>")
            in_ul = False
        body.append(f"<p>{convert_inline(line)}</p>")
        i += 1
    if in_ul:
        body.append("</ul>")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CyberChief #6 — The Signal from Maytag | Mike Anderson</title>
<link rel="stylesheet" href="comic.css">
<style>
.issue-list {{ margin: 1rem 2rem; line-height: 1.7; }}
.issue-list li {{ margin-bottom: .35rem; }}
.chapter > p, .chapter h2, .chapter h3 {{ max-width: 900px; margin: 1rem auto; padding: 0 24px; line-height: 1.65; }}
.chapter h2, .chapter h3 {{ color: var(--caption-yellow); font-family: 'Bangers', Impact, fantasy; letter-spacing: 2px; }}
</style>
</head>
<body>
<nav class="issue-nav">
  <a href="issue-05.html">◀ ISSUE #5</a>
  <span>ISSUE #6 — THE SIGNAL FROM MAYTAG</span>
  <a href="index.html">ALL ISSUES ▶</a>
</nav>
<div class="cover-spread" style="padding:48px 24px;text-align:center;background:radial-gradient(circle at 50% 20%,#113a7a,#080810 65%);">
  <img src="../art/CyberChief Logo.png" alt="CyberChief Logo" style="max-width:300px;filter:drop-shadow(0 0 24px rgba(77,195,255,.7));">
  <div style="font-family:'Bangers',Impact,fantasy;font-size:3rem;letter-spacing:6px;color:var(--caption-yellow);margin-top:24px;">THE SIGNAL FROM MAYTAG</div>
  <div style="font-family:'Bangers',Impact,fantasy;font-size:1.4rem;letter-spacing:3px;color:var(--blue-glow);">CONTAINERS OF CHAOS</div>
  <div style="margin-top:18px;color:#aab;">Issue #6 · Cloud &amp; Container Security · 10 New Tools · 65 Total</div>
</div>
{''.join(body)}
<nav class="issue-nav bottom-nav">
  <a href="issue-05.html">◀ ISSUE #5</a>
  <a href="index.html">ALL ISSUES</a>
</nav>
</body>
</html>
"""


def generate_issue6() -> None:
    ISSUE6_HTML.write_text(md_to_issue_html(ISSUE6_MD.read_text()), encoding="utf-8")
    print(f"wrote {ISSUE6_HTML}")


def chrome_pdf() -> None:
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("WARNING: no Chrome/Chromium found; skipping issue 6 PDF")
        return
    ISSUE6_PDF.parent.mkdir(exist_ok=True)
    url = ISSUE6_HTML.resolve().as_uri()
    run([
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--allow-file-access-from-files",
        f"--print-to-pdf={ISSUE6_PDF}",
        url,
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"wrote {ISSUE6_PDF} ({ISSUE6_PDF.stat().st_size} bytes)")


def copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.html~"))


def stage_release() -> None:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    copytree(ROOT / "issues", STAGING / "issues")
    copytree(ROOT / "art", STAGING / "art")
    copytree(ROOT / "pdfs", STAGING / "pdfs")
    copytree(DIST / "Windows", STAGING / "Windows")
    copytree(DIST / "Linux", STAGING / "Linux")
    for name in ["README.txt", "autorun.inf", "LAUNCH.bat", "launch.sh", "cyberchief-cd-label.html"]:
        src = DIST / name
        if src.exists():
            shutil.copy2(src, STAGING / name)
    # keep launch.sh executable in staged output
    for rel in ["launch.sh", "Linux/launch-cyberchief.sh", "Linux/install-cyberchief.sh"]:
        p = STAGING / rel
        if p.exists():
            p.chmod(p.stat().st_mode | 0o111)
    print(f"staged release at {STAGING}")


def make_zip(zip_path: Path, include_pdfs: bool) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(STAGING.rglob("*")):
            rel = p.relative_to(STAGING)
            if not include_pdfs and (rel.parts and rel.parts[0] == "pdfs"):
                continue
            if p.is_file():
                z.write(p, rel.as_posix())
    print(f"wrote {zip_path} ({zip_path.stat().st_size} bytes)")


def make_iso() -> None:
    iso = OUT / "cyberchief-dvd.iso"
    if iso.exists():
        iso.unlink()
    cmd = [
        "genisoimage",
        "-quiet",
        "-J",
        "-r",
        "-V",
        "CYBERCHIEF",
        "-o",
        str(iso),
        str(STAGING),
    ]
    run(cmd)
    print(f"wrote {iso} ({iso.stat().st_size} bytes)")


def main() -> int:
    os.chdir(ROOT)
    generate_issue6()
    chrome_pdf()
    stage_release()
    make_zip(OUT / "cyberchief-comic-email.zip", include_pdfs=False)
    make_zip(OUT / "cyberchief-comic-full.zip", include_pdfs=True)
    make_iso()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
