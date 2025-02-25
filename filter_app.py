import cv2
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import filters  # Import custom filters

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

        # Contrast filter variables
        self.alpha = tk.DoubleVar(value=1.0)
        self.beta = tk.DoubleVar(value=0)

        # Posterization filter variables
        self.posterization_levels = tk.IntVar(value=1)

        # Blur filter variables
        self.blur_strength = tk.IntVar(value=1)

        # Alien filter variables
        self.alien_color = tk.StringVar(value="none")

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
            values=["Original", "Contrast", "Posterization", "Blur", "Alien"],
            state="readonly", width=20
        )
        self.filter_menu.pack(pady=5)

        # Sliders for contrast filter
        self.contrast_alpha_slider = tk.Scale(self.main_frame,
            label="Alpha (Contrast)", orient=tk.HORIZONTAL,
            from_=0.0, to=3.0,resolution=0.1,
            variable=self.alpha)

        self.contrast_beta_slider = tk.Scale(self.main_frame,
            label="Beta (Brightness)", orient=tk.HORIZONTAL,
            from_=-255, to=255, resolution=1,
            variable=self.beta)

        # Posterization filter variables and sliders
        self.posterization_slider = tk.Scale(self.main_frame,
            label="Posterization Levels", orient=tk.HORIZONTAL,
            from_=1, to=64, resolution=1,
            variable=self.posterization_levels)

        # Slider for blur effect
        self.blur_slider = tk.Scale(self.main_frame,
            label="Blur Strength", orient=tk.HORIZONTAL,
            from_=1, to=255, resolution=2,  # Always odd values
            variable=self.blur_strength)

        # Alien filter color selection
        self.alien_color = ttk.Combobox(
            self.main_frame, textvariable=self.alien_color,
            values=["none", "red", "green", "blue"], state="readonly", width=10
        )

        # Capture and save button
        self.btn_capture = tk.Button(self.main_frame, text="Capture & Save", command=self.capture_and_save)
        self.btn_capture.pack(pady=5)

        # Detect filter change and update UI
        self.filter_menu.bind("<<ComboboxSelected>>", self.update_parameters_ui)

        # Close camera when exiting
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start camera
        self.show_camera_feed()

    def show_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            selected_filter = self.active_filter.get()

            if selected_filter == "Contrast":
                alpha = self.alpha.get()
                beta = self.beta.get()
                frame = filters.contrast(frame, alpha, beta)

            elif selected_filter == "Posterization":
                levels = self.posterization_levels.get()
                frame = filters.posterize(frame, levels)
            
            elif selected_filter == "Blur":
                kernel_size = self.blur_strength.get()
                frame = filters.blur(frame, kernel_size)

            elif selected_filter == "Alien":
                chosen_color = self.alien_color.get()
                frame = filters.alien(frame, chosen_color)

            self.current_frame = frame
            self.display_image(self.current_frame)

        self.root.after(30, self.show_camera_feed)  

    def update_parameters_ui(self, event=None):
        selected_filter = self.active_filter.get()

        # Hide all sliders first
        self.contrast_alpha_slider.pack_forget()
        self.contrast_beta_slider.pack_forget()
        self.posterization_slider.pack_forget()
        self.blur_slider.pack_forget()
        self.alien_color.pack_forget()

        # Show contrast sliders if contrast filter is selected
        if selected_filter == "Contrast":
            self.contrast_alpha_slider.pack(pady=5)
            self.contrast_beta_slider.pack(pady=5)

        # Show posterization sliders if posterization filter is selected
        elif selected_filter == "Posterization":
            self.posterization_slider.pack(pady=5)

        elif selected_filter == "Blur":
            self.blur_slider.pack(pady=5)

        if selected_filter == "Alien":
            self.alien_color.pack(pady=5)  # Show only when Alien is selected

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
