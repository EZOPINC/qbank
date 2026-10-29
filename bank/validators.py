from .models import Language, Difficulty, Question
from .normalize import content_hash


def staged_hash(s):
    return content_hash(s.question_text, s.option_a, s.option_b, s.option_c, s.option_d)


def validate_staged(s):
    """Return (errors, warnings): dicts of field -> message. Errors block approval/import."""
    err, warn = {}, {}
    if not s.question_text.strip():
        err["question_text"] = "Question text is required."
    opts = {"A": s.option_a, "B": s.option_b, "C": s.option_c, "D": s.option_d}
    for k, v in opts.items():
        if not v.strip():
            err[f"option_{k.lower()}"] = f"Option {k} is missing."
    if s.correct_answer is None:
        warn["correct_answer"] = "Answer not verified (allowed, but review before use in tests)."
    elif s.correct_answer not in opts:
        err["correct_answer"] = "Answer must be A, B, C or D."
    elif not opts[s.correct_answer].strip():
        err["correct_answer"] = f"Answer points to empty option {s.correct_answer}."
    if s.language not in Language.values:
        err["language"] = "Unsupported language."
    if s.difficulty_level and s.difficulty_level not in Difficulty.values:
        err["difficulty_level"] = "Must be Easy, Medium or Hard."
    for t in s.previous_year_tags or []:
        y = t.get("year")
        if not isinstance(y, int) or not 1900 <= y <= 2100 or not str(t.get("exam", "")).strip():
            err["previous_year_tags"] = f"Invalid exam/year tag: {t}"
            break
    if not s.previous_year_tags:
        warn["previous_year_tags"] = "No previous-year tag."
    if not err:
        h = staged_hash(s)
        dup = Question.objects.filter(content_hash=h).first()
        if dup:
            warn["question_text"] = f"Duplicate of existing question #{dup.pk}; will be skipped on import."
        elif type(s).objects.filter(document=s.document, id__lt=s.id or 0).exclude(pk=s.pk).filter(
                question_text=s.question_text, option_a=s.option_a).exists():
            warn["question_text"] = "Possible duplicate within this document."
    return err, warn
