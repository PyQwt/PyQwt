// qwt_numeric.h: encapsulates all of PyQwt's calls to the Numeric C-API.
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
// FOR A PARTICULAR PURPOSE.  See the GNU  General Public License for more
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


#ifndef QWT_NUMERIC_H
#define QWT_NUMERIC_H

#include <Python.h>
#include <qimage.h>
#include <qwt_array.h>

#ifdef HAS_NUMERIC
// Numeric's C-API pointer
extern void **PyQwt_Numeric_PyArray_API;
// to #ifdef import_array()
void qwt_import_array();
// returns 1, 0, -1 in case of success, wrong PyObject type, failure
int try_NumericArray_to_QwtArray(PyObject *in, QwtArray<double> &out);
int try_NumericArray_to_QwtArray(PyObject *in, QwtArray<long> &out);
int try_NumericArray_to_QImage(PyObject *in, QImage &out);
PyObject *to_np_array(const QImage &image);
#endif // HAS_NUMERIC

#endif // QWT_NUMERIC

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
