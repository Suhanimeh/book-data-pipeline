
// # Student Name: Ruvi Kathiriya

// # Student ID: ET21BTAI031

// # Course: Web Programming

// # Academic Year: Third Year B.Tech (AI & DS)

// # Semester: 6
import { useState } from "react";

const COLUMNS = [
  { key: "title", label: "Title" },
  { key: "category", label: "Category" },
  { key: "price", label: "Price", numeric: true },
  { key: "rating", label: "Rating" },
  { key: "stock_count", label: "Stock", numeric: true },
];

const Stars = ({ n }) =>
  n ? <span className="stars" aria-label={`${n} out of 5`}>{"★".repeat(n)}<i>{"★".repeat(5 - n)}</i></span> : <span className="muted">Unrated</span>;

export default function BookTable({ data, filters, loading, onSort, onPage }) {
  const [open, setOpen] = useState(null);

  const toggleSort = (key) =>
    onSort({ sort_by: key, order: filters.sort_by === key && filters.order === "asc" ? "desc" : "asc" });

  return (
    <section className="results" aria-busy={loading}>
      <div className="results-head">
        <h2>{data.total} {data.total === 1 ? "book" : "books"}</h2>
        <span className="muted">Select a row to read its description</span>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              {COLUMNS.map((c) => {
                const active = filters.sort_by === c.key;
                return (
                  <th key={c.key} className={c.numeric ? "num" : ""}
                      aria-sort={active ? (filters.order === "asc" ? "ascending" : "descending") : "none"}>
                    <button type="button" className="sort" onClick={() => toggleSort(c.key)}>
                      {c.label}{active ? (filters.order === "asc" ? " ▲" : " ▼") : ""}
                    </button>
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody>
            {data.items.map((b) => (
              <FragmentRow key={b.id} book={b} open={open === b.id}
                           onToggle={() => setOpen(open === b.id ? null : b.id)} />
            ))}
            {!loading && data.items.length === 0 && (
              <tr><td colSpan={COLUMNS.length} className="muted center">
                No books match these filters. Widen the price range or clear the filters.
              </td></tr>
            )}
          </tbody>
        </table>
      </div>

      <nav className="pager" aria-label="Pagination">
        <button disabled={filters.page <= 1} onClick={() => onPage(filters.page - 1)}>Previous</button>
        <span>Page {filters.page} of {data.pages}</span>
        <button disabled={filters.page >= data.pages} onClick={() => onPage(filters.page + 1)}>Next</button>
      </nav>
    </section>
  );
}

function FragmentRow({ book, open, onToggle }) {
  return (
    <>
      <tr className="row" onClick={onToggle} aria-expanded={open} tabIndex={0}
          onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && (e.preventDefault(), onToggle())}>
        <td className="title">{book.title}</td>
        <td>{book.category}</td>
        <td className="num">£{book.price.toFixed(2)}</td>
        <td><Stars n={book.rating} /></td>
        <td className="num">{book.in_stock ? book.stock_count : <span className="muted">Out</span>}</td>
      </tr>
      {open && (
        <tr className="detail">
          <td colSpan={5}>
            <div className="detail-body">
              {book.image_url && <img src={book.image_url} alt={`Cover of ${book.title}`} loading="lazy" />}
              <div>
                <p>{book.description || "No description available for this book."}</p>
                <a href={book.product_url} target="_blank" rel="noreferrer">View source page</a>
              </div>
            </div>
          </td>
        </tr>
      )}
    </>
  );
}
