# GNU-Makefile for PyQwt

# Edit INCDIR and LIBDIR to suit your QwtPlot installation.
INCDIR := /usr/lib/qt3/include/qwt
LIBDIR := /usr/lib/qt3/lib

# To compile and link the Qwt-4.2.0 sources statically into PyQwt.
QWTDIR := ../qwt-4.2.0

# Do not edit below this line, unless you know what you are doing.
CXX := $(shell which ccache) $(CXX)

CVS-QWT := :pserver:anonymous@cvs.sourceforge.net:/cvsroot/qwt
CVS-DATE := "29 Jan 2005 23:59:59 GMT"
CVS-QWT-SSH := :ext:gvermeul@cvs.sourceforge.net:/cvsroot/qwt

QWT420-SOURCES := $(shell echo qwt-4.2.0/include/*.h)
QWT420-SOURCES += $(shell echo qwt-4.2.0/src/*.{cpp,dox})
QWTCVS-SOURCES := $(shell echo qwt-cvs/include/*.h)
QWTCVS-SOURCES += $(shell echo qwt-cvs/src/*.{cpp,dox})

#DIFFERS := -d 'qwt-sources qwt-sources/include qwt-sources/src'
#DIFFERS += -s '.debug .autoscale'

FREE := $(HOME)/Free


# Build and link PyQwt against a shared Qwt library.
all: symlinks
	(cd configure; \
	python configure.py -I $(INCDIR) -L $(LIBDIR) \
	&& $(MAKE) CXX="$(CXX)")

# Build and link PyQwt against a shared Qwt library
# and write LOG.all.
all-log: distclean symlinks
	(cd configure; \
	python configure.py -I $(INCDIR) -L $(LIBDIR) 2>&1 > ../LOG.all \
	&& $(MAKE) CXX="$(CXX)" 2>&1 >> ../LOG.all)

# Build and link PyQwt including the source tree of Qwt-4.2.0.
all-static: symlinks
	(cd configure; \
	python configure.py -Q $(QWTDIR) \
	&& $(MAKE) CXX="$(CXX)")

# Build and link PyQwt including the source tree of Qwt-4.2.0
# and write LOG.all-static.
all-static-log: symlinks
	(cd configure; \
	python configure.py -Q $(QWTDIR) 2>&1 > ../LOG.all-static \
	&& $(MAKE) CXX="$(CXX)" 2>&1 >> ../LOG.all-static)

# Build and link PyQwt including the CVS tree of Qwt-4.2.0.
cvs-static: symlinks
	(cd configure; \
	python configure.py -Q ../qwt-cvs \
	&& $(MAKE) CXX="$(CXX)")

# build and link PyQwt including the CVS tree of Qwt-4.2.0
# and write LOG.cvs-static
cvs-static-log: symlinks
	(cd configure; \
	python configure.py -Q ../qwt-cvs 2>&1 > ../LOG.cvs-static \
	&& $(MAKE) CXX="$(CXX)" 2>&1 >> ../LOG.cvs-static)

# The symlinks work only for SIP >= 4.0.
symlinks:
	(cd iqt; ln -sf ../configure/iqt/_iqt.so)
	(cd qwt; ln -sf ../configure/qwt/_qwt.so)
	(cd examples; ln -sf ../configure/iqt; ln -sf ../configure/qwt)

# Documentation
doc: qwt-docs
	cp -pu setup_cfg_nt setup_cfg_posix Doc/pyqwt/
	(cd Doc; make doc)
	(cd examples; make html)

qwt-docs: qwt-4.2.0/doc/html/index.html qwt-cvs/doc/html/index.html

qwt-4.2.0/doc/html/index.html: $(QWT420-SOURCES) qwt-4.2.0/Doxyfile
	(cd qwt-cvs; doxygen Doxyfile)

qwt-cvs/doc/html/index.html: $(QWTCVS-SOURCES) qwt-cvs/Doxyfile
	(cd qwt-cvs; doxygen Doxyfile)

# Installation
install:
	(cd configure; make install)

.PHONY: dist qwt-cvs

# build a tarball that 'mirrors' CVS
cvs: clean
	python DIFFER $(DIFFERS)
	python setup.py sdist -t MANIFEST.cvs 2>&1 | tee LOG.cvs

# build a distribution tarball
dist: 420-static doc clean
	python DIFFER $(DIFFERS)
	python setup.py sdist --formats=gztar 2>&1 | tee LOG.dist

# get a (patched?) Qwt tree from CVS
qwt-cvs:
	rm -rf qwt-cvs
	mkdir -p tmp
	if [ -e tmp/qwt ]; then \
	    (cd tmp; cvs -q -d $(CVS-QWT) update -D $(CVS-DATE) -dP qwt); \
	else \
	    (cd tmp; cvs -q -d $(CVS-QWT) checkout -D $(CVS-DATE) qwt); \
	fi
	cp -vpur tmp/qwt qwt-cvs
	python untabify.py -t 4 qwt-cvs .cpp .h .pro
	python PATCHER

# get a (patched?) Qwt tree from CVS
qwt-cvs-ssh:
	rm -rf qwt-cvs
	mkdir -p tmp
	if [ -e tmp/qwt ]; then \
	    (cd tmp; cvs -q -d $(CVS-QWT-SSH) update -dP qwt); \
	else \
	    (cd tmp; cvs -q -d $(CVS-QWT-SSH) checkout qwt); \
	fi
	cp -vpur tmp/qwt qwt-cvs
	python untabify.py -t 4 qwt-cvs .cpp .h .pro
	python PATCHER

makefiles:
	(cd qwt-4.2.0; qmake qwt.pro)
	(cd qwt-4.2.0/examples; qmake examples.pro)

build-qwt: makefiles
	(cd qwt-4.2.0; make CXX="$(CXX)")
	(cd qwt-4.2.0/examples; make CXX="$(CXX)")

free:
	find . -name '*~' | xargs rm -f
	(cd Doc; make free)
	(cd examples; make free)
	cp dist/*.tar.gz $(FREE) 

diff:
	python DIFFER $(DIFFERS)


clean: makefiles
	find . -name '*~' -o -name '.mappedfiles' | xargs rm -f
	rm -f *.pyc qwt/*.{cpp,h} qwt/_qwt.py
	rm -f iqt/_iqt.so qwt/_qwt.so  

distclean: clean makefiles
	(cd qwt-4.2.0; make distclean)
	(cd qwt-4.2.0/examples; make distclean)
	(cd qwt-4.2.0; qmake qwt.pro)
	(cd qwt-4.2.0/examples; qmake examples)
	rm -rf configure/iqt configure/qwt

# EOF
