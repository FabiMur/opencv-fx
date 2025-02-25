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

# Applays blur to the image ussing a kernel full of 1s
def blur(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    if kernel_size < 1:
        return image

    # Ensure kerlen size is odd
    kernel_size = max(3, kernel_size | 1)
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size ** 2)

    return cv2.filter2D(image, -1, kernel)

# Applyes the alien effect to an image, replacing colors tones identified as skin for the selected color.
def alien(image: np.ndarray, color: str = "none") -> np.ndarray:
    if color == "none":
        return image

    # Use HSV instead of RGB because skin colors are easier to detect
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Specify the color space that will be identified as skin
    lower_skin = np.array([0, 40,50], dtype=np.uint8)
    upper_skin = np.array([25, 255, 255], dtype=np.uint8)

    # Create mask for skin detection
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Define replacement color (in RGB)
    color_map = {
        "red":   (255, 0, 0),
        "green": (0, 255, 0),
        "blue":  (0, 0, 255)
    }

    if color not in color_map:
        return image

    alien_color = color_map.get(color)

    # Create a blank image with the selected color
    color_layer = np.full_like(image, alien_color, dtype=np.uint8)

    # Replace only the skin regions
    image[mask > 0] = color_layer[mask > 0]

    return image