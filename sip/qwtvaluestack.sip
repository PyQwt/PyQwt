// The SIP interface definition for QValueStack types, implemented:
//      QValueStack<QwtDoubleRect>.
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


%MappedType QValueStack<QwtDoubleRect>
{
%TypeHeaderCode
#include <qwt_array.h>
#include <qvaluestack.h>
%End

%ConvertFromTypeCode
    if (!sipCpp)
        return PyList_New(0);
    
    // FIXME: works because QValueStack is derived from QList 
    PyObject *l = PyList_New(sipCpp->count());;

    if (0 == l)
        return 0;

    int i = 0;
    QValueListConstIterator<QwtDoubleRect> it;

    for (it = sipCpp->begin(); it != sipCpp->end(); ++it, ++i) {
	PyObject *object = sipBuildResult(0, "N",
                                          new QwtDoubleRect(*it),
                                          sipClass_QwtDoubleRect);
        
        if ((0 == object) || PyList_SetItem(l, i, object) < 0) {
	    Py_XDECREF(object);
	    Py_DECREF(l);
	    return 0;
	}
    }
    
    return l;
%End

%ConvertToTypeCode
    if (0 == sipIsErr)
        return PyList_Check(sipPy);

    // FIXME: can we use the fact that QValueStack is derived from QList? 
    QValueStack<QwtDoubleRect> *s = new QValueStack<QwtDoubleRect>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
	int iserr = 0;
        
	QwtDoubleRect *t = reinterpret_cast<QwtDoubleRect *>(
            sipForceConvertTo_QwtDoubleRect(
                PyList_GET_ITEM(sipPy, i), &iserr));

        if (!t || iserr) {
            delete s;
            *sipIsErr = 1;
            
            return 0;
        }
        s->push(*t);
    }

    *sipCppPtr = s;
    return 1;
%End
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
