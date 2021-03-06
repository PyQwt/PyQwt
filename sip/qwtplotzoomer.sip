// The SIP interface definition for QwtPlotZoomer.
//
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


class QwtPlotZoomer: QwtPlotPicker
{
%TypeHeaderCode
#include <qwt_plot_zoomer.h>
%End

public:
    QwtPlotZoomer(QwtPlotCanvas *, const char * = 0);
    QwtPlotZoomer(int, int, QwtPlotCanvas *, const char * = 0);
    QwtPlotZoomer(int, int, int, DisplayMode,
                  QwtPlotCanvas *, const char * = 0);

    virtual void setZoomBase();
    virtual void setZoomBase(const QwtDoubleRect &);

    QwtDoubleRect zoomBase() const;
    QwtDoubleRect zoomRect() const;

    void setAxis(int, int);

    void setMaxStackDepth(int);
    int maxStackDepth() const;

    // dead code: const QValueStack<QwtDoubleRect> &zoomStack() const;
    uint zoomRectIndex() const;

    virtual void setSelectionFlags(int);

public slots:
    void moveBy(double, double);
    virtual void move(double, double);

    virtual void zoom(const QwtDoubleRect &);
    virtual void zoom(int);

signals:
    void zoomed(const QwtDoubleRect &);

protected:
    // not implemented: 
    QValueStack<QwtDoubleRect> &zoomStack();

    virtual void rescale();

    virtual QwtDoubleSize minZoomSize() const;

    virtual void widgetMouseReleaseEvent(QMouseEvent *);
    virtual void widgetKeyPressEvent(QKeyEvent *);

    virtual void begin();
    virtual bool end(bool = 1);
    virtual bool accept(QPointArray &) const;
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
