// The SIP interface definition for
//	QwtText,
//	QwtPlainText,
//	QwtRichText.
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


class QwtText
{
%HeaderCode
#include <qwt_text.h>
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

    static QwtText *makeText(const QString &, const QFont &, int,
                             const QColor & = QColor(),
                             Qt::TextFormat = Qt::AutoText);

    virtual void setText(const QString &);
    QString text() const;

    virtual void setFont(const QFont &);
    QFont font() const;
    QFontMetrics fontMetrics() const;

    virtual void setAlignment(int);
    int alignment() const;

    virtual void setColor(const QColor &);
    QColor color() const;

    virtual int heightForWidth(int) const = 0;
    virtual QRect boundingRect(QPainter * = 0) const = 0;

    virtual void draw(QPainter *, const QRect &) const = 0;

protected:
    QwtText(QString &, const QFont &, int, const QColor &);
};

class QwtPlainText: QwtText
{
%HeaderCode
#include <qwt_text.h>
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

    QwtPlainText(const QString &, const QFont &,
                int = Qt::AlignCenter | Qt::WordBreak | Qt::ExpandTabs,
                const QColor & = QColor());
    //FIXME QwtPlainText(const QString &, const QFont &, const QColor & = QColor());

    virtual int heightForWidth(int) const;
    virtual QRect boundingRect(QPainter * = 0) const;

    virtual void draw(QPainter *, const QRect &) const;
};

class QwtRichText: QwtText
{
%HeaderCode
#include <qwt_text.h>
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

    QwtRichText(const QString &, const QFont &,
                int = Qt::AlignCenter | Qt::WordBreak | Qt::ExpandTabs,
                const QColor & = QColor());
    QwtRichText(const QString &, const QFont &, const QColor &);

    virtual void setText(const QString &);
    virtual void setFont(const QFont &);
    virtual void setAlignment(int);

    virtual int heightForWidth(int) const;
    virtual QRect boundingRect(QPainter * = 0) const;

    virtual void draw(QPainter *, const QRect &) const;
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
