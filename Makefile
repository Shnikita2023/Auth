dev_up:
	docker compose up -d

dev_down:
	docker compose down --remove-orphans && docker volume prune -f && docker image rm fast_api_build

include .env.dev
export

run_server:
	uvicorn application.web.app:app --port 8002 --reload

dev_migration:
	alembic revision --autogenerate -m "Initial tables v1"

dev_upgrade:
	alembic upgrade head
