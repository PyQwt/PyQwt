// The SIP interface definition for the Qwt module of PyQwt.
//
// Copyright (C) 2001-2003 Gerard Vermeulen
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
// educational versions of Qt, PyQt and sip, PyQwt becomes a free plug-in for
// a non-free program.


%Module qwt

%Include features.sip

%Import qtmod.sip

%HeaderCode
#include <qwt_python.h>
%End

%C++Code

// Hack: more than 1 sipSubClass_QObject() is not supported by sip.
// So we do it, with a little bit of help from pyqwt_sip_output_patch.py

static PyObject *sipSubClass_QObject(const QObject *sipCpp)
{
    // The table of Python class objects indexed by their names.
    // The table must be sorted by name.
#ifdef OLD_SIP_NAMES
    static sipStringTypeClassMap map[] = {
        { sipName_qwt_QwtAnalogClock, &sipClass_QwtAnalogClock },
        { sipName_qwt_QwtArrowButton, &sipClass_QwtArrowButton },
        { sipName_qwt_QwtCompass, &sipClass_QwtCompass },
        { sipName_qwt_QwtCounter, &sipClass_QwtCounter },
        { sipName_qwt_QwtDial, &sipClass_QwtDial },
        { sipName_qwt_QwtDynGridLayout, &sipClass_QwtDynGridLayout },
        { sipName_qwt_QwtKnob, &sipClass_QwtKnob },
        { sipName_qwt_QwtLegend, &sipClass_QwtLegend },
        { sipName_qwt_QwtLegendButton, &sipClass_QwtLegendButton },
        { sipName_qwt_QwtLegendLabel, &sipClass_QwtLegendLabel },
        { sipName_qwt_QwtPicker, &sipClass_QwtPicker },
        { sipName_qwt_QwtPlot, &sipClass_QwtPlot },
        { sipName_qwt_QwtPlotCanvas, &sipClass_QwtPlotCanvas },
        { sipName_qwt_QwtPlotPicker, &sipClass_QwtPlotPicker },
        { sipName_qwt_QwtPushButton, &sipClass_QwtPushButton },
        { sipName_qwt_QwtScale, &sipClass_QwtScale },
        { sipName_qwt_QwtSlider, &sipClass_QwtSlider },
        { sipName_qwt_QwtSliderBase, &sipClass_QwtSliderBase },
        { sipName_qwt_QwtThermo, &sipClass_QwtThermo },
        { sipName_qwt_QwtWheel, &sipClass_QwtWheel },
    };
#else
    static sipStringTypeClassMap map[] = {
        { sipName_QwtAnalogClock, &sipClass_QwtAnalogClock },
        { sipName_QwtArrowButton, &sipClass_QwtArrowButton },
        { sipName_QwtCompass, &sipClass_QwtCompass },
        { sipName_QwtCounter, &sipClass_QwtCounter },
        { sipName_QwtDial, &sipClass_QwtDial },
        { sipName_QwtDynGridLayout, &sipClass_QwtDynGridLayout },
        { sipName_QwtKnob, &sipClass_QwtKnob },
        { sipName_QwtLegend, &sipClass_QwtLegend },
        { sipName_QwtLegendButton, &sipClass_QwtLegendButton },
        { sipName_QwtLegendLabel, &sipClass_QwtLegendLabel },
        { sipName_QwtPicker, &sipClass_QwtPicker },
        { sipName_QwtPlot, &sipClass_QwtPlot },
        { sipName_QwtPlotCanvas, &sipClass_QwtPlotCanvas },
        { sipName_QwtPlotPicker, &sipClass_QwtPlotPicker },
        { sipName_QwtPushButton, &sipClass_QwtPushButton },
        { sipName_QwtScale, &sipClass_QwtScale },
        { sipName_QwtSlider, &sipClass_QwtSlider },
        { sipName_QwtSliderBase, &sipClass_QwtSliderBase },
        { sipName_QwtThermo, &sipClass_QwtThermo },
        { sipName_QwtWheel, &sipClass_QwtWheel },
    };
#endif

    return sipMapStringToClass(
        sipCpp->className(), map, sizeof(map)/sizeof(map[0]));
}
%End    

// Hack: improve rlcompleter support for PyQt & sip-3.6 and earlier
%Include qwtgetlazynames.sip

// Normal include files
%Include qwt.sip
%Include qwtanalogclock.sip
%Include qwtarray.sip
%Include qwtarrowbutton.sip
%Include qwtautoscale.sip
%Include qwtcompass.sip
%Include qwtcompassrose.sip
%Include qwtcounter.sip
%Include qwtcurve.sip
%Include qwtcurvedict.sip
%Include qwtdata.sip
%Include qwtdblrange.sip
%Include qwtdial.sip
%Include qwtdialneedle.sip
%Include qwtdimap.sip
%Include qwtdoublerect.sip
%Include qwtdyngridlayout.sip
%Include qwteventpattern.sip
%Include qwtglobal.sip
%Include qwtgrid.sip
%Include qwtknob.sip
%Include qwtlayoutmetrics.sip
%Include qwtlegend.sip
%Include qwtlegendbutton.sip
%Include qwtlegenditem.sip
%Include qwtlegendlabel.sip
%Include qwtmarker.sip
%Include qwtmarkerdict.sip
%Include qwtmath.sip
%Include qwtpicker.sip
%Include qwtpickermachine.sip
%Include qwtplot.sip
%Include qwtplotcanvas.sip
%Include qwtplotcurve.sip
%Include qwtplotgrid.sip
%Include qwtplotitem.sip
%Include qwtplotlayout.sip
%Include qwtplotmarker.sip
%Include qwtplotpicker.sip
%Include qwtplotzoomer.sip
%Include qwtpaintbuffer.sip
%Include qwtpainter.sip
%Include qwtplotprintfilter.sip
%Include qwtpushbutton.sip
%Include qwtrect.sip
%Include qwtscale.sip
%Include qwtscalediv.sip
%Include qwtscaledraw.sip
%Include qwtscaleif.sip
%Include qwtsliderbase.sip
%Include qwtslider.sip
%Include qwtspline.sip
%Include qwtsymbol.sip
%Include qwttext.sip
%Include qwtthermo.sip
%Include qwtvaluelist.sip
%Include qwtvaluestack.sip
%Include qwtwheel.sip

// Image support
%Include qwtqimage.sip

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
