// The SIP interface definition file for QwtPlot.
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


class QwtPlot: QFrame
{
%TypeHeaderCode
#include <qwt_plot.h>
%End

public:
    enum Axis {
	yLeft,
	yRight,
	xBottom,
	xTop,
	axisCnt,
    };
    enum Position {
	Left,
	Right,
	Bottom,
	Top,
    };

    QwtPlot(QWidget * /TransferThis/ = 0, const char * = 0);
    QwtPlot(const QString &, QWidget * /TransferThis/ = 0, const char * = 0);

    void enableXBottomAxis(bool);
    bool xBottomAxisEnabled() const;
    void enableXTopAxis(bool);
    bool xTopAxisEnabled() const;
    void enableYRightAxis(bool);
    bool yRightAxisEnabled() const;
    void enableYLeftAxis(bool);
    bool yLeftAxisEnabled() const;

    void setAutoReplot(bool = 1);
    bool autoReplot() const;

    void print(QPaintDevice &,
	       const QwtPlotPrintFilter & = QwtPlotPrintFilter()) const
	/PyName=printPlot/;
    virtual void print(QPainter *, const QRect &,
		       const QwtPlotPrintFilter & = QwtPlotPrintFilter()) const
	/PyName=printPlot/;

%If (Qwt_COMPAT)
    // Outline

    void enableOutline(bool);
    bool outlineEnabled() const;
    void setOutlineStyle(Qwt::Shape);
    Qwt::Shape outlineStyle() const;
    void setOutlinePen(const QPen &);
    const QPen& outlinePen() const;
%End

    // Layout

    QwtPlotLayout *plotLayout();
    // dead code: const QwtPlotLayout *plotLayout() const;

    void setMargin(int);
    int margin() const;

    // Title
    void setTitle(const QString &);
    QString title() const;
    void setTitleFont (const QFont &);
    QFont titleFont() const;

    QLabel *titleLabel();
    const QLabel *titleLabel() const;

    // Canvas
    QwtPlotCanvas *canvas();
    const QwtPlotCanvas *canvas() const;

    void setCanvasBackground (const QColor &);
    const QColor& canvasBackground() const;

    void setCanvasLineWidth(int);
    int canvasLineWidth() const;

    // FIXME: QwtPlotCurveIterator curveIterator() const;
    // FIXME: QwtPlotMarkerIterator markerIterator() const;

    QwtDiMap canvasMap(int) const;

    double invTransform(int, int) const;
    int transform(int, double) const;

    // Curves

    long insertCurve(QwtPlotCurve *);
    long insertCurve(const QString &, int = xBottom, int = yLeft);

    QwtPlotCurve *curve(long);
    // dead code: const QwtPlotCurve *curve(long) const;

    QwtArray<long> curveKeys() const;
    long closestCurve(int, int, int & /Out/,
                      double & /Out/, double & /Out/, int & /Out/) const;

    bool setCurveBaseline(long, double);
    double curveBaseline(long) const;

    bool setCurveData(long, SIP_PYOBJECT, SIP_PYOBJECT);
%MethodCode
    QwtArray<double> xArray;
    if (-1 == try_PyObject_to_QwtArray(a1, xArray))
        return 0;

    QwtArray<double> yArray;
    if (-1 == try_PyObject_to_QwtArray(a2, yArray))
        return 0;

    Py_BEGIN_ALLOW_THREADS
    sipRes = sipCpp->setCurveData(a0, xArray, yArray);
    Py_END_ALLOW_THREADS
%End

    bool setCurveOptions(long, int);
    int curveOptions(long) const;

    bool setCurvePen(long, const QPen &);
    QPen curvePen(long) const;

    bool setCurveBrush(long, const QBrush &);
    QBrush curveBrush(long) const;

    bool setCurveSplineSize(long, int);
    int curveSplineSize(long) const;

    bool setCurveStyle(long, int, int = 0);
    int curveStyle(long) const;

    bool setCurveSymbol(long, const QwtSymbol &);
    QwtSymbol curveSymbol(long) const;

    bool setCurveTitle(long, const QString &);
    QString curveTitle(long) const;

    bool setCurveXAxis(long, int);
    int curveXAxis(long) const;
    bool setCurveYAxis(long, int);
    int curveYAxis(long) const;

    void drawCurve(long, int, int);

    // Grid

    void enableGridX(bool = 1);
    void enableGridXMin(bool = 1);
    void enableGridY(bool = 1);
    void enableGridYMin(bool = 1);

    bool gridXEnabled() const;
    bool gridXMinEnabled() const;
    bool gridYEnabled() const;
    bool gridYMinEnabled() const;

    void setGridXAxis(int);
    int gridXAxis() const;
    void setGridYAxis(int);
    int gridYAxis() const;

    void setGridPen(const QPen &);
    void setGridMajPen(const QPen &);
    const QPen& gridMajPen();
    void setGridMinPen(const QPen &);
    const QPen& gridMinPen();

    QwtPlotGrid &grid();
    // dead code: const QwtPlotGrid &grid() const;

    // Axes

    void setAxisAutoScale(int);
    bool axisAutoScale(int) const;

    void enableAxis(int, bool = 1);
    bool axisEnabled(int) const;

    void changeAxisOptions(int, int, bool);
    void setAxisOptions(int, int);
    int axisOptions(int) const;

    void setAxisFont(int, const QFont &);
    const QFont axisFont(int);

