// qwt_numarray.cpp: encapsulates all of PyQwt's calls to the numarray C-API.
// 
// Copyright (C) 2001-2003 Gerard Vermeulen
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


#ifdef HAS_NUMARRAY

#include <Python.h>
#include <qimage.h>
#include <qwt_array.h>
#undef NO_IMPORT // to force: void **PyQwt_Numarray_PyArray_API;
#define PY_ARRAY_UNIQUE_SYMBOL PyQwt_Numarray_PyArray_API
#include <numarray/arrayobject.h>

void import_NumarrayArray() {
    import_array();
}

int try_NumarrayArray_to_QwtArray(PyObject *in, QwtArray<double> &out)
{
    if (!PyArray_Check(in))
        return 0;

    // FIXME: how costly is PyArray_ContiguousFromObject?
    PyArrayObject *array = (PyArrayObject *)
    PyArray_ContiguousFromObject(in, PyArray_DOUBLE, 1, 0);
    
    if (!array) {
        PyErr_SetString(PyExc_RuntimeError,
                        "Failed to make a contiguous array of PyArray_DOUBLE");
        return -1;
    }

    out.duplicate((double *)(array->data), array->dimensions[0]);
    Py_DECREF(array);

    return 1;
}

int try_NumarrayArray_to_QImage(PyObject *in, QImage &out)
{
    if (!PyArray_Check(in))
        return 0;

    if (2 != ((PyArrayObject *)in)->nd) {
        PyErr_SetString(PyExc_RuntimeError,
                        "Image array must be 2-dimensional");
        return -1;
    }

    int nx = ((PyArrayObject *)in)->dimensions[0];
    int ny = ((PyArrayObject *)in)->dimensions[1];
    int xstride = ((PyArrayObject *)in)->strides[0];
    int ystride = ((PyArrayObject *)in)->strides[1];

    //  8 bit data - palette
    if (((PyArrayObject *)in)->descr->elsize == 1) {
        if (!out.create(nx, ny, 8, 256)) {
            PyErr_SetString(PyExc_RuntimeError,
                            "failed to create a 8 bit image");
            return -1;
        }
        for (int j=0; j<ny; j++) {
            char *line = (char *)out.scanLine(j);
            char *data = ((PyArrayObject *)in)->data + j*ystride;
            for (int i=0; i<nx; i++) {
                *line++ = data[0];
                data += xstride;
            }
        }
        return 1;
    }
    // 16 bit data
    if (((PyArrayObject *)in)->descr->elsize == 2) {
#if QT_VERSION < 300
//#if 0
        PyErr_SetString(PyExc_RuntimeError,
                        "Qt < 3.0.0 does not support 16 bit images");
        return -1;
#else
        if (!out.create(nx, ny, 16)) {
            PyErr_SetString(PyExc_RuntimeError,
                            "failed to create a 16 bit image");
            return -1;
        }
        for (int j=0; j<ny; j++) {
            char *line = (char *)out.scanLine(j);
            char *data = ((PyArrayObject *)in)->data + j*ystride;
            for (int i=0; i<nx; i++) {
                *line++ = data[0];
                *line++ = data[1];
                data += xstride;
            }
        }
        return 1;
#endif
    }
    // 32 bit data
    if (((PyArrayObject *)in)->descr->elsize == 4) {
        if (!out.create(nx, ny, 32)) {
            PyErr_SetString(PyExc_RuntimeError,
                            "failed to create a 32 bit image");
            return -1;
        }
        for (int j=0; j<ny; j++) {
            char *line = (char *)out.scanLine(j);
            char *data = ((PyArrayObject *)in)->data + j*ystride;
            for (int i=0; i<nx; i++) {
                *line++ = data[0];
                *line++ = data[1];
                *line++ = data[2];
                *line++ = data[3];
                data += xstride;
            }
        }
        return 1;
    }

    PyErr_SetString(PyExc_RuntimeError, "FIXME");

    return -1;
}

#endif // HAS_NUMARRAY

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
