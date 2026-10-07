EDUCATION_POINTS = {
    "BAC": 5,
    "BAC2": 8,
    "LICENCE": 12,
    "MASTER": 15,
    "DOCTORAT": 15,
}

SKILL_POINTS = {
    "Python": 5,
    "Django": 5,
    "React": 5,
    "SQL": 5,
    "Git": 3,
    "Docker": 3,
    "IA": 2,
    "Cybersécurité": 2,
}

MAX_SKILL_SCORE = 30

def normalize_skills(skills):
    return list(dict.fromkeys(str(skill).strip() for skill in skills if str(skill).strip()))

def score_experience(years):
    years = max(0, int(years))
    if years >= 3:
        return 20
    if years == 2:
        return 15
    if years == 1:
        return 10
    return 5 if years == 0 else 5

def score_projects(count):
    count = max(0, int(count))
    if count >= 3:
        return 15
    if count == 2:
        return 10
    if count == 1:
        return 5
    return 0

def score_motivation(text):
    length = len((text or "").strip())
    if length >= 250:
        return 10
    if length >= 150:
        return 8
    if length >= 80:
        return 6
    if length >= 30:
        return 4
    return 2

def calculate_score(education_level, years_experience, skills, projects_count, teamwork, motivation):
    skills = normalize_skills(skills)
    education = EDUCATION_POINTS.get(education_level, 0)
    experience = score_experience(years_experience)
    skill_score = min(MAX_SKILL_SCORE, sum(SKILL_POINTS.get(skill, 0) for skill in skills))
    projects = score_projects(projects_count)
    team = 10 if teamwork else 0
    motivation_score = score_motivation(motivation)

    breakdown = {
        "Formation": education,
        "Expérience": experience,
        "Compétences": skill_score,
        "Projets": projects,
        "Travail en équipe": team,
        "Motivation": motivation_score,
    }
    total = min(100, sum(breakdown.values()))

    if total >= 75:
        status = "PRIORITY"
    elif total >= 50:
        status = "PENDING"
    else:
        status = "LOW"

    return total, status, breakdown
