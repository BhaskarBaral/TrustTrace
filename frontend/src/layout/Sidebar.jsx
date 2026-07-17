import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

import { getBackendHealth } from "../services/api";


// ---------------------------------------------------------
// SIDEBAR NAVIGATION
// ---------------------------------------------------------

function Sidebar() {

  // -------------------------------------------------------
  // BACKEND CONNECTION STATE
  // -------------------------------------------------------

  const [backendStatus, setBackendStatus] = useState("checking");


  // -------------------------------------------------------
  // CHECK BACKEND HEALTH
  // -------------------------------------------------------

  useEffect(() => {
    async function checkBackendHealth() {
      try {
        const healthData = await getBackendHealth();

        if (healthData.status === "healthy") {
          setBackendStatus("connected");
        } else {
          setBackendStatus("offline");
        }

      } catch (error) {
        console.error(
          "Backend health check failed:",
          error
        );

        setBackendStatus("offline");
      }
    }

    checkBackendHealth();
  }, []);


  // -------------------------------------------------------
  // BACKEND STATUS TEXT
  // -------------------------------------------------------

  const backendStatusText = {
    checking: "Checking Backend...",
    connected: "Backend Connected",
    offline: "Backend Offline",
  };


  // -------------------------------------------------------
  // SIDEBAR UI
  // -------------------------------------------------------

  return (
    <aside className="sidebar">

      {/* --------------------------------------------------
          BRAND
      -------------------------------------------------- */}
      <div className="sidebar-brand">
        <h1>TrustTrace</h1>
        <p>Traceability Platform</p>
      </div>


      {/* --------------------------------------------------
          NAVIGATION LINKS
      -------------------------------------------------- */}
      <nav className="sidebar-navigation">

        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/pieces"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Pieces
        </NavLink>

        <NavLink
          to="/production"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Production
        </NavLink>

        <NavLink
          to="/inspections"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Inspections
        </NavLink>

        <NavLink
          to="/passport"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Digital Passport
        </NavLink>

        <NavLink
          to="/analytics"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Analytics
        </NavLink>

      </nav>


      {/* --------------------------------------------------
          BACKEND CONNECTION STATUS
      -------------------------------------------------- */}
      <div className="sidebar-footer">

        <span
          className={`status-indicator ${backendStatus}`}
        ></span>

        <div>
          <p>Prototype System</p>

          <span>
            {backendStatusText[backendStatus]}
          </span>
        </div>

      </div>

    </aside>
  );
}

export default Sidebar;