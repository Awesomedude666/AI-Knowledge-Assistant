import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="flex items-center justify-between bg-white px-8 py-4 shadow">
        <h1 className="text-2xl font-bold">
          AI Knowledge Assistant
        </h1>

        <button
          onClick={handleLogout}
          className="rounded bg-red-500 px-4 py-2 text-white transition hover:bg-red-600"
        >
          Logout
        </button>
      </header>

      <main className="mx-auto mt-12 grid max-w-5xl gap-8 md:grid-cols-3">
        <div
          onClick={() => navigate("/chat")}
          className="cursor-pointer rounded-lg bg-white p-8 shadow transition hover:shadow-lg"
        >
          <h2 className="mb-2 text-xl font-semibold">
            Chat
          </h2>

          <p className="text-gray-600">
            Start chatting with your uploaded documents.
          </p>
        </div>

        <div
          onClick={() => navigate("/documents")}
          className="cursor-pointer rounded-lg bg-white p-8 shadow transition hover:shadow-lg"
        >
          <h2 className="mb-2 text-xl font-semibold">
            Documents
          </h2>

          <p className="text-gray-600">
            View and manage your uploaded PDFs.
          </p>
        </div>

        <div
          onClick={() => navigate("/documents")}
          className="cursor-pointer rounded-lg bg-white p-8 shadow transition hover:shadow-lg"
        >
          <h2 className="mb-2 text-xl font-semibold">
            Upload PDF
          </h2>

          <p className="text-gray-600">
            Upload a new PDF to your knowledge base.
          </p>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;