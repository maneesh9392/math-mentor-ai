import easyocr
import numpy as np
from PIL import Image

# initialize once (important for performance)
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(image_file):
    """
    Returns:
        text (str)
        confidence (float between 0 and 1)
    """

    image = Image.open(image_file).convert("RGB")
    image_np = np.array(image)

    results = reader.readtext(image_np)

    if not results:
        return "", 0.0

    texts = []
    confidences = []

    for (_, text, conf) in results:
        texts.append(text)
        confidences.append(conf)

    full_text = " ".join(texts)
    avg_conf = float(np.mean(confidences))

    return full_text, avg_conf