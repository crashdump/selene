build:
	docker build -t selene .

run:
	poetry run

test:
	poetry run pytest

lint:
	find . -type f -name "*.py" | xargs pylint