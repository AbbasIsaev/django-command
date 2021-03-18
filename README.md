# DjangoFastCommands

DjangoFastCommands - список часто используемых команд при разработке проектов на Django.

### Запуск

```shell
python command.py
```

### Доступные команды

```shell
(venv) .\DjangoFastCommands>python command.py
Доступные команды:
create_local                   Создание локалей ['ru', 'en']
update_local                   Обновление и компилирование локалей
collect_static                 Сборка статических файлов в папку STATIC_ROOT
make_migrations                Создание миграций
make_migrations_app            Создание первой миграции для приложения
make_empty_migrations_app      Создание пустой миграции для приложения. Используется для добавления default данных в таблицу БД
migrate                        Применение миграций
create_superuser               Создание пользовтеля с правами superuser. Если не работает попробуйте запустить в терминале: python command.py create_superuser
create_app                     Создание приложения
run_server                     Запуск проекта на порту (по умолчанию 8000)
install_requirements           Установит все зависимости для проекта из файла (по умолчанию requirements.txt)
print_requirements             Автоматически сгенерирует все необходимые зависимости для проекта, а также позволяет сохранить этот список в файл (по умолчанию requirements.txt)
help или ?                     Описания команд
```