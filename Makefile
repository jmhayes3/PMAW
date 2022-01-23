.PHONY:	test lint install clean uninstall
test:
	pytest tests/ -v
lint:
	flake8 --exit-zero pmaw
install:
	pipenv run python setup.py install
clean:
	rm -rf build dist pmaw.egg-info
uninstall:
	pipenv run pip uninstall -y pmaw
