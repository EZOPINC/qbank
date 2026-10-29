import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

private_storage = FileSystemStorage(location=str(settings.PRIVATE_MEDIA_ROOT))


def upload_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1].lower()
    # never trust user-supplied names
    return f"papers/{uuid.uuid4().hex}.{ext}"


class ReviewStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    NEEDS_REVIEW = "needs_review", "Needs Review"
    APPROVED = "approved", "Approved"
    IMPORTED = "imported", "Imported"


class Language(models.TextChoices):
    EN = "en", "English"
    HI = "hi", "Hindi"
    BN = "bn", "Bengali"


class Difficulty(models.TextChoices):
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"


class ExamCategory(models.Model):
    # WBCS, PSC, Clerkship, SSC ...
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "exam categories"

    def __str__(self):
        return self.name


class SourceDocument(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded"
        PROCESSING = "processing"
        EXTRACTED = "extracted"
        FAILED = "failed"

    file = models.FileField(storage=private_storage, upload_to=upload_path)
    original_name = models.CharField(max_length=255)
    # blocks accidental re-upload
    sha256 = models.CharField(max_length=64, unique=True)
    size = models.PositiveBigIntegerField()
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.UPLOADED)
    pages_total = models.PositiveIntegerField(default=0)
    pages_done = models.PositiveIntegerField(default=0)
    error = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name


class Question(models.Model):
    """Exam-independent canonical question; reused by exams / mock tests via other tables."""
    question_text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_answer = models.CharField(max_length=1, null=True, blank=True,
                                      choices=[(c, c) for c in "ABCD"])
    explanation = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=6, choices=Difficulty.choices, blank=True)
    exam_categories = models.ManyToManyField(
        ExamCategory, blank=True, related_name="questions")
    language = models.CharField(
        max_length=2, choices=Language.choices, default=Language.EN)
    source_document = models.ForeignKey(
        SourceDocument, null=True, blank=True, on_delete=models.SET_NULL)
    source_question_number = models.PositiveIntegerField(null=True, blank=True)
    content_hash = models.CharField(
        max_length=64, unique=True)   # duplicate guard
    review_status = models.CharField(
        max_length=12, choices=ReviewStatus.choices, default=ReviewStatus.IMPORTED)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def options(self):
        return [("A", self.option_a), ("B", self.option_b), ("C", self.option_c), ("D", self.option_d)]

    def __str__(self):
        return self.question_text[:60]


class PreviousYearRef(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="previous_year_tags")
    exam_name = models.CharField(max_length=120)
    year = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["question", "exam_name", "year"], name="uniq_question_exam_year")]

    def __str__(self):
        return f"{self.exam_name} {self.year}"


class ImportBatch(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    succeeded = models.PositiveIntegerField(default=0)
    skipped = models.PositiveIntegerField(default=0)
    failed = models.PositiveIntegerField(default=0)
    # [{staged_id, number, outcome, reason}]
    report = models.JSONField(default=list)

    class Meta:
        ordering = ["-created_at"]


class StagedQuestion(models.Model):
    """Editable extraction result. `original` keeps the untouched extraction for comparison."""
    document = models.ForeignKey(
        SourceDocument, on_delete=models.CASCADE, related_name="staged")
    source_question_number = models.PositiveIntegerField(null=True, blank=True)
    page_number = models.PositiveIntegerField(null=True, blank=True)
    question_text = models.TextField(blank=True)
    option_a = models.TextField(blank=True)
    option_b = models.TextField(blank=True)
    option_c = models.TextField(blank=True)
    option_d = models.TextField(blank=True)
    correct_answer = models.CharField(
        max_length=1, null=True, blank=True, choices=[(c, c) for c in "ABCD"])
    explanation = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=6, choices=Difficulty.choices, blank=True)
    language = models.CharField(
        max_length=2, choices=Language.choices, default=Language.EN)
    exam_categories = models.ManyToManyField(ExamCategory, blank=True)
    # [{"exam": "UPPCS (Pre)", "year": 2014}]
    previous_year_tags = models.JSONField(default=list)
    review_status = models.CharField(
        max_length=12, choices=ReviewStatus.choices, default=ReviewStatus.DRAFT)
    confidence = models.FloatField(null=True, blank=True)
    flags = models.JSONField(default=list)
    # {"errors": {...}, "warnings": {...}}
    validation = models.JSONField(default=dict)
    original = models.JSONField(default=dict)
    imported_question = models.ForeignKey(
        Question, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["document_id", "id"]
