#!/usr/bin/env python3
"""
RAFTcorr Demo Video Builder v2
Combines segmented screen recordings into a polished demo video.

Changes from v1:
- Much larger fonts on title/transition cards
- Per-step speed adjustments (2x/3x)
- Magnifier overlay on processing steps (bottom-left zoom-in)

Output: assets/videos/raftcorr_demo.mp4 (1920x1080 @30fps)
"""

import subprocess
import os
import re
import shutil
import sys

# ─── Configuration ────────────────────────────────────────────────────────────

FFMPEG = (
    r"C:\Users\13014\anaconda3\Lib\site-packages"
    r"\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_DIR = os.path.join(BASE_DIR, "assets", "videos", "Demo")
OUTPUT = os.path.join(BASE_DIR, "assets", "videos", "raftcorr_demo.mp4")
TEMP_DIR = os.path.join(DEMO_DIR, "_temp")

W, H, FPS = 1920, 1080, 30

# Font paths escaped for ffmpeg drawtext (colons need \\:)
FONT = "C\\\\:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C\\\\:/Windows/Fonts/segoeuib.ttf"

# Theme colors (match website dark sci-fi theme)
BG = "0x0A0A0F"
ACCENT = "0x00D4FF"

# Timing
TITLE_DURATION = 2.0
STEP_TITLE_DURATION = 2.0
END_DURATION = 3.5
FADE = 0.4

# Magnifier: crop bottom-left sidebar (status/progress area), zoom & overlay
MAG_CROP_W = 576           # crop width (covers sidebar + bit of image)
MAG_CROP_H = 324           # crop height (bottom portion: status/progress/buttons)
MAG_ZOOM = 1.5             # enlargement factor
MAG_W = int(MAG_CROP_W * MAG_ZOOM)   # 864 display width
MAG_H = int(MAG_CROP_H * MAG_ZOOM)   # 486 display height
MAG_BORDER = 3             # border thickness (accent color)
MAG_MARGIN = 16            # margin from edges
MAG_Y_OFFSET = 56          # below the 48px top bar + gap

# Workflow steps
STEPS = [
    {"file": "selection_image_folder.mp4", "step": 1,
     "title": "Load Image Sequence",      "speed": 2, "magnifier": False},
    {"file": "draw_ROI.mp4",               "step": 2,
     "title": "Draw Region of Interest",   "speed": 2, "magnifier": False},
    {"file": "processing.mp4",             "step": 3,
     "title": "Compute Displacement Field","speed": 3, "magnifier": True},
    {"file": "preview_displacement.mp4",   "step": 4,
     "title": "Displacement Results",      "speed": 2, "magnifier": False},
    {"file": "preview_strain.mp4",         "step": 5,
     "title": "Strain Results",            "speed": 1, "magnifier": False},
]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def run_ff(args, desc=""):
    """Run ffmpeg with -y (overwrite) and given arguments."""
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "warning"] + args
    print(f"  -> {desc}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[-800:]}")
        sys.exit(1)


def get_duration(path):
    """Probe video duration in seconds."""
    result = subprocess.run(
        [FFMPEG, "-i", path], capture_output=True, text=True
    )
    match = re.search(r"Duration: (\d+):(\d+):([\d.]+)", result.stderr)
    if match:
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 10.0


def esc(text):
    """Escape text for ffmpeg drawtext filter."""
    return text.replace(":", "\\\\:").replace("'", "'\\''")


# ─── Video generators ────────────────────────────────────────────────────────

def make_text_card(output_path, duration, lines, desc="card"):
    """Generate a dark-background card with centered text lines."""
    vf_parts = []
    for line in lines:
        t = esc(line["text"])
        vf_parts.append(
            f"drawtext=text='{t}'"
            f":fontfile={line['font']}"
            f":fontsize={line['size']}"
            f":fontcolor={line['color']}"
            f":x=(w-text_w)/2"
            f":y={line['y']}"
        )
    vf_parts.append(f"fade=t=in:st=0:d={FADE}")
    vf_parts.append(f"fade=t=out:st={duration - FADE}:d={FADE}")
    vf = ",".join(vf_parts)

    run_ff([
        "-f", "lavfi", "-i", f"color=c={BG}:s={W}x{H}:d={duration}:r={FPS}",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path,
    ], desc=desc)


def _base_scale_filter(speed):
    """Return the common scale/pad/fps filter chain with speed adjustment."""
    return (
        f"setpts=PTS/{speed},"
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color={BG},"
        f"fps={FPS}"
    )


def _label_filter(label):
    """Return the top-bar + step label drawtext filter chain."""
    return (
        f"drawbox=x=0:y=0:w={W}:h=48:color=black@0.55:t=fill,"
        f"drawbox=x=0:y=48:w={W}:h=2:color={ACCENT}@0.4:t=fill,"
        f"drawtext=text='{label}'"
        f":fontfile={FONT_BOLD}:fontsize=22"
        f":fontcolor=white@0.9:x=16:y=13"
    )


def _fade_filter(dur):
    """Return fade in/out filter string."""
    return (
        f"fade=t=in:st=0:d={FADE},"
        f"fade=t=out:st={max(dur - FADE, FADE + 0.1)}:d={FADE}"
    )


