// The SIP interface definition file for QwtKnob.
//
// Copyright (C) 2000 Mark Colclough
// Copyright (C) 2000-2003 Gerard Vermeulen
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


class QwtKnob: QwtSliderBase, QwtScaleIf
{
%HeaderCode
#include <qwt_knob.h>
%End

public:
    enum Symbol {
	Line,
	Dot
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

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
    void getScrollMode(const QPoint &, int &, int &);
%MemberCode
    // sip requires MemberCode to generate a dummy wrapper :-)
%End
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
