import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import {
  getSessions,
  getChatHistory,
  sendMessage,
  deleteSession,
} from "../services/chatService";

function Chat() {
  const [sessions, setSessions] = useState([]);
  const [messages, setMessages] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isNewChat, setIsNewChat] = useState(false);

  // Fetch all chat sessions
  const fetchSessions = async () => {
    try {
      const data = await getSessions();

      setSessions(data);

      // Auto-open latest session only if the user
      // isn't creating a new chat.
      if (!selectedSession && !isNewChat && data.length > 0) {
        await fetchChatHistory(data[0]._id);
      }
    } catch (error) {
      console.error(error);
      alert("Failed to load chat sessions.");
    }
  };

  // Fetch chat history
  const fetchChatHistory = async (sessionId) => {
    try {
      const data = await getChatHistory(sessionId);

      setMessages(data);
      setSelectedSession(sessionId);
      setIsNewChat(false);
    } catch (error) {
      console.error(error);
      alert("Failed to load chat history.");
    }
  };

  // Start a new chat
  const handleNewChat = () => {
    setSelectedSession(null);
    setMessages([]);
    setIsNewChat(true);
  };

  // Send a message
  const handleSendMessage = async (question) => {
    try {
      setLoading(true);

      const response = await sendMessage(selectedSession, question);

      const currentSessionId = response.sessionId || selectedSession;

      setSelectedSession(currentSessionId);
      setIsNewChat(false);

      await fetchChatHistory(currentSessionId);
      await fetchSessions();
    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.message ||
          "Failed to send message."
      );
    } finally {
      setLoading(false);
    }
  };

  // Delete a chat session
  const handleDeleteSession = async (sessionId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this conversation?"
    );

    if (!confirmed) return;

    try {
      await deleteSession(sessionId);

      // If the currently open chat was deleted,
      // clear the chat window.
      if (selectedSession === sessionId) {
        setSelectedSession(null);
        setMessages([]);
        setIsNewChat(false);
      }

      const updatedSessions = await getSessions();

      setSessions(updatedSessions);

      // Automatically open the latest remaining session
      if (updatedSessions.length > 0) {
        await fetchChatHistory(updatedSessions[0]._id);
      } else {
        setSelectedSession(null);
        setMessages([]);
      }
    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.message ||
          "Failed to delete chat."
      );
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar
        sessions={sessions}
        selectedSession={selectedSession}
        onSelectSession={fetchChatHistory}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
      />

      <div className="flex flex-1 flex-col">
        <div className="border-b bg-white px-6 py-4 shadow-sm">
          <h1 className="text-xl font-semibold">
            AI Knowledge Assistant
          </h1>
        </div>

        <ChatWindow
          messages={messages}
          selectedSession={selectedSession || isNewChat}
        />

        <ChatInput
          onSend={handleSendMessage}
          loading={loading}
        />
      </div>
    </div>
  );
}

export default Chat;