FREE := $(HOME)/Free

SOURCES := \
	pyqwt/QwtArrayLongExample.txt \
	pyqwt/copyright.tex \
	pyqwt/numeric.example \
	pyqwt/pyqwt.tex \
	pyqwt/qplt.example \
	pyqwt/setup_cfg_nt \
	pyqwt/setup_cfg_posix


doc: $(SOURCES)
	if [ ! -e html/pyqwt ]; then mkdir html/pyqwt; fi
	(cd html/pyqwt; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	cp -pu html/icons/*.png html/pyqwt
	python tools/mkhowto --html --dir html/pyqwt \
	    --image-type png --favicon pyfav.png \
	    --up-link http://pyqwt.sourceforge.net --up-title "PyQwt Home" \
	    pyqwt/pyqwt.tex
	(cd html/pyqwt; rm -f *.dat *.idx *.old *.pl *.gif)
	python tools/nospam.py html/pyqwt/*.html
	date -u "+%Y-%m-%d %T" > doc

htdoc: doc $(SOURCES)
	if [ ! -e html/htdoc ]; then mkdir html/htdoc; fi
	(cd html/htdoc; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	cp -pur html/pyqwt/* html/htdoc
	python tools/sourceforge.py html/htdoc/*.html
	date -u "+%Y-%m-%d %T" > htdoc

free:
	mkdir -p $(FREE)/html
	cp -vpur html/pyqwt/* $(FREE)/html

