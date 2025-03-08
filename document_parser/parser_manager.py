
from io import StringIO
from pathlib import Path

from document_parser.parsers import HtmlParser
from document_parser.parsers import PdfParser
from document_parser.parsers import DocParser
from document_parser.parsers import DjvuParser

class ParserManager:
    SUPPORTED_EXTENSIONS = {
        ".html": HtmlParser,
        ".pdf": PdfParser,
        ".doc": DocParser,
        ".docx": DocParser,
        ".djvu": DjvuParser,
    }
     
    @staticmethod
    def get_parser(path: Path):
        """Chooses parser due to it's extension

        Args:
            path (Path): path to the file in system
        """
        path = Path(path)
        if not path.is_file():
            raise ValueError("file not found")

        extension = path.suffix
        parser_class = ParserManager.SUPPORTED_EXTENSIONS[extension]
        if parser_class:
            return parser_class(path)
       
        raise ValueError("Unsupported file")

def main():
    path = r"C:\Users\Очир\Downloads\file-sample_500kB.doc"
    parser = ParserManager.get_parser(path)
    text = parser.parse().getvalue()
    
    #print(text)

    with open("test.txt", mode='w', encoding='utf-8') as file:
        file.write(text)

if __name__ == "__main__":
    main()