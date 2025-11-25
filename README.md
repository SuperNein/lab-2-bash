# Лабораторная работа 2
## Medium

---

*test в разработке*

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
    └───__init__.py
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

```
# Установка зависимостей
pip install -r requirements.txt

# Документация по командам
python -m src.main --help

# Вызов команды
python -m src.main COMMAND [OPTIONS] [ARGS]... 

# Запуск интерактивного режима
python -m src.main run
```

--- 

### Выводы

В ходе работы я научился:
- Работать с os, pathlib, shutil, shlex
- Разрабатывать консольный интерфейс с typer
