// The SIP interface definition for QwtDoubleInterval.
//
// Copyright (C) 2001-2005 Gerard Vermeulen
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


%If (QWT_4_3_0 -)

class QwtDoubleInterval
{
%TypeHeaderCode
#include <qwt_double_interval.h>
%End

public:
    QwtDoubleInterval();
    QwtDoubleInterval(double, double);

    void setInterval(double, double);

    QwtDoubleInterval normalize() const;
    QwtDoubleInterval invert() const;
    QwtDoubleInterval limit(double, double) const;

    int operator==(const QwtDoubleInterval &) const;
    int operator!=(const QwtDoubleInterval &) const;

    double minValue() const;
    double maxValue() const;

    double width() const;

    void setMinValue(double);
    void setMaxValue(double);

    bool contains(double) const;

    bool intersects(const QwtDoubleInterval &) const;
    QwtDoubleInterval intersect(const QwtDoubleInterval &) const;
    QwtDoubleInterval unite(const QwtDoubleInterval &) const;

    QwtDoubleInterval operator|(const QwtDoubleInterval &) const;
    QwtDoubleInterval operator&(const QwtDoubleInterval &) const;

    QwtDoubleInterval &operator|=(const QwtDoubleInterval &);
    QwtDoubleInterval &operator&=(const QwtDoubleInterval &);

    QwtDoubleInterval extend(double) const;
    QwtDoubleInterval operator|(double) const;
    QwtDoubleInterval &operator|=(double);

    bool isValid() const;
    void invalidate();

    QwtDoubleInterval symmetrize(double) const;

}; // class QwtDoubleInterval

%End // (QWT_4_3_0 - )


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
