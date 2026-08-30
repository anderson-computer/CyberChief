#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess

BASE = Path('/home/mike/dev/LRN-Man')
BUILD = BASE / 'episode-build'
OUT = BUILD / 'output'
CLIPS = OUT / 'clips'
for d in (OUT, CLIPS):
    d.mkdir(parents=True, exist_ok=True)

NARRATION_CANDIDATES = [
    OUT / 'lrn-episode1-narration.wav',
    OUT / 'lrn-episode1-narration.mp3',
]
NARRATION = next((p for p in NARRATION_CANDIDATES if p.exists()), None)
FINAL = OUT / 'lrn-man-episode1-animatic.mp4'
PREMUX = OUT / 'lrn-man-episode1-animatic-premux.mp4'
SRT = OUT / 'lrn-man-episode1-animatic.srt'
ASS = OUT / 'lrn-man-episode1-animatic.ass'
MANIFEST = OUT / 'scene_manifest.json'

scenes = [
    {'kind': 'intro', 'image': str(BASE / 'art/LRN Man Logo=blk background.png'), 'duration': 5.0, 'label': 'LRN MAN: DEFENDER OF THE NETWORK', 'sub': 'Episode 1 — The Last Son of Maytag'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202415.png'), 'duration': 7.5, 'label': 'PLANET MAYTAG — THE COUNCIL OF ROOT ADMINS', 'sub': 'A perfect digital civilization sees Earth standing exposed.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202411.png'), 'duration': 7.5, 'label': 'THE LAST DEPARTURE', 'sub': 'LRN accepts the mission and launches from Maytag.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202146.png'), 'duration': 7.5, 'label': 'FIRST BOOT COMPLETE', 'sub': 'LRN Man arrives on Earth and begins his scan.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202348.png'), 'duration': 7.5, 'label': 'THREATS DETECTED', 'sub': 'He finds a planet drowning in exposed systems and weak defenses.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202656.png'), 'duration': 7.5, 'label': 'THE MISSION BEGINS', 'sub': 'Earth becomes the site of the greatest infrastructure project in history.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202352.png'), 'duration': 7.5, 'label': 'IDENTITY AND TRUST', 'sub': 'FreeIPA, Kerberos, LDAP, and SSSD form the network backbone.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202356.png'), 'duration': 7.5, 'label': 'ENCRYPTION LAYERS ACTIVE', 'sub': 'DogTag, TLS, and AIDE seal the foundation with cryptographic proof.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202401.png'), 'duration': 7.5, 'label': 'THE WATCHTOWERS RISE', 'sub': 'SELinux, Splunk, Wazuh, and CyberArk give the fortress eyes.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202422.png'), 'duration': 7.5, 'label': 'AUTOMATION ONLINE', 'sub': 'GitLab, CMMD, and SBAI turn security into a living system.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202425.png'), 'duration': 7.5, 'label': 'THE SHADOW SYNDICATE MOBILIZES', 'sub': 'The Zero-Day King gathers every attack vector for one massive strike.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202418.png'), 'duration': 7.5, 'label': 'COUNTERATTACK', 'sub': 'DDoS traffic is scrubbed. Zero-days are contained. Keys are rotated.'},
    {'kind': 'scene', 'image': str(BASE / 'art/lrn-man_20260328_202352.png'), 'duration': 7.5, 'label': 'THE NETWORK STANDS', 'sub': 'Honeypots bloom and command channels collapse across the battlefield.'},
    {'kind': 'outro', 'image': str(BASE / 'art/LRN Man.png'), 'duration': 6.0, 'label': 'HE IS LRN MAN', 'sub': 'This is his network. And he defends it.'},
]


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=nk=1:nw=1', str(path)
    ], text=True).strip()
    return float(out)


if NARRATION is not None:
    audio_duration = ffprobe_duration(NARRATION)
    base_total = sum(s['duration'] for s in scenes)
    scale = audio_duration / base_total
    for s in scenes:
        s['duration'] = round(s['duration'] * scale, 3)

