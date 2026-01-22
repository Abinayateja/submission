import re

def extract_hp(words):
    for w in words:
        text = w["text"].upper()

        match = re.search(r"(\d{2,3})\s*(HP|H\.P|HORSE)", text)
        if match:
            hp = int(match.group(1))
            if 20 <= hp <= 120:
                return hp, 1.0

    # fallback: numeric-only line near model
    for w in words:
        if w["text"].isdigit():
            hp = int(w["text"])
            if 20 <= hp <= 120:
                return hp, 0.5

    return None, 0.0
