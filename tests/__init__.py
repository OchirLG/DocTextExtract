import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import pytest
    from document_parser.parser_manager import ParserManager
    from document_parser.parsers import HtmlParser, PdfParser, DocParser, DjvuParser
    from io import StringIO


# Тест работоспособности
def test_true_html():
    parser = ParserManager.get_parser("test_files/test.html")
    assert isinstance(parser, HtmlParser)
    stream = parser.parse()
    assert isinstance(stream, StringIO)
    assert "Hello" in stream.getvalue()


def test_true_pdf():
    parser = ParserManager.get_parser("test_files/test.pdf")
    assert isinstance(parser, PdfParser)
    stream = parser.parse()
    assert isinstance(stream, StringIO)
    assert "Hello" in stream.getvalue()


def test_true_doc():
    parser = ParserManager.get_parser("test_files/test.doc")
    assert isinstance(parser, DocParser)
    stream = parser.parse()
    assert isinstance(stream, StringIO)
    assert "Hello" in stream.getvalue()


def test_true_docx():
    parser = ParserManager.get_parser("test_files/test.docx")
    assert isinstance(parser, DocParser)
    stream = parser.parse()
    assert isinstance(stream, StringIO)
    assert "Hello" in stream.getvalue()


def test_true_djvu():
    parser = ParserManager.get_parser("test_files/test.djvu")
    assert isinstance(parser, DjvuParser)

    try:
        stream = parser.parse()
    except FileNotFoundError:
        warnings.warn("DJVU parser not found")
        return
    assert isinstance(stream, StringIO)
    assert "Hello" in stream.getvalue()


# Тест неверных входных данных
def test_invalid_file():
    with pytest.raises(ValueError):
        ParserManager.get_parser("test_files/test.pptx")


def test_nonexistent_file():
    with pytest.raises(ValueError):
        ParserManager.get_parser("test_files/nonexistent.pdf")


def test_empty_file():
    parser = ParserManager.get_parser("test_files/empty.pdf")
    stream = parser.parse()
    assert len(stream.getvalue()) == 0


# Специальные тесты
# Проверка особых символов
def test_special_chars():
    parser = ParserManager.get_parser("test_files/special_chars.html")
    stream = parser.parse()
    assert "Hello \\n Привет 你好 * < p>" in stream.getvalue()


# Проверка кодировки файла
def test_encoding():
    parser = ParserManager.get_parser("test_files/cp1251.html")
    stream = parser.parse()
    assert "Привет" in stream.getvalue()

