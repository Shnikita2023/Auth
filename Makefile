dev_up:
	docker compose up -d

dev_down:
	docker compose down --remove-orphans && docker volume prune -f && docker image rm fast_api_build

include .env
export

run_server:
	uvicorn application.web.app:main_app --port 8000 --reload

dev_migration:
	alembic revision --autogenerate -m "Initial tables v3"

dev_upgrade:
	alembic upgrade head

test_up:
	docker compose -f docker-compose-dev.yaml up -d

test_down:
	docker compose -f docker-compose-dev.yaml down --remove-orphans && docker volume prune -f

test:
	pytest application/tests/web -v

deploy_server:
	docker build . -t kubernetes-fastapi-app-img
	docker tag kubernetes-fastapi-app-img nikitapython/fast_api:v3
	docker push nikitapython/fast_api:v3

