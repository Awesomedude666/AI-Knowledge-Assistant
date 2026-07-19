import express from "express";

import { chat, getChatHistory, getSessions , deleteSession} from "../controllers/chatController.js";
import protect  from "../middleware/authMiddleware.js";

const router = express.Router();

router.post("/", protect, chat);
router.get("/", protect, getSessions);
router.get("/:sessionId", protect, getChatHistory);
router.delete("/:sessionId", protect, deleteSession);

export default router;