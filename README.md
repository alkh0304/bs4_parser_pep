# Python Docs and PEP Parser

## Описание:

Python Docs and PEP Parser - учебный проект, целью которого является практика в создании парсеров.

Написанные в этом проекте парсеры берут с официального сайта, посвященного [Python](https://docs.python.org/3/).

Для удобства пользователя, в проекте реализован парсинг аргументов командной строки для выбора режима работы программы.

## Технологии и библиотеки:
- [Python](https://www.python.org/);
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/);
- [argparse](https://docs.python.org/3/library/argparse.html);
- [prettytable](https://pypi.org/project/prettytable/);
- [tqdm](https://pypi.org/project/tqdm/);
- [requests_cache](https://pypi.org/project/requests-cache/).

## Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке

- Создать виртуальное окружение и установить зависимости

- Перейти в директорию src

## Как использовать парсеры:
Вызов вспомогательной справки:

```
python main.py -h
```

Вызов парсера, выдающего список ссылок на перечень изменений в версиях Python:

```
python main.py whats-new
```

Вызов парсера, выдающего список ссылок на документацию всех версий Python:

```
python main.py latest-versions
```

Вызов парсера, скачивающего архив документации для последней версии Python:

```
python main.py download
```

Вызов парсера, считывающего статусы всех PEP и выводящего их в общем списке:

```
python main.py pep
```

## Дополнительные способы вывода данных:
- **--output pretty**: выводит данные в терминале в ASCII таблице.
- **--output file**: сохраняет вывод данных в папке results в csv формате с указанием даты.

## Над проектом [Python Docs and PEP Parser](https://github.com/alkh0304/bs4_parser_pep) работал:

[Александр Хоменко](https://github.com/alkh0304)
