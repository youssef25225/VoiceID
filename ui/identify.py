import streamlit as st
import numpy as np
from core.features import extract_embedding
from core.faiss_db import VoiceModel

MIN_AUDIO_BYTES = 40_000
DEFAULT_K       = 3
DEFAULT_THRESH  = 0.75


def render():
    model: VoiceModel = st.session_state.get("model")

    if "results" not in st.session_state:
        st.session_state.results = []

    if not st.session_state.get("model_ready") or model is None:
        st.markdown("""
        <div style="
          text-align:center;
          padding:3rem 1.5rem;
          border:1px dashed var(--border-strong);
          border-radius:var(--r-lg);
        ">
          <div style="font-size:2rem;margin-bottom:12px">🔒</div>
          <div style="font-size:var(--sz-md);font-weight:600;color:var(--ink);margin-bottom:6px">
            النموذج غير مبني
          </div>
          <div style="font-size:var(--sz-sm);color:var(--ink3);font-family:var(--ff-mono)">
            اذهب الى تبويب التسجيل وابن النموذج اولا
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div style="margin-bottom:1.6rem;display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap">
      <div>
        <div style="font-size:var(--sz-xl);font-weight:700;font-family:var(--ff-display);
                    color:var(--ink);letter-spacing:-.02em;">التعرف على المتحدث</div>
        <div style="font-size:var(--sz-sm);color:var(--ink3);margin-top:4px;font-family:var(--ff-mono)">
          سجل مقطعا صوتيا للتعرف على هوية المتحدث
        </div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
        <span class="badge violet">{model.n_speakers} متحدث</span>
        <span class="badge blue">{model.n_vectors} متجه</span>
        <span class="badge green">النموذج نشط</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if "identify_audio_key" not in st.session_state:
        st.session_state.identify_audio_key = 0

    audio_data = st.audio_input(
        "تسجيل الصوت",
        key=f"identify_audio_{st.session_state.identify_audio_key}",
    )
    if audio_data:
        st.audio(audio_data)

    if st.button("التعرف على الصوت", use_container_width=True):
        if audio_data is None:
            st.error("سجل صوتا اولا")
            return
        if len(audio_data.getvalue()) < MIN_AUDIO_BYTES:
            st.error("الصوت قصير جدا — سجل 3 ثوان على الاقل")
            return

        with st.spinner("استخراج البصمة الصوتية..."):
            feat = extract_embedding(audio_data.getvalue())

        if feat is None:
            st.error("فشل استخراج البصمة الصوتية")
            return

        speaker, score, votes = model.predict(feat, k=DEFAULT_K, threshold=DEFAULT_THRESH)
        is_unknown = speaker == "Unknown"
        score_pct  = int(max(0, min(100, score * 100)))

        st.markdown(f"""
        <div class="result-card {'unknown' if is_unknown else 'match'}">
          <div class="result-eyebrow">{'غير معروف' if is_unknown else 'تم التعرف'}</div>
          <div class="result-name">{speaker if not is_unknown else 'مجهول'}</div>
          <div class="result-meta">
            <span>Score: <b>{score:.3f}</b></span>
            <span>Threshold: <b>{DEFAULT_THRESH:.2f}</b></span>
          </div>
          <div class="conf-track">
            <div class="conf-fill {'unknown' if is_unknown else 'match'}" style="width:{score_pct}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if votes and len(votes) > 1:
            st.markdown("<div class='section-header' style='margin-top:1.5rem'>توزيع الاصوات</div>",
                        unsafe_allow_html=True)
            total  = sum(votes.values())
            winner = max(votes, key=votes.get)
            for name, count in sorted(votes.items(), key=lambda x: -x[1]):
                pct    = int((count / total) * 100)
                is_win = name == winner
                st.markdown(f"""
                <div class="vote-row">
                  <div class="vote-name">{name}</div>
                  <div class="vote-track">
                    <div class="vote-fill {'winner' if is_win else ''}" style="width:{pct}%"></div>
                  </div>
                  <div class="vote-pct">{pct}%</div>
                </div>
                """, unsafe_allow_html=True)

        st.session_state.results.append({
            "speaker":  speaker if not is_unknown else "مجهول",
            "score":    round(score, 3),
            "unknown":  is_unknown,
            "k":        DEFAULT_K,
        })
        st.session_state.identify_audio_key += 1

    if st.session_state.results:
        st.markdown("<div class='section-header' style='margin-top:2rem'>سجل التعرف</div>",
                    unsafe_allow_html=True)
        for r in reversed(st.session_state.results[-10:]):
            color = "var(--red)" if r["unknown"] else "var(--green)"
            label = "مجهول" if r["unknown"] else r["speaker"]
            st.markdown(f"""
            <div class="log-item">
              <div class="log-name" style="color:{color}">{label}</div>
              <div class="log-k">K={r['k']}</div>
              <div class="log-conf">score={r['score']}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("مسح السجل"):
            st.session_state.results = []
            st.rerun()