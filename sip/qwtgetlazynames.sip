// Hack to improve rlcompleter support for PyQt&sip-3.6 and earlier.
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
// link PyQwt with commercial, non-commercial or educational versions of Qt,
// PyQt and sip, and distribute PyQwt in this form, provided that equally
// powerful versions of Qt, PyQt and sip have been released under the terms
// of the GNU General Public License.
//
// If PyQwt is dynamically linked with commercial, non-commercial or
// educational versions of Qt, PyQt and sip, PyQwt becomes a free plug-in
// for a non-free program.


%If (SIP_DUMB_DIR)
%HeaderCode
PyObject *getLazyNames(const sipLazyAttrDef &la);
%End // HeaderCode
 
%C++Code
PyObject *getLazyNames(const sipLazyAttrDef &la)
{
    int i;
    int n = la.la_nrmethods;
    int m = la.la_nrenums;

    PyObject *result = PyList_New(n+m);
    if (!(result))
	return 0;

    for (i=0; i<n; i++) {
	PyList_SetItem(
	    result, i, PyString_FromString(la.la_methods[i].ml_name));
    }

    for (i=0; i<m; i++) {
	PyList_SetItem(
	    result, n+i, PyString_FromString(la.la_enums[i].evi_name));
    }

    return result;
}
%End // C++Code
%End // SIP_DUMB_DIR


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
