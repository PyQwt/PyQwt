// The SIP interface definition for QwtSliderBase.
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


class QwtSliderBase: QWidget, QwtDblRange
{
%HeaderCode
#include <qwt_sldbase.h>
%End

public:
    enum {
	ScrNone,
	ScrMouse,
	ScrTimer,
	ScrDirect,
	ScrPage
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtSliderBase(Qt::Orientation, QWidget * /TransferThis/ = 0,
		  const char * = 0, WFlags = 0);

    void setUpdateTime(int);
    void stopMoving();
    void setTracking(bool);

    virtual void setMass(double);
    virtual double mass() const;

    virtual void setOrientation(Orientation);
    Orientation orientation() const;

    bool isReadOnly() const;

    bool isValid() const;
    void setValid(bool);

public slots:
    void setValue(double);
    void fitValue(double);
    void incValue(int);

    virtual void setReadOnly(bool);
	
signals:
    void valueChanged(double);
    void sliderPressed();
    void sliderReleased();
    void sliderMoved(double);

protected:
    void setPosition(const QPoint &);
    virtual void valueChange();

    virtual void timerEvent(QTimerEvent *);
    virtual void mousePressEvent(QMouseEvent *);
    virtual void mouseReleaseEvent(QMouseEvent *);
    virtual void mouseMoveEvent(QMouseEvent *);
    virtual void keyPressEvent(QKeyEvent *);
    virtual void wheelEvent(QWheelEvent *);

    virtual double getValue(const QPoint &) = 0;
    virtual void getScrollMode(const QPoint &, int &, int &) = 0;
    // see 'virtual State QValidator::validate(QString &, int &) = 0;'
    // see 'virtual void getButtonShift(int &, int &) = 0;
%MemberCode
    // The Python interface takes a QPoint and returns a tuple.
    QPoint *point;
    sipQwtSliderBase *ptr;

    if (sipParseArgs(&sipArgsParsed, sipArgs, "pJ1",
 		     sipThisObj, sipClass_QwtSliderBase, &ptr,
		     sipClass_QPoint, &point)) {
	int scrollMode, direction;

	Py_BEGIN_ALLOW_THREADS
	ptr->getScrollMode(*point, scrollMode, direction);
	Py_END_ALLOW_THREADS
	
	return Py_BuildValue("(ii)", scrollMode, direction);
    }
%End
%VirtualCode
    // The Python interface takes a QPoint and returns a tuple.
    PyObject *pyArgs, *pyRes;

    if (0 == (pyArgs = Py_BuildValue(
	"ON", sipThis->sipSelf, sipMapCppToSelf(&a0, sipClass_QPoint))))
	goto reperr;

    pyRes = sipEvalMethod(&pymc->pyMethod, pyArgs);

    Py_DECREF(pyArgs);

    if (0 != pyRes) {
	int scrollMode, direction, rc;

	rc = PyArg_ParseTuple(pyRes, "ii", &scrollMode, &direction);
	Py_DECREF(pyRes);
	if (rc) {
	    a1 = scrollMode;
	    a2 = direction;
	    goto releaseLock;
	}
#ifdef OLD_SIP_NAMES
	sipBadVirtualResultType(sipName_qwt_QwtSliderBase,
				sipName_qwt_getScrollMode);
#else
	sipBadVirtualResultType(sipName_QwtSliderBase,
				sipName_getScrollMode);
#endif
    }
reperr:
    PyErr_Print();
releaseLock:
    SIP_UNBLOCK_THREADS
%End
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
