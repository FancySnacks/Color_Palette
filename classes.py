from helper_functions import is_hex_color, is_rgb_color, hex_to_rgb, rgb_to_hex, random_rgb
from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import pyperclip
import ast



# Main GUI window
class MainWindow:
    def __init__(self):
        # GUI creation
        self.root = Tk()
        self.root.geometry("670x425")
        self.root.resizable(height=False, width=False)
        self.root.title("Color Palette")
        self.root.config(bg="#212024")

        # Variables
        self.HistoryMaster = None
        self.PaletteMaster = None
        self.ColorButton = None
        self.picked_color: tuple = ()
        self.context = ""
        self.on_top = False
        self.opacity_value = StringVar(self.root)
        self.opacity_value.set("100")

        self.hex_user_entry = StringVar(self.root)
        self.previous_hex = "#c72231"
        self.rgb_user_entry = StringVar(self.root)
        self.previous_rgb = hex_to_rgb(self.previous_hex)
        self.manual_entry = False

        # Palettes
        self.saved_palettes = []
        self.saved_palettes.append(Palette("Temporary Palette", []))
        self.palettes = self.saved_palettes

        self.selected_palette = StringVar(self.root)
        self.selected_palette.set(self.saved_palettes[0].name)
        self.current_palette = self.saved_palettes[0]

        # User Preferences
        self.savefile_dir = "./save/palettes.txt"
        self.configfile_dir = "./save/config.txt"

        self.DEFAULT_SETTINGS = {"AutoLoadSaveFile":"True",
                              "PaletteSaveFileDir":f'{self.savefile_dir}',
                              "ConfigFileDir":f'{self.configfile_dir}'}
        self.user_settings = self.DEFAULT_SETTINGS


        # --- Main Container --- #

        self.MainFrame = Frame(self.root, padx=5, pady=5, bg="#212024")
        self.MainFrame.pack(expand=True, fill=Y)

        # --- Top Toolbar --- #
        self.MenuBar = Menu(self.root)
        self.root.config(menu=self.MenuBar)

        self.FileMenu = Menu(self.MenuBar)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)
        self.FileMenu.add_command(label="Exit", command=exit)


        # --- Top Toolbar --- #

        self.MenuBar = Menu(self.root)
        self.root.config(menu=self.MenuBar)

        # File Menu
        self.FileMenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)

        # General TOol Menu
        self.ToolMenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="Edit", menu=self.ToolMenu)
        self.ToolMenu.add_command(label="Random Color", command=self.add_random_color)
        self.ToolMenu.add_command(label="Random Palette", command=exit)
        self.ToolMenu.add_command(label="Eyedropper", command=exit)

        # Palette Tool Menu
        self.PaletteToolMenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="Palettes", menu=self.PaletteToolMenu)
            # General
        self.PaletteToolMenu.add_command(label="Save All Palettes", command=self.save_palette)
        self.PaletteToolMenu.add_command(label="Reload Save File", command=self.reload_palettes)
        self.PaletteToolMenu.add_separator()

        # Import Menu
        self.ImportMenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="Import", menu=self.ImportMenu)
            # Palette Import
        self.ImportMenu.add_command(label="Image as Palette", command=exit)
        self.ImportMenu.add_command(label="Text File as Palette", command=exit)

        # Export Menu
        self.ExportMenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="Export", menu=self.ExportMenu)
            # History Export
        self.ExportMenu.add_command(label="History as Text File", command=exit)
        self.ExportMenu.add_command(label="History as Image", command=exit)
        self.ExportMenu.add_separator()
            # Palette Export
        self.ExportMenu.add_command(label="Palette as Text File", command=exit)
        self.ExportMenu.add_command(label="Palette as Image", command=exit)

        # About Menu
        self.AboutMenu = Menu(self.MenuBar, tearoff=0)
        self.MenuBar.add_cascade(label="About", menu=self.AboutMenu)
        self.AboutMenu.add_command(label="Info")
        self.AboutMenu.add_command(label="README")


        # --- Bottom Toolbar --- #

        # Toolbar
        self.ToolbarFrame = Frame(self.root, bg="#212024", padx=10)
        self.ToolbarFrame.pack(expand=True, fill=X, anchor="s")

        self.ToolbarDivider = Frame(self.ToolbarFrame, bg="white", width=650, pady=3)
        self.ToolbarDivider.grid(row=0, columnspan=10)

        # Stay-On-Top Button
        self.StayOnTopFrame = Frame(self.ToolbarFrame, bg="#212024", pady=2)
        self.StayOnTopFrame.grid(row=1, column=0, sticky="W")

        self.StayOnTopButton = Button(self.StayOnTopFrame,
                                      font=("Lato", 9),
                                      text="⬜ Unlocked",
                                      fg="white",
                                      bg="#212024",
                                      command=self.stay_on_top)
        self.StayOnTopButton.grid(row=0, column=0, sticky="W")

        # Opacity Scale
        self.OpacitySlider = ttk.Scale(self.ToolbarFrame,
                                       from_=10,
                                       to=100,
                                       variable=self.opacity_value,
                                       command=self.change_window_opacity,
                                       orient=HORIZONTAL)
        self.OpacitySlider.set(100)
        self.OpacitySlider.grid(row=1, column=1, sticky="E")

        self.OpacityLabel = Label(self.ToolbarFrame,
                                  textvariable=self.opacity_value,
                                  bg="#212024",
                                  fg="white")
        self.OpacityLabel.grid(row=1, column=2, sticky="E")
        self.OpacityLabel.config(text=f'{self.opacity_value.get()}%')

        # Eyedropper Tool
        self.EyedropperFrame = Frame(self.ToolbarFrame, bg="#212024", pady=2)
        self.EyedropperFrame.grid(row=1, column=6, sticky="W")

        self.EyedropperButton = Button(self.EyedropperFrame,
                                       font=("Lato", 9),
                                       text="🖊 Sample Color",
                                       fg="white",
                                       bg="#212024")
        self.EyedropperButton.grid(row=0, column=0, sticky="W")

        # Import Palette Button
        self.ImportFrame = Frame(self.ToolbarFrame, bg="#212024", pady=2)
        self.ImportFrame.grid(row=1, column=7, sticky="E")

        self.ImportButton = Button(self.ImportFrame,
                                   font=("Lato", 10),
                                   text="⬇ Import ",
                                   fg="white",
                                   bg="#212024")
        self.ImportButton.grid(row=0, column=0, sticky="E")

        # Export Palette Button
        self.ExportFrame = Frame(self.ToolbarFrame, bg="#212024", pady=2)
        self.ExportFrame .grid(row=1, column=8, sticky="E")

        self.ExportButton = Button(self.ExportFrame,
                                   font=("Lato", 10),
                                   text="⬆ Export ",
                                   fg="white",
                                   bg="#212024")
        self.ExportButton.grid(row=0, column=0, sticky="E")

        # Save Palettes Button

        self.SaveFrame = Frame(self.ToolbarFrame, bg="#212024", pady=2)
        self.SaveFrame.grid(row=1, column=9, sticky="E")
        self.SaveButton = Button(self.SaveFrame,
                                 font=("Lato", 10),
                                 text="Save Palettes ",
                                 fg="white",
                                 bg="#212024",
                                 command=self.save_palette)
        self.SaveButton.grid(row=0, column=0, sticky="E")


        # --- Color Picker --- #

        # Color Picker Frame
        self.ColorFrame = Frame(self.MainFrame, bg="#212024")
        self.ColorFrame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="NW")

        self.ColorLabel = Label(self.ColorFrame,
                                font=("Lato", 12),
                                bg="#212024",
                                text="🌈  Color Picker",
                                fg="white", pady=5)
        self.ColorLabel.grid(row=0, column=0, sticky="NW")

        color_button = ColorButton(self.root, self, self.ColorFrame, 10, 25)
        self.ColorButton = color_button

        # Color values
        # HEX
        self.HexFrame = Frame(self.ColorFrame, bg="#212024")
        self.HexFrame.grid(row=3, column=0, sticky="NW")

        self.HexLabel = Label(self.HexFrame,
                              text="Hex Code :",
                              font=("Lato", 11, "bold"),
                              bg="#212024",
                              fg="#aba7a7",
                              pady=5)
        self.HexLabel.grid(row=0, column=0, sticky="NW")

        self.HexEntryFrame = Frame(self.HexFrame)
        self.HexEntryFrame.grid(row=0, column=1)

        self.HexEntry = Entry(self.HexEntryFrame,
                              font=("Arial", 11),
                              width=10,
                              bg="#212024",
                              fg="white",
                              textvariable=self.hex_user_entry)
        self.HexEntry.insert(END, color_button.current_color[1])
        self.HexEntry.grid(row=0, column=0, sticky="NW")

        self.HexCopyButton = ClipboardButton(self.root, MainWindow, self.HexFrame, color_button.current_color[1])

        # RGB
        self.RGBFrame = Frame(self.ColorFrame, bg="#212024")
        self.RGBFrame.grid(row=4, column=0, sticky="NW")

        self.RGBLabel = Label(self.RGBFrame,
                              text="RGB Code :",
                              font=("lato", 11, "bold"),
                              bg="#212024",
                              fg="#aba7a7",
                              pady=5)
        self.RGBLabel.grid(row=0, column=0, sticky="NW")

        self.RGBEntryFrame = Frame(self.RGBFrame)
        self.RGBEntryFrame.grid(row=0, column=1)

        self.RGBEntry = Entry(self.RGBEntryFrame,
                              font=("Arial", 11),
                              width=10,
                              bg="#212024",
                              fg="white",
                              textvariable=self.rgb_user_entry)
        self.RGBEntry.insert(END, color_button.current_color[0])
        self.RGBEntry.grid(row=0, column=0, sticky="NW")

        self.RGBCopyButton = ClipboardButton(self.root, MainWindow, self.RGBFrame, color_button.current_color[0])

        # Add color to palette button
        self.AddColorFrame = Frame(self.ColorFrame, bg="#212024", padx=8, pady=3)
        self.AddColorFrame.grid(row=2, column=0, sticky="NW")
        self.AddColorButton = Button(self.AddColorFrame,
                                     font=("Arial", 10),
                                     text="➕ Add ",
                                     fg="white",
                                     bg="#212024",
                                     command=self.add_color_to_palette)
        self.AddColorButton.grid(row=0, column=0, sticky="NW")

        # Remove color from palette button
        self.DelColorButton = Button(self.AddColorFrame,
                                     font=("Arial", 10),
                                     text="❌ Remove (🎨)",
                                     fg="white",
                                     bg="#212024",
                                     command=self.remove_color)
        self.DelColorButton.grid(row=0, column=1, sticky="NW")


        # --- Color History --- #

        # Color History Frame
        self.HistoryFrame = Frame(self.MainFrame, bg="#212024", padx=15)
        self.HistoryFrame.grid(row=0, column=2, rowspan=2, columnspan=2, sticky="NE")

        self.HistoryLabel = Label(self.HistoryFrame,
                                  font=("Lato", 12),
                                  bg="#212024",
                                  text="⌛  History",
                                  fg="white",
                                  pady=5)
        self.HistoryLabel.grid(row=0, column=0, sticky="NW")

        # Create 'History Master' object, it manages history of chosen colors
        self.HistoryMaster = HistoryMaster(self.root, self, self.HistoryFrame)
        self.HistoryMaster.add_to_history(self.ColorButton.current_color)

        # Clear History Button
        self.ClearButtonFrame = Frame(self.HistoryFrame, bg="#212024")
        self.ClearButtonFrame.grid(row=1, column=0, sticky="NW")
        self.ClearButton = Button(self.ClearButtonFrame,
                                  font=("Arial", 10),
                                  text="❌  Clear  ",
                                  fg="white",
                                  bg="#212024",
                                  command=self.HistoryMaster.clear_history)
        self.ClearButton.grid(row=0, column=0, sticky="NW")


        # --- Color Palettes --- #

        # Palette List Frame
        self.PaletteFrame = Frame(self.MainFrame, bg="#212024", padx=10)
        self.PaletteFrame.grid(row=0, column=4, rowspan=2, columnspan=2, sticky="NE")

        self.PaletteLabel = Label(self.PaletteFrame,
                                  font=("Lato", 12),
                                  bg="#212024",
                                  text="🎨  Palettes",
                                  fg="white",
                                  pady=5)
        self.PaletteLabel.grid(row=0, column=0, sticky="NW")

        # Create 'Palette Master' object, it manages all created and saved color palettes
        self.PaletteMaster = HistoryMaster(self.root, self, self.PaletteFrame)

        # Palette Tools Frame
        self.PaletteMenuFrame = Frame(self.PaletteFrame, bg="#212024")
        self.PaletteMenuFrame.grid(row=1, column=0, columnspan=3)

        # Palette selection dropdown box
        self.PaletteMenu = ttk.Combobox(self.PaletteMenuFrame, values=self.get_palettes(), width=20)
        self.PaletteMenu.config(textvariable=self.selected_palette)
        self.PaletteMenu.grid(row=0, column=0, columnspan=2)

        self.PaletteMenu.bind("<<ComboboxSelected>>", self.on_palette_changed)

        # Palette Create Button
        self.PaletteAddFrame = Frame(self.PaletteMenuFrame, bg="#212024", padx=4, pady=3)
        self.PaletteAddFrame.grid(row=0, column=2, sticky="NW")

        self.PaletteAddButton = Button(self.PaletteAddFrame,
                                       font=("Lato", 10),
                                       text="➕",
                                       fg="white",
                                       bg="#212024",
                                     command=self.add_palette)
        self.PaletteAddButton.grid(row=0, column=0, sticky="NW")

            # Palette Rename Button
        self.PaletteRenameFrame = Frame(self.PaletteMenuFrame, bg="#212024", padx=2, pady=3)
        self.PaletteRenameFrame.grid(row=0, column=3, sticky="NW")

        self.PaletteRenameButton = Button(self.PaletteRenameFrame,
                                          font=("Lato", 10),
                                          text="✏",
                                          fg="white",
                                          bg="#212024",
                                          command=self.show_rename_menu)
        self.PaletteRenameButton.grid(row=0, column=0, sticky="NW")

            # Palette Delete Button
        self.PaletteDelFrame = Frame(self.PaletteMenuFrame, bg="#212024", padx=2, pady=3)
        self.PaletteDelFrame.grid(row=0, column=4, sticky="NW")

        self.PaletteDelButton = Button(self.PaletteDelFrame,
                                       font=("Lato", 10),
                                       text="❌",
                                       fg="white",
                                       bg="#212024",
                                       command=self.delete_palette)
        self.PaletteDelButton.grid(row=0, column=0, sticky="NW")

        self.PaletteToolMenu.add_command(label="Clear History", command=self.HistoryMaster.clear_history)
        self.PaletteToolMenu.add_command(label="Clear Palette", command=self.PaletteMaster.clear_history)


        # --- GUI Initialization --- #

        # Display main window
        self.hex_user_entry.trace_add("write", self.hex_enter)
        self.rgb_user_entry.trace_add("write", self.rgb_enter)

        self.toggle_button_state()
        self.update_context("history")
        self.load_config()
        self.load_palettes_from_file()

        self.toggle = BooleanVar(self.root)
        self.toggle.set(True) if self.user_settings['AutoLoadSaveFile'] in ["true", "True", True] else self.toggle.set(False)
        self.FileMenu.add_checkbutton(label="Load Save File on Start", variable=self.toggle, command=self.autoload_savefile_toggle)
        self.FileMenu.add_command(label="Reset Config File", command=self.reset_config)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Exit", command=exit)

        self.root.mainloop()


    # --- Functions --- #

    def update_color_values(self, hex_value: str, rgb_value: tuple, context: str):
        self.manual_entry = False

        # Update HEX value
        self.update_context(context)
        self.HexEntry.delete(0, END)
        self.manual_entry = False
        self.HexEntry.insert(END, hex_value)
        self.previous_hex = str(hex_value)

        # Update RGB value
        f_rgb_value = ' '.join(str(rgb_value).split()).replace("(", "").replace(")", "")
        self.RGBEntry.delete(0, END)
        self.manual_entry = False
        self.RGBEntry.insert(END, f_rgb_value)

        # Update clipboard buttons
        self.HexCopyButton.color_value = hex_value
        self.RGBCopyButton.color_value = f_rgb_value

        self.HistoryMaster.add_to_history((rgb_value, hex_value)) # Add new color to the history

    # Update the 'remove button' context so in future it will remove color from either color history or current palette >
    # depending on where the color button you've clicked on is located
    def update_context(self, context: str):
        self.context = context
        if context == "palette":
            self.DelColorButton.config(text="❌ Remove (🎨)")
        else:
            self.DelColorButton.config(text="❌ Remove (⌛)")

    # Add picked color to the current palette
    def add_color_to_palette(self):
        self.PaletteMaster.add_to_palette((self.ColorButton.current_color[0], self.ColorButton.current_color[1], "Name"))
        self.update_context("palette")

    # Remove color from current palette
    def remove_color(self):
        if self.context == "palette":
            self.PaletteMaster.remove_from_palette(self.ColorButton.current_color)
        else:
            self.HistoryMaster.remove_from_history(self.ColorButton.current_color)

    # Get names of all created palettes
    def get_palettes(self):
        return [Palette.name for Palette in self.palettes]

    # Triggers when you switch to another palette using the dropdown box
    # TODO: Obsolete, replace references with the function below, then remove it.
    def on_palette_changed(self, event):
        print("Switched to " + self.selected_palette.get())
        self.on_palette_changed_event()

    # Triggers when you switch to another palette using the dropdown box
    def on_palette_changed_event(self):
        self.current_palette = None
        # Find the currently selected palette
        for palette in self.palettes:
            if palette.name == self.selected_palette.get():
                self.current_palette = palette
        # Clear palette colors
        self.PaletteMaster.clear_history()
        colors = self.current_palette.colors if self.current_palette else None
        # Add colors of the currently selected palette
        if colors:
            for color in colors:
                self.PaletteMaster.add_to_palette(color)
        self.toggle_button_state()

    # Disable rename button for the Temporary Palette
    def toggle_button_state(self):
        if self.current_palette == self.palettes[0]:
            self.PaletteRenameButton.config(state=DISABLED)
            self.PaletteDelButton.config(state=DISABLED)
        else:
            self.PaletteRenameButton.config(state=NORMAL)
            self.PaletteDelButton.config(state=NORMAL)

    # Create new palette
    def add_palette(self):
        prev = self.selected_palette.get()
        list = ' '.join(self.get_palettes()).split()   # Differentiate pallets when creating new ones
        int = list.count("New") + 1
        name = f'New Palette #{int}'

        new_palette = Palette(name, self.PaletteMaster.colors)

        self.palettes.append(new_palette)
        self.PaletteMenu.config(values=self.get_palettes())
        self.selected_palette.set(self.palettes[-1].name)
        self.current_palette = self.palettes[-1]

        self.toggle_button_state()

        # Clear colors in a palette if the previous one wasn't a 'Temporary Palette'
        # Temporary Palette is a working area that is reset upon closing the program
        # Temporary Palette copies the palettes over to the new palett you create
        if prev != "Temporary Palette":
            self.PaletteMaster.clear_history()

        return new_palette

    # Remove palette
    def delete_palette(self):
        if self.selected_palette.get() != "Temporary Palette":  # Prevent user from accidentally deleting the work area palette
            index = self.get_palettes().index(self.selected_palette.get())
            self.selected_palette.set(self.palettes[0].name if self.palettes[index-1] == None else self.palettes[index-1].name)
            self.current_palette = self.palettes[0]if self.palettes[index-1] == None else self.palettes[index-1]
            self.palettes.pop(index)
            self.saved_palettes = self.palettes
            self.PaletteMenu.config(values=self.get_palettes())  # Update palette list in the dropdown menu
            self.on_palette_changed_event()
            self.toggle_button_state()

    # Save current palette to a save file
    def save_palette(self):
        if self.does_save_file_exist(self.savefile_dir):
            self.palette_to_text("w")
        else:
            self.palette_to_text("x") # Create a fresh save file if there isn't one in the directory

    # Save palettes into a text file
    def palette_to_text(self, mode: str):
        results = ""
        file = open(self.savefile_dir, mode)
        if len(self.palettes) > 1:
            for palette in self.palettes:
                if palette.name != "Temporary Palette":
                    results += str(([palette.name, palette.colors])) + "\n"
                    # Each line represents separate color palette
                    # Format: [Palette_Name, [color list]]
                    # Color list element format: (rgb_value, hex_value)
        file.write(str(results))
        file.close()

    def does_save_file_exist(self, name: str):
        try:
            with open(name, "r") as f:
                print("Found save file")
                return True
        except:
            print("Save file doesn't exist")
            return False

    # Load saved palettes from a save file on program launch
    def load_palettes_from_file(self):
        if self.user_settings['AutoLoadSaveFile'] in [True, "true", "True"]:
            if self.does_save_file_exist(self.savefile_dir):
                file = open(self.savefile_dir, "r")

                lines = file.readlines()
                if len(lines) > 0:
                    for line in lines: # read lines from text file, each palette is a separate line
                        palette_info = ast.literal_eval(line) # convert string representation of a list into actual list of colors
                        new_palette = self.add_palette()
                        self.palettes[-1].name = palette_info[0]
                        self.palettes[-1].colors = palette_info[1]
                        self.PaletteMenu.config(values=self.get_palettes())

                    self.selected_palette.set(self.palettes[0].name)
                    self.on_palette_changed_event()
                    print(self.get_palettes())
            else:
                pass

    # Reload save file again
    # Dangerous: will clear newly created unsaved palettes
    def reload_palettes(self):
        self.PaletteMaster.clear_history()
        self.palettes = []
        self.palettes.append(Palette("Temporary Palette", []))
        self.load_palettes_from_file()

    # Load user preferences
    def load_config(self) -> dict[str:str]:
        if self.does_save_file_exist(self.configfile_dir):
            settings = "{"
            with open(self.configfile_dir, "r") as file:
                file_contents: list[str] = file.readlines()
                for line in file_contents:
                    settings += line + ","
                settings = settings[0:-1:]
                settings += "}"
                settings.replace("\n", "").strip()
            self.user_settings = ast.literal_eval(settings)
        else:
            # create new config file
            self.reset_config()
        self.set_config_settings()

    def set_config_settings(self):
        self.autoload_savefile = self.load_setting_value("AutoLoadSaveFile", ["true", "false"])
        self.savefile_dir = self.load_setting_value("PaletteSaveFileDir", [])
        self.configfile_dir = self.load_setting_value("ConfigFileDir", [])

    def does_setting_exist(self, setting_name: str):
        return setting_name in self.DEFAULT_SETTINGS.keys()

    def load_setting_value(self, setting_name: str, valid_values: list[str]):
        if self.does_setting_exist(setting_name):
            # If list is empty it means the value has unlimited options and doesn't have to be checked
            if list == []:
                return self.DEFAULT_SETTINGS.get(setting_name)
            else:
                if self.check_setting_value(setting_name, valid_values)[0]:
                    return self.check_setting_value(setting_name, valid_values)[1]
                else:
                    return self.DEFAULT_SETTINGS.get(setting_name)
        else:
            ...
            # setting not in dictionary / setting doesnt exist / don't load it

    def check_setting_value(self, setting_name: str, valid_values: list[str]) -> tuple[bool, str]:
        return (self.user_settings.get(setting_name).lower() in valid_values, self.user_settings.get(setting_name))

    def create_config_file(self):
        self.config_to_text()
        config_file = None
        try:
            config_file = open(self.configfile_dir, "x")
        except FileExistsError:
            config_file = open(self.configfile_dir, "w")
        finally:
            config_file.write(self.config_to_text())
        config_file.close()
        print("Config file created")

    # Convert user settings to string that can be inserted inside .txt file
    def config_to_text(self) -> str:
        settings: dict = self.user_settings if self.user_settings != None else self.DEFAULT_SETTINGS
        str_settings = ""
        for value in settings.items():
            str_settings += f'"{value[0]}":"{value[1]}"' + "\n"
        return str_settings

    # Reset user preferences to default values
    def reset_config(self):
        self.user_settings = self.DEFAULT_SETTINGS
        self.create_config_file()

    def change_setting(self, setting_name: str, value: str):
        self.user_settings[setting_name] = value
        self.create_config_file()

    def autoload_savefile_toggle(self):
        self.change_setting('AutoLoadSaveFile', "false" if self.user_settings['AutoLoadSaveFile'] in ["true", "True"] else "true")

    # Display palette rename menu
    def show_rename_menu(self):
        Menu = RenameMenu(self.root, self, self.current_palette.name)

    # Set the GUI to stay on top of other programs (or not)
    def stay_on_top(self):
        if self.on_top:
            self.on_top = False
            self.root.attributes('-topmost', False)
            self.StayOnTopButton.config(text="⬜ Unlocked")
        else:
            self.on_top = True
            self.root.attributes('-topmost', True)
            self.StayOnTopButton.config(text="⬛ Locked")

    def change_window_opacity(self, value: str):
        self.root.attributes('-alpha', float(value)/100)
        self.opacity_value.set(f'{float(value):.1f}%')
        self.root.update_idletasks()

    # Check if input is a valid HEX value when user types something in HEX entry widget
    def hex_enter(self, *args):
        if self.manual_entry:
            hex = self.hex_user_entry.get()
            if is_hex_color(hex):
                self.ColorButton.update_color((hex_to_rgb(hex), hex), "history")
        else:
            self.manual_entry = True

    # Check if input is a valid RGB value when user types something in RGB entry widget
    def rgb_enter(self, *args):
        if self.manual_entry:
            print("jhs")
            #rgb = ast.literal_eval(self.rgb_user_entry.get())
            #if is_rgb_color(rgb):
                #self.ColorButton.update_color((rgb, rgb_to_hex(rgb)), "history")
        else:
            self.manual_entry = True

    # Add random color to the history
    def add_random_color(self):
        random_color = random_rgb()
        self.update_color_values(rgb_to_hex(random_color), random_color, "history")


