from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI Knowledge Assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context,
reply with:

"I couldn't find the answer in the uploaded documents."

Do not use outside knowledge.

Keep your answers clear and concise.

Context:
{context}
            """,
        ),

        (
            "human",
            "{question}",
        ),
    ]
)