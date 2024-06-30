.PHONY: run
run:
	poetry run python main.py

.PHONY: test
test:
	poetry run python Tests/tests.py