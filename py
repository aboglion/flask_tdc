ifeq ($(OS),Windows_NT)
    detected_OS := Windows
    PYTHON := venv\Scripts\python.exe
    VENV_ACTIVATE := venv\Scripts\activate
	clear_screen:=cls
else
    detected_OS := $(shell uname -s)
    PYTHON := venv/bin/python3
	pip := venv/bin/pip3
    VENV_ACTIVATE := venv/bin/activate
	clear_screen:=clear
	#"Usage: py <command>" && $(
endif




help:
	$(clear_screen)
	$(pipinstall)
	@echo "Available targets:"
	@echo "  "
	@echo "command            explanation"
	@echo "---------      ---------------------------"
	@echo "init    --> Initialize the virtual environment and install dependencies."
	@echo "active  --> Instructions for manually activating the virtual environment."
	@echo "install --> Install dependencies from requirements.txt."
	@echo "req     --> Generate a list of dependencies into requirements.txt."
	@echo "run-xxx --> Run the code (replace xxx with the name of your Python script without .py)."
	@echo "clean   --> Clean the virtual environment."
	@echo "exit    --> Deactivate the virtual environment."
	@echo "---------      ---------------------------"
	@echo ""
	@echo "Usage: make -f py <command>"
	@echo "* in linux\unix enter this command :"
	@echo "			alias py='make -f py'"
	@echo "			then Usage will be: py <command>"
	@echo ""


# Preparing the virtual environment
init:
	test -d venv || python3 -m venv venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(clear_screen)
	@echo "use this command to active the venv:"
	@echo "source $(VENV_ACTIVATE)"

# Operating the virtual environment
active:
	@echo "use this command to active the venv:"
	@echo "source $(VENV_ACTIVATE)"


# Installation of dependent files
install:
	@if [ -e requirements.txt ]; then \
		$(PYTHON) -m pip install -r requirements.txt; \
	else \
		echo "File does not exist."; \
	fi


# Creating a list of dependent
req:
	$(PYTHON) -m pip freeze > requirements.txt

# Running code
run:
	@if [ -z "$(filter-out run,$(MAKECMDGOALS))" ]; then \
        echo "Please specify a Python script to run using 'make -f py run my_script'"; \
    exit 1; \
    fi
	$(clear_screen)
	$(PYTHON) $(filter-out run,$(MAKECMDGOALS)).py

# Cleaning the virtual environment
clean:
ifeq ($(detected_OS),Windows)
	@del /F /Q venv
else
	@rm -rf venv
endif

exit:
	$(PYTHON) -m pip freeze > requirements.txt

ifeq ($(detected_OS),Windows)
	@echo "Deactivating virtual environment (Windows)"
	call $(VENV_ACTIVATE) && $(VENV_DEACTIVATE)
else
	@echo "Deactivating virtual environment (Unix)"
	$(clear_screen)
	@echo "use this command to deactivate the venv:"
	@echo "deactivate"
endif


