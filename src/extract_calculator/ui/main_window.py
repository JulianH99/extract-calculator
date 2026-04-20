# TODO: build list based on this comment
# https://github.com/Taiko2k/GTK4PythonTutorial?tab=readme-ov-file#using-gridview
from typing import final
import gi

from ..reader.parser import Record
from ..ui.table import Table

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  # pyright: ignore[reportAttributeAccessIssue]


@final
class MainApp(Adw.Application):
    def __init__(self, window: Gtk.ApplicationWindow = None):
        super().__init__(application_id="com.example.ExtractCalculator")
        self.window = window
        self.connect("activate", self.on_activate)

    def on_activate(self, app: Adw.Application):
        app.add_window(self.window)
        self.window.present()
        self.assign_theme()

    def assign_theme(self):
        # theme
        sm = self.get_style_manager()
        sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)


@final
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, records: list[Record]):
        super().__init__(title="Extract Calculator")
        self.set_default_size(1200, 600)

        # Add a simple label

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.open_button = Gtk.Button(label="Seleccionar PDF")
        self.open_button.set_icon_name("document-open-symbolic")

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.header.set_show_title_buttons(False)
        self.header.pack_start(self.open_button)

        # table
        self.scrollable = Gtk.ScrolledWindow()
        self.table = Table(records)

        self.scrollable.set_child(self.table.build())
        self.scrollable.set_propagate_natural_height(True)
        self.box.append(self.scrollable)
        self.set_child(self.box)
