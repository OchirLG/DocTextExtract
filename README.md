Для работы требуется установить `djvutxt`(входящие в пакет [DjvuLibre](https://djvu.sourceforge.net/])) и добавить утилиту в переменные среды `PATH`(Windows)

Для linux систем:
> sudo apt-get install djvulibre-bin

Использование:
```python
import document_parser.parser_manager
from io import StringIO

path = "C:\\Users\\example.html"
parser = ParserManager.get_parser(path)
content: StringIO = parser.parse()
text: str = content.getvalue()
```
Далее можно работать с содержимым в формате `StringIO` или `str`. И потом записать в файл.