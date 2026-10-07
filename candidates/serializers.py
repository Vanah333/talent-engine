from rest_framework import serializers
from .models import Candidate
from .scoring import calculate_score, SKILL_POINTS

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id", "first_name", "last_name", "email", "phone", "city",
            "education_level", "years_experience", "skills",
            "projects_count", "teamwork", "motivation",
            "score", "status", "score_breakdown", "created_at"
        ]
        read_only_fields = ["score", "status", "score_breakdown", "created_at"]

    def validate_years_experience(self, value):
        if value < 0 or value > 50:
            raise serializers.ValidationError("Les années d'expérience doivent être comprises entre 0 et 50.")
        return value

    def validate_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("skills doit être une liste.")
        unknown = [skill for skill in value if skill not in SKILL_POINTS]
        if unknown:
            raise serializers.ValidationError(f"Compétence(s) inconnue(s) : {', '.join(unknown)}")
        return list(dict.fromkeys(value))

    def create(self, validated_data):
        total, status, breakdown = calculate_score(
            validated_data["education_level"],
            validated_data.get("years_experience", 0),
            validated_data.get("skills", []),
            validated_data.get("projects_count", 0),
            validated_data.get("teamwork", False),
            validated_data.get("motivation", ""),
        )
        validated_data.update(score=total, status=status, score_breakdown=breakdown)
        return Candidate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        total, status, breakdown = calculate_score(
            instance.education_level,
            instance.years_experience,
            instance.skills,
            instance.projects_count,
            instance.teamwork,
            instance.motivation,
        )
        instance.score = total
        instance.status = status
        instance.score_breakdown = breakdown
        instance.save()
        return instance
