import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import subprocess
from PIL import Image, ImageTk


# ==============================
# PROJECT PATHS
# ==============================

project = Path(__file__).resolve().parent

tesseract = project / "tesseract.exe"

selected_image = None
preview_image = None


# ==============================
# SELECT IMAGE
# ==============================

def select_image():
    global selected_image
    global preview_image

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    selected_image = Path(file_path)

    try:
        # Open image
        img = Image.open(selected_image)

        # Resize image for preview
        img.thumbnail((400, 250))

        preview_image = ImageTk.PhotoImage(img)

        image_preview.config(
            image=preview_image,
            text=""
        )

        image_name.config(
            text=f"Selected: {selected_image.name}"
        )

        text_box.delete("1.0", tk.END)

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Unable to open image.\n\n{e}"
        )


# ==============================
# OCR FUNCTION
# ==============================

def extract_text():

    if selected_image is None:
        messagebox.showwarning(
            "Warning",
            "Please select an image first."
        )
        return

    if not tesseract.exists():
        messagebox.showerror(
            "Error",
            "tesseract.exe not found."
        )
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
        messagebox.showerror(
            "OCR Error",
            result.stderr
        )
        return

    text = result.stdout.strip()

    text_box.delete("1.0", tk.END)

    text_box.insert(
        tk.END,
        text
    )

    # Automatically save
    output_file = project / "output.txt"

    output_file.write_text(
        text,
        encoding="utf-8"
    )

    messagebox.showinfo(
        "Success",
        "Text extracted successfully!\n\n"
        "Result saved in output.txt"
    )


# ==============================
# SAVE TEXT
# ==============================

def save_text():

    text = text_box.get(
        "1.0",
        tk.END
    ).strip()

    if not text:
        messagebox.showwarning(
            "Warning",
            "No text available to save."
        )
        return

    file_path = filedialog.asksaveasfilename(
        title="Save Recognized Text",
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


# ==============================
# CLEAR
# ==============================

def clear_all():

    global selected_image
    global preview_image

    selected_image = None
    preview_image = None

    image_preview.config(
        image="",
        text="No Image Selected"
    )

    image_name.config(
        text=""
    )

    text_box.delete(
        "1.0",
        tk.END
    )


# ==============================
# MAIN WINDOW
# ==============================

window = tk.Tk()

window.title(
    "AI Image Text Recognition"
)

window.geometry(
    "850x700"
)

window.resizable(
    False,
    False
)


# ==============================
# TITLE
# ==============================

title = tk.Label(
    window,
    text="IMAGE TEXT RECOGNITION",
    font=("Arial", 24, "bold")
)

title.pack(
    pady=15
)


subtitle = tk.Label(
    window,
    text="Extract text from images using Tesseract OCR",
    font=("Arial", 11)
)

subtitle.pack(
    pady=5
)


# ==============================
# IMAGE PREVIEW FRAME
# ==============================

preview_frame = tk.Frame(
    window,
    bd=2,
    relief="groove",
    width=450,
    height=280
)

preview_frame.pack(
    pady=15
)

preview_frame.pack_propagate(False)


image_preview = tk.Label(
    preview_frame,
    text="No Image Selected",
    font=("Arial", 14)
)

image_preview.pack(
    expand=True
)


image_name = tk.Label(
    window,
    text="",
    font=("Arial", 10)
)

image_name.pack()


# ==============================
# BUTTONS
# ==============================

button_frame = tk.Frame(
    window
)

button_frame.pack(
    pady=15
)


select_button = tk.Button(
    button_frame,
    text="Select Image",
    command=select_image,
    width=18,
    font=("Arial", 11)
)

select_button.grid(
    row=0,
    column=0,
    padx=8
)


extract_button = tk.Button(
    button_frame,
    text="Extract Text",
    command=extract_text,
    width=18,
    font=("Arial", 11)
)

extract_button.grid(
    row=0,
    column=1,
    padx=8
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_all,
    width=18,
    font=("Arial", 11)
)

clear_button.grid(
    row=0,
    column=2,
    padx=8
)


# ==============================
# RECOGNIZED TEXT
# ==============================

text_label = tk.Label(
    window,
    text="Recognized Text",
    font=("Arial", 14, "bold")
)

text_label.pack(
    pady=5
)


text_box = tk.Text(
    window,
    height=10,
    width=90,
    font=("Arial", 11),
    wrap=tk.WORD
)

text_box.pack(
    padx=20,
    pady=5
)


# ==============================
# SAVE BUTTON
# ==============================

save_button = tk.Button(
    window,
    text="Save Text",
    command=save_text,
    width=20,
    font=("Arial", 11)
)

save_button.pack(
    pady=12
)


# ==============================
# START APPLICATION
# ==============================

window.mainloop()