import os
from PIL import Image


def resize_image(image, percentage):
    img = Image.open(image)
    # orig size --> h=886, w=452
    width, height = img.size
    print(f"height: {height} -> width: {width}")
    target_size = (height*percentage,width*percentage)
    img.thumbnail(target_size)
    return img


def iterate_over_images(directory, percentage):
    for fname in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, fname)):
            resized_image = resize_image(directory + "/" + fname, percentage)
            resized_image.save(directory + "/thumbnail_" + fname)


if __name__ == "__main__":

    percentage = .5
    directory = "./static/images/"
    iterate_over_images(directory, percentage)
