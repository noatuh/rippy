import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import string

VIDEO_EXTENSIONS = ['.vob', '.mpg', '.mpeg', '.avi', '.mp4', '.mov']

def get_available_drives():
    return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

class CDRipperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wedding Video CD Ripper")
        self.geometry("500x250")
        self.resizable(False, False)

        # Drive selector
        tk.Label(self, text="Select CD/DVD Drive:").pack(pady=5)
        self.drive_var = tk.StringVar()
        self.drive_menu = ttk.Combobox(self, textvariable=self.drive_var, state="readonly", width=40)
        self.drive_menu.pack()
        self.refresh_drives()

        # Destination folder selector
        tk.Label(self, text="Select Destination Folder:").pack(pady=10)
        self.dest_var = tk.StringVar()
        self.dest_entry = tk.Entry(self, textvariable=self.dest_var, width=50)
        self.dest_entry.pack(pady=2)
        tk.Button(self, text="Browse...", command=self.browse_dest).pack()

        # Start button
        self.start_button = tk.Button(self, text="Start Ripping", command=self.start_rip)
        self.start_button.pack(pady=10)

        # Progress
        self.progress = ttk.Progressbar(self, length=400, mode='determinate')
        self.progress.pack(pady=5)

        # Status label
        self.status = tk.Label(self, text="")
        self.status.pack()

    def refresh_drives(self):
        drives = get_available_drives()
        self.drive_menu['values'] = drives
        if drives:
            self.drive_menu.current(0)

    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_var.set(folder)

    def start_rip(self):
        source = self.drive_var.get()
        dest = self.dest_var.get()

        if not source or not os.path.exists(source):
            messagebox.showerror("Error", "Please select a valid CD/DVD drive.")
            return
        if not dest:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        self.progress['value'] = 0
        self.status.config(text="Scanning for video files...")
        self.update()

        video_files = []
        for root, _, files in os.walk(source):
            for file in files:
                if any(file.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
                    video_files.append(os.path.join(root, file))

        if not video_files:
            self.status.config(text="No video files found on disc.")
            return

        self.progress['maximum'] = len(video_files)

        for i, filepath in enumerate(video_files, 1):
            try:
                filename = os.path.basename(filepath)
                dest_path = os.path.join(dest, filename)
                shutil.copy2(filepath, dest_path)
                self.status.config(text=f"Copied: {filename}")
            except Exception as e:
                self.status.config(text=f"Error copying {filename}: {e}")
            self.progress['value'] = i
            self.update()

        self.status.config(text=f"Done! {len(video_files)} file(s) copied.")
        messagebox.showinfo("Finished", "Ripping complete!")

if __name__ == "__main__":
    app = CDRipperApp()
    app.mainloop()
