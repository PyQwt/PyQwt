// The SIP interface definition for the Qwt module of PyQwt.
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


%Module qwt

%Include features.sip

%Import qtmod.sip

%HeaderCode
#include <qwt_python.h>
%End

// Hack to improve rlcompleter support for PyQt&sip-3.6 and earlier
%Include qwtgetlazynames.sip

// Normal include files
%Include qwt.sip
%Include qwtarrowbutton.sip
%Include qwtautoscale.sip
%Include qwtcompass.sip
%Include qwtcompassrose.sip
%Include qwtcounter.sip
%Include qwtcurve.sip
%Include qwtcurvedict.sip
%Include qwtdblrange.sip
%Include qwtdial.sip
%Include qwtdialneedle.sip
%Include qwtdimap.sip
%Include qwtdyngridlayout.sip
%Include qwtglobal.sip
%Include qwtgrid.sip
%Include qwtknob.sip
%Include qwtlegend.sip
%Include qwtlegendbutton.sip
%Include qwtmarker.sip
%Include qwtmarkerdict.sip
%Include qwtmath.sip
%Include qwtplot.sip
%Include qwtplotcanvas.sip
%Include qwtplotcurve.sip
%Include qwtplotgrid.sip
%Include qwtplotitem.sip
%Include qwtplotlayout.sip
%Include qwtplotmarker.sip
%Include qwtpaintbuffer.sip
%Include qwtpainter.sip
%Include qwtplotprintfilter.sip
%Include qwtrect.sip
%Include qwtscale.sip
%Include qwtscalediv.sip
%Include qwtscaledraw.sip
%Include qwtscaleif.sip
%Include qwtsliderbase.sip
%Include qwtslider.sip
%Include qwtspline.sip
%Include qwtsymbol.sip
%Include qwtthermo.sip
%Include qwtwheel.sip

// Image support
%Include qwtqimage.sip

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
