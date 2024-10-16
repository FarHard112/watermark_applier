import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance


class WatermarkApp:
    def __init__(self, master):
        self.master = master
        master.title("Watermark Application")

        self.input_dir = ""
        self.output_dir = ""
        self.watermark_path = ""
        self.current_image = None
        self.watermarked_image = None
        self.preview_size = (400, 400)

        self.opacity = tk.DoubleVar(value=0.5)
        self.size_percent = tk.IntVar(value=25)
        self.position_x = tk.DoubleVar(value=0.5)
        self.position_y = tk.DoubleVar(value=0.5)
        self.tile_var = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):

        ttk.Button(self.master, text="Select Input Directory",
                   command=self.select_input_dir).pack(pady=5)
        self.input_label = ttk.Label(
            self.master, text="No input directory selected")
        self.input_label.pack()

        ttk.Button(self.master, text="Select Output Directory",
                   command=self.select_output_dir).pack(pady=5)
        self.output_label = ttk.Label(
            self.master, text="No output directory selected")
        self.output_label.pack()

        ttk.Button(self.master, text="Select Watermark",
                   command=self.select_watermark).pack(pady=5)
        self.watermark_label = ttk.Label(
            self.master, text="No watermark selected")
        self.watermark_label.pack()

        self.create_slider("Opacity", self.opacity, 0, 1, 0.1)
        self.create_slider("Size (%)", self.size_percent, 1, 100, 1)
        self.create_slider("X Position", self.position_x, 0, 1, 0.01)
        self.create_slider("Y Position", self.position_y, 0, 1, 0.01)

        ttk.Checkbutton(self.master, text="Tile Watermark",
                        variable=self.tile_var, command=self.update_preview).pack(pady=5)

        self.preview_canvas = tk.Canvas(
            self.master, width=self.preview_size[0], height=self.preview_size[1])
        self.preview_canvas.pack(pady=10)

        ttk.Button(self.master, text="Process Images",
                   command=self.process_images).pack(pady=10)

    def create_slider(self, label, variable, from_, to, resolution):
        frame = ttk.Frame(self.master)
        frame.pack(pady=5, fill='x', padx=20)
        ttk.Label(frame, text=label).pack(side='left')
        slider = ttk.Scale(frame, from_=from_, to=to, orient='horizontal',
                           variable=variable, command=self.update_preview)
        slider.pack(side='right', expand=True, fill='x')
        slider.set(variable.get())

    def select_input_dir(self):
        self.input_dir = filedialog.askdirectory()
        self.input_label.config(text=f"Input: {self.input_dir}")
        self.load_first_image()

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        self.output_label.config(text=f"Output: {self.output_dir}")

    def select_watermark(self):
        self.watermark_path = filedialog.askopenfilename(
            filetypes=[("PNG files", "*.png")])
        self.watermark_label.config(
            text=f"Watermark: {os.path.basename(self.watermark_path)}")
        self.update_preview()

    def load_first_image(self):
        if self.input_dir:
            for filename in os.listdir(self.input_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.current_image = Image.open(
                        os.path.join(self.input_dir, filename))
                    self.update_preview()
                    break

    def update_preview(self, *args):
        if self.current_image and self.watermark_path:
            preview_image = self.current_image.copy()
            preview_image.thumbnail(self.preview_size)

            watermark = Image.open(self.watermark_path).convert('RGBA')

            watermark_size = (int(preview_image.width * self.size_percent.get() / 100),
                              int(preview_image.height * self.size_percent.get() / 100))
            watermark = watermark.resize(watermark_size, Image.LANCZOS)

            enhancer = ImageEnhance.Brightness(watermark.split()[3])
            alpha = enhancer.enhance(self.opacity.get())
            watermark.putalpha(alpha)

            if self.tile_var.get():

                tiled_watermark = Image.new('RGBA', preview_image.size)
                for y in range(0, preview_image.height, watermark.height):
                    for x in range(0, preview_image.width, watermark.width):
                        tiled_watermark.paste(watermark, (x, y))
                preview_watermarked = Image.alpha_composite(
                    preview_image.convert('RGBA'), tiled_watermark)
            else:

                x = int((preview_image.width - watermark.width)
                        * self.position_x.get())
                y = int((preview_image.height - watermark.height)
                        * self.position_y.get())

                preview_watermarked = preview_image.copy().convert('RGBA')
                preview_watermarked.paste(watermark, (x, y), watermark)

            self.photo = ImageTk.PhotoImage(preview_watermarked)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(
                0, 0, anchor=tk.NW, image=self.photo)

    def process_images(self):
        if not all([self.input_dir, self.output_dir, self.watermark_path]):
            messagebox.showerror(
                "Error", "Please select all directories and watermark")
            return

        watermark = Image.open(self.watermark_path).convert('RGBA')

        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(self.input_dir, filename)
                output_path = os.path.join(
                    self.output_dir, f"watermarked_{filename}")

                base_image = Image.open(input_path).convert('RGBA')

                watermark_size = (int(base_image.width * self.size_percent.get() / 100),
                                  int(base_image.height * self.size_percent.get() / 100))
                watermark_resized = watermark.resize(
                    watermark_size, Image.LANCZOS)

                enhancer = ImageEnhance.Brightness(
                    watermark_resized.split()[3])
                alpha = enhancer.enhance(self.opacity.get())
                watermark_resized.putalpha(alpha)

                if self.tile_var.get():

                    tiled_watermark = Image.new('RGBA', base_image.size)
                    for y in range(0, base_image.height, watermark_resized.height):
                        for x in range(0, base_image.width, watermark_resized.width):
                            tiled_watermark.paste(watermark_resized, (x, y))
                    watermarked = Image.alpha_composite(
                        base_image, tiled_watermark)
                else:

                    x = int((base_image.width - watermark_resized.width)
                            * self.position_x.get())
                    y = int((base_image.height - watermark_resized.height)
                            * self.position_y.get())

                    watermarked = Image.new(
                        'RGBA', base_image.size, (0, 0, 0, 0))
                    watermarked.paste(base_image, (0, 0))
                    watermarked.paste(watermark_resized,
                                      (x, y), watermark_resized)

                watermarked.convert('RGB').save(
                    output_path, 'JPEG', quality=95)

        messagebox.showinfo("Success", "All images processed successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
