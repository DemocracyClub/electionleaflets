.DEFAULT_GOAL := help

export SECRET_KEY?=badf00d
export DJANGO_SETTINGS_MODULE?=electionleaflets.settings
export APP_IS_BEHIND_CLOUDFRONT?=False

.PHONY: all
all: clean collectstatic lambda-layers/DependenciesLayer/requirements.txt thumbs/requirements.txt ## Rebuild everything this Makefile knows how to build

.PHONY: clean
clean: ## Delete any generated static asset or req.txt files and git-restore the rendered API documentation file
	rm -rf electionleaflets/static_files/ lambda-layers/DependenciesLayer/requirements.txt
	rm -rf thumbs/requirements.txt

.PHONY: collectstatic
collectstatic: ## Rebuild the static assets
	uv run python manage.py collectstatic --noinput --clear

lambda-layers/DependenciesLayer:
	mkdir -p $@

lambda-layers/DependenciesLayer/requirements.txt: pyproject.toml uv.lock lambda-layers/DependenciesLayer lambda-layers/DependenciesLayer ## Update the requirements.txt file used to build this Lambda function's DependenciesLayer
	uv export --no-hashes --no-dev > lambda-layers/DependenciesLayer/requirements.txt

thumbs/requirements.txt: thumbs/pyproject.toml uv.lock ## Update the requirements.txt file used to build this Lambda function's DependenciesLayer
	uv export --no-hashes --project thumbs  > thumbs/requirements.txt

.PHONY: help
# gratuitously adapted from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Display this help text
	@grep -E '^[-a-zA-Z0-9_/.]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%s\033[0m\n\t%s\n", $$1, $$2}'
