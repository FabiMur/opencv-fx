import cv2
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyFilter App")

        # ------------------- Attributes -------------------

        self.cap = cv2.VideoCapture(0)
        self.current_frame = None

        # Set window size and disable resizing
        self.root.geometry("600x700")  
        self.root.resizable(False, False)
        self.root.configure(bg="white")  

        # Active filter
        self.active_filter = tk.StringVar(value="Original")

        # ------------------- Widgets -------------------

        # Main container to center content
        self.main_frame = tk.Frame(root, bg="white")  
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")  

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self.main_frame, width=500, height=500, bg="black")
        self.canvas.pack(pady=10)  

        # Filter selection menu
        self.filter_menu = ttk.Combobox(
            self.main_frame, textvariable=self.active_filter,
            values=["Original"],
            state="readonly", width=20, font=("Arial", 12, "bold")
        )
        self.filter_menu.pack(pady=5)

        # Capture and save button
        self.btn_capture = tk.Button(
            self.main_frame, text="Capture & Save", command=self.capture_and_save)
        self.btn_capture.pack(pady=5)

        # Close camera when exiting
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start camera
        self.show_camera_feed()

    def show_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.display_image(self.current_frame)

        self.root.after(30, self.show_camera_feed)  

    def display_image(self, image):
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image.resize((500, 500)))

        self.canvas.delete("all")  
        self.canvas.create_image(250, 250, anchor=tk.CENTER, image=image)  
        self.canvas.image = image  

    def capture_and_save(self):
        if self.current_frame is None:
            messagebox.showerror("Error", "No frame captured")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Success", "Image saved successfully")

    def on_close(self):
        self.cap.release()
        self.root.destroy()

# ------------------- Main -------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = FilterApp(root)
    root.mainloop()
