.PHONY: help
help:     ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: clean
clean:    ## Clean your development environment
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type f -name '*.pyc' -exec rm -r {} \+
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage

.PHONY: test
test:     ## Run tests in docker container
	@docker-compose run app bash -c "\
	    set -x && \
	    DEBUG=0 coverage run --source . -m py.test -sv --html=htmltest/report.html --self-contained-html -c tests/pytest.ini && \
	    coverage report && \
	    coverage html \
	"

.PHONY: lint
lint:     ## Apply all linting possible
	@docker-compose run --no-deps app bash -c "\
	    set -x && \
	    pylint --rcfile pylintrc -r n funcrowd && \
	    pycodestyle funcrowd \
	"

.PHONY: deps
deps:     ## Diagnose outdated dependencies
	@docker-compose run --no-deps app bash -c "set -x && ./bin/check-requirements.py -r requirements.txt"

.PHONY: up
up:       ## Run whole project in docker environment with all its services
	docker-compose up

.PHONY: build
build:    ## Build and run whole project in docker environment with all its services
	docker-compose up --build

.PHONY: makemigrations
makemigrations:    ## Build and run whole project in docker environment with all its services
	docker-compose exec app ./manage.py makemigrations funcrowd

.PHONY: migrate
migrate:    ## Build and run whole project in docker environment with all its services
	docker-compose exec app ./manage.py migrate
