import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import shutil
import os
import imagehash

class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Selector")

        self.image_list = []
        self.selected_image_path = None

        self.selected_image_label = tk.Label(self.root, text="Selected Image:")
        self.selected_image_label.pack()

        self.selected_image_display = tk.Label(self.root)
        self.selected_image_display.pack()

        self.upload_button = tk.Button(self.root, text="Upload Images", command=self.upload_images)
        self.upload_button.pack()

        self.find_duplicates_button = tk.Button(self.root, text="Find Duplicates", command=self.find_duplicates)
        self.find_duplicates_button.pack()

        self.select_button = tk.Button(self.root, text="Select Random Image", command=self.select_random_image)
        self.select_button.pack()

        self.final_button = tk.Button(self.root, text="Final", command=self.copy_selected_image)
        self.final_button.pack()


    def load_images(self, file_paths):
        for file_path in file_paths:
            image = Image.open(file_path)
            self.image_list.append((image, file_path))

    def find_duplicates(self):
        hash_dict = {}
        duplicates = []

        for image, file_path in self.image_list:
            hash_value = imagehash.average_hash(image)
            if hash_value in hash_dict:
                print(f"Duplicate found: {file_path} and {hash_dict[hash_value]}")
                duplicates.append(hash_dict[hash_value])
            else:
                hash_dict[hash_value] = file_path

        return duplicates

    def upload_images(self):
        file_types = [("Image files", ".jpg;.jpeg;.png;.gif")]
        file_paths = filedialog.askopenfilenames(title="Select image files to upload", filetypes=file_types)

        if file_paths:
            self.load_images(file_paths)
            print("Images uploaded successfully.")

    def select_random_image(self):
        if not self.image_list:
            return

        # Filter out duplicates before selecting a random image
        non_duplicates = [item for item in self.image_list if item[1] not in self.find_duplicates()]

        if not non_duplicates:
            print("No non-duplicate images remaining.")
            return

        random_image, self.selected_image_path = random.choice(non_duplicates)
        self.display_image(random_image)
        print(f"Selected Image: {self.selected_image_path}")

    def display_image(self, image):
        resized_image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(resized_image)
        self.selected_image_display.configure(image=photo)
        self.selected_image_display.image = photo

    def copy_selected_image(self):
        if self.selected_image_path:
            destination_directory = filedialog.askdirectory(title="Select destination directory")
            if destination_directory:
                destination_path = os.path.join(destination_directory, os.path.basename(self.selected_image_path))
                shutil.copy2(self.selected_image_path, destination_path)
                print(f"Image copied to: {destination_path}")
            else:
                print("Destination directory not selected.")
        else:
            print("No image selected to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()