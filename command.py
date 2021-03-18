import os
import sys

# Имя этого файла
CURRENT_SCRIPT_NAME = os.path.basename(__file__)
# Список локалей
LOCALES = ['ru', 'en']
DEFAULT_REQUIREMENTS = 'requirements.txt'
DEFAULT_PORT = '8000'
# Список команд
COMMANDS = {
    'create_local': f'Создание локалей {LOCALES}',
    'update_local': 'Обновление и компилирование локалей',
    'collect_static': 'Сборка статических файлов в папку STATIC_ROOT',
    'make_migrations': 'Создание миграций',
    'make_migrations_app': 'Создание первой миграции для приложения',
    'make_empty_migrations_app': 'Создание пустой миграции для приложения. '
                                 'Используется для добавления default данных в таблицу БД',
    'migrate': 'Применение миграций',
    'create_superuser': 'Создание пользовтеля с правами superuser. Если не работает попробуйте запустить в терминале: '
                        f'python {CURRENT_SCRIPT_NAME} create_superuser',
    'create_app': 'Создание приложения',
    'run_server': f'Запуск проекта на порту (по умолчанию {DEFAULT_PORT})',
    'install_requirements': f'Установит все зависимости для проекта из файла (по умолчанию {DEFAULT_REQUIREMENTS})',
    'print_requirements': 'Автоматически сгенерирует все необходимые зависимости для проекта, '
                          f'а также позволяет сохранить этот список в файл (по умолчанию {DEFAULT_REQUIREMENTS})',
    'help или ?': 'Описания команд'
}


def help_command():
    print('Доступные команды:')
    for key, value in COMMANDS.items():
        print("{:<30} {}".format(key, value))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        com = sys.argv[1]
    else:
        help_command()
        # Ввод команды, strip() - для удаления пробелов по краям в строке
        com = input('Введите команду (? - показать список команд): ').strip()

    print('=' * 10, f'start {com}', '=' * 10)

    if com == 'create_local':
        for locale in LOCALES:
            cmd = 'django-admin makemessages -l'
            os.system(f'{cmd} {locale}')
    elif com == 'update_local':
        os.system('django-admin makemessages -a')
        os.system('django-admin compilemessages')
    elif com == 'collect_static':
        os.system('python manage.py collectstatic')
    elif com == 'make_migrations':
        os.system('python manage.py makemigrations')
    elif com == 'make_migrations_app':
        app_name = input('Введите название приложения: ').strip()
        if app_name != '':
            os.system(f'python manage.py makemigrations {app_name}')
        else:
            print('Необходимо вести название приложения!')
    elif com == 'make_empty_migrations_app':
        app_name = input('Введите название приложения: ').strip()
        if app_name != '':
            os.system(f'python manage.py makemigrations --empty {app_name}')
        else:
            print('Необходимо вести название приложения!')
    elif com == 'migrate':
        os.system('python manage.py migrate')
    elif com == 'create_superuser':
        os.system('python manage.py createsuperuser')
    elif com == 'create_app':
        app_name = input('Введите название приложения: ').strip()
        if app_name != '':
            os.system(f'python manage.py startapp {app_name}')
        else:
            print('Необходимо вести название приложения!')
    elif com == 'run_server':
        port = input(f'Введите порт (по умолчанию: {DEFAULT_PORT}): ').strip()
        os.system(f'python manage.py runserver {port}')
    elif com == 'install_requirements':
        name = input(f'Введите название файла (по умолчанию: {DEFAULT_REQUIREMENTS}): ').strip()
        if name == '':
            name = DEFAULT_REQUIREMENTS
        os.system(f'pip install -r {name}')
    elif com == 'print_requirements':
        cmd = 'pip freeze'
        print('Список зависмостей для проекта:')
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

    print('=' * 10, f'end {com}', '=' * 10)
