PYTHON = python3
VENV = . .venv/bin/activate


all: .venv
	$(VENV); $(PYTHON) bdfparse.py

.venv:
	$(PYTHON) -m venv .venv
	$(VENV); pip install -r requirements.txt

clean:
	$(RM) -r .venv
