import io
import os
import random
import string
import sys
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('SD AI training image helper')
        self.geometry('800x600')

        # Create the panes
        self.pane1 = tk.PanedWindow(self)
        self.pane2 = tk.PanedWindow(self)
        self.pane3 = tk.PanedWindow(self)

        # Arrange the panes
        self.pane1.pack(side='left', fill='both', expand=True)
        self.pane2.pack(side='left', fill='both', expand=True)
        self.pane3.pack(side='left', fill='both', expand=True)

        # Create the image list
        self.image_list = tk.Listbox(self.pane1)
        self.image_list.pack(fill='both', expand=True)
        self.image_list.bind('<<ListboxSelect>>', self.on_image_select)

        # Create the image display
        self.image_label = tk.Label(self.pane2)
        self.image_label.pack(fill='both', expand=True)

        # Create the text editor
        self.text_editor = tk.Text(self.pane3)
        self.text_editor.pack(fill='both', expand=True)

        # Create the save button
        self.save_button = tk.Button(self.pane3, text='Save', command=self.save_text_file)
        self.save_button.pack()

        # Create the delete button
        self.delete_button = tk.Button(self.pane3, text='Delete', command=self.delete_text_file)
        self.delete_button.pack()

        # Create the save status label
        self.saved_label = tk.Label(self.pane3, text='')
        self.saved_label.pack()

        # Bind the Control-S key combination to the save_text_file method
        self.bind('<Control-s>', self.save_text_file)

        # Ask the user to choose a folder
        self.folder_path = filedialog.askdirectory()
        self.load_images()

        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        gibberish = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
        with open(self.temp_file.name, 'w') as file:
            file.write(gibberish)

    def on_image_select(self, event):
        # Check if an image is selected
        if not self.image_list.curselection():
            return

        # Display the selected image
        selected_image = self.image_list.get(self.image_list.curselection())
        image_path = os.path.join(self.folder_path, selected_image)
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        # Load the corresponding text file, if it exists
        text_file_path = os.path.splitext(image_path)[0] + '.txt'
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as file:
                content = file.read()
            self.text_editor.delete('1.0', tk.END)
            self.text_editor.insert(tk.END, content)
            # Set the current text file
            self.current_text_file = text_file_path
        else:
            # Ask the user if they want to create a new text file
            if messagebox.askyesno('Create text file', 'Do you want to create a new text file for this image?'):
                with open(text_file_path, 'w') as file:
                    file.write('')
                self.text_editor.delete('1.0', tk.END)
                # Set the current text file
                self.current_text_file = text_file_path

        # Set the focus to the text editor
        self.text_editor.focus_set()

    def delete_text_file(self):
        # Check if an image is selected
        if not self.image_list.curselection():
            return

        # Check if a current text file is set
        if not hasattr(self, 'current_text_file'):
            return

        # Check if the current text file exists
        if not os.path.exists(self.current_text_file):
            return

        # Ask the user to confirm the deletion
        if not messagebox.askyesno('Delete text file', 'Are you sure you want to delete this text file?'):
            return

        # Delete the current text file
        os.remove(self.current_text_file)
        self.current_text_file = None

        # Ask the user if they want to create a new text file
        messagebox.showinfo('Important info', 'Please restart the progrtam to make a new file')
        if messagebox.askyesno('Restart?', 'Do you want to restart the program?'):
            python = sys.executable
            os.execl(python, python, *sys.argv)

    def load_images(self):
        # Load the images and corresponding text files from the chosen folder
        for file in os.listdir(self.folder_path):
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.PNG') or file.endswith('.JPG'):
                self.image_list.insert(tk.END, file)

    def save_text_file(self, event=None):
        # Check if a current text file is set
        if not hasattr(self, 'current_text_file') or self.current_text_file is None:
            return

        # Check if the current text file exists
        if not os.path.exists(self.current_text_file):
            return

        # Save the contents of the text editor to the current text file
        with open(self.current_text_file, 'w') as file:
            file.write(self.text_editor.get('1.0', tk.END))
        self.saved_label.config(text='Saved')

if __name__ == '__main__':
    app = Application()
    app.mainloop()