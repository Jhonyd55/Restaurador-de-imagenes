import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time

class InpaintingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inpainting GUI")
        self.root.geometry("1200x800")

        self.damaged_image = None
        self.restored_image = None
        self.mask = None
        self.inpainting_running = False

        self.setup_ui()

    def setup_ui(self):
        self.method_var = tk.StringVar(value="t")
        self.threshold_var = tk.IntVar(value=200)

        self.frame_controls = ttk.Frame(self.root)
        self.frame_controls.pack(side=tk.TOP, fill=tk.X)

        self.btn_load_damaged = ttk.Button(self.frame_controls, text="Cargar Imagen Dañada", command=self.load_damaged_image)
        self.btn_load_damaged.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_load_mask = ttk.Button(self.frame_controls, text="Cargar Máscara (Opcional)", command=self.load_mask)
        self.btn_load_mask.pack(side=tk.LEFT, padx=5, pady=5)

        self.lbl_method = ttk.Label(self.frame_controls, text="Método de Inpainting:")
        self.lbl_method.pack(side=tk.LEFT, padx=5, pady=5)

        self.radio_telea = ttk.Radiobutton(self.frame_controls, text="Telea", variable=self.method_var, value="t")
        self.radio_telea.pack(side=tk.LEFT, padx=5, pady=5)

        self.radio_ns = ttk.Radiobutton(self.frame_controls, text="Navier-Stokes", variable=self.method_var, value="n")
        self.radio_ns.pack(side=tk.LEFT, padx=5, pady=5)

        self.lbl_threshold = ttk.Label(self.frame_controls, text="Umbral:")
        self.lbl_threshold.pack(side=tk.LEFT, padx=5, pady=5)

        self.lbl_threshold_value = ttk.Label(self.frame_controls, text=f"{self.threshold_var.get()}")
        self.lbl_threshold_value.pack(side=tk.LEFT, padx=5, pady=5)

        self.scale_threshold = ttk.Scale(self.frame_controls, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.threshold_var, command=self.on_threshold_change)
        self.scale_threshold.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_inpaint = ttk.Button(self.frame_controls, text="Restaurar Imagen", command=self.start_inpaint_thread)
        self.btn_inpaint.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_save = ttk.Button(self.frame_controls, text="Guardar Imagen Restaurada", command=self.save_restored_image)
        self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        self.progress = ttk.Progressbar(self.frame_controls, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress.pack(side=tk.LEFT, padx=5, pady=5)

        self.frame_images = ttk.Frame(self.root)
        self.frame_images.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.canvas_damaged = tk.Canvas(self.frame_images, bg="gray")
        self.canvas_damaged.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_restored = tk.Canvas(self.frame_images, bg="gray")
        self.canvas_restored.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def load_damaged_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.damaged_image = cv2.imread(file_path)
            self.show_image(self.damaged_image, self.canvas_damaged)
            self.update_mask()

    def load_mask(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.mask = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    def resize_image(self, image, canvas_width, canvas_height):
        height, width = image.shape[:2]
        scale = min(canvas_width / width, canvas_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image

    def show_image(self, image, canvas):
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        resized_image = self.resize_image(image, canvas_width, canvas_height)
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        canvas.image = image_tk
        canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

    def on_threshold_change(self, value):
        if not self.inpainting_running:
            self.lbl_threshold_value.config(text=f"{int(float(value))}")
            self.update_mask()

    def update_mask(self):
        if self.damaged_image is None:
            return

        threshold = self.threshold_var.get()
        gray_damaged = cv2.cvtColor(self.damaged_image, cv2.COLOR_BGR2GRAY)
        _, self.mask = cv2.threshold(gray_damaged, threshold, 255, cv2.THRESH_BINARY_INV)
        self.show_image(self.damaged_image, self.canvas_damaged)  # Ensure damaged image stays visible

    def inpaint_image(self):
        self.progress['value'] = 0
        self.root.update_idletasks()

        if self.damaged_image is None:
            messagebox.showerror("Error", "Por favor, cargue una imagen dañada.")
            return

        if self.mask is None:
            self.update_mask()

        inpainting_method = cv2.INPAINT_NS if self.method_var.get() == 'n' else cv2.INPAINT_TELEA

        self.restored_image = np.copy(self.damaged_image)
        step_size = self.mask.shape[0] // 10

        self.inpainting_running = True
        for i in range(10):
            time.sleep(0.5)  # Simulate processing time
            self.restored_image = cv2.inpaint(self.restored_image, self.mask, 3, inpainting_method)
            self.progress['value'] += 10
            self.root.update_idletasks()
            self.show_image(self.restored_image, self.canvas_restored)
        self.inpainting_running = False

        self.show_image(self.restored_image, self.canvas_restored)

    def start_inpaint_thread(self):
        if not self.inpainting_running:
            thread = threading.Thread(target=self.inpaint_image)
            thread.start()

    def save_restored_image(self):
        if self.restored_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.restored_image)
                messagebox.showinfo("Guardado", f"Imagen guardada en: {file_path}")
        else:
            messagebox.showerror("Error", "No hay imagen restaurada para guardar.")

def main():
    root = tk.Tk()
    app = InpaintingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
