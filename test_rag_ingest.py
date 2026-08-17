import asyncio

from app.rag.ingest import RAGIngestionService


async def main():

    rag = RAGIngestionService()

    text = """
    BankGold gives 4x dining rewards and
    complimentary travel insurance.
    """

    embedding = await rag.embed_text(
        text
    )

    rag.upsert_snippet(
        "card_perks_1",
        text,
        embedding
    )

    print(
        "Embedding Length:",
        len(embedding)
    )

    print(
        "Stored Successfully"
    )


asyncio.run(main())