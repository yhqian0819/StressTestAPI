run:
	@cd docker; docker-compose up

run-build:
	@cd docker; docker-compose up --build

run-build-force-recreate:
	@cd docker; docker-compose up --build --force-recreate --renew-anon-volumes mysql

build-docker:
	@docker build -t rinha-api .

stack-init:
	@docker swarm init

stack-run:
	@docker stack deploy -c docker/docker-compose.yml vossibility

stack-ps:
	@docker stack ps vossibility

stack-down:
	@docker stack down vossibility

logs-app1:
	@docker service logs vossibility_app1 --follow

logs-app2:
	@docker service logs vossibility_app2 --follow

logs-web:
	@docker service logs vossibility_web --follow

logs-mysql:
	@docker service logs vossibility_mysql --follow

monitor-uwsgi-app1:
	@uwsgitop http://127.0.0.1:3031

monitor-uwsgi-app2:
	@uwsgitop http://127.0.0.1:3032

docker-exec-app1:
	@docker exec -ti vossibility_app1.1.$(shell docker service ps -f 'name=vossibility_app1.1' vossibility_app1 -q --no-trunc | head -n1) /bin/bash

docker-exec-app2:
	@docker exec -ti vossibility_app2.1.$(shell docker service ps -f 'name=vossibility_app2.1' vossibility_app2 -q --no-trunc | head -n1) /bin/bash

dokcer-exec-web:
	@docker exec -ti vossibility_web.1.$(shell docker service ps -f 'name=vossibility_web.1' vossibility_web -q --no-trunc | head -n1) /bin/bash

docker-exec-mysql:
	@docker exec -ti vossibility_mysql.1.$(shell docker service ps -f 'name=vossibility_mysql.1' vossibility_mysql -q --no-trunc | head -n1) /bin/bash