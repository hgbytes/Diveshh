import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import PyPDF2
import os
from threading import Thread

class PDFToAudioConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Audio Converter")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        # Variables
        self.pdf_path = tk.StringVar()
        self.status = tk.StringVar()
        self.status.set("Ready to convert")

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="PDF to Audio Converter",
            font=("Helvetica", 16, "bold"),
            bg='#f0f0f0'
        )
        title_label.pack(pady=10)

        # File selection frame
        file_frame = tk.Frame(main_frame, bg='#f0f0f0')
        file_frame.pack(fill='x', pady=20)

        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            bg='#f0f0f0',
            wraplength=400
        )
        self.file_label.pack()

        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)

        # Buttons
        select_button = tk.Button(
            button_frame,
            text="Select PDF File",
            command=self.select_file,
            width=20,
            bg='#4CAF50',
            fg='white',
            font=("Helvetica", 10)
        )
        select_button.pack(side=tk.LEFT, padx=5)

        convert_button = tk.Button(
            button_frame,
            text="Convert to Audio",
            command=self.start_conversion,
            width=20,
            bg='#2196F3',
            fg='white',
            font=("Helvetica", 10)
        )
        convert_button.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(
            main_frame,
            textvariable=self.status,
            bg='#f0f0f0',
            font=("Helvetica", 10)
        )
        self.status_label.pack(pady=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.pdf_path.set(file_path)
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")

    def convert_pdf_to_audio(self):
        try:
            # Open PDF file
            pdf_file = open(self.pdf_path.get(), 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)  # Updated to PdfReader
            text_list = []

            # Extract text from each page
            for i in range(len(pdf_reader.pages)):  # Updated page count access
                try:
                    page = pdf_reader.pages[i]  # Updated page access
                    text_list.append(page.extract_text())  # Updated method name
                    self.status.set(f"Processing page {i+1} of {len(pdf_reader.pages)}")
                    self.root.update()
                except Exception as e:
                    print(f"Error on page {i}: {str(e)}")
                    continue

            # Convert text to single string
            text_string = " ".join(text_list)

            # Convert to audio
            self.status.set("Converting text to audio...")
            self.root.update()
            audio = gTTS(text=text_string, lang='en', slow=False)

            # Save audio file
            output_path = os.path.splitext(self.pdf_path.get())[0] + '.mp3'
            audio.save(output_path)

            pdf_file.close()
            self.status.set("Conversion completed successfully!")
            messagebox.showinfo("Success", f"Audio file saved as:\n{output_path}")

        except Exception as e:
            self.status.set("Error during conversion")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def start_conversion(self):
        if not self.pdf_path.get():
            messagebox.showwarning("Warning", "Please select a PDF file first!")
            return

        # Start conversion in a separate thread to prevent GUI freezing
        Thread(target=self.convert_pdf_to_audio, daemon=True).start()

def main():
    root = tk.Tk()
    app = PDFToAudioConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
