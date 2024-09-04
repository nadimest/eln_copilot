from models import Sample, PlateSamples

class PlateSamples:
    def __init__(self, samples):
        self.samples = samples
        self.plate_size = len(samples)

def generate_mockup_data() -> PlateSamples:
    samples = []
    starting_compounds = ["Compound A", "Compound B", "Compound C"]
    processes = ["Process 1", "Process 2", "Process 3"]
    enzymes = ["Enzyme X", "Enzyme Y", "Enzyme Z"]

    for i in range(1, 49):  # 48 samples
        sample_name = f"Sample {i}"
        position = f"{chr(65 + (i - 1) // 8)}{(i - 1) % 8 + 1}"  # A1, A2, ..., F8
        sample = Sample(
            sample_name=sample_name,
            position=position,
            starting_compound=starting_compounds[i % len(starting_compounds)],
            process=processes[i % len(processes)],
            enzyme=enzymes[i % len(enzymes)]
        )
        samples.append(sample)

    return PlateSamples(samples=samples)
