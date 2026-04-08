from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re
import difflib
from functools import lru_cache

_ARABIC_MODEL  = "CAMeL-Lab/arabart-qalb15-gec-ged-13"
_ENGLISH_MODEL = "vennify/t5-base-grammar-correction"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@lru_cache(maxsize=2)
def load_model(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model     = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    model.eval()
    return tokenizer, model


def _clean_text(text: str) -> str:
    text = re.sub(r'[^\x00-\x7F\u0600-\u06FF\s.,!?]', '', text)
    return text.strip()


def _generate(tokenizer, model, text: str, max_len=128) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_len,
            num_beams=2,
            early_stopping=True,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def _build_changes(original: str, corrected: str) -> list[dict]:
    orig_words = original.split()
    corr_words = corrected.split()
    matcher    = difflib.SequenceMatcher(None, orig_words, corr_words)
    changes    = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        orig_chunk = " ".join(orig_words[i1:i2])
        corr_chunk = " ".join(corr_words[j1:j2])

        if tag == "replace":
            changes.append({
                "type":        "replace",
                "original":    orig_chunk,
                "corrected":   corr_chunk,
                "description": f'"{orig_chunk}" → "{corr_chunk}"',
            })
        elif tag == "insert":
            changes.append({
                "type":        "insert",
                "original":    "",
                "corrected":   corr_chunk,
                "description": f'أضاف: "{corr_chunk}"',
            })
        elif tag == "delete":
            changes.append({
                "type":        "delete",
                "original":    orig_chunk,
                "corrected":   "",
                "description": f'حذف: "{orig_chunk}"',
            })

    return changes


def correct_arabic(text: str) -> dict:
    tokenizer, model = load_model(_ARABIC_MODEL)
    out = _generate(tokenizer, model, text, max_len=256)
    out = _clean_text(out)
    corrected = out if out else text
    return {
        "original":  text,
        "corrected": corrected,
        "changes":   _build_changes(text, corrected),
    }


def correct_english(text: str) -> dict:
    tokenizer, model = load_model(_ENGLISH_MODEL)
    prompt = f"Fix grammar: {text}"
    out    = _generate(tokenizer, model, prompt)
    out    = _clean_text(out)
    corrected = out if out else text
    return {
        "original":  text,
        "corrected": corrected,
        "changes":   _build_changes(text, corrected),
    }


def correct_text(text: str, is_arabic: bool) -> dict:
    if is_arabic:
        return correct_arabic(text)
    return correct_english(text)