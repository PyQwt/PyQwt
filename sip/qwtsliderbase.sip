// The SIP interface definition for QwtSliderBase.
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


class QwtSliderBase: QWidget, QwtDblRange
{
%TypeHeaderCode
#include <qwt_sldbase.h>
%End

public:
    enum ScrollMode {
	ScrNone,
	ScrMouse,
	ScrTimer,
	ScrDirect,
	ScrPage,
    };

    QwtSliderBase(Qt::Orientation, QWidget * /TransferThis/ = 0,
		  const char * = 0, Qt::WFlags = 0);
    virtual ~QwtSliderBase();

    void setUpdateTime(int);
    void stopMoving();
    void setTracking(bool);

    virtual void setMass(double);
    virtual double mass() const;

    virtual void setOrientation(Orientation);
    Orientation orientation() const;

    bool isReadOnly() const;

    bool isValid() const;
    void setValid(bool);

public slots:
    void setValue(double);
    void fitValue(double);
    void incValue(int);

    virtual void setReadOnly(bool);
	
signals:
    void valueChanged(double);
    void sliderPressed();
    void sliderReleased();
    void sliderMoved(double);

protected:
    void setPosition(const QPoint &);
    virtual void valueChange();

    virtual void timerEvent(QTimerEvent *);
    virtual void mousePressEvent(QMouseEvent *);
    virtual void mouseReleaseEvent(QMouseEvent *);
    virtual void mouseMoveEvent(QMouseEvent *);
    virtual void keyPressEvent(QKeyEvent *);
    virtual void wheelEvent(QWheelEvent *);

    virtual double getValue(const QPoint &) = 0;
    virtual void getScrollMode(const QPoint &, int & /Out/, int & /Out/) = 0;
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
