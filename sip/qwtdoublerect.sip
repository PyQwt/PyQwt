// The SIP interface definition for QwtDoublePoint and QwtDoubleRect.
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


class QwtDoublePoint
{
%HeaderCode
#include <qwt_double_rect.h>
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

    QwtDoublePoint();
    QwtDoublePoint(double, double);
    QwtDoublePoint(const QPoint &);

    bool isNull() const;

    double x() const;
    double y() const;
    void setX(double);
    void setY(double);

    double rx();
    double ry();

    bool operator==(const QwtDoublePoint &) const;
    bool operator!=(const QwtDoublePoint &) const;

    // FIXME: const QwtDoublePoint operator-() const;
    const QwtDoublePoint operator+(const QwtDoublePoint &) const;
    const QwtDoublePoint operator-(const QwtDoublePoint &) const;
    const QwtDoublePoint operator*(double) const;
    const QwtDoublePoint operator/(double) const;

    QwtDoublePoint &operator+=(const QwtDoublePoint &);
    QwtDoublePoint &operator-=(const QwtDoublePoint &);
    QwtDoublePoint &operator*=(double);
    QwtDoublePoint &operator/=(double);

};

class QwtDoubleSize
{
%HeaderCode
#include <qwt_double_rect.h>
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

    QwtDoubleSize();
    QwtDoubleSize(double, double);
    QwtDoubleSize(const QSize &);

    bool isNull() const;
    bool isEmpty() const;
    bool isValid() const;

    double width() const;
    double height() const;
    void setWidth(double);
    void setHeight(double);
    void transpose();

    QwtDoubleSize expandedTo(const QwtDoubleSize &) const;
    QwtDoubleSize boundedTo(const QwtDoubleSize &) const;

    double rwidth();
    double rheight();

    bool operator==(const QwtDoubleSize &) const;
    bool operator!=(const QwtDoubleSize &) const;

    // FIXME: const QwtDoubleSize operator-() const;
    const QwtDoubleSize operator+(const QwtDoubleSize &) const;
    const QwtDoubleSize operator-(const QwtDoubleSize &) const;
    const QwtDoubleSize operator*(double) const;
    const QwtDoubleSize operator/(double) const;

    QwtDoubleSize &operator+=(const QwtDoubleSize &);
    QwtDoubleSize &operator-=(const QwtDoubleSize &);
    QwtDoubleSize &operator*=(double);
    QwtDoubleSize &operator/=(double);
};

class QwtDoubleRect
{
%HeaderCode
#include <qwt_double_rect.h>
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

    QwtDoubleRect();
    QwtDoubleRect(double, double, double, double);
    QwtDoubleRect(double, double, const QwtDoubleSize &);

    bool isNull() const;
    bool isEmpty()   const;
    bool isValid()   const;

    QwtDoubleRect normalize() const;

    double x1()  const;
    double x2()  const;
    double y1()  const;
    double y2()  const;

    double rx1();
    double rx2();
    double ry1();
    double ry2();

    void setX1(double);
    void setX2(double);
    void setY1(double);
    void setY2(double);

    QwtDoublePoint center()  const;

    void moveX(double);
    void moveY(double);
    void move(double, double);
    void moveBy(double, double);
    void moveCenter(const QwtDoublePoint &);
    void moveCenter(double, double);

    void setRect(double, double, double, double);

    double width() const;
    double height() const;
    QwtDoubleSize size() const;

    void setWidth(double);
    void setHeight(double);
    void setSize(const QwtDoubleSize &);

    QwtDoubleRect  operator|(const QwtDoubleRect &) const;
    QwtDoubleRect  operator&(const QwtDoubleRect &) const;
    QwtDoubleRect &operator|=(const QwtDoubleRect &);
    QwtDoubleRect &operator&=(const QwtDoubleRect &);
    bool operator==( const QwtDoubleRect &) const;
    bool operator!=( const QwtDoubleRect &) const;

    bool contains(const QwtDoublePoint &, bool = FALSE) const;
    bool contains(double, double, bool = FALSE) const; 
    bool contains(const QwtDoubleRect &, bool = FALSE) const;

    QwtDoubleRect unite(const QwtDoubleRect &) const;
    QwtDoubleRect intersect(const QwtDoubleRect &) const;
    bool intersects(const QwtDoubleRect &) const;
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
