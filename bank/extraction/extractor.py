import logging
from pathlib import Path
from django.conf import settings
from .base import Page
from .ocr import get_provider

log = logging.getLogger(__name__)


def _digital_text(page, columns):
    """Read printed columns left-to-right so column text is not interleaved."""
    if columns <= 1:
        return page.extract_text() or ""
    w, h = page.width, page.height
    parts = []
    for i in range(columns):
        crop = page.crop((i * w / columns, 0, (i + 1) * w / columns, h))
        parts.append(crop.extract_text() or "")
    return "\n".join(parts)


def _ocr_columns(ocr, image, columns):
    """OCR each printed column separately (overlapping slightly) so columns are not read across."""
    from PIL import ImageOps
    im = ImageOps.autocontrast(image.convert("L"))
    W, H = im.size
    texts, confs = [], []
    for i in range(max(columns, 1)):
        x0, x1 = max(0, int(W * (i / columns - 0.015))), min(W,
                                                             int(W * ((i + 1) / columns + 0.015)))
        t, c = ocr.ocr_image(im.crop((x0, 0, x1, H)) if columns > 1 else im)
        texts.append(t)
        confs.append(c)
    return "\n".join(texts), sum(confs) / len(confs)


def extract_document(path, on_page=None):
    """Yield-free list of Pages; processes one page at a time to bound memory."""
    path = Path(path)
    pages, ocr = [], None
    if path.suffix.lower() == ".pdf":
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            total = len(pdf.pages)
            for i, pg in enumerate(pdf.pages, 1):
                text = _digital_text(pg, settings.PDF_COLUMNS)
                if len(text.strip()) >= settings.MIN_DIGITAL_CHARS:
                    pages.append(Page(i, text, None, "digital"))
                else:
                    ocr = ocr or get_provider()
                    t, c = _ocr_columns(ocr, pg.to_image(
                        resolution=300).original, settings.PDF_COLUMNS)
                    pages.append(Page(i, t, c, "ocr"))
                log.info("page_extracted doc=%s page=%s method=%s",
                         path.name, i, pages[-1].method)
                if on_page:
                    on_page(i, total)
    else:
        from PIL import Image
        t, c = _ocr_columns(get_provider(), Image.open(
            path), settings.PDF_COLUMNS)
        pages.append(Page(1, t, c, "ocr"))
        if on_page:
            on_page(1, 1)
    return pages
