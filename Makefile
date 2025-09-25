PYTHON = python3
VENV = . .venv/bin/activate

prefix = /usr
datadir = $(prefix)/share
fontsdir = $(datadir)/fonts
sysconfdir = /etc

TARBALL = xfonts-terminus_4.48.orig.tar.gz
TARBALL_URI = http://ftp.cz.debian.org/debian/pool/main/x/xfonts-terminus/$(TARBALL)
TARBALL_DIR = xfonts-terminus-4.48.orig

SIZES = 12 14 16 18 20 22 24 28 32

ORIG_REGULAR = $(patsubst %, orig/ter-u%n.bdf, $(SIZES))
ORIG_BOLD = $(patsubst %, orig/ter-u%b.bdf, $(SIZES))
ORIG_FONTS = $(ORIG_REGULAR) $(ORIG_BOLD)

FONTS_REGULAR = $(patsubst %, ter-u%n.bdf, $(SIZES))
FONTS_BOLD = $(patsubst %, ter-u%b.bdf, $(SIZES))

GLYPHS = $(shell find glyph -name '*.png')


all: .venv ter-iast-regular.otb ter-iast-bold.otb

%.bdf: $(GLYPHS) $(ORIG_FONTS)
	$(VENV); PYTHONPATH=$(shell pwd) $(PYTHON) bin/generate.py

%.png:
	$(VENV); PYTHONPATH=$(shell pwd) $(PYTHON) bin/dump.py $*

$(TARBALL):
	$(QUIET_GET) wget $(TARBALL_URI) -qO$@

$(ORIG_FONTS): $(TARBALL)
	@mkdir -p orig
	$(QUIET_UNTAR) tar --xform="s/$(TARBALL_DIR)/orig/"	\
		-xf $(TARBALL) $(TARBALL_DIR)/$(notdir $@) && touch $@

ter-iast-regular.otb: $(FONTS_REGULAR)
	$(QUIET_GEN) fontforge -quiet -lang=ff -script fontmerge.ff $@ $^ 2>/dev/null

ter-iast-bold.otb: $(FONTS_BOLD)
	$(QUIET_GEN) fontforge -quiet -lang=ff -script fontmerge.ff $@ $^ 2>/dev/null

.venv:
	$(PYTHON) -m venv .venv
	$(VENV); pip install -r requirements.txt

mypy:
	PYTHONPATH=$(shell pwd) mypy --strict .

install:
	install -m 0755 -d $(fontsdir)/opentype/terminus-iast $(sysconfdir)/fonts/conf.d
	install -m 0644 *.otb $(fontsdir)/opentype/terminus-iast
	install -m 0644 50-enable-terminus-iast.conf $(sysconfdir)/fonts/conf.d

uninstall:
	$(RM) -r $(fontsdir)/opentype/terminus-iast

enable:
	fc-cache -fv

clean:
	$(RM) -r .venv */__pycache__ .mypy_cache orig
	$(RM) $(TARBALL) *.bdf *.png *.otb

ifndef V
QUIET_GEN   = @echo "  GEN    $@";
QUIET_GET   = @echo "  GET    $@";
QUIET_UNTAR = @echo "  UNTAR  $@";
endif
