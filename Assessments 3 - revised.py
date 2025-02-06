# Setup
from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np  # Import numpy for clip functionality

# Initialize the main window
root = Tk()
root.title("Image Editor")

# Global variables
original_image = None
cropped_image = None
thumbnail = None
crop_coords = None
resize_scale = 100
brightness_scale = 0
pan_offset = [0, 0]  # Offset for panning the cropped image
start_pan_coords = None
history = []  # Stores history of changes for undo/redo
redo_stack = []  # Stores redo actions
current_tool = None  # Current active tool

# Define the maximum history size
MAX_HISTORY_SIZE = 20

# Function to add to history with size limit
def add_to_history():
    global cropped_image, history
    if cropped_image is not None:
        if len(history) >= MAX_HISTORY_SIZE: # Limit history size
            history.pop(0) # Remove the oldest state
        history.append(cropped_image.copy()) # Add the current state

# Function to load the image
def load_image():
    global original_image, cropped_image, crop_coords, resize_scale, pan_offset, brightness_scale, history, redo_stack
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if filepath:
        original_image = cv2.imread(filepath)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        cropped_image = original_image.copy()  # Initialize cropped_image to None initially
        crop_coords = None  # Reset crop coordinates
        resize_scale = 100  # Reset resizing scale
        brightness_scale = 0  # Reset brightness scale
        pan_offset = [0, 0]  # Reset panning
        slider.set(100)  # Reset slider position
        brightness_slider.set(0)  # Reset brightness slider
        canvas_original.delete("all")  # Clear previous image
        canvas_cropped.delete("all")  # Clear cropped canvas
        cropped_size_label.config(text="Cropped Image Size: N/A")
        update_canvas_size()  # Update the canvas size to fit the image
        history.clear()  # Clear history
        redo_stack.clear()  # Clear redo stack
        add_to_history()  # Add initial state to history
        display_images() # Display the image after loading

# Function to update the canvas size based on the image dimensions
def update_canvas_size():
    if original_image is not None:
        h, w, _ = original_image.shape
        scale = min(500 / w, 500 / h)
        new_w, new_h = int(w * scale), int(h * scale)
        canvas_original.config(width=new_w, height=new_h)

# Function to adjust brightness
def adjust_brightness(image, value):
    if image is not None:
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)  # Convert to HSV
        h, s, v = cv2.split(hsv)
        v = np.clip(v.astype(np.int32) + value, 0, 255).astype(np.uint8)  # Adjust brightness
        final_hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)  # Convert back to RGB
    return image

# Function to display the original and cropped images
def display_images():
    global thumbnail, cropped_image

    # Display original image
    if original_image is not None:
        image_pil = Image.fromarray(original_image)  # Convert to PIL Image
        img_w, img_h = image_pil.size
        scale = min(500 / img_w, 500 / img_h)
        new_w, new_h = int(img_w * scale), int(img_h * scale)
        thumbnail = image_pil.resize((new_w, new_h))
        tk_image = ImageTk.PhotoImage(thumbnail)
        canvas_original.create_image(new_w // 2, new_h // 2, anchor=CENTER, image=tk_image)
        canvas_original.image = tk_image  # Prevent garbage collection

    # Display cropped image
    if cropped_image is not None:
        h, w = cropped_image.shape[:2]
        resized_h, resized_w = int(h * resize_scale / 100), int(w * resize_scale / 100)
        resized = cv2.resize(cropped_image, (resized_w, resized_h), interpolation=cv2.INTER_LINEAR)
        adjusted = adjust_brightness(resized, brightness_scale)  # Apply brightness adjustment

        # Ensure the cropped image is in RGB format
        if len(adjusted.shape) == 3 and adjusted.shape[2] == 3:  # Check if it's a color image
            image_rgb = adjusted  # Assume it's already RGB
        else:
            image_rgb = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)  # Convert if needed

        image_pil = Image.fromarray(image_rgb)
        tk_image = ImageTk.PhotoImage(image_pil)
        canvas_cropped.delete("all")  # Clear previous content
        canvas_cropped.create_image(
            250 + pan_offset[0], 250 + pan_offset[1], anchor=CENTER, image=tk_image
        )
        canvas_cropped.image = tk_image  # Prevent garbage collection
        cropped_size_label.config(text=f"Cropped Image Size: {resized_w} x {resized_h}")

