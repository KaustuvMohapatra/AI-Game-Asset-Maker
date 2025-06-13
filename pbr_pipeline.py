# pbr_pipeline.py

from PIL import Image, ImageChops, ImageFilter
import os
import cv2
import numpy as np
import torch
import torchvision.transforms as T
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from transformers import DPTFeatureExtractor, DPTForDepthEstimation
from PIL import Image as PILImage

def make_image_seamless(input_image_path):
    print(f"✅ In Function")
    # Load image
    img = Image.open(input_image_path).convert("RGB")
    width, height = img.size

    # Offset the image by 50% in both directions
    offset_img = ImageChops.offset(img, width // 2, height // 2)

    # Slight blur to blend the seams (placeholder for inpainting)
    blended_img = offset_img.filter(ImageFilter.GaussianBlur(radius=1.5))

    # Prepare output path
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    output_path = os.path.join("output", f"{base_name}_Albedo.jpg")

    # Save result
    blended_img.save(output_path)
    print(f"✅ Seamless Albedo saved at: {output_path}")




def generate_pbr_from_albedo(input_image_path):
    print("🤖 [AI] Generating PBR maps from Albedo...")

    # Load image with PIL and convert to RGB
    pil_image = PILImage.open(input_image_path).convert("RGB")

    # Load MiDaS model + feature extractor
    feature_extractor = DPTFeatureExtractor.from_pretrained("Intel/dpt-hybrid-midas")
    model = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas")
    model.eval()

    # Prepare input
    inputs = feature_extractor(images=pil_image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_depth = outputs.predicted_depth

    # Resize to original image size
    depth = torch.nn.functional.interpolate(
        predicted_depth.unsqueeze(1),
        size=pil_image.size[::-1],  # (height, width)
        mode="bicubic",
        align_corners=False
    ).squeeze().cpu().numpy()

    # Normalize depth
    depth_normalized = cv2.normalize(depth, None, 0, 1, cv2.NORM_MINMAX)

    # Convert depth to normal map using Sobel gradients
    sobelx = cv2.Sobel(depth_normalized, cv2.CV_32F, 1, 0, ksize=5)
    sobely = cv2.Sobel(depth_normalized, cv2.CV_32F, 0, 1, ksize=5)

    normal_map = np.zeros((*depth.shape, 3), dtype=np.float32)
    normal_map[..., 0] = sobelx
    normal_map[..., 1] = sobely
    normal_map[..., 2] = 1.0

    # Normalize to 0–255
    normal_map = cv2.normalize(normal_map, None, 0, 255, cv2.NORM_MINMAX)
    normal_map = normal_map.astype(np.uint8)

    # Roughness: invert grayscale image
    albedo_bgr = cv2.imread(input_image_path)
    gray = cv2.cvtColor(albedo_bgr, cv2.COLOR_BGR2GRAY)
    roughness = cv2.bitwise_not(gray)

    # AO: blurred grayscale
    ao = cv2.GaussianBlur(gray, (15, 15), 0)

    # Save all outputs
    base_name = os.path.splitext(os.path.basename(input_image_path))[0].replace("_Albedo", "")
    
    #cv2.imwrite(f"output/{base_name}_Normal.jpg", normal_map)
    # --- SOBEL NORMAL ---
    sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=5)
    sobel_normal = np.zeros_like(albedo_bgr, dtype=np.float32)
    sobel_normal[..., 0] = sobelx
    sobel_normal[..., 1] = sobely
    sobel_normal[..., 2] = 255
    sobel_normal = cv2.normalize(sobel_normal, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # --- BLEND NORMALS ---
    blended_normal = blend_normals(normal_map, sobel_normal, alpha=0.6)
    cv2.imwrite(f"output/{base_name}_Normal.jpg", blended_normal)


    cv2.imwrite(f"output/{base_name}_Roughness.jpg", roughness)
    cv2.imwrite(f"output/{base_name}_AO.jpg", ao)

    print("✅ [AI] Normal, Roughness, AO saved (AI-enhanced).")


def blend_normals(normal_ai, normal_sobel, alpha=0.5):
    """
    Blend two normal maps: AI-based and edge-based.
    `alpha` controls weight of AI normal vs Sobel.
    """
    # Ensure both inputs are same size and uint8
    normal_ai = cv2.resize(normal_ai, (normal_sobel.shape[1], normal_sobel.shape[0]))
    blended = cv2.addWeighted(normal_ai, alpha, normal_sobel, 1 - alpha, 0)
    return blended


# ✅ This block must be outside the function
if __name__ == "__main__":
    make_image_seamless("input/texture2.jpg")
    generate_pbr_from_albedo("output/texture2_Albedo.jpg")

