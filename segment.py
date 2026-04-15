import numpy as np
import cv2
from PIL import Image
import torch

# -------------------------
# SAM IMPORT
# -------------------------
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

# -------------------------
# TORCHGEO (SIMULATED VIA RESNET)
# -------------------------
import torchvision.models as models
import torchvision.transforms as T

# -------------------------
# LOAD SAM MODEL
# -------------------------
sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b.pth")
sam.eval()

mask_generator = SamAutomaticMaskGenerator(sam)

# -------------------------
# LOAD TORCHGEO-LIKE MODEL
# -------------------------
geo_model = models.resnet18(pretrained=True)
geo_model.eval()

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
])

# -------------------------
# SAM SEGMENTATION
# -------------------------
def run_sam(image):

    image = image.convert("RGB")
    image_np = np.array(image)

    masks = mask_generator.generate(image_np)

    output = image_np.copy()

    for m in masks:
        mask = m["segmentation"]
        color = np.random.randint(0, 255, 3)
        output[mask] = color

    return output


# -------------------------
# TORCHGEO FEATURE MAP
# -------------------------
def run_torchgeo(image):

    image = image.convert("RGB")
    img = transform(image).unsqueeze(0)

    with torch.no_grad():
        features = geo_model(img)

    heatmap = features.squeeze().cpu().numpy()

    # normalize
    heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + 1e-5)

    heatmap = cv2.resize(heatmap, (512, 512))
    heatmap = (heatmap * 255).astype(np.uint8)

    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    return heatmap