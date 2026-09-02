from fastapi import FastAPI, HTTPException

from models import (
    LabAnalysisRequest,
    LabAnalysisResponse,
    LabAnalysisResult
)

from agent import analyze_lab_with_mcp


app = FastAPI(
    title="Clinical Lab Results Analyzer",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Clinical Lab Results Analyzer API",
        "status": "running"
    }


@app.post("/analyze_labs", response_model=LabAnalysisResponse)
async def analyze_labs(request: LabAnalysisRequest):

    results = []

    for lab in request.labs:

        try:
            analysis = await analyze_lab_with_mcp(
                lab.test_name,
                lab.value
            )

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        result = LabAnalysisResult(
            test_name=lab.test_name,
            value=lab.value,
            unit=lab.unit,
            status=analysis["status"],
            explanation="Pending LLM explanation",
            next_step=analysis["routing"]
        )

        results.append(result)

    severity_order = {
        "Critical": 1,
        "Warning": 2,
        "Normal": 3
    }

    results.sort(
        key=lambda result: severity_order[result.status]
    )

    return LabAnalysisResponse(
        results=results
    )