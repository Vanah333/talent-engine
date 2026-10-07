from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Candidate(models.Model):
    DISPO = [("full", "Totale"), ("part", "Partielle"), ("none", "Indisponible")]
    NIVEAUX = [(0, "Autodidacte"), (1, "Bac"), (2, "Bac+2"), (3, "Bac+3"), (5, "Bac+5 et plus")]

    nom = models.CharField(max_length=120)
    email = models.EmailField(unique=True, error_messages={"unique": "Cet email est déjà enregistré."})
    niveau = models.IntegerField(choices=NIVEAUX, default=0)
    experience = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(40)])
    projets = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50)])
    github = models.CharField(max_length=200, blank=True)
    disponibilite = models.CharField(max_length=4, choices=DISPO, default="full")
    competences = models.JSONField(default=list)
    motivation = models.TextField(blank=True, max_length=3000)
    score = models.IntegerField(default=0, db_index=True)
    detail = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score", "-projets", "created_at"]

    def __str__(self):
        return f"{self.nom} ({self.score})"
