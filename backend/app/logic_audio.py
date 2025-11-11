import io, numpy as np, librosa, soundfile as sf
from pydub import AudioSegment

def load_audio_to_mono_wav_bytes(file_bytes: bytes) -> tuple[np.ndarray, int]:
    # Normalize any common format to mono PCM via pydub+ffmpeg, then to numpy with soundfile
    audio = AudioSegment.from_file(io.BytesIO(file_bytes))
    audio = audio.set_channels(1).set_frame_rate(16000)
    out = io.BytesIO()
    audio.export(out, format="wav")
    out.seek(0)
    y, sr = sf.read(out)
    if y.ndim > 1: y = y.mean(axis=1)
    return y.astype(np.float32), sr

def audio_metrics(file_bytes: bytes):
    y, sr = load_audio_to_mono_wav_bytes(file_bytes)
    dur = len(y)/sr
    # crude amplitude & pitch proxy
    mean_amp = float(np.mean(np.abs(y)))
    # syllable rate proxy via energy zero crossings
    zcr = librosa.feature.zero_crossing_rate(y, frame_length=1024, hop_length=512).mean()
    # very rough syll/sec estimate
    syl_per_sec = float(5.0 * zcr)  # tuned constant; refine with real data
    wpm = syl_per_sec * 12.0  # ~ average 12 syllables per 10 words -> 120 wpm baseline

    # pitch (fundamental) estimate using librosa yin (guarded)
    pitch = None
    try:
        f0 = librosa.yin(y, fmin=70, fmax=350, sr=sr, frame_length=2048)
        pitch = float(np.nanmedian(f0))
    except Exception:
        pass

    return {
        "duration_s": float(dur),
        "est_syllables_per_sec": float(syl_per_sec),
        "est_wpm": float(wpm),
        "mean_amplitude": mean_amp,
        "pitch_hz": pitch
    }
