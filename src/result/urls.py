from django.urls import path
from .views import ResultAPI, ResultDetailAPI, ResultResponseAPI

urlpatterns = [
    path('registrations/', ResultAPI.as_view(), name="results"),
    path('registrations/<int:id>', ResultDetailAPI.as_view(), name="results-detail"),
    path('registrations/<int:id>/responses/', ResultResponseAPI.as_view(), name="results-responses"),
]