def process_clip(input_path, output_path, step_num, step_title,
                 speed=1, magnifier=False):
    """Process a clip: speed change, normalize, overlay, optional magnifier."""
    orig_dur = get_duration(input_path)
    new_dur = orig_dur / speed

    label = esc(f"Step {step_num}  |  {step_title}")
    base = _base_scale_filter(speed)
    lbl = _label_filter(label)
    fades = _fade_filter(new_dur)
    desc_suffix = f"({speed}x" + (" + magnifier)" if magnifier else ")")

    if magnifier:
        # Use complex filtergraph: split -> crop/zoom -> overlay
        mag_x = W - MAG_W - MAG_MARGIN       # right-aligned
        mag_y = MAG_Y_OFFSET                  # below top bar
        crop_y = H - MAG_CROP_H               # bottom edge of frame

        fc = (
            # Split the processed base video into two streams
            f"[0:v]{base},split[main][forcrop];"
            # Crop bottom-left, zoom in, add accent border
            f"[forcrop]"
            f"crop={MAG_CROP_W}:{MAG_CROP_H}:0:ih-{MAG_CROP_H},"
            f"scale={MAG_W}:{MAG_H},"
            f"drawbox=0:0:iw-1:ih-1:color={ACCENT}@0.8:t={MAG_BORDER}"
            f"[mag];"
            # Overlay magnifier on main, add highlight box + labels + fades
            f"[main][mag]overlay={mag_x}:{mag_y},"
            # Highlight rectangle on bottom-left (shows what is magnified)
            f"drawbox=x=0:y={crop_y}:w={MAG_CROP_W}:h={MAG_CROP_H}"
            f":color={ACCENT}@0.4:t=2,"
            f"{lbl},{fades}[outv]"
        )

        run_ff([
            "-i", input_path,
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-filter_complex", fc,
            "-map", "[outv]", "-map", "1:a",
            "-t", str(new_dur),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            output_path,
        ], desc=f"Step {step_num}: {step_title} {desc_suffix}")

    else:
        # Simple single-stream filter
        vf = f"{base},{lbl},{fades}"

        run_ff([
            "-i", input_path,
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(new_dur),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            output_path,
        ], desc=f"Step {step_num}: {step_title} {desc_suffix}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("RAFTcorr Demo Video Builder v2")
    print("=" * 50)

    os.makedirs(TEMP_DIR, exist_ok=True)
    segments = []

    # ── 1. Title Card (large fonts) ──────────────────────────────────────────
    print("\n[1/3] Creating title & end cards...")
    title_path = os.path.join(TEMP_DIR, "00_title.mp4")
    make_text_card(title_path, TITLE_DURATION, [
        {"text": "RAFTcorr",
         "font": FONT_BOLD, "size": 120, "color": ACCENT,
         "y": "(h/2)-110"},
        {"text": "Deep Learning Digital Image Correlation",
         "font": FONT, "size": 48, "color": "white",
         "y": "(h/2)+10"},
        {"text": "Software Demonstration",
         "font": FONT, "size": 36, "color": "0x888888",
         "y": "(h/2)+80"},
    ], desc="Title card")
    segments.append(title_path)

    # ── 2. Step segments ─────────────────────────────────────────────────────
    print("\n[2/3] Processing step clips...")
    for step in STEPS:
        idx = step["step"]

        # Step title slide (large fonts)
        st_path = os.path.join(TEMP_DIR, f"{idx:02d}a_title.mp4")
        make_text_card(st_path, STEP_TITLE_DURATION, [
            {"text": f"Step {idx}",
             "font": FONT_BOLD, "size": 96, "color": ACCENT,
             "y": "(h/2)-60"},
            {"text": step["title"],
             "font": FONT, "size": 44, "color": "white",
             "y": "(h/2)+50"},
        ], desc=f"Step {idx} title card")
        segments.append(st_path)

        # Processed clip (speed + optional magnifier)
        clip_in = os.path.join(DEMO_DIR, step["file"])
        clip_out = os.path.join(TEMP_DIR, f"{idx:02d}b_clip.mp4")
        process_clip(
            clip_in, clip_out, idx, step["title"],
            speed=step["speed"], magnifier=step["magnifier"],
        )
        segments.append(clip_out)

    # ── 3. End Card (large fonts) ────────────────────────────────────────────
    end_path = os.path.join(TEMP_DIR, "99_end.mp4")
    make_text_card(end_path, END_DURATION, [
        {"text": "Try RAFTcorr Today",
         "font": FONT_BOLD, "size": 96, "color": ACCENT,
         "y": "(h/2)-70"},
        {"text": "github.com/zachtong/RAFTcorr",
         "font": FONT, "size": 40, "color": "white",
         "y": "(h/2)+30"},
        {"text": "Free & Open Source",
         "font": FONT, "size": 32, "color": "0x888888",
         "y": "(h/2)+90"},
    ], desc="End card")
    segments.append(end_path)

    # ── 4. Concatenate ───────────────────────────────────────────────────────
    print("\n[3/3] Concatenating final video...")
    concat_list = os.path.join(TEMP_DIR, "concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in segments:
            safe_path = seg.replace("\\", "/")
            f.write(f"file '{safe_path}'\n")

    run_ff([
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        OUTPUT,
    ], desc="Final concat")

    # ── 5. Cleanup ───────────────────────────────────────────────────────────
    shutil.rmtree(TEMP_DIR)

    size_mb = os.path.getsize(OUTPUT) / (1024 * 1024)
    dur = get_duration(OUTPUT)

    print(f"\n{'=' * 50}")
    print(f"  Done!  {OUTPUT}")
    print(f"  Duration: {dur:.1f}s  |  Size: {size_mb:.1f} MB")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
