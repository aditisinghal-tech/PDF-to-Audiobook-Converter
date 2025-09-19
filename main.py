import pymupdf
import fitz  # PyMuPDF
import pyttsx3
from tkinter import *
from tkinter import filedialog, messagebox

# function to extract text from pdf
def extract_text_from_pdf(pdf_path):
    text_content = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            txt = page.get_text()
            if txt.strip():  # ignore empty pages
                text_content.append(txt)
        return " ".join(text_content)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read PDF: {e}")
        return ""


# function to convert text to speech and save as mp3
def text_to_speech(text, save_path=None, rate=150, volume=1.0):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", rate)  # speech speed
        engine.setProperty("volume", volume)  # volume (0.0 - 1.0)

        if save_path:
            engine.save_to_file(text, save_path)
            engine.runAndWait()
        else:
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"Speech conversion failed: {e}")


# upload pdf and convert
def upload_and_convert():
    pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not pdf_file:
        return
    text = extract_text_from_pdf(pdf_file)
    if not text:
        messagebox.showwarning("Empty", "No text found in PDF!")
        return

    # get slider values
    rate = speed_slider.get()
    volume = volume_slider.get()

    # ask to play or save
    choice = messagebox.askyesno("Save?", "Do you want to save as MP3?")
    if choice:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")])
        if save_path:
            text_to_speech(text, save_path=save_path, rate=rate, volume=volume)
            messagebox.showinfo("Done", f"Saved at {save_path}")
    else:
        text_to_speech(text, rate=rate, volume=volume)


# GUI part
root = Tk()
root.title("PDF to Audiobook Converter")
root.geometry("420x350")

label = Label(root, text="Convert your PDF to Audio", font=("Arial", 14))
label.pack(pady=15)

# Speed control slider
speed_label = Label(root, text="Speech Speed:")
speed_label.pack()
speed_slider = Scale(root, from_=100, to=250, orient=HORIZONTAL)
speed_slider.set(150)  # default speed
speed_slider.pack(pady=5)

# Volume control slider
volume_label = Label(root, text="Volume:")
volume_label.pack()
volume_slider = Scale(root, from_=0, to=1, resolution=0.1, orient=HORIZONTAL)
volume_slider.set(1.0)  # default full volume
volume_slider.pack(pady=5)

# Buttons
upload_btn = Button(root, text="Upload PDF", command=upload_and_convert,
                    width=20, height=2, bg="lightblue")
upload_btn.pack(pady=10)

exit_btn = Button(root, text="Exit", command=root.quit,
                  width=20, height=2, bg="lightcoral")
exit_btn.pack(pady=10)

root.mainloop()
