import fs from "fs";
import axios from "axios";
import FormData from "form-data";
import mongoose from "mongoose";
import Document from "../models/Document.js";

export const uploadDocument = async (req, res) => {
  let document;

  try {
    if (!req.file) {
      return res.status(400).json({
        message: "No PDF uploaded.",
      });
    }

    document = await Document.create({
      filename: req.file.filename,
      originalFilename: req.file.originalname,
      fileSize: req.file.size,
      user: req.user._id,
      status: "processing",
    });

    const formData = new FormData();

    formData.append(
      "file",
      fs.createReadStream(req.file.path)
    );

    formData.append(
      "user_id",
      req.user._id.toString()
    );

    formData.append("document_id", document._id.toString());

    await axios.post(
      `${process.env.AI_SERVICE_URL}/documents/upload`,
      formData,
      {
        headers: formData.getHeaders(),
      }
    );

    document.status = "completed";
    await document.save();

    return res.status(201).json({
      message: "Document uploaded successfully.",
      documentId: document._id,
    });

  } catch (error) {

    if (document) {
      document.status = "failed";
      await document.save();
    }

    return res.status(500).json({
      message: "Failed to process document.",
    });

  } finally {

    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }

  }
};

export const getDocuments = async (req, res) => {
  try {
    const documents = await Document.find({
      user: req.user._id,
    })
      .sort({ createdAt: -1 });

    return res.status(200).json(documents);
  } catch (error) {
    return res.status(500).json({
      message: "Failed to fetch documents.",
    });
  }
};

export const deleteDocument = async (req, res) => {
  try {


    if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
      return res.status(400).json({
        message: "Invalid document id.",
      });
    }

    const document = await Document.findOne({
      _id: req.params.id,
      user: req.user._id,
    });

    if (!document) {
      return res.status(404).json({
        message: "Document not found.",
      });
    }

   await axios.delete(
  `${process.env.AI_SERVICE_URL}/documents/${req.user._id}/${document._id}`
);
    await document.deleteOne();

    return res.status(200).json({
      message: "Document deleted successfully.",
    });

  } catch (error) {
    return res.status(500).json({
      message: "Failed to delete document.",
  });
  }
};