import os

from dotenv import load_dotenv
from semantic_kernel.functions import kernel_function

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import MessageRole, BingGroundingTool


load_dotenv()


class SearchTools:
    """
    SearchTools performs live travel search using Azure AI Agents
    with Grounding with Bing Search.
    """

    @kernel_function(
        name="search_web",
        description="Search live travel information using Azure AI Agent with Bing grounding"
    )
    def search_web(
        self,
        query: str
    ) -> list:

        try:
            project_endpoint = os.getenv("PROJECT_ENDPOINT")
            model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")
            bing_connection_id = os.getenv("BING_CONNECTION_ID")
            bing_connection_name = os.getenv("BING_CONNECTION_NAME")

            if not project_endpoint:
                return [
                    {
                        "title": "Configuration error",
                        "url": "N/A",
                        "snippet": "PROJECT_ENDPOINT is missing."
                    }
                ]

            if not model_deployment:
                return [
                    {
                        "title": "Configuration error",
                        "url": "N/A",
                        "snippet": "MODEL_DEPLOYMENT_NAME is missing."
                    }
                ]

            credential = DefaultAzureCredential()

            # Prefer direct connection ID if available.
            # Otherwise retrieve connection ID from Foundry connection name.
            if not bing_connection_id:
                if not bing_connection_name:
                    return [
                        {
                            "title": "Configuration error",
                            "url": "N/A",
                            "snippet": "Set either BING_CONNECTION_ID or BING_CONNECTION_NAME in .env."
                        }
                    ]

                project_client = AIProjectClient(
                    endpoint=project_endpoint,
                    credential=credential
                )

                with project_client:
                    connection = project_client.connections.get(
                        bing_connection_name
                    )

                    bing_connection_id = connection.id

            bing_tool = BingGroundingTool(
                connection_id=bing_connection_id
            )

            results = []

            with AgentsClient(
                endpoint=project_endpoint,
                credential=credential
            ) as agents_client:

                agent = agents_client.create_agent(
                    model=model_deployment,
                    name="travel-bing-search-agent",
                    instructions=(
                        "You are a travel search assistant. "
                        "Use Bing grounding to find current travel information. "
                        "Return concise results with titles, URLs, and snippets."
                    ),
                    tools=bing_tool.definitions
                )

                try:
                    thread = agents_client.threads.create()

                    agents_client.messages.create(
                        thread_id=thread.id,
                        role=MessageRole.USER,
                        content=query
                    )

                    run = agents_client.runs.create_and_process(
                        thread_id=thread.id,
                        agent_id=agent.id
                    )

                    if str(run.status).lower() == "failed":
                        return [
                            {
                                "title": "Bing search failed",
                                "url": "N/A",
                                "snippet": str(run.last_error)
                            }
                        ]

                    response_message = agents_client.messages.get_last_message_by_role(
                        thread_id=thread.id,
                        role=MessageRole.AGENT
                    )

                    if not response_message:
                        return [
                            {
                                "title": "No response",
                                "url": "N/A",
                                "snippet": "Bing grounded agent returned no message."
                            }
                        ]

                    response_parts = []

                    for text_message in response_message.text_messages:
                        response_parts.append(
                            text_message.text.value
                        )

                    response_text = " ".join(response_parts)

                    for annotation in response_message.url_citation_annotations:
                        citation = annotation.url_citation

                        results.append(
                            {
                                "title": citation.title,
                                "url": citation.url,
                                "snippet": annotation.text or response_text[:250]
                            }
                        )

                    if not results:
                        results.append(
                            {
                                "title": "Bing grounded response",
                                "url": "N/A",
                                "snippet": response_text
                            }
                        )

                    return results[:5]

                finally:
                    agents_client.delete_agent(
                        agent.id
                    )

        except Exception as error:
            return [
                {
                    "title": "Bing search error",
                    "url": "N/A",
                    "snippet": str(error)
                }
            ]