manifest = []
start = 0.0
for idx, s in enumerate(scenes, 1):
    entry = dict(s)
    entry['index'] = idx
    entry['start'] = round(start, 3)
    entry['end'] = round(start + entry['duration'], 3)
    manifest.append(entry)
    start += entry['duration']
MANIFEST.write_text(json.dumps(manifest, indent=2), encoding='utf-8')


def fmt_srt(sec: float) -> str:
    ms = int(round(sec * 1000))
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def fmt_ass(sec: float) -> str:
    cs = int(round(sec * 100))
    h = cs // 360000
    cs %= 360000
    m = cs // 6000
    cs %= 6000
    s = cs // 100
    cs %= 100
    return f'{h}:{m:02d}:{s:02d}.{cs:02d}'


srt_blocks = []
ass_lines = [
    '[Script Info]',
    'ScriptType: v4.00+',
    'PlayResX: 1920',
    'PlayResY: 1080',
    'ScaledBorderAndShadow: yes',
    '',
    '[V4+ Styles]',
    'Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding',
    'Style: Title,DejaVu Sans,28,&H00FFD77F,&H000000FF,&H00081424,&H64000000,1,0,0,0,100,100,0,0,1,2.2,0.6,8,90,90,55,1',
    'Style: Subtitle,DejaVu Sans,22,&H00FFFFFF,&H000000FF,&H00081424,&H78000000,0,0,0,0,100,100,0,0,1,2.0,0.5,2,120,120,58,1',
    '',
    '[Events]',
    'Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text',
]

for s in manifest:
    top = s['label']
    bottom = s['sub'] if s['kind'] != 'intro' else 'Episode 1 — The Last Son of Maytag'
    srt_blocks.append(f"{s['index']}\n{fmt_srt(s['start'])} --> {fmt_srt(s['end'])}\n{top}\\N{bottom}\n")
    ass_lines.append(f"Dialogue: 0,{fmt_ass(s['start'])},{fmt_ass(s['end'])},Title,,0,0,0,,{top}")
    ass_lines.append(f"Dialogue: 1,{fmt_ass(s['start'])},{fmt_ass(s['end'])},Subtitle,,0,0,0,,{bottom}")

SRT.write_text('\n'.join(srt_blocks), encoding='utf-8')
ASS.write_text('\n'.join(ass_lines) + '\n', encoding='utf-8')

clip_paths = []
for s in manifest:
    clip = CLIPS / f"scene_{s['index']:02d}.mp4"
    clip_paths.append(clip)
    dur = s['duration']
    fade_out = max(0.1, dur - 0.45)
    filtergraph = (
        '[0:v]split=2[bg][fg];'
        '[bg]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=18:2[bg2];'
        '[fg]scale=1920:1080:force_original_aspect_ratio=decrease[fg2];'
        '[bg2][fg2]overlay=(W-w)/2:(H-h)/2,'
        'drawbox=x=60:y=70:w=1800:h=96:color=0x081020@0.45:t=fill,'
        'drawbox=x=60:y=880:w=1800:h=116:color=0x081020@0.55:t=fill,'
        f'fade=t=in:st=0:d=0.45,fade=t=out:st={fade_out}:d=0.45,format=yuv420p[v]'
    )
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', s['image'], '-t', str(dur),
        '-filter_complex', filtergraph,
        '-map', '[v]', '-r', '30', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', str(clip)
    ]
    subprocess.run(cmd, check=True)

concat_list = OUT / 'concat_list.txt'
concat_list.write_text(''.join([f"file '{p}'\n" for p in clip_paths]), encoding='utf-8')

if NARRATION is not None:
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat_list), '-i', str(NARRATION),
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', str(PREMUX)
    ]
else:
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat_list), '-c', 'copy', str(PREMUX)
    ]
subprocess.run(cmd, check=True)

subprocess.run([
    'ffmpeg', '-y', '-i', str(PREMUX), '-vf', f'ass={ASS}',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-c:a', 'copy', str(FINAL)
], check=True)

print(FINAL)
print(SRT)
print(ASS)
print(MANIFEST)
