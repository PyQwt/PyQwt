// The SIP interface definition for QwtCounter.
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


class QwtCounter: QWidget, QwtDblRange
{
%TypeHeaderCode
#include <qwt_counter.h>
%End

public:
    enum Button {
	Button1,
	Button2,
	Button3,
	ButtonCnt,
    };

    QwtCounter(QWidget * /TransferThis/ = 0, char * = 0);
  
%If (QWT_4_3_0 -)
    bool editable() const;
    void setEditable(bool);
%End // (QWT_4_3_0 -)

    void setNumButtons(int);
    int numButtons() const;

    void setIncSteps(QwtCounter::Button, int);
    int incSteps(QwtCounter::Button) const;

    virtual void setValue(double);
    virtual QSizePolicy sizePolicy() const;
    virtual QSize sizeHint() const;

    virtual bool eventFilter(QObject *, QEvent *);

    double step() const;
    void setStep(double);
    double minVal() const;
    void setMinValue(double);
    double maxVal() const;
    void setMaxValue(double);
    void setStepButton1(int);
    int stepButton1() const;
    void setStepButton2(int);
    int stepButton2() const;
    void setStepButton3(int);
    int stepButton3() const;
    virtual double value() const;

signals:
    void buttonReleased(double);  
    void valueChanged(double);

protected:
    virtual void rangeChange();
    virtual void fontChange(const QFont &);

private slots:
    void btnReleased();
    void btnClicked();

private:
    void updateButtons();
    void showNum(double);
    virtual void valueChange();
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
