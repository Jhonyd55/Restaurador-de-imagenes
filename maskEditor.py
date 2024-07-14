import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

class MaskEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Máscara")
        
        self.image_path = ""
        self.mask = None
        self.pen_thickness = 5  # Grosor inicial del lápiz

        self.setup_ui()

    def setup_ui(self):
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        

        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set,yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.draw)

        # Marco para contener los controles deslizantes
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.btn_load_image = ttk.Button(self.controls_frame, text="Cargar Imagen", command=self.load_image)
        self.btn_load_image.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_create_mask = ttk.Button(self.controls_frame, text="Crear Máscara", command=self.create_mask)
        self.btn_create_mask.pack(side=tk.LEFT, padx=5, pady=5)

        # Etiqueta para el control deslizante del grosor del lápiz
        self.label_pen_thickness = tk.Label(self.controls_frame, text="Grosor del Lápiz:")
        self.label_pen_thickness.pack(side=tk.TOP, padx=5, pady=5)

        # Añadir control deslizante para el grosor del lápiz
        self.scale_pen_thickness = ttk.Scale(self.controls_frame, from_=1, to=20, length=200, orient=tk.HORIZONTAL)
        self.scale_pen_thickness.set(self.pen_thickness)
        self.scale_pen_thickness.pack(side=tk.TOP, padx=5, pady=5)
        self.scale_pen_thickness.bind("<ButtonRelease-1>", self.set_pen_thickness)

        # Botón para borrar o retroceder
        self.btn_erase = ttk.Button(self.controls_frame, text="Borrar", command=self.erase)
        self.btn_erase.pack(side=tk.RIGHT, padx=5, pady=5)

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = cv2.imread(self.image_path)            
            self.show_image(self.image)

    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        self.image_tk = ImageTk.PhotoImage(image_pil)
        self.canvas.config(scrollregion=(0, 0, image_pil.width, image_pil.height))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def draw(self, event):
        if event.widget == self.canvas:
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            r = self.pen_thickness // 2  # Radio del lápiz
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black", outline="")

    def create_mask(self):
        self.mask = np.zeros_like(self.image[:, :, 0])
        for item in self.canvas.find_all():
            if self.canvas.type(item) == 'oval':
                coords = self.canvas.coords(item)
                if len(coords) == 4:
                    x1, y1, x2, y2 = coords
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    self.mask[y1:y2, x1:x2] = 255
        cv2.imwrite("mask.png", self.mask)
        self.root.quit()

    def set_pen_thickness(self, event):
        self.pen_thickness = int(self.scale_pen_thickness.get())

    def erase(self):
        # Eliminar el último objeto dibujado
        items = self.canvas.find_all()
        if items:
            self.canvas.delete(items[-1])

def main():
    root = tk.Tk()
    app = MaskEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
