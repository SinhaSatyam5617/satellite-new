import torch
import numpy as np
import cv2
from unet_model import UNet

def load_model():
    model = UNet()
    model.load_state_dict(torch.load("model.pth", map_location="cpu"))
    model.eval()
    return model


def predict_on_patch(model, img_np):
    img_np = cv2.resize(img_np, (64, 64))

    x = torch.tensor(img_np).permute(2, 0, 1).unsqueeze(0).float()
    pred = model(x)

    return pred.squeeze().detach().numpy()