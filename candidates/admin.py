from django.contrib import admin
from .models import Candidate

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "education_level", "score", "status", "created_at")
    list_filter = ("education_level", "status", "teamwork")
    search_fields = ("first_name", "last_name", "email", "city")
    ordering = ("-score",)
