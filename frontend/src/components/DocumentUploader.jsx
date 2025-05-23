import React, { useState } from "react";
import { uploadDocument } from "../services/api";

function DocumentUploader() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please choose a file first.");
      return;
    }
    try {
      setStatus("Uploading...");
      await uploadDocument(file);
      setStatus("✅ Upload successful");
    } catch (err) {
      setStatus("❌ Upload failed");
    }
  };

  return (
    <div>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ marginBottom: "10px" }}
      />
      <br />
      <button
        onClick={handleUpload}
        style={{
          padding: "8px 16px",
          backgroundColor: "#28a745",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Upload
      </button>
      <p style={{ marginTop: "10px", fontStyle: "italic" }}>{status}</p>
    </div>
  );
}

export default DocumentUploader;
