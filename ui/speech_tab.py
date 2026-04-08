from __future__ import annotations
import streamlit as st
import re
import difflib

from core.transcribe import transcribe_audio
from core.correct import correct_text
from core.emotional import analyse_emotion
from core.features import extract_embedding

MIN_AUDIO_BYTES = 40_000
DEFAULT_K       = 3
DEFAULT_THRESH  = 0.75


def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r'(^\w)', lambda m: m.group(1).upper(), text)
    if not re.search(r'[.!?]$', text):
        text += '.'
    return text


def split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return parts if parts else [text]


def is_bad_output(original: str, corrected: str) -> bool:
    if not corrected.strip():
        return True
    if len(corrected.split()) > len(original.split()) * 2:
        return True
    if re.search(r'[^\w\s.,!?]', corrected):
        return True
    return False


def _diff_highlight(original: str, corrected: str) -> str:
    orig_words = original.split()
    corr_words = corrected.split()
    diff  = difflib.ndiff(orig_words, corr_words)
    parts = []
    for d in diff:
        word = d[2:]
        if d.startswith(" "):
            parts.append(f'<span style="color:var(--green)">{word}</span>')
        elif d.startswith("+"):
            parts.append(
                f'<span style="color:var(--amber);font-weight:600;'
                f'background:var(--amber-bg);padding:1px 6px;'
                f'border-radius:3px;border:1px solid var(--amber-border)">{word}</span>'
            )
    return " ".join(parts)


def smart_correct(text: str, is_arabic: bool) -> dict:
    text      = normalize_text(text)
    sentences = split_sentences(text)

    corrected_sentences = []
    all_changes         = []

    for sent in sentences:
        if not sent.strip():
            corrected_sentences.append(sent)
            continue

        result = correct_text(sent, is_arabic=is_arabic)

        if is_bad_output(sent, result["corrected"]):
            corrected_sentences.append(sent)
        else:
            corrected_sentences.append(result["corrected"])
            all_changes.extend(result["changes"])

    final_corrected = " ".join(corrected_sentences)

    return {
        "original":  text,
        "corrected": final_corrected,
        "changes":   all_changes,
    }


def _render_emotion(emotion: dict, is_arabic: bool):
    if emotion.get("error"):
        st.warning(f"Emotion error: {emotion['error']}")
        return

    emoji    = emotion.get("emoji", "")
    label_ar = emotion.get("label_ar", emotion.get("label", ""))
    score    = emotion.get("score", 0.0)
    color    = emotion.get("color", "amber")

    st.markdown(
        f'<div style="font-size:2rem;margin-bottom:4px">{emoji} '
        f'<span style="color:var(--{color})">{label_ar}</span> '
        f'<span style="font-size:0.9rem;opacity:0.7">({score:.0%})</span></div>',
        unsafe_allow_html=True,
    )

    all_scores = emotion.get("all_scores", {})
    if all_scores:
        for lbl, sc in sorted(all_scores.items(), key=lambda x: -x[1]):
            ar = {
                "positive": "إيجابي", "negative": "سلبي",   "neutral": "محايد",
                "joy":      "فرح",    "anger":    "غضب",    "sadness": "حزن",
                "fear":     "خوف",    "surprise": "مفاجأة", "love":    "حب",
            }.get(lbl, lbl)
            st.progress(sc, text=f"{ar}  {sc:.0%}")


def render():
    for key, val in [("speech_audio_key", 0), ("speech_result", None)]:
        if key not in st.session_state:
            st.session_state[key] = val

    model       = st.session_state.get("model")
    model_ready = st.session_state.get("model_ready", False)

    st.title("🎙️ Speech Analysis")

    if not model_ready:
        st.warning("Speaker model not ready")

    audio_data = st.audio_input("Record Audio", key=f"audio_{st.session_state.speech_audio_key}")

    if audio_data:
        st.audio(audio_data)

    if st.button("Analyze", use_container_width=True):
        if audio_data is None:
            st.error("Record audio first")
            return

        if len(audio_data.getvalue()) < MIN_AUDIO_BYTES:
            st.error("Audio too short")
            return

        audio_bytes = audio_data.getvalue()

        with st.spinner("Transcribing..."):
            stt = transcribe_audio(audio_bytes)

        if not stt.get("text"):
            st.error("Speech recognition failed")
            return

        with st.spinner("Correcting..."):
            correction = smart_correct(stt["text"], stt["is_arabic"])

        with st.spinner("Analyzing emotion..."):
            emotion = analyse_emotion(stt["text"], stt["is_arabic"])

        speaker_result = None
        if model_ready and model is not None:
            with st.spinner("Identifying speaker..."):
                emb = extract_embedding(audio_bytes)
                if emb is not None:
                    spk, score, votes = model.predict(emb, k=DEFAULT_K, threshold=DEFAULT_THRESH)
                    speaker_result = {
                        "speaker": spk,
                        "score":   score,
                        "votes":   votes,
                        "unknown": spk == "Unknown",
                    }

        st.session_state.speech_result = {
            "raw":        stt["text"],
            "correction": correction,
            "is_arabic":  stt["is_arabic"],
            "emotion":    emotion,
            "speaker":    speaker_result,
        }

        st.session_state.speech_audio_key += 1
        st.rerun()

    result = st.session_state.speech_result
    if result is None:
        return

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("النص الأصلي")
        st.write(result["raw"])

    with col2:
        st.subheader("النص المصحح")
        correction = result["correction"]
        diff_html  = _diff_highlight(correction["original"], correction["corrected"])
        st.markdown(diff_html, unsafe_allow_html=True)

    changes = correction.get("changes", [])
    if changes:
        st.subheader("التعديلات")
        for ch in changes:
            icon = {"replace": "✏️", "insert": "➕", "delete": "🗑️"}.get(ch["type"], "•")
            st.markdown(f"{icon} {ch['description']}")
    else:
        st.success("لا توجد تعديلات — النص سليم")

    st.subheader("المشاعر")
    _render_emotion(result["emotion"], result["is_arabic"])

    if result["speaker"]:
        st.subheader("المتحدث")
        spk = result["speaker"]
        if spk["unknown"]:
            st.warning("متحدث غير معروف")
        else:
            st.success(f"**{spk['speaker']}** — {spk['score']:.0%}")

    if st.button("Clear"):
        st.session_state.speech_result = None
        st.rerun()