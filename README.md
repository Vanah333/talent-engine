# Talent Engine (Django + React)

Candidatures -> validation -> score /100 -> classement -> priorités.

## Lancer le backend
    cd backend
    python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py makemigrations talent
    python manage.py migrate
    python manage.py test            # tests unitaires + API
    python manage.py runserver       # http://localhost:8000/api/candidates/

## Lancer le frontend
    cd frontend
    npm install
    npm run dev                      # http://localhost:5173 (proxy /api -> :8000)

## API
- POST   /api/candidates/         créer (score calculé côté serveur)
- GET    /api/candidates/         liste classée (score desc, projets desc, ancienneté)
- GET    /api/candidates/{id}/    détail
- DELETE /api/candidates/{id}/    supprimer
- GET    /api/candidates/export/  CSV

## Scoring (100 pts) – voir backend/talent/scoring.py
Compétences 35 · Expérience 15 · Projets+dépôt 20 · Motivation 15 · Disponibilité 10 · Formation 5
Priorité : >=70 prioritaire, 45-69 à examiner, <45 faible.

## Choix et limites
- Scoring à règles, explicable, sans IA : chaque point est traçable (champ `detail`).
- Le score est calculé côté serveur uniquement (le client ne peut pas le falsifier).
- Limites : mots-clés simples, pas d'analyse de CV, pondérations à calibrer avec des données réelles.
- Évolutions : auth recruteur, pagination, PostgreSQL, upload CV, revue humaine obligatoire des décisions.
