FREE := $(HOME)/Free

html:
	python py2html.py *.py iqt/*.py qwt/*.py
	./PyCute --grab

free: html
	rm -rf $(FREE)/examples/*
	mkdir -p $(FREE)/examples/iqt
	mkdir -p $(FREE)/examples/qwt
	cp *.py.html *.png $(FREE)/examples
	cp iqt/*.py.html $(FREE)/examples/iqt
	cp qwt/*.py.html $(FREE)/examples/qwt
