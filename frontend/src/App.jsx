import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import AppLayout from "./layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import Inspections from "./pages/Inspections";
import Passport from "./pages/Passport";
import Pieces from "./pages/Pieces";
import Production from "./pages/Production";


// ---------------------------------------------------------
// TRUSTTRACE ROUTE CONFIGURATION
// ---------------------------------------------------------

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* ------------------------------------------------
            MAIN APPLICATION LAYOUT
        ------------------------------------------------ */}
        <Route element={<AppLayout />}>

          <Route
            index
            element={<Dashboard />}
          />

          <Route
            path="pieces"
            element={<Pieces />}
          />

          <Route
            path="production"
            element={<Production />}
          />

          <Route
            path="inspections"
            element={<Inspections />}
          />

          <Route
            path="passport"
            element={<Passport />}
          />

        </Route>


        {/* ------------------------------------------------
            UNKNOWN ROUTE FALLBACK
        ------------------------------------------------ */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;