doc:
	(cd html/pyqwt; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	python tools/mkhowto --html --dir html/pyqwt --iconserver ../icons --image-type png pyqwt/pyqwt.tex
	(cd html/pyqwt; rm -f *.dat *.idx *.old *.pl *.gif)

free:
	rm -rf ../../Free/html
	mkdir -p ../../Free/html
	cp html/pyqwt/* ../../Free/html

