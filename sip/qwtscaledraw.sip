// The SIP interface definition for QwtScaleDraw.
//
// Copyright (C) 2002-2003 Gerard Vermeulen
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


class QwtScaleDraw: QwtDiMap
{
%HeaderCode
#include <qwt_scldraw.h>
%End

public:
    enum Orientation {
	Bottom,
	Top,
	Left,
	Right,
	Round,
    };

    enum Option {
	None = 0,
	Backbone = 1,
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtScaleDraw();
    
    void setScale(const QwtScaleDiv &);
    void setScale(double, double, int, int, double = 0.0, int = 0);

    void setOptions(int);
    int options() const;

    void setGeometry(int, int, int, Orientation);
    int x() const;
    int y() const;
    int length() const;
    Orientation orientation() const;

    void setAngleRange(double, double);
    void setLabelFormat(char, int, int = 0);
    void setLabelAlignment(int);
    void setLabelRotation(double);
    void setTickLength(unsigned int, unsigned int, unsigned int);

    const QwtScaleDiv& scaleDiv() const;
    int maxWidth(const QPen &, const QFontMetrics &) const;
    int maxHeight(const QPen &, const QFontMetrics &) const;

    void minBorderDist(const QFontMetrics &, int &, int &) const;
%MemberCode
    // The Python interface returns (start, end)
    QwtScaleDraw *ptr;
    const QFontMetrics *fm;

    if (sipParseArgs(&sipArgsParsed, sipArgs, "mJ1",
		     sipThisObj, sipClass_QwtScaleDraw, &ptr,
		     sipClass_QFontMetrics, &fm)) {
	int start, end;

	Py_BEGIN_ALLOW_THREADS
	ptr->minBorderDist(*fm, start, end);
	Py_END_ALLOW_THREADS
	
	return Py_BuildValue("(ii)", start, end);
    }
%End

    int minLabelDist(const QFontMetrics &) const;

    int minHeight(const QPen &, const QFontMetrics &) const; 
    int minWidth(const QPen &, const QFontMetrics &) const; 
    void labelFormat(char &, int &, int &) const;
%MemberCode
    // The Python interface returns (format, precision, width)
    QwtScaleDraw *ptr;
   
    if (sipParseArgs(&sipArgsParsed, sipArgs, "m",
		     sipThisObj, sipClass_QwtScaleDraw, &ptr)) {
	char format;
	int precision;
	int width;

	Py_BEGIN_ALLOW_THREADS
	ptr->labelFormat(format, precision, width);
	Py_END_ALLOW_THREADS

	return Py_BuildValue("(cii)", int(format), precision, width);
    }
%End
        
    int labelAlignment() const;
    double labelRotation() const;
    void tickLength(unsigned int &, unsigned int &, unsigned int &) const;
%MemberCode
    // The Python interface returns (minLen, medLen, majLen)
    QwtScaleDraw *ptr;
   
    if (sipParseArgs(&sipArgsParsed, sipArgs, "m",
		     sipThisObj, sipClass_QwtScaleDraw, &ptr)) {
	unsigned int minLen, medLen, majLen;

	Py_BEGIN_ALLOW_THREADS
	ptr->tickLength(minLen, medLen, majLen);
	Py_END_ALLOW_THREADS

	return Py_BuildValue("(iii)", minLen, medLen, majLen);
    }
%End
        
    unsigned int majTickLength() const;
         
    virtual void draw(QPainter *) const;
    virtual QString label(double) const;

protected:
    virtual void labelPlacement(const QFontMetrics &, double, QPoint &,
				int &, double &) const;
%MemberCode
    // The Python interface returns (alignment, rotation)
    QFontMetrics *a0;
    double a1;
    QPoint *a2;
    sipQwtScaleDraw *ptr;

    if (sipParseArgs(&sipArgsParsed, sipArgs, "pJ1dJ1",
		     sipThisObj, sipClass_QwtScaleDraw, &ptr,
		     sipClass_QFontMetrics, &a0,
		     &a1,
		     sipClass_QPoint, &a2)) {
	int alignment;
	double rotation;
	
	Py_BEGIN_ALLOW_THREADS
	ptr->sipProtect_labelPlacement(*a0, a1, *a2, alignment, rotation);
	Py_END_ALLOW_THREADS

	return Py_BuildValue("(id)", alignment, rotation);
    }
%End // %MemberCode

%VirtualCode
    PyObject *pyRes;

    PyObject *a0obj = sipMapCppToSelf(&a0, sipClass_QFontMetrics);
    PyObject *a2obj = sipMapCppToSelf(&a2, sipClass_QPoint);

    PyObject *sipArgs = Py_BuildValue(
	"(ONdN)", sipThis->sipSelf, a0obj, a1, a2obj);
    if (0 == sipArgs)
	goto reportError;

    pyRes = sipEvalMethod(&pymc->pyMethod, sipArgs);
    Py_DECREF(sipArgs);

    if (0 != pyRes) {
	int alignment;
	double rotation;

	int ok = PyArg_ParseTuple(pyRes, "id", &alignment, &rotation);
	Py_DECREF(pyRes);
	if (ok) {
	    a3 = alignment;
	    a4 = rotation;
	    goto releaseLock;
	}
#ifdef OLD_SIP_NAMES
	sipBadVirtualResultType(sipName_qwt_QwtScaleDraw,
				sipName_qwt_labelPlacement);
#else
	sipBadVirtualResultType(sipName_QwtScaleDraw,
				sipName_labelPlacement);
#endif
    }

reportError:
    PyErr_Print();
releaseLock:
    SIP_UNBLOCK_THREADS
%End // %VirtualCode

    virtual int maxLabelHeight(const QFontMetrics &) const;
    virtual int maxLabelWidth(const QFontMetrics &) const;
    QRect labelBoundingRect(const QFontMetrics &, double) const;

    void drawTick(QPainter *, double, int) const;
    void drawBackbone(QPainter *) const;
    void drawLabel(QPainter *, double) const;

    QWMatrix labelWorldMatrix(const QFontMetrics &, const QPoint &,
			      int, double, const QString &) const;
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