# Stores colors
# Is used both for color history and color palettes
class HistoryMaster():
    def __init__(self, root, window_ref, parent_widget):
        self.window_root = root
        self.window_ref = window_ref
        self.parent_widget = parent_widget

        self.colors = []
        self.color_buttons = []

        self.MainFrame = Frame(self.parent_widget, bg="#212024", pady=3)
        self.MainFrame.grid(row=2, sticky="NS")

        self.List1 = Frame(self.MainFrame, bg="#212024")
        self.List1.grid(row=0, column=0, sticky="NS")
        self.List1.grid_columnconfigure(1, minsize=70)

        self.current_column = 0
        self.current_row = 0


    # --- Functions --- #

    def add_to_history(self, color):
        if color not in self.colors:
            if self.is_history_full():
                self.color_buttons[0].remove_self()
                self.remove_color(0)
                self.reset(False)
            self.colors.append(color)
            new_color = History_ColorButton(self.window_root, self.window_ref, self.List1, self.window_ref.current_palette, color, len(self.color_buttons), self.current_column, self.current_row, False, "")
            self.color_buttons.append(new_color)

            if self.current_column == 0:
                self.current_column = 1
            else:
                self.current_column = 0
                self.current_row += 1

    def is_color_in_history(self, rgb: tuple) -> bool:
        for color in self.colors:
            if color[0] == rgb:
                return True
        return False

    def remove_color(self, index):
        self.colors.pop(index)
        self.color_buttons.pop(index)
        self.update_indexes()

    def update_indexes(self):
        for index, child in enumerate(self.color_buttons):
            child.index = index

    def is_history_full(self):
        return len(self.colors) > 11

    def reset(self, b_palette):
        self.update_indexes()
        self.current_row = 0
        self.current_column = 0
        for child in self.List1.winfo_children():
            child.destroy()
        self.color_buttons = []
        for color in self.colors:
            new_button = History_ColorButton(self.window_root, self.window_ref, self.List1, self.window_ref.current_palette, color, len(self.color_buttons), self.current_column, self.current_row, b_palette, "Name")
            if b_palette:
                new_button.context = "palette"
            self.color_buttons.append(new_button)
            if self.current_column == 0:
                self.current_column = 1
            else:
                self.current_column = 0
                self.current_row += 1

    def clear_history(self):
        self.colors = []
        for elem in self.color_buttons:
            elem.remove_self()
        for child in self.List1.winfo_children():
            child.destroy()
        self.color_buttons = []
        self.current_column = 0
        self.current_row = 0

    def add_to_palette(self, color):
        if color not in self.colors:
            self.colors.append((color[0], color[1], color[2]))
            new_color = History_ColorButton(self.window_root,
                                            self.window_ref,
                                            self.List1,
                                            self.window_ref.current_palette,
                                            (color[0], color[1]),
                                            len(self.color_buttons),
                                            self.current_column,
                                            self.current_row,
                                            True,
                                            color[2])
            new_color.context = "palette"
            self.window_ref.update_context("palette")
            self.color_buttons.append(new_color)

            if self.current_column == 0:
                self.current_column = 1
            elif self.current_column == 1:
                self.current_column = 2
            else:
                self.current_column = 0
                self.current_row += 1

        if color not in self.window_ref.current_palette.colors:
            self.window_ref.current_palette.colors.append((color[0], color[1], "Name"))

    def remove_from_palette(self, color):
        if color in self.colors:
            index = self.colors.index(color)
            self.List1.winfo_children()[index].destroy()
            self.remove_color(index)
            self.window_ref.current_palette.colors.pop(index)
            self.update_indexes()

            self.current_row = 0
            self.current_column = 0

            for child in self.List1.winfo_children():
                child.destroy()
            self.color_buttons = []

            for color in self.colors:
                new_button = History_ColorButton(self.window_root, self.window_ref, self.List1, self.window_ref.current_palette,
                                                 color,
                                                 len(self.color_buttons), self.current_column, self.current_row,
                                                 True, "")
                new_button.context = "palette"
                self.color_buttons.append(new_button)
                if self.current_column == 0:
                    self.current_column = 1
                elif self.current_column == 1:
                    self.current_column = 2
                else:
                    self.current_column = 0
                    self.current_row += 1

            self.set_default("palette")

    def remove_from_history(self, color):
        if (color[0], color[1]) in self.colors:
            index = self.colors.index(color)
            self.List1.winfo_children()[index].destroy()
            self.remove_color(index)
            self.reset(False)
            self.set_default("history")

    def set_default(self, context):
        try:
            self.window_ref.update_color_values(self.colors[0][1], self.colors[0][0], context)
            self.window_ref.picked_color = (self.colors[0][1], self.colors[0][0])
            self.window_ref.ColorButton.ColorButton.config(bg=str(self.colors[0][1]))
            self.window_ref.ColorButton.current_color = (self.colors[0][0], self.colors[0][1])
            self.window_ref.previous_hex = str(self.colors[0][1])
        except:
            self.window_ref.update_color_values("#c72231", "199, 34, 49", context)
            self.window_ref.picked_color = ("#c72231", "199, 34, 49")
            self.window_ref.ColorButton.ColorButton.config(bg="#c72231")
            self.window_ref.ColorButton.current_color = ("#c72231", "199, 34, 49")
            self.window_ref.previous_hex = "#c72231"
            if context != "history":
                self.window_ref.update_context("history")


