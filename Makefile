build-tar:
    pyproject-build --sdist
    # or python -m build --sdist

check-build-tar:
	twine check dist/*.tar.gz

build-and-check-tar: build-tar check-build-tar

upload-build-tar:
	twine upload --repository testpypi dist/*.tar.gz

build-exe:
    pyinstaller ./django_command/command.py --onefile