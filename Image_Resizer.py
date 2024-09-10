from PIL import Image
import os


def resize_image(image_path, output_path, size):
    image = Image.open(image_path)
    resized_image = image.resize(size)
    resized_image.save(output_path)


def get_image_filenames(folder_path):
    image_filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_filenames.append(filename)
    return image_filenames


# Example usage
folder_path = "Images/Uline/full_size/"

image_filenames = get_image_filenames(folder_path)

for image_name in image_filenames:
    output_path_600 = f"Images/Uline/Uline/{image_name}"
    resize_image(folder_path + image_name, output_path_600, (250, 250))

#
