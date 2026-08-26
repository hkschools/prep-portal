#!/usr/bin/env python3
"""Generate the Listening recordings for every level and version.

    python3 gen_audio.py [level-b] [2]     # optional: one level / one version

Each content module (level_X_vN.py) declares its own AUDIO dict:
    AUDIO = {"listening1.m4a": [(voice, rate, text), ...], ...}

ENGINE: Microsoft neural voices via edge-tts (human-quality; free). A `voice`
containing "Neural" is used as-is with a percent rate string ("-8%"); legacy
macOS names (Samantha/Daniel + wpm ints) are auto-mapped so older modules keep
working. If edge-tts is unavailable or offline, falls back to macOS `say`.
Multi-line entries are stitched as dialogues (WAV concat, short gap).
Output: baseline-tests/<level>/v<N>/<filename> (AAC .m4a).
"""
import glob
import importlib.util
import os
import subprocess
import sys
import tempfile
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
PORTAL = os.path.dirname(os.path.dirname(HERE))

# legacy macOS voice/rate -> neural equivalents
LEGACY_VOICE = {"Samantha": "en-US-AvaNeural", "Daniel": "en-GB-RyanNeural",
                "Karen": "en-AU-NatashaNeural", "Moira": "en-IE-EmilyNeural"}


def _norm(voice, rate):
    if "Neural" in str(voice):
        return voice, (rate if isinstance(rate, str) else "-8%")
    v = LEGACY_VOICE.get(voice, "en-US-AvaNeural")
    wpm = int(rate) if not isinstance(rate, str) else 170
    pct = "-14%" if wpm <= 155 else ("-8%" if wpm <= 170 else "-4%")
    return v, pct


def edge_seg(voice, rate, text, out_mp3):
    v, pct = _norm(voice, rate)
    subprocess.run([sys.executable, "-m", "edge_tts", "--voice", v, f"--rate={pct}",
                    "--text", text, "--write-media", out_mp3],
                   check=True, capture_output=True, timeout=120)


def say_seg(voice, rate, text, out_aiff):
    v = voice if "Neural" not in str(voice) else ("Daniel" if "GB" in voice else "Samantha")
    r = rate if not isinstance(rate, str) else 165
    subprocess.run(["say", "-v", v, "-r", str(r), "-o", out_aiff, text], check=True)


def to_wav(path):
    wav = path.rsplit(".", 1)[0] + ".wav"
    subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@24000", path, wav],
                   check=True, capture_output=True)
    return wav


def concat_wavs(paths, out_path, gap_ms=420):
    with wave.open(paths[0], "rb") as first:
        params = first.getparams()
        frames = [first.readframes(first.getnframes())]
    gap = b"\x00" * int(params.framerate * gap_ms / 1000) * params.sampwidth * params.nchannels
    for p in paths[1:]:
        with wave.open(p, "rb") as f:
            assert f.getparams()[:3] == params[:3], "voice segment format mismatch"
            frames.append(gap)
            frames.append(f.readframes(f.getnframes()))
    with wave.open(out_path, "wb") as out:
        out.setparams(params)
        for fr in frames:
            out.writeframes(fr)


def load_module(path):
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def render(level, version, audio, has_bilingual):
    en_dir = os.path.join(PORTAL, "baseline-tests", level, f"v{version}")
    bi_dir = os.path.join(PORTAL, "baseline-tests", level + "-bilingual", f"v{version}")
    os.makedirs(en_dir, exist_ok=True)
    if has_bilingual:
        os.makedirs(bi_dir, exist_ok=True)
    for fname, lines in audio.items():
        is_zh = "-zh" in fname
        dest_dir = bi_dir if (is_zh and has_bilingual) else en_dir
        dest = os.path.join(dest_dir, fname)
        with tempfile.TemporaryDirectory() as td:
            wavs = []
            engine = "edge"
            for i, (voice, rate, text) in enumerate(lines):
                mp3 = os.path.join(td, f"seg{i}.mp3")
                try:
                    edge_seg(voice, rate, text, mp3)
                    wavs.append(to_wav(mp3))
                except Exception:
                    engine = "say"
                    aiff = os.path.join(td, f"seg{i}.aiff")
                    say_seg(voice, rate, text, aiff)
                    wavs.append(to_wav(aiff))
            combined = wavs[0] if len(wavs) == 1 else os.path.join(td, "combined.wav")
            if len(wavs) > 1:
                concat_wavs(wavs, combined)
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", combined, dest],
                           check=True, capture_output=True)
        if has_bilingual and not is_zh:
            import shutil
            shutil.copy2(dest, os.path.join(bi_dir, fname))
        print(f"{level} v{version}: {fname} ({os.path.getsize(dest)//1024} KB, {engine})")


def main():
    only_level = sys.argv[1] if len(sys.argv) > 1 else None
    only_ver = sys.argv[2] if len(sys.argv) > 2 else None
    for path in sorted(glob.glob(os.path.join(HERE, "level_*_v*.py"))):
        parts = os.path.basename(path)[:-3].split("_")     # [level, b, v1]
        level = f"level-{parts[1]}"
        version = parts[2][1:]
        if only_level and level != only_level:
            continue
        if only_ver and version != only_ver:
            continue
        mod = load_module(path)
        audio = getattr(mod, "AUDIO", None)
        if audio:
            has_bi = any(sec.get("opt") for sec in mod.SECTIONS)
            render(level, version, audio, has_bi)


if __name__ == "__main__":
    main()
