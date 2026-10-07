from rest_framework import serializers

from .models import Candidate
from .scoring import GIT_RE, SKILLS, compute_score, priority


class CandidateSerializer(serializers.ModelSerializer):
    competences = serializers.ListField(child=serializers.ChoiceField(choices=SKILLS), required=False, allow_empty=True)
    priorite = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ["id", "nom", "email", "niveau", "experience", "projets", "github", "disponibilite",
                  "competences", "motivation", "score", "detail", "priorite", "created_at"]
        read_only_fields = ["score", "detail", "created_at"]

    def get_priorite(self, obj):
        return priority(obj.score)

    def validate_nom(self, v):
        v = v.strip()
        if len(v) < 2:
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return v

    def validate_email(self, v):
        v = v.strip().lower()
        if Candidate.objects.filter(email__iexact=v).exists():
            raise serializers.ValidationError("Cet email est déjà enregistré.")
        return v

    def validate_github(self, v):
        v = v.strip()
        if v and not GIT_RE.match(v):
            raise serializers.ValidationError("Lien GitHub/GitLab invalide (https://github.com/...).")
        return v

    def create(self, validated):
        validated["score"], validated["detail"] = compute_score(validated)
        return super().create(validated)
