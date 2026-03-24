import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import sys

# ---------------- FUNCTIONS ----------------

def run_script(script):
    try:
        status_label.config(text=f"Running {script}...")
        subprocess.run([sys.executable, script])
        status_label.config(text=f"{script} Done ✅")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Error ❌")


def capture():
    name = name_entry.get().strip()

    if name == "":
        messagebox.showwarning("Warning", "Enter Name First!")
        return

    threading.Thread(target=run_script, args=("capture_images.py",)).start()


def train():
    threading.Thread(target=run_script, args=("train_model.py",)).start()


def start_attendance():
    threading.Thread(target=run_script, args=("recognize.py",)).start()


# ---------------- UI ----------------

root = tk.Tk()
root.title("Face Attendance System")
root.geometry("350x450")
root.config(bg="#0f172a")

# Title
title = tk.Label(root, text="Face Attendance System",
                 font=("Segoe UI", 16, "bold"),
                 fg="#38bdf8", bg="#0f172a")
title.pack(pady=20)

# Status
status_label = tk.Label(root, text="Stopped",
                        font=("Segoe UI", 10),
                        fg="white", bg="#0f172a")
status_label.pack(pady=5)

# Name Entry
name_entry = tk.Entry(root, font=("Segoe UI", 12))
name_entry.pack(pady=10)

# Button style function
def create_button(text, cmd, color):
    return tk.Button(
        root,
        text=text,
        command=cmd,
        font=("Segoe UI", 12, "bold"),
        bg=color,
        fg="white",
        width=20,
        height=2,
        bd=0
    )

# Buttons
create_button("📸 Capture Images", capture, "#22c55e").pack(pady=10)
create_button("🧠 Train Model", train, "#3b82f6").pack(pady=10)
create_button("🎯 Start Attendance", start_attendance, "#f59e0b").pack(pady=10)
create_button("❌ Exit", root.quit, "#ef4444").pack(pady=20)

root.mainloop()