// The SIP interface definition for QwtLegend.
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


class QwtLegend: QScrollView
{
%HeaderCode
#include <qwt_legend.h>
%End

public:
    enum LegendDisplayPolicy
    {
        None = 0,
        Fixed = 1,
        Auto = 2
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtLegend(QWidget * /TransferThis/ = 0, const char * = 0);

    void setReadOnly(bool);
    bool isReadOnly() const;

    void setDisplayPolicy(LegendDisplayPolicy, int = -1);
    LegendDisplayPolicy displayPolicy() const;

    int identifierMode() const;

    QWidget *contentsWidget();    
    // dead code: const QWidget *contentsWidget() const;

    void insertItem(QWidget *, long);
    QWidget *findItem(long);
    // dead code: const QWidget *findItem() const;
    QWidget *takeItem(long);

    // FIXME: virtual QIntDictIterator<QWidget> itemIterator() const;

    long key(const QWidget *) const;

    void clear();

    bool isEmpty() const;
    uint itemCount() const;

    virtual bool eventFilter(QObject *, QEvent *);
    virtual QSize sizeHint() const;
    virtual int heightForWidth(int) const;

protected:
    virtual void viewportResizeEvent(QResizeEvent *);
    virtual void layoutContents();
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
