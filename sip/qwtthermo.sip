// The SIP interface definition for QwtThermo.
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


class QwtThermo: QWidget, QwtScaleIf
{
%HeaderCode
#include <qwt_thermo.h>
%End
	
public:
    enum ScalePos {
	None,
	Left,
	Right,
	Top,
	Bottom
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtThermo(QWidget * /TransferThis/ = 0, const char * = 0);

    void setOrientation(Qt::Orientation, ScalePos);
    void setBorderWidth(int);
    void setFillColor(const QColor &);
    void setAlarmColor(const QColor &);
    void setAlarmLevel(double);
    void setAlarmEnabled (int);
    void setPipeWidth(int);
    void setRange(double, double);
    void setMargin(int);
    double maxValue();
    double minValue();
    double value();

    virtual QSize sizeHint() const;
    virtual QSize minimumSizeHint() const;
    virtual QSizePolicy sizePolicy() const;

public slots:
    void setValue(double);
	
protected:
    void draw(QPainter *, const QRect &);
    void drawThermo(QPainter *);
    void layoutThermo(bool = 1);
    virtual void scaleChange();
    virtual void fontChange(const QFont &);
    
    virtual void paintEvent(QPaintEvent *);
    virtual void resizeEvent(QResizeEvent *);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
