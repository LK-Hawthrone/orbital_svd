## Orbital Image SVD Compressor (Tkinter Version)
# Author: L.K Hawthrone
# Purpose: CCSDS-compliant image processing tool

import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from PIL import Image
import numpy as np
import os
import logic_svd as engine
import results_viewer as viewer

# --- Global root reference for window management ---
root = None

# --- Utility functions ---

def load_xml_config(config_path="config_mission.xml"):
    """
    Reads mission parameters from the tactical XML file.
    """
    fallback = {"k_target": 0.08, "quality": 65, "blur_radius": 1.5}
    
    if not os.path.exists(config_path):
        return fallback

    try:
        tree = ET.parse(config_path)
        xml_root = tree.getroot()
        
        return {
            "k_target": float(xml_root.find('k_target').text),
            "quality": int(xml_root.find('quality').text),
            "blur_radius": float(xml_root.find('blur_radius').text)
        }
    except Exception as e:
        print(f"[!] XML Error: {e}. Using tactical fallback.")
        return fallback


def process_image(input_path):
    """
    Orchestrates the SVD mission and redirects to the results viewer.
    "Nanomachines, son! They harden in response to digital noise."
    """
    config = load_xml_config()
    
    try:
        # Load and convert to Grayscale (L)
        img = Image.open(input_path).convert('L')
        A = np.array(img)
        
        # 1. Low-Pass Filter (The 'Alchemy' step via logic_svd)
        A_blurred = engine.apply_low_pass_filter(A, config['blur_radius'])
        
        # 2. SVD Reconstruction (The Core Engine via logic_svd)
        A_k, k_value = engine.compute_svd_compression(A_blurred, config['k_target'])
        
        # 3. Create PIL Image object from processed array
        final_img = Image.fromarray(np.clip(A_k, 0, 255).astype(np.uint8))
        
        # 4. Hand over to Results Viewer for preview and final saving
        # We pass 'root' to keep the window hierarchy stable
        viewer.show_mission_results(root, final_img, k_value, config['quality'])
        
    except Exception as e:
        messagebox.showerror("Critical Error", f"The system crashed: {e}")


# --- GUI functions ---

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select Image for SVD Compression",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        process_image(file_path)


def main():
    """
    Tkinter Main Window. Custom Dark Theme for Xubuntu Users.
    """
    global root
    root = tk.Tk()
    root.title("SVD Orbital Processor")
    root.geometry("400x250")
    
    # Dark Theme Colors (Xubuntu/Codium Palette)
    bg_color = "#1e1e1e"  
    fg_color = "#d4d4d4"  
    accent_color = "#0e639c" 

    root.configure(bg=bg_color)

    label = tk.Label(root, text="SVD Image Compression Tool", 
                    font=("Helvetica", 14, "bold"), 
                    bg=bg_color, fg=fg_color)
    label.pack(pady=20)

    # Tactical Deployment Button
    btn = tk.Button(root, text="SELECT IMAGE & DEPLOY", 
                    command=select_file, 
                    bg=accent_color, fg="white", 
                    activebackground="#1177bb", activeforeground="white",
                    font=("Helvetica", 10, "bold"),
                    padx=20, pady=10, relief="flat")
    btn.pack(pady=10)

    footer = tk.Label(root, text="Standard protocol for INPE/DCTA research", 
                     font=("Helvetica", 8, "italic"),
                     bg=bg_color, fg="#888888")
    footer.pack(side="bottom", pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()