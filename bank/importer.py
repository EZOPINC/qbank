import logging
from django.db import transaction
from .models import ImportBatch, PreviousYearRef, Question, ReviewStatus, StagedQuestion
from .validators import staged_hash, validate_staged

log = logging.getLogger(__name__)


def import_staged(ids, user=None):
    """Import approved rows in one transaction; each row in a savepoint so one bad row can't sink the batch."""
    batch = ImportBatch.objects.create(created_by=user)
    report = []
    with transaction.atomic():
        rows = (StagedQuestion.objects.select_for_update()
                .filter(pk__in=ids, review_status=ReviewStatus.APPROVED, imported_question__isnull=True))
        found = set()
        for s in rows:
            found.add(s.pk)
            row = {"staged_id": s.pk, "number": s.source_question_number}
            errors, _ = validate_staged(s)
            if errors:
                batch.failed += 1; report.append({**row, "outcome": "failed", "reason": str(errors)}); continue
            h = staged_hash(s)
            existing = Question.objects.filter(content_hash=h).first()
            if existing:
                s.imported_question, s.review_status = existing, ReviewStatus.IMPORTED
                s.save(update_fields=["imported_question", "review_status"])
                batch.skipped += 1; report.append({**row, "outcome": "skipped", "reason": f"duplicate of #{existing.pk}"}); continue
            try:
                with transaction.atomic():
                    q = Question.objects.create(
                        question_text=s.question_text, option_a=s.option_a, option_b=s.option_b,
                        option_c=s.option_c, option_d=s.option_d, correct_answer=s.correct_answer,
                        explanation=s.explanation, difficulty_level=s.difficulty_level, language=s.language,
                        source_document=s.document, source_question_number=s.source_question_number,
                        content_hash=h, review_status=ReviewStatus.IMPORTED, created_by=user, reviewed_by=user)
                    q.exam_categories.set(s.exam_categories.all())
                    PreviousYearRef.objects.bulk_create(
                        [PreviousYearRef(question=q, exam_name=t["exam"], year=t["year"]) for t in s.previous_year_tags],
                        ignore_conflicts=True)
                s.imported_question, s.review_status = q, ReviewStatus.IMPORTED
                s.save(update_fields=["imported_question", "review_status"])
                batch.succeeded += 1; report.append({**row, "outcome": "imported", "reason": ""})
            except Exception as exc:  # noqa: BLE001
                log.exception("import_failed staged=%s", s.pk)
                batch.failed += 1; report.append({**row, "outcome": "failed", "reason": str(exc)})
        for pk in set(ids) - found:
            batch.skipped += 1
            report.append({"staged_id": pk, "number": None, "outcome": "skipped", "reason": "not approved or already imported"})
        batch.report = report
        batch.save()
    log.info("import_done batch=%s ok=%s skipped=%s failed=%s", batch.pk, batch.succeeded, batch.skipped, batch.failed)
    return batch
