from img2table.document import PDF
from io import BytesIO
from bs4 import BeautifulSoup
import re
import json
import fitz
from pathlib import Path

def extract_table(pdf_path):
    file_name = Path(pdf_path).stem 
    # Definition of PDF from path
    # The optional pages argument enables the extraction of table on specific pages of the PDF
    pdf_from_path = PDF(src=pdf_path, pages=[0, 1])

    # Definition of PDF from bytes
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    pdf_from_bytes = PDF(src=pdf_bytes)

    # Definition of PDF from file-like object
    pdf_from_file_like = PDF(src=BytesIO(pdf_bytes))
    tables = pdf_from_file_like.extract_tables()

    docs = []
    for table_list in tables.values():
        for table in table_list:
            soup = BeautifulSoup(table.html, 'html.parser')
            table_data = [
                [
                    re.sub(' +', ' ', 
                        cell.text
                        .replace("\n", " ")
                        .replace("  ", " ")
                        .replace('"', "'")
                        .strip()
                        ) 
                    for cell in row("td")
                ] 
                for row in soup("tr")
            ]
            column_names = table_data[0]
            doc = []
            if len(table_data) > 1:
                for row in table_data[1:]:
                    row_text = {}
                    for idx, cell in enumerate(row):
                        row_text [column_names[idx] ] =  cell
                    doc.append(row_text)
            else:
                for row in table_data:
                    for idx, cell in enumerate(row):
                        doc.append({column_names[idx]  : cell })
            docs.append(f'{file_name} :' + json.dumps(doc))
    return docs

def extract_text(pdf_path):
    file_name = Path(pdf_path).stem
    docs = []
    doc = fitz.open(pdf_path)
    text = ""
    # Extract text from each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
        text = text.replace("\n", " ")
        for t in text.split('</sec>'):
            docs.append(f'{file_name} :' + t)
    return docs

def extract(pdf_path):
    return extract_text(pdf_path) + extract_table(pdf_path)