# Function to resize the cropped image dynamically
def resize_cropped_image(scale):
    global resize_scale, redo_stack , cropped_image  # Make sure cropped_image is global
    if cropped_image is not None: # Only add to history if cropped_image exists
        add_to_history()  # Use the new helper function
        redo_stack.clear()  # Clear redo stack
    resize_scale = int(scale)
    display_images()

# Function to adjust brightness dynamically
def adjust_brightness_slider(value):
    global brightness_scale, redo_stack
    if cropped_image is not None:
        add_to_history()  # Use the new helper function
        redo_stack.clear()  # Clear redo stack
    brightness_scale = int(value)
    display_images()

# Function to start cropping
def start_crop(event):
    global crop_coords
    if current_tool == "crop":
        crop_coords = [event.x, event.y]

# Function to show the crop area dynamically
def show_crop(event):
    if current_tool == "crop":
        canvas_original.delete("crop_rectangle")
        canvas_original.create_rectangle(crop_coords[0], crop_coords[1], event.x, event.y, outline="red", tags="crop_rectangle")

# Function to finalize cropping
def finish_crop(event):
    global cropped_image, redo_stack
    if current_tool == "crop":
        x1, y1 = crop_coords[0], crop_coords[1]
        x2, y2 = event.x, event.y
        x1, y1, x2, y2 = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        # Ensure valid crop coordinates
        if x1 < x2 and y1 < y2:  # Check for valid coordinates 
        if original_image is not None:
            h, w, _ = original_image.shape
            scale = min(500 / w, 500 / h)
            x1, y1 = int(x1 / scale), int(y1 / scale)
            x2, y2 = int(x2 / scale), int(y2 / scale)
            if cropped_image is not None:
                add_to_history()
                redo_stack.clear()
            cropped_image = original_image[y1:y2, x1:x2]
            display_images()

# Function to undo the last change
def undo_action():
    global cropped_image, history, redo_stack
    if history:
        redo_stack.append(cropped_image.copy()) # Store current state in redo stack
        cropped_image = history.pop() # Retrieve previous state from history
        display_images() 
        elif original_image is not None and not history: # handles the initial state
        cropped_image = None
        display_images()

# Function to redo the last undone change
def redo_action():
    global cropped_image, history, redo_stack
    if redo_stack:
      history.append(cropped_image.copy())  # Store current state in history
        cropped_image = redo_stack.pop()  # Retrieve state from redo stack
        display_images()
 
# Function to start panning
def start_pan(event):
    global start_pan_coords
    if current_tool == "pan":
        start_pan_coords = [event.x, event.y]

# Function to handle panning
def pan_image(event):
    global pan_offset, start_pan_coords
    if current_tool == "pan" and start_pan_coords is not None:
        dx = event.x - start_pan_coords[0]
        dy = event.y - start_pan_coords[1]
        pan_offset[0] += dx
        pan_offset[1] += dy
        start_pan_coords = [event.x, event.y]
        display_images()

# Function to stop panning
def stop_pan(event):
    global start_pan_coords
    if current_tool == "pan":
        start_pan_coords = None

# Function to save the image
def save_image():
    if cropped_image is not None:
        h, w = int(cropped_image.shape[0] * resize_scale / 100), int(cropped_image.shape[1] * resize_scale / 100)
        resized = cv2.resize(cropped_image, (w, h), interpolation=cv2.INTER_LINEAR)
        adjusted = adjust_brightness(resized, brightness_scale)  # Apply brightness adjustment
        filepath = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if filepath:
            cv2.imwrite(filepath, cv2.cvtColor(adjusted, cv2.COLOR_RGB2BGR))  # Convert to BGR format before saving

