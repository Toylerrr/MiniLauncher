import customtkinter as ctk
import subprocess
import os
import sys
from PIL import Image

# Determine the directory where the EXE is located
if getattr(sys, 'frozen', False):  # Running as a PyInstaller EXE
    script_dir = os.path.dirname(sys.executable)  # Directory of the EXE
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Normal script location

# Function to log messages in the GUI console and also print to terminal for debugging
def log_message(message):
    # Debug: Print to console for visibility in terminal
    print(message)
    
    # Update the console in the GUI
    console_text.configure(state="normal")  # Enable editing
    console_text.insert("end", message + "\n")  # Append message
    console_text.configure(state="disabled")  # Disable editing
    console_text.yview("end")  # Scroll to the bottom of the text widget

# Load config file
config_path = os.path.join(script_dir, "config.txt")
APP_PATHS = {}

if os.path.exists(config_path):
    with open(config_path, "r") as f:
        for line in f:
            parts = line.strip().split("=", 1)
            if len(parts) == 2:
                APP_PATHS[parts[0].strip()] = parts[1].strip()
else:
    log_message(f"Warning: Config file not found at {config_path}. Place it next to the EXE.")

if not APP_PATHS:
    log_message("Warning: No applications loaded from config.")

def open_app(app_path):
    # First check if the app path exists
    if not os.path.exists(app_path):
        log_message(f"Error: {app_path} does not exist.")
        return
    
    # Try to open the application
    try:
        subprocess.Popen(app_path, shell=True)
        log_message(f"Opened: {app_path}")
    except Exception as e:
        log_message(f"Error: Failed to open {app_path}. Exception: {e}")

# Create the main window
root = ctk.CTk()
root.title("App Launcher")
root.geometry("600x400")  # Increased width to fit both image and buttons

# Create TabView widget for two tabs (App Launcher and Console)
tabview = ctk.CTkTabview(root)
tabview.pack(fill="both", expand=True, padx=10, pady=0)  # Removed top padding to reduce extra space

# Tab 1: Buttons and Image
tabview.add("App Launcher")

# Create a frame for the left and right parts (image and buttons)
top_frame = ctk.CTkFrame(tabview.tab("App Launcher"))
top_frame.pack(side=ctk.TOP, fill="x", padx=5, pady=0)  # Reduced padding to remove extra space

# Left side image
image_frame = ctk.CTkFrame(top_frame)
image_frame.pack(side=ctk.LEFT, padx=10)

img_path = os.path.join(script_dir, "220X313.png")
if os.path.exists(img_path):
    try:
        img = ctk.CTkImage(light_image=Image.open(img_path), size=(220, 313))
        image_label = ctk.CTkLabel(image_frame, image=img, text="")
        image_label.pack(side=ctk.TOP, padx=10, pady=10)
    except Exception as e:
        log_message(f"Error loading image: {e}")
else:
    log_message(f"Warning: Image file not found at {img_path}. Place it next to the EXE.")

# Right side buttons
button_frame = ctk.CTkFrame(top_frame)
button_frame.pack(side=ctk.LEFT, padx=10, fill="both", expand=True)

for app_name, app_path in APP_PATHS.items():
    btn = ctk.CTkButton(button_frame, text=app_name, command=lambda p=app_path: open_app(p))
    btn.pack(pady=5, fill=ctk.X)

# Tab 2: Console (Log messages)
tabview.add("Console")

# Console output area (log messages)
console_frame = ctk.CTkFrame(tabview.tab("Console"))
console_frame.pack(fill="both", expand=True, padx=5, pady=5)  # Reduced padding to remove extra space

console_text = ctk.CTkTextbox(console_frame, wrap="word", state="disabled")
console_text.pack(fill="both", expand=True, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
