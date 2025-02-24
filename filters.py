import cv2
import numpy as np


# Adjust contrast and brightness of an image.
# - alpha: >1 increases contrast, <1 reduces it
# - beta: >0 brightens, <0 darkens
def contrast(image: np.ndarray, alpha: float = 1.0, beta: int = 0) -> np.ndarray:
    # Apply the contrast and brightness correction
    # Limit pixel values to the [0, 255] interval
    image[:] = np.clip(alpha * image + beta, 0, 255).astype(np.uint8)
    return image

# Reduces the color resolution of the image
def posterize(image: np.ndarray, levels: int = 1) -> np.ndarray:
    if levels < 2:
        return image

    factor = 255 // (levels - 1)

    image[:] = (image.astype(np.int32) // factor) * factor

    return image