# Function to center the cropped image
def center_cropped_image():
    global pan_offset
    pan_offset = [0, 0]
    display_images()

# Function to bind keyboard shortcuts
def bind_shortcuts():
    root.bind("<Control-o>", lambda event: load_image())  # Ctrl+O to load image
    root.bind("<Control-s>", lambda event: save_image())  # Ctrl+S to save image
    root.bind("<Control-z>", lambda event: undo_action())  # Ctrl+Z to undo
    root.bind("<Control-y>", lambda event: redo_action())  # Ctrl+Y to redo

# GUI Layout
title = Label(root, text="Brad and Jaafar Assessment 3", font=("Arial", 18, "bold"))
title.pack(pady=5)

subtitle = Label(root, text="Group Members:\nS379982 - Brad Kempe\nS367627 Jaafar Mehydeen", font=("Arial", 12))
subtitle.pack(pady=5)

frame = Frame(root)
frame.pack(side=LEFT, padx=10)

# Canvas for images
canvas_frame = Frame(root)
canvas_frame.pack()

canvas_original = Canvas(canvas_frame, width=500, height=500, bg="gray")
canvas_original.grid(row=0, column=0, padx=10)

# Bind mouse events to the original canvas AFTER defining it
canvas_original.bind("<ButtonPress-1>", start_crop)
canvas_original.bind("<B1-Motion>", show_crop)
canvas_original.bind("<ButtonRelease-1>", finish_crop)

canvas_cropped = Canvas(canvas_frame, width=500, height=500, bg="gray")
canvas_cropped.grid(row=0, column=1, padx=10)

# Bind mouse events for panning
canvas_cropped.bind("<ButtonPress-1>", start_pan)
canvas_cropped.bind("<B1-Motion>", pan_image)
canvas_cropped.bind("<ButtonRelease-1>", stop_pan)

# Function to set the current tool
def set_tool(tool_name):
    global current_tool
    current_tool = tool_name

# Tool buttons
tool_frame = Frame(root)
tool_frame.pack()

load_button = Button(tool_frame, text="Load Image", command=load_image)
load_button.grid(row=0, column=0, padx=10)

save_button = Button(tool_frame, text="Save Image", command=save_image)
save_button.grid(row=0, column=4, padx=10)

crop_button = Button(tool_frame, text="Crop Tool", command=lambda: (set_tool("crop")))
crop_button.grid(row=0, column=1, padx=10)

pan_button = Button(tool_frame, text="Pan Tool", command=lambda: (set_tool("pan")))
pan_button.grid(row=0, column=2, padx=10)

center_button = Button(tool_frame, text="Center Image", command=center_cropped_image)
center_button.grid(row=0, column=3, padx=10)

undo_button = Button(tool_frame, text="Undo", command=undo_action)
undo_button.grid(row=1, column=0, padx=10)

redo_button = Button(tool_frame, text="Redo", command=redo_action)
redo_button.grid(row=1, column=1, padx=10)

# Instructions for shortcuts
instructions = Label(root, text="Shortcuts:\nCtrl+O: Open Image\nCtrl+S: Save Image after changes\nCtrl+Z: Undo\nCtrl+Y: Redo", justify=LEFT, anchor="w")
instructions.pack(side=LEFT, padx=10, pady=10)

# Sliders
slider = Scale(root, from_=10, to=200, orient=HORIZONTAL, label="Resize Image (%)", command=resize_cropped_image)
slider.set(100)
slider.pack(pady=5)

brightness_slider = Scale(root, from_=-100, to=100, orient=HORIZONTAL, label="Brightness", command=adjust_brightness_slider)
brightness_slider.set(0)
brightness_slider.pack(pady=5)

cropped_size_label = Label(root, text="Cropped Image Size: N/A", justify=LEFT, anchor="w")
cropped_size_label.pack(pady=5)

# Bind shortcuts
bind_shortcuts()

# Run the main loop
root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
