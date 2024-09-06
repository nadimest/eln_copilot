from pydantic import BaseModel, Field
from typing import List, Optional

class Sample(BaseModel):
    sample_name: str
    position: str
    starting_compound: str
    process: str
    enzyme: str

class HeatmapConfig(BaseModel):
    plate_size: int = Field(description="Minimum plate size of 1")
    rows: List[str] = Field(description="List of row labels (e.g., ['A', 'B', 'C'])")
    columns: List[str] = Field(description="List of column labels (e.g., ['1', '2', '3'])")
    metadata: dict = Field(description="Metadata for the samples")

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

class ExperimentOutput(BaseModel):
    plate_size: int = Field(description="Minimum plate size of 1")
    rows: List[str] = Field(description="List of row labels (e.g., ['A', 'B', 'C'])")
    columns: List[str] = Field(description="List of column labels (e.g., ['1', '2', '3'])")
    samples: List[Sample] = Field(..., description="List of samples in the experiment")
    #heatmap_config: HeatmapConfig = Field(..., description="Configuration for the heatmap")