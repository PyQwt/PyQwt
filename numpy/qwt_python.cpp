// qwt_python.cpp: to convert Python objects to QwtArray<double>.
// 
// Copyright (C) 2001-2005 Gerard Vermeulen
// Copyright (C) 2000 Mark Colclough
//
// This file is part of PyQwt
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
// link PyQwt dynamically with commercial, non-commercial or educational
// versions of Qt, PyQt and sip, and distribute PyQwt in this form, provided
// that equally powerful versions of Qt, PyQt and sip have been released under
// the terms of the GNU General Public License.
//
// If PyQwt is dynamically linked with commercial, non-commercial or
// educational versions of Qt, PyQt and sip, PyQwt becomes a free plug-in
// for a non-free program.


#include <qwt_python.h>

static int try_PySequence_to_QwtArray(PyObject *in, QwtArray<double> &out)
{
    if (!PyList_Check(in) && !PyTuple_Check(in))
        return 0;
    
    // MSVC-6.0 chokes on passing an uint in QwtArray<double>::operator[](int)
    int size = PySequence_Size(in);
    out.resize(size);

    for (int i=0; i<size; i++) {
        PyObject *element = PySequence_Fast_GET_ITEM(in, i);
        if (PyFloat_Check(element)) {
            out[i] = PyFloat_AsDouble(element);
        } else if (PyInt_Check(element)) {
            out[i] = double(PyInt_AsLong(element));    
        } else if (PyLong_Check(element)) {
            out[i] = PyLong_AsDouble(element);
        } else {
            PyErr_SetString(
		PyExc_TypeError,
		"The sequence may only contain float, int, or long types.");

            return -1;
        }
    }

    return 1;
}

int try_PyObject_to_QwtArray(PyObject *in, QwtArray<double> &out)
{
    int result;

#ifdef HAS_NUMERIC
    if ((result = try_NumericArray_to_QwtArray(in, out)))
        return result;
#endif
    
#ifdef HAS_NUMARRAY
    if ((result = try_NumarrayArray_to_QwtArray(in, out)))
        return result;
#endif

    if ((result = try_PySequence_to_QwtArray(in, out)))
        return result;

    PyErr_SetString(PyExc_TypeError, "expected is\n"
                    "(*) a list or tuple of Python numbers.\n"
#ifdef HAS_NUMERIC
                    "(*) a Numeric array coercible to PyArray_DOUBLE.\n"
#else
                    "(!) rebuild PyQwt to support Numeric arrays.\n" 
#endif
#ifdef HAS_NUMARRAY
                    "(*) a numarray array coercible to PyArray_DOUBLE.\n"
#else
                    "(!) rebuild PyQwt to support numarray arrays.\n"
#endif
        );
            
    return -1;
}

static int try_PySequence_to_QwtArray(PyObject *in, QwtArray<long> &out)
{
    if (!PyList_Check(in) && !PyTuple_Check(in))
        return 0;
    
    // MSVC-6.0 chokes on passing an uint in QwtArray<double>::operator[](int)
    int size = PySequence_Size(in);
    out.resize(size);

    for (int i=0; i<size; i++) {
        PyObject *element = PySequence_Fast_GET_ITEM(in, i);
        if (PyInt_Check(element)) {
            out[i] = PyInt_AsLong(element);
        } else if (PyLong_Check(element)) {
            out[i] = PyLong_AsLong(element);
        } else {
            PyErr_SetString(
		PyExc_TypeError,
		"The sequence may only contain int and long types.");

            return -1;
        }
    }

    return 1;
}

int try_PyObject_to_QwtArray(PyObject *in, QwtArray<long> &out)
{
    int result;

#ifdef HAS_NUMERIC
    if ((result = try_NumericArray_to_QwtArray(in, out)))
        return result;
#endif
    
#ifdef HAS_NUMARRAY
    if ((result = try_NumarrayArray_to_QwtArray(in, out)))
        return result;
#endif

    if ((result = try_PySequence_to_QwtArray(in, out)))
        return result;

    PyErr_SetString(PyExc_TypeError, "expected is\n"
                    "(*) a list or tuple of Python numbers.\n"
#ifdef HAS_NUMERIC
                    "(*) a Numeric array coercible to PyArray_LONG.\n"
#else
                    "(!) rebuild PyQwt to support Numeric arrays.\n" 
#endif
#ifdef HAS_NUMARRAY
                    "(*) a numarray array coercible to PyArray_LONG.\n"
#else
                    "(!) rebuild PyQwt to support numarray arrays.\n"
#endif
        );
            
    return -1;
}

int try_PyObject_to_QImage(PyObject *in, QImage &out)
{
    int result;

#ifdef HAS_NUMERIC
    if ((result = try_NumericArray_to_QImage(in, out)))
        return result;
#endif

#ifdef HAS_NUMARRAY
    if ((result = try_NumarrayArray_to_QImage(in, out)))
        return result;
#endif

    PyErr_SetString(PyExc_TypeError, "expected is\n"
#ifdef HAS_NUMERIC
                    "(*) a Numeric array.\n"
#else
                    "(!) rebuild PyQwt to support Numeric arrays.\n" 
#endif
#ifdef HAS_NUMARRAY
                    "(*) a numarray array.\n"
#else
                    "(!) rebuild PyQwt to support numarray arrays.\n"
#endif
        );
            
    return -1;
}


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
