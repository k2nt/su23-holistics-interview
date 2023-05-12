SHELL := /bin/zsh


# HELP =================================================================================================================
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
.DEFAULT_GOAL := help


help: ## Display this help screen
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


run: ## Start application
	docker-compose up --detach --remove-orphans
.PHONY: run


run-build:  ## Start and rebuild application
	docker-compose up --detach --remove-orphans --build
.PHONY: run-build


down: ## Down microservices
	docker-compose down --remove-orphans
.PHONY: down
