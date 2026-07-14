import { useEffect, useState } from "react";

import {
  createPiece,
  getPieces,
} from "../services/api";


// ---------------------------------------------------------
// PIECE MANAGEMENT PAGE
// ---------------------------------------------------------

function Pieces() {

  // -------------------------------------------------------
  // PIECE LIST STATE
  // -------------------------------------------------------

  const [pieces, setPieces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // -------------------------------------------------------
  // CREATE PIECE FORM STATE
  // -------------------------------------------------------

  const [formData, setFormData] = useState({
    product_type: "",
    material: "",
  });

  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");


  // -------------------------------------------------------
  // LOAD PIECES FROM BACKEND
  // -------------------------------------------------------

  useEffect(() => {
    async function loadPieces() {
      try {
        setLoading(true);
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
        setLoading(false);
      }
    }

    loadPieces();
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
  // CREATE NEW PIECE
  // -------------------------------------------------------

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setSubmitting(true);
      setFormError("");
      setSuccessMessage("");

      const newPiece = await createPiece(formData);


      // ---------------------------------------------------
      // ADD CREATED PIECE TO CURRENT TABLE
      // ---------------------------------------------------

      setPieces((currentPieces) => [
        ...currentPieces,
        newPiece,
      ]);


      // ---------------------------------------------------
      // RESET FORM
      // ---------------------------------------------------

      setFormData({
        product_type: "",
        material: "",
      });


      // ---------------------------------------------------
      // SHOW SUCCESS MESSAGE
      // ---------------------------------------------------

      setSuccessMessage(
        `Piece ${newPiece.piece_id} registered successfully.`
      );

    } catch (error) {
      console.error(
        "Failed to create piece:",
        error
      );

      setFormError(error.message);

    } finally {
      setSubmitting(false);
    }
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
          PIECE MANAGEMENT
        </p>

        <h1>Jewellery Pieces</h1>

        <p>
          Register and manage jewellery pieces in the
          traceability system.
        </p>
      </div>


      {/* --------------------------------------------------
          REGISTER PIECE SECTION
      -------------------------------------------------- */}
      <div className="content-section">

        <div className="section-header">
          <div>
            <h2>Register New Piece</h2>

            <p>
              Add a new jewellery piece to the TrustTrace
              production workflow.
            </p>
          </div>
        </div>


        {/* ------------------------------------------------
            CREATE PIECE FORM
        ------------------------------------------------ */}
        <form
          className="piece-form"
          onSubmit={handleSubmit}
        >

          <div className="form-group">

            <label htmlFor="product_type">
              Product Type
            </label>

            <input
              id="product_type"
              name="product_type"
              type="text"
              placeholder="Example: Gold Necklace"
              value={formData.product_type}
              onChange={handleInputChange}
              required
            />

          </div>


          <div className="form-group">

            <label htmlFor="material">
              Material
            </label>

            <input
              id="material"
              name="material"
              type="text"
              placeholder="Example: 22K Gold"
              value={formData.material}
              onChange={handleInputChange}
              required
            />

          </div>


          <button
            className="primary-button"
            type="submit"
            disabled={submitting}
          >
            {submitting
              ? "Registering..."
              : "Register Piece"}
          </button>

        </form>


        {/* ------------------------------------------------
            FORM ERROR MESSAGE
        ------------------------------------------------ */}
        {formError && (
          <div className="form-message form-error">
            {formError}
          </div>
        )}


        {/* ------------------------------------------------
            FORM SUCCESS MESSAGE
        ------------------------------------------------ */}
        {successMessage && (
          <div className="form-message form-success">
            {successMessage}
          </div>
        )}

      </div>


      {/* --------------------------------------------------
          PIECE LIST SECTION
      -------------------------------------------------- */}
      <div className="content-section">

        <div className="section-header">
          <div>
            <h2>Registered Pieces</h2>

            <p>
              Jewellery pieces currently registered in
              TrustTrace.
            </p>
          </div>

          <div className="record-count">
            {pieces.length}{" "}
            {pieces.length === 1 ? "Piece" : "Pieces"}
          </div>
        </div>


        {/* ------------------------------------------------
            LOADING STATE
        ------------------------------------------------ */}
        {loading && (
          <div className="state-message">
            Loading pieces...
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
          pieces.length === 0 && (
            <div className="state-message">
              No jewellery pieces have been registered yet.
            </div>
          )}


        {/* ------------------------------------------------
            PIECE TABLE
        ------------------------------------------------ */}
        {!loading &&
          !error &&
          pieces.length > 0 && (

            <div className="table-container">

              <table className="data-table">

                <thead>
                  <tr>
                    <th>Piece ID</th>
                    <th>Product Type</th>
                    <th>Material</th>
                    <th>Current Stage</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>

                  {pieces.map((piece) => (

                    <tr key={piece.id}>

                      <td className="piece-id">
                        {piece.piece_id}
                      </td>

                      <td>
                        {piece.product_type}
                      </td>

                      <td>
                        {piece.material}
                      </td>

                      <td>
                        {piece.current_stage}
                      </td>

                      <td>
                        <span className="status-badge">
                          {piece.status}
                        </span>
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

export default Pieces;