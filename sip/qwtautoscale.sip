// The SIP interface definition for QwtAutoScale.
//
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


class QwtAutoScale
{
%HeaderCode
#include <qwt_autoscl.h>
%End

public:
    enum {
	None = 0,
	IncludeRef = 1,
	Symmetric = 2,
	Floating = 4, 
	Logarithmic = 8,
	Inverted = 16
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtAutoScale();

    void setAutoScale();
    bool autoScale() const;

    void setAutoRebuild(bool);
    bool autoRebuild() const;

    void changeOptions(int, int);
    void setOptions(int);
    bool option(int) const;
    int options() const;

    void setMaxMajor(int);
    int maxMajor() const;
    void setMaxMinor(int);
    int maxMinor() const;

    void setReference(double);
    double reference() const;

    void setMargins(double, double);
    double loMargin() const;
    double hiMargin() const;

    void setScale(double, double, double = 0.0);
    const QwtScaleDiv &scaleDiv() const;

    void adjust(double, double, int);
%MemberCode
    long reset = 0;
    double minVal, maxVal;
    PyObject *xObject;
    QwtAutoScale *ptr;
    if (sipParseArgs(&sipArgsParsed, sipArgs, "mdd|l",
		     sipThisObj, sipClass_QwtAutoScale, &ptr,
		     &minVal, &maxVal, &reset)) {

	Py_BEGIN_ALLOW_THREADS
	ptr->adjust(minVal, maxVal, (int)reset);
	Py_END_ALLOW_THREADS

	Py_INCREF(Py_None);
	return Py_None;
    } else if (sipParseArgs(&sipArgsParsed, sipArgs, "mO|l",
			    sipThisObj, sipClass_QwtAutoScale, &ptr,
			    &xObject, &reset)) {
	QwtArray<double> xArray;
        if (-1 == try_PyObject_to_QwtArray(xObject, xArray))
            return 0;

	Py_BEGIN_ALLOW_THREADS
	ptr->adjust(xArray, (int)reset);
	Py_END_ALLOW_THREADS

	Py_INCREF(Py_None);
	return Py_None;
    }
%End

    void build();
    void reset();

protected:
    void buildLinScale();
    void buildLogScale();
    void setRange(double, double);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
