.PHONY: clean test install lint install_deps

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
	@rm -rf results/*txt

test:
	tox

install:
	python3 setup.py install

install_deps:
	pip3 install -r requirements.txt

lint:
	tox -e lint