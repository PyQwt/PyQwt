// The SIP interface definition for QwtThermo.
//
// Copyright (C) 2001-2004 Gerard Vermeulen
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


class QwtThermo: QWidget, QwtScaleIf
{
%TypeHeaderCode
#include <qwt_thermo.h>
%End
	
public:
    enum ScalePos {
	None,
	Left,
	Right,
	Top,
	Bottom,
    };

    QwtThermo(QWidget * /TransferThis/ = 0, const char * = 0);

    void setOrientation(Qt::Orientation, ScalePos);

    void setScalePosition(ScalePos);
    ScalePos scalePosition() const;

    void setBorderWidth(int);
    int borderWidth() const;

    void setFillBrush(const QBrush &);
    const QBrush &fillBrush() const;

    void setFillColor(const QColor &);
    const QColor &fillColor() const;

    void setAlarmBrush(const QBrush &);
    const QBrush &alarmBrush() const;

    void setAlarmColor(const QColor &);
    const QColor &alarmColor() const;

    void setAlarmLevel(double);
    double alarmLevel() const;

    void setAlarmEnabled(bool);
    bool alarmEnabled() const;

    void setPipeWidth(int);
    int pipeWidth() const;

    void setMaxValue(double);
    double maxValue() const;

    void setMinValue(double);
    double minValue() const;

    double value() const;

    void setRange(double, double, bool = 0);
    void setMargin(int);

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
