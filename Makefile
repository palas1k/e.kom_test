include .env
RUN_PYTHON=PYTHONPATH=./ poetry run

dev:
	docker compose up --build -d

test:
	pytest .