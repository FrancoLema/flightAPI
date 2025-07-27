.PHONY: all setup venv run up down init-migrate migrate migrate-up migrate-down migrate-new wait-for-postgres db-reset alembic-reset hard-reset start-services

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python
PIP=${VENV_NAME}/bin/pip
ALEMBIC=alembic

DOCKER_COMPOSE=docker-compose
DOCKER=docker
FLIGHT_APP=flight-backend

up:
	@$(DOCKER_COMPOSE) up -d && docker attach $(FLIGHT_APP)

logs:
	@$(DOCKER) logs $(FLIGHT_APP)

it-back:
	@$(DOCKER) exec -it $(FLIGHT_APP)


migrate:
	@$(DOCKER) exec -it $(FLIGHT_APP) $(ALEMBIC) upgrade head

test:
	@$(DOCKER) exec -it $(FLIGHT_APP) pytest -v

load-data:
	@$(DOCKER) exec -it $(FLIGHT_APP) python data/load_data.py