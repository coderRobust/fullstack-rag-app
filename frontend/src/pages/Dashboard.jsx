import React, { useState } from "react";
import DocumentUploader from "../components/DocumentUploader";
import axios from "axios";

function Dashboard() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    try {
      const res = await axios.post(
        "http://localhost:8000/qa/",
        { question },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );
      setAnswer(res.data.answer);
    } catch (err) {
      alert("Error fetching answer");
    }
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h2 style={{ fontSize: "24px", marginBottom: "20px" }}>
        <strong>Document Dashboard</strong>
      </h2>

      {/* Document Upload Section */}
      <div style={{ marginBottom: "40px" }}>
        <h3 style={{ fontWeight: "bold", marginBottom: "10px" }}>
          Upload a Document (.pdf / .txt)
        </h3>
        <DocumentUploader />
      </div>

      {/* QA Section */}
      <div style={{ borderTop: "1px solid #ccc", paddingTop: "20px" }}>
        <h3 style={{ fontWeight: "bold", marginBottom: "10px" }}>
          Ask a Question
        </h3>
        <input
          type="text"
          placeholder="Type your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{
            padding: "8px",
            width: "60%",
            marginRight: "10px",
            border: "1px solid #999",
            borderRadius: "4px",
          }}
        />
        <button
          onClick={handleAsk}
          style={{
            padding: "8px 16px",
            backgroundColor: "#007BFF",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Ask
        </button>

        {answer && (
          <div
            style={{
              marginTop: "20px",
              padding: "10px",
              border: "1px solid #ddd",
              borderRadius: "5px",
              backgroundColor: "#f9f9f9",
              maxWidth: "700px",
            }}
          >
            <h4 style={{ fontWeight: "bold", marginBottom: "5px" }}>Answer:</h4>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
