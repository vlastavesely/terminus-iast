PYTHON = python3
VENV = . .venv/bin/activate

TARBALL = xfonts-terminus_4.48.orig.tar.gz
TARBALL_URI = http://ftp.cz.debian.org/debian/pool/main/x/xfonts-terminus/$(TARBALL)
TARBALL_DIR = xfonts-terminus-4.48.orig

SIZES = 12 14 16 18 20 22 24 28 32

ORIG_REGULAR = $(patsubst %, orig/ter-u%n.bdf, $(SIZES))
ORIG_BOLD = $(patsubst %, orig/ter-u%b.bdf, $(SIZES))
ORIG_FONTS = $(ORIG_REGULAR) $(ORIG_BOLD)

FONTS_REGULAR = $(patsubst %, ter-u%n.bdf, $(SIZES))
FONTS_BOLD = $(patsubst %, ter-u%b.bdf, $(SIZES))


all: .venv $(ORIG_FONTS)
	$(VENV); PYTHONPATH=$(PWD) $(PYTHON) bin/generate.py

%.png:
	$(VENV); PYTHONPATH=$(PWD) $(PYTHON) bin/dump.py $*

$(TARBALL):
	$(QUIET_GET) wget $(TARBALL_URI) -qO$@

$(ORIG_FONTS): $(TARBALL)
	@mkdir -p orig
	$(QUIET_UNTAR) tar --xform="s/$(TARBALL_DIR)/orig/"	\
		-xf $(TARBALL) $(TARBALL_DIR)/$(notdir $@) && touch $@

.venv:
	$(PYTHON) -m venv .venv
	$(VENV); pip install -r requirements.txt

mypy:
	PYTHONPATH=$(PWD) mypy --strict .

clean:
	$(RM) -r .venv */__pycache__ .mypy_cache
	$(RM) $(TARBALL) *.bdf *.png orig

ifndef V
QUIET_GEN   = @echo "  GEN    $@";
QUIET_GET   = @echo "  GET    $@";
QUIET_UNTAR = @echo "  UNTAR  $@";
endif
