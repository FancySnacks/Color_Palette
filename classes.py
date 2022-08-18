from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import pyperclip


class MainWindow:
    def __init__(self):
        # GUI creation
        self.root = Tk()
        self.root.geometry("650x425")
        self.root.resizable(height=False, width=False)
        self.root.title("Color Palette")
        self.root.config(bg="#212024")

        # Variables
        self.ColorButton = None
        self.picked_color = None
        self.context = ""

        # Palettes
        self.saved_palettes = ["Temporary Palette"]
        self.palettes = self.saved_palettes
        self.selected_palette = StringVar(self.root)
        self.selected_palette.set(self.saved_palettes[0])

        # Main Container
        self.MainFrame = Frame(self.root, padx=5, pady=5, bg="#212024")
        self.MainFrame.grid(row=0, column=0)

        # Color Picker Frame
        self.ColorFrame = Frame(self.MainFrame, bg="#212024")
        self.ColorFrame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="NW")

        self.ColorLabel = Label(self.ColorFrame, font=("Lato", 12), bg="#212024", text="🌈  Color Picker", fg="white", pady=5)
        self.ColorLabel.grid(row=0, column=0, sticky="NW")

        color_button = ColorButton(self.root, self, self.ColorFrame, 10, 25)
        self.ColorButton = color_button

            # Color values
            # HEX
        self.HexFrame = Frame(self.ColorFrame, bg="#212024")
        self.HexFrame.grid(row=3, column=0, sticky="NW")

        self.HexLabel = Label(self.HexFrame, text="Hex Code :", font=("Lato", 11, "bold"), bg="#212024", fg="#aba7a7", pady=5)
        self.HexLabel.grid(row=0, column=0, sticky="NW")

        self.HexEntryFrame = Frame(self.HexFrame)
        self.HexEntryFrame.grid(row=0, column=1)

        self.HexEntry = Entry(self.HexEntryFrame, font=("Arial", 11), width=10, bg="#212024", fg="white")
        self.HexEntry.insert(END, color_button.current_color[1])
        self.HexEntry.grid(row=0, column=0, sticky="NW")

        self.HexCopyButton = ClipboardButton(self.root, MainWindow, self.HexFrame, color_button.current_color[1])

            # RGB
        self.RGBFrame = Frame(self.ColorFrame, bg="#212024")
        self.RGBFrame.grid(row=4, column=0, sticky="NW")

        self.RGBLabel = Label(self.RGBFrame, text="RGB Code :", font=("lato", 11, "bold"), bg="#212024", fg="#aba7a7", pady=5)
        self.RGBLabel.grid(row=0, column=0, sticky="NW")

        self.RGBEntryFrame = Frame(self.RGBFrame)
        self.RGBEntryFrame.grid(row=0, column=1)

        self.RGBEntry = Entry(self.RGBEntryFrame, font=("Arial", 11), width=10, bg="#212024", fg="white")
        self.RGBEntry.insert(END, color_button.current_color[0])
        self.RGBEntry.grid(row=0, column=0, sticky="NW")

        self.RGBCopyButton = ClipboardButton(self.root, MainWindow, self.RGBFrame, color_button.current_color[0])

        # Color History Frame
        self.HistoryFrame = Frame(self.MainFrame, bg="#212024", padx=15)
        self.HistoryFrame.grid(row=0, column=2, rowspan=2, columnspan=2, sticky="NE")

        self.HistoryLabel = Label(self.HistoryFrame, font=("Lato", 12), bg="#212024", text="⌛  History", fg="white", pady=5)
        self.HistoryLabel.grid(row=0, column=0, sticky="NW")

        self.HistoryMaster = HistoryMaster(self.root, self, self.HistoryFrame)
        self.HistoryMaster.add_to_history(self.ColorButton.current_color)

        # Clear History Button
        self.ClearButtonFrame = Frame(self.HistoryFrame, bg="#212024")
        self.ClearButtonFrame.grid(row=1, column=0, sticky="NW")
        self.ClearButton = Button(self.ClearButtonFrame, font=("Arial", 10), text="❌ Clear", fg="white", bg="#212024", command=self.HistoryMaster.clear_history)
        self.ClearButton.grid(row=0, column=0, sticky="NW")

        # Palette List Frame
        self.PaletteFrame = Frame(self.MainFrame, bg="#212024", padx=10)
        self.PaletteFrame.grid(row=0, column=4, rowspan=2, columnspan=2, sticky="NE")

        self.PaletteLabel = Label(self.PaletteFrame, font=("Lato", 12), bg="#212024", text="🎨  Palettes", fg="white", pady=5)
        self.PaletteLabel.grid(row=0, column=0, sticky="NW")

        self.PaletteMaster = HistoryMaster(self.root, self, self.PaletteFrame)

        # Palette Dropdown Box
        self.PaletteMenuFrame = Frame(self.PaletteFrame, bg="#212024")
        self.PaletteMenuFrame.grid(row=1, column=0, columnspan=3)

        self.PaletteMenu = ttk.Combobox(self.PaletteMenuFrame, values=self.palettes, width=20)
        self.PaletteMenu.set(self.palettes[0])
        self.PaletteMenu.config(textvariable=self.selected_palette)
        self.PaletteMenu.grid(row=0, column=0, columnspan=2)

        self.PaletteMenu.bind("<<ComboboxSelected>>", self.on_palette_changed)

        # Palette Create Button
        self.PaletteAddFrame = Frame(self.PaletteMenuFrame, bg="#212024", padx=4, pady=3)
        self.PaletteAddFrame.grid(row=0, column=2, sticky="NW")

        self.PaletteAddButton = Button(self.PaletteAddFrame, font=("Lato", 10), text="➕", fg="white", bg="#212024",
                                     command=self.add_palette)
        self.PaletteAddButton.grid(row=0, column=0, sticky="NW")

        # Palette Delete Button
        self.PaletteDelFrame = Frame(self.PaletteMenuFrame, bg="#212024", padx=2, pady=3)
        self.PaletteDelFrame.grid(row=0, column=3, sticky="NW")

        self.PaletteDelButton = Button(self.PaletteDelFrame, font=("Lato", 10), text="❌", fg="white", bg="#212024",
                                       command=self.delete_palette)
        self.PaletteDelButton.grid(row=0, column=0, sticky="NW")

        # Palette Save Button
        self.PaletteSaveFrame = Frame(self.PaletteMenuFrame, bg="#212024", padx=2, pady=3)
        self.PaletteSaveFrame.grid(row=0, column=4, sticky="NW")

        self.PaletteSaveButton = Button(self.PaletteSaveFrame, font=("Lato", 10), text="Save", fg="white", bg="#212024",
                                       command=self.save_palette)
        self.PaletteSaveButton.grid(row=0, column=0, sticky="NW")

        # Add color to palette button
        self.AddColorFrame = Frame(self.ColorFrame, bg="#212024", padx=8, pady=3)
        self.AddColorFrame.grid(row=2, column=0, sticky="NW")
        self.AddColorButton = Button(self.AddColorFrame, font=("Arial", 10), text="➕ Add ", fg="white", bg="#212024", command=self.add_color_to_palette)
        self.AddColorButton.grid(row=0, column=0, sticky="NW")

        self.DelColorButton = Button(self.AddColorFrame, font=("Arial", 10), text="❌ Remove (🎨)", fg="white",
                                     bg="#212024", command=self.remove_color)
        self.DelColorButton.grid(row=0, column=1, sticky="NW")


        # Display main window
        self.root.mainloop()


    # Functions

    def update_color_values(self, hex_value, rgb_value, context):
        self.update_context(context)

        # HEX
        self.HexEntry.delete(0, END)
        self.HexEntry.insert(END, hex_value)

        # RGB
        f_rgb_value = ' '.join(str(rgb_value).split()).replace("(", "").replace(")", "")
        self.RGBEntry.delete(0, END)
        self.RGBEntry.insert(END, f_rgb_value)

        # Clipboard buttons
        self.HexCopyButton.color_value = hex_value
        self.RGBCopyButton.color_value = f_rgb_value

        # Add color button to the history
        self.HistoryMaster.add_to_history((rgb_value, hex_value))

    def update_context(self, context):
        self.context = context
        if context == "palette":
            self.DelColorButton.config(text="❌ Remove (🎨)")
        else:
            self.DelColorButton.config(text="❌ Remove (⌛)")

    def add_color_to_palette(self):
        self.PaletteMaster.add_to_palette(self.ColorButton.current_color)

    def remove_color(self):
        if self.context == "palette":
            self.PaletteMaster.remove_from_palette(self.ColorButton.current_color)
        else:
            self.HistoryMaster.remove_from_palette(self.ColorButton.current_color)


    def on_palette_changed(self, event):
        print(self.selected_palette.get())

    def add_palette(self):
        self.palettes.append("New Palette")
        self.PaletteMenu.config(values=self.palettes)
        self.selected_palette.set(self.palettes[-1])

    def delete_palette(self):
        if self.selected_palette.get() != "Temporary Palette":
            index = self.palettes.index(self.selected_palette.get())
            self.palettes.remove(self.selected_palette.get())
            self.selected_palette.set(self.saved_palettes[0] if self.saved_palettes[index-1] == None else self.saved_palettes[index-1])
            self.PaletteMenu.config(values=self.palettes)

    def save_palette(self):
        pass



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

        self.current_column = 0
        self.current_row = 0


    # Functions

    def add_to_history(self, color):
        if color not in self.colors:
            if self.is_history_full():
                self.color_buttons[0].remove_self()
                self.remove_color(0)
                self.reset()
            self.colors.append(color)
            new_color = History_ColorButton(self.window_root, self.window_ref, self.List1, color, len(self.color_buttons), self.current_column, self.current_row, False)
            self.color_buttons.append(new_color)

            if self.current_column == 0:
                self.current_column = 1
            else:
                self.current_column = 0
                self.current_row += 1

    def remove_color(self, index):
        self.colors.pop(index)
        self.color_buttons.pop(index)
        self.update_indexes()

    def update_indexes(self):
        for index, child in enumerate(self.color_buttons):
            child.index = index

    def is_history_full(self):
        return len(self.colors) > 11

    def reset(self):
        self.update_indexes()
        self.current_row = 0
        self.current_column = 0
        for elem in self.color_buttons:
            elem.remove_self()
        self.color_buttons = []
        for color in self.colors:
            self.color_buttons.append(History_ColorButton(self.window_root, self.window_ref, self.List1, color, len(self.color_buttons), self.current_column, self.current_row, False))
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
            self.colors.append(color)
            new_color = History_ColorButton(self.window_root, self.window_ref, self.List1, color, len(self.color_buttons), self.current_column, self.current_row, True)
            self.color_buttons.append(new_color)

            if self.current_column == 0:
                self.current_column = 1
            elif self.current_column == 1:
                self.current_column = 2
            else:
                self.current_column = 0
                self.current_row += 1

    def remove_from_palette(self, color):
        if color in self.colors:
            index = self.colors.index(color)
            self.List1.winfo_children()[index].destroy()
            self.remove_color(index)

            if self.current_column == 0:
                self.current_column = 1
            elif self.current_column == 1:
                self.current_column = 2
            else:
                self.current_column = 0
                self.current_row += 1




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

        self.DEFAULT_COLOR = "#c72231"
        self.current_color = ("199, 34, 49", self.DEFAULT_COLOR)

        self.MainFrame = Frame(self.parent_widget, bg="#212024", pady=5)
        self.MainFrame.grid()

        self.ColorButton = Button(self.MainFrame, height=self.height, width=self.width, bg=self.current_color[1], highlightbackground = "black", highlightthickness = 2, bd=0, command=self.pick_color)
        self.ColorButton.grid(row=0, column=0)


    # Functions

    def pick_color(self):
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



class History_ColorButton():
    def __init__(self, root, window_ref, parent_widget, color, index, column, row, b_palette):
        self.window_root = root
        self.window_ref = window_ref
        self.parent_widget = parent_widget
        self.index = index
        self.column = column
        self.row = row
        self.b_palette = b_palette

        self.color = color
        self.ColorName = StringVar(self.window_root)
        self.ColorName.set("Name")

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


    # Functions

    def change_main_color(self):
        self.window_ref.ColorButton.update_color(self.color, "palette" if self.b_palette else "history")

    def remove_self(self):
        self.MainFrame.destroy()
        del self



# Saved palette
class Palette:
    def __init__(self, name: str, colors):
        self.name = name
        self.colors = colors