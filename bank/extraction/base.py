from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass
class Page:
    number: int
    text: str
    confidence: Optional[float]  # 0..1; None for digital text (treated as 1.0)
    method: str                  # "digital" | "ocr"


class OCRProvider(Protocol):
    """Implement this to plug in another OCR engine (PaddleOCR, Google Vision, ...)."""
    def ocr_image(self, image) -> tuple[str, float]:
        """Return (text, mean_confidence 0..1) for a PIL image."""
