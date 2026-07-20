import { useEffect, useState } from "react";

import {
  uploadDocument,
  getDocuments,
  deleteDocument,
} from "../services/documentService";

function Documents() {
  const [documents, setDocuments] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      alert("Failed to fetch documents.");
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a PDF.");
      return;
    }

    try {
      setLoading(true);

      await uploadDocument(selectedFile);

      setSelectedFile(null);

      await fetchDocuments();

      alert("Document uploaded successfully.");
    } catch (error) {
      alert(
        error.response?.data?.message ||
          "Upload failed."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteDocument(id);

      await fetchDocuments();
    } catch (error) {
      alert("Delete failed.");
    }
  };

  return (
    <div className="mx-auto max-w-5xl p-10">
      <h1 className="mb-8 text-3xl font-bold">
        Documents
      </h1>

      <div className="mb-8 flex gap-4">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) =>
            setSelectedFile(e.target.files[0])
          }
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="rounded bg-blue-600 px-6 py-2 text-white"
        >
          {loading ? "Uploading..." : "Upload"}
        </button>
      </div>

      <div className="space-y-4">
        {documents.map((document) => (
          <div
            key={document._id}
            className="flex items-center justify-between rounded border bg-white p-4 shadow"
          >
            <div>
              <h2 className="font-semibold">
                {document.originalFilename}
              </h2>

              <p className="text-sm text-gray-500">
                {(document.fileSize / 1024).toFixed(2)} KB
              </p>
            </div>

            <button
              onClick={() =>
                handleDelete(document._id)
              }
              className="rounded bg-red-500 px-4 py-2 text-white"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Documents;