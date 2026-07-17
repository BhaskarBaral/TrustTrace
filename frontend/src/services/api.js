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

export function getPieceQualityGates(pieceId) {
  return apiRequest(`/api/quality/gates/piece/${pieceId}`);
}

export function getQualitySummary(stage) {
  return apiRequest(`/api/quality/summary${stage || ""}`);
}

export function reviewQualityGate(gateId, verdict, reviewerId) {
  return apiRequest(`/api/quality/gates/${gateId}/review`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ verdict, reviewer_id: reviewerId }),
  });
}

// Passport
export function getPiecePassport(pieceId) {
  return apiRequest(`/api/passport/${pieceId}`);
}

export function getComplianceReport(pieceId) {
  return apiRequest(`/api/passport/${pieceId}/compliance`);
}

// Batches
export function createBatch(batchData) {
  return apiRequest("/api/batches", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(batchData),
  });
}

export function generatePieces(batchId) {
  return apiRequest(`/api/batches/${batchId}/pieces`, { method: "POST" });
}

export function getBatches() {
  return apiRequest("/api/batches");
}

export function getBatch(batchId) {
  return apiRequest(`/api/batches/${batchId}`);
}

// Weights
export function getPieceWeights(pieceId) {
  return apiRequest(`/api/weights/piece/${pieceId}`);
}

export function getStageWeights(stage) {
  return apiRequest(`/api/weights/stage/${stage}`);
}

export function getGoldReconciliation() {
  return apiRequest("/api/weights/reconciliation");
}

// Analytics
export function getWipStatus() {
  return apiRequest("/api/analytics/wip");
}

export function getQualityAnalytics(stage) {
  const query = stage ? `?stage=${encodeURIComponent(stage)}` : "";
  return apiRequest(`/api/analytics/quality${query}`);
}

export function getGoldReconciliationAnalytics() {
  return apiRequest("/api/analytics/gold-reconciliation");
}

export function getProductionInsights() {
  return apiRequest("/api/analytics/insights");
}

export function getOperatorAnalytics(operatorId) {
  return apiRequest(`/api/analytics/operator/${operatorId}`);
}

// Auth
export function login(email, password) {
  return apiRequest("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
}

export { API_BASE_URL };
