// The SIP interface definition for
//      QwtPickerMachine,
//      QwtPickerClickPointMachine,
//      QwtPickerDragPointMachine,
//      QwtPickerClickRectMachine,
//      QwtPickerDragRectMachine,
//      QwtPickerPolygonMachine.
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


%MappedType QValueList<QwtPickerMachine::Command>
{
%HeaderCode
#include <qvaluelist.h>
#include <qwt_picker_machine.h>
%End

%ConvertFromTypeCode
    // Handle no list.
    if (!sipCpp)
        return PyList_New(0);

    // Convert to a Python list of integers.
    PyObject *list;

    // Create the list.
    if (0 == (list = PyList_New(sipCpp -> count())))
        return 0;

    // Get it.
    for (int i = 0; i < sipCpp->count(); ++i)
        if (PyList_SetItem(list, i, PyInt_FromLong((long)(*sipCpp)[i])) < 0) {
            Py_DECREF(list);
            
            return 0;
        }

    return list;
%End

%ConvertToTypeCode
    // Convert a Python list of integers to a
    // QValueList<QwtPickerMachine::Command> on the heap.

    if (0 == sipIsErr)
        return PyList_Check(sipPy);

    if (sipPy == Py_None) {
        *sipCppPtr = 0;

        return 0;
    }

    QValueList<QwtPickerMachine::Command> *qvl =
        new QValueList<QwtPickerMachine::Command>;

    PyErr_Clear();

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
        qvl -> append((QwtPickerMachine::Command)PyInt_AsLong(
                          PyList_GET_ITEM(sipPy, i)));
            
        if (0 != PyErr_Occurred()) {
            *sipIsErr = 1;
            delete qvl;
            
            return 0;
        }
    }

    *sipCppPtr = qvl;

    return 1;
%End
};

class QwtPickerMachine
{
%HeaderCode
#include <qwt_picker_machine.h>
%End

public:
    enum Command
    {
        Begin,
        Append,
        Move,
        End
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    virtual ~QwtPickerMachine();

    //! Transition
    virtual QValueList<QwtPickerMachine::Command> transition(
        const QwtEventPattern &, const QEvent *) = 0;
    void reset();

protected:
    QwtPickerMachine();

    int state() const;
    void setState(int);
};

class QwtPickerClickPointMachine: QwtPickerMachine
{
public:
%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    virtual QValueList<QwtPickerMachine::Command> transition(
        const QwtEventPattern &, const QEvent *);
};

class QwtPickerDragPointMachine: QwtPickerMachine
{
public:
%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    virtual QValueList<QwtPickerMachine::Command> transition(
        const QwtEventPattern &, const QEvent *);
};

class QwtPickerClickRectMachine: QwtPickerMachine
{
public:
%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    virtual QValueList<QwtPickerMachine::Command> transition(
        const QwtEventPattern &, const QEvent *);
};

class QwtPickerDragRectMachine: QwtPickerMachine
{
public:
%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    virtual QValueList<QwtPickerMachine::Command> transition(
        const QwtEventPattern &, const QEvent *);
};

class QwtPickerPolygonMachine: QwtPickerMachine
{
public:
%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    virtual QValueList<QwtPickerMachine::Command> transition(
        const QwtEventPattern &, const QEvent *);
};


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
