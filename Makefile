.PHONY: run clean install test

run:
	PYTHONDONTWRITEBYTECODE=1 python3 -B app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf data/sessions

install:
	pip3 install -r requirements.txt

test:
	PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests
