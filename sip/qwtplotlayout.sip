// The SIP interface definition for QwtPlotLayout.
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
// FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
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


class QwtPlotLayout
{
%TypeHeaderCode
#include <qwt_plot_layout.h>
%End

public:
    enum Options {
        AlignScales = 1,
        IgnoreScrollbars = 2,
        IgnoreFrames = 4,
        IgnoreMargin = 8,
        IgnoreLegend = 16,
    };

    QwtPlotLayout();

    void setMargin(int);
    int margin() const;

    void setCanvasMargin(int, int = -1);
    int canvasMargin(int) const;

    void setAlignCanvasToScales(bool);
    bool alignCanvasToScales() const;

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

    void expandLineBreaks(int, const QRect &, int &, int * = 0) const;
%MethodCode
    int axis[QwtPlot::axisCnt] = {0, 0, 0, 0};

    sipCpp->sipProtect_expandLineBreaks(a0, *a1, a2, axis);
    return sipBuildResult(&sipIsErr, "(iiiii)",
                          a2, axis[0], axis[1], axis[2], axis[3]);
%End

    void alignScales(int, QRect &, QRect *) const;
%MethodCode
    QRect *canvasRect = new QRect();
    QRect scaleRect[QwtPlot::axisCnt];

    sipCpp->sipProtect_alignScales(a0, *canvasRect, scaleRect);
    
    QRect *heapCopy[QwtPlot::axisCnt];
    for (int i=0; i<QwtPlot::axisCnt; i++)
        heapCopy[i] = new QRect(scaleRect[i]);

    return sipBuildResult(&sipIsErr,"(NNNNN)",
                          canvasRect, sipClass_QRect,
                          &heapCopy[0], sipClass_QRect,
                          &heapCopy[1], sipClass_QRect,
                          &heapCopy[2], sipClass_QRect, 
                          &heapCopy[3], sipClass_QRect);
%End
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
