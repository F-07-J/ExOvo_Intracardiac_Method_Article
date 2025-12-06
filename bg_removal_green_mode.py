import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Input and Output Paths
img_path = r"/content/Snap-8380z.jpeg"
output_folder = r"/content/Group_Control_day_05_dataset/COntrol_day_5_bk_iso"

os.makedirs(output_folder, exist_ok=True)
bgr = cv2.imread(img_path)
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

# Step 1: Background suppression 
blur = cv2.GaussianBlur(rgb, (41, 41), 0)
subtracted = cv2.subtract(rgb, blur)

# Step 2: CLAHE 
lab = cv2.cvtColor(subtracted, cv2.COLOR_RGB2LAB)
l, a, b = cv2.split(lab)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
l_clahe = clahe.apply(l)
lab_clahe = cv2.merge([l_clahe, a, b])
enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2RGB)

# Step 3: Convert to HSV 
hsv = cv2.cvtColor(enhanced, cv2.COLOR_RGB2HSV)
H, S, V = cv2.split(hsv)

# Step 4: RELAXED GREEN MASK (cells reappear) 
mask_hsv = (
    (H > 25) & (H < 105) &
    (S > 5) &        # saturation
    (V > 15)          # brightness
).astype(np.uint8) * 255

# Step 5: Green channel detector 
R, G, B = cv2.split(enhanced)

mask_green = (
    (G > R + 5) &
    (G > B + 5) &
    (G > 14)          
).astype(np.uint8) * 255

# KEY FIX
mask_combined = cv2.bitwise_or(mask_hsv, mask_green)

# Step 6: Light cleaning 
kernel = np.ones((3, 3), np.uint8)
mask_clean = cv2.morphologyEx(mask_combined, cv2.MORPH_OPEN, kernel)

# Step 7: Connected components
num_labels, labels = cv2.connectedComponents(mask_clean)

min_size = 3   # cell size
final_mask = np.zeros_like(mask_clean)

for label in range(1, num_labels):
    component_size = np.sum(labels == label)
    if component_size >= min_size:
        final_mask[labels == label] = 255

# Step 8: Apply mask 
result = cv2.bitwise_and(rgb, rgb, mask=final_mask)
black_background = np.zeros_like(rgb)
final = np.where(result > 0, result, black_background)

# Step 9: Show results 
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(rgb)
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(final)
plt.title("Green Cells Detected")
plt.axis('off')
plt.show()

# Step 10: Save 
filename = os.path.basename(img_path)
output_path = os.path.join(output_folder, filename)
cv2.imwrite(output_path, cv2.cvtColor(final, cv2.COLOR_RGB2BGR))

print("Output saved:", output_path)
