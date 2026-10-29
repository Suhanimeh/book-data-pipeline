//   Student Name: Suhani Mehta
//  Student ID: ET21BTAI042
//  Course: Web Programming
//  Program: Third Year B.Tech (AI & DS)
//  Semester: 6
//  Group: 15 
import { useCallback, useEffect, useState } from "react";
import { api } from "./api";
import Filters from "./components/Filters.jsx";
import BookTable from "./components/BookTable.jsx";
import Trends from "./components/Trends.jsx";
import PipelineStatus from "./components/PipelineStatus.jsx";

const DEFAULT_FILTERS = {
  search: "", category: "", rating: "", in_stock: "",
  min_price: "", max_price: "", sort_by: "title", order: "asc", page: 1,
};

export default function App() {
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [data, setData] = useState({ items: [], total: 0, pages: 1 });
  const [stats, setStats] = useState(null);
  const [categories, setCategories] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const loadOverview = useCallback(async () => {
    try {
      const [s, c] = await Promise.all([api.stats(), api.categories()]);
      setStats(s);
      setCategories(c);
    } catch (e) {
      setError(e.message);
    }
  }, []);

  useEffect(() => { loadOverview(); }, [loadOverview]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    const t = setTimeout(async () => {          // debounce typing in the search box
      try {
        const res = await api.books({ ...filters, page_size: 15 });
        if (!cancelled) { setData(res); setError(""); }
      } catch (e) {
        if (!cancelled) setError(e.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }, 250);
    return () => { cancelled = true; clearTimeout(t); };
  }, [filters]);

  const update = (patch) => setFilters((f) => ({ ...f, page: 1, ...patch }));
  const refreshAll = () => { loadOverview(); setFilters((f) => ({ ...f })); };

  return (
    <div className="app">
      <header className="masthead">
        <div>
          <h1>Book Market Explorer</h1>
          <p>Prices, ratings and stock scraped from books.toscrape.com, cleaned and stored in PostgreSQL.</p>
        </div>
        <PipelineStatus onFinished={refreshAll} lastUpdated={stats?.last_updated} />
      </header>

      {error && <div className="banner" role="alert">{error}</div>}

      {stats && stats.total_books === 0 ? (
        <div className="empty">
          <h2>No data collected yet</h2>
          <p>Select “Collect data” to scrape the catalogue. The first run takes about a minute.</p>
        </div>
      ) : (
        <>
          <Trends stats={stats} />
          <main className="explorer">
            <Filters filters={filters} categories={categories} onChange={update}
                     onReset={() => setFilters(DEFAULT_FILTERS)} />
            <BookTable data={data} filters={filters} loading={loading}
                       onSort={update} onPage={(page) => setFilters((f) => ({ ...f, page }))} />
          </main>
        </>
      )}
    </div>
  );
}
