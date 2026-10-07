from django.core.management.base import BaseCommand
from candidates.models import Candidate
from candidates.scoring import calculate_score

class Command(BaseCommand):
    help = "Ajoute quelques candidats de démonstration."

    def handle(self, *args, **options):
        data = [
            ("Sarah","Rakoto","sarah.demo@example.com","Antananarivo","MASTER",3,["Python","Django","React","SQL","Git","Docker"],3,True,"Je souhaite contribuer à des projets concrets, apprendre rapidement et travailler avec une équipe internationale."),
            ("Jean","Rasoanaivo","jean.demo@example.com","Toamasina","LICENCE",2,["Python","SQL","Git"],2,True,"Je veux développer mes compétences et participer à des projets utiles."),
            ("Mina","Andriamihaja","mina.demo@example.com","Fianarantsoa","BAC2",1,["JavaScript"],1,False,"Je suis motivée pour apprendre."),
        ]
        for first,last,email,city,edu,exp,skills,projects,team,motivation in data:
            if Candidate.objects.filter(email=email).exists():
                continue
            score,status,breakdown=calculate_score(edu,exp,skills,projects,team,motivation)
            Candidate.objects.create(first_name=first,last_name=last,email=email,city=city,education_level=edu,years_experience=exp,skills=skills,projects_count=projects,teamwork=team,motivation=motivation,score=score,status=status,score_breakdown=breakdown)
        self.stdout.write(self.style.SUCCESS("Données de démonstration ajoutées."))
