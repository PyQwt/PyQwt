// The SIP interface definition file for QwtScale.
//
// Copyright (C) 2001-2004 Gerard Vermeulen
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
// educational versions of Qt, PyQt and sip, PyQwt becomes a free plug-in
// for a non-free program.


class QwtScale: QWidget
{
%TypeHeaderCode
#include <qwt_scale.h>
%End

public:
    enum Position {
	Left,
	Right,
	Top,
	Bottom,
    };

    QwtScale(QWidget * /TransferThis/ = 0, const char * = 0);
    QwtScale(Position, QWidget * /TransferThis/, const char * = 0);
    virtual ~QwtScale();
    
    void setTitle(const QString &);
    const QString title() const;

    void setTitleColor(const QColor &);
    const QColor titleColor() const;

    void setTitleFont(const QFont &);
    const QFont titleFont() const;

    void setTitleAlignment(int);
    int titleAlignment() const;

    void setBorderDist(int, int);
    int startBorderDist() const;
    int endBorderDist() const;
    void minBorderDist(int & /Out/, int & /Out/) const;

    void setBaselineDist(int);
    int baseLineDist() const;

    void setScaleDiv(const QwtScaleDiv &);
    void setScaleDraw(QwtScaleDraw *);
    const QwtScaleDraw *scaleDraw() const;

    void setLabelFormat(char, int, int);
    void labelFormat(char & /Out/, int & /Out/, int & /Out/) const;

    void setLabelAlignment(int);
    void setLabelRotation(double);

    QSize sizeHint() const;
    virtual QSize minimumSizeHint() const;
    virtual QSizePolicy sizePolicy() const;

    int titleHeightForWidth(int) const;
    int dimForLength(int, const QFontMetrics &) const;

    void drawTitle(QPainter *, QwtScaleDraw::Orientation, const QRect &);

    void setPosition(Position);
    Position position() const;

protected:
    void draw(QPainter *) const;
    void paintEvent(QPaintEvent *);
    void resizeEvent(QResizeEvent *);
    void scaleChange();
    void fontChange(const QFont &);
    void layoutScale(bool = 1);
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
