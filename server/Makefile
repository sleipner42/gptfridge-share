start-dev:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml up -d --build

start-dev-debug:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml -f compose.dev.debug.yaml up -d --build

start-dev-backend:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml up --build -d backend

dev-migrate:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml exec backend bash -c 'alembic upgrade head'

dev-seed:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml exec backend bash -c 'python seed.py'

log-dev-backend:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml logs -f backend

run-bash-backend:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml run backend bash

restart-dev:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml stop; docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml up -d

stop:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml stop

exec_dev:
	docker-compose -p gptfridge -f compose.yaml -f compose.dev.yaml exec backend bash
