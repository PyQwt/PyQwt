// The SIP interface definition for QwtWheel.
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


class QwtWheel: QwtSliderBase 
{
%HeaderCode
#include <qwt_wheel.h>
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

    QwtWheel(QWidget * /TransferThis/ = 0, const char * = 0);
    
    virtual void setOrientation(Qt::Orientation);

    double totalAngle() const;
    double viewAngle() const;
    int tickCnt() const;
    int internalBorder() const;
    double mass() const;

    void setTotalAngle(double);
    void setTickCnt(int);
    void setViewAngle(double);
    void setInternalBorder(int);
    void setMass(double);
    void setWheelWidth(int);

    virtual QSize sizeHint() const;
    virtual QSize minimumSizeHint() const;
    virtual QSizePolicy sizePolicy() const;

protected:
    virtual void resizeEvent(QResizeEvent *);
    virtual void paintEvent(QPaintEvent *);

    void layoutWheel(bool = 1);
    void draw(QPainter *, const QRect &);
    void drawWheel(QPainter *, const QRect &);
    void drawWheelBackground(QPainter *, const QRect &);
    void setColorArray();

    virtual void valueChange();
    virtual void paletteChange(const QPalette &);

    virtual double getValue(const QPoint &);
    virtual void getScrollMode(const QPoint &, int &, int &);
%MemberCode
    QPoint *point;
    sip$C *ptr;

    if (sipParseArgs(&sipArgsParsed, sipArgs, "pJ1",
		     sipThisObj, sipClass_$C, &ptr,
		     sipClass_QPoint, &point)) {
	int scrollMode, direction;

        Py_BEGIN_ALLOW_THREADS
	ptr->sipProtect_getScrollMode(*point, scrollMode, direction);
        Py_END_ALLOW_THREADS

	return Py_BuildValue("(ii)", scrollMode, direction);
    }
%End
%VirtualCode
    // sip requires VirtualCode, but does not use it :-)
%End
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
