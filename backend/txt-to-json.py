import os
import json

IMAGE_DIR = "C:/nus_adv/train"
captions = {}

for file in os.listdir(IMAGE_DIR):
    if file.endswith(".png") or file.endswith(".jpg"):
        base = os.path.splitext(file)[0]
        txt_file = os.path.join(IMAGE_DIR, base + ".txt")

        if os.path.exists(txt_file):
            with open(txt_file, "r", encoding="utf-8") as f:
                description = f.read().strip()
            captions[file] = description
        else:
            print(f"No caption for: {file}")

# Save JSON
output_path = os.path.join("C:/nus_adv", "captions.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(captions, f, indent=2)

print(f"captions.json saved at {output_path}")
