from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Candidate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100, verbose_name="Prénom")),
                ("last_name", models.CharField(max_length=100, verbose_name="Nom")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="Email")),
                ("phone", models.CharField(blank=True, max_length=30, verbose_name="Téléphone")),
                ("city", models.CharField(blank=True, max_length=100, verbose_name="Ville")),
                ("education_level", models.CharField(choices=[("BAC","Baccalauréat"),("BAC2","Bac+2"),("LICENCE","Licence"),("MASTER","Master"),("DOCTORAT","Doctorat")], max_length=20, verbose_name="Niveau d'études")),
                ("years_experience", models.PositiveIntegerField(default=0, verbose_name="Années d'expérience")),
                ("skills", models.JSONField(default=list, verbose_name="Compétences")),
                ("projects_count", models.PositiveIntegerField(default=0, verbose_name="Nombre de projets")),
                ("teamwork", models.BooleanField(default=False, verbose_name="Travail en équipe")),
                ("motivation", models.TextField(verbose_name="Motivation")),
                ("score", models.PositiveIntegerField(default=0, verbose_name="Score")),
                ("status", models.CharField(choices=[("PRIORITY","Prioritaire"),("PENDING","À examiner"),("LOW","Faible priorité")], default="PENDING", max_length=20, verbose_name="Priorité")),
                ("score_breakdown", models.JSONField(default=dict, verbose_name="Détail du score")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-score", "-created_at"]},
        ),
    ]
}