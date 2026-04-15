import pandas as pd

# -----------------------------
# LOAD FILES (same folder)
# -----------------------------
synthetic_df = pd.read_csv("final_environment_dataset.csv")
real_df = pd.read_csv("real_partial_dataset.csv")

# -----------------------------
# MATCH COLUMNS (IMPORTANT)
# -----------------------------
real_df = real_df[synthetic_df.columns]

# -----------------------------
# CONCAT
# -----------------------------
final_df = pd.concat([synthetic_df, real_df], ignore_index=True)

# -----------------------------
# SHUFFLE
# -----------------------------
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

# -----------------------------
# SAVE FINAL
# -----------------------------
final_df.to_csv("final_dataset_for_risk.csv", index=False)

print("✅ Final dataset saved: final_dataset_for_risk.csv")
print("Shape:", final_df.shape)