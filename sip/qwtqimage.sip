// The SIP interface definition for:
//      toImage,
//      to_na_array,
//      to_np_array.
//
// Copyright (C) 2000 Mark Colclough
// Copyright (C) 2001-2004 Gerard Vermeulen
//
// This file is part of PyQwt.
//
// -- LICENSE --
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
//
// -- LICENSE --


%ModuleHeaderCode
#include <sipqtQImage.h>
QImage &toQImage(PyObject *);
%End


QImage &toQImage(SIP_PYOBJECT);
%MethodCode
    // Numeric is not thread-safe
    sipRes = new QImage();
    if (-1 == try_PyObject_to_QImage(a0, *sipRes))
        return 0;
%End


%If (HAS_NUMARRAY)
SIP_PYOBJECT to_na_array(const QImage &);
%End


%If (HAS_NUMERIC)
SIP_PYOBJECT to_np_array(const QImage &);
%End


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
