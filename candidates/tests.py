from django.test import TestCase
from .models import Candidate
from .scoring import calculate_score

class ScoringTests(TestCase):
    def test_maximum_profile(self):
        score, status, breakdown = calculate_score(
            "MASTER", 3,
            ["Python", "Django", "React", "SQL", "Git", "Docker", "IA", "Cybersécurité"],
            3, True,
            "Je suis très motivé pour apprendre, contribuer et travailler en équipe sur des projets concrets."
        )
        self.assertEqual(score, 100)
        self.assertEqual(status, "PRIORITY")
        self.assertEqual(sum(breakdown.values()), 100)

    def test_low_profile(self):
        score, status, breakdown = calculate_score(
            "BAC", 0, [], 0, False, "Oui"
        )
        self.assertLess(score, 50)
        self.assertEqual(status, "LOW")

class CandidateModelTests(TestCase):
    def test_candidate_creation(self):
        candidate = Candidate.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            education_level="LICENCE",
            years_experience=1,
            skills=["Python"],
            projects_count=1,
            teamwork=True,
            motivation="Je souhaite apprendre et contribuer à des projets concrets.",
            score=0,
            status="PENDING",
        )
        self.assertEqual(str(candidate), "Test User — 0/100")
