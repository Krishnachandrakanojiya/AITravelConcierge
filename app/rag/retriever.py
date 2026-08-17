from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding

import os
import math
import asyncio


load_dotenv()


class RAGRetriever:
    """
    RAGRetriever is responsible for:
    1. Connecting to Cosmos DB
    2. Connecting to Azure OpenAI embedding deployment
    3. Creating query embeddings
    4. Reading stored embedded documents from Cosmos DB
    5. Calculating cosine similarity
    6. Returning the most relevant document
    """

    def __init__(self):
        """
        Initialize Cosmos DB client and Azure embedding service.
        All credentials are loaded from .env.
        """

        self.embedding_service = AzureTextEmbedding(
            deployment_name=os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )

        self.client = CosmosClient(
            os.getenv("COSMOS_ENDPOINT"),
            credential=os.getenv("COSMOS_KEY")
        )

        self.database = self.client.get_database_client(
            os.getenv("COSMOS_DB")
        )

        self.container = self.database.get_container_client(
            os.getenv("COSMOS_CONTAINER")
        )

    async def create_query_embedding(self, query: str):
        """
        Generate embedding vector for the user query using Azure OpenAI embedding model.
        """

        result = await self.embedding_service.generate_embeddings(
            [query]
        )

        embedding = result[0]

        return list(embedding)

    def get_all_documents(self):
        """
        Retrieve all documents from Cosmos DB container.
        """

        query = "SELECT * FROM c"

        results = list(
            self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            )
        )

        return results

    def cosine_similarity(self, vector_a, vector_b):
        """
        Calculate cosine similarity between two vectors.
        Higher score means more similar.
        """

        dot_product = sum(
            a * b for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(
            sum(a * a for a in vector_a)
        )

        magnitude_b = math.sqrt(
            sum(b * b for b in vector_b)
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0

        return dot_product / (magnitude_a * magnitude_b)

    async def retrieve(self, query: str):
        """
        Main retrieval method:
        1. Generate query embedding
        2. Load all stored documents
        3. Compare query embedding with stored document embeddings
        4. Return best matching document and similarity score
        """

        print("Generating query embedding...")

        query_embedding = await self.create_query_embedding(query)

        print("Query embedding generated.")
        print("Query embedding length:", len(query_embedding))

        documents = self.get_all_documents()

        best_document = None
        best_score = -1

        print()
        print("Executing similarity search over Cosmos DB documents...")

        for document in documents:

            if "embedding" not in document:
                print(
                    f"Skipping document without embedding: {document.get('id')}"
                )
                continue

            document_embedding = document["embedding"]

            score = self.cosine_similarity(
                query_embedding,
                document_embedding
            )

            print(
                f"Document ID: {document.get('id')} | Similarity Score: {score}"
            )

            if score > best_score:
                best_score = score
                best_document = document

        return best_document, best_score


async def main():
    """
    Local test runner.
    Run using:
        python -m app.rag.retriever
    """

    retriever = RAGRetriever()

    query = "Which card gives dining rewards?"

    document, score = await retriever.retrieve(query)

    print()
    print("====================================")
    print("RAG RETRIEVAL RESULT")
    print("====================================")

    print("User Query:", query)
    print("Best Similarity Score:", score)

    if document:
        print("Best Document ID:", document.get("id"))
        print("Partition Key:", document.get("pk"))
        print()
        print("Retrieved Content:")
        print(document.get("content"))
    else:
        print("No matching document found.")


if __name__ == "__main__":
    asyncio.run(main())