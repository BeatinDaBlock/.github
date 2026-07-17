#!/usr/bin/env python3
"""
scripts/transcribe-episodes.py

Transcribes local podcast episode audio files to text using OpenAI's
Whisper model, running entirely on your machine (no API key, no cost).

Intended to run against a directory where your Cloudflare R2 bucket
(e.g. "beatindablock-media") is mounted locally via rclone:

    rclone mount R2:beatindablock-media ~/mnt/beatindablock-media &
    python3 scripts/transcribe-episodes.py ~/mnt/beatindablock-media

Requirements (install once):
    pip install openai-whisper
    # ffmpeg must also be installed and on PATH:
    #   macOS:  brew install ffmpeg
    #   Ubuntu: sudo apt install ffmpeg

Usage:
    python3 scripts/transcribe-episodes.py <audio_dir> [--model base] [--out transcribed/]

Output:
    One .txt file per episode under the --out directory (default: transcribed/),
    mirroring the source filename, plus a manifest at transcribed/manifest.json
    summarizing what was processed.

    Bring the resulting .txt files back (paste the content, or push them to a
    branch) and they can be cleaned up and published as episode posts, the
    same way BeatinDaBlock #88 was handled.
"""

import argparse
import json
import sys
from pathlib import Path

AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".wma"}


def find_audio_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.suffix.lower() in AUDIO_EXTENSIONS)


def transcribe_all(audio_dir: Path, out_dir: Path, model_name: str) -> None:
    try:
        import whisper
    except ImportError:
        print(
            "ERROR: openai-whisper is not installed.\n"
            "Run: pip install openai-whisper\n"
            "(also requires ffmpeg on your PATH)",
            file=sys.stderr,
        )
        sys.exit(1)

    audio_files = find_audio_files(audio_dir)
    if not audio_files:
        print(f"No audio files found under {audio_dir}")
        return

    print(f"Found {len(audio_files)} audio file(s). Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []

    for i, audio_path in enumerate(audio_files, 1):
        rel = audio_path.relative_to(audio_dir)
        out_path = (out_dir / rel).with_suffix(".txt")

        if out_path.exists():
            print(f"[{i}/{len(audio_files)}] Skipping (already transcribed): {rel}")
            manifest.append({"source": str(rel), "transcript": str(out_path), "status": "skipped"})
            continue

        print(f"[{i}/{len(audio_files)}] Transcribing: {rel}")
        try:
            result = model.transcribe(str(audio_path))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(result["text"].strip() + "\n", encoding="utf-8")
            manifest.append({
                "source": str(rel),
                "transcript": str(out_path),
                "status": "ok",
                "language": result.get("language"),
            })
        except Exception as exc:
            print(f"  ERROR transcribing {rel}: {exc}", file=sys.stderr)
            manifest.append({"source": str(rel), "status": "error", "error": str(exc)})

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nDone. Transcripts written to {out_dir}/")
    print(f"Manifest: {manifest_path}")


def main():
    parser = argparse.ArgumentParser(description="Transcribe local podcast episode audio with Whisper.")
    parser.add_argument("audio_dir", type=Path, help="Directory of audio files (e.g. your rclone R2 mount)")
    parser.add_argument("--model", default="base", help="Whisper model size: tiny, base, small, medium, large (default: base)")
    parser.add_argument("--out", type=Path, default=Path("transcribed"), help="Output directory for .txt transcripts (default: transcribed/)")
    args = parser.parse_args()

    if not args.audio_dir.is_dir():
        print(f"Not a directory: {args.audio_dir}", file=sys.stderr)
        sys.exit(1)

    transcribe_all(args.audio_dir, args.out, args.model)


if __name__ == "__main__":
    main()
