from typing import Tuple

import wave
import numpy as np


def load_wav(
    filepath: str,
    max_duration: float = -1,
    channel=0
) -> Tuple[bytes, int, str, float]:
    """
    Loading bytes and other information from an audio file

    Args:
        filepath: path to the audio file
        max_duration: the max duration in seconds from start
            of the audio clip to load
            if max_duration == -1, load full audio clip

    Returns:
        audio_bytes: bytes that are further sent via POST request
        sr: sampling rate of the audio file
        dtype: audio bit depth
        duration: the duration in seconds
    """
    dtype_tranposed = {1: 'int8', 2: 'int16', 4: 'int32'}
    f = wave.open(filepath)
    sr = f.getframerate()
    if sr < 8000:
        raise ValueError("Sampling rate is too low "
                         "please use audio clips with sampling rate >= 8000")

    if f.getsampwidth() not in list(dtype_tranposed.keys()):
        raise ValueError("This file format is not supported")

    dtype = dtype_tranposed[f.getsampwidth()]
    channels = f.getnchannels()

    if max_duration != -1:
        frames = int(f.getframerate() * max_duration)
        audio_bytes = f.readframes(frames)
        duration = min(frames, f.getnframes()) / f.getframerate()
    else:
        audio_bytes = f.readframes(f.getnframes())
        duration = f.getnframes() / f.getframerate()

    if channel < channels:
        if channels != 1:
            audio_bytes = np.frombuffer(
                audio_bytes, dtype=dtype
            )[channel::channels].tobytes()
    else:
        raise ValueError("The number of channels in "
                         "the audio clip must be greater than channel + 1")

    return audio_bytes, sr, dtype, duration
