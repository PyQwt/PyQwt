// The SIP interface definition for QwtAutoScale.
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

class QwtAutoScale
{
%TypeHeaderCode
#include <qwt_autoscl.h>
%End

public:
    enum {
	None = 0,
	IncludeRef = 1,
	Symmetric = 2,
	Floating = 4, 
	Logarithmic = 8,
	Inverted = 16,
    };

    QwtAutoScale();

    void setAutoScale();
    bool autoScale() const;

    void setAutoRebuild(bool);
    bool autoRebuild() const;

    void changeOptions(int, int);
    void setOptions(int);
    bool option(int) const;
    int options() const;

    void setMaxMajor(int);
    int maxMajor() const;
    void setMaxMinor(int);
    int maxMinor() const;

    void setReference(double);
    double reference() const;

    void setMargins(double, double);
    double loMargin() const;
    double hiMargin() const;

    void setScale(double, double, double = 0.0);
    const QwtScaleDiv &scaleDiv() const;

    void adjust(double, double, int = 0);
    void adjust(SIP_PYOBJECT, int = 0);
%MethodCode
    QwtArray<double> array;
    // Numeric is not thread-safe
    if (-1 == try_PyObject_to_QwtArray(a0, array))
        return 0;

    Py_BEGIN_ALLOW_THREADS
    sipCpp->QwtAutoScale::adjust(array, a1);
    Py_END_ALLOW_THREADS
%End

    void build();
    void reset();

protected:
    void buildLinScale();
    void buildLogScale();
    void setRange(double, double);
};

%End // (QWT_4_2_0 - QWT_4_3_0)

%If (QWT_4_3_0 -)

class QwtAutoScaler
{
%TypeHeaderCode
#include <qwt_autoscl.h>
%End

public:
    enum {
	None = 0,
	IncludeRef = 1,
	Symmetric = 2,
        Floating = 4,
        Inverted = 8,
    };

    QwtAutoScaler();
    virtual ~QwtAutoScaler();

    virtual void autoScale(int, double &, double &, double &) const = 0;

    virtual QwtScaleDiv divide(double, double, int, double) const = 0;

    virtual double stepSize(double, double, int) const = 0;

    void changeOptions(int, bool);
    void setOptions(int);
    bool option(int) const;
    int options() const;

    void setReference(double);
    double reference() const;

    void setMargins(double, double);
    double loMargin() const;
    double hiMargin() const;

protected:
    bool almostZero(double, double) const;
};


class QwtLinearAutoScaler: QwtAutoScaler
{
%TypeHeaderCode
#include <qwt_autoscl.h>
%End

public:
    virtual void autoScale(int, double &, double &, double &) const;

    virtual QwtScaleDiv divide(double, double, int, double) const;

    virtual double stepSize(double, double, int) const;
};


class QwtLog10AutoScaler: QwtAutoScaler
{
%TypeHeaderCode
#include <qwt_autoscl.h>
%End

public:
    virtual void autoScale(int, double &, double &, double &) const;

    virtual QwtScaleDiv divide(double, double, int, double) const;

    virtual double stepSize(double, double, int) const;
};

%End // (QWT_4_3_0 -)


// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
