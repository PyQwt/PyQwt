// The SIP interface definition for QwtPlotLayout.
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


class QwtPlotLayout
{
%HeaderCode
#include <qwt_plot_layout.h>
%End

public:
    enum Options
    {
        AlignScales = 1,
        IgnoreScrollbars = 2,
        IgnoreFrames = 4,
        IgnoreMargin = 8,
        IgnoreLegend = 16
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtPlotLayout();

    void setMargin(int);
    int margin() const;

    void setCanvasMargin(int);
    int canvasMargin() const;

    void setAlignCanvasToTicks(bool);
    bool alignCanvasToTicks() const;

    void setSpacing(int);
    int spacing() const;

    void setLegendPos(int, double = 0.0);
    int legendPos() const;
    double legendRatio() const;

    virtual QSize minimumSizeHint(const QwtPlot *) const;
    virtual void activate(const QwtPlot *, QRect &, int = 0);

    virtual void invalidate();

    const QRect &titleRect() const;
    const QRect &legendRect() const;
    const QRect &scaleRect(int) const;
    const QRect &canvasRect() const;

protected:

    QRect layoutLegend(int, const QRect &) const;
    QRect alignLegend(const QRect &, const QRect &) const;

    void expandLineBreaks(int, const QRect &, int &, int *) const;
%MemberCode
    // takes an integer and a QRect
    // returns a tuple of 5 ints (title, yLeft, yRight, xBottom, xTop)
    int options;
    QRect *rect;
    sipQwtPlotLayout *ptr;

    if (sipParseArgs(&sipArgsParsed, sipArgs, "piJ1",
		     sipThisObj, sipClass_QwtPlotLayout, &ptr,
		     &options, sipClass_QRect, &rect))
	{
	    int title;
	    int axis[QwtPlot::axisCnt];

	    Py_BEGIN_ALLOW_THREADS
	    ptr->sipProtect_expandLineBreaks(options, *rect, title, axis);
	    Py_END_ALLOW_THREADS

	    return Py_BuildValue("(iiiii)",
				 title, axis[0], axis[1], axis[2], axis[3]);
	}
%End
    void alignScales(int, QRect &, QRect *) const;
%MemberCode
    // takes an integer
    // returns a tuple of 4 QRects
    int options;
    QRect *rect;
    sipQwtPlotLayout *ptr;

    if (sipParseArgs(&sipArgsParsed, sipArgs, "piJ1",
		     sipThisObj, sipClass_QwtPlotLayout, &ptr,
		     &options, sipClass_QRect, &rect))
	{
	    QRect scaleRect[QwtPlot::axisCnt];
	    PyObject *result[QwtPlot::axisCnt];

	    Py_BEGIN_ALLOW_THREADS
	    ptr->sipProtect_alignScales(options, *rect, scaleRect);
	    Py_END_ALLOW_THREADS

	    for (int i=0; i<QwtPlot::axisCnt; i++)
                // FIXME: scaleRect lives on the stack, should be on the heap?
		result[i] = sipNewCppToSelf(&scaleRect[i], sipClass_QRect,
					    SIP_PY_OWNED|SIP_SIMPLE);

	    return Py_BuildValue("(NNNN)", 
				 result[0], result[1], result[2], result[3]);
	}
%End
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
