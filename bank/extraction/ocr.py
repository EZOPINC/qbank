from django.conf import settings
from django.utils.module_loading import import_string


class TesseractProvider:
    def ocr_image(self, image):
        import pytesseract
        lang = settings.OCR_LANGS
        text = pytesseract.image_to_string(image, lang=lang, config="--psm 4")
        data = pytesseract.image_to_data(
            image, lang=lang, output_type=pytesseract.Output.DICT)
        confs = [float(c) for c in data["conf"] if str(c) not in ("-1", "")]
        return text, (sum(confs) / len(confs) / 100 if confs else 0.0)


def get_provider():
    return import_string(settings.OCR_PROVIDER)()
