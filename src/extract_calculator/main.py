import gi

from .ui.main_window import MainWindow, MainApp
from .reader.reader import read_pdf_rows
from .reader.parser import parse_rows

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")


# def on_activate(app):
#     win = MainWindow()
#     app.add_window(win)
#     win.present()


if __name__ == "__main__":
    rows = read_pdf_rows("./extracto1.pdf")
    records = parse_rows(rows)

    window = MainWindow(records)

    app = MainApp(window=window)
    app.run(None)

    # main()
