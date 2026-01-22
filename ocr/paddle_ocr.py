from paddleocr import PaddleOCR

# Initialize once (important for speed)
_ocr = PaddleOCR(use_angle_cls=True, lang="en")

def run_ocr(image):
    """
    image: OpenCV BGR image
    returns: list of dicts [{text, bbox, confidence}]
    """
    results = _ocr.ocr(image, cls=True)

    words = []

    if results and results[0]:
        for line in results[0]:
            bbox, (text, conf) = line
            words.append({
                "text": text,
                "bbox": bbox,
                "confidence": conf
            })

    return words
  