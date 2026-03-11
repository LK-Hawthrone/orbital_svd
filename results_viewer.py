import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io
import os

def show_mission_results(parent, image_obj, k_value, quality):
    """
    Shows preview and calculates real size before saving.
    """
    results_win = tk.Toplevel(parent)
    results_win.title("Mission Report: Output Preview")
    results_win.geometry("500x650")
    results_win.configure(bg="#1e1e1e")

    # Calculate REAL size using a buffer (ByteIO)
    img_buffer = io.BytesIO()
    image_obj.save(img_buffer, format="JPEG", quality=quality, optimize=True)
    size_kb = len(img_buffer.getvalue()) / 1024

    # Preview Image
    preview_img = image_obj.copy()
    preview_img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(preview_img)

    lbl_img = tk.Label(results_win, image=img_tk, bg="#1e1e1e")
    lbl_img.image = img_tk 
    lbl_img.pack(pady=10)

    # Technical Data Table (Styled)
    info_text = f"RANK (k): {k_value}\nESTIMATED SIZE: {size_kb:.2f} KB\nSTATUS: MISSION READY"
    lbl_info = tk.Label(results_win, text=info_text, bg="#1e1e1e", fg="#00ff00", # Green for success
                       font=("Courier", 10, "bold"), justify="left")
    lbl_info.pack(pady=10)

    def save_action():
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG Image", "*.jpg")],
            initialfile="svd_compressed.jpg"
        )
        if save_path:
            with open(save_path, "wb") as f:
                f.write(img_buffer.getvalue())
            messagebox.showinfo("Success", "Data extracted to local storage.")
            results_win.destroy()

    btn_save = tk.Button(results_win, text="EXTRACT DATA (SAVE)", command=save_action,
                         bg="#0e639c", fg="white", font=("Helvetica", 10, "bold"),
                         padx=20, pady=10, relief="flat")
    btn_save.pack(pady=20)