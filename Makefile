COMPOSE := docker-compose -f docker/docker-compose.dev.yml

.PHONY: up stop down reload ps bash migrate logs
up:
	$(COMPOSE) up --build -d
	${COMPOSE} exec mongodb mongorestore /backup

stop:
	$(COMPOSE) stop

down:
	$(COMPOSE) exec mongodb mongodump --out /backup
	$(COMPOSE) down -v

reload:
	$(COMPOSE) exec mongodb mongodump --out /backup
	$(COMPOSE) down -v
	$(COMPOSE) up --build -d
	${COMPOSE} exec mongodb mongorestore /backup

db-save:
	$(COMPOSE) exec mongodb mongodump --out /backup

ps:
	$(COMPOSE) ps

bash:
	$(COMPOSE) exec api bash

logs:
	$(COMPOSE) logs -f --tail 100 api
