from __future__ import annotations
import io
import os
import tempfile

import numpy as np
import torch
import torchaudio
import soundfile as sf
from pydub import AudioSegment
from transformers import AutoFeatureExtractor, WavLMForXVector

TARGET_SR = 16_000
MIN_SIGNAL_SAMPLES = TARGET_SR * 1

_MODEL_ID = "microsoft/wavlm-base-plus-sv"

_feature_extractor = None
_model             = None


def _load_model():
    global _feature_extractor, _model
    if _feature_extractor is None or _model is None:
        _feature_extractor = AutoFeatureExtractor.from_pretrained(_MODEL_ID)
        _model = WavLMForXVector.from_pretrained(_MODEL_ID)
        _model.eval()
    return _feature_extractor, _model


def _load_audio_bytes(audio_bytes: bytes):
    try:
        signal, sr = torchaudio.load(io.BytesIO(audio_bytes))
        return signal, sr
    except Exception:
        pass

    tmp_in = tmp_wav = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            f.write(audio_bytes)
            tmp_in = f.name
        tmp_wav = tmp_in.replace(".webm", ".wav")
        seg = AudioSegment.from_file(tmp_in)
        seg = seg.set_channels(1).set_frame_rate(TARGET_SR)
        seg.export(tmp_wav, format="wav")
        signal, sr = torchaudio.load(tmp_wav)
        return signal, sr
    except Exception:
        pass
    finally:
        for p in [tmp_in, tmp_wav]:
            if p:
                try:
                    os.remove(p)
                except Exception:
                    pass

    try:
        arr, sr = sf.read(io.BytesIO(audio_bytes), dtype="float32", always_2d=True)
        return torch.tensor(arr.T), sr
    except Exception:
        pass

    raise RuntimeError("Could not decode audio")


def extract_embedding(audio_bytes: bytes) -> np.ndarray | None:
    try:
        fe, model = _load_model()

        signal, sr = _load_audio_bytes(audio_bytes)

        if signal.shape[0] > 1:
            signal = signal.mean(dim=0, keepdim=True)

        if sr != TARGET_SR:
            signal = torchaudio.transforms.Resample(sr, TARGET_SR)(signal)

        if signal.shape[-1] < MIN_SIGNAL_SAMPLES:
            return None

        waveform    = signal.squeeze(0)
        waveform_np = waveform.numpy()

        inputs = fe(
            [waveform_np],
            sampling_rate=TARGET_SR,
            return_tensors="pt",
            padding=True,
        )

        with torch.no_grad():
            outputs = model(**inputs)
            emb = outputs.embeddings[0]

        return emb.cpu().numpy().astype("float32")

    except Exception as e:
        print(f"[features] extract_embedding error: {e}")
        return None


EMBEDDING_DIM = 512