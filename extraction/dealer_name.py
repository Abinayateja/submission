from rapidfuzz import process

DEALER_KEYWORDS = ["dealer", "m/s", "authorized", "tractors", "motors"]

def extract_dealer(words, master_dealers, img_height):
    lines = {}

    # group words into horizontal lines
    for w in words:
        y = int(w["bbox"][0][1] // 40)
        lines.setdefault(y, []).append(w)

    candidates = []
    for y, ws in lines.items():
        # only top 40% of page
        if (ws[0]["bbox"][0][1] / img_height) > 0.4:
            continue

        line = " ".join(w["text"] for w in ws)
        if any(k in line.lower() for k in DEALER_KEYWORDS):
            candidates.append(line)

    if not candidates:
        return None, 0.0

    best_line = max(candidates, key=len)

    # 🔐 SAFE FUZZY MATCH
    if not master_dealers:
        return best_line, 0.5   # fallback confidence

    result = process.extractOne(best_line, master_dealers)

    if result is None:
        return best_line, 0.5

    match, score, _ = result

    if score >= 90:
        return match, round(score / 100, 2)

    return best_line, round(score / 200, 2)
