from django.db import models

class Candidate(models.Model):
    LEVEL_CHOICES = [
        ("BAC", "Baccalauréat"),
        ("BAC2", "Bac+2"),
        ("LICENCE", "Licence"),
        ("MASTER", "Master"),
        ("DOCTORAT", "Doctorat"),
    ]

    STATUS_CHOICES = [
        ("PRIORITY", "Prioritaire"),
        ("PENDING", "À examiner"),
        ("LOW", "Faible priorité"),
    ]

    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Téléphone", max_length=30, blank=True)
    city = models.CharField("Ville", max_length=100, blank=True)
    education_level = models.CharField("Niveau d'études", max_length=20, choices=LEVEL_CHOICES)
    years_experience = models.PositiveIntegerField("Années d'expérience", default=0)
    skills = models.JSONField("Compétences", default=list)
    projects_count = models.PositiveIntegerField("Nombre de projets", default=0)
    teamwork = models.BooleanField("Travail en équipe", default=False)
    motivation = models.TextField("Motivation")
    score = models.PositiveIntegerField("Score", default=0)
    status = models.CharField("Priorité", max_length=20, choices=STATUS_CHOICES, default="PENDING")
    score_breakdown = models.JSONField("Détail du score", default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-score", "-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.score}/100"
