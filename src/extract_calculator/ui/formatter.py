import locale

_ = locale.setlocale(locale.LC_ALL, "")


# def format_money(money: float) -> str:
#     return locale.currency(money, grouping=True)


def format_money(value: float) -> str:
    return "${:0,.0f}".format(value)
