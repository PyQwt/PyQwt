// The SIP interface definition for QwtPicker.
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


class QwtPicker: QObject
{
%HeaderCode
#include <qwt_picker.h>
%End

public:
    enum SelectionType {
        None,
        Point,
        Rect,
        Polygon,
    };

    enum SelectionMode {
        Drag,
        Click
    };

    enum CursorLabel {
        AlwaysOff,
        AlwaysOn,
        ActiveOnly
    };

    enum ResizeMode {
        Stretch,
        KeepSize
    };

%If (SIP_DUMB_DIR)
    void getLazyNames();
%MemberCode
    if (sipParseArgs(&sipArgsParsed, sipArgs, "")) {
	return getLazyNames(sipClassAttrTab_$C);
    }
%End
%End

    QwtPicker(QWidget * = 0, const char * = 0);
    virtual ~QwtPicker();

    virtual void setSelectionType(SelectionType);
    SelectionType selectionType() const;

    virtual void setSelectionMode(SelectionMode);
    SelectionMode selectionMode() const;

    virtual void setRubberBand(bool);
    bool rubberBand() const;

    virtual void setCursorLabel(CursorLabel);
    CursorLabel cursorLabel() const;

    virtual void setResizeMode(ResizeMode);
    ResizeMode resizeMode() const;

    virtual void setRubberBandPen(const QPen &);
    QPen rubberBandPen() const;

    virtual void setCursorLabelPen(const QPen &);
    QPen cursorLabelPen() const;

    virtual void setCursorLabelFont(const QFont &);
    QFont cursorLabelFont() const;

    bool isEnabled() const;
    virtual void setEnabled(bool);

    bool isActive() const;

    virtual bool event(QEvent *);
    virtual bool eventFilter(QObject *, QEvent *);

    QWidget *canvas();
    // dead code: const QWidget *canvas() const;

    virtual QRect pickRect() const;
    // dead code: const QPointArray &selection() const;

signals:
    void selected(const QPointArray &);

protected:
    QPointArray &selection();
    virtual void begin();
    virtual void append(const QPoint &);
    virtual void move(const QPoint &);
    virtual void end(bool = TRUE);


    virtual void canvasMousePressEvent(QMouseEvent *);
    virtual void canvasMouseReleaseEvent(QMouseEvent *);
    virtual void canvasMouseDoubleClickEvent(QMouseEvent *); 
    virtual void canvasMouseMoveEvent(QMouseEvent *); 
    virtual void canvasWheelEvent(QWheelEvent *);
    virtual void canvasKeyPressEvent(QKeyEvent *); 
    virtual void canvasKeyReleaseEvent(QKeyEvent *); 

    virtual void drawRubberBand(const QRect & = QRect()) const;
    virtual void drawRubberBand(QPainter *, 
        const QRect &, const QPointArray &) const;

    virtual void drawCursorLabel(const QRect & = QRect()) const;
    virtual void drawCursorLabel(QPainter *, const QRect &, 
        const QPoint &, const QPointArray &) const;

    virtual void stretchSelection(const QSize &, const QSize &);

    virtual QString cursorLabel(const QPoint &) const;
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
