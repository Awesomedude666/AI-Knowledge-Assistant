import api from "../api/axios";

export const getSessions = async () => {
  const response = await api.get("/chat");
  return response.data;
};

export const getChatHistory = async (sessionId) => {
  const response = await api.get(`/chat/${sessionId}`);
  return response.data;
};

export const sendMessage = async (sessionId, question) => {
  const response = await api.post("/chat", {
    sessionId,
    question,
  });

  return response.data;
};

export const deleteSession = async (sessionId) => {
  const response = await api.delete(`/chat/${sessionId}`);
  return response.data;
};