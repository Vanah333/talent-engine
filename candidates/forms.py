from django import forms
from .models import Candidate
from .scoring import SKILL_POINTS, calculate_score

class CandidateForm(forms.ModelForm):
    available_skills = forms.MultipleChoiceField(
        label="Compétences techniques",
        choices=[(key, key) for key in SKILL_POINTS.keys()],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Candidate
        fields = [
            "first_name", "last_name", "email", "phone", "city",
            "education_level", "years_experience", "projects_count",
            "teamwork", "motivation"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Sarah"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Rakoto"}),
            "email": forms.EmailInput(attrs={"placeholder": "sarah@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+261 34 00 000 00"}),
            "city": forms.TextInput(attrs={"placeholder": "Antananarivo"}),
            "years_experience": forms.NumberInput(attrs={"min": 0, "max": 50}),
            "projects_count": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "motivation": forms.Textarea(attrs={"rows": 6, "placeholder": "Expliquez votre motivation..."})
        }

    def clean_years_experience(self):
        value = self.cleaned_data["years_experience"]
        if value > 50:
            raise forms.ValidationError("L'expérience doit être inférieure ou égale à 50 ans.")
        return value

    def save(self, commit=True):
        candidate = super().save(commit=False)
        skills = self.cleaned_data.get("available_skills", [])
        total, status, breakdown = calculate_score(
            candidate.education_level,
            candidate.years_experience,
            skills,
            candidate.projects_count,
            candidate.teamwork,
            candidate.motivation,
        )
        candidate.skills = skills
        candidate.score = total
        candidate.status = status
        candidate.score_breakdown = breakdown
        if commit:
            candidate.save()
        return candidate
