// The SIP interface definition for QwtCompass.
//
// Copyright (C) 2003 Gerard Vermeulen
//
// This file is part of PyQwt.
//
// PyQwt is free software; you can redistribute it and/or modify it under the
// terms of the GNU General Public License as published by the Free Software
// Foundation; either version 2 of the License, or (at your option) any later
// version.
//
// PyQwt is distributed in the hope that it will be useful, but WITHOUT ANY
// WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.  See the GNU  General Public License for more
// details.
//
// You should have received a copy of the GNU General Public License along with
// PyQwt; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
// Suite 330, Boston, MA 02111-1307, USA.
//
// In addition, as a special exception, Gerard Vermeulen gives permission to
// link PyQwt with commercial, non-commercial and educational versions of Qt,
// PyQt and sip, and distribute PyQwt in this form, provided that equally
// powerful versions of Qt, PyQt and sip have been released under the terms
// of the GNU General Public License.
//
// If PyQwt is linked with commercial, non-commercial and educational versions
// of Qt, PyQt and sip, Python scripts using PyQwt do not have to be released
// under the terms of the GNU General Public License. 
//
// You must obey the GNU General Public License in all respects for all of the
// code used other than Qt, PyQt and sip, including the Python scripts that are
// part of PyQwt.


%MappedType QMap<double, QString>
{
%HeaderCode
#include <qwt_compass.h>
%End

%ConvertFromTypeCode
    PyObject *d = PyDict_New();

    if (!sipCpp || !d)
	return d;

    const QMap<double, QString> map = *sipCpp;
    QMap<double, QString>::ConstIterator i;

    for (i=map.begin(); i!=map.end(); ++i) {
	PyObject *k, *v;
	if (0 == (k = PyFloat_FromDouble(i.key())) 
	    || 0 == (v = sipNewCppToSelf(new QString(i.data()),
					 sipClass_QString,
					 SIP_SIMPLE || SIP_PY_OWNED))
	    || 0 > PyDict_SetItem(d, k, v)) {
	    Py_XDECREF(k);
	    Py_XDECREF(v);
	    Py_DECREF(d);
	    return 0;
	}
    }

    return d;
%End

%ConvertToTypeCode
    if (0 == sipIsErr)
	return PyDict_Check(sipPy);

    QMap<double, QString> *map = new QMap<double, QString>;

    PyObject *k, *v;
    double ck;
    QString *cv;
    int i = 0;

    while (PyDict_Next(sipPy, &i, &k, &v)) {
	int iserr = 0;
	
	ck = PyFloat_AS_DOUBLE(k);
	sipConvertTo_QString(v, &cv, &iserr);
	
	if (iserr) {
	    *sipIsErr = 1;
	    delete map;
	    return 0;
	}
       
	map->insert(ck, *cv);
    }

    *sipCppPtr = map;
    
    return 1;
%End
};

class QwtCompass: QwtDial
{
%HeaderCode
#include <qwt_compass.h>
%End

public:
%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtCompass(QWidget * /TransferThis/ = 0, const char * = 0);

    void setRose(QwtCompassRose * /Transfer/);
    // dead code: const QwtCompassRose *rose() const;
    QwtCompassRose *rose();

    // dead code: const QMap<double, QString> &labelMap() const;
    QMap<double, QString> &labelMap();
    void setLabelMap(const QMap<double, QString> &);

protected:
    virtual QString scaleLabel(double) const;

    virtual void drawRose(QPainter *, const QPoint &,
			  int, double, QPalette::ColorGroup) const;

    virtual void drawScaleContents(QPainter *, const QPoint &, int) const;

    virtual void keyPressEvent(QKeyEvent *);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
