from django.contrib import admin
from . import models
for m in (models.ExamCategory, models.SourceDocument, models.Question, models.ImportBatch):
    admin.site.register(m)
