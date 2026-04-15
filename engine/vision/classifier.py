YOLO_TO_CATEGORY = {
    "person": "human_activity",
    "car": "transport",
    "truck": "transport",
    "bus": "transport",
    "train": "transport",
    "bicycle": "transport",
    "motorcycle": "transport",
    "airplane": "transport",
    "boat": "transport",
    "dog": "other",
    "cat": "other"
}

def map_to_categories(results, model):
    names = model.names
    category_counts = {}

    for r in results:
        if r.boxes is None:
            continue

        classes = r.boxes.cls.cpu().numpy()

        for cls_id in classes:
            name = names[int(cls_id)]
            category = YOLO_TO_CATEGORY.get(name, "other")

            category_counts[category] = category_counts.get(category, 0) + 1

    return category_counts