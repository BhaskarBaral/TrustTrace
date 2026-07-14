// ---------------------------------------------------------
// BACKEND API CONFIGURATION
// ---------------------------------------------------------

const API_BASE_URL = "http://127.0.0.1:8000";


// ---------------------------------------------------------
// GENERIC API REQUEST HELPER
// ---------------------------------------------------------

async function apiRequest(endpoint, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    options
  );


  // -------------------------------------------------------
  // HANDLE FAILED API RESPONSES
  // -------------------------------------------------------

  if (!response.ok) {
    let errorMessage =
      "Something went wrong while contacting the backend.";

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        errorMessage =
          typeof errorData.detail === "string"
            ? errorData.detail
            : JSON.stringify(errorData.detail);
      }

    } catch {
      // Keep the default error message if response is not JSON.
    }

    throw new Error(errorMessage);
  }


  // -------------------------------------------------------
  // RETURN JSON RESPONSE
  // -------------------------------------------------------

  return response.json();
}


// ---------------------------------------------------------
// HEALTH API
// ---------------------------------------------------------

export function getBackendHealth() {
  return apiRequest("/health");
}


// ---------------------------------------------------------
// PIECE API
// ---------------------------------------------------------

export function getPieces() {
  return apiRequest("/api/pieces");
}


export function createPiece(pieceData) {
  return apiRequest(
    "/api/pieces",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(pieceData),
    }
  );
}


// ---------------------------------------------------------
// USER / OPERATOR API
// ---------------------------------------------------------

export function getUsers() {
  return apiRequest("/api/users");
}


export function createUser(userData) {
  return apiRequest(
    "/api/users",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(userData),
    }
  );
}

// ---------------------------------------------------------
// PRODUCTION EVENT API
// ---------------------------------------------------------

export function getProductionEvents() {
  return apiRequest("/api/events");
}


export function createProductionEvent(eventData) {
  return apiRequest(
    "/api/events",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(eventData),
    }
  );
}


// ---------------------------------------------------------
// EXPORT BACKEND BASE URL
// ---------------------------------------------------------

export { API_BASE_URL };