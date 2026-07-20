import { useState } from "react";

function ChatInput({ onSend, loading }) {
  const [question, setQuestion] = useState("");

  const handleSend = () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    onSend(trimmedQuestion);
    setQuestion("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="border-t bg-white p-4">
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Ask anything about your documents..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          className="flex-1 rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-blue-500"
        />

        <button
          onClick={handleSend}
          disabled={loading}
          className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatInput;