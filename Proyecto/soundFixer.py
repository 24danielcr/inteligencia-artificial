import os
import subprocess
from pathlib import Path
from shutil import copy2

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

# Configuration
BITRATE = "192k"
CHANNELS = "2"
SAMPLE_RATE = "44100"
NORMALISE = "loudnorm"  # Options: "loudnorm", "peak_simple", "peak_exact"

# Destination MP3 file extension
OUTPUT_EXT = ".mp3"

def ffmpeg_audio_stream_exists(path):
    cmd = [
        FFPROBE, "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=codec_type",
        "-of", "csv=p=0",
        str(path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return "audio" in result.stdout.lower()

def detect_peak_gain(path):
    """Return gain needed to bring max_volume to ~-1 dBFS"""
    proc = subprocess.run(
        [FFMPEG, "-i", path, "-af", "volumedetect", "-f", "null", "NUL"],
        stderr=subprocess.PIPE, text=True
    )
    for line in proc.stderr.splitlines():
        if "max_volume" in line:
            max_db = float(line.split(":")[1].strip().split()[0])
            return -(max_db + 1.0)
    return 0.0

def convert_to_mp3(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)

    if NORMALISE == "loudnorm":
        af_filter = (
            "loudnorm=I=-16:LRA=11:TP=-1.5:"
            "measured_I=-16:measured_LRA=0:"
            "measured_TP=-2:measured_thresh=-26:offset=0"
        )
    elif NORMALISE == "peak_simple":
        af_filter = "dynaudnorm=p=1:m=100:f=150"
    elif NORMALISE == "peak_exact":
        gain = detect_peak_gain(src)
        af_filter = f"volume={gain}dB"
    else:
        af_filter = None

    cmd = [
        FFMPEG, "-y", "-i", str(src),
        "-vn",
    ]
    if af_filter:
        cmd += ["-af", af_filter]
    cmd += [
        "-ar", SAMPLE_RATE,
        "-ac", CHANNELS,
        "-b:a", BITRATE,
        str(dst)
    ]

    print(f"Converting: {src} → {dst.name}")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def batch_convert(src_root, dst_root):
    for root, _, files in os.walk(src_root):
        for file in files:
            src_path = Path(root) / file
            rel_path = src_path.relative_to(src_root)
            dst_path = Path(dst_root) / rel_path.with_suffix(OUTPUT_EXT)

            try:
                if ffmpeg_audio_stream_exists(src_path):
                    convert_to_mp3(src_path, dst_path)
                else:
                    print(f"Skipped (no audio stream): {src_path}")
            except Exception as e:
                print(f"Error processing {src_path}: {e}")

if __name__ == "__main__":
    # Change these paths to your actual folders
    src_root = r"..\Sounds\Strident"
    dst_root = r"..\SoundsUpdated\Strident"

    batch_convert(src_root, dst_root)
