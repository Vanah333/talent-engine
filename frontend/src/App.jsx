import { useEffect, useState } from "react";
import { createCandidate, deleteCandidate, listCandidates } from "./api.js";
 
const SKILLS = ["JavaScript", "Python", "SQL", "HTML/CSS", "Git", "API REST", "React", "Node.js", "Data/IA"];
const EMPTY = { nom: "", email: "", niveau: 0, experience: 0, projets: 0, github: "",
  disponibilite: "full", competences: [], motivation: "" };
const PRIORITE = { prioritaire: "À examiner en priorité", a_examiner: "À examiner", faible: "Faible" };
const DETAIL = { competences: "Compétences", experience: "Expérience", projets: "Projets",
  motivation: "Motivation", disponibilite: "Disponibilité", formation: "Formation" };
 
export default function App() {
  const [list, setList] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
 
  const refresh = () =>
    listCandidates().then(setList).catch((e) => setError(e.message)).finally(() => setLoading(false));
  useEffect(() => { refresh(); }, []);
 
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  const num = (k) => (e) => setForm({ ...form, [k]: Number(e.target.value) });
  const toggle = (s) =>
    setForm({ ...form, competences: form.competences.includes(s)
      ? form.competences.filter((x) => x !== s) : [...form.competences, s] });
 
  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      await createCandidate(form);
      setForm(EMPTY);
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }
 
  async function remove(id) {
    await deleteCandidate(id).catch((e) => setError(e.message));
    refresh();
  }
 
  const count = (p) => list.filter((c) => c.priorite === p).length;
  const shown = list.filter((c) => filter === "all" || c.priorite === filter);
 
  return (
    <>
      <header className="hero">
        <div className="hero-in">
          <h1>Talent Engine</h1>
          <p>Chaque candidature est qualifiée, notée sur 100 et classée pour que les meilleurs profils soient lus en premier.</p>
          <div className="stats">
            <div className="stat"><b>{list.length}</b><span>Candidatures</span></div>
            <div className="stat"><b>{count("prioritaire")}</b><span>À examiner en priorité</span></div>
            <div className="stat"><b>{count("a_examiner")}</b><span>À examiner</span></div>
            <div className="stat"><b>{count("faible")}</b><span>Faibles</span></div>
          </div>
        </div>
      </header>
 
      <main>
        <section className="panel">
          <h2>Classement</h2>
          <div className="bar">
            <select className="ghost" value={filter} onChange={(e) => setFilter(e.target.value)} aria-label="Filtrer par priorité">
              <option value="all">Toutes les priorités</option>
              {Object.entries(PRIORITE).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </select>
            <a className="btn ghost" href="/api/candidates/export/">Exporter en CSV</a>
          </div>
          {loading ? <p className="empty">Chargement…</p> : shown.length === 0 ? (
            <p className="empty">Aucune candidature pour l'instant. Ajoutez la première ci-dessous.</p>
          ) : (
            <div className="scroll">
              <table>
                <thead><tr><th>Rang</th><th>Candidat</th><th>Score</th><th>Priorité</th><th>Détail des points</th><th></th></tr></thead>
                <tbody>
                  {shown.map((c, i) => (
                    <tr key={c.id} className={i === 0 ? "top" : ""}>
                      <td className="rank">{i + 1}</td>
                      <td><div className="name">{c.nom}</div><div className="sub">{c.email}</div></td>
                      <td className="score">
                        <b>{c.score}</b><i>/100</i>
                        <div className="meter"><div style={{ width: `${c.score}%` }} /></div>
                      </td>
                      <td><span className={`tier ${c.priorite}`}>{PRIORITE[c.priorite]}</span></td>
                      <td>
                        <div className="detail">
                          {Object.entries(c.detail).map(([k, v]) => (
                            <span key={k}>{DETAIL[k] || k} <b>{v}</b></span>
                          ))}
                        </div>
                      </td>
                      <td><button className="link" onClick={() => remove(c.id)}>Supprimer</button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
 
        <form onSubmit={submit} className="panel">
          <h2>Nouvelle candidature</h2>
          <div className="grid">
            <label>Nom complet<input required value={form.nom} onChange={set("nom")} /></label>
            <label>Email<input required type="email" value={form.email} onChange={set("email")} /></label>
            <label>Formation
              <select value={form.niveau} onChange={num("niveau")}>
                <option value={0}>Autodidacte</option><option value={1}>Bac</option>
                <option value={2}>Bac+2</option><option value={3}>Bac+3</option>
                <option value={5}>Bac+5 et plus</option>
              </select>
            </label>
            <label>Années d'expérience
              <input type="number" min="0" max="40" value={form.experience} onChange={num("experience")} /></label>
            <label>Projets réalisés
              <input type="number" min="0" max="50" value={form.projets} onChange={num("projets")} /></label>
            <label>Lien GitHub ou GitLab
              <input placeholder="https://github.com/..." value={form.github} onChange={set("github")} /></label>
            <label>Disponibilité au 2 novembre
              <select value={form.disponibilite} onChange={set("disponibilite")}>
                <option value="full">Totale</option><option value="part">Partielle</option>
                <option value="none">Indisponible</option>
              </select>
            </label>
          </div>
          <fieldset>
            <legend>Compétences</legend>
            <div className="chips">
              {SKILLS.map((s) => (
                <label key={s} className="chip">
                  <input type="checkbox" checked={form.competences.includes(s)} onChange={() => toggle(s)} />
                  <span>{s}</span>
                </label>
              ))}
            </div>
          </fieldset>
          <label>Motivation
            <textarea rows={3} value={form.motivation} onChange={set("motivation")} /></label>
          {error && <p className="error" role="alert">{error}</p>}
          <button type="submit">Ajouter la candidature</button>
        </form>
      </main>
    </>
  );
}
