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

stack-services:
	@docker stack services vossibility