    void setAxisMargins(int, double, double);
    bool axisMargins(int, double & /Out/, double & /Out/) const;

    void setAxisScale(int, double, double, double = 0.0);
    void setAxisScaleDraw(int, QwtScaleDraw * /Transfer/);
    const QwtScaleDiv *axisScale(int) const;
    const QwtScaleDraw *axisScaleDraw(int) const;
    const QwtScale *axis(int) const;

    void setAxisLabelFormat(int, char, int);
    void axisLabelFormat(int, char & /Out/, int & /Out/, int & /Out/) const;

    void setAxisLabelAlignment(int, int);
    void setAxisLabelRotation(int, double);

    void setAxisTitle(int, const QString &);
    const QString axisTitle(int) const;
    void setAxisTitleFont(int, const QFont &);
    QFont axisTitleFont(int) const;
    void setAxisTitleAlignment(int, int);
    int axisTitleAlignment(int) const;

    void setAxisMaxMinor(int, int);
    int axisMaxMajor(int) const;
    void setAxisMaxMajor(int, int);
    int axisMaxMinor(int) const;

    void setAxisReference(int, double);
    double axisReference(int) const;

    // Markers

    long insertMarker(QwtPlotMarker *);
    long insertMarker(
	const QString & = QString::null, int = xBottom, int = yLeft);
    long insertLineMarker(const QString, int);

    QwtPlotMarker *marker(long);
    // dead code: const QwtPlotMarker *marker(long) const;

    long closestMarker(int, int, int & /Out/) const;
    QwtArray<long> markerKeys() const;

    bool setMarkerXAxis(long, int);
    int markerXAxis(long) const;
    bool setMarkerYAxis(long, int);
    int markerYAxis(long) const;

    bool setMarkerPos(long, double, double);
    bool setMarkerXPos(long, double);
    bool setMarkerYPos(long, double);
    void markerPos(long, double & /Out/, double & /Out/) const;

    bool setMarkerFont(long, const QFont &);
    QFont markerFont(long) const;
    bool setMarkerPen(long, const QPen &);

    bool setMarkerLabel(long, const QString &, const QFont & = QFont(),
                        const QColor & = QColor(),
                        const QPen & = QPen(Qt::NoPen),
                        const QBrush & = QBrush(Qt::NoBrush));
    bool setMarkerLabelText(long, const QString &);
    const QString markerLabel(long) const;
    bool setMarkerLabelAlign(long, int);
    int markerLabelAlign(long) const;
    bool setMarkerLabelPen(long, const QPen &);
    QPen markerLabelPen(long) const;

    bool setMarkerLinePen(long, const QPen &);
    QPen markerLinePen(long) const;
    bool setMarkerLineStyle(long, QwtMarker::LineStyle);
    QwtMarker::LineStyle markerLineStyle(long) const;

    bool setMarkerSymbol(long, const QwtSymbol &);
    QwtSymbol markerSymbol(long) const;

    // Legend

    void setAutoLegend(bool);
    bool autoLegend() const;

    void enableLegend(bool, long = -1);
    bool legendEnabled(long) const;

    void setLegendPosition(Position, double);

    void setLegendPosition(Position);
    Position legendPosition() const;

%If (Qwt_COMPAT)
    void setLegendPos(int, double = 0.0);
    int legendPos() const;
%End

    void setLegendFont(const QFont &);
    const QFont legendFont() const;

    void setLegendFrameStyle(int);
    int legendFrameStyle() const;

    QwtLegend *legend();
    // dead code: const QwtLegend *legend() const;

    void setLegendDisplayPolicy(QwtLegend::LegendDisplayPolicy, int = -1);
    
    // Misc

    virtual QSize sizeHint() const;
    virtual QSize minimumSizeHint() const;
    virtual QSizePolicy sizePolicy() const;

    virtual bool event(QEvent *);
    
public slots:
    void clear();

    bool removeCurve(long);
    void removeCurves();

    bool removeMarker(long);
    void removeMarkers();

    virtual void replot();

protected slots:
    virtual void lgdClicked();

%If (Qwt_COMPAT)
signals:
    void plotMousePressed(const QMouseEvent &);
    void plotMouseReleased(const QMouseEvent &);
    void plotMouseMoved(const QMouseEvent &);
%End
signals:
    void legendClicked(long);

protected:
    void autoRefresh();
    static bool axisValid(int);

    virtual void drawCanvas(QPainter *);
    virtual void drawCanvasItems(QPainter *,
                                 const QRect &, 
                                 const QwtArray<QwtDiMap> &,
                                 const QwtPlotPrintFilter &) const;
    virtual void drawContents(QPainter *);

    virtual void updateTabOrder();

    void updateAxes();
    void updateLayout();

    virtual void resizeEvent(QResizeEvent *);

    virtual void insertLegendItem(long);
    virtual void updateLegendItem(long);
    virtual void printLegendItem(
        QPainter *, const QWidget *, const QRect &) const;

    virtual void printTitle(QPainter *, const QRect &) const;
    virtual void printScale(
	QPainter *, int, int, int, int, const QRect &) const;
    virtual void printCanvas(QPainter *,
                             const QRect &,
                             const QwtArray<QwtDiMap> &,
                             const QwtPlotPrintFilter &) const;
    virtual void printLegend(QPainter *, const QRect &) const;
};

// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// End:
