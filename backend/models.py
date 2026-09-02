from pydantic import BaseModel, Field
from typing import List


class LabResult(BaseModel):
    test_name: str = Field(..., min_length=1)
    value: float
    unit: str = Field(..., min_length=1)


class LabAnalysisRequest(BaseModel):
    labs: List[LabResult]


class LabAnalysisResult(BaseModel):
    test_name: str
    value: float
    unit: str
    status: str
    explanation: str
    next_step: str


class LabAnalysisResponse(BaseModel):
    results: List[LabAnalysisResult]