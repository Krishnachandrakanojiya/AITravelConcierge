from azure.cosmos import CosmosClient
from dotenv import load_dotenv

import os

load_dotenv()


class CosmosMemory:

    def __init__(self):

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

    def add_memory(
        self,
        memory_id,
        content
    ):

        item = {
            "id": memory_id,
            "pk": memory_id,
            "content": content
        }

        self.container.upsert_item(item)

    def get_memory(
        self,
        memory_id
    ):

        return self.container.read_item(
            item=memory_id,
            partition_key=memory_id
        )