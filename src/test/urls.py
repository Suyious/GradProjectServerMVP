from django.urls import path
from .views import (
    TestsAPI,
    TestDetailAPI,
    TestQuestionAPI,
    TestQuestionDetailAPI,
    TestResultAPI,
)

urlpatterns = [
    path('tests/', TestsAPI.as_view(), name="tests"),
    path('tests/<int:id>/', TestDetailAPI.as_view(), name="test-detail"),
    path('tests/<int:id>/question/', TestQuestionAPI.as_view(), name="test-questions"),
    path('tests/<int:tid>/question/<int:qid>/', TestQuestionDetailAPI.as_view(), name="test-question-detail"),
    path('tests/<int:id>/registrations/', TestResultAPI.as_view(), name="test-results")
]
