from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
import torch
import numpy as np
import cv2

# Load model
processor = SegformerImageProcessor.from_pretrained("nvidia/segformer-b5-finetuned-cityscapes-1024-1024")
model = SegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b5-finetuned-cityscapes-1024-1024")

def run_segmentation(image):

    image = image.convert("RGB")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits  # (1, num_classes, H, W)

    mask = logits.argmax(dim=1).squeeze().cpu().numpy()

    # Resize mask to original image
    mask = cv2.resize(mask.astype(np.uint8), (image.size[0], image.size[1]))

    image_np = np.array(image)

    # Color map (adjust classes)
    color_map = {
    8: [0,255,0],      # vegetation
    2: [128,128,128],  # building
    0: [0,0,0],        # road
}

    overlay = image_np.copy()

    for k, color in color_map.items():
        overlay[mask == k] = color

    overlay = cv2.addWeighted(image_np, 0.6, overlay, 0.4, 0)

    return {
        "mask": mask,
        "colored_mask": overlay,
        "results": None
    }