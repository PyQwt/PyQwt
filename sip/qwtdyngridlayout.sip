// The SIP interface definition for QwtDynGridLayout.
//
// Copyright (C) 2003 Gerard Vermeulen
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


%MappedType QValueList<QRect>
{
%HeaderCode
#include <qwt_dyngrid_layout.h>
%End

%ConvertFromTypeCode
    // Handle no list.
    if (!sipCpp)
	return PyList_New(0);

    // Convert to a Python list of QRect instances.
    PyObject *list;

    // Create the list.
    if (0 == (list = PyList_New(sipCpp->count())))
	return 0;

    // Get it.

    int i = 0;
    QValueListConstIterator<QRect> it;

    for (it = sipCpp -> begin(); it != sipCpp -> end(); ++it, ++i) {
	PyObject *tmobj;

	if (0 == (tmobj = sipNewCppToSelf(new QRect(*it), sipClass_QRect,
					  SIP_SIMPLE | SIP_PY_OWNED)) 
	    || PyList_SetItem(list, i, tmobj) < 0) {
	    Py_XDECREF(tmobj);
	    Py_DECREF(list);
	    
	    return 0;
	}
    }

    return list;
%End // %ConvertFromTypeCode

%ConvertToTypeCode
    // Convert a Python list of QRect instances to a
    // QValueList<QRect> on the heap.

    if (0 == sipIsErr)
	return PyList_Check(sipPy);

    if (sipPy == Py_None) {
	*sipCppPtr = 0;
	
	return 0;
    }

    QValueList<QRect> *qvl = new QValueList<QRect>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
	int iserr = 0;

	QRect *itm = sipForceConvertTo_QRect(
	    PyList_GET_ITEM(sipPy, i), &iserr);

	if (!itm || iserr) {
	    *sipIsErr = 1;
	    delete qvl;

	    return 0;
	}

	qvl -> append(*itm);
    }

    *sipCppPtr = qvl;

    return 1;
%End // %ConvertToTypeCode
};

class QwtDynGridLayout: QLayout
{
%HeaderCode
#include <qwt_dyngrid_layout.h>
%End

public:
%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtDynGridLayout(QWidget *, int = 0, int = -1, const char * = 0);
    QwtDynGridLayout(QLayout *, int =-1, const char * = 0);
    QwtDynGridLayout(int = -1, const char * = 0);

    void setMaxCols(uint);
    uint maxCols() const;

    uint numRows () const;
    uint numCols () const;

    virtual void addItem(QLayoutItem *);
    virtual QLayoutIterator iterator();

    virtual int maxItemWidth() const;

    virtual void setGeometry(const QRect &);

    virtual bool hasHeightForWidth() const;
    virtual int heightForWidth(int) const;

    virtual QSize sizeHint() const;

    void setExpanding(QSizePolicy::ExpandData);
    virtual QSizePolicy::ExpandData expanding() const;

    virtual bool isEmpty() const;

    virtual uint columnsForWidth(int) const;

    QValueList<QRect> layoutItems(const QRect &, uint) const;

protected:
%If (- Qt_3_0_0)
    void layoutGrid(uint, QArray<int> &, QArray<int> &) const;
    void stretchGrid(const QRect &, uint, QArray<int> &, QArray<int> &) const;
%End // %If (- Qt_3_0_0)

%If (Qt_3_0_0 -)
    void layoutGrid(uint, QMemArray<int> &, QMemArray<int> &) const;
    void stretchGrid(const QRect &, uint,
		     QMemArray<int> &, QMemArray<int> &) const;
%End // %If (Qt_3_0_0 -)
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
