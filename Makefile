PYTHON = python3
VENV = . .venv/bin/activate


all: .venv
	$(VENV); PYTHONPATH=$(PWD) $(PYTHON) generate.py ter-u16n.bdf

.venv:
	$(PYTHON) -m venv .venv
	$(VENV); pip install -r requirements.txt

mypy:
	PYTHONPATH=$(PWD) mypy --strict .

clean:
	$(RM) -r .venv */__pycache__ .mypy_cache *.bdf
