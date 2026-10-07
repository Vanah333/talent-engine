from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CandidateForm
from .models import Candidate

def dashboard(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    candidates = Candidate.objects.all()
    if query:
        candidates = candidates.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(city__icontains=query)
        )
    if status:
        candidates = candidates.filter(status=status)

    all_candidates = Candidate.objects.all()
    context = {
        "candidates": candidates[:100],
        "total": all_candidates.count(),
        "priority": all_candidates.filter(status="PRIORITY").count(),
        "pending": all_candidates.filter(status="PENDING").count(),
        "low": all_candidates.filter(status="LOW").count(),
        "average": round(sum(c.score for c in all_candidates) / all_candidates.count(), 1) if all_candidates.exists() else 0,
        "query": query,
        "status_filter": status,
    }
    return render(request, "dashboard.html", context)

def candidate_create(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f"Candidature enregistrée. Score : {candidate.score}/100.")
            return redirect("candidate_detail", pk=candidate.pk)
    else:
        form = CandidateForm()
    return render(request, "candidate_form.html", {"form": form})

def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    return render(request, "candidate_detail.html", {"candidate": candidate})
