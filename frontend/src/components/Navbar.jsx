import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("access_token"); // ✅ match Login.jsx
    navigate("/");
  };

  return (
    <nav
      style={{
        background: "#333",
        color: "white",
        padding: "10px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <div>
        <Link to="/dashboard" style={{ color: "white", marginRight: "20px" }}>
          Dashboard
        </Link>
        <Link to="/qa" style={{ color: "white", marginRight: "20px" }}>
          Q&A
        </Link>
      </div>
      <button
        onClick={logout}
        style={{
          background: "red",
          color: "white",
          border: "none",
          padding: "5px 10px",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </nav>
  );
}

export default Navbar;
