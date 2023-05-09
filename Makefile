COMPOSE := docker-compose -f docker/docker-compose.dev.yml

.PHONY: up stop down reload ps bash migrate logs
up:
	$(COMPOSE) up --build -d
	$(COMPOSE) exec api pip install -e src

stop:
	$(COMPOSE) stop

down:
	$(COMPOSE) down -v

reload:
	$(COMPOSE) down -v
	$(COMPOSE) up --build -d
	$(COMPOSE) exec api pip install -e src

ps:
	$(COMPOSE) ps

bash:
	$(COMPOSE) exec api bash

migrate:
	$(COMPOSE) exec api alembic upgrade head

logs:
	$(COMPOSE) logs -f --tail 100 api
