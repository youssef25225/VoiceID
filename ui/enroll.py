import streamlit as st
import numpy as np
from core.features import extract_embedding

MIN_SAMPLES     = 3
MAX_BAR         = 5
MIN_AUDIO_BYTES = 40_000


def _initials(name: str) -> str:
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper() if len(name) >= 2 else name.upper()


def _speaker_grid(enrolled: dict):
    if not enrolled:
        st.markdown("""
        <div style="
          text-align:center; padding:3rem 1rem;
          border:1px dashed var(--border-strong);
          border-radius:var(--r-lg);
          color:var(--ink3);
          font-family:var(--ff-mono);
          font-size:var(--sz-sm);
        ">
          لا يوجد متحدثين مسجلين بعد<br>
          <span style="font-size:var(--sz-2xs); margin-top:4px; display:block; color:var(--ink4)">
            ابدأ بإضافة تسجيل أعلاه
          </span>
        </div>
        """, unsafe_allow_html=True)
        return

    for name, vecs in enrolled.items():
        count    = len(vecs)
        fill_pct = min(count / MAX_BAR * 100, 100)
        is_ready = count >= MIN_SAMPLES
        bar_cls  = "ready" if is_ready else "partial"
        status   = "جاهز" if is_ready else f"{count}/{MIN_SAMPLES}"
        card_cls = "ready" if is_ready else ""
        initials = _initials(name)

        st.markdown(f"""
        <div class="speaker-card {card_cls}">
          <div class="speaker-avatar">{initials}</div>
          <div class="speaker-info">
            <div class="speaker-name">{name}</div>
            <div class="progress-bar">
              <div class="progress-fill {bar_cls}" style="width:{fill_pct}%"></div>
            </div>
            <div class="speaker-meta">
              <span>{count} تسجيل</span>
              <span>•</span>
              <span class="status-dot {bar_cls}">{status}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


def render(on_build_model):
    enrolled = st.session_state.get("enrolled", {})

    st.markdown("""
    <div style="margin-bottom:1.6rem">
      <div style="font-size:var(--sz-xl);font-weight:700;font-family:var(--ff-display);
                  color:var(--ink);letter-spacing:-.02em;">تسجيل المتحدثين</div>
      <div style="font-size:var(--sz-sm);color:var(--ink3);margin-top:4px;font-family:var(--ff-mono)">
        سجل 3 عينات صوتية لكل متحدث على الاقل
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_name, col_pad = st.columns([2, 1])
    with col_name:
        speaker_name = st.text_input("اسم المتحدث", placeholder="مثال: يوسف امام")

    if "enroll_audio_key" not in st.session_state:
        st.session_state.enroll_audio_key = 0

    audio_data = st.audio_input(
        "تسجيل الصوت",
        key=f"enroll_audio_{st.session_state.enroll_audio_key}",
    )

    if audio_data:
        st.audio(audio_data)

    col_add, col_build, col_clear = st.columns([1, 1, 1])

    with col_add:
        if st.button("اضافة تسجيل", use_container_width=True):
            name = speaker_name.strip()
            if not name:
                st.error("ادخل اسم المتحدث")
            elif audio_data is None:
                st.error("سجل صوتا اولا")
            elif len(audio_data.getvalue()) < MIN_AUDIO_BYTES:
                st.error("الصوت قصير جدا — سجل 3 ثوان على الاقل")
            else:
                with st.spinner("استخراج البصمة الصوتية..."):
                    feat = extract_embedding(audio_data.getvalue())
                if feat is None:
                    st.error("فشل استخراج البصمة — جرب صوتا اوضح")
                else:
                    if name not in enrolled:
                        enrolled[name] = []
                    enrolled[name].append(feat)
                    st.session_state.enrolled = enrolled
                    st.session_state.enroll_audio_key += 1
                    st.success(f"تمت الاضافة لـ {name}  ({len(enrolled[name])}/{MIN_SAMPLES})")
                    st.rerun()

    with col_build:
        if st.button("بناء النموذج", use_container_width=True):
            if len(enrolled) < 2:
                st.error("يجب تسجيل متحدثين على الاقل")
            else:
                ready = {n: v for n, v in enrolled.items() if len(v) >= MIN_SAMPLES}
                if len(ready) < 2:
                    st.error(f"يجب ان يكون لدى متحدثين على الاقل {MIN_SAMPLES} تسجيلات")
                else:
                    with st.spinner("جاري بناء النموذج..."):
                        on_build_model(enrolled)

    with col_clear:
        if st.button("مسح الكل", use_container_width=True):
            st.session_state.enrolled = {}
            st.session_state.model_ready = False
            st.session_state.model = None
            st.rerun()

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">المتحدثون المسجلون</div>
    """, unsafe_allow_html=True)

    _speaker_grid(enrolled)

    if enrolled:
        total_ready = sum(1 for v in enrolled.values() if len(v) >= MIN_SAMPLES)
        total       = len(enrolled)
        st.markdown(f"""
        <div style="
          margin-top:1rem;
          padding:12px 16px;
          background:var(--accent-dim);
          border:1px solid var(--accent-border);
          border-radius:var(--r-md);
          font-size:var(--sz-xs);
          font-family:var(--ff-mono);
          color:var(--accent);
        ">
          {total_ready}/{total} متحدثين جاهزون •
          {'يمكن بناء النموذج الان' if total_ready >= 2 else f'تحتاج {max(0, 2-total_ready)} متحدث اضافي على الاقل'}
        </div>
        """, unsafe_allow_html=True)