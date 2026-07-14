import { useEffect, useState } from "react";

import {
  createUser,
  getUsers,
} from "../services/api";


// ---------------------------------------------------------
// DASHBOARD PAGE
// ---------------------------------------------------------

function Dashboard() {

  // -------------------------------------------------------
  // OPERATOR LIST STATE
  // -------------------------------------------------------

  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // -------------------------------------------------------
  // OPERATOR FORM STATE
  // -------------------------------------------------------

  const [formData, setFormData] = useState({
    name: "",
    operator_id: "",
    email: "",
    password: "",
    role: "operator",
  });

  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");


  // -------------------------------------------------------
  // LOAD OPERATORS FROM BACKEND
  // -------------------------------------------------------

  useEffect(() => {
    async function loadUsers() {
      try {
        setLoading(true);
        setError("");

        const userData = await getUsers();

        setUsers(userData);

      } catch (error) {
        console.error(
          "Failed to load operators:",
          error
        );

        setError(error.message);

      } finally {
        setLoading(false);
      }
    }

    loadUsers();
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
  // CREATE NEW OPERATOR
  // -------------------------------------------------------

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setSubmitting(true);
      setFormError("");
      setSuccessMessage("");

      const newUser = await createUser(formData);


      // ---------------------------------------------------
      // ADD NEW OPERATOR TO CURRENT LIST
      // ---------------------------------------------------

      setUsers((currentUsers) => [
        ...currentUsers,
        newUser,
      ]);


      // ---------------------------------------------------
      // RESET FORM
      // ---------------------------------------------------

      setFormData({
        name: "",
        operator_id: "",
        email: "",
        password: "",
        role: "operator",
      });


      // ---------------------------------------------------
      // SHOW SUCCESS MESSAGE
      // ---------------------------------------------------

      setSuccessMessage(
        `Operator ${newUser.operator_id} registered successfully.`
      );

    } catch (error) {
      console.error(
        "Failed to create operator:",
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
          SYSTEM OVERVIEW
        </p>

        <h1>Dashboard</h1>

        <p>
          Manage prototype operators and monitor the
          TrustTrace jewellery manufacturing workflow.
        </p>
      </div>


      {/* --------------------------------------------------
          REGISTER OPERATOR SECTION
      -------------------------------------------------- */}
      <div className="content-section">

        <div className="section-header">
          <div>
            <h2>Register Operator</h2>

            <p>
              Add an operator or inspector who can participate
              in the production and inspection workflow.
            </p>
          </div>
        </div>


        {/* ------------------------------------------------
            OPERATOR FORM
        ------------------------------------------------ */}
        <form
          className="operator-form"
          onSubmit={handleSubmit}
        >

          <div className="form-group">
            <label htmlFor="name">
              Name
            </label>

            <input
              id="name"
              name="name"
              type="text"
              placeholder="Example: Rahul Sharma"
              value={formData.name}
              onChange={handleInputChange}
              required
            />
          </div>


          <div className="form-group">
            <label htmlFor="operator_id">
              Operator ID
            </label>

            <input
              id="operator_id"
              name="operator_id"
              type="text"
              placeholder="Example: OP-002"
              value={formData.operator_id}
              onChange={handleInputChange}
              required
            />
          </div>


          <div className="form-group">
            <label htmlFor="email">
              Email
            </label>

            <input
              id="email"
              name="email"
              type="email"
              placeholder="operator@trusttrace.com"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>


          <div className="form-group">
            <label htmlFor="password">
              Password
            </label>

            <input
              id="password"
              name="password"
              type="password"
              placeholder="Enter password"
              value={formData.password}
              onChange={handleInputChange}
              required
            />
          </div>


          <div className="form-group">
            <label htmlFor="role">
              Role
            </label>

            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleInputChange}
              required
            >
              <option value="operator">
                Operator
              </option>

              <option value="inspector">
                Inspector
              </option>
            </select>
          </div>


          <button
            className="primary-button"
            type="submit"
            disabled={submitting}
          >
            {submitting
              ? "Registering..."
              : "Register Operator"}
          </button>

        </form>


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
          REGISTERED OPERATORS SECTION
      -------------------------------------------------- */}
      <div className="content-section">

        <div className="section-header">
          <div>
            <h2>Registered Operators</h2>

            <p>
              Operators and inspectors currently registered
              in the TrustTrace prototype.
            </p>
          </div>

          <div className="record-count">
            {users.length}{" "}
            {users.length === 1 ? "User" : "Users"}
          </div>
        </div>


        {/* ------------------------------------------------
            LOADING STATE
        ------------------------------------------------ */}
        {loading && (
          <div className="state-message">
            Loading operators...
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
          users.length === 0 && (
            <div className="state-message">
              No operators have been registered yet.
            </div>
          )}


        {/* ------------------------------------------------
            OPERATOR TABLE
        ------------------------------------------------ */}
        {!loading &&
          !error &&
          users.length > 0 && (

            <div className="table-container">

              <table className="data-table">

                <thead>
                  <tr>
                    <th>Operator ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                  </tr>
                </thead>

                <tbody>

                  {users.map((user) => (

                    <tr key={user.id}>

                      <td className="piece-id">
                        {user.operator_id}
                      </td>

                      <td>
                        {user.name}
                      </td>

                      <td>
                        {user.email}
                      </td>

                      <td>
                        <span className="role-badge">
                          {user.role}
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

export default Dashboard;