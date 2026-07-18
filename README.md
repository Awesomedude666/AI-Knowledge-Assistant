# AI-Knowledge-Assistant


















## Performance Benchmarks

Test Setup
- 82 document chunks
- Gemini 2.5 Flash
- Gemini Embedding 001
- CrossEncoder: ms-marco-MiniLM-L-6-v2
- ChromaDB + BM25 Hybrid Retrieval
- Intel i5-12450H CPU

Average Latency

History Retriever          : 1.90 s
Multi Query Generation     : 1.31 s
Hybrid Retrieval (5 queries): 3.09 s
CrossEncoder Reranking     : 1.65 s
Answer Generation          : 2.77 s

Total End-to-End           : 10.75 s