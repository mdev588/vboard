import gi
import uinput
import time
import os
import configparser

os.environ['GDK_BACKEND'] = 'x11'

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk


key_mapping = {uinput.KEY_ESC: "Esc", uinput.KEY_1: "1", uinput.KEY_2: "2", uinput.KEY_3: "3", uinput.KEY_4: "4", uinput.KEY_5: "5", uinput.KEY_6: "6",
    uinput.KEY_7: "7", uinput.KEY_8: "8", uinput.KEY_9: "9", uinput.KEY_0: "0", uinput.KEY_MINUS: "-", uinput.KEY_EQUAL: "=",
    uinput.KEY_BACKSPACE: "Backspace", uinput.KEY_TAB: "Tab", uinput.KEY_Q: "Q", uinput.KEY_W: "W", uinput.KEY_E: "E", uinput.KEY_R: "R",
    uinput.KEY_T: "T", uinput.KEY_Y: "Y", uinput.KEY_U: "U", uinput.KEY_I: "I", uinput.KEY_O: "O", uinput.KEY_P: "P",
    uinput.KEY_LEFTBRACE: "[", uinput.KEY_RIGHTBRACE: "]", uinput.KEY_ENTER: "Enter", uinput.KEY_LEFTCTRL: "Ctrl_L", uinput.KEY_A: "A",
    uinput.KEY_S: "S", uinput.KEY_D: "D", uinput.KEY_F: "F", uinput.KEY_G: "G", uinput.KEY_H: "H", uinput.KEY_J: "J", uinput.KEY_K: "K",
    uinput.KEY_L: "L", uinput.KEY_SEMICOLON: ";", uinput.KEY_APOSTROPHE: "'", uinput.KEY_GRAVE: "`", uinput.KEY_LEFTSHIFT: "Shift_L",
    uinput.KEY_BACKSLASH: "\\", uinput.KEY_Z: "Z", uinput.KEY_X: "X", uinput.KEY_C: "C", uinput.KEY_V: "V", uinput.KEY_B: "B",
    uinput.KEY_N: "N", uinput.KEY_M: "M", uinput.KEY_COMMA: ",", uinput.KEY_DOT: ".", uinput.KEY_SLASH: "/", uinput.KEY_RIGHTSHIFT: "Shift_R",
    uinput.KEY_KPENTER: "Enter", uinput.KEY_LEFTALT: "Alt_L", uinput.KEY_RIGHTALT: "Alt_R", uinput.KEY_SPACE: "Space", uinput.KEY_CAPSLOCK: "CapsLock",
    uinput.KEY_F1: "F1", uinput.KEY_F2: "F2", uinput.KEY_F3: "F3", uinput.KEY_F4: "F4", uinput.KEY_F5: "F5", uinput.KEY_F6: "F6",
    uinput.KEY_F7: "F7", uinput.KEY_F8: "F8", uinput.KEY_F9: "F9", uinput.KEY_F10: "F10", uinput.KEY_F11: "F11", uinput.KEY_F12: "F12",
    uinput.KEY_SCROLLLOCK: "ScrollLock", uinput.KEY_PAUSE: "Pause", uinput.KEY_INSERT: "Insert", uinput.KEY_HOME: "Home",
    uinput.KEY_PAGEUP: "PageUp", uinput.KEY_DELETE: "Delete", uinput.KEY_END: "End", uinput.KEY_PAGEDOWN: "PageDown",
    uinput.KEY_RIGHT: "→", uinput.KEY_LEFT: "←", uinput.KEY_DOWN: "↓", uinput.KEY_UP: "↑", uinput.KEY_NUMLOCK: "NumLock",
    uinput.KEY_RIGHTCTRL: "Ctrl_R", uinput.KEY_LEFTMETA:"Super_L", uinput.KEY_RIGHTMETA:"Super_R"}

