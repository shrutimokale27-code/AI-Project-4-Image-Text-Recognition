import subprocess
from pathlib import Path

# Tesseract executable
tesseract = Path(".\tesseract.exe")

# Input image
image = Path("images\test.png")

# Output file
output = Path("output.txt")

# Check Tesseract
if not tesseract.exists():
    print("ERROR: tesseract.exe not found.")
    exit()

# Check image
if not image.exists():
    print("ERROR: test.png not found.")
    exit()

# Run Tesseract
result = subprocess.run(
    [
        str(tesseract),
        str(image),
        "stdout"
    ],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace"
)

# Check for errors
if result.returncode != 0:
    print("OCR Error:")
    print(result.stderr)
    exit()

# Get recognized text
text = result.stdout.strip()

# Display result
print()
print("===================================")
print("       IMAGE TEXT RECOGNITION")
print("===================================")
print()
print("Recognized Text:")
print("-------------------------")
print(text)
print("-------------------------")

# Save result
output.write_text(text, encoding="utf-8")

print()
print("Text saved successfully in output.txt")