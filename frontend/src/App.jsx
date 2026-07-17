import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import AppLayout from "./layout/AppLayout";
import Analytics from "./pages/Analytics";
import Dashboard from "./pages/Dashboard";
import Inspections from "./pages/Inspections";
import Passport from "./pages/Passport";
import Pieces from "./pages/Pieces";
import Production from "./pages/Production";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="pieces" element={<Pieces />} />
          <Route path="production" element={<Production />} />
          <Route path="inspections" element={<Inspections />} />
          <Route path="passport" element={<Passport />} />
          <Route path="analytics" element={<Analytics />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;