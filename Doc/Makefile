doc: pyqwt/pyqwt.tex
	(cd html/pyqwt; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	cp -pu html/icons/*.png html/pyqwt
	python tools/mkhowto --html --dir html/pyqwt \
	    --image-type png --favicon pyfav.png \
	    --up-link http://pyqwt.sourceforge.net --up-title "PyQwt Home" \
	    pyqwt/pyqwt.tex
	(cd html/pyqwt; rm -f *.dat *.idx *.old *.pl *.gif)
	date -u "+%Y-%m-%d %T" > doc

htdoc: pyqwt/pyqwt.tex
	(cd html/htdoc; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	cp -pu html/icons/*.png html/htdoc
	python tools/mkhowto --html --dir html/htdoc \
	    --image-type png --favicon pyfav.png \
	    --up-link ../index.html --up-title "PyQwt Home" \
	    pyqwt/pyqwt.tex
	(cd html/htdoc; rm -f *.dat *.idx *.old *.pl *.gif)
	date -u "+%Y-%m-%d %T" > htdoc

free:
	rm -rf ../../Free/html
	mkdir -p ../../Free/html
	cp html/pyqwt/* ../../Free/html

