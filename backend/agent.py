import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def analyze_lab_with_mcp(test_name: str, value: float):

    server_params = StdioServerParameters(
    command=sys.executable,
    args=["mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            # Step 1: Classify the laboratory result
            classification = await session.call_tool(
                "classify_lab_result",
                arguments={
                    "test_name": test_name,
                    "value": value
                }
            )

            classification_data = classification.content[0].text

            import json

            classification_data = json.loads(classification_data)

            if "error" in classification_data:
                raise ValueError(classification_data["error"])

            status = classification_data["status"]

            # Step 2: Route according to severity
            routing = await session.call_tool(
                "route_by_severity",
                arguments={
                    "status": status
                }
            )

            routing_data = routing.content[0].text
            routing_data = json.loads(routing_data)

            if "error" in routing_data:
                raise ValueError(routing_data["error"])

            return {
                "test_name": test_name,
                "value": value,
                "status": status,
                "reference_range": classification_data["reference_range"],
                "routing": routing_data["routing"]
            }


if __name__ == "__main__":

    result = asyncio.run(
        analyze_lab_with_mcp(
            "Glucose",
            180
        )
    )

    print("\nMCP Agent Analysis:")
    print(result)