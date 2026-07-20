function Message({ message }) {
  return (
    <div className="mb-6">
      {/* User Message */}
      <div className="flex justify-end mb-2">
        <div className="max-w-2xl rounded-lg bg-blue-600 px-4 py-2 text-white shadow">
          <p className="whitespace-pre-wrap">{message.question}</p>
        </div>
      </div>

      {/* AI Message */}
      <div className="flex justify-start">
        <div className="max-w-2xl rounded-lg bg-gray-200 px-4 py-2 text-gray-900 shadow">
          <p className="whitespace-pre-wrap">{message.answer}</p>
        </div>
      </div>
    </div>
  );
}

export default Message;