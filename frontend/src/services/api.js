const API_BASE_URL = "http://127.0.0.1:8000";

async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

  if (!response.ok) {
    let errorMessage = "Something went wrong while contacting the backend.";
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === "string"
          ? errorData.detail
          : JSON.stringify(errorData.detail);
      }
    } catch {}
    throw new Error(errorMessage);
  }

  return response.json();
}

async function apiUpload(endpoint, formData) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    let errorMessage = "Something went wrong while contacting the backend.";
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === "string"
          ? errorData.detail
          : JSON.stringify(errorData.detail);
      }
    } catch {}
    throw new Error(errorMessage);
  }

  return response.json();
}

// Health
export function getBackendHealth() {
  return apiRequest("/health");
}

// Pieces
export function getPieces() {
  return apiRequest("/api/pieces");
}

export function createPiece(pieceData) {
  return apiRequest("/api/pieces", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(pieceData),
  });
}

// Users
export function getUsers() {
  return apiRequest("/api/users");
}

export function createUser(userData) {
  return apiRequest("/api/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });
}

export function assignStation(operatorId, stationId) {
  return apiRequest(`/api/users/${operatorId}/station`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ station_id: stationId }),
  });
}

export function pinLogin(operatorId, pin) {
  return apiRequest("/api/users/pin-login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ operator_id: operatorId, pin }),
  });
}

// Events
export function getProductionEvents(stage) {
  const query = stage ? `?stage=${encodeURIComponent(stage)}` : "";
  return apiRequest(`/api/events${query}`);
}

export function createProductionEvent(eventData) {
  return apiRequest("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(eventData),
  });
}

// Quality Gates
export function submitQualityGate(pieceId, stage, inspectorId, imageFile) {
  const formData = new FormData();
  formData.append("piece_id", pieceId);
  formData.append("stage", stage);
  formData.append("inspector_id", inspectorId);
  formData.append("image", imageFile);
  return apiUpload("/api/quality/gates", formData);
}

export function getQualityGates() {
  return apiRequest("/api/quality/gates");
}



// ---------------------------------------------------------
// INSPECTION API
// ---------------------------------------------------------

export function getInspections() {
  return apiRequest("/api/inspections");
}


// ---------------------------------------------------------
// CREATE INSPECTION WITH IMAGE UPLOAD
// ---------------------------------------------------------

export function createInspection(inspectionData) {

  // -------------------------------------------------------
  // BUILD MULTIPART FORM DATA
  // -------------------------------------------------------

  const formData = new FormData();

  formData.append(
    "piece_id",
    inspectionData.piece_id
  );

  formData.append(
    "inspector_id",
    inspectionData.inspector_id
  );

  formData.append(
    "image",
    inspectionData.image
  );


  // -------------------------------------------------------
  // SEND IMAGE UPLOAD REQUEST
  // -------------------------------------------------------

  return apiRequest(
    "/api/inspections",
    {
      method: "POST",
      body: formData,
    }
  );
}


// ---------------------------------------------------------
// BUILD BACKEND FILE URL
// ---------------------------------------------------------

export function getBackendFileUrl(filePath) {
  if (!filePath) {
    return "";
  }

  const normalizedPath = filePath.replace(/\\/g, "/");

  return `${API_BASE_URL}/${normalizedPath}`;
}

// ---------------------------------------------------------
// DIGITAL PIECE PASSPORT API
// ---------------------------------------------------------

export function getPiecePassport(pieceId) {
  return apiRequest(
    `/api/passport/${pieceId}`
  );
}

// ---------------------------------------------------------
// EXPORT BACKEND BASE URL
// ---------------------------------------------------------

export { API_BASE_URL };
