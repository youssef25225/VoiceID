import whisper
import tempfile
import os
from pydub import AudioSegment

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("small")
    return _model


def transcribe_audio(audio_bytes: bytes) -> dict:
    tmp_in = None
    tmp_wav = None

    try:
        suffix = ".webm"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(audio_bytes)
            tmp_in = f.name

        tmp_wav = tmp_in.replace(suffix, ".wav")

        audio = None
        try:
            audio = AudioSegment.from_file(tmp_in)
        except Exception:
            for fmt in ("wav", "ogg", "mp3", "mp4", "m4a"):
                try:
                    audio = AudioSegment.from_file(tmp_in, format=fmt)
                    break
                except Exception:
                    continue

        if audio is None:
            raise RuntimeError("Could not decode audio in any known format")

        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(tmp_wav, format="wav")

        model = _get_model()
        result = model.transcribe(tmp_wav, task="transcribe", fp16=False)

        lang = result.get("language", "unknown")
        text = result.get("text", "").strip()

        return {
            "text": text,
            "language": lang,
            "is_arabic": lang == "ar",
            "is_english": lang == "en",
        }

    except Exception as e:
        return {
            "text": "",
            "language": "unknown",
            "is_arabic": False,
            "is_english": False,
            "error": str(e),
        }

    finally:
        for p in [tmp_in, tmp_wav]:
            if p:
                try:
                    os.remove(p)
                except Exception:
                    pass