
// # Student Name: Ruvi Kathiriya

// # Student ID: ET21BTAI031

// # Course: Web Programming

// # Academic Year: Third Year B.Tech (AI & DS)

// # Semester: 6
import {
  Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";

const INK = "#1b2a34";
const TEAL = "#0e6e6e";
const GOLD = "#c98a00";
const axis = { fontSize: 12, fill: "#4a5b64" };

function Figure({ title, note, children }) {
  return (
    <figure className="figure">
      <figcaption><strong>{title}</strong><span>{note}</span></figcaption>
      <div className="chart">{children}</div>
    </figure>
  );
}

export default function Trends({ stats }) {
  if (!stats) return <div className="skeleton" aria-busy="true">Loading overview…</div>;

  const topCategories = stats.by_category.slice(0, 8);

  return (
    <section aria-label="Overview and trends">
      <dl className="numbers">
        <div><dt>Books collected</dt><dd>{stats.total_books}</dd></div>
        <div><dt>Average price</dt><dd>£{stats.avg_price.toFixed(2)}</dd></div>
        <div><dt>Price range</dt><dd>£{stats.min_price.toFixed(0)}–£{stats.max_price.toFixed(0)}</dd></div>
        <div><dt>In stock</dt><dd>{stats.in_stock}</dd></div>
        <div><dt>Categories</dt><dd>{stats.by_category.length}</dd></div>
      </dl>

      <div className="figures">
        <Figure title="Price distribution" note="Number of books per £10 band">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={stats.price_histogram} margin={{ left: -16, right: 8 }}>
              <CartesianGrid vertical={false} stroke="#d5dedc" />
              <XAxis dataKey="range" tick={axis} interval={0} angle={-30} textAnchor="end" height={54} />
              <YAxis tick={axis} allowDecimals={false} />
              <Tooltip cursor={{ fill: "#e3ebe9" }} />
              <Bar dataKey="count" name="Books" fill={TEAL} radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Figure>

        <Figure title="Average price by rating" note="Do better-rated books cost more?">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={stats.by_rating.map((r) => ({ ...r, label: `${r.rating}★` }))} margin={{ left: -8, right: 8 }}>
              <CartesianGrid vertical={false} stroke="#d5dedc" />
              <XAxis dataKey="label" tick={axis} />
              <YAxis tick={axis} tickFormatter={(v) => `£${v}`} />
              <Tooltip cursor={{ fill: "#e3ebe9" }} formatter={(v) => `£${v}`} />
              <Bar dataKey="avg_price" name="Avg price" fill={GOLD} radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Figure>

        <Figure title="Largest categories" note="Books per category, top 8">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={topCategories} layout="vertical" margin={{ left: 24, right: 16 }}>
              <CartesianGrid horizontal={false} stroke="#d5dedc" />
              <XAxis type="number" tick={axis} allowDecimals={false} />
              <YAxis type="category" dataKey="category" tick={axis} width={110} />
              <Tooltip cursor={{ fill: "#e3ebe9" }} />
              <Bar dataKey="count" name="Books" fill={INK} radius={[0, 2, 2, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Figure>
      </div>
    </section>
  );
}
