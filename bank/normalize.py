import hashlib
import re
import unicodedata


def normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s or "")   # keeps Bengali/Hindi conjuncts + maths symbols intact
    return re.sub(r"[ \t]+", " ", s).strip()


def content_hash(text, a, b, c, d) -> str:
    canon = "|".join(re.sub(r"\W+", "", normalize_text(x).casefold()) for x in (text, a, b, c, d))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def detect_language(s: str) -> str:
    bn = sum("\u0980" <= ch <= "\u09FF" for ch in s)
    hi = sum("\u0900" <= ch <= "\u097F" for ch in s)
    letters = sum(ch.isalpha() for ch in s) or 1
    if bn / letters > 0.3:
        return "bn"
    if hi / letters > 0.3:
        return "hi"
    return "en"
