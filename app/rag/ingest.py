from semantic_kernel.connectors.ai.open_ai import (
    AzureTextEmbedding
)

from azure.cosmos import CosmosClient
from dotenv import load_dotenv

import os

load_dotenv()


class RAGIngestionService:

    def __init__(self):

        self.embedding_service = AzureTextEmbedding(
            deployment_name=os.getenv(
                "AZURE_OPENAI_EMBED_DEPLOYMENT"
            ),
            endpoint=os.getenv(
                "AZURE_OPENAI_ENDPOINT"
            ),
            api_key=os.getenv(
                "AZURE_OPENAI_KEY"
            ),
            api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION"
            )
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

    async def embed_text(
        self,
        text: str
    ):

        result = await self.embedding_service.generate_embeddings(
            [text]
        )

        return result[0]

    def upsert_snippet(
        self,
        item_id: str,
        content: str,
        embedding
    ):

        item = {

            "id": item_id,

            "pk": "travel",

            "content": content,

            "embedding": embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
        }

        self.container.upsert_item(item)

        return item