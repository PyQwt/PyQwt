// The SIP interface definition file for QwtDiMap.
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


%If (QWT_4_2_0 - QWT_4_3_0)

class QwtDiMap
{
%TypeHeaderCode
#include <qwt_dimap.h>
%End

public:
    QwtDiMap();
    QwtDiMap(int, int, double, double, bool = 0);

    bool contains(double) const;
    bool contains(int /Constrained/) const;

    void setIntRange(int, int);
    void setDblRange(double, double, bool = 0);

    int transform(double) const;
    double invTransform(int) const;

    int limTransform(double) const;
    double xTransform(double) const;
	
    double d1() const;
    double d2() const;
    int i1() const;
    int i2() const;
    bool logarithmic() const;	

    static const double LogMin;
    static const double LogMax;

}; // class QwtDimap

%End // (QWT_4_2_0 - QWT_4_3_0)

%If (QWT_4_3_0 -)

class QwtScaleTransformation
{
%TypeHeaderCode
#include <qwt_dimap.h>
%End

public:
    QwtScaleTransformation();
//    QwtScaleTransformation(
//        double (*xForm)(double, double, double, double, double),
//        double (*invXForm)(double, double, double, double, double)
//    );

    static double linearXForm(double, double, double, double, double);

    static double logXForm(double, double, double, double, double);
    static double logInvXForm(double, double, double, double, double);


//    double (*xForm)(double, double, double, double, double);
//    double (*invXForm)(double, double, double, double, double);

}; // class QwtScaleTransformation


class QwtScaleMap
{
%TypeHeaderCode
#include <qwt_dimap.h>
%End

public:
    QwtScaleMap();
    QwtScaleMap(int, int, double, double);
    ~QwtScaleMap();

    void setTransformation(bool);
    void setTransformation(const QwtScaleTransformation &);
    const QwtScaleTransformation &transformation() const;

    void setPaintInterval(int, int);
    void setScaleInterval(double, double);

    int transform(double) const;
    double invTransform(int) const;

    double xTransform(double) const;

    double p1() const;
    double p2() const;

    double s1() const;
    double s2() const;

    // FIXME: how to wrap QT_STATIC_CONST?
    static const double LogMin;
    static const double LogMax;

}; // class QwtDiMap

%End // (QWT_4_3_0 -)


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// indent-tabs-mode: nil
// End:
