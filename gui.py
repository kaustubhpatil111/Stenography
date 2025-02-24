import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from steganography import encode_message, decode_message

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Modern theme

        # Configure colors and fonts
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.text_color = "#333333"
        self.root.configure(bg=self.bg_color)

        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Image Path Section
        ttk.Label(self.main_frame, text="Image Path:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.image_path = tk.StringVar()
        self.image_entry = ttk.Entry(self.main_frame, textvariable=self.image_path, width=50, font=("Arial", 10))
        self.image_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_image, style="TButton").grid(row=0, column=2, padx=10, pady=10)

        # Message Section
        ttk.Label(self.main_frame, text="Message:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.message = tk.StringVar()
        self.message_entry = ttk.Entry(self.main_frame, textvariable=self.message, width=50, font=("Arial", 10))
        self.message_entry.grid(row=1, column=1, padx=10, pady=10)

        # Output Path Section
        ttk.Label(self.main_frame, text="Output Path:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(self.main_frame, textvariable=self.output_path, width=50, font=("Arial", 10))
        self.output_entry.grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_output, style="TButton").grid(row=2, column=2, padx=10, pady=10)

        # Encode and Decode Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=1, pady=20)
        ttk.Button(self.button_frame, text="Encode", command=self.encode, style="Accent.TButton").grid(row=0, column=0, padx=10)
        ttk.Button(self.button_frame, text="Decode", command=self.decode, style="Accent.TButton").grid(row=0, column=1, padx=10)

        # Status Bar
        self.status_bar = ttk.Label(self.main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10))
        self.status_bar.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Tooltips
        self.create_tooltips()

        # Configure styles
        self.style.configure("TButton", background=self.button_color, foreground=self.text_color, font=("Arial", 10))
        self.style.configure("Accent.TButton", background="#0078D7", foreground="white", font=("Arial", 10, "bold"))
        self.style.map("Accent.TButton", background=[("active", "#005BB5")])

    def browse_image(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if filename:
            self.image_path.set(filename)
            self.status_bar.config(text=f"Selected Image: {filename}")

    def browse_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if filename:
            self.output_path.set(filename)
            self.status_bar.config(text=f"Output File: {filename}")

    def encode(self):
        if not self.image_path.get() or not self.message.get() or not self.output_path.get():
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            self.status_bar.config(text="Encoding...")
            self.root.update_idletasks()  # Update UI
            encode_message(self.image_path.get(), self.message.get(), self.output_path.get())
            self.status_bar.config(text="Message encoded successfully!")
            messagebox.showinfo("Success", "Message encoded successfully!")
        except Exception as e:
            self.status_bar.config(text="Error during encoding.")
            messagebox.showerror("Error", str(e))

    def decode(self):
        if not self.image_path.get():
            messagebox.showwarning("Input Error", "Please select an image to decode.")
            return

        try:
            self.status_bar.config(text="Decoding...")
            self.root.update_idletasks()  # Update UI
            decoded_message = decode_message(self.image_path.get())
            self.status_bar.config(text="Message decoded successfully!")
            messagebox.showinfo("Decoded Message", f"Decoded message: {decoded_message}")
        except Exception as e:
            self.status_bar.config(text="Error during decoding.")
            messagebox.showerror("Error", str(e))

    def create_tooltips(self):
        # Add tooltips for better UX
        tooltips = {
            self.image_entry: "Select the image file in which you want to hide the message.",
            self.message_entry: "Enter the secret message you want to encode.",
            self.output_entry: "Choose the location and name for the output image file.",
        }

        for widget, text in tooltips.items():
            self.create_tooltip(widget, text)

    def create_tooltip(self, widget, text):
        tooltip = ttk.Label(self.root, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 9))
        def enter(event):
            tooltip.place(x=widget.winfo_rootx(), y=widget.winfo_rooty() - 30)
        def leave(event):
            tooltip.place_forget()
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()