// The SIP interface definition for QwtPlotPicker.
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


class QwtPlotPicker: QwtPicker
{
%HeaderCode
#include <qwt_plot_picker.h>
%End

public:
    enum Shape
    {
        HLine,
        VLine,
        Cross,
        Rect,
        Ellipse
    };
%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtPlotPicker(QwtPlotCanvas *, const char * = 0);

    virtual void setAxis(int, int);

    int xAxis() const;
    int yAxis() const;

    virtual void setShape(Shape);
    Shape shape() const;

    QwtPlot *plot();
    // dead code: const QwtPlot *plot() const;
    
signals:
    void moved(const QwtDoublePoint &);
    void selected(const QwtDoublePoint &);
    void selected(const QwtDoubleRect &);
    // FIXME: void selected(const QwtArray<QwtDoublePoint> &);

protected:
    QwtDoubleRect scaleRect() const;

    QwtDoubleRect invTransform(const QRect &) const;
    QRect transform(const QwtDoubleRect &) const;

    QwtDoublePoint invTransform(const QPoint &) const;
    QPoint transform(const QwtDoublePoint &) const;

    virtual QString cursorLabel(const QPoint &) const;
    virtual QString cursorLabel(const QwtDoublePoint &) const;

    virtual void drawRubberBand(QPainter *, const QRect &,
                                const QPointArray &) const;

    virtual void move(const QPoint &);
    virtual void end(bool = TRUE);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
