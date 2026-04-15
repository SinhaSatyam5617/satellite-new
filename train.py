import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
from unet_model import UNet
from dataset import generate_dataset

# -----------------------------
# LOSS
# -----------------------------
def dice_loss(pred, target):
    smooth = 1e-6
    intersection = (pred * target).sum()
    return 1 - (2. * intersection + smooth) / (pred.sum() + target.sum() + smooth)


def combined_loss(pred, target):
    bce = nn.BCELoss()(pred, target)
    return bce + dice_loss(pred, target)


# -----------------------------
# TRAIN
# -----------------------------
def train():

    print("📡 Generating dataset...")
    X, y = generate_dataset(100)

    print("🧠 Preparing tensors...")

    X = torch.tensor(X).permute(0, 3, 1, 2).float()
    y = torch.tensor(y).unsqueeze(1).float()

    dataset = TensorDataset(X, y)

    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size

    train_ds, val_ds = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_ds, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=8)

    model = UNet(in_channels=3)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    best_loss = float("inf")

    for epoch in range(10):
        model.train()
        train_loss = 0

        for xb, yb in train_loader:
            preds = model(xb)
            loss = combined_loss(preds, yb)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        # VALIDATION
        model.eval()
        val_loss = 0

        with torch.no_grad():
            for xb, yb in val_loader:
                preds = model(xb)
                loss = combined_loss(preds, yb)
                val_loss += loss.item()

        print(f"\nEpoch {epoch+1}")
        print(f"Train Loss: {train_loss:.4f}")
        print(f"Val Loss: {val_loss:.4f}")

        # SAVE BEST
        if val_loss < best_loss:
            best_loss = val_loss
            torch.save(model.state_dict(), "model.pth")
            print("✅ Saved best model")

    print("\n🎯 Training complete")


if __name__ == "__main__":
    train()