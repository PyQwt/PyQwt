# GNU-Makefile for PyQwt

# Edit INCDIR and LIBDIR to suit your QwtPlot installation.
INCDIR := /usr/lib/qt3/include/qwt
LIBDIR := /usr/lib/qt3/lib

# To compile and link the Qwt-4.2.0 sources statically into PyQwt.
QWTDIR := /home/packer/RPM/BUILD/qwt-4.2.0

# Do not edit below this line, unless you know what you are doing.
CXX := $(shell which ccache) $(CXX)

CVS-QWT := :pserver:anonymous@cvs.sourceforge.net:/cvsroot/qwt
CVS-DATE := "8 Jan 2005 23:59:59 GMT"
CVS-TABS := qwt-sources -name '*.h' -o -name '*.cpp' -o -name '*.pro'
CVS-QWT-SSH := :ext:gvermeul@cvs.sourceforge.net:/cvsroot/qwt

QWT-SOURCES := $(shell echo qwt-sources/include/*.h)
QWT-SOURCES += $(shell echo qwt-sources/src/*.{cpp,dox})

DIFFERS := -d 'qwt-sources qwt-sources/include qwt-sources/src'
#DIFFERS += -s '.debug .autoscale'

FREE := $(HOME)/Free

all:
	(cd configure; \
	python configure.py -I $(INCDIR) -L $(LIBDIR) \
	&& $(MAKE) CXX="$(CXX)")
	(cd examples; ln -sf ../configure/iqt)
	(cd examples; ln -sf ../configure/qwt)

all-log: distclean
	(cd configure; \
	python configure.py -I $(INCDIR) -L $(LIBDIR) 2>&1 > ../LOG.all \
	&& $(MAKE) CXX="$(CXX)" 2>&1 >> ../LOG.all)
	(cd examples; ln -sf ../configure/iqt)
	(cd examples; ln -sf ../configure/qwt)

420-static:
4	(cd configure; \
	python configure.py -Q $(QWTDIR) \
	&& $(MAKE) CXX="$(CXX)")
	(cd examples; ln -sf ../configure/iqt)
	(cd examples; ln -sf ../configure/qwt)

420-static-log:
	(cd configure; \
	python configure.py -Q $(QWTDIR) 2>&1 > ../LOG.420-static \
	&& $(MAKE) CXX="$(CXX)" 2>&1 >> ../LOG.420-static)
	(cd examples; ln -sf ../configure/iqt)
	(cd examples; ln -sf ../configure/qwt)

cvs-static:
	(cd configure; \
	python configure.py -Q ../qwt-sources \
	&& $(MAKE) CXX="$(CXX)")
	(cd examples; ln -sf ../configure/iqt)
	(cd examples; ln -sf ../configure/qwt)

cvs-static-log:
	(cd configure; \
	python configure.py -Q ../qwt-sources  > ../LOG.cvs-static \
	&& $(MAKE) CXX="$(CXX)" 2>&1 >> ../LOG.cvs-static)
	(cd examples; ln -sf ../configure/iqt)
	(cd examples; ln -sf ../configure/qwt)

doc: qwt-docs
	cp -pu setup_cfg_nt setup_cfg_posix Doc/pyqwt/
	(cd Doc; make doc)
	(cd examples; make html)

qwt-docs: qwt-sources/doc/html/index.html

qwt-sources/doc/html/index.html: $(QWT-SOURCES) qwt-sources/Doxyfile
	(cd qwt-sources; doxygen Doxyfile)

install:
	(cd configure; make install)

.PHONY: dist qwt-sources

# build a tarball that 'mirrors' CVS
cvs: clean
	python DIFFER $(DIFFERS)
	python setup.py sdist -t MANIFEST.cvs 2>&1 | tee LOG.cvs

# build a distribution tarball
dist: cvs-static clean doc
	python DIFFER $(DIFFERS)
	unix2dos qwt-sources/msvc-qmake.bat 
	unix2dos qwt-sources/msvc-tmake.bat 
	python setup.py sdist --formats=gztar 2>&1 | tee LOG.dist

# create a Qwt source tree compatible with PyQwt 
qwt-sources:
	rm -rf qwt-sources
	mkdir -p tmp
	if [ -e tmp/qwt ]; then \
	    (cd tmp; cvs -q -d $(CVS-QWT) update -D $(CVS-DATE) -dP qwt); \
	else \
	    (cd tmp; cvs -q -d $(CVS-QWT) checkout -D $(CVS-DATE) qwt); \
	fi
	cp -vpur tmp/qwt qwt-sources
	find $(CVS-TABS) | xargs perl -pi -e 's|\t|    |g'
	python PATCHER

qwt-sources-ssh:
	rm -rf qwt-sources
	mkdir -p tmp
	if [ -e tmp/qwt ]; then \
	    (cd tmp; cvs -q -d $(CVS-QWT-SSH) update -dP qwt); \
	else \
	    (cd tmp; cvs -q -d $(CVS-QWT-SSH) checkout qwt); \
	fi
	cp -vpur tmp/qwt qwt-sources
	find $(CVS-TABS) | xargs perl -pi -e 's|\t|    |g'
	python PATCHER

makefiles:
	(cd qwt-sources; qmake qwt.pro)
	(cd qwt-sources/examples; qmake examples.pro)

build-qwt: makefiles
	(cd qwt-sources; make CXX="$(CXX)")
	(cd qwt-sources/examples; make CXX="$(CXX)")

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

distclean: clean makefiles
	(cd qwt-sources; make distclean)
	(cd qwt-sources/examples; make distclean)
	(cd qwt-sources; qmake qwt.pro)
	(cd qwt-sources/examples; qmake examples)
	rm -rf configure/iqt configure/qwt
