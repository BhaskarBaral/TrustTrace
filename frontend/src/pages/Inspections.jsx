import { useEffect, useState } from "react";

import {
  createInspection,
  getBackendFileUrl,
  getInspections,
  getPieces,
  getUsers,
} from "../services/api";


// ---------------------------------------------------------
// INSPECTIONS PAGE
// ---------------------------------------------------------

function Inspections() {

  // -------------------------------------------------------
  // BACKEND DATA STATE
  // -------------------------------------------------------

  const [pieces, setPieces] = useState([]);
  const [users, setUsers] = useState([]);
  const [inspections, setInspections] = useState([]);


  // -------------------------------------------------------
  // PAGE STATE
  // -------------------------------------------------------

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // -------------------------------------------------------
  // INSPECTION FORM STATE
  // -------------------------------------------------------

  const [formData, setFormData] = useState({
    piece_id: "",
    inspector_id: "",
    image: null,
  });

  const [imagePreview, setImagePreview] = useState("");

  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");


  // -------------------------------------------------------
  // LOAD INSPECTION PAGE DATA
  // -------------------------------------------------------

  useEffect(() => {

    async function loadInspectionData() {

      try {

        setLoading(true);
        setError("");


        // -------------------------------------------------
        // LOAD PIECES, USERS AND INSPECTIONS TOGETHER
        // -------------------------------------------------

        const [
          pieceData,
          userData,
          inspectionData,
        ] = await Promise.all([
          getPieces(),
          getUsers(),
          getInspections(),
        ]);


        setPieces(pieceData);
        setUsers(userData);
        setInspections(inspectionData);

      } catch (error) {

        console.error(
          "Failed to load inspection data:",
          error
        );

        setError(error.message);

      } finally {

        setLoading(false);

      }

    }


    loadInspectionData();

  }, []);


  // -------------------------------------------------------
  // FILTER INSPECTOR USERS
  // -------------------------------------------------------

  const inspectors = users.filter(
    (user) => user.role === "inspector"
  );


  // -------------------------------------------------------
  // HANDLE SELECT INPUT
  // -------------------------------------------------------

  function handleInputChange(event) {

    const { name, value } = event.target;


    setFormData((currentFormData) => ({
      ...currentFormData,
      [name]: value,
    }));

  }


  // -------------------------------------------------------
  // HANDLE IMAGE SELECTION
  // -------------------------------------------------------

  function handleImageChange(event) {

    const selectedFile = event.target.files[0];


    // -----------------------------------------------------
    // NO IMAGE SELECTED
    // -----------------------------------------------------

    if (!selectedFile) {

      setFormData((currentFormData) => ({
        ...currentFormData,
        image: null,
      }));

      setImagePreview("");

      return;

    }


    // -----------------------------------------------------
    // VALIDATE IMAGE TYPE
    // -----------------------------------------------------

    if (!selectedFile.type.startsWith("image/")) {

      setFormError(
        "Please select a valid image file."
      );

      event.target.value = "";

      return;

    }


    // -----------------------------------------------------
    // SAVE IMAGE FILE
    // -----------------------------------------------------

    setFormData((currentFormData) => ({
      ...currentFormData,
      image: selectedFile,
    }));


    // -----------------------------------------------------
    // CREATE LOCAL IMAGE PREVIEW
    // -----------------------------------------------------

    const previewUrl =
      URL.createObjectURL(selectedFile);

    setImagePreview(previewUrl);

    setFormError("");

  }


  // -------------------------------------------------------
  // CREATE NEW INSPECTION
  // -------------------------------------------------------

  async function handleSubmit(event) {

    event.preventDefault();


    // -----------------------------------------------------
    // VERIFY IMAGE EXISTS
    // -----------------------------------------------------

    if (!formData.image) {

      setFormError(
        "Please select an inspection image."
      );

      return;

    }


    try {

      setSubmitting(true);
      setFormError("");
      setSuccessMessage("");


      // ---------------------------------------------------
      // SEND INSPECTION TO BACKEND
      // ---------------------------------------------------

      const newInspection =
        await createInspection(formData);


      // ---------------------------------------------------
      // ADD NEW INSPECTION TO CURRENT LIST
      // ---------------------------------------------------

      setInspections((currentInspections) => [
        ...currentInspections,
        newInspection,
      ]);


      // ---------------------------------------------------
      // CLEAN LOCAL PREVIEW URL
      // ---------------------------------------------------

      if (imagePreview) {
        URL.revokeObjectURL(imagePreview);
      }


      // ---------------------------------------------------
      // RESET FORM
      // ---------------------------------------------------

      setFormData({
        piece_id: "",
        inspector_id: "",
        image: null,
      });

      setImagePreview("");


      // ---------------------------------------------------
      // RESET FILE INPUT
      // ---------------------------------------------------

      const fileInput =
        document.getElementById("inspection-image");

      if (fileInput) {
        fileInput.value = "";
      }


      // ---------------------------------------------------
      // SHOW SUCCESS MESSAGE
      // ---------------------------------------------------

      setSuccessMessage(
        `Inspection created for ${newInspection.piece_id}.`
      );

    } catch (error) {

      console.error(
        "Failed to create inspection:",
        error
      );

      setFormError(error.message);

    } finally {

      setSubmitting(false);

    }

  }


  // -------------------------------------------------------
  // FORMAT CONFIDENCE VALUE
  // -------------------------------------------------------

  function formatConfidence(confidence) {

    if (
      confidence === null ||
      confidence === undefined
    ) {
      return "—";
    }


    // -----------------------------------------------------
    // SUPPORT 0-1 AND 0-100 CONFIDENCE FORMATS
    // -----------------------------------------------------

    const confidenceValue =
      confidence <= 1
        ? confidence * 100
        : confidence;


    return `${confidenceValue.toFixed(1)}%`;

  }


  // -------------------------------------------------------
  // FORMAT TIMESTAMP
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
          QUALITY CONTROL
        </p>

        <h1>Quality Inspections</h1>

        <p>
          Upload jewellery inspection images and track
          quality analysis results.
        </p>

      </div>


      {/* --------------------------------------------------
          CREATE INSPECTION SECTION
      -------------------------------------------------- */}

      <div className="content-section">

        <div className="section-header">

          <div>

            <h2>New Inspection</h2>

            <p>
              Select a jewellery piece and inspector,
              then upload an image for quality analysis.
            </p>

          </div>

        </div>


        {/* ------------------------------------------------
            INSPECTION FORM
        ------------------------------------------------ */}

        <form
          className="inspection-form"
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
              INSPECTOR SELECTION
          ------------------------------------------------ */}

          <div className="form-group">

            <label htmlFor="inspector_id">
              Inspector
            </label>

            <select
              id="inspector_id"
              name="inspector_id"
              value={formData.inspector_id}
              onChange={handleInputChange}
              required
            >

              <option value="">
                Select an inspector
              </option>


              {inspectors.map((user) => (

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
              IMAGE FILE INPUT
          ------------------------------------------------ */}

          <div className="form-group inspection-file-group">

            <label htmlFor="inspection-image">
              Inspection Image
            </label>

            <input
              id="inspection-image"
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              required
            />

          </div>


          {/* ------------------------------------------------
              IMAGE PREVIEW
          ------------------------------------------------ */}

          {imagePreview && (

            <div className="inspection-preview">

              <p className="inspection-preview-label">
                Image Preview
              </p>

              <img
                src={imagePreview}
                alt="Selected inspection preview"
              />

            </div>

          )}


          {/* ------------------------------------------------
              SUBMIT BUTTON
          ------------------------------------------------ */}

          <div className="inspection-submit">

            <button
              className="primary-button"
              type="submit"
              disabled={
                submitting ||
                loading ||
                pieces.length === 0 ||
                inspectors.length === 0
              }
            >

              {submitting
                ? "Uploading..."
                : "Upload Inspection"}

            </button>

          </div>

        </form>


        {/* ------------------------------------------------
            NO INSPECTOR WARNING
        ------------------------------------------------ */}

        {!loading &&
          inspectors.length === 0 && (

            <div className="form-message form-error">

              No inspector account is available.
              Register a user with the Inspector role
              from the Dashboard first.

            </div>

          )}


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
          INSPECTION HISTORY
      -------------------------------------------------- */}

      <div className="content-section">

        <div className="section-header">

          <div>

            <h2>Inspection History</h2>

            <p>
              Uploaded inspection images and their
              quality analysis status.
            </p>

          </div>


          <div className="record-count">

            {inspections.length}{" "}

            {inspections.length === 1
              ? "Inspection"
              : "Inspections"}

          </div>

        </div>


        {/* ------------------------------------------------
            LOADING STATE
        ------------------------------------------------ */}

        {loading && (

          <div className="state-message">
            Loading inspections...
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
          inspections.length === 0 && (

            <div className="state-message">
              No inspections have been uploaded yet.
            </div>

          )}


        {/* ------------------------------------------------
            INSPECTION CARDS
        ------------------------------------------------ */}

        {!loading &&
          !error &&
          inspections.length > 0 && (

            <div className="inspection-grid">


              {inspections.map((inspection) => (

                <article
                  className="inspection-card"
                  key={inspection.id}
                >


                  {/* ----------------------------------------
                      INSPECTION IMAGE
                  ---------------------------------------- */}

                  <div className="inspection-image-container">

                    <img
                      src={getBackendFileUrl(
                        inspection.image_path
                      )}
                      alt={
                        `Inspection for ${inspection.piece_id}`
                      }
                    />

                  </div>


                  {/* ----------------------------------------
                      INSPECTION DETAILS
                  ---------------------------------------- */}

                  <div className="inspection-card-content">

                    <div className="inspection-card-header">

                      <div>

                        <p className="inspection-piece-id">
                          {inspection.piece_id}
                        </p>

                        <p className="inspection-inspector">
                          Inspector:{" "}
                          {inspection.inspector_id}
                        </p>

                      </div>


                      <span className="inspection-status">

                        {inspection.inspection_status}

                      </span>

                    </div>


                    {/* --------------------------------------
                        AI ANALYSIS RESULTS
                    -------------------------------------- */}

                    <div className="inspection-results">


                      <div className="inspection-result">

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


                      <div className="inspection-result">

                        <span>
                          Defect Type
                        </span>

                        <strong>

                          {inspection.defect_type || "—"}

                        </strong>

                      </div>


                      <div className="inspection-result">

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


                    {/* --------------------------------------
                        TIMESTAMP
                    -------------------------------------- */}

                    <p className="inspection-timestamp">

                      Uploaded:{" "}

                      {formatTimestamp(
                        inspection.created_at
                      )}

                    </p>

                  </div>

                </article>

              ))}

            </div>

          )}

      </div>

    </section>

  );

}

export default Inspections;