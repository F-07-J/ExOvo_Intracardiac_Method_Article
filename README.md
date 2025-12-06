# Microscopy-Cell-Detection-and-Quantification
A Python-based fluorescence microscopy analysis pipeline for automated detection and quantification of green and blue cells. Includes background removal, contrast enhancement, noise suppression, and cell counting using classical image processing and optional Cellpose integration.

1. bg_removal_blue_mode.py
2. bg_removal_green_mode.py

The above two scripts are used for the preprocessing of fluorescence microscopy images.
Our dataset contains two different types of images based on their background color:
Images with a blue fluorescence background 
Images with a green fluorescence background
Because the color distribution and background noise are different in these two datasets, we use two separate preprocessing pipelines, each tuned for its respective background color.

1. bg_removal_blue_mode.py Script:

This script is designed for images where the background contains a blue haze and the blue cells have weak signals with green interference dots. It performs the following operations these are also similar in the script for the green background:

Processing Steps
a. Gaussian background subtraction
b. LAB-based contrast enhancement
c. HSV conversion
d. Binary masking
e. Morphology cleaning
f. Connected-component filtering
g. Replace background with black
h. Save final processed image

Key adjustable parameters
The blue-background preprocessing script allows several parameters to be tuned depending on the image intensity and noise level. The blue detection is primarily controlled by the hue range (75–160) and the relaxed saturation (≥45) and brightness thresholds (≥80), which help capture weak blue cells. Additionally, a blue-dominance rule (B > G + 25 and B > R + 25) is used to ensure that even faint blue cells are detected while suppressing non-cell regions. Two levels of area filtering are applied: an initial minimum area of 80 pixels to remove background noise and a final minimum area of 120 pixels to keep only real cell regions. Since blue cells often contain small green interference dots, the script also includes color-correction parameters where the green channel is reduced to 40% and the red channel to 85% for pixels classified as “only blue.” These parameters can be relaxed or tightened depending on how strong or weak the blue fluorescence appears in the dataset.

2. bg_removal_green_mode.py Script:
Key adjustable parameters
The green-background preprocessing script includes flexible thresholds designed to preserve even faint green fluorescence. The primary HSV mask uses a wide hue range (25–105) with very relaxed saturation (>5) and value (>15) limits, allowing the script to recover low-intensity green cells that would otherwise disappear. The secondary green-intensity mask relies on green dominance (G > R + 5 and G > B + 5) to ensure that genuine green cells are included while suppressing background artifacts. Since some green cells can be extremely small, the minimum connected-component size is set to 3 pixels, making the filter very permissive. The script also applies CLAHE enhancement (clipLimit = 3.0) to boost visibility of small and dim cell regions. These parameters can be adjusted depending on how strong, weak, or noisy the green fluorescence is in each batch of images.
