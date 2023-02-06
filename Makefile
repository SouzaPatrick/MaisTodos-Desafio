## @ Project
.PHONY: install
install:
	@python generate_db.py


## @ Pre-commit
.PHONY: format
format:
	@pre-commit run --all-files
