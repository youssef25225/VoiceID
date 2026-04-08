from __future__ import annotations
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

_arabic_pipe: object | None  = None
_english_pipe: object | None = None

_ARABIC_MODEL  = "CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment"
_ENGLISH_MODEL = "j-hartmann/emotion-english-distilroberta-base"


def _get_arabic_pipe():
    global _arabic_pipe
    if _arabic_pipe is None:
        tokenizer = AutoTokenizer.from_pretrained(_ARABIC_MODEL)
        model     = AutoModelForSequenceClassification.from_pretrained(_ARABIC_MODEL)
        _arabic_pipe = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1,
            top_k=None,
        )
    return _arabic_pipe


def _get_english_pipe():
    global _english_pipe
    if _english_pipe is None:
        tokenizer = AutoTokenizer.from_pretrained(_ENGLISH_MODEL)
        model     = AutoModelForSequenceClassification.from_pretrained(_ENGLISH_MODEL)
        _english_pipe = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1,
            top_k=None,
        )
    return _english_pipe


def _normalise_arabic(label: str) -> str:
    label = label.lower().strip()
    if label in ("positive", "pos", "label_2", "label_pos"):
        return "positive"
    if label in ("negative", "neg", "label_0", "label_neg"):
        return "negative"
    return "neutral"


def _normalise_english(label: str) -> str:
    return label.lower().strip()


EMOJI_MAP = {
    "positive": "😊",
    "negative": "😞",
    "neutral":  "😐",
    "joy":      "😄",
    "anger":    "😠",
    "sadness":  "😢",
    "fear":     "😨",
    "surprise": "😲",
    "love":     "❤️",
    "disgust":  "🤢",
}

COLOR_MAP = {
    "positive": "green",
    "negative": "red",
    "neutral":  "amber",
    "joy":      "green",
    "anger":    "red",
    "sadness":  "blue",
    "fear":     "purple",
    "surprise": "amber",
    "love":     "pink",
    "disgust":  "purple",
}

LABEL_AR_MAP = {
    "positive": "إيجابي",
    "negative": "سلبي",
    "neutral":  "محايد",
    "joy":      "فرح",
    "anger":    "غضب",
    "sadness":  "حزن",
    "fear":     "خوف",
    "surprise": "مفاجأة",
    "love":     "حب",
    "disgust":  "اشمئزاز",
}


def analyse_emotion(text: str, is_arabic: bool) -> dict:
    empty = {
        "label":      "neutral",
        "score":      0.0,
        "emoji":      "😐",
        "color":      "amber",
        "label_ar":   "محايد",
        "all_scores": {},
        "error":      None,
    }

    if not text or not text.strip():
        empty["error"] = "empty_text"
        return empty

    try:
        if is_arabic:
            pipe = _get_arabic_pipe()
            raw  = pipe(text[:512])
            results = raw[0] if isinstance(raw[0], list) else raw

            all_scores: dict[str, float] = {}
            for item in results:
                norm  = _normalise_arabic(item["label"])
                score = float(item["score"])
                all_scores[norm] = max(all_scores.get(norm, 0.0), score)

            for lbl in ("positive", "negative", "neutral"):
                all_scores.setdefault(lbl, 0.0)

        else:
            pipe = _get_english_pipe()
            raw  = pipe(text[:512])
            results = raw[0] if isinstance(raw[0], list) else raw

            all_scores = {}
            for item in results:
                norm  = _normalise_english(item["label"])
                score = float(item["score"])
                all_scores[norm] = max(all_scores.get(norm, 0.0), score)

            for lbl in ("joy", "anger", "sadness", "fear", "surprise", "love", "disgust", "neutral"):
                all_scores.setdefault(lbl, 0.0)

        best_label = max(all_scores, key=all_scores.__getitem__)
        best_score = all_scores[best_label]

        return {
            "label":      best_label,
            "score":      best_score,
            "emoji":      EMOJI_MAP.get(best_label, "😐"),
            "color":      COLOR_MAP.get(best_label, "amber"),
            "label_ar":   LABEL_AR_MAP.get(best_label, best_label),
            "all_scores": all_scores,
            "error":      None,
        }

    except Exception as exc:
        empty["error"] = str(exc)
        return empty