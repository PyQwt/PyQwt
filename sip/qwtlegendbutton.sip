// The SIP interface definition for QwtLegendButton.
//
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


class QwtLegendButton: QwtPushButton
{
%HeaderCode
#include <qwt_legend.h>
%End

public:

    enum IdentifierMode
    {
        NoIdentifier = 0,
        ShowLine = 1,
        ShowSymbol = 2,
        ShowText = 4,
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtLegendButton(QWidget * = 0, const char * = 0);
    QwtLegendButton(const QwtSymbol &, const QPen &, const QString &,
		    QWidget * = 0, const char * = 0);

    int identifierMode() const;
    const QwtSymbol& symbol() const;
    const QPen& curvePen() const;

    void setIdentifierMode(int);
    void setSymbol(const QwtSymbol &);
    void setCurvePen(const QPen &);

    virtual void drawContents(QPainter *, const QRect &) const;

protected:
    virtual void updateIconset();
    virtual void drawButtonLabel(QPainter *);
    virtual void drawIdentifier(QPainter *, const QRect &) const;    
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
