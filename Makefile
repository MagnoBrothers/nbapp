#--- SETUP --------------------------------#

SHELL := /bin/bash

# print env vars
# $(foreach v, $(.VARIABLES), $(info $(v) = $($(v))))

# get all positional arguments passed to make (except the first one, i.e the
# target) and passed them as arguments to the target
RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# ...and turn them into do-nothing targets
$(eval $(RUN_ARGS):;@:)

.PHONY: echo
echo:
	echo '-> ' $(RUN_ARGS)

.PHONY: format
format:
	isort nbapi/
	black nbapi/

.PHONY: api-coverage
api-coverage:
	coverage run -m pytest && coverage html && open htmlcov/index.html

#--- VSCODE --------------------------------#
.PHONY: vscode-install-extensions
vscode-install-extensions:
	. nbweb/scripts/vscode_install_extensions.sh nbweb/.vscode/extensions.txt

.PHONY: vscode-export-extensions
vscode-export-extensions:
	. nbweb/scripts/vscode_export_extensions.sh nbweb/.vscode/extensions.txt


#--- TEST --------------------------------#

.PHONY: run-test
run-test: stop clean
	docker compose -f docker/docker-compose.local.test.yml up -d api
	docker compose -f docker/docker-compose.local.test.yml logs -f

.PHONY: run-test-prod
run-test-prod: stop clean
	docker compose -f docker/docker-compose.prod.test.yml up -d api
	docker compose -f docker/docker-compose.prod.test.yml logs -f

.PHONY: run-e2e-test
run-e2e-test:
	docker compose -f docker/docker-compose.local.e2e.yml rm -f e2e
	docker compose -f docker/docker-compose.local.e2e.yml up -d
	docker compose -f docker/docker-compose.local.e2e.yml logs -f

.PHONY: restart-e2e-test
restart-e2e-test: stop build run-e2e-test


#--- LOCAL -------------------------------#
.PHONY: build
build:
	docker compose -f docker/docker-compose.local.yml build
	docker compose -f docker/docker-compose.local.test.yml build
	docker compose -f docker/docker-compose.local.e2e.yml build

.PHONY: build-no-cache
build-no-cache:
	docker compose -f docker/docker-compose.local.yml build --no-cache
	docker compose -f docker/docker-compose.local.test.yml build --no-cache

.PHONY: exec-sh
exec-sh:
	docker compose -f docker/docker-compose.local.yml exec api /bin/sh

.PHONY: run
run: run-services run-mc-setup

.PHONY: run-services
run-services:
	docker compose -f docker/docker-compose.local.yml up -d

.PHONY: run-mc-setup
run-mc-setup:
	docker compose -f docker/docker-compose.local.yml exec minio mc mb local/basins || true
	docker compose -f docker/docker-compose.local.yml exec minio mc anonymous set download local/basins || true
	docker compose -f docker/docker-compose.local.yml exec minio mc anonymous links local/basins || true

.PHONY: api-ipython
api-ipython: docker-run-other
	docker compose -f docker/docker-compose.local.yml exec -w /app/nbapi/ api ipython

.PHONY: logs
logs:
	docker compose -f docker/docker-compose.local.yml logs -f

.PHONY: logs-e2e
logs-e2e:
	docker compose -f docker/docker-compose.local.e2e.yml logs -f

.PHONY: logs-api
logs-api:
	docker compose -f docker/docker-compose.local.yml logs -f api

.PHONY: stop
stop:
	docker compose -f docker/docker-compose.local.test.yml down --remove-orphans || true
	docker compose -f docker/docker-compose.local.yml down --remove-orphans || true
	docker compose -f docker/docker-compose.prod.yml down --remove-orphans || true
	docker compose -f docker/docker-compose.local.e2e.yml down --remove-orphans || true

.PHONY: stop-api
stop-api:
	docker compose -f docker/docker-compose.local.yml rm -svf api

.PHONY: restart
restart: stop build run logs

#--- PRODUCTION --------------------------#

.PHONY: build-prod
build-prod:
	docker compose -f docker/docker-compose.prod.yml build

.PHONY: build-no-cache-prod
build-no-cache-prod:
	docker compose -f docker/docker-compose.prod.yml build --no-cache

.PHONY: exec-sh-prod
exec-sh-prod:
	docker compose -f docker/docker-compose.prod.yml exec api /bin/sh

.PHONY: run-prod
run-prod:
	docker compose -f docker/docker-compose.prod.yml up -d

.PHONY: api-ipython-prod
api-ipython-prod: docker-run-other
	docker compose -f docker/docker-compose.prod.yml exec -w /app/nbapi/ api ipython

.PHONY: logs-prod
logs-prod:
	docker compose -f docker/docker-compose.prod.yml logs -f

.PHONY: logs-api-prod
logs-api-prod:
	docker compose -f docker/docker-compose.prod.yml logs -f api

.PHONY: stop-prod
stop-prod:
	docker compose -f docker/docker-compose.prod.yml down

.PHONY: stop-api-prod
stop-api-prod:
	docker compose -f docker/docker-compose.prod.yml rm -svf api



#--- DB -------------------------------#

.PHONY: alembic-revision
alembic-revision:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config revision --autogenerate -m '$(RUN_ARGS)'

.PHONY: alembic-upgrade-head
alembic-upgrade-head:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config upgrade head

.PHONY: alembic-upgrade
alembic-upgrade:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config upgrade +1

.PHONY: alembic-downgrade
alembic-downgrade:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config downgrade -1

.PHONY: alembic-current
alembic-current:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config current

.PHONY: alembic-history
alembic-history:
	docker compose -f docker/docker-compose.local.yml exec api python -m alembic.config history

#--- TEARDOWN -----------------------------#

.PHONY: clean
clean: clean-files clean-volumes

.PHONY: clean-files
clean-files:
	find . \( -name __pycache__ -o -name "*.pyc" -o -name .pytest_cache -o -name .mypy_cache \) -exec rm -rf {} +

.PHONY: clean-volumes
clean-volumes:
	docker volume rm -f docker_local_postgres_data docker_local_test_postgres_data docker_local_minio_data docker_local_tusd_data docker_local_web_node_modules
	docker volume rm -f docker_prod_postgres_data docker_prod_test_postgres_data
