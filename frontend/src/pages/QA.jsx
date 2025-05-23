import React, { useState } from "react";
import axios from "axios";

function QA() {
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
        Ask a Question (RAG)
      </h2>
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Type your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{
            width: "60%",
            padding: "10px",
            border: "1px solid #ccc",
            borderRadius: "5px",
            marginRight: "10px",
          }}
        />
        <button
          onClick={handleAsk}
          style={{
            padding: "10px 20px",
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Ask
        </button>
      </div>
      {answer && (
        <div
          style={{
            marginTop: "20px",
            backgroundColor: "#f0f0f0",
            padding: "20px",
            borderRadius: "5px",
            maxWidth: "700px",
          }}
        >
          <h4 style={{ marginBottom: "10px" }}>Answer:</h4>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default QA;
