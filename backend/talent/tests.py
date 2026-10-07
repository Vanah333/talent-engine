from django.test import SimpleTestCase
from rest_framework.test import APITestCase

from .scoring import compute_score, priority

FULL = {"competences": ["JavaScript", "Python", "SQL", "Git", "React"], "experience": 5, "projets": 5,
        "github": "https://github.com/x", "disponibilite": "full", "niveau": 5,
        "motivation": "apprendre équipe projet contribuer " + "mot " * 40}
VALID = {"nom": "Aina R.", "email": "aina@ex.com", "niveau": 3, "experience": 2, "projets": 3,
         "github": "https://github.com/aina", "disponibilite": "full",
         "competences": ["Python", "SQL", "Git"], "motivation": "Je veux apprendre en équipe."}


class ScoringTests(SimpleTestCase):
    def test_perfect_is_100(self):
        self.assertEqual(compute_score(FULL)[0], 100)

    def test_empty_is_0(self):
        self.assertEqual(compute_score({"disponibilite": "none"})[0], 0)

    def test_never_above_100(self):
        self.assertLessEqual(compute_score({**FULL, "experience": 999, "projets": 999})[0], 100)

    def test_invalid_github_gives_no_points(self):
        self.assertEqual(compute_score({"github": "http://x.com"})[1]["projets"], 0)

    def test_thresholds(self):
        self.assertEqual((priority(70), priority(45), priority(44)), ("prioritaire", "a_examiner", "faible"))


class ApiTests(APITestCase):
    url = "/api/candidates/"

    def test_create_computes_score_server_side(self):
        r = self.client.post(self.url, {**VALID, "score": 99}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertNotEqual(r.data["score"], 99)

    def test_duplicate_email_rejected(self):
        self.client.post(self.url, VALID, format="json")
        r = self.client.post(self.url, {**VALID, "email": "AINA@ex.com"}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_invalid_email_and_github_rejected(self):
        self.assertEqual(self.client.post(self.url, {**VALID, "email": "abc"}, format="json").status_code, 400)
        self.assertEqual(self.client.post(self.url, {**VALID, "github": "http://x.com"}, format="json").status_code, 400)

    def test_out_of_range_rejected(self):
        self.assertEqual(self.client.post(self.url, {**VALID, "experience": -1}, format="json").status_code, 400)

    def test_unknown_skill_rejected(self):
        self.assertEqual(self.client.post(self.url, {**VALID, "competences": ["Cobol"]}, format="json").status_code, 400)

    def test_list_sorted_by_score(self):
        self.client.post(self.url, {**VALID, "email": "low@ex.com", "competences": [], "github": "", "projets": 0}, format="json")
        self.client.post(self.url, VALID, format="json")
        scores = [c["score"] for c in self.client.get(self.url).data]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_export_csv(self):
        self.client.post(self.url, VALID, format="json")
        r = self.client.get(self.url + "export/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("aina@ex.com", r.content.decode())
