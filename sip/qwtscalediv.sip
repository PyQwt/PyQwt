// The SIP interface definition for QwtScaleDiv.
//
// Copyright (C) 2001-2005 Gerard Vermeulen
// Copyright (C) 2000 Mark Colclough
//
// This file is part of PyQwt
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

class QwtScaleDiv
{
%TypeHeaderCode
#include <qwt_scldiv.h>
%End

public:
    QwtScaleDiv();

    int operator== (const QwtScaleDiv &) const;
    int operator!= (const QwtScaleDiv &) const;
    
    double lBound() const;
    double hBound() const;
    int minCnt() const;
    int majCnt() const;
    bool logScale() const;
    double majMark(int) const;
    double minMark(int) const;
    double majStep() const;
    void reset();

    bool rebuild(double, double, int, int, bool, double = 0.0, bool = TRUE);
};

%End // (QWT_4_2_0 - QWT_4_3_0)

%If (QWT_4_3_0 -)

class QwtScaleDiv
{
%TypeHeaderCode
#include <qwt_scldiv.h>
%End

public:
    enum TickType
    {
        NoTick,
        MinorTick,
        MediumTick,
        MajorTick,
        NTickTypes
    };

    QwtScaleDiv();
    QwtScaleDiv(bool, const QwtDoubleInterval &,
		QwtArrayDouble, QwtArrayDouble, QwtArrayDouble); // FIXME??
%MethodCode
        // minor, medium, major instead of QwtArray<double> ticks[NTickTypes]

	QwtArray<double> ticks[QwtScaleDiv::NTickTypes];
	ticks[QwtScaleDiv::MinorTick] = *a2;
	ticks[QwtScaleDiv::MediumTick] = *a3;
	ticks[QwtScaleDiv::MajorTick] = *a4;

	sipCpp = new QwtScaleDiv(a0, *a1, ticks);
%End

    QwtScaleDiv(bool, double, double, 
		QwtArrayDouble, QwtArrayDouble, QwtArrayDouble); // FIXME??
%MethodCode
        // minor, medium, major instead of QwtArray<double> ticks[NTickTypes]

	QwtArray<double> ticks[QwtScaleDiv::NTickTypes];
	ticks[QwtScaleDiv::MinorTick] = *a3;
	ticks[QwtScaleDiv::MediumTick] = *a4;
	ticks[QwtScaleDiv::MajorTick] = *a5;

	sipCpp = new QwtScaleDiv(a0, a1, a2, ticks);
%End

    int operator==(const QwtScaleDiv &) const;
    int operator!=(const QwtScaleDiv &) const;

    bool logScale() const;
    double lBound() const;
    double hBound() const;

    const QwtArrayDouble &ticks(int) const;

    void invalidate();
    bool isValid() const;

    void invert();
};

%End // (QWT_4_3_0 - )

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
