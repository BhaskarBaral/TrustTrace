import { useEffect, useState } from "react";

import {
  getBackendFileUrl,
  getPiecePassport,
  getPieces,
} from "../services/api";


// ---------------------------------------------------------
// DIGITAL PIECE PASSPORT PAGE
// ---------------------------------------------------------

function Passport() {

  // -------------------------------------------------------
  // PAGE STATE
  // -------------------------------------------------------

  const [pieces, setPieces] = useState([]);
  const [selectedPieceId, setSelectedPieceId] = useState("");
  const [passport, setPassport] = useState(null);

  const [loadingPieces, setLoadingPieces] = useState(true);
  const [loadingPassport, setLoadingPassport] = useState(false);

  const [error, setError] = useState("");


  // -------------------------------------------------------
  // LOAD REGISTERED PIECES
  // -------------------------------------------------------

  useEffect(() => {

    async function loadPieces() {

      try {

        setLoadingPieces(true);
        setError("");

        const pieceData = await getPieces();

        setPieces(pieceData);

      } catch (error) {

        console.error(
          "Failed to load pieces:",
          error
        );

        setError(error.message);

      } finally {

        setLoadingPieces(false);

      }

    }


    loadPieces();

  }, []);


  // -------------------------------------------------------
  // HANDLE PIECE SELECTION
  // -------------------------------------------------------

  function handlePieceChange(event) {

    setSelectedPieceId(event.target.value);

    setPassport(null);

    setError("");

  }


  // -------------------------------------------------------
  // LOAD DIGITAL PASSPORT
  // -------------------------------------------------------

  async function handleLoadPassport(event) {

    event.preventDefault();


    if (!selectedPieceId) {

      setError(
        "Please select a jewellery piece."
      );

      return;

    }


    try {

      setLoadingPassport(true);
      setError("");


      const passportData =
        await getPiecePassport(selectedPieceId);


      setPassport(passportData);

    } catch (error) {

      console.error(
        "Failed to load digital passport:",
        error
      );

      setPassport(null);

      setError(error.message);

    } finally {

      setLoadingPassport(false);

    }

  }


  // -------------------------------------------------------
  // FORMAT TIMESTAMP
  // -------------------------------------------------------

  function formatTimestamp(timestamp) {

    if (!timestamp) {
      return "—";
    }

    return new Date(timestamp).toLocaleString();

  }


  // -------------------------------------------------------
  // FORMAT CONFIDENCE
  // -------------------------------------------------------

  function formatConfidence(confidence) {

    if (
      confidence === null ||
      confidence === undefined
    ) {
      return "—";
    }


    const confidenceValue =
      confidence <= 1
        ? confidence * 100
        : confidence;


    return `${confidenceValue.toFixed(1)}%`;

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
          TRACEABILITY RECORD
        </p>

        <h1>Digital Piece Passport</h1>

        <p>
          View the complete production and inspection
          history of a registered jewellery piece.
        </p>

      </div>


      {/* --------------------------------------------------
          PIECE SEARCH SECTION
      -------------------------------------------------- */}

      <div className="content-section">

        <div className="section-header">

          <div>

            <h2>Find Piece Passport</h2>

            <p>
              Select a registered jewellery piece to view
              its complete traceability record.
            </p>

          </div>

        </div>


        <form
          className="passport-search-form"
          onSubmit={handleLoadPassport}
        >

          <div className="form-group">

            <label htmlFor="passport-piece">
              Jewellery Piece
            </label>

            <select
              id="passport-piece"
              value={selectedPieceId}
              onChange={handlePieceChange}
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


          <button
            className="primary-button"
            type="submit"
            disabled={
              loadingPieces ||
              loadingPassport ||
              pieces.length === 0
            }
          >

            {loadingPassport
              ? "Loading Passport..."
              : "View Passport"}

          </button>

        </form>


        {/* ------------------------------------------------
            ERROR MESSAGE
        ------------------------------------------------ */}

        {error && (

          <div className="form-message form-error">
            {error}
          </div>

        )}

      </div>


      {/* --------------------------------------------------
          DIGITAL PASSPORT
      -------------------------------------------------- */}

      {passport && (

        <div className="passport-container">


          {/* ------------------------------------------------
              PASSPORT HEADER
          ------------------------------------------------ */}

          <div className="passport-header">

            <div>

              <p className="passport-label">
                TRUSTTRACE DIGITAL PASSPORT
              </p>

              <h2>
                {passport.piece.piece_id}
              </h2>

              <p>
                Complete manufacturing and quality
                traceability record.
              </p>

            </div>


            <span className="status-badge">
              {passport.piece.status}
            </span>

          </div>


          {/* ------------------------------------------------
              PIECE DETAILS
          ------------------------------------------------ */}

          <div className="passport-section">

            <div className="section-header">

              <div>

                <h2>Piece Details</h2>

                <p>
                  Core identification and production status.
                </p>

              </div>

            </div>


            <div className="passport-details-grid">


              <div className="passport-detail">

                <span>
                  Piece ID
                </span>

                <strong>
                  {passport.piece.piece_id}
                </strong>

              </div>


              <div className="passport-detail">

                <span>
                  Product Type
                </span>

                <strong>
                  {passport.piece.product_type}
                </strong>

              </div>


              <div className="passport-detail">

                <span>
                  Material
                </span>

                <strong>
                  {passport.piece.material}
                </strong>

              </div>


              <div className="passport-detail">

                <span>
                  Current Stage
                </span>

                <strong>
                  {passport.piece.current_stage}
                </strong>

              </div>


              <div className="passport-detail">

                <span>
                  Status
                </span>

                <strong>
                  {passport.piece.status}
                </strong>

              </div>


              <div className="passport-detail">

                <span>
                  Registered
                </span>

                <strong>
                  {formatTimestamp(
                    passport.piece.created_at
                  )}
                </strong>

              </div>


            </div>

          </div>


          {/* ------------------------------------------------
              PRODUCTION HISTORY
          ------------------------------------------------ */}

          <div className="passport-section">

            <div className="section-header">

              <div>

                <h2>Production History</h2>

                <p>
                  Manufacturing events recorded for this
                  jewellery piece.
                </p>

              </div>


              <div className="record-count">

                {passport.production_history.length}{" "}

                {passport.production_history.length === 1
                  ? "Event"
                  : "Events"}

              </div>

            </div>


            {passport.production_history.length === 0 ? (

              <div className="state-message">
                No production events recorded.
              </div>

            ) : (

              <div className="table-container">

                <table className="data-table">

                  <thead>

                    <tr>
                      <th>Operator</th>
                      <th>Stage</th>
                      <th>Event Type</th>
                      <th>Notes</th>
                      <th>Timestamp</th>
                    </tr>

                  </thead>


                  <tbody>

                    {passport.production_history.map(
                      (productionEvent) => (

                        <tr key={productionEvent.id}>

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

                      )
                    )}

                  </tbody>

                </table>

              </div>

            )}

          </div>


          {/* ------------------------------------------------
              INSPECTION HISTORY
          ------------------------------------------------ */}

          <div className="passport-section">

            <div className="section-header">

              <div>

                <h2>Inspection History</h2>

                <p>
                  Quality inspection records and AI
                  analysis results.
                </p>

              </div>


              <div className="record-count">

                {passport.inspections.length}{" "}

                {passport.inspections.length === 1
                  ? "Inspection"
                  : "Inspections"}

              </div>

            </div>


            {passport.inspections.length === 0 ? (

              <div className="state-message">
                No inspections recorded.
              </div>

            ) : (

              <div className="passport-inspection-grid">


                {passport.inspections.map(
                  (inspection) => (

                    <article
                      className="passport-inspection-card"
                      key={inspection.id}
                    >


                      {/* ------------------------------------
                          INSPECTION IMAGE
                      ------------------------------------ */}

                      <div className="passport-inspection-image">

                        <img
                          src={getBackendFileUrl(
                            inspection.image_path
                          )}
                          alt={
                            `Inspection for ${inspection.piece_id}`
                          }
                        />

                      </div>


                      {/* ------------------------------------
                          INSPECTION INFORMATION
                      ------------------------------------ */}

                      <div className="passport-inspection-content">


                        <div className="passport-inspection-header">

                          <div>

                            <p>
                              Inspector
                            </p>

                            <strong>
                              {inspection.inspector_id}
                            </strong>

                          </div>


                          <span className="inspection-status">

                            {inspection.inspection_status}

                          </span>

                        </div>


                        <div className="passport-inspection-results">


                          <div>

                            <span>
                              Defect
                            </span>

                            <strong>

                              {inspection.inspection_status ===
                              "Pending AI Analysis"
                                ? "Pending"
                                : inspection.defect_detected
                                  ? "Detected"
                                  : "Not Detected"}

                            </strong>

                          </div>


                          <div>

                            <span>
                              Defect Type
                            </span>

                            <strong>
                              {inspection.defect_type || "—"}
                            </strong>

                          </div>


                          <div>

                            <span>
                              Confidence
                            </span>

                            <strong>

                              {formatConfidence(
                                inspection.confidence
                              )}

                            </strong>

                          </div>


                        </div>


                        <p className="inspection-timestamp">

                          Inspected:{" "}

                          {formatTimestamp(
                            inspection.created_at
                          )}

                        </p>


                      </div>

                    </article>

                  )
                )}


              </div>

            )}

          </div>


        </div>

      )}

    </section>

  );

}

export default Passport;