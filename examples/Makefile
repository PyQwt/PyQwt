html:
	python py2html.py *.py iqt/*.py qwt/*.py
	./PyCute --grab

free: html
	rm -rf ../../Free/examples/*
	mkdir -p ../../Free/examples/iqt
	mkdir -p ../../Free/examples/qwt
	cp *.py.html *.png ../../Free/examples
	cp iqt/*.py.html ../../Free/examples/iqt
	cp qwt/*.py.html ../../Free/examples/qwt
