import os
import sys

# Имя этого файла
CURRENT_SCRIPT_NAME = os.path.basename(__file__)
# Список локалей
LOCALES = ['ru', 'en']
DEFAULT_REQUIREMENTS = 'requirements.txt'
DEFAULT_PORT = '8000'
DEFAULT_DB_LABEL = 'default'
# Список команд
COMMANDS = {
    'create_local': f'[1] Создание локалей {LOCALES}',
    'update_local': '[2] Обновление и компилирование локалей',
    'collect_static': '[3] Сборка статических файлов в папку STATIC_ROOT',
    'make_migrations': '[4] Создание миграций',
    'make_migrations_app': '[5] Создание первой миграции для приложения',
    'make_empty_migrations_app': '[6] Создание пустой миграции для приложения. '
                                 'Используется для добавления default данных в таблицу БД',
    'migrate': '[7] Применение миграций',
    'create_superuser': '[8] Создание пользовтеля с правами superuser. '
                        'Если не работает попробуйте запустить в терминале: '
                        f'python {CURRENT_SCRIPT_NAME} create_superuser',
    'create_app': '[9] Создание приложения',
    'run_server': f'[10] Запуск проекта на порту (по умолчанию {DEFAULT_PORT})',
    'install_requirements': f'[11] Установит все зависимости для проекта из файла (по умолчанию {DEFAULT_REQUIREMENTS})',
    'print_requirements': '[12] Автоматически сгенерирует все необходимые зависимости для проекта, '
                          f'а также позволяет сохранить этот список в файл (по умолчанию {DEFAULT_REQUIREMENTS})',
    'help или ?': 'Описания команд'
}


def help_command():
    print('Доступные команды:')
    for key, value in COMMANDS.items():
        print("{:<30} {}".format(key, value))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Список переданных аргуметов начиная с 1 индекса
        commands = sys.argv[1:]
    else:
        help_command()
        # Ввод команды, strip() - для удаления пробелов по краям в строке
        commands = input('Введите команды через пробел или их числовое значение: ').strip()
        commands = commands.split()

    for com in commands:
        print('=' * 10, f'start {com}', '=' * 10)

        if com == 'create_local' or com == '1':
            for locale in LOCALES:
                cmd = 'django-admin makemessages -l'
                os.system(f'{cmd} {locale} -i venv')
        elif com == 'update_local' or com == '2':
            os.system('django-admin makemessages -a -i venv')
            os.system('django-admin compilemessages')
        elif com == 'collect_static' or com == '3':
            os.system('python manage.py collectstatic')
        elif com == 'make_migrations' or com == '4':
            os.system('python manage.py makemigrations')
        elif com == 'make_migrations_app' or com == '5':
            app_name = input('Введите название приложения: ').strip()
            if app_name != '':
                os.system(f'python manage.py makemigrations {app_name}')
            else:
                print('Необходимо вести название приложения!')
        elif com == 'make_empty_migrations_app' or com == '6':
            app_name = input('Введите название приложения: ').strip()
            if app_name != '':
                os.system(f'python manage.py makemigrations --empty {app_name}')
            else:
                print('Необходимо вести название приложения!')
        elif com == 'migrate' or com == '7':
            db = input(f'Введите метку БД по-умолчанию ({DEFAULT_DB_LABEL}): ').strip()
            os.system(f'python manage.py migrate --database={db or DEFAULT_DB_LABEL}')
        elif com == 'create_superuser' or com == '8':
            os.system('python manage.py createsuperuser')
        elif com == 'create_app' or com == '9':
            app_name = input('Введите название приложения: ').strip()
            if app_name != '':
                os.system(f'python manage.py startapp {app_name}')
            else:
                print('Необходимо вести название приложения!')
        elif com == 'run_server' or com == '10':
            port = input(f'Введите порт (по умолчанию: {DEFAULT_PORT}): ').strip()
            os.system(f'python manage.py runserver {port}')
        elif com == 'install_requirements' or com == '11':
            name = input(f'Введите название файла (по умолчанию: {DEFAULT_REQUIREMENTS}): ').strip()
            if name == '':
                name = DEFAULT_REQUIREMENTS
            os.system(f'pip install -r {name}')
        elif com == 'print_requirements' or com == '12':
            cmd = 'pip freeze'
            print('Список зависимостей для проекта:')
            os.system(f'{cmd}')
            is_yes = input('Сохранить этот список в файл? (yes или no): ').strip()
            if is_yes == 'yes' or is_yes == 'y':
                name = input(f'Введите название файла (по умолчанию: {DEFAULT_REQUIREMENTS}): ').strip()
                if name == '':
                    name = DEFAULT_REQUIREMENTS
                os.system(f'{cmd} > {name}')
                print(f'Сохранено в файл {name}')
        elif com == 'help' or com == '?':
            help_command()
        else:
            print(f'Такой команды {com} нет!')
            help_command()

        print('=' * 10, f'end {com}', '=' * 10, '\n')
