const BASE = "/api/candidates/";

export async function listCandidates() {
  const r = await fetch(BASE);
  if (!r.ok) throw new Error("Impossible de charger les candidatures.");
  return r.json();
}

export async function createCandidate(data) {
  const r = await fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) {
    // DRF renvoie {champ: [messages]}
    const msgs = Object.entries(body).map(([k, v]) => `${k} : ${[].concat(v).join(" ")}`);
    throw new Error(msgs.join(" | ") || "Erreur serveur.");
  }
  return body;
}

export async function deleteCandidate(id) {
  const r = await fetch(`${BASE}${id}/`, { method: "DELETE" });
  if (!r.ok) throw new Error("Suppression impossible.");
}
