// The SIP interface definition for QwtPainter.
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


class QwtPainter
{
%HeaderCode
#include <qwt_painter.h>
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

    static void setScaleMetrics(const QPaintDevice *, const QPaintDevice *);
    static void resetScaleMetrics();
    static double scaleMetricsX();
    static double scaleMetricsY();

    static void setDeviceClipping(bool);
    static bool deviceClipping();

    static QRect invScale(const QRect &, const QPainter * = 0);
    static QPoint invScale(const QPoint &, const QPainter * = 0);
    static QRect scale(const QRect &, const QPainter * = 0);
    static QPoint scale(const QPoint &, const QPainter * = 0);
    static QPointArray scale(const QPointArray &, const QPainter * = 0);
    
    static void setClipRect(QPainter *, const QRect &);

    static void drawText(QPainter *, int, int,
			 const QString &, int = -1);
    static void drawText(QPainter *, const QPoint &,
			 const QString &, int = -1);
    static void drawText(QPainter *, int, int, int, int, int,
			 const QString &, int = -1);
    static void drawText(QPainter *, const QRect &, int,
			 const QString &, int = -1);

    static void drawSimpleRichText(QPainter *, const QRect &,
        int, QSimpleRichText &);

    static void drawRect(QPainter *, int, int, int, int);
    static void drawRect(QPainter *, const QRect &);
    static void fillRect(QPainter *, const QRect &, const QBrush &); 

    static void drawEllipse(QPainter *, const QRect &);

    static void drawLine(QPainter *, int, int, int, int);
    static void drawLine(QPainter *, const QPoint &, const QPoint &);
    static void drawPolygon(QPainter *, const QPointArray &);
    static void drawPolyline(QPainter *, const QPointArray &);
    static void drawPoint(QPainter *, int, int);

    static QRect map(const QWMatrix &, const QRect &);
    static QPointArray map(const QWMatrix &, const QPointArray &);

    static void drawRoundFrame(QPainter *, const QRect &, int,
                               const QColorGroup &, bool);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
