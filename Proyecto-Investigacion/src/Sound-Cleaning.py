import os, random, subprocess, json
from pathlib import Path

import librosa
import numpy as np

# ----------------------------------------------------------------------------------
#                             CONFIGURATION
# ----------------------------------------------------------------------------------
SR = 22_050
CLIP_LEN_S = 8
N_MELS = 128
HOP_LENGTH = 512
CLIP_SAMPLES = SR * CLIP_LEN_S

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
BITRATE = "192k"
CHANNELS = "2"
SAMPLE_RATE = "44100"
NORMALISE = "loudnorm" # "loudnorm" | "peak_simple" | "peak_exact"
OUTPUT_EXT = ".mp3"

SPLIT_FRACTIONS = dict(train=0.8, val=0.1, test=0.1)  # must sum to 1.0

RND_SEED = 42

# ----------------------------------------------------------------------------------
#                          UTILITY FUNCTIONS
# ----------------------------------------------------------------------------------

def ffmpeg_audio_stream_exists(path: Path) -> bool:
    """Return True if at least one audio stream is present."""
    cmd = [FFPROBE, "-v", "error", "-select_streams", "a",
           "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)]
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return "audio" in r.stdout.lower()


def detect_peak_gain(path: Path) -> float:
    """Gain (in dB) needed to push the file's true‑peak to ≈ –1 dBFS."""
    null = "NUL" if os.name == "nt" else "/dev/null"
    proc = subprocess.run([FFMPEG, "-i", path, "-af", "volumedetect", "-f", "null", null],
                          stderr=subprocess.PIPE, text=True)
    for line in proc.stderr.splitlines():
        if "max_volume" in line:
            max_db = float(line.split(":")[1].strip().split()[0])
            return -(max_db + 1.0)
    return 0.0


def convert_to_mp3(src: Path, dst: Path):
    """Normalise + transcode *src* to MP3 at *dst*."""
    dst.parent.mkdir(parents=True, exist_ok=True)

    if NORMALISE == "loudnorm":
        af = ("loudnorm=I=-16:LRA=11:TP=-1.5:"
              "measured_I=-16:measured_LRA=0:"
              "measured_TP=-2:measured_thresh=-26:offset=0")
    elif NORMALISE == "peak_simple":
        af = "dynaudnorm=p=1:m=100:f=150"
    elif NORMALISE == "peak_exact":
        af = f"volume={detect_peak_gain(src):.2f}dB"
    else:
        af = None

    cmd = [FFMPEG, "-y", "-i", str(src), "-vn"]
    if af:
        cmd += ["-af", af]
    cmd += ["-ar", SAMPLE_RATE, "-ac", CHANNELS, "-b:a", BITRATE, str(dst)]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ----------------------------------------------------------------------------------
#                 DATA SPLIT AND AUDIO CONVERSION
# ----------------------------------------------------------------------------------

def gather_files_by_class(src_root: Path):
    """Return {class_name: [list of Path]} filtering non‑audio."""
    mapping = {}
    for p in src_root.rglob("*"):
        if p.is_file() and ffmpeg_audio_stream_exists(p):
            rel = p.relative_to(src_root)
            class_name = rel.parts[0]
            mapping.setdefault(class_name, []).append(p)
    return mapping


def split_list(items, fractions):
    random.shuffle(items)
    n, idx, out = len(items), 0, {}
    for name, frac in fractions.items():
        take = round(n * frac)
        out[name] = items[idx:idx + take]
        idx += take
    out["train"].extend(items[idx:])
    return out


def batch_convert(src_root: Path, dst_root: Path):
    random.seed(RND_SEED)

    class_map = gather_files_by_class(src_root)

    print("=== File counts per class ===")
    for cls, files in class_map.items():
        print(f"{cls}: {len(files)} files")
    print()

    for cls, files in class_map.items():
        splits = split_list(files, SPLIT_FRACTIONS)

        for split_name, items in splits.items():
            for src_path in items:
                rel = src_path.relative_to(src_root)
                dst_path = (dst_root / split_name / rel).with_suffix(OUTPUT_EXT)
                try:
                    convert_to_mp3(src_path, dst_path)
                except Exception as e:
                    print(f"Error on {src_path}: {e}")

        counts = {k: len(v) for k, v in splits.items()}
        print(f"{cls} split → {counts}")

# ----------------------------------------------------------------------------------
#                     SPECTROGRAM CACHING FOR CNN
# ----------------------------------------------------------------------------------

def waveform_to_logmelspec(y, sr, n_mels=N_MELS, hop_length=HOP_LENGTH):
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048,
                                       hop_length=hop_length,
                                       n_mels=n_mels, power=2.0)
    S_db = librosa.power_to_db(S, ref=np.max)
    return ((S_db + 80) / 80).astype(np.float32)


def process_file(path: Path):
    y, sr = librosa.load(path, sr=None, mono=True)
    if sr != SR:
        y = librosa.resample(y, orig_sr=sr, target_sr=SR)
    y, _ = librosa.effects.trim(y, top_db=25)

    # pad / crop
    if y.shape[0] < CLIP_SAMPLES:
        y = np.pad(y, (0, CLIP_SAMPLES - y.shape[0]))
    else:
        start = random.randint(0, y.shape[0] - CLIP_SAMPLES)
        y = y[start:start + CLIP_SAMPLES]

    return waveform_to_logmelspec(y, SR)

def denoise_spec(spec_norm: np.ndarray, margin_db: float = 6.0) -> np.ndarray:
    spec_db = spec_norm * 80.0 - 80.0

    noise_floor = np.median(spec_db, axis=1, keepdims=True)

    cleaned_db = np.clip(spec_db - noise_floor - margin_db, -80.0, 0.0)

    return (cleaned_db + 80.0) / 80.0


def debug_stats(arr, name):
    print(f"{name}: min {arr.min():.2f}, max {arr.max():.2f}, "
          f"mean {arr.mean():.2f}, std {arr.std():.2f}")


def build_cache(audio_dir: Path, cache_dir: Path, save_png: bool = True):
    cache_dir.mkdir(parents=True, exist_ok=True)
    spec_paths = []

    for ext in ("*.mp3", "*.wav", "*.flac", "*.ogg", "*.m4a"):
        for audio_path in audio_dir.rglob(ext):
            spec = process_file(audio_path)
            spec = denoise_spec(spec)
            out = cache_dir / (audio_path.stem + ".npy")
            np.save(out, spec)
            if save_png:
                import matplotlib.pyplot as plt
                plt.imsave(out.with_suffix(".png"),
                           spec,       # dB scale (spec * 80 - 80) -> To undo normalization
                           origin="lower", cmap="magma", vmin=0, vmax=1) # -> vmin = 80, wmax = 0 if normalization undone
            spec_paths.append(out)

    (cache_dir / "manifest.json").write_text(json.dumps([str(p) for p in spec_paths]))
    print(f"Cached {len(spec_paths)} specs → {cache_dir}")


if __name__ == "__main__":
    SRC_ROOT = Path("Proyecto-Investigacion/Sounds-Raw").resolve()
    DST_ROOT = Path("Proyecto-Investigacion/Sounds-Processed").resolve()

    batch_convert(SRC_ROOT, DST_ROOT)

    '''
    for split in ("train", "val", "test"):
        build_cache(DST_ROOT / split / "Non-Strident", DST_ROOT / "cache" / split / "Non-Strident")

    for split in ("train", "val", "test"):
        build_cache(DST_ROOT / split / "Strident", DST_ROOT / "cache" / split / "Strident")
    '''

    print("\nAll done — audio converted & spectrogram cache ready!")