class ClipboardButton():
    def __init__(self, root, window_ref, parent_widget, color_value):
        self.window_root = root
        self.window_ref = window_ref
        self.parent_widget = parent_widget
        self.color_value = color_value

        self.MainFrame = Frame(self.parent_widget, padx=2, bg="#212024")
        self.MainFrame.grid(row=0, column=2)

        self.ColorButton = Button(self.MainFrame, font=("Arial", 12), text="📑", fg="white", bg="#212024", highlightbackground="black", highlightthickness=2, bd=0, command=self.copy_to_cliboard)
        self.ColorButton.grid(row=0, column=0)


    def copy_to_cliboard(self):
        pyperclip.copy(self.color_value)



class ColorButton():
    def __init__(self, root, window_ref, parent_widget, height, width):
        self.window_root = root
        self.window_ref = window_ref
        self.parent_widget = parent_widget
        self.height = height
        self.width = width
        self.context = "history"

        self.ColorName = StringVar(self.window_root)
        self.ColorName.set("Name")

        self.DEFAULT_COLOR = "#c72231"
        self.current_color = ("199, 34, 49", self.DEFAULT_COLOR)

        self.MainFrame = Frame(self.parent_widget, bg="#212024", pady=5)
        self.MainFrame.grid(sticky="W")

        self.ColorButton = Button(self.MainFrame, height=self.height, width=self.width, bg=self.current_color[1], highlightbackground = "black", highlightthickness = 2, bd=0, command=self.pick_color)
        self.ColorButton.grid(row=0, column=0, sticky="W")


    # Functions

    def pick_color(self):
        self.window_ref.update_context(self.context)
        color = colorchooser.askcolor(title="Pick a color")
        if color != (None, None):
            self.update_color(color, "")
            print(color)
        else:
            print("No color was picked")

    def update_color(self, color, context):
        self.current_color = color
        self.ColorButton.config(bg=color[1])
        self.window_ref.update_color_values(hex_value=self.current_color[1], rgb_value=self.current_color[0], context=context)



