.PHONY: install run debug clean lint setup fclean build

install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

setup:
	virtualenv amazeing_env
	./amazeing_env/bin/pip install -r requirements.txt

fclean:clean
	@if [ "$$VIRTUAL_ENV" = "" ]; then \
		rm -rf amazeing_env; \
		echo "rm -rf amazeing_env"; \
	fi

build:
	python3 -m build