## Instructions for Parsing Experimental Data

### Overview
You are running experiments to study reactions between a starting compound and enzymes within eppendorf tubes arranged on a 6x8 tube rack. Each experiment varies based on:
- The type of enzyme used.
- The starting compound.
- The processing parameters.

### Rack Layout
- The rack has 6 rows (A to F) and 8 columns (1 to 8).
- The first 3 rows (A, B, C) use Enzyme 1.
- The last 3 rows (D, E, F) use Enzyme 2.
  
### Experimental Design
- Each experiment is run in triplicates.
- Columns alternate between starting compounds:
  - Columns 1, 3, 5, 7: Starting Compound 1.
  - Columns 2, 4, 6, 8: Starting Compound 2.
- Three different processes are used:
  - Process A: 30 min @ 45°C (columns 1 and 2).
  - Process B: 60 min @ 45°C (columns 3 and 4).
  - Process C: 30 min @ 50°C (columns 5 and 6).

### Initial Example Rack Layout and Experimental Design
```
| Experiment ID | Enzyme | Process          | Starting Compound | Rack ID | Position | Yield (%) |
|---------------|--------|------------------|-------------------|---------|----------|-----------|
| 1             | Enz1   | A (30 min @ 45°C)| Compound I        | RACK001 | A1       |           |
| 1             | Enz1   | A (30 min @ 45°C)| Compound I        | RACK001 | A2       |           |
| 1             | Enz1   | A (30 min @ 45°C)| Compound I        | RACK001 | A3       |           |
| 2             | Enz1   | A (30 min @ 45°C)| Compound II       | RACK001 | A4       |           |
| 2             | Enz1   | A (30 min @ 45°C)| Compound II       | RACK001 | A5       |           |
| 2             | Enz1   | A (30 min @ 45°C)| Compound II       | RACK001 | A6       |           |
| 3             | Enz1   | B (60 min @ 45°C)| Compound I        | RACK001 | A7       |           |
| 3             | Enz1   | B (60 min @ 45°C)| Compound I        | RACK001 | A8       |           |
| 3             | Enz1   | B (60 min @ 45°C)| Compound I        | RACK001 | B1       |           |
| 4             | Enz1   | B (60 min @ 45°C)| Compound II       | RACK001 | B2       |           |
| 4             | Enz1   | B (60 min @ 45°C)| Compound II       | RACK001 | B3       |           |
| 4             | Enz1   | B (60 min @ 45°C)| Compound II       | RACK001 | B4       |           |
| 5             | Enz1   | C (30 min @ 50°C)| Compound I        | RACK001 | B5       |           |
| 5             | Enz1   | C (30 min @ 50°C)| Compound I        | RACK001 | B6       |           |
| 5             | Enz1   | C (30 min @ 50°C)| Compound I        | RACK001 | B7       |           |
| 6             | Enz1   | C (30 min @ 50°C)| Compound II       | RACK001 | B8       |           |
| 6             | Enz1   | C (30 min @ 50°C)| Compound II       | RACK001 | C1       |           |
| 6             | Enz1   | C (30 min @ 50°C)| Compound II       | RACK001 | C2       |           |
| 7             | Enz2   | A (30 min @ 45°C)| Compound I        | RACK001 | C3       |           |
| 7             | Enz2   | A (30 min @ 45°C)| Compound I        | RACK001 | C4       |           |
| 7             | Enz2   | A (30 min @ 45°C)| Compound I        | RACK001 | C5       |           |
...
```
### Generalize the Template

```
| Experiment ID | Enzyme | Process          | Starting Compound | Rack ID | Position | Yield (%) |
|---------------|--------|------------------|-------------------|---------|----------|-----------|
| X1            | Enz1   | Process A        | Compound I        | RACK001 | Position1|           |
| X1            | Enz1   | Process A        | Compound I        | RACK001 | Position2|           |
| X1            | Enz1   | Process A        | Compound I        | RACK001 | Position3|           |
| X2            | Enz1   | Process A        | Compound II       | RACK001 | Position4|           |
| X2            | Enz1   | Process A        | Compound II       | RACK001 | Position5|           |
| X2            | Enz1   | Process A        | Compound II       | RACK001 | Position6|           |
...
```

### User Input
Users can define their own experimental designs and rack layouts using their language. The LLM will parse these inputs to generate the table structure similar to the example provided.

Please input your own experimental setup using your specific parameters and conditions.

### Example User Input
```
I'm running experiments with a different setup. I have a 5x10 tube rack.

Experiment:
- Enzyme A in rows 1, 2
- Enzyme B in rows 3, 4, 5
- Starting Compound X in even columns
- Starting Compound Y in odd columns
- Processes:
  - P1: 15 min @ 40°C (cols 1, 2)
  - P2: 30 min @ 45°C (cols 3, 4)
  - P3: 45 min @ 50°C (cols 5, 6)

Setup the experiments in duplicates and provide a table template for adding yield values.
```

The LLM will then parse this user input and generate the corresponding table.