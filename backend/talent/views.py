import csv

from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from .models import Candidate
from .scoring import priority
from .serializers import CandidateSerializer


class CandidateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    @action(detail=False, methods=["get"])
    def export(self, request):
        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = 'attachment; filename="classement.csv"'
        w = csv.writer(resp)
        w.writerow(["rang", "nom", "email", "score", "priorite"])
        for i, c in enumerate(self.get_queryset(), 1):
            # protection contre l'injection de formules CSV
            nom = f"'{c.nom}" if c.nom[:1] in "=+-@" else c.nom
            w.writerow([i, nom, c.email, c.score, priority(c.score)])
        return resp
