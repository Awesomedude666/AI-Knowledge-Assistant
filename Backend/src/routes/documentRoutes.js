import express from "express";

import protect from "../middleware/authMiddleware.js";
import upload from "../middleware/uploadMiddleware.js";

import { uploadDocument, getDocuments , deleteDocument} from "../controllers/documentController.js";

const router = express.Router();

router.post(
  "/upload",
  protect,
  upload.single("file"),
  uploadDocument
);

router.get(
    "/",
    protect,
    getDocuments
);

router.delete(
  "/:id",
  protect,
  deleteDocument
);

export default router;