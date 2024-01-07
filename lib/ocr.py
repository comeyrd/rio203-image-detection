""" path to text OCR"""

from collections import Counter
import pytesseract


def most_common(lst):
    """return most common element"""
    combined_text = " ".join(lst)
    words = combined_text.split()
    return Counter(words).most_common(1)[0][0]


def do_pytesseract(path_to_image):
    """return text from image"""
    whitelist = "0123456789-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    p = []
    for psm in range(6, 13 + 1):
        config = f"--oem 3 --psm {psm} -c tessedit_char_whitelist={whitelist}"
        txt = pytesseract.image_to_string(path_to_image, config=config)
        p.append(txt)
    return most_common(p)


def path_to_text(path_to_image):
    """return text from image"""
    text = do_pytesseract(path_to_image)
    return text
