// The SIP interface definition for
//      QwtPickerMachine,
//      QwtPickerClickPointMachine,
//      QwtPickerDragPointMachine,
//      QwtPickerClickRectMachine,
//      QwtPickerDragRectMachine,
//      QwtPickerPolygonMachine.
//
// Copyright (C) 2001-2003 Gerard Vermeulen
// Copyright (C) 2000 Mark Colclough
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

%If (CXX_DYNAMIC_CAST)
%ConvertToSubClassCode
    if (dynamic_cast<const QwtPickerClickPointMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerClickPointMachine;
    else if (dynamic_cast<const QwtPickerClickRectMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerClickRectMachine;
    else if (dynamic_cast<const QwtPickerDragPointMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerDragPointMachine;
    else if (dynamic_cast<const QwtPickerDragRectMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerDragRectMachine;
    else if (dynamic_cast<const QwtPickerPolygonMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerPolygonMachine;
    else
        sipClass = 0;
%End
%End

    // virtual ~QwtPickerMachine();

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
