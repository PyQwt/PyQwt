// The SIP interface definition file for QwtKnob.
//
// Copyright (C) 2000-2004 Gerard Vermeulen
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


class QwtKnob: QwtSliderBase, QwtScaleIf
{
%TypeHeaderCode
#include <qwt_knob.h>
%End

public:
    enum Symbol {
	Line,
	Dot,
    };

    QwtKnob(QWidget * /TransferThis/ = 0, const char * = 0);

    void setKnobWidth(int);
    int knobWidth() const;
    void setTotalAngle(double);
    double totalAngle() const;
    int borderWidth() const;
    void setBorderWidth(int);
    void setSymbol(Symbol);
    Symbol symbol() const;

    virtual QSize sizeHint() const;
    virtual QSize minimumSizeHint() const;
    virtual QSizePolicy sizePolicy() const;

protected:
    virtual void paintEvent(QPaintEvent *);
    virtual void resizeEvent(QResizeEvent *);

    void draw(QPainter *, const QRect &);
    void drawKnob(QPainter *, const QRect &);
    void drawMarker(QPainter *, double, const QColor &);

private:
    void layoutKnob(bool = 1);
    double getValue(const QPoint &);
    void getScrollMode(const QPoint &, int & /Out/, int & /Out/);
    void recalcAngle();
 
    virtual void valueChange();
    virtual void rangeChange();
    virtual void scaleChange();
    virtual void fontChange(const QFont &);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
