import { useState } from "react";
import UploadForm from "../components/UploadForm";

export default function AdminPage() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [reindexing, setReindexing] = useState(false);

  async function handleReindex() {
    setError(null);
    setStatus(null);
    setReindexing(true);
    try {
      const res = await fetch("/documents/reindex", { method: "POST" });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || "Reindex failed.");
      }
      setStatus("Reindex triggered.");
    } catch (err) {
      setError(err.message);
    } finally {
      setReindexing(false);
    }
  }

  return (
    <div>
      <h2>Admin</h2>
      <UploadForm onUploaded={() => setStatus("Document uploaded.")} onError={setError} />
      <button onClick={handleReindex} disabled={reindexing}>
        {reindexing ? "Reindexing..." : "Reindex"}
      </button>

      {error && <div className="error-banner">{error}</div>}
      {status && <div className="status-banner">{status}</div>}
    </div>
  );
}
