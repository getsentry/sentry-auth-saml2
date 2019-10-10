.PHONY: clean develop install-tests lint publish test

develop:
	pip install "pip==19.2.3"
	SENTRY_LIGHT_BUILD=1 pip install --no-use-pep517 -e ../sentry
	pip install .[tests]

lint:
	@echo "--> Linting python"
	flake8
	@echo ""

test:
	@echo "--> Running Python tests"
	py.test tests || exit 1
	@echo ""

publish:
	python setup.py sdist bdist_wheel upload

clean:
	rm -rf *.egg-info src/*.egg-info
	rm -rf dist build
