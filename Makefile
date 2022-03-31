.PHONY: clean test install lint

clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf  '.pytest_cache'
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf Pipfile.lock
	@rm -rf .tox
	@rm -rf venv/lib/python3.9/site-packages/bdex*.egg

test:
	tox

install:
	python3 setup.py install

lint:
	tox -e lint