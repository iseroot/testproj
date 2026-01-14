db:
	docker compose up -d db

run-local:
	APP_ENV=local python -m uvicorn main:app --reload

run-docker:
	APP_ENV=docker python -m uvicorn main:app --reload


