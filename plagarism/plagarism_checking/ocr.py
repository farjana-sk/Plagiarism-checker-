from PIL import Image
import pytesseract

def extract_text_from_image(filepath):
    try:
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
        return text
    except:
        return ""
