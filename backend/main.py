from fastapi import FastAPI, HTTPException

from models import (
    LabAnalysisRequest,
    LabAnalysisResponse,
    LabAnalysisResult
)

from agent import analyze_lab_with_mcp
from llm_service import generate_clinical_explanation


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
            # Step 1 + Step 2:
            # MCP classification and severity routing
            analysis = await analyze_lab_with_mcp(
                lab.test_name,
                lab.value
            )

            # Step 3:
            # Gemini generates the clinical explanation
            llm_result = await generate_clinical_explanation(
                test_name=lab.test_name,
                value=lab.value,
                unit=lab.unit,
                status=analysis["status"],
                reference_min=analysis["reference_range"]["min"],
                reference_max=analysis["reference_range"]["max"],
                routing=analysis["routing"]
            )

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"AI analysis failed: {str(e)}"
            )

        result = LabAnalysisResult(
            test_name=lab.test_name,
            value=lab.value,
            unit=lab.unit,
            status=analysis["status"],
            explanation=llm_result["explanation"],
            next_step=llm_result["next_step"]
        )

        results.append(result)

    # Critical → Warning → Normal
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