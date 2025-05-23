import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import QA from "./pages/QA";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>
      <Navbar /> {/* Add here to show on all pages */}
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/qa" element={<QA />} />
      </Routes>
    </Router>
  );
}

export default App;

