import os
import shutil

source = "Data/train"
target = "dataset"

os.makedirs(f"{target}/benign", exist_ok=True)
os.makedirs(f"{target}/malignant", exist_ok=True)

benign_class = ["normal"]
malignant_classes = [
    "adenocarcinoma",
    "large.cell.carcinoma",
    "squamous.cell.carcinoma"
]

for folder in os.listdir(source):
    folder_path = os.path.join(source, folder)

    for img in os.listdir(folder_path):
        src = os.path.join(folder_path, img)

        if folder in benign_class:
            dst = os.path.join(target, "benign", img)
        else:
            dst = os.path.join(target, "malignant", img)

        shutil.copy(src, dst)

print("✅ Conversion Done!")