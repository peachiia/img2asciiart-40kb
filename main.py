# img2asciiart-40kb
# Convert an image to ASCII art with a size limit of 40kB
#
# @peachiia, 20231027

import PIL.Image
import math
import os
 
TARGET_SIZE_LIMIT_BYTE = 40000  # 40 KB
 


def get_imgSize_from_targetWidth(img_origin, target_width):
    width_origin, height_origin = img_origin.size
    aspect_ratio = height_origin/width_origin
    target_width = int(target_width)
    target_height = int(aspect_ratio * target_width * 0.4) # 0.55 is a magic number
    return (target_width, target_height)



def calc_imgSize_from_targetSizeLimit(img_origin):
    target_width = 1000
    target_size = get_imgSize_from_targetWidth(img_origin, target_width)
    print(f"Target Size : {target_size} ({target_size[0] * target_size[1]} bytes)")
    scale = math.sqrt(TARGET_SIZE_LIMIT_BYTE / (target_size[0] * target_size[1]))
    target_width = int(target_width * scale)
    target_size = get_imgSize_from_targetWidth(img_origin, target_width)
    return target_size
    


def get_grayscaleImage_resized(img, width_target, height_target):
    img = img.resize((width_target, height_target))
    img = img.convert('L') # convert to grayscale
    return img
   


def get_asciiImage(img, reverse=False):
    gradient_chars = ["@", "#", "8", "&", "W", "*", "o", ":", ".", " "]
    gradient_step = round(255/len(gradient_chars))

    if reverse:
        gradient_chars.reverse()
    pixels = img.getdata()
    new_pixels = [gradient_chars[int(pixel//gradient_step)] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)

    width_target, height_target = img.size
    ascii_image = [new_pixels[index:index + width_target] for index in range(0, new_pixels_count, width_target)]
    ascii_image = "\n".join(ascii_image)
    return ascii_image



def main():

    # --- Step 1 : Get the image path ---
    image_path = input("Image filename (or path): \n")

    image_directory = os.path.dirname(image_path)
    image_filename, image_fileextension = os.path.splitext(os.path.basename(image_path))

    # --- Step 2: If no directory is specified, use the current directory ---
    if image_directory == "":
        image_directory = os.getcwd()
        image_path = os.path.join(image_directory, image_filename + image_fileextension)

    # --- Step 3 : Open image file ---    
    try:
        img_origin = PIL.Image.open(image_path)
    except:
        print(f"ERROR: Unable to find image {image_path} !");
        return
    
    # --- Step 4 : Get image size to fit 40kB ---
    (target_width, target_height) = calc_imgSize_from_targetSizeLimit(img_origin)
    print(f"Origin Dimension : {img_origin.size}")
    print(f"Target Dimension : ({target_width},{target_height})")
    print(f"Limit Size  : {TARGET_SIZE_LIMIT_BYTE} bytes")
    print(f"Target Size : {target_width * target_height} bytes")

    # --- Step 5 : Resize image ---
    img = get_grayscaleImage_resized(img_origin, target_width, target_height)

    # --- Step 6 : Convert image to ASCII ---
    ascii_image = get_asciiImage(img, reverse=True)

    # --- Step 7 : Save ASCII image ---
    output_filename = image_filename + "_ascii.txt"
    output_path = os.path.join(image_directory, output_filename)
    with open(output_path, "w") as f:
        f.write(ascii_image)

    print(f'ASCII image saved as {output_filename} ! :P ')



if __name__ == '__main__':
    main()