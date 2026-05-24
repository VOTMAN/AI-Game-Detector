from typing import List, Tuple
from sqlmodel import SQLModel, Field, Column, JSON

class PredResults(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key = True)
    prediction: str
    confidences: List[Tuple[str, float]] = Field(
        sa_column=Column(JSON)
    )
    frames: List[str] = Field(sa_column=Column(JSON))
    time_taken: float