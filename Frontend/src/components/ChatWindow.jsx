import { useEffect, useRef } from "react";
import Message from "./Message";

function ChatWindow({ messages, selectedSession }) {
  const bottomRef = useRef(null);

  // Auto-scroll to the latest message whenever messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  if (!selectedSession) {
    return (
      <div className="flex flex-1 items-center justify-center text-gray-500">
        Select a chat or click <span className="mx-1 font-semibold">New Chat</span>
        to start.
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className="flex flex-1 items-center justify-center text-gray-500">
        No messages yet.
        <br />
        Ask your first question!
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50 p-6">
      {messages.map((message) => (
        <Message
          key={message._id}
          message={message}
        />
      ))}

      <div ref={bottomRef} />
    </div>
  );
}

export default ChatWindow;