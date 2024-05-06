# django-command

Django-command is a command line tool that allows you to run commonly used commands in development
Django projects.

### Installation

```shell
pip install django-command
```

### Launch

There are several ways to run commands:

1. In the terminal, type django-command, after which a list of available commands for execution will appear, check
   through
   space which commands to execute. The marked commands will be executed in the order they were selected.
   ```shell
   (venv) PS .\> django-command
   [?] Select 1 or more commands:
    > [ ] create_local                   [1] Creating locales (ru, en)
      [ ] update_local                   [2] Updating and compiling locales
      [ ] collect_static                 [3] Assembling static files in the STATIC_ROOT folder
      [ ] make_migrations                [4] Creating migrations
      [ ] make_migrations_app            [5] Creating the first migration for the application
      [ ] make_empty_migrations_app      [6] Create a blank migration for the application. Used to add default data to the database table
      [ ] migrate                        [7] Applying migrations [--db_label default]
      [ ] create_superuser               [8] Creating a user with superuser rights
      [ ] create_app                     [9] Creating an application
      [ ] run_server                     [10] Running a project on a port number, or ipaddr:port (default "127.0.0.1:8000") [--port 127.0.0.1:8000]
      [ ] install_requirements           [11] Install all dependencies for a project from a file (default "requirements.txt")
      [ ] print_requirements             [12] Automatically generates all the necessary dependencies for the project, and also allows you to save this list to a file (default "requirements.txt") [--save_in_file requirements.txt]
   ```

2. Commands can be executed by their name or number.
    ```shell
    django-command make_migrations migrate
    # or with argument
    django-command make_migrations migrate -db default
    # or
    django-command 4 7
    ```

#### List of commands and arguments

 ```shell
(venv) PS .\> django-command -h
usage: django-command [-h] [-db DB_LABEL] [-s SAVE_IN_FILE] [-p PORT] [-v] commands [commands ...]   

CLI tool that allows you to run commonly used commands when developing Django projects.              

positional arguments:                                                                                
  commands              commands to run: create_local, update_local, collect_static, make_migrations,
                        make_migrations_app, make_empty_migrations_app, migrate, create_superuser,   
                        create_app, run_server, install_requirements, print_requirements             

optional arguments:
  -h, --help            show this help message and exit
  -db DB_LABEL, --db_label DB_LABEL
                        database label for "migrate" command
  -s SAVE_IN_FILE, --save_in_file SAVE_IN_FILE
                        save to file for "print_requirements" command
  -p PORT, --port PORT  port number, or ipaddr:port for "run_server" command
  -v, --version         show program's version number and exit
```