// The SIP interface definition file for mapped QwtArray types.
//
// Copyright (C) 2000 Mark Colclough
// Copyright (C) 2001-2003 Gerard Vermeulen
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


%MappedType QwtArray<QwtDiMap>
{
%HeaderCode
#include <qwt_array.h>
#include <qwt_dimap.h>
%End

%ConvertFromTypeCode
    if (!sipCpp)
        return PyList_New(0);

    PyObject *l = PyList_New(sipCpp->count());;

    if (0 == l)
        return 0;

    for (int i = 0; i < int(sipCpp->count()); i++) {
        PyObject *o;
        if ((0 == (o = sipNewCppToSelf(new QwtDiMap((*sipCpp)[i]),
                                       sipClass_QwtDiMap,
                                       SIP_SIMPLE | SIP_PY_OWNED)))
            || (-1 == PyList_SetItem(l, i, o)))
        {
            Py_DECREF(l);
            return 0;
        }             
    }
    
    return l;
%End

%ConvertToTypeCode
    if (0 == sipIsErr)
        return PyList_Check(sipPy);

    QwtArray<QwtDiMap> *a = new QwtArray<QwtDiMap>(
        PyList_GET_SIZE(sipPy));
    int iserr = 0;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
        (*a)[i] = *sipForceConvertTo_QwtDiMap(
            PyList_GET_ITEM(sipPy, i), &iserr);

        if (iserr) {
            delete a;
            *sipIsErr = 1;
            
            return 0;
        }
    }

    *sipCppPtr = a;

    return 1;
%End
};

%MappedType QwtArray<QwtDoublePoint>
{
%HeaderCode
#include <qwt_array.h>
#include <qwt_double_rect.h>
%End

%ConvertFromTypeCode
    if (!sipCpp)
        return PyList_New(0);

    PyObject *l = PyList_New(sipCpp->count());;

    if (0 == l)
        return 0;

    for (int i = 0; i < int(sipCpp->count()); i++) {
        PyObject *o;
        if ((0 == (o = sipNewCppToSelf(new QwtDoublePoint((*sipCpp)[i]),
                                       sipClass_QwtDoublePoint,
                                       SIP_SIMPLE | SIP_PY_OWNED)))
            || (-1 == PyList_SetItem(l, i, o)))
        {
            Py_DECREF(l);
            return 0;
        }             
    }
    
    return l;
%End

%ConvertToTypeCode
    if (0 == sipIsErr)
        return PyList_Check(sipPy);

    QwtArray<QwtDoublePoint> *a = new QwtArray<QwtDoublePoint>(
        PyList_GET_SIZE(sipPy));
    int iserr = 0;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
        (*a)[i] = *sipForceConvertTo_QwtDoublePoint(
            PyList_GET_ITEM(sipPy, i), &iserr);

        if (iserr) {
            delete a;
            *sipIsErr = 1;
            
            return 0;
        }
    }

    *sipCppPtr = a;

    return 1;
%End
};


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
