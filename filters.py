import cv2
import numpy as np


# Adjust contrast and brightness of an image.
# - alpha: >1 increases contrast, <1 reduces it
# - beta: >0 brightens, <0 darkens
def contrast(image: np.ndarray, alpha: float = 1.0, beta: int = 0) -> np.ndarray:
    # Copy image with changed type to avoid overflow
    new_image = image.astype(np.float32)
    # Apply the contrast and brightness correction
    new_image = alpha * new_image + beta
    # Limit pixel values to the [0, 255] interval
    new_image = np.clip(new_image, 0, 255)
    # Convert back to uint8, used by openCV
    new_image = new_image.astype(np.uint8)
    
    return new_image
