from django.urls import path
from . import views
urlpatterns = [
    path("", views.upload, name="upload"),
    path("documents/<int:pk>/", views.document, name="document"),
    path("questions/<int:pk>/", views.staged_edit, name="staged_edit"),
    path("bank/", views.question_list, name="question_list"),
    path("history/", views.history, name="history"),
]
