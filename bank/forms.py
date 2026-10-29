import hashlib
import re
from django import forms
from django.conf import settings
from .models import SourceDocument, StagedQuestion

MAGIC = {"pdf": (b"%PDF",), "png": (b"\x89PNG",), "jpg": (b"\xff\xd8\xff",), "jpeg": (b"\xff\xd8\xff",)}


class UploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        f = self.cleaned_data["file"]
        ext = f.name.rsplit(".", 1)[-1].lower() if "." in f.name else ""
        if ext not in MAGIC:
            raise forms.ValidationError("Only PDF, JPG, JPEG and PNG files are allowed.")
        if f.size > settings.MAX_UPLOAD_MB * 1024 * 1024:
            raise forms.ValidationError(f"File exceeds {settings.MAX_UPLOAD_MB} MB.")
        head = f.read(8); f.seek(0)
        if not head.startswith(MAGIC[ext]):
            raise forms.ValidationError("File content does not match its extension.")
        h = hashlib.sha256()
        for chunk in f.chunks():
            h.update(chunk)
        f.seek(0)
        f.sha256 = h.hexdigest()
        if SourceDocument.objects.filter(sha256=f.sha256).exists():
            raise forms.ValidationError("This exact file was already uploaded.")
        return f


class StagedForm(forms.ModelForm):
    tags_text = forms.CharField(required=False, label="Previous-year tags",
                                help_text="Separate with ';'  e.g.  UPPCS (Pre) 2014; WBCS 2022")
    correct_answer = forms.ChoiceField(required=False, choices=[("", "— not verified —")] + [(c, c) for c in "ABCD"])

    class Meta:
        model = StagedQuestion
        fields = ["question_text", "option_a", "option_b", "option_c", "option_d", "correct_answer",
                  "explanation", "difficulty_level", "language", "exam_categories"]
        widgets = {"question_text": forms.Textarea(attrs={"rows": 4}), "explanation": forms.Textarea(attrs={"rows": 4}),
                   "exam_categories": forms.CheckboxSelectMultiple}

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.fields["difficulty_level"].required = False
        if self.instance.pk:
            self.fields["tags_text"].initial = "; ".join(f'{t["exam"]} {t["year"]}' for t in self.instance.previous_year_tags)

    def clean_correct_answer(self):
        return self.cleaned_data["correct_answer"] or None

    def clean_tags_text(self):
        tags = []
        for part in filter(None, (p.strip() for p in self.cleaned_data["tags_text"].split(";"))):
            m = re.match(r"^(.+?)\s+(\d{4})$", part)
            if not m:
                raise forms.ValidationError(f"Cannot read tag '{part}'. Use 'EXAM YEAR'.")
            tags.append({"exam": m.group(1), "year": int(m.group(2))})
        return tags

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.previous_year_tags = self.cleaned_data["tags_text"]
        if commit:
            obj.save(); self.save_m2m()
        return obj
