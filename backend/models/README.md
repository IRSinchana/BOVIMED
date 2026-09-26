# BOVIMED YOLO11 weights

Place the trained Ultralytics checkpoint here as a **single file**:

```
backend/models/best.pt
```

## Important

- `best.pt` must be a PyTorch/Ultralytics weight file (usually several MB), not a folder.
- If you unzipped a `.pt` by mistake, re-export/copy the original `best.pt` from your training `runs/detect/.../weights/best.pt`.

## Classes (BOVIMED trained model)

| ID | Class |
|----|--------|
| 0 | Cow_Feeding |
| 1 | Cow_drinking_water |
| 2 | Cow_lying |
| 3 | Cow_standing |
| 4 | Healthy_udder |
| 5 | Lumpy_infected_cow |
| 6 | Mastitis_infected_udder |

Set `DEMO_MODE=false` in `.env` to use this model for `/api/analyze`.
