// The SIP interface definition for mapped QValueList types, implemented:
//      QValueList<QRect>,
//      QValueList<QwtPickerMachine::Command>.
//
// Copyright (C) 2001-2003 Gerard Vermeulen
// Copyright (C) 2000 Mark Colclough
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
// FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
// details.
//
// You should have received a copy of the GNU General Public License along with
// PyQwt; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
// Suite 330, Boston, MA 02111-1307, USA.
//
// In addition, as a special exception, Gerard Vermeulen gives permission to
// link PyQwt with commercial, non-commercial or educational versions of Qt,
// PyQt and sip, and distribute PyQwt in this form, provided that equally
// powerful versions of Qt, PyQt and sip have been released under the terms
// of the GNU General Public License.
//
// If PyQwt is dynamically linked with commercial, non-commercial or
// educational versions of Qt, PyQt and sip, PyQwt becomes a free plug-in
// for a non-free program.


%MappedType QValueList<QRect>
{
%TypeHeaderCode
#include <qwt_dyngrid_layout.h>
%End

%ConvertFromTypeCode
    if (!sipCpp)
	return PyList_New(0);

    PyObject *l = PyList_New(sipCpp->count());

    if (0 == l)
	return 0;

    int i = 0;
    QValueListConstIterator<QRect> it;

    for (it = sipCpp->begin(); it != sipCpp->end(); ++it, ++i) {
	PyObject *object = sipBuildResult(0, "N",
                                          new QRect(*it),
                                          sipClass_QRect);
	if ((0 == object) || PyList_SetItem(l, i, object) < 0) {
	    Py_XDECREF(object);
	    Py_DECREF(l);
	    return 0;
	}
    }

    return l;
%End // %ConvertFromTypeCode

%ConvertToTypeCode
    if (0 == sipIsErr)
	return PyList_Check(sipPy);

    if (sipPy == Py_None) {
	*sipCppPtr = 0;
	return 0;
    }

    QValueList<QRect> *l = new QValueList<QRect>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
	int iserr = 0;

	QRect *t = reinterpret_cast<QRect *>(
            sipForceConvertTo_QRect(PyList_GET_ITEM(sipPy, i), &iserr));

	if (!t || iserr) {
	    *sipIsErr = 1;
	    delete l;
	    return 0;
	}

	l->append(*t);
    }

    *sipCppPtr = l;
    return 1;

%End // %ConvertToTypeCode
};

%MappedType QValueList<QwtPickerMachine::Command>
{
%TypeHeaderCode
#include <qvaluelist.h>
#include <qwt_picker_machine.h>
%End

%ConvertFromTypeCode
    if (!sipCpp)
        return PyList_New(0);

    PyObject *l = PyList_New(sipCpp->count());

    if (0 == l)
        return 0;

    for (int i = 0; i < int(sipCpp->count()); ++i)
        if (PyList_SetItem(l, i, PyInt_FromLong((long)(*sipCpp)[i])) < 0) {
            Py_DECREF(l);
            
            return 0;
        }

    return l;
%End // %ConvertFromTypeCode

%ConvertToTypeCode
    if (0 == sipIsErr)
        return PyList_Check(sipPy);

    if (sipPy == Py_None) {
        *sipCppPtr = 0;
        return 0;
    }

    QValueList<QwtPickerMachine::Command> *l =
        new QValueList<QwtPickerMachine::Command>;

    PyErr_Clear();

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
        l->append((QwtPickerMachine::Command)PyInt_AsLong(
                      PyList_GET_ITEM(sipPy, i)));
            
        if (0 != PyErr_Occurred()) {
            *sipIsErr = 1;
            delete l;
            return 0;
        }
    }

    *sipCppPtr = l;
    return 1;

%End // %ConvertToTypeCode
};


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
