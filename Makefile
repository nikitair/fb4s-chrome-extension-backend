runserver:
	python3 src/main.py

test:
	pytest src

test-coverage:
	pytest --cov=src

test-coverage-html:
	pytest --cov=src --cov-report=html

clear:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
