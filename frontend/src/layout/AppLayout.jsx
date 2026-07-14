import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";


// ---------------------------------------------------------
// MAIN APPLICATION LAYOUT
// ---------------------------------------------------------

function AppLayout() {
  return (
    <div className="app-layout">

      {/* --------------------------------------------------
          SIDEBAR
      -------------------------------------------------- */}
      <Sidebar />


      {/* --------------------------------------------------
          CURRENT PAGE CONTENT
      -------------------------------------------------- */}
      <main className="main-content">
        <Outlet />
      </main>

    </div>
  );
}

export default AppLayout;