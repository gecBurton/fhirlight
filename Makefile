format:
	poetry run ruff format
	poetry run ruff check --fix

migrations:
	poetry run python manage.py makemigrations

web:
	poetry run python manage.py runserver

clean:
	docker-compose down
	docker rm -f -v fhirlight_local_postgres_data
	docker-compose up -d
