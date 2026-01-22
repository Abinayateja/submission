COST_KEYWORDS = ["total", "amount", "price", "cost", "rupees"]

def extract_cost(words):
    candidates = []

    for w in words:
        txt = w["text"].replace(",", "").replace(".", "")
        if txt.isdigit():
            val = int(txt)
            if 50_000 <= val <= 10_000_000:
                candidates.append((val, w))

    if not candidates:
        return None, 0.0

    # keyword reinforcement
    for val, w in candidates:
        if any(k in w["text"].lower() for k in COST_KEYWORDS):
            return val, 1.0

    # fallback: max reasonable amount
    return max(candidates, key=lambda x: x[0])[0], 0.6
