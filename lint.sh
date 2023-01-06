# TODO: add autopep8 here.
echo "Start autopep8 ..."
autopep8 . -r --in-place --aggressive --aggressive

# TODO: add autoflake here.
echo "Start autoflake ..."
autoflake app/. -r --in-place --remove-all-unused-imports --ignore-init-module-imports
autoflake tests/. -r --in-place --remove-all-unused-imports --ignore-init-module-imports
autoflake manage.py -r --in-place --remove-all-unused-imports --ignore-init-module-imports

# TODO: add isort here.
echo "Start isort ..."
isort . -rc

# TODO: add flake8 here.
echo "Start flake8 ..."
flake8