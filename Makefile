.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help


test:		## Run tests with pytest
	pytest tests

clean:			## Clean cache, build files, coverage
	rm -rf build dist tplink_archer.egg-info .coverage .pytest_cache htmlcov build dist

coverage:		## Run tests with coverage
	coverage run --source=tplink_archer/ -m pytest tests

coverage-report:		## Show coverage report
	coverage report

coverage-html:		## Generate and serve html report
	coverage html && cd htmlcov/ && python -m http.server