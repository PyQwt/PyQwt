// qwt_numarray.cpp: encapsulates all of PyQwt's calls to the numarray C-API.
// 
// Copyright (C) 2001-2004 Gerard Vermeulen
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


#include <Python.h>

#ifdef HAS_NUMARRAY

#include <qimage.h>
#include <qwt_array.h>
#undef NO_IMPORT // to force: void **PyQwt_Numarray_PyArray_API;
#define PY_ARRAY_UNIQUE_SYMBOL PyQwt_Numarray_PyArray_API
#include <numarray/arrayobject.h>

void qwt_import_libnumarray() {
    import_array();
}

int try_NumarrayArray_to_QwtArray(PyObject *in, QwtArray<double> &out)
{
    if (!PyArray_Check(in))
        return 0;

    // FIXME: how costly is PyArray_ContiguousFromObject?
    PyArrayObject *array = (PyArrayObject *)PyArray_ContiguousFromObject(
	in, PyArray_DOUBLE, 1, 0);
    
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

    //  8 bit data
    if (((PyArrayObject *)in)->descr->type_num == tUInt8) {
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
        // initialize the palette as all gray
        for (int i = 0; i<out.numColors(); i++)
            out.setColor(i, qRgb(i, i, i));
        return 1;
    }

    // 16 bit data
    // FIXME: endianness
    if (((PyArrayObject *)in)->descr->type_num == tUInt16) {
#if QT_VERSION < 300
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
    // FIXME: what does it do on a 64 bit platform?
    // FIXME: endianness
    if (((PyArrayObject *)in)->descr->type_num == tUInt32) {
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

    PyErr_SetString(
        PyExc_RuntimeError, "Data type must be UInt8, UInt16 or UInt32");

    return -1;
}

PyObject *to_na_array(const QImage &image)
{
    PyArrayObject *result = 0;
    const int nx = image.width();
    const int ny = image.height();

    // 8 bit data
    if (image.depth() == 8) {
        int dimensions[2] = { nx, ny };

        if (0 == (result = (PyArrayObject *)PyArray_FromDims(
                      2, dimensions, tUInt8))) {
            PyErr_SetString(PyExc_MemoryError,
                            "failed to allocate memory for array");
            return 0;
        }

        const int xstride = result->strides[0];
        const int ystride = result->strides[1];

        for (int j=0; j<ny; j++) {
            unsigned char *line = (unsigned char *)image.scanLine(j);
            unsigned char *data = (unsigned char *)(result->data + j*ystride);
            for (int i=0; i<nx; i++) {
                data[0] = *line++;
                data += xstride;
            }
        }
        return PyArray_Return(result);
    }

    // 16 bit data
    // FIXME: endianness
    if (image.depth() == 16) {
#if QT_VERSION < 300
        PyErr_SetString(PyExc_RuntimeError,
                        "Qt < 3.0.0 does not support 16 bit images");
        return 0;
#else
        int dimensions[2] = { nx, ny };

        if (0 == (result = (PyArrayObject *)PyArray_FromDims(
                      2, dimensions, tUInt16))) {
            PyErr_SetString(PyExc_MemoryError,
                            "failed to allocate memory for array");
            return 0;
        }

        const int xstride = result->strides[0];
        const int ystride = result->strides[1];

        for (int j=0; j<ny; j++) {
            unsigned char *line = (unsigned char *)image.scanLine(j);
            unsigned char *data = (unsigned char *)(result->data + j*ystride);
            for (int i=0; i<nx; i++) {
                data[0] = *line++;
                data[1] = *line++;
                data += xstride;
            }
        }
        return PyArray_Return(result);
#endif
    }

    // 32 bit data.
    // FIXME: what does it do on a 64 bit platform?
    // FIXME: endianness
    if (image.depth() == 32) {
        int dimensions[2] = { nx, ny };

        if (0 == (result = (PyArrayObject *)PyArray_FromDims(
                      2, dimensions, tUInt32))) {
            PyErr_SetString(PyExc_MemoryError,
                            "failed to allocate memory for array");
            return 0;
        }

        const int xstride = result->strides[0];
        const int ystride = result->strides[1];

        for (int j=0; j<ny; j++) {
            unsigned char *line = (unsigned char *)image.scanLine(j);
            unsigned char *data = (unsigned char *)(result->data + j*ystride);
            for (int i=0; i<nx; i++) {
                data[0] = *line++;
                data[1] = *line++;
                data[2] = *line++;
                data[3] = *line++;
                data += xstride;
            }
        }
        return PyArray_Return(result);
    }
    return 0;
}


#endif // HAS_NUMARRAY

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
