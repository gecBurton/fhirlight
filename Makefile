format:
	poetry run ruff format
	poetry run ruff check --fix

migrations:
	poetry run python manage.py makemigrations

web:
	poetry run python manage.py runserver

clean:
	docker-compose down
	docker volume rm -f fhirlight_local_postgres_data
	docker-compose up -d

test:
	poetry run pytest tests
