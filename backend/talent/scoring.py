"""Logique de qualification : fonction pure, sans accès base -> facile à tester."""
import re

SKILLS = ["JavaScript", "Python", "SQL", "HTML/CSS", "Git", "API REST", "React", "Node.js", "Data/IA"]
KEYWORDS = ["apprendre", "équipe", "equipe", "projet", "contribuer", "curieux", "évoluer", "collaborer"]
GIT_RE = re.compile(r"^https://(www\.)?(github|gitlab)\.com/[\w.-]+", re.I)

WEIGHTS = {"competences": 35, "experience": 15, "projets": 20, "motivation": 15, "disponibilite": 10, "formation": 5}
THRESHOLD_PRIORITY, THRESHOLD_REVIEW = 70, 45


def compute_score(c):
    """c : dict avec competences, experience, projets, github, motivation, disponibilite, niveau."""
    skills = len(set(c.get("competences") or []))
    comp = 35 * min(1, skills / 5)
    exp = 15 * min(c.get("experience") or 0, 3) / 3
    proj = 10 * min(c.get("projets") or 0, 3) / 3 + (10 if GIT_RE.match(c.get("github") or "") else 0)
    text = (c.get("motivation") or "").lower()
    words = len(text.split())
    kw = sum(1 for k in KEYWORDS if k in text)
    mot = (8 if words >= 40 else 4 if words >= 20 else 0) + min(7, kw * 2)
    dispo = {"full": 10, "part": 5}.get(c.get("disponibilite"), 0)
    form = min(5, c.get("niveau") or 0)
    detail = {
        "competences": round(comp), "experience": round(exp), "projets": round(proj),
        "motivation": round(mot), "disponibilite": dispo, "formation": form,
    }
    return min(100, sum(detail.values())), detail


def priority(score):
    if score >= THRESHOLD_PRIORITY:
        return "prioritaire"
    return "a_examiner" if score >= THRESHOLD_REVIEW else "faible"
