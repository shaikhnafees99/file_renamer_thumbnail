import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import shutil
from pathlib import Path
from datetime import datetime

class FileRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer")
        self.root.geometry("800x700")
        
        # Initialize main frames first
        self.main_content = ttk.Frame(root)
        self.main_content.pack(fill="both", expand=True)
        
        # Left side container
        self.left_side = ttk.Frame(self.main_content)
        self.left_side.pack(side="left", fill="both", expand=True, padx=5)
        
        # Right side container
        self.right_side = ttk.Frame(self.main_content)
        self.right_side.pack(side="right", fill="y", padx=5)
        
        # Folder path frame
        self.folder_frame = ttk.LabelFrame(self.left_side, text="Folder Selection", padding="10")
        self.folder_frame.pack(fill="x", pady=5)
        
        self.folder_path = tk.StringVar()
        self.folder_entry = ttk.Entry(self.folder_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.pack(side="left", padx=5)
        
        self.browse_button = ttk.Button(self.folder_frame, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side="left", padx=5)
        
        # Count information frame
        self.count_frame = ttk.LabelFrame(self.left_side, text="File Counts", padding="10")
        self.count_frame.pack(fill="x", pady=5)
        
        self.file_count_var = tk.StringVar(value="Files in directory: 0")
        self.name_count_var = tk.StringVar(value="New names provided: 0")
        self.status_var = tk.StringVar(value="Status: Waiting for input")
        
        ttk.Label(self.count_frame, textvariable=self.file_count_var).pack(anchor="w")
        ttk.Label(self.count_frame, textvariable=self.name_count_var).pack(anchor="w")
        self.status_label = ttk.Label(self.count_frame, textvariable=self.status_var)
        self.status_label.pack(anchor="w")
        
        # Names input frame
        self.names_frame = ttk.LabelFrame(self.left_side, text="New File Names", padding="10")
        self.names_frame.pack(fill="both", expand=True, pady=5)
        
        self.names_text = tk.Text(self.names_frame, height=12, width=50)
        self.names_text.pack(side="left", fill="both", expand=True)
        self.names_text.bind('<<Modified>>', self.on_text_modified)
        
        self.scrollbar = ttk.Scrollbar(self.names_frame, orient="vertical", command=self.names_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.names_text.configure(yscrollcommand=self.scrollbar.set)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self.left_side, text="Preview", padding="10")
        self.preview_frame.pack(fill="both", expand=True, pady=5)
        
        self.preview_text = tk.Text(self.preview_frame, height=8, width=50, state="disabled")
        self.preview_text.pack(side="left", fill="both", expand=True)
        
        self.preview_scrollbar = ttk.Scrollbar(self.preview_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_scrollbar.pack(side="right", fill="y")
        self.preview_text.configure(yscrollcommand=self.preview_scrollbar.set)
        
        # Thumbnail frame (right side)
        self.thumbnail_frame = ttk.LabelFrame(self.right_side, text="Thumbnail Preview", padding="10")
        self.thumbnail_frame.pack(fill="both", expand=True)
        
        # Canvas for thumbnail and text overlay
        self.thumbnail_canvas = tk.Canvas(self.thumbnail_frame, width=200, height=200)
        self.thumbnail_canvas.pack(fill="both", expand=True)
        
        # Buttons frame
        self.button_frame = ttk.Frame(self.left_side)
        self.button_frame.pack(fill="x", pady=5)
        
        self.preview_button = ttk.Button(self.button_frame, text="Preview Changes", command=self.preview_changes)
        self.preview_button.pack(side="left", padx=5)
        
        self.rename_button = ttk.Button(self.button_frame, text="Rename Files", command=self.rename_files)
        self.rename_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(self.button_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(side="right", padx=5)
        
        # Initialize variables
        self.current_thumbnail = None
        self.current_ref_number = None
        self.current_file_path = None
        
        # Create downloads directory
        self.renamed_files_dir = os.path.join(str(Path.home()), "Downloads", "Renamed Files")
        os.makedirs(self.renamed_files_dir, exist_ok=True)

    def create_thumbnail_with_overlay(self, image_path, new_name=None):
        try:
            self.current_file_path = image_path
            # Open and resize image
            image = Image.open(image_path)
            
            # Calculate aspect ratio
            aspect_ratio = image.width / image.height
            
            # Set thumbnail size
            thumb_width = 200
            thumb_height = int(thumb_width / aspect_ratio)
            
            # Resize image
            image = image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            
            # Create drawing object
            draw = ImageDraw.Draw(image)
            
            # Get filename without extension for reference
            ref_number = os.path.splitext(os.path.basename(image_path))[0]
            self.current_ref_number = ref_number
            
            # Use new name if provided, otherwise use reference number
            display_text = new_name if new_name else ref_number
            
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Calculate text size
            text_bbox = draw.textbbox((0, 0), display_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Add semi-transparent black background
            padding = 4
            bg_left = thumb_width - text_width - (padding * 2)
            bg_top = thumb_height - text_height - (padding * 2)
            bg_right = thumb_width
            bg_bottom = thumb_height
            
            # Draw semi-transparent black background
            background_shape = [(bg_left, bg_top), (bg_right, bg_bottom)]
            draw.rectangle(background_shape, fill=(0, 0, 0, 128))
            
            # Position text
            text_position = (thumb_width - text_width - padding, thumb_height - text_height - padding)
            
            # Draw text
            draw.text(text_position, display_text, font=font, fill="white")
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            self.current_thumbnail = photo
            
            # Update canvas
            self.thumbnail_canvas.delete("all")
            self.thumbnail_canvas.create_image(100, 100, image=photo, anchor="center")
            
        except Exception as e:
            print(f"Error creating thumbnail: {e}")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.update_counts()
            self.load_first_image_thumbnail()

    def load_first_image_thumbnail(self):
        folder = self.folder_path.get()
        if not folder:
            return
            
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        for file in os.listdir(folder):
            if file.lower().endswith(image_extensions):
                image_path = os.path.join(folder, file)
                self.create_thumbnail_with_overlay(image_path)
                break

    def on_text_modified(self, event=None):
        self.names_text.edit_modified(False)
        self.update_counts()
        
        # Update thumbnail with new name if available
        if self.current_file_path:
            new_names = self.get_new_names()
            if new_names and len(new_names) > 0:
                self.create_thumbnail_with_overlay(self.current_file_path, new_names[0])

    def update_counts(self):
        folder = self.folder_path.get()
        new_names = self.get_new_names()
        
        file_count = 0
        if folder and os.path.exists(folder):
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            file_count = len(files)
        
        name_count = len(new_names)
        
        self.file_count_var.set(f"Files in directory: {file_count}")
        self.name_count_var.set(f"New names provided: {name_count}")
        
        if file_count == 0 and name_count == 0:
            self.status_var.set("Status: Waiting for input")
            self.status_label.configure(foreground="black")
        elif file_count == name_count:
            self.status_var.set("Status: ✓ Counts match")
            self.status_label.configure(foreground="green")
        else:
            self.status_var.set("Status: ✗ Counts don't match")
            self.status_label.configure(foreground="red")

    def get_new_names(self):
        names_text = self.names_text.get("1.0", tk.END).strip()
        return [name.strip() for name in names_text.split('\n') if name.strip()]

    def preview_changes(self):
        folder = self.folder_path.get()
        new_names = self.get_new_names()
        
        if not folder or not new_names:
            messagebox.showwarning("Warning", "Please select a folder and enter new names.")
            return
            
        files = sorted([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])
        
        if len(files) != len(new_names):
            messagebox.showerror("Error", 
                f"Number of files ({len(files)}) doesn't match number of new names ({len(new_names)}).\n"
                "Please provide exactly one name for each file.")
            return
        
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)
        
        for i, (old_name, new_name) in enumerate(zip(files, new_names)):
            ext = os.path.splitext(old_name)[1]
            new_name_with_ext = f"{new_name}{ext}"
            self.preview_text.insert(tk.END, f"{old_name} → {new_name_with_ext}\n")
        
        self.preview_text.configure(state="disabled")
        
        # Update thumbnail with first new name
        if self.current_file_path and new_names:
            self.create_thumbnail_with_overlay(self.current_file_path, new_names[0])
    def process_image_with_overlay(self, image_path, new_name):
        """Add text overlay to the actual image"""
        try:
            # Open original image
            image = Image.open(image_path)
            
            # Create drawing object
            draw = ImageDraw.Draw(image)
            
            # Try to use Arial font, fall back to default if not available
            try:
                # Use larger font size for the actual image
                font_size = int(min(image.width, image.height) * 0.05)  # 5% of image size
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate text size
            text_bbox = draw.textbbox((0, 0), new_name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Add semi-transparent black background
            padding = int(text_height * 0.2)  # 20% of text height for padding
            bg_left = image.width - text_width - (padding * 2)
            bg_top = image.height - text_height - (padding * 2)
            bg_right = image.width
            bg_bottom = image.height
            
            # Draw semi-transparent black background
            background_shape = [(bg_left, bg_top), (bg_right, bg_bottom)]
            draw.rectangle(background_shape, fill=(0, 0, 0, 128))
            
            # Position text
            text_position = (image.width - text_width - padding, 
                           image.height - text_height - padding)
            
            # Draw text
            draw.text(text_position, new_name, font=font, fill="white")
            
            return image
            
        except Exception as e:
            print(f"Error processing image overlay: {e}")
            return None

    def rename_files(self):
        folder = self.folder_path.get()
        new_names = self.get_new_names()
        
        if not folder or not new_names:
            messagebox.showwarning("Warning", "Please select a folder and enter new names.")
            return
            
        files = sorted([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])
        
        if len(files) != len(new_names):
            messagebox.showerror("Error", 
                f"Number of files ({len(files)}) doesn't match number of new names ({len(new_names)}).\n"
                "Please provide exactly one name for each file.")
            return
        
        try:
            # Create a new directory for this batch
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_dir = os.path.join(self.renamed_files_dir, f"renamed_{timestamp}")
            os.makedirs(batch_dir, exist_ok=True)
            
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
            
            for old_name, new_name in zip(files, new_names):
                ext = os.path.splitext(old_name)[1]
                new_name_with_ext = f"{new_name}{ext}"
                
                old_path = os.path.join(folder, old_name)
                new_path = os.path.join(batch_dir, new_name_with_ext)
                
                if os.path.exists(new_path):
                    raise FileExistsError(f"File {new_name_with_ext} already exists!")
                
                # If it's an image file, process it with overlay
                if ext.lower() in image_extensions:
                    processed_image = self.process_image_with_overlay(old_path, new_name)
                    if processed_image:
                        processed_image.save(new_path, quality=95)
                    else:
                        # If overlay processing fails, just copy the original
                        shutil.copy2(old_path, new_path)
                else:
                    # For non-image files, just copy
                    shutil.copy2(old_path, new_path)
                
            messagebox.showinfo("Success", f"Files copied and renamed successfully!\nLocation: {batch_dir}")
            self.preview_changes()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    

    def clear_all(self):
        self.folder_path.set("")
        self.names_text.delete("1.0", tk.END)
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.configure(state="disabled")
        self.thumbnail_canvas.delete("all")
        self.current_thumbnail = None
        self.current_ref_number = None
        self.current_file_path = None
        self.update_counts()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamer(root)
    root.mainloop()