// The SIP interface definition for QwtPlotZoom.
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


%MappedType QValueStack<QwtDoubleRect>
{
%HeaderCode
#include <qwt_array.h>
#include <qvaluestack.h>
%End

%ConvertFromTypeCode
    if (!sipCpp)
        return PyList_New(0);
    
    // FIXME: works because QValueStack is derived from QList 
    PyObject *l = PyList_New(sipCpp->count());;

    if (0 == l)
        return 0;

    for (int i = 0; i < int(sipCpp->count()); i++) {
        PyObject *o;
        if ((0 == (o = sipNewCppToSelf(new QwtDoubleRect((*sipCpp)[i]),
                                       sipClass_QwtDoubleRect,
                                       SIP_SIMPLE | SIP_PY_OWNED)))
            || (-1 == PyList_SetItem(l, i, o))) {
            Py_DECREF(l);
            return 0;
        }             
    }
    
    return l;
%End

%ConvertToTypeCode
    if (0 == sipIsErr)
        return PyList_Check(sipPy);

    // FIXME: can we use the fact that QValueStack is derived from QList? 
    QValueStack<QwtDoubleRect> *c = new QValueStack<QwtDoubleRect>;
    int iserr = 0;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
        c->push(*(QwtDoubleRect *)(sipForceConvertTo_QwtDoubleRect(
                                        PyList_GET_ITEM(sipPy, i), &iserr)));

        if (iserr) {
            delete c;
            *sipIsErr = 1;
            
            return 0;
        }
    }

    *sipCppPtr = c;

    return 1;
%End
};


class QwtPlotZoom: QwtPicker
{
%HeaderCode
#include <qwt_plot_zoom.h>
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

    QwtPlotZoom(QwtPlotCanvas *, const char * = 0);

    virtual void setZoomBase();

    QwtDoubleRect zoomBase() const;
    QwtDoubleRect zoomRect() const;

    void setAxis(int, int);
    // not implemented: void setXAxis(int);
    // not implemented: void setYAxis(int);

    int xAxis() const;
    int yAxis() const;

    void setMaxStackDepth(int);
    int maxStackDepth() const;

    // not implemented: const QValueStack<QwtDoubleRect> &zoomStack() const;

    QwtPlot *plot();
    // dead code: const QwtPlot *plot() const;
    
public slots:
    void moveBy(double, double);
    virtual void move(double, double);

    virtual void setZoomBase(const QwtDoubleRect &);
    virtual void zoom(const QwtDoubleRect &);

    virtual void unzoom(int = -1);

signals:
    void zoomed(const QwtDoubleRect &);

protected:
    // not implemented: QValueStack<QwtDoubleRect> &zoomStack();

    virtual void rescale();

    virtual bool isValidSelection(QRect &) const;
    virtual QwtDoubleSize minZoomSize() const;

    virtual void canvasMousePressEvent(QMouseEvent *);
    virtual void canvasMouseReleaseEvent(QMouseEvent *);

    QwtDoubleRect scaleRect() const;

    virtual QString cursorLabel(const QPoint &) const;
    virtual QString cursorLabel(double, double) const;
    virtual void end(bool = TRUE);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
