// The SIP interface definition for
//	QwtDialNeedle,
//	QwtDialSimpleNeedle,
//	QwtCompassMagnetNeedle,
//	QwtCompassWindArrow.
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


class QwtDialNeedle
{
%TypeHeaderCode
#include <qwt_dial_needle.h>
%End

public:
    QwtDialNeedle();

    virtual void draw(QPainter *, const QPoint &, int, double,
		      QPalette::ColorGroup = QPalette::Active) const = 0;

    virtual void setPalette(const QPalette &);
    const QPalette &palette() const;
protected:
    const QColorGroup &colorGroup(QPalette::ColorGroup) const;
    static void drawKnob(QPainter *, const QPoint &,
                         int, const QBrush &, bool);
};

class QwtDialSimpleNeedle: QwtDialNeedle
{
%TypeHeaderCode
#include <qwt_dial_needle.h>
%End

public:
    enum Style {
        Arrow,
        Ray,
    };

    QwtDialSimpleNeedle(Style, bool = 1,
			const QColor & = Qt::gray, const QColor & = Qt::white);

    virtual void draw(QPainter *, const QPoint &, int,
		      double, QPalette::ColorGroup = QPalette::Active) const;

    static void drawArrowNeedle(QPainter *, const QColorGroup &,
                                const QPoint &, int, int, double, bool);
    
    static void drawRayNeedle(QPainter *, const QColorGroup &,
                              const QPoint &, int, int, double, bool);

    void setWidth(int);
    int width() const;
};

class QwtCompassMagnetNeedle: QwtDialNeedle
{
%TypeHeaderCode
#include <qwt_dial_needle.h>
%End

public:
    enum Style {
        TriangleStyle,
        ThinStyle,
    };

    QwtCompassMagnetNeedle(Style = TriangleStyle,
			   const QColor & = Qt::white,
			   const QColor & = Qt::red);

    virtual void draw(QPainter *, const QPoint &, int, double,
		      QPalette::ColorGroup = QPalette::Active) const;

    static void drawTriangleNeedle(QPainter *, const QColorGroup &,
                                   const QPoint &, int, double);

    static void drawThinNeedle(QPainter *, const QColorGroup &,
                               const QPoint &, int, double);

protected:
    static void drawPointer(QPainter *, const QBrush &,
			    int, const QPoint &,
			    int, int, double);
};

class QwtCompassWindArrow: QwtDialNeedle
{
%TypeHeaderCode
#include <qwt_dial_needle.h>
%End

public:
    enum Style {
        Style1,
        Style2,
    };

    QwtCompassWindArrow(Style,
			const QColor & = Qt::white,
			const QColor & = Qt::gray);

    virtual void draw(QPainter *, const QPoint &,
		      int, double,
		      QPalette::ColorGroup = QPalette::Active) const;

    static void drawStyle1Needle(QPainter *, const QColorGroup &,
                                 const QPoint &, int, double);

    static void drawStyle2Needle(QPainter *, const QColorGroup &,
                                 const QPoint &, int, double);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
