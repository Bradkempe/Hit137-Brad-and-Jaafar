import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        self.original_image = None
        self.cropped_image = None
        self.thumbnail = None  # For displaying the original image
        self.cropped_thumbnail = None #For displaying the cropped image
        self.crop_coords = None

        self._setup_gui()

    def _setup_gui(self):
        container = ttk.Frame(self.root, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Original Image Canvas
        self.original_canvas = tk.Canvas(container, width=500, height=500, bg="gray")
        self.original_canvas.grid(row=0, column=0, padx=5, pady=5)
        self.original_canvas.bind("<ButtonPress-1>", self.start_crop)
        self.original_canvas.bind("<B1-Motion>", self.update_crop)
        self.original_canvas.bind("<ButtonRelease-1>", self.perform_crop)

        # Cropped Image Canvas
        self.cropped_canvas = tk.Canvas(container, width=500, height=500, bg="gray")
        self.cropped_canvas.grid(row=0, column=1, padx=5, pady=5)

        # Control Frame
        control_frame = ttk.Frame(container)
        control_frame.grid(row=1, column=0, columnspan=2, pady=(5,0))  # Place below canvases

        # Load Button
        self.load_button = ttk.Button(control_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        # Save Button
        self.save_button = ttk.Button(control_frame, text="Save Image", command=self.save_image)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        # Resize Slider
        self.resize_slider = ttk.Scale(control_frame, from_=10, to=200, orient=tk.HORIZONTAL, command=self.resize_image)
        self.resize_slider.set(100)  # Default value
        self.resize_slider.grid(row=0, column=2, padx=5, pady=5)


    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
            if file_path:
                self.original_image = cv2.imread(file_path)
                self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)  # Convert to RGB
                self.cropped_image = None  # Reset cropped image
                self.crop_coords = None
                self.display_image(self.original_canvas, self.original_image, self.thumbnail) #Display original image
                self.cropped_canvas.delete("all") #Clear the cropped canvas
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")

    def display_image(self, canvas, image, image_tk): #Generalized function to display images in canvas
        if image is not None:
            h, w, _ = image.shape
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            scale = min(canvas_width / w, canvas_height / h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            image_pil = Image.fromarray(resized_image)
            image_tk = ImageTk.PhotoImage(image_pil)
            canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            canvas.image = image_tk  # Keep a reference to prevent garbage collection

    def save_image(self):
        try:
            if self.cropped_image is not None:
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
                if file_path:
                    cv2.imwrite(file_path, cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2BGR)) #Save cropped image
            else:
                messagebox.showwarning("Warning", "No cropped image to save.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {e}")

    def resize_image(self, value):
        try:
            scale = int(value) / 100
            if self.cropped_image is not None:
                h, w, _ = self.cropped_image.shape
                new_h = int(h * scale)
                new_w = int(w * scale)
                resized_image = cv2.resize(self.cropped_image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
                self.display_image(self.cropped_canvas, resized_image, self.cropped_thumbnail) #Display resized image
        except Exception as e:
             messagebox.showerror("Error", f"Could not resize image: {e}")

    def start_crop(self, event):
        self.crop_coords = [event.x, event.y]
        self.original_canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", tags="crop_rect")

    def update_crop(self, event):
        if self.crop_coords:
            self.original_canvas.delete("crop_rect")  # Remove previous rectangle
            self.original_canvas.create_rectangle(self.crop_coords[0], self.crop_coords[1], event.x, event.y, outline="red", tags="crop_rect")

    def perform_crop(self, event):
        if self.crop_coords:
            x1, y1 = self.crop_coords
            x2, y2 = event.x, event.y

            x1 = min(x1, x2)
            y1 = min(y1, y2)
            x2 = max(x1, x2)
            y2 = max(y1, y2)

            try:
                if self.original_image is not None:
                    h, w, _ = self.original_image.shape
                    canvas_width = self.original_canvas.winfo_width()
                    canvas_height = self.original_canvas.winfo_height()
                    scale = min(canvas_width / w, canvas_height / h)
                    x1 = int(x1 / scale)
                    y1 = int(y1 / scale)
                    x2 = int(x2 / scale)
                    y2 = int(y2 / scale)
                    self.cropped_image = self.original_image[y1:y2, x1:x2]
                    self.display_image(self.cropped_canvas, self.cropped_image, self.cropped_thumbnail) #Display cropped image
            except Exception as e:
                messagebox.showerror("Error", f"Could not perform crop: {e}")

            self.crop_coords = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
