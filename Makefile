format:
	poetry run ruff format
	poetry run ruff check --fix

migrations:
	rm -f api/migrations/0002_v1.py
	poetry run python manage.py makemigrations --name v1

web:
	poetry run python manage.py runserver

clean:
	docker-compose down
	docker volume rm -f fhirlight_local_postgres_data
	docker-compose up -d

test:
	poetry run pytest --cov=api --cov-report term-missing --cov-fail-under=99 tests

examples:
	poetry run python manage.py load_example_data
