from mcp.server import MCPServer

from classifier import classify_lab


# Create MCP server
mcp = MCPServer("Clinical Lab Analyzer")


@mcp.tool()
def classify_lab_result(test_name: str, value: float) -> dict:
    """Classify a laboratory result as Normal, Warning, or Critical."""

    try:
        result = classify_lab(test_name, value)

        return {
            "test_name": test_name,
            "value": value,
            "status": result["status"],
            "reference_range": result["reference_range"]
        }

    except ValueError as e:
        return {
            "error": str(e)
        }


@mcp.tool()
def route_by_severity(status: str) -> dict:
    """Route a laboratory result according to its severity."""

    routing = {
        "Critical": "Immediate attention required",
        "Warning": "Further review recommended",
        "Normal": "No abnormality detected"
    }

    if status not in routing:
        return {
            "error": f"Invalid status: {status}"
        }

    return {
        "status": status,
        "routing": routing[status]
    }


if __name__ == "__main__":
    mcp.run()