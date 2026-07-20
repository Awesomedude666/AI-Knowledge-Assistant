import { Trash2 } from "lucide-react";

function Sidebar({
  sessions,
  selectedSession,
  onSelectSession,
  onNewChat,
  onDeleteSession,
}) {
  return (
    <div className="flex h-full w-72 flex-col border-r bg-gray-100">
      <div className="border-b p-4">
        <h2 className="mb-4 text-xl font-bold">
          Chats
        </h2>

        <button
          onClick={onNewChat}
          className="w-full rounded-lg bg-blue-600 py-2 font-medium text-white hover:bg-blue-700"
        >
          + New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 ? (
          <p className="p-4 text-sm text-gray-500">
            No chat sessions yet.
          </p>
        ) : (
          sessions.map((session) => (
            <div
              key={session._id}
              className={`flex items-center justify-between border-b p-4 transition ${
                selectedSession === session._id
                  ? "bg-blue-100"
                  : "hover:bg-gray-200"
              }`}
            >
              <div
                className="flex-1 cursor-pointer"
                onClick={() =>
                  onSelectSession(session._id)
                }
              >
                <p className="truncate font-medium">
                  {session.lastQuestion ||
                    "New Conversation"}
                </p>

                <p className="mt-1 text-xs text-gray-500">
                  {new Date(
                    session.updatedAt
                  ).toLocaleString()}
                </p>
              </div>

              <button
                onClick={() =>
                  onDeleteSession(session._id)
                }
                className="ml-2 rounded p-2 text-red-500 hover:bg-red-100"
              >
                <Trash2 size={18} />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Sidebar;