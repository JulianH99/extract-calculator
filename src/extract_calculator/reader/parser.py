import re
from typing import final, override


@final
class Record:
    def __init__(
        self,
        date: str,
        concept: str,
        movement_value: float,
        paid_this_month: float,
        left_to_pay: float,
    ):
        self.date = date
        self.concept = concept
        self.movement_value = movement_value
        self.paid_this_month = paid_this_month
        self.left_to_pay = left_to_pay

    @override
    def __str__(self) -> str:
        return f"{self.date}: {self.concept} -> ${self.movement_value} / ${self.paid_this_month} / ${self.left_to_pay}"


def _parse_row(row: str) -> Record:
    """
    Parse a row using regex to extract the different values
    TODO: test and ensure no errors show up
    """

    date_matches = re.match(r"(\d{1,}\/\d{1,}\/\d{4})", row)
    date = date_matches.group(1) if date_matches else ""
    date_end = date_matches.end() if date_matches else 0

    concept_matches: list[str] = re.findall(r"([A-Za-z]*)", row[date_end:])
    concept = " ".join([match for match in concept_matches if len(match.strip()) > 0])

    first_dollar_sign = row.find("$")
    number_matches: list[str] = re.findall(
        r"([-{0,}\d.{0,}/{0,}]*)", row[first_dollar_sign:]
    )
    number_matches = [
        match.replace(".", "").replace(",", ".")
        for match in number_matches
        if len(match.strip()) > 0 and match.find("/") == -1
    ]

    total_to_pay = float(number_matches[0])
    paid_this_month = float(number_matches[1])
    left_to_pay = float(number_matches[-1])

    return Record(
        date=date,
        concept=concept,
        movement_value=total_to_pay,
        paid_this_month=paid_this_month,
        left_to_pay=left_to_pay,
    )


def parse_rows(rows: list[str]) -> list[Record]:
    """
    Parse every row from the pdf into a Record instance.
    An example of a row in the row list is as follows:
    05/10/2025 AIRLAF INTERNACIONAL S $ 311.900,00     1/12 $ 25.991,67 1,8312 % 24,3283 %        $ 285.908,33
    ^          ^                        ^              ^      ^         ^         ^               ^
    Date       Concept                  Total to pay   Terms  Paid      Interest  More Interest   Left to pay
    """

    return [_parse_row(row) for row in rows]
