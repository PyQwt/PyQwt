// The SIP interface definition for QwtDial
//
// Copyright (C) 2003 Gerard Vermeulen
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


class QwtDialScaleDraw: QwtScaleDraw
{
%HeaderCode
#include <qwt_dial.h>
%End

public:
    QwtDialScaleDraw(QwtDial * /TransferThis/);
    virtual QString label(double) const;

    void setPenWidth(uint);
    uint penWidth() const;
};

class QwtDial: QwtSliderBase
{
%HeaderCode
#include <qwt_dial.h>
%End

public:
    enum Shadow
    {
        Plain = QFrame::Plain,
        Raised = QFrame::Raised,
        Sunken = QFrame::Sunken
    };

    enum Mode {
        RotateNeedle,
        RotateScale,
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtDial(QWidget * /TransferThis/ = 0, const char * = 0);

    void setFrameShadow(Shadow);
    Shadow frameShadow() const;

    bool hasVisibleBackground() const;
    void showBackground(bool);

    void setLineWidth(int);
    int lineWidth() const;

    void setMode(Mode);
    Mode mode() const;

    void setWrapping(bool);
    bool wrapping() const;

    void setScale(int, int, double = 0.0);

    void setScaleArc(double, double);
    double minScaleArc() const;
    double maxScaleArc() const;

    void setOrigin(double);
    double origin() const;

    void setNeedle(QwtDialNeedle * /Transfer/);
    // dead code: const QwtDialNeedle *needle() const;
    QwtDialNeedle *needle();

    QRect boundingRect() const;
    QRect contentsRect() const;
    virtual QRect scaleContentsRect() const;

    virtual QSize sizeHint() const;
    virtual QSize minimumSizeHint() const;

    // setAutoDelete
protected:
    virtual void keyPressEvent(QKeyEvent *);
    virtual void paintEvent(QPaintEvent *);
    virtual void resizeEvent(QResizeEvent *);

    virtual void drawFrame(QPainter *);
    virtual void drawContents(QPainter *) const;

    virtual void drawScale(QPainter *, const QPoint &,
			   int, double, double, double) const;
    virtual void drawScaleContents(QPainter *, const QPoint &, int) const;

    virtual void drawNeedle(QPainter *, const QPoint &,
			    int, double, QPalette::ColorGroup) const;

    virtual void setScaleDraw(QwtDialScaleDraw * /Transfer/);
    QwtDialScaleDraw *scaleDraw();
    // dead code: const QwtDialScaleDraw *scaleDraw();

    virtual QString scaleLabel(double) const;
    void updateScale();

    virtual void rangeChange();
    virtual void valueChange();

    virtual double getValue(const QPoint &);
    virtual void getScrollMode(const QPoint &, int &, int &);
%MemberCode
    QPoint *point;
    sipQwtDial *ptr;

    if (sipParseArgs(&sipArgsParsed, sipArgs, "pJ1",
		     sipThisObj, sipClass_QwtDial, &ptr,
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
