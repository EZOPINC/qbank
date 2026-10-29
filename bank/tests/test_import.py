from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from bank.importer import import_staged
from bank.models import ExamCategory, Question, ReviewStatus, SourceDocument, StagedQuestion
from bank.validators import validate_staged


def make_doc(name="p.pdf", sha="a" * 64):
    return SourceDocument.objects.create(file="papers/x.pdf", original_name=name, sha256=sha, size=1)


def make_staged(doc, **kw):
    d = dict(document=doc, source_question_number=1, question_text="Capital of Bengal?", option_a="Kolkata",
             option_b="Dhaka", option_c="Patna", option_d="Delhi", correct_answer="A",
             previous_year_tags=[{"exam": "WBCS", "year": 2022}], review_status=ReviewStatus.APPROVED)
    d.update(kw)
    return StagedQuestion.objects.create(**d)


class ValidatorTests(TestCase):
    def test_errors_and_warnings(self):
        s = make_staged(make_doc(), option_b="", correct_answer="B")
        err, _ = validate_staged(s)
        self.assertIn("option_b", err)
        self.assertIn("correct_answer", err)

    def test_null_answer_is_warning_only(self):
        err, warn = validate_staged(
            make_staged(make_doc(), correct_answer=None))
        self.assertFalse(err)
        self.assertIn("correct_answer", warn)

    def test_bad_year(self):
        err, _ = validate_staged(make_staged(
            make_doc(), previous_year_tags=[{"exam": "X", "year": 20}]))
        self.assertIn("previous_year_tags", err)


class ImportTests(TestCase):
    def test_import_creates_normalized_records_and_is_idempotent(self):
        doc = make_doc()
        s = make_staged(doc)
        s.exam_categories.add(ExamCategory.objects.create(name="WBCS"))
        b = import_staged([s.pk])
        self.assertEqual(b.succeeded, 1)
        q = Question.objects.get()
        self.assertEqual(q.previous_year_tags.get().year, 2022)
        self.assertEqual(
            list(q.exam_categories.values_list("name", flat=True)), ["WBCS"])
        b2 = import_staged([s.pk])
        self.assertEqual((b2.succeeded, b2.skipped), (0, 1))
        self.assertEqual(Question.objects.count(), 1)

    def test_duplicate_content_skipped_and_invalid_not_imported(self):
        doc = make_doc()
        a, dup = make_staged(doc), make_staged(doc, source_question_number=2)
        bad = make_staged(doc, source_question_number=3,
                          question_text="Other?", option_a="")
        b = import_staged([a.pk, dup.pk, bad.pk])
        self.assertEqual((b.succeeded, b.skipped, b.failed), (1, 1, 1))
        self.assertEqual(Question.objects.count(), 1)

    def test_unapproved_rows_not_imported(self):
        s = make_staged(make_doc(), review_status=ReviewStatus.DRAFT)
        self.assertEqual(import_staged([s.pk]).succeeded, 0)
        self.assertEqual(Question.objects.count(), 0)

    def test_unicode_roundtrip(self):
        s = make_staged(make_doc(), question_text="ভারতের রাজধানী কোথায়?",
                        option_a="নয়াদিল্লি", language="bn")
        import_staged([s.pk])
        self.assertEqual(Question.objects.get().language, "bn")


@override_settings(PRIVATE_MEDIA_ROOT="/tmp/qbank_test_media")
class ViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("u", password="p")
        self.client.login(username="u", password="p")

    def test_login_required(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse("upload")).status_code, 302)

    def test_rejects_wrong_type_and_spoofed_content(self):
        for name, body in (("x.exe", b"MZ"), ("x.pdf", b"not a pdf")):
            r = self.client.post(reverse("upload"), {
                                 "file": SimpleUploadedFile(name, body)})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(SourceDocument.objects.count(), 0)

    def test_upload_queues_processing(self):
        with patch("bank.views.process_document.delay") as m:
            r = self.client.post(reverse("upload"), {
                                 "file": SimpleUploadedFile("a.pdf", b"%PDF-1.4 test")})
        self.assertEqual(r.status_code, 302)
        m.assert_called_once()

    def test_edit_revalidates_and_bulk_approve_blocks_errors(self):
        doc = make_doc()
        s = make_staged(doc, review_status=ReviewStatus.DRAFT, option_c="")
        self.client.post(reverse("document", args=[doc.pk]), {
                         "action": "approve", "sel": [s.pk]})
        s.refresh_from_db()
        self.assertEqual(s.review_status, ReviewStatus.NEEDS_REVIEW)
