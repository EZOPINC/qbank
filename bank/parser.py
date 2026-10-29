"""Turns page text into question dicts. Never invents answers: missing -> None + flag."""
import re
from django.conf import settings
from .normalize import normalize_text, detect_language

Q_RE = re.compile(r"^(\d{1,3})\s*[.,)]\s*(\S.*)")
# tolerates OCR slips: (p)->D, (Cc)->C
OPT_MARK = re.compile(r"(?:^|(?<=\s))[(\[]?\s*(Cc|[A-Da-dpP])\s*[)\]]")
OCR_FIX = {"P": "D", "CC": "C"}
ANS_HDR = re.compile(r"^answer\s*sheet", re.I)
ANS_PAIR = re.compile(r"(\d{1,3})\s*[.,)]?\s*\(\s*(\w)\s*\)")
# running page header, e.g. "Indian National Movement 133"
NOISE = re.compile(r"^[A-Za-z ]{3,40}\s+\d{3}$")
BRACKET = re.compile(r"\[([^\]]{3,160})\]", re.S)
TAG = re.compile(
    r"([A-Za-z0-9][A-Za-z0-9.\-/ ]*?(?:\s*\([A-Za-z ]+\))?)\s*(\d{4}(?:\s*,\s*\d{4})*)")


def extract_tags(text):
    """'[UPPCS (Pre) 1993, 1991]' -> remove from text, return [{'exam','year'}]."""
    tags = []

    def repl(m):
        found = [(re.sub(r"\s+", " ", t.group(1)).strip(), y)
                 for t in TAG.finditer(m.group(1)) for y in re.findall(r"\d{4}", t.group(2))]
        if not found:
            return m.group(0)
        tags.extend({"exam": e, "year": int(y)} for e, y in found)
        return " "
    return BRACKET.sub(repl, text), tags


def split_options(line):
    """'(A) Lahore (B) Delhi' -> [('A','Lahore'),('B','Delhi')]; [] if line doesn't start with an option."""
    marks = list(OPT_MARK.finditer(line))
    if not marks or marks[0].start() != 0:
        return []
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(line)
        k = m.group(1).upper()
        out.append((OCR_FIX.get(k, k), line[m.end():end].strip()))
    return out


def _starts_new(cur, last, n):
    if cur is None:
        return True
    # numbered statements inside a stem ("1. ...", "2. ...")
    if not cur["options"]:
        return False
    # tolerate OCR-dropped numbers; gaps get flagged
    return n == 1 or last < n <= last + 4


def _finalize(q):
    stem, tags = extract_tags(" ".join(q["stem"]))
    opts = {}
    for k, v in q["options"].items():
        v, t = extract_tags(v)
        opts[k] = normalize_text(v)
        tags += t
    flags = []
    if len(opts) < 4 or not all(opts.get(k) for k in "ABCD"):
        flags.append("incomplete_options")
    if any(len(v) > 250 for v in opts.values()) or len(stem) > 900:
        # likely swallowed a neighbouring question
        flags.append("possible_merge")
    if not q.get("answer"):
        flags.append("missing_answer")
    if not tags:
        flags.append("no_year_tag")
    conf = q["conf"]
    if conf is not None and conf < settings.LOW_CONFIDENCE:
        flags.append("low_ocr_confidence")
    stem = normalize_text(stem)
    return {
        "number": q["number"], "text": stem, "options": {k: opts.get(k, "") for k in "ABCD"},
        "answer": q.get("answer"), "tags": tags, "page": q["page"],
        "confidence": conf, "flags": flags, "language": detect_language(stem),
    }


def parse_pages(pages):
    done, block, answers = [], [], {}
    # state: q (questions) | ans (answer sheet) | heading (skip chapter title)
    cur, last, state = None, 0, "q"

    def close():
        nonlocal cur
        if cur:
            block.append(cur)
            cur = None

    def flush():
        close()
        for q in block:
            if q["number"] in answers:
                q["answer"] = answers[q["number"]]
        done.extend(_finalize(q) for q in block)
        block.clear()
        answers.clear()

    for page in pages:
        for raw in page.text.splitlines():
            line = raw.strip()
            if not line or NOISE.match(line):
                continue
            if ANS_HDR.match(line):
                close()
                state = "ans"
                continue
            if state == "ans":
                pairs = ANS_PAIR.findall(line)
                if pairs and not ANS_PAIR.sub("", line).strip(" ,;"):
                    # unreadable letters stay empty
                    answers.update({int(n): a.upper()
                                   for n, a in pairs if a.upper() in "ABCD"})
                    continue
                flush()
                state = "heading"
            if state == "heading":
                m = Q_RE.match(line)
                if m and int(m.group(1)) == 1:
                    state = "q"
                    last = 0
                else:
                    continue
            m = Q_RE.match(line)
            if m and _starts_new(cur, last, int(m.group(1))):
                close()
                last = int(m.group(1))
                cur = {"number": last, "stem": [m.group(2)], "options": {}, "page": page.number,
                       "conf": page.confidence, "last_opt": None}
                continue
            if cur is None:
                continue
            opts = split_options(line)
            if opts:
                for k, v in opts:
                    cur["options"][k] = v
                    cur["last_opt"] = k
            elif cur["options"]:
                cur["options"][cur["last_opt"]] += " " + line
            else:
                cur["stem"].append(line)
    flush()
    return done
