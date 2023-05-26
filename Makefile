COMPOSE := docker-compose -f docker/docker-compose.dev.yml

.PHONY: up stop down reload ps bash migrate logs
up:
	$(COMPOSE) up --build -d

stop:
	$(COMPOSE) stop

down:
	$(COMPOSE) down -v

reload:
	$(COMPOSE) down -v
	$(COMPOSE) up --build -d

ps:
	$(COMPOSE) ps

bash:
	$(COMPOSE) exec api bash

logs:
	$(COMPOSE) logs -f --tail 100 api
