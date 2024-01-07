import cv2
import imutils
import pytesseract
import os
import shutil

counter = 0


def i():
    global counter
    counter += 1
    return counter


def analyze(filename, save=False):
    global counter
    counter = 0
    if save:
        fold = "temppp"
        if not os.path.exists(fold):
            os.makedirs(fold)
        else:
            shutil.rmtree(fold)  # Removes all the subdirectories!
            os.makedirs(fold)

    image = cv2.imread(filename)

    # Convert the image to grayscale
    original_image = image  # imutils.resize(image, width=500)
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    if save:
        cv2.imwrite(f"{fold}/{i()}_grayscale.png", gray_image)

    contours, new = cv2.findContours(
        gray_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )
    contoure = cv2.drawContours(original_image.copy(), contours, -1, (0, 255, 0), 3)
    if save:
        cv2.imwrite(f"{fold}/{i()}_contours.png", contoure)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

    contoure2 = cv2.drawContours(original_image.copy(), contours, -1, (0, 255, 0), 3)
    if save:
        cv2.imwrite(f"{fold}/{i()}_contours.png", contoure2)

    count = 0
    idx = 7

    OFFSET = 2

    finded = False

    cropped_License_Plate = f"./{fold}/{i()}_plaque.png"
    for c in contours:
        # approximate the license plate contour
        contour_perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * contour_perimeter, True)

        # Look for contours with 4 corners
        if len(approx) == 4:
            screenCnt = approx

            # find the coordinates of the license plate contour
            x, y, w, h = cv2.boundingRect(c)
            new_img = original_image[
                y + OFFSET : (y + h) - OFFSET, (x) + OFFSET : (x + w) - OFFSET
            ]

            # stores the new image
            cv2.imwrite(cropped_License_Plate, new_img)
            idx += 1
            finded = True
            break
    print("Rectangle finded: ", finded)
    if not finded:
        return "Not finded"

    from skimage import io
    from skimage import transform as tf

    # Load the image as a matrix

    # converts the license plate characters to string
    import numpy as np

    p = []

    from skimage import img_as_ubyte

    def remove_non_ascii(text):
        return "".join(
            char for char in text if ord(char) < 128 and char != "\n" and char != "\x0c"
        )

    from collections import Counter

    for she in np.arange(-0.5, 0.5, 0.1):
        image = io.imread(cropped_License_Plate)
        # Create Afine transform
        afine_tf = tf.AffineTransform(shear=she)

        # Apply transform to image data
        modified = tf.warp(image, inverse_map=afine_tf)

        # Display the result
        # io.imshow(modified)
        m = f"{fold}/modified.jpg"
        io.imsave(m, img_as_ubyte(modified))
        for psm in range(6, 13 + 1):
            config = "--oem 3 --psm %d" % psm
            txt = pytesseract.image_to_string(m, config=config, lang="eng")
            name = remove_non_ascii(txt)
            p.append(name)
            if save:
                io.imsave(
                    f"{fold}/{she:.2f}-----------{name}.png", img_as_ubyte(modified)
                )

    # print(p)

    combined_text = " ".join(p)

    # Split the combined text into words
    words = combined_text.split()

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Find the most common pattern
    most_common_pattern = word_counts.most_common(1)[0][0]
    return most_common_pattern


if __name__ == "__main__":
    print(analyze("../imageToSave2.png", save=True))
