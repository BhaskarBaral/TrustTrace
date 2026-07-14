import { useEffect, useState } from "react";

import {
  createProductionEvent,
  getPieces,
  getProductionEvents,
  getUsers,
} from "../services/api";


// ---------------------------------------------------------
// PRODUCTION TRACKING PAGE
// ---------------------------------------------------------

function Production() {

  // -------------------------------------------------------
  // BACKEND DATA STATE
  // -------------------------------------------------------

  const [pieces, setPieces] = useState([]);
  const [users, setUsers] = useState([]);
  const [events, setEvents] = useState([]);


  // -------------------------------------------------------
  // PAGE STATE
  // -------------------------------------------------------

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // -------------------------------------------------------
  // PRODUCTION EVENT FORM STATE
  // -------------------------------------------------------

  const [formData, setFormData] = useState({
    piece_id: "",
    operator_id: "",
    stage: "",
    event_type: "",
    notes: "",
  });

  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");


  // -------------------------------------------------------
  // LOAD PRODUCTION PAGE DATA
  // -------------------------------------------------------

  useEffect(() => {
    async function loadProductionData() {
      try {
        setLoading(true);
        setError("");

        const [
          pieceData,
          userData,
          eventData,
        ] = await Promise.all([
          getPieces(),
          getUsers(),
          getProductionEvents(),
        ]);

        setPieces(pieceData);
        setUsers(userData);
        setEvents(eventData);

      } catch (error) {
        console.error(
          "Failed to load production data:",
          error
        );

        setError(error.message);

      } finally {
        setLoading(false);
      }
    }

    loadProductionData();
  }, []);


  // -------------------------------------------------------
  // HANDLE FORM INPUT
  // -------------------------------------------------------

  function handleInputChange(event) {
    const { name, value } = event.target;

    setFormData((currentFormData) => ({
      ...currentFormData,
      [name]: value,
    }));
  }


  // -------------------------------------------------------
  // CREATE PRODUCTION EVENT
  // -------------------------------------------------------

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setSubmitting(true);
      setFormError("");
      setSuccessMessage("");

      const newEvent =
        await createProductionEvent(formData);


      // ---------------------------------------------------
      // ADD NEW EVENT TO PRODUCTION HISTORY
      // ---------------------------------------------------

      setEvents((currentEvents) => [
        ...currentEvents,
        newEvent,
      ]);


      // ---------------------------------------------------
      // RESET FORM
      // ---------------------------------------------------

      setFormData({
        piece_id: "",
        operator_id: "",
        stage: "",
        event_type: "",
        notes: "",
      });


      // ---------------------------------------------------
      // SHOW SUCCESS MESSAGE
      // ---------------------------------------------------

      setSuccessMessage(
        `Production event recorded for ${newEvent.piece_id}.`
      );

    } catch (error) {
      console.error(
        "Failed to create production event:",
        error
      );

      setFormError(error.message);

    } finally {
      setSubmitting(false);
    }
  }


  // -------------------------------------------------------
  // FORMAT EVENT TIMESTAMP
  // -------------------------------------------------------

  function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
  }


  // -------------------------------------------------------
  // PAGE UI
  // -------------------------------------------------------

  return (
    <section className="page">

      {/* --------------------------------------------------
          PAGE HEADER
      -------------------------------------------------- */}
      <div className="page-header">

        <p className="page-label">
          PRODUCTION TRACEABILITY
        </p>

        <h1>Production Tracking</h1>

        <p>
          Record manufacturing events and track each
          jewellery piece through the production workflow.
        </p>

      </div>


      {/* --------------------------------------------------
          RECORD PRODUCTION EVENT
      -------------------------------------------------- */}
      <div className="content-section">

        <div className="section-header">

          <div>
            <h2>Record Production Event</h2>

            <p>
              Select a registered piece and operator, then
              record the latest manufacturing activity.
            </p>
          </div>

        </div>


        {/* ------------------------------------------------
            PRODUCTION EVENT FORM
        ------------------------------------------------ */}
        <form
          className="production-form"
          onSubmit={handleSubmit}
        >

          {/* ------------------------------------------------
              PIECE SELECTION
          ------------------------------------------------ */}
          <div className="form-group">

            <label htmlFor="piece_id">
              Jewellery Piece
            </label>

            <select
              id="piece_id"
              name="piece_id"
              value={formData.piece_id}
              onChange={handleInputChange}
              required
            >

              <option value="">
                Select a piece
              </option>

              {pieces.map((piece) => (
                <option
                  key={piece.id}
                  value={piece.piece_id}
                >
                  {piece.piece_id} — {piece.product_type}
                </option>
              ))}

            </select>

          </div>


          {/* ------------------------------------------------
              OPERATOR SELECTION
          ------------------------------------------------ */}
          <div className="form-group">

            <label htmlFor="operator_id">
              Operator
            </label>

            <select
              id="operator_id"
              name="operator_id"
              value={formData.operator_id}
              onChange={handleInputChange}
              required
            >

              <option value="">
                Select an operator
              </option>

              {users.map((user) => (
                <option
                  key={user.id}
                  value={user.operator_id}
                >
                  {user.operator_id} — {user.name}
                </option>
              ))}

            </select>

          </div>


          {/* ------------------------------------------------
              PRODUCTION STAGE
          ------------------------------------------------ */}
          <div className="form-group">

            <label htmlFor="stage">
              Production Stage
            </label>

            <select
              id="stage"
              name="stage"
              value={formData.stage}
              onChange={handleInputChange}
              required
            >

              <option value="">
                Select a stage
              </option>

              <option value="Design">
                Design
              </option>

              <option value="Casting">
                Casting
              </option>

              <option value="Crafting">
                Crafting
              </option>

              <option value="Stone Setting">
                Stone Setting
              </option>

              <option value="Polishing">
                Polishing
              </option>

              <option value="Quality Inspection">
                Quality Inspection
              </option>

              <option value="Completed">
                Completed
              </option>

            </select>

          </div>


          {/* ------------------------------------------------
              EVENT TYPE
          ------------------------------------------------ */}
          <div className="form-group">

            <label htmlFor="event_type">
              Event Type
            </label>

            <select
              id="event_type"
              name="event_type"
              value={formData.event_type}
              onChange={handleInputChange}
              required
            >

              <option value="">
                Select event type
              </option>

              <option value="Stage Started">
                Stage Started
              </option>

              <option value="Stage Completed">
                Stage Completed
              </option>

              <option value="Quality Check">
                Quality Check
              </option>

              <option value="Status Update">
                Status Update
              </option>

            </select>

          </div>


          {/* ------------------------------------------------
              NOTES
          ------------------------------------------------ */}
          <div className="form-group production-notes">

            <label htmlFor="notes">
              Notes
            </label>

            <textarea
              id="notes"
              name="notes"
              rows="3"
              placeholder="Enter production notes..."
              value={formData.notes}
              onChange={handleInputChange}
            ></textarea>

          </div>


          {/* ------------------------------------------------
              SUBMIT BUTTON
          ------------------------------------------------ */}
          <div className="production-submit">

            <button
              className="primary-button"
              type="submit"
              disabled={
                submitting ||
                loading ||
                pieces.length === 0 ||
                users.length === 0
              }
            >
              {submitting
                ? "Recording..."
                : "Record Event"}
            </button>

          </div>

        </form>


        {/* ------------------------------------------------
            FORM ERROR
        ------------------------------------------------ */}
        {formError && (
          <div className="form-message form-error">
            {formError}
          </div>
        )}


        {/* ------------------------------------------------
            FORM SUCCESS
        ------------------------------------------------ */}
        {successMessage && (
          <div className="form-message form-success">
            {successMessage}
          </div>
        )}

      </div>


      {/* --------------------------------------------------
          PRODUCTION HISTORY
      -------------------------------------------------- */}
      <div className="content-section">

        <div className="section-header">

          <div>
            <h2>Production History</h2>

            <p>
              Manufacturing events recorded across all
              jewellery pieces.
            </p>
          </div>

          <div className="record-count">
            {events.length}{" "}
            {events.length === 1 ? "Event" : "Events"}
          </div>

        </div>


        {/* ------------------------------------------------
            LOADING STATE
        ------------------------------------------------ */}
        {loading && (
          <div className="state-message">
            Loading production data...
          </div>
        )}


        {/* ------------------------------------------------
            ERROR STATE
        ------------------------------------------------ */}
        {!loading && error && (
          <div className="state-message error-message">
            {error}
          </div>
        )}


        {/* ------------------------------------------------
            EMPTY STATE
        ------------------------------------------------ */}
        {!loading &&
          !error &&
          events.length === 0 && (
            <div className="state-message">
              No production events have been recorded yet.
            </div>
          )}


        {/* ------------------------------------------------
            PRODUCTION EVENT TABLE
        ------------------------------------------------ */}
        {!loading &&
          !error &&
          events.length > 0 && (

            <div className="table-container">

              <table className="data-table">

                <thead>
                  <tr>
                    <th>Piece ID</th>
                    <th>Operator</th>
                    <th>Stage</th>
                    <th>Event Type</th>
                    <th>Notes</th>
                    <th>Timestamp</th>
                  </tr>
                </thead>

                <tbody>

                  {events.map((productionEvent) => (

                    <tr key={productionEvent.id}>

                      <td className="piece-id">
                        {productionEvent.piece_id}
                      </td>

                      <td>
                        {productionEvent.operator_id}
                      </td>

                      <td>
                        {productionEvent.stage}
                      </td>

                      <td>
                        <span className="event-badge">
                          {productionEvent.event_type}
                        </span>
                      </td>

                      <td>
                        {productionEvent.notes || "—"}
                      </td>

                      <td>
                        {formatTimestamp(
                          productionEvent.timestamp
                        )}
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          )}

      </div>

    </section>
  );
}

export default Production;