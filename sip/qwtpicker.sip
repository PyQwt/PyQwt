// The SIP interface definition for QwtPicker.
//
// Copyright (C) 2001-2003 Gerard Vermeulen
// Copyright (C) 2000 Mark Colclough
//
// This file is part of PyQwt
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
// link PyQwt dynamically with commercial, non-commercial or educational
// versions of Qt, PyQt and sip, and distribute PyQwt in this form, provided
// that equally powerful versions of Qt, PyQt and sip have been released under
// the terms of the GNU General Public License.
//
// If PyQwt is dynamically linked with commercial, non-commercial or
// educational versions of Qt, PyQt and sip, PyQwt becomes a free plug-in
// for a non-free program.


class QwtPicker: QObject, QwtEventPattern
{
%HeaderCode
#include <qwt_picker.h>
%End

public:
    enum SelectionType {
        NoSelection = 0,
        PointSelection = 1,
        RectSelection = 2,
        PolygonSelection = 4,
    };

    enum RectSelectionType {
        CornerToCorner = 64,
        CenterToCorner = 128,
        CenterToRadius = 256
    };

    enum SelectionMode {
        ClickSelection = 1024,
        DragSelection = 2048
    };

    enum RubberBand {
        NoRubberBand = 0,
        HLineRubberBand,
        VLineRubberBand,
        CrossRubberBand,
        RectRubberBand,
        EllipseRubberBand,
        PolygonRubberBand,
        UserRubberBand = 100
    };

    enum DisplayMode {
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
    QwtPicker(int, RubberBand,DisplayMode, QWidget *, const char * = 0);
    // virtual ~QwtPicker();

    virtual void setSelectionFlags(int);
    int selectionFlags() const;

    virtual void setRubberBand(RubberBand);
    bool rubberBand() const;

    virtual void setCursorLabelMode(DisplayMode);
    DisplayMode cursorLabelMode() const;

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

    QWidget *parentWidget();
    // dead code: const QWidget *parentWidget() const;

    virtual QRect pickRect() const;
    const QPointArray &selection() const;

signals:
    void selected(const QPointArray &);
    void appended(const QPoint &);
    void moved(const QPoint &);
    void changed(const QPointArray &);

protected:
    virtual bool accept(QPointArray &) const;

    virtual void begin();
    virtual void append(const QPoint &);
    virtual void move(const QPoint &);
    virtual bool end(bool = TRUE);

    virtual void widgetMousePressEvent(QMouseEvent *);
    virtual void widgetMouseReleaseEvent(QMouseEvent *);
    virtual void widgetMouseDoubleClickEvent(QMouseEvent *);
    virtual void widgetMouseMoveEvent(QMouseEvent *);
    virtual void widgetWheelEvent(QWheelEvent *);
    virtual void widgetKeyPressEvent(QKeyEvent *);
    virtual void widgetKeyReleaseEvent(QKeyEvent *);

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
