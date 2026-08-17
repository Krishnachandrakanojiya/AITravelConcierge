from app.rag.retriever import RAGRetriever

retriever = RAGRetriever()

docs = retriever.get_all_documents()

for doc in docs:

    print("\nID:", doc["id"])

    print(
        "Content:",
        doc["content"]
    )