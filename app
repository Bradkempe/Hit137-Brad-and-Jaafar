import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np

class ImageEditor:
    def __init__(self, root):
        self.root = root
        root.title("Image Editor")

        # Global variables (now instance variables)
        self.original_image = None
        self.cropped_image = None
        self.thumbnail = None
        self.crop_coords = None
        self.resize_scale = 100
        self.brightness_scale = 0
        self.pan_offset = [0, 0]
        self.start_pan_coords = None
        self.history = []
        self.redo_stack = []
        self.current_tool = None
        self.MAX_HISTORY_SIZE = 20

        # GUI elements and layout (using self.)
        self.create_gui()

    def create_gui(self):  #Organizing GUI creation
        # ... (All your Tkinter widget creation and layout code goes here)
        # Use self.widget_name for all widgets (e.g., self.canvas_original = tk.Canvas(...))

        #Bind events using self.
        self.canvas_original.bind("<ButtonPress-1>", self.start_crop)
        self.canvas_original.bind("<B1-Motion>", self.show_crop)
        self.canvas_original.bind("<ButtonRelease-1>", self.finish_crop)
        self.canvas_cropped.bind("<ButtonPress-1>", self.start_pan)
        self.canvas_cropped.bind("<B1-Motion>", self.pan_image)
        self.canvas_cropped.bind("<ButtonRelease-1>", self.stop_pan)
        #... other binding events

    def add_to_history(self):
        # ... (same as before)

    def load_image(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
            if filepath:
                self.original_image = cv2.imread(filepath)
                if self.original_image is None: #Check if the image was loaded correctly
                    raise ValueError("Could not load the image. File might be corrupted or invalid.")
                self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                self.cropped_image = None
                self.crop_coords = None
                self.resize_scale = 100
                self.brightness_scale = 0
                self.pan_offset = [0, 0]
                self.slider.set(100)
                self.brightness_slider.set(0)
                self.canvas_original.delete("all")
                self.canvas_cropped.delete("all")
                self.cropped_size_label.config(text="Cropped Image Size: N/A")
                self.update_canvas_size()
                self.history = []  # Clear history
                self.redo_stack = []  # Clear redo stack
                self.add_to_history()
                self.display_images()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except ValueError as e:
            messagebox.showerror("Error", str(e)) #Displaying the error message from the exception
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")

    def update_canvas_size(self):
        # ... (same as before, but using self.original_image, etc.)

    def adjust_brightness(self, image, value):
        # ... (same as before)

    def display_images(self):
        # ... (same as before, but using self.original_image, etc.)

    def resize_cropped_image(self, scale):
        # ... (same as before)

    def adjust_brightness_slider(self, value):
        # ... (same as before)

    def start_crop(self, event):
        # ... (same as before)

    def show_crop(self, event):
        # ... (same as before)

    def finish_crop(self, event):
        if self.current_tool == "crop" and self.crop_coords is not None:
            x1, y1 = self.crop_coords[0], self.crop_coords[1]
            x2, y2 = event.x, event.y
            x1, y1, x2, y2 = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)

            if self.original_image is not None:
                h, w, _ = self.original_image.shape
                scale = min(500 / w, 500 / h)
                x1, y1 = int(x1 / scale), int(y1 / scale)
                x2, y2 = int(x2 / scale), int(y2 / scale)

                # Cropping Edge Case Handling (Option 1: Do Nothing - Current Behavior)
                if x1 < x2 and y1 < y2:  # Only crop if valid coordinates
                    if self.cropped_image is not None:
                        self.add_to_history()
                        self.redo_stack.clear()
                    self.cropped_image = self.original_image[y1:y2, x1:x2]
                    self.display_images()

                # Cropping Edge Case Handling (Option 2: 1x1 Crop)
                # if self.crop_coords == [event.x, event.y]: # Click without drag
                #     if self.cropped_image is not None:
                #         self.add_to_history()
                #         self.redo_stack.clear()
                #     self.cropped_image = self.original_image[y1:y1+1, x1:x1+1] # 1x1 crop
                #     self.display_images()
                # elif x1 < x2 and y1 < y2:
                #     #... (rest of the cropping code)

                # Cropping Edge Case Handling (Option 3: Message to User)
                # if self.crop_coords == [event.x, event.y]:
                #     messagebox.showinfo("Crop Info", "Please drag to select a cropping area.")
                # elif x1 < x2 and y1 < y2:
                #     # ... (rest of the cropping code)

            self.crop_coords = None

    def undo_action(self):
        # ... (same as before)

    def redo_action(self):
        # ... (same as before)

    def start_pan(self, event):
        # ... (same as before)

    def pan_image(self, event):
        # ... (same as before)

    def stop_pan(self, event):
        # ... (same as before)

    def save_image(self):
        try:
            if self.cropped_image is not None:
                h, w = int(self.cropped_image.shape[0] * self.resize_scale / 100), int(self.cropped_image.shape[1] * self.resize_scale / 100)
                resized = cv2.resize(self.cropped_image, (w, h), interpolation=cv2.INTER_LINEAR)
                adjusted = self.adjust_brightness(resized, self.brightness_scale)
                filepath = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
                if filepath:
                    cv2.imwrite(filepath, cv2.cvtColor(adjusted, cv2.COLOR_RGB2BGR))
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {e}")

    def center_cropped_image(self):
        # ... (same as before)

    def bind_shortcuts(self):
        # ... (same as before)


root = tk.Tk()
app = ImageEditor(root)
app.bind_shortcuts() #Call the bind_shortcuts method
root.mainloop()
