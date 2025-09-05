.PHONY: up down logs ps bash migrate new-migration test scan ci-test lint format security-check

up:
	docker compose up -d

down:
	docker compose down 

logs:
	docker compose logs -f

ps:
	docker compose ps

bash:
	docker compose exec api bash 

migrate:
	docker compose exec api alembic revision --autogenerate -m "init" && \
	docker compose exec api alembic upgrade head 

new-migration:
	docker compose exec api alembic revision --autogenerate -m "init" && \
	docker compose exec api alembic upgrade head 

test:
	docker compose exec api python -m pip install -q requests && \
	API_URL=http://localhost:8000 docker compose exec -T api python -c "import requests; print('Smoke:', requests.get('http://localhost:8000/health').ok)"

ci-test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker compose -f docker-compose.test.yml down -v

scan:
	trivy image --severity HIGH,CRITICAL docker-e2e-api:latest || true

lint:
	docker compose exec api python -m pip install -q flake8 black isort && \
	docker compose exec api flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && \
	docker compose exec api black --check . && \
	docker compose exec api isort --check-only .

format:
	docker compose exec api python -m pip install -q black isort && \
	docker compose exec api black . && \
	docker compose exec api isort .

security-check:
	docker compose exec api python -m pip install -q safety && \
	docker compose exec api safety check

build:
	docker compose build

clean:
	docker compose down -v --remove-orphans
	docker system prune -f