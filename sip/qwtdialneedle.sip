// The SIP interface definition for
//	QwtDialNeedle,
//	QwtDialSimpleNeedle,
//	QwtCompassMagnetNeedle,
//	QwtCompassWindArrow.
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
%HeaderCode
#include <qwt_dial_needle.h>
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

    QwtDialNeedle();

    virtual void draw(QPainter *, const QPoint &, int, double,
		      QPalette::ColorGroup = QPalette::Active) const = 0;

    virtual void setPalette(const QPalette &);
    const QPalette &palette() const;
protected:
    const QColorGroup &colorGroup(QPalette::ColorGroup) const;
};

class QwtDialSimpleNeedle: QwtDialNeedle
{
%HeaderCode
#include <qwt_dial_needle.h>
%End

public:
    enum Style
    {
        Arrow,
        Ray
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtDialSimpleNeedle(Style, bool = 1,
			const QColor & = Qt::gray, const QColor & = Qt::white);

    virtual void draw(QPainter *, const QPoint &, int,
		      double, QPalette::ColorGroup = QPalette::Active) const;

    static void drawArrowNeedle(QPainter *, const QPoint &,
				int, int, double, bool,
				const QColor &, const QColor &);
    
    static void drawRayNeedle(QPainter *, const QPoint &,
			      int, int, double, bool,
			      const QColor &, const QColor &);

    void setWidth(int);
    int width() const;

protected:
    static void drawKnob(QPainter *, const QPoint &, int, const QColor &);
};

class QwtCompassMagnetNeedle: QwtDialNeedle
{
%HeaderCode
#include <qwt_dial_needle.h>
%End

public:
    enum Style
    {
        TriangleStyle,
        ThinStyle
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
        return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtCompassMagnetNeedle(Style = TriangleStyle,
			   const QColor & = Qt::white,
			   const QColor & = Qt::red);

    virtual void draw(QPainter *, const QPoint &, int, double,
		      QPalette::ColorGroup = QPalette::Active) const;

    static void drawTriangleNeedle(QPainter *, const QPoint &,
				   int, double,
				   const QColor &, const QColor &);

    static void drawThinNeedle(QPainter *, const QPoint &,
			       int, double,
			       const QColor &, const QColor &, const QColor &);

protected:
    static void drawPointer(QPainter *, const QColor &,
			    int, const QPoint &,
			    int, int, double);
};

class QwtCompassWindArrow: QwtDialNeedle
{
%HeaderCode
#include <qwt_dial_needle.h>
%End

public:
    enum Style
    {
        Style1,
        Style2
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
        return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtCompassWindArrow(Style,
			const QColor & = Qt::white,
			const QColor & = Qt::gray);

    virtual void draw(QPainter *, const QPoint &,
		      int, double,
		      QPalette::ColorGroup = QPalette::Active) const;

    static void drawStyle1Needle(QPainter *, const QPoint &,
				 int, double, const QColor &, const QColor &);

    static void drawStyle2Needle(QPainter *, const QPoint &,
				 int, double, const QColor &, const QColor &);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
