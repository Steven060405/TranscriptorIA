import os
import subprocess
from pathlib import Path


def split_audio(input_path, output_dir, chunk_length=60):
    """Split an audio file into chunks (seconds) using ffmpeg.

    Returns a list of paths to the chunk files (WAV, 16k mono).
    """
    input_path = str(input_path)
    output_dir = str(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    base = Path(input_path).stem
    out_pattern = os.path.join(output_dir, f"{base}_%04d.wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ar",
        "16000",
        "-ac",
        "1",
        "-f",
        "segment",
        "-segment_time",
        str(chunk_length),
        "-reset_timestamps",
        "1",
        out_pattern,
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise RuntimeError("ffmpeg no está disponible. Instala FFmpeg y asegúrate que 'ffmpeg' esté en el PATH.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error al partir el audio: {e}")

    parts = sorted(
        [
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.startswith(base) and f.lower().endswith(".wav")
        ]
    )

    return parts
