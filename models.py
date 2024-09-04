from pydantic import BaseModel, conint, constr
from typing import List, Optional

class Sample(BaseModel):
    sample_name: str
    position: str
    starting_compound: str
    process: str
    enzyme: str

class HeatmapConfig(BaseModel):
    plate_size: conint(ge=1)  # Minimum plate size of 1
    rows: List[constr(min_length=1)]  # List of row labels (e.g., ['A', 'B', 'C'])
    columns: List[constr(min_length=1)]  # List of column labels (e.g., ['1', '2', '3'])
    metadata: Optional[dict] = None  # Optional metadata for the samples

    class Config:
        schema_extra = {
            "example": {
                "plate_size": 96,
                "rows": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "columns": ["1", "2", "3", "4", "5", "6", "7", "8"],
                "metadata": {
                    "Sample 1": {"description": "Control sample", "concentration": 5.0},
                    "Sample 2": {"description": "Test sample", "concentration": 10.0},
                }
            }
        }
