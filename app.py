import streamlit as st
from ui.theme import THEME_CSS
from ui.enroll import render as render_enroll
from ui.speech_tab import render as render_speech
from ui.identify import render as render_identify
from core.faiss_db import VoiceModel
from core.correct import load_model as _load_correction_model
from core.emotional import _get_arabic_pipe, _get_english_pipe

st.set_page_config(
    page_title="VoiceID",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(THEME_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading Arabic correction model...")
def _cache_arabic_correction():
    return _load_correction_model("CAMeL-Lab/arabart-qalb15-gec-ged-13")


@st.cache_resource(show_spinner="Loading English correction model...")
def _cache_english_correction():
    return _load_correction_model("vennify/t5-base-grammar-correction")


@st.cache_resource(show_spinner="Loading Arabic emotion model...")
def _cache_arabic_emotion():
    return _get_arabic_pipe()


@st.cache_resource(show_spinner="Loading English emotion model...")
def _cache_english_emotion():
    return _get_english_pipe()


def _preload_models():
    _cache_arabic_correction()
    _cache_english_correction()
    _cache_arabic_emotion()
    _cache_english_emotion()


def init_state():
    defaults = {
        "enrolled":    {},
        "model":       None,
        "model_ready": False,
        "results":     [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()
_preload_models()

n_spk = len(st.session_state.enrolled)
n_vec = sum(len(v) for v in st.session_state.enrolled.values())
ready = bool(st.session_state.model_ready)

st.markdown(f"""
<div class="app-header">
  <div class="app-wordmark">
    <div class="app-icon">🎙</div>
    <div>
      <div class="app-title">VoiceID</div>
      <div class="app-subtitle">by Yousef Emam</div>
    </div>
  </div>
  <div class="header-pills">
    <span class="pill">{n_spk} متحدث</span>
    <span class="pill">{n_vec} تسجيل</span>
    <span class="pill {'active' if ready else ''}">
      {'النموذج جاهز' if ready else 'النموذج غير مبني'}
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

step1 = "done" if ready else "active"
step2 = "active" if ready else "idle"

st.markdown(f"""
<div class="stepper">
  <div class="step-btn {step1}">
    <div class="step-badge">{'✓' if ready else '1'}</div>
    <div class="step-text">
      <div class="step-name">التسجيل</div>
      <div class="step-hint">سجل اصوات المتحدثين</div>
    </div>
  </div>
  <div class="step-btn {step2}">
    <div class="step-badge">2</div>
    <div class="step-text">
      <div class="step-name">التعريف والكلام</div>
      <div class="step-hint">تعرف على المتحدث وصحح النص</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def on_build_model(enrolled: dict):
    if not enrolled:
        st.warning("لا توجد بيانات تسجيل")
        return
    model = VoiceModel()
    model.rebuild(enrolled)
    st.session_state.model       = model
    st.session_state.model_ready = True
    st.success(f"النموذج جاهز — {model.n_speakers} متحدث · {model.n_vectors} متجه")
    st.rerun()


tab_enroll, tab_speech, tab_identify = st.tabs([
    "التسجيل",
    "النسخ والتحليل",
    "التعرف فقط",
])

with tab_enroll:
    render_enroll(on_build_model)

with tab_speech:
    render_speech()

with tab_identify:
    render_identify()