# The environment variable QTDIR must be set 
PWD := $(shell pwd)
CXX := $(shell which ccache) $(CXX)

CVS-QWT := :pserver:anonymous@cvs.sourceforge.net:/cvsroot/qwt
CVS-DATE := "05 Oct 2003 23:59:59 GMT"
CVS-TABS := qwt-sources -name '*.h' -o -name '*.cpp' -o -name '*.pro'
CVS-QWT-SSH := :ext:gvermeul@cvs.sourceforge.net:/cvsroot/qwt

QWT-SOURCES := $(shell echo qwt-sources/include/*.h)
QWT-SOURCES += $(shell echo qwt-sources/src/*.{cpp,dox})

DIFFERS := -d 'qwt-sources/include qwt-sources/src'
DIFFERS += -s '.debug'

FREE := $(HOME)/Free

all:
	python setup.py build 2>&1 | tee LOG.all

doc: qwt-docs
	cp -pu setup_cfg_nt setup_cfg_posix Doc/pyqwt/
	(cd Doc; make doc)
	(cd examples; make html)

qwt-docs: qwt-sources/doc/html/index.html

qwt-sources/doc/html/index.html: $(QWT-SOURCES) qwt-sources/Doxyfile
	(cd qwt-sources; doxygen Doxyfile)

install:
	python setup.py install --record=LOG.record 2>&1 | tee LOG.install

# test: installs to a temporary directory
install-root:
	rm -rf tmp/usr; mkdir tmp
	python setup.py install --root=tmp 2>&1 | tee LOG.install-root

# force a complete rebuild
force:
	python setup.py build --force 2>&1 | tee LOG.force

.PHONY: dist qwt-sources

# build a tarball that 'mirrors' CVS
cvs: clean
	python DIFFER $(DIFFERS)
	python setup.py sdist -t MANIFEST.cvs 2>&1 | tee LOG.cvs

# build a distribution tarball
dist: clean doc
	python DIFFER $(DIFFERS)
	python setup.py sdist --formats=gztar 2>&1 | tee LOG.dist

# create a Qwt source tree compatible with PyQwt 
qwt-sources:
	rm -rf qwt-sources
	mkdir -p tmp
	if [ -e tmp/qwt ]; then \
	    (cd tmp; cvs -q -z3 -d $(CVS-QWT) update -D $(CVS-DATE) -d qwt); \
	else \
	    (cd tmp; cvs -q -z3 -d $(CVS-QWT) checkout -D $(CVS-DATE) qwt); \
	fi
	cp -vpur tmp/qwt qwt-sources
	find $(CVS-TABS) | xargs perl -pi -e 's|\t|    |g'
	python PATCHER

qwt-sources-ssh:
	rm -rf qwt-sources
	mkdir -p tmp
	if [ -e tmp/qwt ]; then \
	    (cd tmp; cvs -q -z3 -d $(CVS-QWT-SSH) update -d qwt); \
	else \
	    (cd tmp; cvs -q -z3 -d $(CVS-QWT-SSH) checkout qwt); \
	fi
	cp -vpur tmp/qwt qwt-sources
	find $(CVS-TABS) | xargs perl -pi -e 's|\t|    |g'
	python PATCHER
	(cd qwt-sources; qmake qwt.pro)
	(cd qwt-sources/examples; qmake examples.pro)

build-qwt:
	(cd qwt-sources; make CXX="$(CXX)")
	(cd qwt-sources/examples; make CXX="$(CXX)")

free:
	find . -name '*~' | xargs rm -f
	(cd Doc; make free)
	(cd examples; make free)
	cp dist/*.tar.gz $(FREE) 

diff:
	python DIFFER $(DIFFERS)

patch:
	cd qwt-sources; patch -p1 -b -z .canvas <$(PWD)/qwt.canvas.patch
	cd qwt-sources; patch -p1 -b -z .rich <$(PWD)/qwt.rich.patch

clean:
	(cd qwt-sources; make distclean)
	(cd qwt-sources/examples; make distclean)
	rm -f MANIFEST
	find . -name '*~' -o -name '.mappedfiles' | xargs rm -f
	rm -f *.pyc qwt/*.{cpp,h} qwt/__init__.py

distclean: clean
	(cd qwt-sources; qmake qwt.pro)
	(cd qwt-sources/examples; qmake examples)
	rm -rf build tmp/usr

