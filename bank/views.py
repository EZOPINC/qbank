from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import StagedForm, UploadForm
from .importer import import_staged
from .models import ExamCategory, ImportBatch, Language, Question, ReviewStatus, SourceDocument, StagedQuestion
from .tasks import process_document
from .validators import validate_staged


@login_required
@require_http_methods(["GET", "POST"])
def upload(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        f = form.cleaned_data["file"]
        doc = SourceDocument.objects.create(file=f, original_name=f.name[:255], sha256=f.sha256,
                                            size=f.size, uploaded_by=request.user)
        process_document.delay(doc.pk)
        return redirect("document", pk=doc.pk)
    return render(request, "bank/upload.html", {"form": form, "documents": SourceDocument.objects.all()[:20]})


def _revalidate(s):
    errors, warnings = validate_staged(s)
    s.validation = {"errors": errors, "warnings": warnings}
    return errors


@login_required
@require_http_methods(["GET", "POST"])
def document(request, pk):
    doc = get_object_or_404(SourceDocument, pk=pk)
    if request.method == "POST":
        qs = doc.staged.filter(pk__in=request.POST.getlist("sel"))
        action = request.POST.get("action")
        if action == "approve":
            ok = bad = 0
            for s in qs.exclude(review_status=ReviewStatus.IMPORTED):
                if _revalidate(s):
                    bad += 1
                    s.review_status = ReviewStatus.NEEDS_REVIEW
                else:
                    ok += 1
                    s.review_status = ReviewStatus.APPROVED
                s.save()
            messages.info(
                request, f"Approved {ok}; {bad} blocked by validation errors.")
        elif action == "import":
            b = import_staged(
                list(qs.values_list("pk", flat=True)), request.user)
            messages.success(
                request, f"Import #{b.pk}: {b.succeeded} imported, {b.skipped} skipped, {b.failed} failed.")
            return redirect("history")
        return redirect("document", pk=pk)
    flt = request.GET.get("status")
    rows = doc.staged.all()
    if flt:
        rows = rows.filter(review_status=flt)
    page = Paginator(rows, 25).get_page(request.GET.get("page"))
    return render(request, "bank/document.html", {"doc": doc, "page": page, "statuses": ReviewStatus.choices, "flt": flt})


@login_required
@require_http_methods(["GET", "POST"])
def staged_edit(request, pk):
    s = get_object_or_404(StagedQuestion, pk=pk)
    form = StagedForm(request.POST or None, instance=s)
    if request.method == "POST" and form.is_valid() and s.review_status != ReviewStatus.IMPORTED:
        s = form.save()
        errors = _revalidate(s)
        s.review_status = ReviewStatus.NEEDS_REVIEW if errors else ReviewStatus.DRAFT
        s.save()
        messages.success(
            request, "Saved." if not errors else "Saved with validation errors.")
        return redirect("staged_edit", pk=pk)
    return render(request, "bank/edit.html", {"form": form, "s": s})


@login_required
def history(request):
    return render(request, "bank/history.html", {"batches": ImportBatch.objects.all()[:50]})


@login_required
def question_list(request):
    """Browse every question stored in the bank (independent of any exam)."""
    g = request.GET
    qs = Question.objects.prefetch_related(
        "previous_year_tags", "exam_categories")
    if g.get("q"):
        qs = qs.filter(question_text__icontains=g["q"])
    if g.get("language"):
        qs = qs.filter(language=g["language"])
    if g.get("status"):
        qs = qs.filter(review_status=g["status"])
    if g.get("exam"):
        qs = qs.filter(exam_categories__pk=g["exam"])
    if g.get("year", "").isdigit():
        qs = qs.filter(previous_year_tags__year=int(g["year"]))
    if g.get("answer") == "missing":
        qs = qs.filter(correct_answer__isnull=True)
    elif g.get("answer") == "set":
        qs = qs.filter(correct_answer__isnull=False)
    qs = qs.distinct().order_by("-id")
    page = Paginator(qs, 20).get_page(g.get("page"))
    params = g.copy()
    params.pop("page", None)
    return render(request, "bank/question_list.html", {
        "page": page, "total": page.paginator.count, "f": g, "qstring": params.urlencode(),
        "languages": Language.choices, "statuses": ReviewStatus.choices, "exams": ExamCategory.objects.all()})
