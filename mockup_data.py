import json
from models import Sample, HeatmapConfig

# Create sample data
samples = [
    Sample(
        sample_name=f"Sample {i+1}",
        position=f"{chr(65 + i // 12)}{i % 12 + 1}",
        starting_compound=f"Compound {(i % 12) + 1}",
        process=f"Process {(i % 3) + 1}",
        enzyme=f"Enzyme {(i % 4) + 1}"
    )
    for i in range(96)
]

# Create heatmap configuration
heatmap_config = HeatmapConfig(
    plate_size=96,
    rows=["A", "B", "C", "D", "E", "F", "G", "H"],
    columns=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    metadata={
        sample.sample_name: {
            "starting_compound": sample.starting_compound,
            "process": sample.process,
            "enzyme": sample.enzyme
        }
        for sample in samples
    }
)

# Convert data to JSON format
mockup_data = {
    "samples": [sample.model_dump() for sample in samples],
    "heatmap_config": heatmap_config.model_dump()
}

# Save mockup data to a JSON file
with open("mockup_data.json", "w") as f:
    json.dump(mockup_data, f, indent=2)

print("Mockup data has been generated and saved to mockup_data.json")
