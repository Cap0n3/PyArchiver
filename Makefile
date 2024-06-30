# to use run with args: make run ARGS="backup -h"
.PHONY: run
run:
	poetry run python main.py $(ARGS)

.PHONY: main_test
main_test:
	poetry run python Tests/main_tests.py

.PHONY: util_test
util_test:
	poetry run python Tests/backup_utility_tests.py
