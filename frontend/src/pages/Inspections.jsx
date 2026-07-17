import { useEffect, useState } from "react";
import {
  getPieces,
  getPieceQualityGates,
  getQualityGates,
  getUsers,
  reviewQualityGate,
  submitQualityGate,
} from "../services/api";

function Inspections() {
  const [gates, setGates] = useState([]);
  const [pieces, setPieces] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [formData, setFormData] = useState({
    piece_id: "",
    stage: "",
    inspector_id: "",
  });
  const [imageFile, setImageFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const [reviewGateId, setReviewGateId] = useState(null);
  const [reviewVerdict, setReviewVerdict] = useState("PASS");
  const [reviewerId, setReviewerId] = useState("");
  const [reviewSubmitting, setReviewSubmitting] = useState(false);

  const [filterPieceId, setFilterPieceId] = useState("");

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const [gateData, pieceData, userData] = await Promise.all([
          getQualityGates(),
          getPieces(),
          getUsers(),
        ]);
        setGates(gateData);
        setPieces(pieceData);
        setUsers(userData);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  function handleInputChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  function handleFileChange(e) {
    setImageFile(e.target.files[0]);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!imageFile) {
      setFormError("Please select an image to upload.");
      return;
    }
    try {
      setSubmitting(true);
      setFormError("");
      const newGate = await submitQualityGate(
        formData.piece_id,
        formData.stage,
        formData.inspector_id,
        imageFile,
      );
      setGates((prev) => [newGate, ...prev]);
      setFormData({ piece_id: "", stage: "", inspector_id: "" });
      setImageFile(null);
      setSuccessMessage(`Inspection recorded. AI verdict: ${newGate.ai_verdict}${newGate.defect_type ? ` (${newGate.defect_type})` : ""}`);
    } catch (e) {
      setFormError(e.message);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleReviewSubmit() {
    if (!reviewVerdict || !reviewerId) return;
    try {
      setReviewSubmitting(true);
      const updatedGate = await reviewQualityGate(reviewGateId, reviewVerdict, reviewerId);
      setGates((prev) =>
        prev.map((g) => (g.id === updatedGate.id ? updatedGate : g))
      );
      setReviewGateId(null);
    } catch (e) {
      setFormError(e.message);
    } finally {
      setReviewSubmitting(false);
    }
  }

  async function loadPieceGates() {
    if (!filterPieceId) return;
    try {
      const pieceGates = await getPieceQualityGates(filterPieceId);
      setGates(pieceGates);
    } catch (e) {
      setError(e.message);
    }
  }

  function verdictBadge(verdict) {
    const styles = {
      PASS: { bg: "#edf7f1", color: "#287a50" },
      FLAG: { bg: "#fef9ee", color: "#b8891d" },
      FAIL: { bg: "#fff5f5", color: "#b14343" },
      PENDING: { bg: "#eef2f8", color: "#52627a" },
    };
    const s = styles[verdict] || styles.PENDING;
    return (
      <span
        className="role-badge"
        style={{ background: s.bg, color: s.color }}
      >
        {verdict}
      </span>
    );
  }

  if (loading) return <section className="page"><div className="state-message">Loading inspections...</div></section>;

  return (
    <section className="page">
      <div className="page-header">
        <p className="page-label">QUALITY CONTROL</p>
        <h1>Quality Inspections</h1>
        <p>Upload inspection images to AI quality gates and review flagged pieces.</p>
      </div>

      {/* Submit Inspection */}
      <div className="content-section">
        <div className="section-header">
          <div>
            <h2>Submit Inspection</h2>
            <p>Select a piece, stage, and inspector, then upload an image for AI quality analysis.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="production-form">
          <div className="form-group">
            <label htmlFor="piece_id">Piece</label>
            <select id="piece_id" name="piece_id" value={formData.piece_id} onChange={handleInputChange} required>
              <option value="">Select a piece</option>
              {pieces.map((p) => (
                <option key={p.id} value={p.piece_id}>{p.piece_id} — {p.product_type}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="stage">Checkpoint</label>
            <select id="stage" name="stage" value={formData.stage} onChange={handleInputChange} required>
              <option value="">Select checkpoint</option>
              <option value="casting">Post-Casting</option>
              <option value="stone-setting">Post-Stone Setting</option>
              <option value="polishing">Post-Polishing</option>
              <option value="plating">Post-Plating</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="inspector_id">Inspector</label>
            <select id="inspector_id" name="inspector_id" value={formData.inspector_id} onChange={handleInputChange} required>
              <option value="">Select inspector</option>
              {users.map((u) => (
                <option key={u.id} value={u.operator_id}>{u.operator_id} — {u.name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="image">Inspection Image</label>
            <input id="image" type="file" accept="image/jpeg,image/png,image/webp" onChange={handleFileChange} required />
          </div>

          <div className="production-submit">
            <button className="primary-button" type="submit" disabled={submitting || pieces.length === 0}>
              {submitting ? "Analyzing..." : "Submit for AI Inspection"}
            </button>
          </div>
        </form>

        {formError && <div className="form-message form-error">{formError}</div>}
        {successMessage && <div className="form-message form-success">{successMessage}</div>}
      </div>

      {/* Inspection History */}
      <div className="content-section">
        <div className="section-header">
          <div>
            <h2>Inspection History</h2>
            <p>All quality gate submissions with AI verdicts and human review status.</p>
          </div>
          <div className="record-count">{gates.length} {gates.length === 1 ? "Gate" : "Gates"}</div>
        </div>

        <div style={{ display: "flex", gap: "12px", marginBottom: "18px", alignItems: "end" }}>
          <div className="form-group" style={{ flex: 1, maxWidth: "300px" }}>
            <label>Filter by Piece</label>
            <div style={{ display: "flex", gap: "8px" }}>
              <select value={filterPieceId} onChange={(e) => setFilterPieceId(e.target.value)}>
                <option value="">All pieces</option>
                {pieces.map((p) => <option key={p.id} value={p.piece_id}>{p.piece_id}</option>)}
              </select>
              <button className="primary-button" type="button" onClick={loadPieceGates} disabled={!filterPieceId}>Filter</button>
            </div>
          </div>
        </div>

        {error && <div className="form-message form-error">{error}</div>}

        {gates.length === 0 && !error && (
          <div className="state-message">No quality inspections recorded yet.</div>
        )}

        {gates.length > 0 && (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Gate ID</th>
                  <th>Piece</th>
                  <th>Stage</th>
                  <th>AI Verdict</th>
                  <th>Defect</th>
                  <th>Confidence</th>
                  <th>Human Review</th>
                  <th>Time</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {gates.map((gate) => (
                  <tr key={gate.id}>
                    <td className="piece-id">GATE-{gate.id}</td>
                    <td>{gate.piece_id}</td>
                    <td>{gate.stage}</td>
                    <td>{verdictBadge(gate.ai_verdict)}</td>
                    <td>{gate.defect_type || "—"}</td>
                    <td>{gate.confidence ? `${(gate.confidence * 100).toFixed(1)}%` : "—"}</td>
                    <td>{gate.human_review ? verdictBadge(gate.human_review) : "—"}</td>
                    <td>{new Date(gate.created_at).toLocaleString()}</td>
                    <td>
                      {!gate.human_review && gate.ai_verdict !== "PASS" && (
                        <button
                          className="primary-button"
                          style={{ padding: "6px 12px", fontSize: "12px" }}
                          onClick={() => setReviewGateId(gate.id)}
                        >
                          Review
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Review Modal */}
      {reviewGateId && (
        <div style={{
          position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
          background: "rgba(0,0,0,0.4)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000,
        }}>
          <div style={{
            background: "#fff", borderRadius: "14px", padding: "32px", maxWidth: "480px", width: "100%",
            margin: "20px",
          }}>
            <h2 style={{ marginBottom: "16px" }}>Human Review — GATE-{reviewGateId}</h2>
            <div className="form-group" style={{ marginBottom: "16px" }}>
              <label>Verdict</label>
              <select value={reviewVerdict} onChange={(e) => setReviewVerdict(e.target.value)}>
                <option value="PASS">PASS — Accept piece</option>
                <option value="FAIL">FAIL — Reject piece</option>
              </select>
            </div>
            <div className="form-group" style={{ marginBottom: "16px" }}>
              <label>Reviewer ID</label>
              <select value={reviewerId} onChange={(e) => setReviewerId(e.target.value)}>
                <option value="">Select reviewer</option>
                {users.map((u) => <option key={u.id} value={u.operator_id}>{u.operator_id} — {u.name}</option>)}
              </select>
            </div>
            <div style={{ display: "flex", gap: "12px" }}>
              <button className="primary-button" onClick={handleReviewSubmit} disabled={reviewSubmitting || !reviewerId}>
                {reviewSubmitting ? "Submitting..." : "Submit Review"}
              </button>
              <button className="primary-button" style={{ background: "#eef2f8", color: "#3d485a" }} onClick={() => setReviewGateId(null)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export default Inspections;
