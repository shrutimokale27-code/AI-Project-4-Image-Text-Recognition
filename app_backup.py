import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import subprocess


# Project folder
project = Path(__file__).resolve().parent

# Tesseract path
tesseract = project / "tesseract.exe"

# Selected image
selected_image = None


# ---------------- OCR FUNCTION ----------------

def extract_text():
    global selected_image

    if selected_image is None:
        messagebox.showwarning("Warning", "Please select an image first.")
        return

    if not tesseract.exists():
        messagebox.showerror("Error", "Tesseract not found.")
        return

    result = subprocess.run(
        [
            str(tesseract),
            str(selected_image),
            "stdout"
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        messagebox.showerror("OCR Error", result.stderr)
        return

    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, result.stdout)

    # Save automatically
    output_file = project / "output.txt"
    output_file.write_text(result.stdout, encoding="utf-8")

    messagebox.showinfo(
        "Success",
        "Text extracted successfully!\n\nSaved in output.txt"
    )


# ---------------- SELECT IMAGE ----------------

def select_image():
    global selected_image

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        selected_image = Path(file_path)

        image_label.config(
            text=f"Selected Image:\n{selected_image.name}"
        )

        text_box.delete("1.0", tk.END)


# ---------------- SAVE TEXT ----------------

def save_text():
    text = text_box.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Warning",
            "No text available to save."
        )
        return

    file_path = filedialog.asksaveasfilename(
        title="Save Text",
        defaultextension=".txt",
        filetypes=[
            ("Text File", "*.txt")
        ]
    )

    if file_path:
        Path(file_path).write_text(
            text,
            encoding="utf-8"
        )

        messagebox.showinfo(
            "Success",
            "Text saved successfully!"
        )


# ---------------- CLEAR ----------------

def clear_text():
    global selected_image

    selected_image = None
    image_label.config(text="No image selected")
    text_box.delete("1.0", tk.END)


# ---------------- GUI ----------------

window = tk.Tk()

window.title("AI Image Text Recognition")
window.geometry("800x600")

title = tk.Label(
    window,
    text="IMAGE TEXT RECOGNITION",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)


image_label = tk.Label(
    window,
    text="No image selected",
    font=("Arial", 12)
)

image_label.pack(pady=10)


select_button = tk.Button(
    window,
    text="Select Image",
    command=select_image,
    width=20
)

select_button.pack(pady=5)


extract_button = tk.Button(
    window,
    text="Extract Text",
    command=extract_text,
    width=20
)

extract_button.pack(pady=5)


text_label = tk.Label(
    window,
    text="Recognized Text",
    font=("Arial", 14, "bold")
)

text_label.pack(pady=10)


text_box = tk.Text(
    window,
    height=15,
    width=80,
    font=("Arial", 12)
)

text_box.pack(padx=20, pady=5)


save_button = tk.Button(
    window,
    text="Save Text",
    command=save_text,
    width=20
)

save_button.pack(side=tk.LEFT, padx=120, pady=15)


clear_button = tk.Button(
    window,
    text="Clear",
    command=clear_text,
    width=20
)

clear_button.pack(side=tk.RIGHT, padx=120, pady=15)


window.mainloop()