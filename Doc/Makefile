FREE := $(HOME)/Free

SOURCES := \
	pyqwt/copyright.tex \
	pyqwt/numeric.example \
	pyqwt/pyqwt.tex \
	pyqwt/qplt.example \
	pyqwt/setup_cfg_nt \
	pyqwt/setup_cfg_posix


doc: $(SOURCES)
	(cd html/pyqwt; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	cp -pu html/icons/*.png html/pyqwt
	python tools/mkhowto --html --dir html/pyqwt \
	    --image-type png --favicon pyfav.png \
	    --up-link http://pyqwt.sourceforge.net --up-title "PyQwt Home" \
	    pyqwt/pyqwt.tex
	(cd html/pyqwt; rm -f *.dat *.idx *.old *.pl *.gif)
	date -u "+%Y-%m-%d %T" > doc

htdoc: $(SOURCES)
	(cd html/htdoc; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	cp -pu html/icons/*.png html/htdoc
	python tools/mkhowto --html --dir html/htdoc \
	    --image-type png --favicon pyfav.png \
	    --up-link ../index.html --up-title "PyQwt Home" \
	    pyqwt/pyqwt.tex
	(cd html/htdoc; rm -f *.dat *.idx *.old *.pl *.gif)
	date -u "+%Y-%m-%d %T" > htdoc

free:
	mkdir -p $(FREE)/html
	cp -vpur html/pyqwt/* $(FREE)/html

