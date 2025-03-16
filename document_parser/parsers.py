import subprocess
from abc import ABC, abstractmethod
from io import StringIO
from pathlib import Path

import fitz  # PyMuPDF
import ftfy
import html2text
from pymupdf import EmptyFileError
from spire.doc import Document
import chardet

class BaseParser(ABC):
    def __init__(self, path: Path):
        self.path = path

    @abstractmethod
    def parse(self) -> StringIO:
        pass


class HtmlParser(BaseParser):
    def __init__(self, path):
        super().__init__(path)

    def parse(self) -> StringIO:
        text_handler = html2text.HTML2Text()
        text_handler.ignore_links = True
        text_handler.ignore_images = True
        text_handler.ignore_mailto_links = True
        stream = StringIO()
        with self.path.open('rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        with self.path.open("r", encoding=encoding) as file:
            content = file.read()
            stream.write(text_handler.handle(content))

        return stream


class PdfParser(BaseParser):
    def __init__(self, path):
        super().__init__(path)

    def parse(self) -> StringIO:
        stream = StringIO()
        try:
            file = fitz.open(self.path)
            for page in file:
                text = page.get_text(sort=False)  # что лучше True/False
                stream.write(ftfy.fix_text(text))
            file.close()
        except EmptyFileError:
            pass
        return stream


# NOTE: Возможен переход на python-docx или другое
class DocParser(BaseParser):
    def __init__(self, path):
        super().__init__(path)

    def parse(self) -> StringIO:
        stream = StringIO()
        doc = Document()

        try:
            doc.LoadFromFile(str(self.path.resolve()))

            text = doc.GetText() + "\n"

            # убираем первую строку(там говно от spire.doc)
            lines = (line for line in text.splitlines())
            next(lines)
            text = "\n".join(lines)

            stream.write(text + "\n")
        except Exception as e:
            print(f"Error while processing file: {e}")
        finally:
            doc.Close()

        return stream


class DjvuParser(BaseParser):
    def __init__(self, path):
        super().__init__(path)

    def parse(self) -> StringIO:
        stream = StringIO()
        result = subprocess.run(
            ["djvutxt", str(self.path.resolve())], capture_output=True, text=True
        )

        # ftfy должен порешать траблы с кодировкой и убираем переводной символ
        result = ftfy.fix_text(result.stdout).replace("\x0c", "")
        stream.write(result)
        return stream
