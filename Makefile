# to use run with args: make run ARGS="backup -h"
.PHONY: run
run:
	poetry run python main.py $(ARGS)
	
.PHONY: test
test:
	poetry run python Tests/tests.py
