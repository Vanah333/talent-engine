from django.contrib import admin
from django.urls import path, include
from candidates.views import dashboard, candidate_create, candidate_detail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("candidature/", candidate_create, name="candidate_create"),
    path("candidat/<int:pk>/", candidate_detail, name="candidate_detail"),
    path("api/", include("candidates.api_urls")),
]
