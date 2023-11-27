import os
import sys

import inquirer

# Имя этого файла
CURRENT_SCRIPT_NAME = os.path.basename(__file__)
# Список локалей
LOCALES = ['ru', 'en']
DEFAULT_REQUIREMENTS = 'requirements.txt'
DEFAULT_PORT = '8000'
DEFAULT_DB_LABEL = 'default'

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
    'create_superuser': 'Создание пользователя с правами superuser. '
                        'Если не работает попробуйте запустить в терминале: '
                        f'python {CURRENT_SCRIPT_NAME} create_superuser',
    'create_app': 'Создание приложения',
    'run_server': f'Запуск проекта на порту (по умолчанию {DEFAULT_PORT})',
    'install_requirements': f'Установит все зависимости для проекта из файла (по умолчанию {DEFAULT_REQUIREMENTS})',
    'print_requirements': 'Автоматически сгенерирует все необходимые зависимости для проекта, '
                          f'а также позволяет сохранить этот список в файл (по умолчанию {DEFAULT_REQUIREMENTS})'
}


def cli():
    answers = {}
    if len(sys.argv) > 1:
        # Список переданных аргументов начиная с 1 индекса
        answers['commands'] = sys.argv[1:]
    else:
        choices_commands = [
            ("{:<30} [{}] {}".format(key, index + 1, value), key) for index, (key, value) in enumerate(COMMANDS.items())
        ]
        questions = [
            inquirer.Checkbox(
                'commands',
                message="Выберите 1 или несколько команд",
                choices=choices_commands,
            )
        ]
        answers = inquirer.prompt(questions)
        if answers is None:
            return

    for com in answers['commands']:
        try:
            com = int(com)
            com = list(COMMANDS)[com - 1]
        except ValueError as e:
            pass
        except Exception as e:
            pass

        print('=' * 10, f'start {com}', '=' * 10)

        if com == 'create_local':
            for locale in LOCALES:
                cmd = 'django-admin makemessages -l'
                os.system(f'{cmd} {locale} -i venv')
        elif com == 'update_local':
            os.system('django-admin makemessages -a -i venv')
            os.system('django-admin compilemessages -i venv')
        elif com == 'collect_static':
            os.system('python manage.py collectstatic')
        elif com == 'make_migrations':
            os.system('python manage.py makemigrations')
        elif com == 'make_migrations_app':
            question = [
                inquirer.Text(
                    'app_name',
                    message='Введите название приложения'
                )
            ]
            answer = inquirer.prompt(question)
            app_name = answer['app_name']

            if app_name != '':
                os.system(f'python manage.py makemigrations {app_name}')
            else:
                print('Необходимо вести название приложения!')
        elif com == 'make_empty_migrations_app':
            question = [
                inquirer.Text(
                    'app_name',
                    message='Введите название приложения'
                )
            ]
            answer = inquirer.prompt(question)
            app_name = answer['app_name']

            if app_name != '':
                os.system(f'python manage.py makemigrations --empty {app_name}')
            else:
                print('Необходимо вести название приложения!')
        elif com == 'migrate':
            question = [
                inquirer.Text(
                    'db',
                    message='Введите метку БД',
                    default=DEFAULT_DB_LABEL
                )
            ]
            answer = inquirer.prompt(question)
            db = answer['db']

            os.system(f'python manage.py migrate --database={db or DEFAULT_DB_LABEL}')
        elif com == 'create_superuser':
            os.system('python manage.py createsuperuser')
        elif com == 'create_app':
            question = [
                inquirer.Text(
                    'app_name',
                    message='Введите название приложения'
                )
            ]
            answer = inquirer.prompt(question)
            app_name = answer['app_name']

            if app_name != '':
                os.system(f'python manage.py startapp {app_name}')
            else:
                print('Необходимо вести название приложения!')
        elif com == 'run_server':
            question = [
                inquirer.Text(
                    'port',
                    message='Введите порт',
                    default=DEFAULT_PORT
                )
            ]
            answer = inquirer.prompt(question)
            port = answer['port']

            os.system(f'python manage.py runserver {port}')
        elif com == 'install_requirements':
            question = [
                inquirer.Text(
                    'fileName',
                    message='Установить зависимости из файла',
                    default=DEFAULT_REQUIREMENTS
                )
            ]
            answer = inquirer.prompt(question)
            name = answer['fileName']
            if name == '':
                name = DEFAULT_REQUIREMENTS

            os.system(f'pip install -r {name}')
        elif com == 'print_requirements':
            cmd = 'pip freeze'
            print('Список зависимостей для проекта:')
            os.system(f'{cmd}')

            question = [
                inquirer.List(
                    'saveToFile',
                    message='Сохранить этот список в файл',
                    choices=['yes', 'no']
                )
            ]
            answer = inquirer.prompt(question)
            if answer['saveToFile'] == 'yes':
                question = [
                    inquirer.Text(
                        'fileName',
                        message='Введите название файла',
                        default=DEFAULT_REQUIREMENTS
                    )
                ]
                answer = inquirer.prompt(question)
                name = answer['fileName']
                if name == '':
                    name = DEFAULT_REQUIREMENTS

                os.system(f'{cmd} > {name}')
                print(f'Сохранено в файл {name}')
        else:
            print(f'Такой команды {com} нет!')

        print('=' * 10, f'end {com}', '=' * 10, '\n')


if __name__ == '__main__':
    cli()
