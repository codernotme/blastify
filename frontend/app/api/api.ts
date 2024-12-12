import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export const uploadFile = async (file: File): Promise<Record<string, unknown>> => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${BASE_URL}/process-file/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    if (file.type === "application/pdf") {
      return {
        fileType: "pdf",
        data: response.data,
      };
    }
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      console.error("Error uploading file:", error.response?.data || error.message);
    } else {
      console.error("Error uploading file:", error);
    }
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
    });
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      console.error("Error sending messages:", error.response?.data || error.message);
    } else {
      console.error("Error sending messages:", error);
    }
    throw error;
  }
};

export const fetchContacts = async (): Promise<{ id: string; name: string; email: string; phone: string }[]> => {
  try {
    const response = await axios.get(`${BASE_URL}/contacts/`);
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      console.error("Error fetching contacts:", error.response?.data || error.message);
    } else {
      console.error("Error fetching contacts:", error);
    }
    throw error;
  }
};