class VirtualKeyboard(Gtk.Window):
    def __init__(self):
        super().__init__(title="Virtual Keyboard", name="toplevel")

        self.set_border_width(0)
        self.set_resizable(True)
        self.set_keep_above(True)
        self.set_modal(False)
        self.set_focus_on_map(False)
        self.set_can_focus(False)
        self.set_accept_focus(False)
        # Geometry state variables, initialized to indicate unset
        self.x_landscape, self.y_landscape = -1, -1
        self.width_landscape, self.height_landscape = -1, -1
        self.x_portrait, self.y_portrait = -1, -1
        self.width_portrait, self.height_portrait = -1, -1

        # Connect to the window's realize signal
        self.connect("realize", self.on_realize)
        # Connect configure-event for position/size changes
        self.connect("configure-event", self.on_configure)

        # Connect to screen change signals to handle rotation and monitor config changes
        screen = Gdk.Screen.get_default()
        screen.connect("size-changed", self.on_screen_changed)
        screen.connect("monitors-changed", self.on_screen_changed)

        self.CONFIG_DIR = os.path.expanduser("~/.config/vboard")
        self.CONFIG_FILE = os.path.join(self.CONFIG_DIR, "settings.conf")
        self.config = configparser.ConfigParser()

        self.bg_color = "0, 0, 0"  # background color
        self.opacity="0.90"
        self.text_color="white"
        self.read_settings()

        self.modifiers = {
            uinput.KEY_LEFTSHIFT: False,
            uinput.KEY_RIGHTSHIFT: False,
            uinput.KEY_LEFTCTRL: False,
            uinput.KEY_RIGHTCTRL: False,
            uinput.KEY_LEFTALT: False,
            uinput.KEY_RIGHTALT: False,
            uinput.KEY_LEFTMETA: False,
            uinput.KEY_RIGHTMETA: False
        }
        self.colors = [
            ("Black", "0,0,0"),
            ("Red", "255,0,0"),
            ("Pink", "255,105,183"),
            ("White", "255,255,255"),
            ("Green", "0,255,0"),
            ("Blue", "0,0,110"),
            ("Gray", "128,128,128"),
            ("Dark Gray", "64,64,64"),
            ("Orange", "255,165,0"),
            ("Yellow", "255,255,0"),
            ("Purple", "128,0,128"),
            ("Cyan", "0,255,255"),
            ("Teal", "0,128,128"),
            ("Brown", "139,69,19"),
            ("Gold", "255,215,0"),
            ("Silver", "192,192,192"),
            ("Turquoise", "64,224,208"),
            ("Magenta", "255,0,255"),
            ("Olive", "128,128,0"),
            ("Maroon", "128,0,0"),
            ("Indigo", "75,0,130"),
            ("Beige", "245,245,220"),
            ("Lavender", "230,230,250")

        ]

        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.buttons=[]
        self.row_buttons=[]
        self.color_combobox = Gtk.ComboBoxText()
        # Set the header bar as the titlebar of the window
        self.set_titlebar(self.header)
        self.create_settings()

        grid = Gtk.Grid()  # Use Grid for layout
        grid.set_row_homogeneous(True)  # Allow rows to resize based on content
        grid.set_column_homogeneous(True)  # Columns are homogeneous
        grid.set_margin_start(3)
        grid.set_margin_end(3)
        grid.set_name("grid")
        self.add(grid)
        self.apply_css()
        self.device = uinput.Device(list(key_mapping.keys()))

        # Define rows for keys
        rows = [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace" ],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
            ["Shift_L", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift_R", "↑"],
            ["Ctrl_L","Super_L", "Alt_L", "Space", "Alt_R", "Super_R", "Ctrl_R", "←", "→", "↓"]
        ]

        # Create each row and add it to the grid
        for row_index, keys in enumerate(rows):
            self.create_row(grid, row_index, keys)


    def create_settings(self):
        self.create_button("☰", self.change_visibility,callbacks=1)
        self.create_button("+", self.change_opacity,True,2)
        self.create_button("-", self.change_opacity, False,2)
        self.create_button( f"{self.opacity}")
        self.color_combobox.append_text("Change Background")
        self.color_combobox.set_active(0)
        self.color_combobox.connect("changed", self.change_color)
        self.color_combobox.set_name("combobox")
        self.header.add(self.color_combobox)


        for label, color in self.colors:
            self.color_combobox.append_text(label)

    def on_screen_changed(self, *args):
        # Apply geometry for the potentially new orientation/resolution
        self.apply_geometry()
        return False

    def get_current_orientation(self):
        """Determines the orientation of the primary monitor."""
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        if not monitor:
            # Fallback to screen size if primary monitor not found
            screen = Gdk.Screen.get_default()
            width, height = screen.get_width(), screen.get_height()
        else:
            geo = monitor.get_geometry()
            width, height = geo.width, geo.height

        return "landscape" if width >= height else "portrait"

    def apply_geometry(self):
        """Applies the saved or default geometry based on current orientation."""
        self.orientation = self.get_current_orientation()

        changed = False
        width, height = self.get_saved_size()
        if width < 0 or height < 0:
            width, height = self.get_size()
            self.update_size(width, height)
            changed = True
        
        x, y = self.get_saved_position()

        # Use default position (centered) if not set or invalid
        if x < 0 or y < 0:
            display = Gdk.Display.get_default()
            monitor = display.get_primary_monitor()
            if monitor:
                geo = monitor.get_geometry()
                mon_x, mon_y = geo.x, geo.y
                mon_width, mon_height = geo.width, geo.height
            else:
                screen = Gdk.Screen.get_default()
                mon_x, mon_y = 0, 0
                mon_width, mon_height = screen.get_width(), screen.get_height()

            x = mon_x + (mon_width - width) // 2
            y = mon_y + (mon_height - height) // 2 # Center vertically as well
            
            self.update_position(x, y)
            changed = True

        current_width, current_height = self.get_size()
        if width != current_width or height != current_height:
            self.resize(width, height)

        current_x, current_y = self.get_position()
        if x != current_x or y != current_y:
            # Move the window to the new position
            self.move(x, y)

        if changed:
            self.save_settings()

    def on_realize(self, widget):
        # Apply initial geometry once the window is realized
        self.apply_geometry()
        return False

    def on_configure(self, widget, event):
        """Handles window move and resize events."""
        # In debugging, I found that the configure event is triggered right before
        # the screen change event, with a weird position.
        # So we need to delay the update to avoid false triggers.
        GLib.timeout_add(100, self.update_geometry)
        return False

    def update_geometry(self):
        self.orientation = self.get_current_orientation()

        # Gdk.EventConfigure contains the window's position relative to its parent (screen)
        # and its allocated size.
        current_x, current_y = self.get_position() # Use get_position for screen coordinates
        current_width, current_height = self.get_size() # Use get_size for actual dimensions

        saved_x, saved_y = self.get_saved_position()
        saved_width, saved_height = self.get_saved_size()

        changed = False
        if current_x != saved_x or current_y != saved_y:
            self.update_position(current_x, current_y)
            changed = True
        
        if current_width != saved_width or current_height != saved_height:
            self.update_size(current_width, current_height)
            changed = True

        # Save settings whenever the window is moved or resized
        if changed:
            self.save_settings()
    
    def update_position(self, x, y):
        if self.orientation == "landscape":
            self.x_landscape, self.y_landscape = x, y
        else: # portrait
            self.x_portrait, self.y_portrait = x, y
    
    def update_size(self, width, height):
        if self.orientation == "landscape":
            self.width_landscape, self.height_landscape = width, height
        else:
            self.width_portrait, self.height_portrait = width, height

    def get_saved_position(self):
        if self.orientation == "landscape":
            return self.x_landscape, self.y_landscape
        else:
            return self.x_portrait, self.y_portrait

    def get_saved_size(self):
        if self.orientation == "landscape":
            return self.width_landscape, self.height_landscape
        else:
            return self.width_portrait, self.height_portrait
    
    def create_button(self, label_="", callback=None, callback2=None, callbacks=0):
        button= Gtk.Button(label=label_)
        button.set_name("headbar-button")
        if callbacks==1:
            button.connect("clicked", callback)
        elif callbacks==2:
            button.connect("clicked", callback, callback2)

        if label_==self.opacity:
            self.opacity_btn=button
            self.opacity_btn.set_tooltip_text("opacity")

        self.header.add(button)
        self.buttons.append(button)

    def change_visibility(self, widget=None):
        for button in self.buttons:
            if button.get_label()!="☰":
                button.set_visible(not button.get_visible())
        self.color_combobox.set_visible(not self.color_combobox.get_visible() )

    def change_color (self, widget):
        label=self.color_combobox.get_active_text()
        for label_ , color_ in self.colors:
            if label_==label:
                self.bg_color = color_

        if (self.bg_color in {"255,255,255" ,"0,255,0" , "255,255,0", "245,245,220", "230,230,250", "255,215,0"}):
            self.text_color="#1C1C1C"
        else:
            self.text_color="white"
        self.apply_css()


    def change_opacity(self,widget, boolean):
        if (boolean):
            self.opacity = str(round(min(1.0, float(self.opacity) + 0.01),2))
        else:
            self.opacity = str(round(max(0.0, float(self.opacity) - 0.01),2))
        self.opacity_btn.set_label(f"{self.opacity}")
        self.apply_css()
    def apply_css (self):
        provider = Gtk.CssProvider()


        css = f"""
        headerbar {{
            background-color: rgba({self.bg_color}, {self.opacity});
            border: 0px;

        }}

        headerbar button{{
            min-width: 40px;
            padding: 0px;
            border: 0px;
            


        }}

        headerbar button label{{
        color: {self.text_color};

        }}

        #headbar-button, #combobox button.combo {{
            background-image: none;
        }}

        #toplevel {{
            background-color: rgba({self.bg_color}, {self.opacity});




        }}

        #grid button label{{
            color: {self.text_color};


        }}

        #grid button {{
                    border: 1px solid rgba(85, 85, 85, 0.7) ;
                    background-image: none;

                }}

        button {{
            background-color: transparent;
            color:{self.text_color};

        }}

       #grid button:hover {{
            border: 1px solid #00CACB;
        }}

       tooltip {{
            color: white;
            padding: 5px;
        }}

       #combobox button.combo  {{

            color: {self.text_color};
            padding: 5px;
        }}


        """

        try:
            provider.load_from_data(css.encode("utf-8"))
        except GLib.GError as e:
            print(f"CSS Error: {e.message}")
        Gtk.StyleContext.add_provider_for_screen(self.get_screen(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def create_row(self, grid, row_index, keys):
        col = 0  # Start from the first column
        width=0


        for key_label in keys:
            key_event = next((key for key, label in key_mapping.items() if label == key_label), None)
            if key_event:
                if key_label in ("Shift_R", "Shift_L", "Alt_L", "Alt_R", "Ctrl_L", "Ctrl_R", "Super_L", "Super_R"):
                    button = Gtk.Button(label=key_label[:-2])
                else:
                    button = Gtk.Button(label=key_label)
                button.connect("clicked", self.on_button_click, key_event)
                self.row_buttons.append(button)
                if key_label == "Space": width=12
                elif key_label == "CapsLock": width=3
                elif key_label == "Shift_R" : width=4
                elif key_label == "Shift_L" : width=4
                elif key_label == "Backspace": width=5
                elif key_label == "`": width=1
                elif key_label == "\\" : width=4
                elif key_label == "Enter": width=5
                else: width=2

                grid.attach(button, col, row_index, width, 1)
                col += width  # Skip 4 columns for the space button

    def update_label(self, show_symbols):
        button_positions = [(0, "` ~"), (1, "1 !"), (2, "2 @"), (3, "3 #"), (4, "4 $"), (5, "5 %"), (6, "6 ^"), (7, "7 &"), (8, "8 *"), (9, "9 ("), (10, "0 )")
        , (11, "- _"), (12, "= +"),(25,"[ {"), (26,"] }"), (27,"\\ |"), (38, "; :"), (39, "' \""), (49, ", <"), (50, ". >"), (51, "/ ?")]

        for pos, label in button_positions:
            label_parts = label.split()  
            if show_symbols:
                self.row_buttons[pos].set_label(label_parts[1])
            else:
                self.row_buttons[pos].set_label(label_parts[0])


    def on_button_click(self, widget, key_event):
        # If the key event is one of the modifiers, update its state and return.
        if key_event in self.modifiers:
            self.modifiers[key_event] = not self.modifiers[key_event]
            if(self.modifiers[uinput.KEY_LEFTSHIFT]==True and self.modifiers[uinput.KEY_RIGHTSHIFT]==True):
                self.modifiers[uinput.KEY_LEFTSHIFT]=False
                self.modifiers[uinput.KEY_RIGHTSHIFT]=False
            if(self.modifiers[uinput.KEY_LEFTSHIFT]==True or self.modifiers[uinput.KEY_RIGHTSHIFT]==True):
                self.update_label(True)
            else:
                self.update_label(False)
            return
        # For a normal key, press any active modifiers.
        for mod_key, active in self.modifiers.items():
            if active:
                self.device.emit(mod_key, 1)

        # Emit the normal key press.
        self.device.emit(key_event, 1)
        #time.sleep(0.05)
        self.device.emit(key_event, 0)
        self.update_label(False)
        # Release the modifiers that were active.
        for mod_key, active in self.modifiers.items():
            if active:
                self.device.emit(mod_key, 0)
                self.modifiers[mod_key] = False


    def read_settings(self):
        # Ensure the config directory exists
        try:
            os.makedirs(self.CONFIG_DIR, exist_ok=True)
        except PermissionError:
            print("Warning: No permission to create the config directory. Proceeding without it.")

        try:
            if os.path.exists(self.CONFIG_FILE):
                self.config.read(self.CONFIG_FILE)
                # Read general settings
                self.bg_color = self.config.get("DEFAULT", "bg_color")
                self.opacity = self.config.get("DEFAULT", "opacity")
                self.text_color = self.config.get("DEFAULT", "text_color", fallback="white")

                # Read landscape geometry (use old width/height as fallback for compatibility)
                old_width = self.config.getint("DEFAULT", "width", fallback=-1)
                old_height = self.config.getint("DEFAULT", "height", fallback=-1)
                self.x_landscape = self.config.getint("DEFAULT", "x_landscape", fallback=-1)
                self.y_landscape = self.config.getint("DEFAULT", "y_landscape", fallback=-1)
                self.width_landscape = self.config.getint("DEFAULT", "width_landscape", fallback=old_width)
                self.height_landscape = self.config.getint("DEFAULT", "height_landscape", fallback=old_height)

                # Read portrait geometry
                self.x_portrait = self.config.getint("DEFAULT", "x_portrait", fallback=-1)
                self.y_portrait = self.config.getint("DEFAULT", "y_portrait", fallback=-1)
                self.width_portrait = self.config.getint("DEFAULT", "width_portrait", fallback=-1)
                self.height_portrait = self.config.getint("DEFAULT", "height_portrait", fallback=-1)
        except (configparser.Error, ValueError) as e:
            print(f"Warning: Could not read config file or value ({e}). Using default values.")
            # Reset geometry if reading fails to ensure defaults are used
            self.x_landscape, self.y_landscape = -1, -1
            self.width_landscape, self.height_landscape = -1, -1
            self.x_portrait, self.y_portrait = -1, -1
            self.width_portrait, self.height_portrait = -1, -1


    def save_settings(self):
        # Save settings including orientation-specific geometry
        self.config["DEFAULT"] = {
            "bg_color": self.bg_color,
            "opacity": self.opacity,
            "text_color": self.text_color,
            # Landscape
            "x_landscape": str(self.x_landscape),
            "y_landscape": str(self.y_landscape),
            "width": str(self.width_landscape),
            "height": str(self.height_landscape),
            # Portrait
            "x_portrait": str(self.x_portrait),
            "y_portrait": str(self.y_portrait),
            "width_portrait": str(self.width_portrait),
            "height_portrait": str(self.height_portrait)
        }

        try:
            with open(self.CONFIG_FILE, "w") as configfile:
                self.config.write(configfile)

        except (configparser.Error, IOError) as e:
            print(f"Warning: Could not write to config file ({e}). Changes will not be saved.")


if __name__ == "__main__":
    win = VirtualKeyboard()
    win.connect("destroy", Gtk.main_quit)
    win.connect("destroy", lambda w: win.save_settings())
    win.show_all()
    win.change_visibility()
    Gtk.main()
