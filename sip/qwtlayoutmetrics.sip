// The SIP interface definition for QwtMetricsMap and QwtLayoutMetrics.
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


class QwtMetricsMap
{
%HeaderCode
#include <qwt_layout_metrics.h>
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

    QwtMetricsMap();

    bool isIdentity() const;

    void setMetrics(const QPaintDeviceMetrics &, const QPaintDeviceMetrics &);

    int layoutToDeviceX(int) const;
    int deviceToLayoutX(int) const;
    int screenToLayoutX(int) const;
    int layoutToScreenX(int) const;

    int layoutToDeviceY(int) const;
    int deviceToLayoutY(int) const;
    int screenToLayoutY(int) const;
    int layoutToScreenY(int) const;

    QPoint layoutToDevice(const QPoint &, const QPainter * = 0) const;
    QPoint deviceToLayout(const QPoint &, const QPainter * = 0) const;
    QPoint screenToLayout(const QPoint &) const;

    QRect layoutToDevice(const QRect &, const QPainter * = 0) const;
    QRect deviceToLayout(const QRect &, const QPainter * = 0) const;
    QRect screenToLayout(const QRect &) const;

    QPointArray layoutToDevice(const QPointArray &,
                               const QPainter * = 0) const;
    QPointArray deviceToLayout(const QPointArray &,
                               const QPainter * = 0) const;

    static QRect translate(const QWMatrix &, const QRect &);
    static QPointArray translate(const QWMatrix &, const QPointArray &);
};

class QwtLayoutMetrics
{
%HeaderCode
#include <qwt_layout_metrics.h>
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

    QwtLayoutMetrics();
    QwtLayoutMetrics(const QwtMetricsMap &);

    void setMap(const QwtMetricsMap &);

    QRect boundingRect(const QString &, int, QPainter *) const;
    QRect boundingRect(const QString &, int, const QFontMetrics &) const;

    int heightForWidth(const QString &, int, int, const QFontMetrics &) const;
    int heightForWidth(const QString &, int, int, QPainter *) const;

    QRect boundingRect(const QSimpleRichText &, int, QPainter * = 0) const;
    int heightForWidth(QSimpleRichText &, int) const;
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
