from rapidfuzz import process

def extract_model(words, model_master):
    text_blob = " ".join(w["text"] for w in words).lower()

    # fallback: raw model-like tokens
    for token in text_blob.split():
        if token.startswith(("744", "735", "843", "855", "xm")):
            return token.upper(), 0.5

    if not model_master:
        return None, 0.0

    result = process.extractOne(text_blob, model_master)

    if result is None:
        return None, 0.0

    match, score, _ = result

    if score >= 85:
        return match, round(score / 100, 2)

    return match, round(score / 200, 2)
