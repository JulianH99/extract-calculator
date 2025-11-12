import re
import pdfplumber

from pdfplumber.pdf import PDF


def _clean_text(text: str) -> str:
    def remove_repeats(word: str):
        if not word:
            return word
        cleaned = word[0]
        for char in word[1:]:
            if char != cleaned[-1] or char.isdigit():
                cleaned += char
        return cleaned

    words = text.split()
    cleaned_words = [remove_repeats(word) for word in words]
    return " ".join(cleaned_words)


def _get_text(file: PDF) -> str:
    text = ""
    pages = file.pages

    for page in pages:
        text += page.extract_text()
        text += "\n"

    clean_text = _clean_text(text)
    return clean_text


def _clean_row(row: str) -> str:
    text_without_reference = re.split(r"[RXFC]\d{2,}|0{6}", row)[0]
    cut_text_start = text_without_reference.find('"En')
    text_start = cut_text_start if cut_text_start != -1 else len(text_without_reference)

    return text_without_reference[:text_start].strip()


def _join_date(rows: list[str]) -> list[str]:
    """
    Joins the row that contains the date with the next row
    that holds the record corresponding to that date

    """
    joined_rows = []
    for i in range(len(rows)):
        if i % 2 == 0:
            joined_rows.append(rows[i - 1] + " " + rows[i])
    return joined_rows


def _get_rows(text: str) -> list[str]:
    table_start = text.find("Nuevosmovimientosentre")
    table_end = text.find("Movimientosantes")

    table_text = text[table_start:table_end]

    rows = re.split(r"(\d{1,}\/\d{2}\/\d{4})", table_text)

    cleaned_rows = [_clean_row(row) for row in rows]
    cleaned_rows = _join_date(cleaned_rows)
    cleaned_rows = [
        row for row in cleaned_rows if re.match(r".*\d{1,}\/\d{2}\/\d{4}.*", row)
    ]
    return cleaned_rows


def read_pdf_rows(path: str) -> list[str]:
    with pdfplumber.open(path) as file:
        text = _get_text(file)
        rows = _get_rows(text)

        return rows