# Saved palette
class Palette:
    def __init__(self, name: str, colors):
        self.name = name
        self.colors = colors



class History_ColorButton():
    def __init__(self,
                 root: Tk,
                 window_ref: MainWindow,
                 parent_widget,
                 palette_ref: Palette,
                 color: (str, str),
                 index: int,
                 column: int,
                 row: int,
                 b_palette: bool,
                 color_name: str):

        self.window_root = root
        self.window_ref = window_ref
        self.parent_widget = parent_widget
        self.palette_ref = palette_ref
        self.index = index
        self.column = column
        self.row = row
        self.b_palette = b_palette
        self.context = "palette"

        self.color = color
        self.ColorName = StringVar(self.window_root)

        self.MainFrame = Frame(self.parent_widget, bg="#212024", pady=5, padx=2)
        self.MainFrame.grid(row=row, column=column)

        self.ColorButton = Button(self.MainFrame, height=1, width=8, bg=self.color[1], highlightbackground = "black", highlightthickness = 2, bd=0, command=self.change_main_color)
        self.ColorButton.grid(row=0, column=0)

        self.HEXEntry = Entry(self.MainFrame, bg="#212024", fg="#aba7a7", width=10, highlightthickness=0)
        self.HEXEntry.configure(highlightbackground="#212024", highlightcolor="#212024")
        self.HEXEntry.insert(END, self.color[1])
        self.HEXEntry.grid(row=1, column=0)

        if b_palette:
            self.NameEntry = Entry(self.MainFrame, textvariable=self.ColorName, bg="#212024", fg="#aba7a7", width=10,
                                   highlightthickness=0)
            self.NameEntry.configure(highlightbackground="#212024", highlightcolor="#212024")
            self.NameEntry.grid(row=0, column=0)

            self.ColorButton.grid(row=1)
            self.HEXEntry.grid(row=2)

            self.ColorName.set(color_name or  self.palette_ref.colors[self.index][2])

            self.ColorName.trace_add('write', self.save_color_name)



    # Functions
    def change_main_color(self):
        self.window_ref.ColorButton.update_color((self.color[0], self.color[1], self.ColorName.get()),
                                                 "palette" if self.b_palette else "history")

    def remove_self(self):
        self.MainFrame.destroy()
        del self

    def save_color_name(self, *args):
        color_info = self.palette_ref.colors[self.index]
        self.palette_ref.colors[self.index] = (color_info[0], color_info[1], self.ColorName.get())



