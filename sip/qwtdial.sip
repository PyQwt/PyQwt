// The SIP interface definition for QwtDial
///
// Copyright (C) 2001-2004 Gerard Vermeulen
// Copyright (C) 2000 Mark Colclough
//
// This file is part of PyQwt.
//
// -- LICENSE --
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
// link PyQwt dynamically with commercial, non-commercial or educational
// versions of Qt, PyQt and sip, and distribute PyQwt in this form, provided
// that equally powerful versions of Qt, PyQt and sip have been released under
// the terms of the GNU General Public License.
//
// If PyQwt is dynamically linked with commercial, non-commercial or
// educational versions of Qt, PyQt and sip, PyQwt becomes a free plug-in
// for a non-free program.
//
// -- LICENSE --


class QwtDialScaleDraw: QwtScaleDraw
{
%TypeHeaderCode
#include <qwt_dial.h>
%End

public:
    QwtDialScaleDraw(QwtDial * /TransferThis/);
    virtual QString label(double) const;

    void showLabels(bool);
    bool visibleLabels() const;

    void setPenWidth(uint);
    uint penWidth() const;
};

class QwtDial: QwtSliderBase
{
%TypeHeaderCode
#include <qwt_dial.h>
%End

public:
    enum Shadow {
        Plain = QFrame::Plain,
        Raised = QFrame::Raised,
        Sunken = QFrame::Sunken,
    };

    enum ScaleOptions {
        ScaleBackbone = 1,
        ScaleTicks = 2,
        ScaleLabel = 4
    };

    enum Mode {
        RotateNeedle,
        RotateScale,
    };

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
    void setScaleOptions(int);
    void setScaleTicks(int, int, int, int = 1);

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

    virtual void setScaleDraw(QwtDialScaleDraw *);
    QwtDialScaleDraw *scaleDraw();
    // dead code: const QwtDialScaleDraw *scaleDraw() const;

    // setAutoDelete
protected:
    virtual void paintEvent(QPaintEvent *);
    virtual void resizeEvent(QResizeEvent *);
    virtual void keyPressEvent(QKeyEvent *);

    virtual void drawFrame(QPainter *);
    virtual void drawContents(QPainter *) const;
    virtual void drawFocusIndicator(QPainter *) const;

    virtual void drawScale(QPainter *, const QPoint &,
			   int, double, double, double) const;
    virtual void drawScaleContents(QPainter *, const QPoint &, int) const;

    virtual void drawNeedle(QPainter *, const QPoint &,
			    int, double, QPalette::ColorGroup) const;

    virtual QString scaleLabel(double) const;
    void updateScale();

    virtual void rangeChange();
    virtual void valueChange();

    virtual double getValue(const QPoint &);
    virtual void getScrollMode(const QPoint &, int & /Out/, int & /Out/);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
