import argparse
import os
import sys

import inquirer

__version__ = '2.2.0'

# Имя этого файла
CURRENT_SCRIPT_NAME = os.path.basename(__file__)
# Список локалей
LOCALES = ['ru', 'en']
DEFAULT_REQUIREMENTS = 'requirements.txt'
DEFAULT_ADDR_PORT = '127.0.0.1:8000'
DEFAULT_DB_LABEL = 'default'

# Список команд
COMMANDS = {
    'create_local': f'Creating locales ({", ".join(LOCALES)})',
    'update_local': 'Updating and compiling locales',
    'collect_static': 'Assembling static files in the STATIC_ROOT folder',
    'make_migrations': 'Creating migrations',
    'make_migrations_app': 'Creating the first migration for the application',
    'make_empty_migrations_app': 'Create a blank migration for the application. '
                                 'Used to add default data to the database table',
    'migrate': f'Applying migrations [--db_label {DEFAULT_DB_LABEL}]',
    'create_superuser': 'Creating a user with superuser rights',
    'create_app': 'Creating an application',
    'run_server': f'Running a project on a port number, or ipaddr:port '
                  f'(default "{DEFAULT_ADDR_PORT}") [--port {DEFAULT_ADDR_PORT}]',
    'install_requirements': f'Install all dependencies for a project from a file (default "{DEFAULT_REQUIREMENTS}")',
    'print_requirements': 'Automatically generates all the necessary dependencies for the project, '
                          f'and also allows you to save this list to a file (default "{DEFAULT_REQUIREMENTS}") '
                          f'[--save_in_file {DEFAULT_REQUIREMENTS}]'
}


def print_requirements(file_name: str = None):
    cmd = 'pip freeze'
    if file_name:
        os.system(f'{cmd} > {file_name}')
        print(f'Saved to file {file_name}')
    else:
        os.system(f'{cmd}')


def cli():
    answers = {}
    args = None
    if len(sys.argv) > 1:
        # Список переданных аргументов начиная с 1 индекса
        # answers['commands'] = sys.argv[1:]
        parser = argparse.ArgumentParser(prog='django-command',
                                         description=f'CLI tool that allows you to run commonly used commands '
                                                     f'when developing Django projects.')
        parser.add_argument('commands', nargs='+', type=str, help=f'commands to run: {", ".join(COMMANDS.keys())}')
        parser.add_argument('-db', '--db_label', help='database label for "migrate" command')
        parser.add_argument('-s', '--save_in_file', help='save to file for "print_requirements" command')
        parser.add_argument('-p', '--port', default=DEFAULT_ADDR_PORT,
                            help='port number, or ipaddr:port for "run_server" command')
        parser.add_argument('-v', '--version', action='version', version=__version__)
        args = parser.parse_args()

        answers['commands'] = args.commands
    else:
        choices_commands = [
            ("{:<30} [{}] {}".format(key, index + 1, value), key) for index, (key, value) in enumerate(COMMANDS.items())
        ]
        questions = [
            inquirer.Checkbox(
                'commands',
                message="Select 1 or more commands",
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
            os.system('python manage.py collectstatic --noinput')
        elif com == 'make_migrations':
            os.system('python manage.py makemigrations')
        elif com == 'make_migrations_app':
            question = [
                inquirer.Text(
                    'app_name',
                    message='Enter the application name'
                )
            ]
            answer = inquirer.prompt(question)
            app_name = answer['app_name']

            if app_name != '':
                os.system(f'python manage.py makemigrations {app_name}')
            else:
                print('You must enter the name of the application!')
        elif com == 'make_empty_migrations_app':
            question = [
                inquirer.Text(
                    'app_name',
                    message='Enter the application name'
                )
            ]
            answer = inquirer.prompt(question)
            app_name = answer['app_name']

            if app_name != '':
                os.system(f'python manage.py makemigrations --empty {app_name}')
            else:
                print('You must enter the name of the application!')
        elif com == 'migrate':
            if args and args.db_label:
                db = args.db_label
            else:
                question = [
                    inquirer.Text(
                        'db',
                        message='Enter database label',
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
                    message='Enter the application name'
                )
            ]
            answer = inquirer.prompt(question)
            app_name = answer['app_name']

            if app_name != '':
                os.system(f'python manage.py startapp {app_name}')
            else:
                print('You must enter the name of the application!')
        elif com == 'run_server':
            if args and args.port:
                addr_port = args.port
            else:
                question = [
                    inquirer.Text(
                        'addr_port',
                        message='Enter port number, or ipaddr:port',
                        default=DEFAULT_ADDR_PORT
                    )
                ]
                answer = inquirer.prompt(question)
                addr_port = answer['addr_port']

            os.system(f'python manage.py runserver {addr_port}')
        elif com == 'install_requirements':
            question = [
                inquirer.Text(
                    'fileName',
                    message='Install dependencies from file',
                    default=DEFAULT_REQUIREMENTS
                )
            ]
            answer = inquirer.prompt(question)
            name = answer['fileName']
            if name == '':
                name = DEFAULT_REQUIREMENTS

            os.system(f'pip install -r {name}')
        elif com == 'print_requirements':
            print('List of dependencies for the project:')
            print_requirements()

            if args and args.save_in_file:
                print_requirements(args.save_in_file)
            else:
                question = [
                    inquirer.List(
                        'saveToFile',
                        message='Save this list to a file',
                        choices=['yes', 'no']
                    )
                ]
                answer = inquirer.prompt(question)
                if answer['saveToFile'] == 'yes':
                    question = [
                        inquirer.Text(
                            'fileName',
                            message='Enter file name',
                            default=DEFAULT_REQUIREMENTS
                        )
                    ]
                    answer = inquirer.prompt(question)
                    name = answer['fileName']
                    if name == '':
                        name = DEFAULT_REQUIREMENTS

                    print_requirements(name)
        else:
            print(f'There is no such "{com}" command!')

        print('=' * 10, f'end {com}', '=' * 10, '\n')


if __name__ == '__main__':
    cli()
