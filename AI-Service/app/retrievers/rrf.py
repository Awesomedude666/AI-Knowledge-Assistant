from collections import defaultdict

from langchain_core.documents import Document


def reciprocal_rank_fusion(
    ranked_lists: list[list[Document]],
    k: int = 60,
) -> list[Document]:
 
    scores = defaultdict(float)
    documents = {}

    for ranked_list in ranked_lists:

        for rank, document in enumerate(ranked_list, start=1):

            chunk_id = document.metadata["chunk_id"]

            scores[chunk_id] += 1 / (k + rank)

            documents[chunk_id] = document

    ranked_chunk_ids = sorted(
        scores,
        key=lambda chunk_id: scores[chunk_id],
        reverse=True,
    )

    return [
        documents[chunk_id]
        for chunk_id in ranked_chunk_ids
    ]