import axios from "axios";
import { v4 as uuidv4 } from "uuid";

import Chat from "../models/Chat.js";

export const chat = async (req, res) => {
  try {
    const { sessionId, question } = req.body;

    if (!question || question.trim() === "") {
      return res.status(400).json({
        message: "Question is required.",
      });
    }

    // Generate a new session ID if this is a new conversation
    const currentSessionId = sessionId || uuidv4();

    // Fetch previous messages for this session
    const chats = await Chat.find({
      user: req.user._id,
      sessionId: currentSessionId,
    }).sort({ createdAt: 1 });

    // Convert MongoDB chats to FastAPI chat history format
    const chatHistory = [];

    for (const chat of chats) {
      chatHistory.push({
        role: "user",
        content: chat.question,
      });

      chatHistory.push({
        role: "assistant",
        content: chat.answer,
      });
    }

    // Call FastAPI
    const response = await axios.post(
      `${process.env.AI_SERVICE_URL}/chat`,
      {
        question,
        user_id: req.user._id.toString(),
        chat_history: chatHistory,
      }
    );

    const answer = response.data.answer;

    // Save latest chat
    await Chat.create({
      user: req.user._id,
      sessionId: currentSessionId,
      question,
      answer,
    });

    return res.status(200).json({
      sessionId: currentSessionId,
      answer,
    });
  } catch (error) {
    console.error(
      "Chat Error:",
      error.response?.data || error.message
    );

    return res.status(500).json({
      message: "Failed to generate response.",
    });
  }
};

export const getChatHistory = async (req, res) => {
  try {
    const { sessionId } = req.params;

    const chats = await Chat.find({
      user: req.user._id,
      sessionId,
    }).sort({ createdAt: 1 });

    return res.status(200).json(chats);
  } catch (error) {
    console.error(error);

    return res.status(500).json({
      message: "Failed to fetch chat history.",
    });
  }
};

export const getSessions = async (req, res) => {
  try {
    const sessions = await Chat.aggregate([
      {
        $match: {
          user: req.user._id,
        },
      },
      {
        $sort: {
          createdAt: -1,
        },
      },
      {
        $group: {
          _id: "$sessionId",
          lastQuestion: {
            $first: "$question",
          },
          updatedAt: {
            $first: "$createdAt",
          },
        },
      },
      {
        $sort: {
          updatedAt: -1,
        },
      },
    ]);

    return res.status(200).json(sessions);
  } catch (error) {
    console.error(error);

    return res.status(500).json({
      message: "Failed to fetch sessions.",
    });
  }
};

export const deleteSession = async (req, res) => {
  try {
    const { sessionId } = req.params;

    const result = await Chat.deleteMany({
      user: req.user._id,
      sessionId,
    });

    if (result.deletedCount === 0) {
      return res.status(404).json({
        message: "Session not found.",
      });
    }

    return res.status(200).json({
      message: "Session deleted successfully.",
    });
  } catch (error) {
    console.error(error);

    return res.status(500).json({
      message: "Failed to delete session.",
    });
  }
};