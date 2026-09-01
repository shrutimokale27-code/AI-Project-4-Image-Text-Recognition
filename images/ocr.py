import cv2
import pytesseract
from pathlib import Path


# ==========================================
# TESSERACT PATH
# ==========================================

project = Path(__file__).resolve().parent

pytesseract.pytesseract.tesseract_cmd = str(
    project / "tesseract.exe"
)


# ==========================================
# INPUT IMAGE
# ==========================================

image_path = project / "images" / "test.png"

image = cv2.imread(str(image_path))


if image is None:
    print("ERROR: Image not found.")
    exit()


# ==========================================
# PRE-PROCESSING
# ==========================================

# Convert image to grayscale
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)


# Remove noise
blur = cv2.GaussianBlur(
    gray,
    (5, 5),
    0
)


# Adaptive thresholding
thresh = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)


# ==========================================
# OCR CONFIGURATION
# ==========================================

config = "--psm 6"


# ==========================================
# TEXT RECOGNITION
# ==========================================

text = pytesseract.image_to_string(
    thresh,
    config=config
).strip()


# ==========================================
# CONFIDENCE SCORE
# ==========================================

data = pytesseract.image_to_data(
    thresh,
    config=config,
    output_type=pytesseract.Output.DICT
)


confidences = []

for confidence in data["conf"]:
    try:
        value = float(confidence)

        if value >= 0:
            confidences.append(value)

    except ValueError:
        pass


if confidences:
    average_confidence = sum(confidences) / len(confidences)
else:
    average_confidence = 0


# ==========================================
# DISPLAY RESULT
# ==========================================

print()
print("==========================================")
print("       IMAGE TEXT RECOGNITION")
print("==========================================")

print()
print("Input Image:")
print(image_path)

print()
print("Recognized Text:")
print("------------------------------------------")
print(text)
print("------------------------------------------")

print()
print(
    f"Average OCR Confidence: "
    f"{average_confidence:.2f}%"
)


# ==========================================
# VALIDATION
# ==========================================

if average_confidence >= 80:
    print("Validation: PASSED")
    print("Recognition confidence is above 80%.")
else:
    print("Validation: BELOW 80%")
    print("Try a clearer or higher-resolution image.")


# ==========================================
# SAVE OUTPUT
# ==========================================

output_path = project / "output.txt"

with open(
    output_path,
    "w",
    encoding="utf-8"
) as file:

    file.write("IMAGE TEXT RECOGNITION\n")
    file.write("======================\n\n")

    file.write("Recognized Text:\n")
    file.write(text)

    file.write("\n\n")
    file.write(
        f"Average OCR Confidence: "
        f"{average_confidence:.2f}%\n"
    )

    if average_confidence >= 80:
        file.write("Validation: PASSED\n")
    else:
        file.write("Validation: BELOW 80%\n")


print()
print("Output saved successfully:")
print(output_path)