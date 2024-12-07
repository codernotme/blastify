import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api"; // Ensure this URL is correct and the server is running

export const uploadFile = async (formData: FormData, file: File) => {
  formData.append("file", file);

  try {
    const response = await axios.post(`${BASE_URL}/process-file/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 5000, // 5 seconds timeout
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading file:", error);
    throw error;
  }
};

export const sendMessages = async (payload: {
  contacts: { value: string }[];
  message: string;
  method: string;
}): Promise<Record<string, unknown>> => {
  try {
    const response = await axios.post(`${BASE_URL}/send-messages/`, payload, {
      headers: {
        "Content-Type": "application/json",
      },
      timeout: 5000, // 5 seconds timeout
    });
    return response.data;
  } catch (error) {
    console.error("Error sending messages:", error);
    throw error;
  }
};
