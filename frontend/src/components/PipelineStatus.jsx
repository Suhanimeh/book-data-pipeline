
// # Student Name: Ruvi Kathiriya

// # Student ID: ET21BTAI031

// # Course: Web Programming

// # Academic Year: Third Year B.Tech (AI & DS)

// # Semester: 6
import { useEffect, useRef, useState } from "react";
import { api } from "../api";

export default function PipelineStatus({ onFinished, lastUpdated }) {
  const [run, setRun] = useState(null);
  const [error, setError] = useState("");
  const prevStatus = useRef(null);

  const poll = async () => {
    try {
      const [latest] = await api.runs();
      setRun(latest || null);
    } catch (e) { setError(e.message); }
  };

  useEffect(() => { poll(); }, []);

  useEffect(() => {
    if (run?.status !== "running") return undefined;
    const id = setInterval(poll, 2500);
    return () => clearInterval(id);
  }, [run?.status]);

  useEffect(() => {
    if (prevStatus.current === "running" && run?.status !== "running") onFinished();
    prevStatus.current = run?.status;
  }, [run?.status]);   // eslint-disable-line react-hooks/exhaustive-deps

  const start = async () => {
    setError("");
    try { setRun(await api.startRun()); } catch (e) { setError(e.message); }
  };

  const running = run?.status === "running";
  let summary = "No runs yet";
  if (running) summary = "Collecting data…";
  else if (run?.status === "success")
    summary = `Last run stored ${run.rows_stored} books, ${run.rows_dropped} discarded`;
  else if (run?.status === "failed") summary = `Last run failed: ${run.error}`;

  return (
    <div className="pipeline">
      <button className="primary" onClick={start} disabled={running}>
        {running ? "Collecting…" : "Collect data"}
      </button>
      <span className={`pipeline-note ${run?.status === "failed" ? "bad" : ""}`} aria-live="polite">
        {error || summary}
      </span>
      {lastUpdated && !running && (
        <span className="pipeline-note">Data as of {new Date(lastUpdated).toLocaleString()}</span>
      )}
    </div>
  );
}
