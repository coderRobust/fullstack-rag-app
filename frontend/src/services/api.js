import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // Update if running behind proxy

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export const uploadDocument = async (file) => {
  const token = localStorage.getItem("access_token");
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await apiClient.post("/documents/upload", formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Upload failed:", error.response?.data || error.message);
    throw error;
  }
};
