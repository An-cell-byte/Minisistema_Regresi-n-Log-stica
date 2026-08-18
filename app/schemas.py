from typing import Literal

from pydantic import BaseModel, Field


class CustomerFeatures(BaseModel):
    age: int = Field(ge=18, le=100)
    job: Literal[
        "admin.", "blue-collar", "entrepreneur", "housemaid", "management",
        "retired", "self-employed", "services", "student", "technician",
        "unemployed", "unknown",
    ]
    marital: Literal["married", "single", "divorced"]
    education: Literal["primary", "secondary", "tertiary", "unknown"]
    balance: float = Field(ge=-1000000, le=10000000)
    housing: Literal["yes", "no"]
    loan: Literal["yes", "no"]
    campaign: int = Field(ge=1, le=100)


class PredictionResponse(BaseModel):
    prediction: Literal["yes", "no"]
    probability: float
    classification: str
