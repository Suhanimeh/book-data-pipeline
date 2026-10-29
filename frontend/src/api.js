
// # Student Name: Ruvi Kathiriya

// # Student ID: ET21BTAI031

// # Course: Web Programming

// # Academic Year: Third Year B.Tech (AI & DS)

// # Semester: 6

const BASE = import.meta.env.VITE_API_URL || "";

async function request(path, { params, method = "GET" } = {}) {
  const qs = new URLSearchParams();
  Object.entries(params || {}).forEach(([k, v]) => {
    if (v !== "" && v !== null && v !== undefined) qs.append(k, v);
  });
  const url = `${BASE}${path}${qs.toString() ? `?${qs}` : ""}`;
  const res = await fetch(url, { method });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

export const api = {
  books: (params) => request("/api/books", { params }),
  categories: () => request("/api/categories"),
  stats: () => request("/api/stats"),
  runs: () => request("/api/pipeline/runs", { params: { limit: 1 } }),
  startRun: () => request("/api/pipeline/run", { method: "POST" }),
};
