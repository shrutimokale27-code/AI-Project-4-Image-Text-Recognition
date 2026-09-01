import cv2
import pytesseract

# Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Dell\OneDrive\Desktop\AI_Project_4\tesseract.exe"

# Read input image
image = cv2.imread("images/test.png")
# Check whether image is loaded
if image is None:
    print("Error: Image not found.")
    exit()

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Remove noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Adaptive thresholding
thresh = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

# OCR configuration
config = "--psm 6"

# Extract text
text = pytesseract.image_to_string(
    thresh,
    config=config
)

# Display recognized text
print("\nRecognized Text:")
print("-------------------------")
print(text)
print("-------------------------")

# Save recognized text
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(text)

print("\nText saved successfully in output.txt")
