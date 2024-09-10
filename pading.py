import cv2
import os

import numpy as np


def resize_and_pad(image_path, output_path, target_size, frame_size=10):
    # Read the original image
    img = cv2.imread(image_path)

    # Get dimensions of the original image
    height, width = img.shape[:2]

    # Calculate the target size including the frame
    target_size_with_frame = target_size + 2 * frame_size

    # Calculate the scaling factor for resizing
    if height > width:
        scale = target_size / height
        new_height = target_size
        new_width = int(width * scale)
    else:
        scale = target_size / width
        new_width = target_size
        new_height = int(height * scale)

    # Resize the image to fit inside the frame
    img_resized = cv2.resize(img, (new_width, new_height))

    # Create a new white canvas with the target size including the frame
    canvas = 255 * np.ones((target_size_with_frame, target_size_with_frame, 3), dtype=np.uint8)

    # Calculate the position to paste the resized image at the center of the canvas
    y_offset = (target_size_with_frame - new_height) // 2
    x_offset = (target_size_with_frame - new_width) // 2

    # Paste the resized image onto the canvas
    canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = img_resized

    # Save the output image
    cv2.imwrite(output_path, canvas)

