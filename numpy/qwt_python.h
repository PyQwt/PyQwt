// qwt_python.h:
// - conversion from Python objects to QwtArray<double>.
// - conversion between Python objects and QImage.
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


#ifndef QWT_PYTHON_H
#define QWT_PYTHON_H

#include <qwt_numarray.h>
#include <qwt_numeric.h>

// returns 1, 0, -1 in case of success, wrong object type, failure
int try_PyObject_to_QwtArray(PyObject *object, QwtArray<double> &array);
int try_PyObject_to_QImage(PyObject *object, QImage &image);
PyObject *to_na_array(const QImage &image);
PyObject *to_np_array(const QImage &image); 

#endif // QWT_PYTHON_H

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
