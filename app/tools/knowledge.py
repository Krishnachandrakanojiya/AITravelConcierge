from semantic_kernel.functions import kernel_function

from app.rag.retriever import RAGRetriever


class KnowledgeTools:

    @kernel_function(
        name="search_knowledge",
        description="Search travel knowledge base using RAG"
    )
    async def search_knowledge(
        self,
        query: str
    ):

        retriever = RAGRetriever()

        document, score = await retriever.retrieve(query)

        if document is None:
            return {
                "similarity_score": 0.0,
                "document_id": None,
                "content": None
            }

        return {

            "similarity_score":
                float(score),

            "document_id":
                document.get("id"),

            "content":
                document.get("content")
        }