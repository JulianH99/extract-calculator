from typing import final


from ..reader.parser import Record
from .formatter import format_money

from gi.repository import Gtk, GObject, Gio


@final
class RecordRow(GObject.GObject):
    __gtype_name__ = "RecordRow"
    selected = GObject.Property(type=bool, default=False)
    concept = GObject.Property(type=str, default=None)
    movement_value = GObject.Property(type=float, default=None)
    date = GObject.Property(type=str, default=None)
    paid_this_month = GObject.Property(type=float, default=None)
    left_to_pay = GObject.Property(type=float, default=None)
    id = None

    def __init__(self, record: Record):
        super().__init__()
        self.concept = record.concept
        self.movement_value = record.movement_value
        self.date = record.date
        self.paid_this_month = record.paid_this_month
        self.left_to_pay = record.left_to_pay
        self.id = id(self)


def setup_text_widget(_, item: GObject.GObject):
    label = Gtk.Label()
    item.set_child(label)


def setup_checkbox_widget(on_toggle):
    def fn(_, item: GObject.GObject):
        checkbox = Gtk.CheckButton()
        checkbox.connect("toggled", on_toggle(item))
        item.set_child(checkbox)

    return fn


def bind_selected(_, item: GObject.GObject):
    checkbox = item.get_child()
    checkbox.set_active(item.get_item().selected)


def bind_concept(_, item: GObject.GObject):
    label = item.get_child()
    label.set_text(item.get_item().concept)


def bind_movement_value(_, item: GObject.GObject):
    label = item.get_child()
    label.set_text(format_money(item.get_item().movement_value))


def bind_date(_, item: GObject.GObject):
    label = item.get_child()
    label.set_text(item.get_item().date)  # TODO: format the date


def bind_paid_this_month(_, item: GObject.GObject):
    label = item.get_child()
    label.set_text(format_money(item.get_item().paid_this_month))


def bind_left_to_pay(_, item: GObject.GObject):
    label = item.get_child()
    label.set_text(format_money(item.get_item().left_to_pay))


def create_column_factory(bind_fn, setup_fn) -> Gtk.SignalListItemFactory:
    factory = Gtk.SignalListItemFactory()
    factory.connect("setup", setup_fn)
    factory.connect("bind", bind_fn)
    return factory


def create_column(
    title: str, factory: Gtk.SignalListItemFactory
) -> Gtk.ColumnViewColumn:
    column = Gtk.ColumnViewColumn()
    column.set_title(title)
    column.set_factory(factory)

    return column


@final
class Table:
    def __init__(self, records: list[Record]):
        self.records = records
        self.selected_records = []
        self.on_list_change = None

    def set_on_list_change(self, fn):
        self.on_list_change = fn

    def on_toggle(self, item):
        def fn(_):
            print(item.get_item().id)

        return fn

    def build(self):
        list_view = Gtk.ColumnView()

        selected_factory = create_column_factory(
            bind_selected, setup_checkbox_widget(self.on_toggle)
        )
        selected_column = create_column("Selected", selected_factory)

        concept_factory = create_column_factory(bind_concept, setup_text_widget)
        concept_column = create_column("Concept", concept_factory)

        movement_value_factory = create_column_factory(
            bind_movement_value, setup_text_widget
        )
        movement_value_column = create_column("Movement value", movement_value_factory)

        date_value_factory = create_column_factory(bind_date, setup_text_widget)
        date_column = create_column("Date", date_value_factory)

        paid_this_month_factory = create_column_factory(
            bind_paid_this_month, setup_text_widget
        )
        paid_this_month_column = create_column(
            "Paid this month", paid_this_month_factory
        )

        left_to_pay_factory = create_column_factory(bind_left_to_pay, setup_text_widget)
        left_to_pay_column = create_column("Left to pay", left_to_pay_factory)

        store = Gio.ListStore.new(RecordRow)
        for item in self.records:
            store.append(RecordRow(item))

        selection = Gtk.SingleSelection(model=store)
        list_view.set_model(selection)

        list_view.append_column(selected_column)
        list_view.append_column(concept_column)
        list_view.append_column(movement_value_column)
        list_view.append_column(date_column)
        list_view.append_column(paid_this_month_column)
        list_view.append_column(left_to_pay_column)

        return list_view
