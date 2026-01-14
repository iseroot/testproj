run:
	python -m uvicorn main:app --reload

db:
	docker compose up -d db
