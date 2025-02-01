import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        
        self.image = None
        self.cropped_image = None
        self.modified_image = None
        self.history = []
        self.redo_stack = []
        
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()
        
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()
        
        self.save_button = tk.Button(root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack()
        
        self.crop_button = tk.Button(root, text="Crop Image", command=self.start_cropping, state=tk.DISABLED)
        self.crop_button.pack()
        
        self.resize_slider = tk.Scale(root, from_=10, to=200, orient=tk.HORIZONTAL, label="Resize %", command=self.resize_image)
        self.resize_slider.pack()
        
        self.process_button = tk.Button(root, text="Apply Filters", command=self.apply_filters, state=tk.DISABLED)
        self.process_button.pack()
        
        self.undo_button = tk.Button(root, text="Undo", command=self.undo, state=tk.DISABLED)
        self.undo_button.pack()
        
        self.redo_button = tk.Button(root, text="Redo", command=self.redo, state=tk.DISABLED)
        self.redo_button.pack()
        
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
        
        self.selection_rect = None
        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.cropping = False
        
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not file_path:
            return
        
        self.image = cv2.imread(file_path)
        self.display_image(self.image)
        self.save_button["state"] = tk.NORMAL
        self.crop_button["state"] = tk.NORMAL
        self.process_button["state"] = tk.NORMAL
        self.history.append(self.image.copy())
        self.undo_button["state"] = tk.NORMAL
    
    def display_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.canvas.create_image(300, 200, image=image)
        self.canvas.image = image
    
    def start_cropping(self):
        self.cropping = True
    
    def start_selection(self, event):
        if not self.cropping:
            return
        self.start_x, self.start_y = event.x, event.y
    
    def update_selection(self, event):
        if not self.cropping:
            return
        self.end_x, self.end_y = event.x, event.y
        self.canvas.delete(self.selection_rect)
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red")
    
    def end_selection(self, event):
        if not self.cropping:
            return
        self.end_x, self.end_y = event.x, event.y
        self.crop_image()
        self.cropping = False
    
    def crop_image(self):
        if self.image is None:
            return
        x1, y1, x2, y2 = self.start_x, self.start_y, self.end_x, self.end_y
        self.cropped_image = self.image[y1:y2, x1:x2]
        self.modified_image = self.cropped_image.copy()
        self.display_image(self.cropped_image)
        self.history.append(self.cropped_image.copy())
    
    def resize_image(self, value):
        if self.modified_image is None:
            return
        scale = int(value) / 100
        width = int(self.cropped_image.shape[1] * scale)
        height = int(self.cropped_image.shape[0] * scale)
        resized = cv2.resize(self.cropped_image, (width, height))
        self.modified_image = resized
        self.display_image(resized)
        self.history.append(resized.copy())
    
    def apply_filters(self):
        if self.modified_image is None:
            return
        self.modified_image = cv2.cvtColor(self.modified_image, cv2.COLOR_BGR2GRAY)
        self.display_image(self.modified_image)
        self.history.append(self.modified_image.copy())
    
    def save_image(self):
        if self.modified_image is None:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if not file_path:
            return
        cv2.imwrite(file_path, self.modified_image)
        messagebox.showinfo("Success", "Image saved successfully!")
    
    def undo(self):
        if len(self.history) > 1:
            self.redo_stack.append(self.history.pop())
            self.modified_image = self.history[-1]
            self.display_image(self.modified_image)
            self.redo_button["state"] = tk.NORMAL
        if len(self.history) <= 1:
            self.undo_button["state"] = tk.DISABLED
    
    def redo(self):
        if self.redo_stack:
            self.history.append(self.redo_stack.pop())
            self.modified_image = self.history[-1]
            self.display_image(self.modified_image)
            self.undo_button["state"] = tk.NORMAL
        if not self.redo_stack:
            self.redo_button["state"] = tk.DISABLED

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()