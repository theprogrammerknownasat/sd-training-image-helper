import configparser
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

        # Set the default theme
        self.theme = 'light'

        self.minsize(800, 600)

        # Define the color values for the dark theme
        self.dark_theme = {
            'bg': '#2D2D2D',
            'fg': '#CCCCCC',
            'cursor': '#FFCC00',
            'selectbackground': '#FFCC00',
            'selectforeground': '#2D2D2D'
        }

        # Create the menu bar
        self.menu_bar = tk.Menu(self)

        # Create the File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Save', command=self.save_text_file)
        self.file_menu.add_command(label='Delete', command=self.delete_text_file)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Create the Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label='Preferences', command=self.open_preferences)
        self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)

        # Add the menu bar to the window
        self.config(menu=self.menu_bar)

        # Create the panes
        self.pane1 = tk.PanedWindow(self)
        self.pane2 = tk.PanedWindow(self)
        self.pane3 = tk.PanedWindow(self)

        # Arrange the panes
        self.pane1.place(relx=0, rely=0, relwidth=0.1875, relheight=1)  # image chooser
        self.pane2.place(relx=0.1875, rely=0, relwidth=0.5625, relheight=1)  # image viewer
        self.pane3.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)  # text editor

        # Create the image list
        self.image_list = tk.Listbox(self.pane1, borderwidth=0)
        self.image_list.pack(fill='both', expand=True)
        self.image_list.bind('<<ListboxSelect>>', self.on_image_select)

        # Create the image scale slider
        self.image_scale = tk.Scale(self.pane2, from_=1, to=200, orient='horizontal', command=self.on_image_select)
        self.image_scale.pack(fill='x')
        self.image_scale.set(100)

        # Create a frame for the image display canvas
        self.image_frame = tk.Frame(self.pane2)
        self.image_frame.pack(side='left', fill='both', expand=True)

        # Create the image display canvas
        self.image_canvas = tk.Canvas(self.image_frame)
        self.image_canvas.pack(side='left', fill='both', expand=True)

        # Create the vertical scrollbar
        self.image_scrollbar_y = tk.Scrollbar(self.pane2, orient='vertical', command=self.image_canvas.yview)
        self.image_scrollbar_y.pack(side='right', fill='y')
        self.image_canvas.configure(yscrollcommand=self.image_scrollbar_y.set)

        # Create the horizontal scrollbar
        self.image_scrollbar_x = tk.Scrollbar(self.pane2, orient='horizontal', command=self.image_canvas.xview)
        self.image_scrollbar_x.pack(side='bottom', fill='x')
        self.image_canvas.configure(xscrollcommand=self.image_scrollbar_x.set)

        self.image_scrollbar_x.place(relx=0, rely=0.97, relwidth=1, relheight=0.03)
        self.image_scrollbar_y.place(relx=0.97, rely=0, relwidth=0.03, relheight=1)


        # Bind the <MouseWheel> event to the on_mouse_wheel method on the image pane
        self.pane2.bind('<MouseWheel>', self.on_mouse_wheel)

        # Create the image display
        self.image_label = tk.Label(self.pane2)
        self.image_label.pack(fill='both', expand=True)

        # Create the text editor with a minimum width of 26 characters
        self.text_editor = tk.Text(self.pane3, width=26)
        self.text_editor.pack(fill='both', expand=True)

        # Load the preferences
        self.load_preferences()

        self.toggle_theme()

        # Ask the user to choose a folder
        self.folder_path = filedialog.askdirectory()
        self.load_images()

        # Create a temporary file and fill it with random gibberish
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        gibberish = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
        with open(self.temp_file.name, 'w') as file:
            file.write(gibberish)

    def open_preferences(self):
        # Create a new window
        self.preferences_window = tk.Toplevel(self)

        # Apply the current theme to the preferences window
        if self.theme == 'dark':
            self.preferences_window.config(bg=self.dark_theme['bg'])

        # Create a label and a button for the theme option
        tk.Label(self.preferences_window, text='Theme:', padx=10, pady=10).pack(side='left')
        tk.Button(self.preferences_window, text='Toggle Dark/Light Mode', command=self.toggle_theme, padx=10,
                  pady=10).pack(side='left')

    def toggle_theme(self):
        # Toggle between dark and light mode
        if self.theme == 'light':
            self.theme = 'dark'
            self.config(bg=self.dark_theme['bg'])
            self.pane1.config(bg=self.dark_theme['bg'])
            self.pane2.config(bg=self.dark_theme['bg'])
            self.pane3.config(bg=self.dark_theme['bg'])
            self.image_list.config(bg=self.dark_theme['bg'], fg=self.dark_theme['fg'],
                                   selectbackground=self.dark_theme['selectbackground'],
                                   selectforeground=self.dark_theme['selectforeground'])
            self.image_frame.config(bg=self.dark_theme['bg'])
            self.image_canvas.config(bg=self.dark_theme['bg'])
            self.image_scrollbar_x.config(bg=self.dark_theme['bg'], troughcolor=self.dark_theme['bg'],
                                          activebackground=self.dark_theme['bg'])
            self.image_scrollbar_y.config(bg=self.dark_theme['bg'], troughcolor=self.dark_theme['bg'],
                                          activebackground=self.dark_theme['bg'])
            self.image_scale.config(bg=self.dark_theme['bg'], fg=self.dark_theme['fg'],
                                    troughcolor=self.dark_theme['bg'])
            self.text_editor.config(bg=self.dark_theme['bg'], fg=self.dark_theme['fg'],
                                    insertbackground=self.dark_theme['cursor'],
                                    selectbackground=self.dark_theme['selectbackground'],
                                    selectforeground=self.dark_theme['selectforeground'])
        else:
            self.theme = 'light'
            self.config(bg='white')
            self.pane1.config(bg='white')
            self.pane2.config(bg='white')
            self.pane3.config(bg='white')
            self.image_list.config(bg='white', fg='black', selectbackground='blue', selectforeground='white')
            self.image_frame.config(bg='white')
            self.image_canvas.config(bg='white')
            self.image_scrollbar_x.config(bg='white', troughcolor='white', activebackground='white')
            self.image_scrollbar_y.config(bg='white', troughcolor='white', activebackground='white')
            self.image_scale.config(bg='white', fg='black', troughcolor='white')
            self.text_editor.config(bg='white', fg='black', insertbackground='black', selectbackground='blue',
                                    selectforeground='white')

        self.save_preferences()

    def on_image_select(self, event=None):
        # Check if an image is selected
        if not self.image_list.curselection():
            return

        # Display the selected image
        selected_image = self.image_list.get(self.image_list.curselection())
        image_path = os.path.join(self.folder_path, selected_image)
        image = Image.open(image_path)

        # Resize the image based on the value of the scale slider
        scale_percent = self.image_scale.get()
        width = int(image.width * scale_percent / 100)
        height = int(image.height * scale_percent / 100)
        image = image.resize((width, height), Image.LANCZOS)

        # Create a PhotoImage object and keep a reference to it
        self.photo = ImageTk.PhotoImage(image)

        # Clear the canvas and display the image
        self.image_canvas.delete('all')
        self.image_canvas.create_image(0, 0, image=self.photo, anchor='nw')

        # Update the scroll region to fit the size of the image
        self.image_canvas.configure(scrollregion=self.image_canvas.bbox('all'))

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

    def on_mouse_wheel(self, event):
        # Adjust the value of the scale slider
        if event.delta > 0:
            self.image_scale.set(self.image_scale.get() + 1)
        else:
            self.image_scale.set(self.image_scale.get() - 1)

        # Resize the image
        self.on_image_select()

    def save_preferences(self):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Add the current settings to the ConfigParser object
        config['Settings'] = {'theme': self.theme}

        # Determine the appropriate directory to save the file based on the operating system
        if sys.platform == 'win32':
            config_dir = os.path.join(os.environ['APPDATA'], 'SDimageHelper')
        else:
            config_dir = os.path.join(os.path.expanduser('~'), '.local', 'SDimageHelper')

        # Create the directory if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)

        # Write the ConfigParser object to a file in the directory
        with open(os.path.join(config_dir, 'settings.cfg'), 'w') as config_file:
            config.write(config_file)

        print(f"Preferences saved to {os.path.join(config_dir, 'settings.cfg')}")

    def load_preferences(self):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Determine the appropriate directory to read the file from based on the operating system
        if sys.platform == 'win32':
            config_dir = os.path.join(os.environ['APPDATA'], 'SDimageHelper')
        else:
            config_dir = os.path.join(os.path.expanduser('~'), '.local', 'SDimageHelper')

        # Check if the configuration file exists
        config_file_path = os.path.join(config_dir, 'settings.cfg')
        if not os.path.exists(config_file_path):
            print(f"No preferences file found at {config_file_path}")
            return

        # Read the ConfigParser object from the file
        config.read(config_file_path)

        # Apply the settings from the ConfigParser object
        if 'Settings' in config and 'theme' in config['Settings']:
            self.theme = config['Settings']['theme']
            self.toggle_theme()

        print(f"Preferences loaded from {config_file_path}")


if __name__ == '__main__':
    app = Application()
    app.bind('<MouseWheel>', app.on_mouse_wheel)
    app.mainloop()
