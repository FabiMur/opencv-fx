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
    lower_skin = np.array([5, 50, 150], dtype=np.uint8)
    upper_skin = np.array([15, 160, 220], dtype=np.uint8)

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

# Applies the barrel and/or pincushion distortion effect to the image
def distort(image: np.ndarray, k_barrel: float = 0.0, k_pincushion: float = 0.0) -> np.ndarray:
    # Skip effect calculation if both parameters are 0
    if k_pincushion == 0 and k_barrel == 0:
        return image

    # Read the dimensions of the image
    height, width = image.shape[:2]

    # Create 2 matrices with the x and y coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Normalize the coordinates to the range [-1, 1]
    x_n = (x - width / 2) / (width / 2)
    y_n = (y - height / 2) / (height / 2)

    # Compute the distance to the center of each pixel position
    r = np.sqrt(x_n**2 + y_n**2)

    # Initialize distorted coordinates
    x_n_distorted = x_n
    y_n_distorted = y_n

    # Apply barrel distortion effect
    # If k is POSITIVE, pixels move AWAY from the center
    # If k is NEGATIVE, pixels move TOWARD the center
    if k_barrel != 0:
        x_n_distorted = x_n * (1 + k_barrel * r**2)
        y_n_distorted = y_n * (1 + k_barrel * r**2)

    # Apply pincushion distortion
    # If k is POSITIVE, pixels move TOWARD the center
    # If k is NEGATIVE, pixels move AWAY from the center
    if k_pincushion != 0:
        x_n_distorted *= (1 + k_pincushion * r**4)
        y_n_distorted *= (1 + k_pincushion * r**4)

    # Convert normalized coordinates back to pixel coordinates
    x_distorted = (x_n_distorted * (width / 2) + width / 2).astype(np.float32)
    y_distorted = (y_n_distorted * (height / 2) + height / 2).astype(np.float32)

    # Reassign pixels to their new coordinates
    distorted_image = cv2.remap(image, x_distorted, y_distorted, interpolation=cv2.INTER_LINEAR)

    return distorted_image