# Rename Palette Widget
class RenameMenu:
    def __init__(self, root, window_ref, name):
        self.window_root = root
        self.window_ref = window_ref
        self.name = name

        # Create widgets
        self.root = Tk()
        self.root.geometry("250x125")
        self.root.resizable(height=False, width=False)
        self.root.title("Rename Palette")
        self.root.config(bg="#212024")

        self.entry_input = StringVar(self.root)
        self.entry_input.set(self.name)

        self.MainFrame = Frame(self.root, padx=15, bg="#212024")
        self.MainFrame.pack(fill=BOTH, expand=1)

        self.RenameLabel = Label(self.MainFrame, text="Rename Palette:", pady=7, font=("Lato", 11), bg="#212024", fg="white")
        self.RenameLabel.pack(fill=BOTH)

        self.RenameEntry = Entry(self.MainFrame, width=30, font=("Lato", 12), textvariable=self.entry_input)
        self.RenameEntry.pack()

        self.ButtonFrame = Frame(self.root, bg="#212024", pady=5)
        self.ButtonFrame.pack()

        self.ErrorLabel = Label(self.MainFrame, text="", pady=7, font=("Lato", 9), bg="#212024", fg="red")
        self.ErrorLabel.pack()

        self.ConfirmButtom = Button(self.ButtonFrame, bg="#212024", font=("Lato", 11), text="Confirm", fg="white", command=self.rename_palette)
        self.ConfirmButtom.pack()


    # Functions

    def rename_palette(self):
        if self.entry_input.get() in self.window_ref.get_palettes() and self.entry_input.get() != self.window_ref.current_palette.name:
            self.ErrorLabel.config(text="Palette with this name already exists")
        else:
            self.ErrorLabel.config(text="")
            self.window_ref.current_palette.name = self.entry_input.get()
            self.window_ref.PaletteMenu.config(values=self.window_ref.get_palettes())
            self.window_ref.selected_palette.set(self.window_ref.current_palette.name)

            self.root.destroy()
            del self