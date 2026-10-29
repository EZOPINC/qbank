import logging
from celery import shared_task
from django.db import transaction
from .extraction.extractor import extract_document
from .models import ReviewStatus, SourceDocument, StagedQuestion
from .parser import parse_pages
from .validators import validate_staged

log = logging.getLogger(__name__)


@shared_task
def process_document(doc_id):
    doc = SourceDocument.objects.get(pk=doc_id)
    doc.status, doc.error, doc.pages_done = SourceDocument.Status.PROCESSING, "", 0
    doc.save()

    def progress(done, total):
        SourceDocument.objects.filter(pk=doc.pk).update(pages_done=done, pages_total=total)

    try:
        pages = extract_document(doc.file.path, on_page=progress)
        parsed = parse_pages(pages)
        with transaction.atomic():
            doc.staged.all().delete()
            for p in parsed:
                o = p["options"]
                s = StagedQuestion(
                    document=doc, source_question_number=p["number"], page_number=p["page"],
                    question_text=p["text"], option_a=o["A"], option_b=o["B"], option_c=o["C"], option_d=o["D"],
                    correct_answer=p["answer"], language=p["language"], previous_year_tags=p["tags"],
                    confidence=p["confidence"], flags=p["flags"], original=p)
                s.save()
                errors, warnings = validate_staged(s)
                s.validation = {"errors": errors, "warnings": warnings}
                s.review_status = ReviewStatus.NEEDS_REVIEW if (errors or p["flags"]) else ReviewStatus.DRAFT
                s.save(update_fields=["validation", "review_status"])
        doc.status = SourceDocument.Status.EXTRACTED
        log.info("document_done doc=%s questions=%s", doc.pk, len(parsed))
    except Exception as exc:  # noqa: BLE001
        log.exception("document_failed doc=%s", doc.pk)
        doc.status, doc.error = SourceDocument.Status.FAILED, str(exc)
    doc.save()
