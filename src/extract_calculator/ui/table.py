from typing import final
from ..reader.parser import Record

from gi.repository import Gtk, GObject, Gio


@final
class RecordRow(GObject.GObject):
    __gtype_name__ = "RecordRow"
    concept = GObject.Property(type=str, default=None)
    movement_value = GObject.Property(type=float, default=None)

    def __init__(self, record: Record):
        super().__init__()
        self.concept = record.concept
        self.movement_value = record.movement_value


def setup_text_widget(_, item: GObject.GObject):
    label = Gtk.Label()
    item.set_child(label)


def bind_concept(_, item: GObject.GObject):
    label = item.get_child()
    label.set_text(item.get_item().concept)


def bind_movement_value(_, item: GObject.GObject):
    label = item.get_child()
    label.set_text(str(item.get_item().movement_value))


def build_table(records: list[Record]):
    # TODO: build scrollable window

    list_view = Gtk.ColumnView()

    concept_factory = Gtk.SignalListItemFactory()
    concept_factory.connect("setup", setup_text_widget)
    concept_factory.connect("bind", bind_concept)

    movement_value_factory = Gtk.SignalListItemFactory()
    movement_value_factory.connect("setup", setup_text_widget)
    movement_value_factory.connect("bind", bind_movement_value)

    store = Gio.ListStore.new(RecordRow)
    for item in records:
        store.append(RecordRow(item))

    selection = Gtk.SingleSelection(model=store)
    list_view.set_model(selection)

    concept_column = Gtk.ColumnViewColumn()
    concept_column.set_title("Concept")
    concept_column.set_factory(concept_factory)

    movement_value_column = Gtk.ColumnViewColumn()
    movement_value_column.set_title("Movement value")
    movement_value_column.set_factory(movement_value_factory)

    list_view.append_column(concept_column)
    list_view.append_column(movement_value_column)

    return list_view
