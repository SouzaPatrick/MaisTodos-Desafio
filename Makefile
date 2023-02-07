## @ Project
.PHONY: install up generate_db down
install: generate_db up # Generate the backend image and upload ALL containers in the project

up: ## Starts ALL containers in the project
	@docker-compose up -d --build

down: ## Stop ALL containers in the project
	@docker-compose down

generate_db:
	@python generate_db.py


## @ Pre-commit
.PHONY: format
format:
	@pre-commit run --all-files
