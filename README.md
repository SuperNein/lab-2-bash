# Лабораторная работа 2
## Medium

---

### Цели работы
- Освоить работу с файловой системой средствами Python.
- Реализовать основные команды управления файлами и каталогами.
- Научиться вести журнал действий пользователя.
- Освоить расширение функциональности за счёт
дополнительных модулей-плагинов.

---

### Структура проекта

```
lab-2-bash
│   .gitignore
│   .pre-commit-config.yaml
│   pyproject.toml
│   README.md
│   requirements.txt
│    
├───src
│   │   main.py
│   │   __init__.py
│   │   
│   ├───common
│   │       config.py
│   │       constants.py
│   │       __init__.py
│   │           
│   ├───dependencies
│   │       container.py
│   │       __init__.py
│   │           
│   └───services
│           base.py
│           console.py
│           path_funcs.py
│           typer_std.py
│           __init__.py
│           
└───tests
        conftest.py
        tests_cat.py
        tests_cd.py
        tests_cp.py
        tests_ls.py
        tests_mv.py
        tests_rm.py
        tests_tar.py
        tests_untar.py
        tests_unzip.py
        tests_zip.py
        __init__.py
```

### Библиотеки

```
- logging
- pathlib
- os
- shutil
- shlex
- zipfile
- tarfile
- typer
```

---

### Документация

#### Установка и запуск

```
# Установка зависимостей
pip install -r requirements.txt

# Документация по командам
python -m src.main [COMMAND] --help

# Вызов команды
python -m src.main COMMAND [OPTIONS] [ARGS]... 

# Запуск интерактивного режима
python -m src.main run
```

#### Команды

```
# Интерактивный режим
run    # Запуск интерактивного режима
exit    # Прерывание интерактивного режима

# Работа с файлами
ls [OPTIONS] [PATH]    # Содержимое директории. [-l] - Подробная информация о содержимом
cd PATH    # Переход в директорию
cat PATH    # Вывод содержимого файла
cp [OPTIONS] PATH_FROM PATH_TO    # Копирование. [-r] - Рекурсивное копирование
mv PATH_FROM PATH_TO    # Переместить
rm [OPTIONS] PATH    # Удаление (перемещает удаленное в .trash корня проекта). [-r] - Рекурсивное удаление

# Архивы и история
zip FOLDER ARCHIVE    # Архивация zip
unzip ARCHIVE    # Разархивация zip
tar FOLDER ARCHIVE    # Архивация tar.gz
untar ARCHIVE    # Разархивация tar.gz
history [NUM]    # Вывод последних NUM введенных команд. Выводит всю историю без аргумента
```

- Для подробного описания конкретной команды в интерактивном режиме можно использовать `COMMAND --help`

--- 

### Выводы

В ходе работы я научился:
- Работать с os, pathlib, shutil, shlex
- Разрабатывать консольный интерфейс с typer
- Писать тесты с фикстурами
