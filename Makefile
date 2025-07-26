.PHONY: all setup venv run up down init-migrate migrate migrate-up migrate-down migrate-new wait-for-postgres db-reset alembic-reset hard-reset start-services

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
PIP=${VENV_NAME}/bin/pip
ALEMBIC=alembic

DOCKER_COMPOSE=docker-compose
DOCKER=docker
FLIGHT_APP=flight-backend

build:
	@echo "Starting application..."
	@$(DOCKER_COMPOSE) up -d --build

up:
	@$(DOCKER_COMPOSE) up -d && docker attach $(FLIGHT_APP)

logs:
	@$(DOCKER) logs $(FLIGHT_APP)

it-back:
	@$(DOCKER) exec -it $(FLIGHT_APP)

init-migrate:
	@$(DOCKER) exec -it $(FLIGHT_APP) $(ALEMBIC) init

migrate:
	@$(DOCKER) exec -it $(FLIGHT_APP) $(ALEMBIC) upgrade head

migrate-up: @$(DOCKER) exec -it $(FLIGHT_APP) $(ALEMBIC) migrate

migrate-down:
	@$(ALEMBIC) downgrade -1