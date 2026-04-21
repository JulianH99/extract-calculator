from typing import final
from ..ui.formatter import format_money



from gi.repository import Gtk


_total_template = '<b>Total (movement value):</b> {total}'
_total_paid = '<b>Paid in this period:</b> {total}'
_total_left_to_pay = '<b>Total left to pay:</b> {total}'

@final
class Footer(Gtk.ActionBar):
    __gtype_name__ = "Footer"

    def __init__(self):
        super().__init__()

        self.total_label = Gtk.Label(label="Total")
        self.total_paid_label  = Gtk.Label()
        self.total_left_to_pay_label  = Gtk.Label()

        self.pack_start(self.total_label)
        self.pack_start(Gtk.Separator())
        self.pack_start(self.total_paid_label)
        self.pack_start(Gtk.Separator())
        self.pack_start(self.total_left_to_pay_label)

    def set_total(self, total_value: float):
        self.total_label.set_markup(_total_template.format(total=format_money(total_value)))

    def set_total_paid(self, total_value: float):
        self.total_paid_label.set_markup(_total_paid.format(total=format_money(total_value)))

    def set_total_left_to_pay(self, total_value: float):
        self.total_left_to_pay_label.set_markup(_total_left_to_pay.format(total=format_money(total_value)))



