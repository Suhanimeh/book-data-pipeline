
// # Student Name: Ruvi Kathiriya

// # Student ID: ET21BTAI031

// # Course: Web Programming

// # Academic Year: Third Year B.Tech (AI & DS)

// # Semester: 6
export default function Filters({ filters, categories, onChange, onReset }) {
  return (
    <aside className="filters" aria-label="Filters">
      <h2>Filter books</h2>

      <label>Title contains
        <input type="search" value={filters.search} placeholder="e.g. secret"
               onChange={(e) => onChange({ search: e.target.value })} />
      </label>

      <label>Category
        <select value={filters.category} onChange={(e) => onChange({ category: e.target.value })}>
          <option value="">All categories</option>
          {categories.map((c) => (
            <option key={c.name} value={c.name}>{c.name} ({c.count})</option>
          ))}
        </select>
      </label>

      <div className="pair">
        <label>Min price (£)
          <input type="number" min="0" value={filters.min_price}
                 onChange={(e) => onChange({ min_price: e.target.value })} />
        </label>
        <label>Max price (£)
          <input type="number" min="0" value={filters.max_price}
                 onChange={(e) => onChange({ max_price: e.target.value })} />
        </label>
      </div>

      <label>Minimum rating
        <select value={filters.rating} onChange={(e) => onChange({ rating: e.target.value })}>
          <option value="">Any rating</option>
          {[5, 4, 3, 2, 1].map((r) => <option key={r} value={r}>{r} stars and up</option>)}
        </select>
      </label>

      <label>Availability
        <select value={filters.in_stock} onChange={(e) => onChange({ in_stock: e.target.value })}>
          <option value="">In stock or not</option>
          <option value="true">In stock only</option>
          <option value="false">Out of stock only</option>
        </select>
      </label>

      <button type="button" onClick={onReset}>Clear filters</button>
    </aside>
  );
}
