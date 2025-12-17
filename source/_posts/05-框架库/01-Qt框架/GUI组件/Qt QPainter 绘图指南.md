---
tags:
  - Qt
  - QPainter
  - 绘图
  - 自定义控件
  - 2D图形
  - C++
title: Qt QPainter 绘图指南
categories:
  - C++核心开发
  - Qt框架
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: 38ea5a46
date: 2025-12-04 13:13:21
---

# Qt QPainter 绘图指南
## 目录
- [概述](#概述)
- [QPainter 核心概念](#qpainter-核心概念)
- [示例1：绘制基础图形](#示例1绘制基础图形)
- [示例2：绘制高级路径与形状](#示例2绘制高级路径与形状)
- [示例3：渲染文本](#示例3渲染文本)
- [示例4：绘制与变换图像](#示例4绘制与变换图像)
- [示例5：应用渐变和特效](#示例5应用渐变和特效)
- [示例6：自定义控件 (圆形进度条)](#示例6自定义控件-圆形进度条)
- [性能优化](#性能优化)
- [常见问题](#常见问题)

## 概述

本指南详细介绍如何使用 Qt 的 `QPainter` 类实现各种 2D 绘图功能。与原文将所有功能塞入一个类不同，本指南将功能拆分为多个独立的示例控件，以展示更清晰的编程实践。

## QPainter 核心概念

- **Paint Engine**: `QPainter` 是一个高级 API，它可以在不同的“绘图引擎”上进行绘制，例如在 `QWidget`、`QPixmap` 或 `QImage` 上。
- **Paint Event**: 在自定义 `QWidget` 中，所有的绘制代码都应在 `paintEvent()` 这个虚函数中完成。
- **State Machine**: `QPainter` 是一个状态机。你设置的 `QPen`（画笔）、`QBrush`（画刷）、`QFont`（字体）等会一直保持，直到你再次修改它们。可以使用 `painter.save()` 和 `painter.restore()` 来保存和恢复状态。
- **Render Hints**: 通过 `painter.setRenderHint()` 可以开启抗锯齿等功能，提升绘图质量。

## 示例1：绘制基础图形

这个控件演示如何绘制直线、矩形、圆形等基本形状。

`basic_shapes_widget.h`:
```cpp
#ifndef BASICSHAPESWIDGET_H
#define BASICSHAPESWIDGET_H

#include <QWidget>

class BasicShapesWidget : public QWidget {
    Q_OBJECT
public:
    explicit BasicShapesWidget(QWidget *parent = nullptr);

protected:
    void paintEvent(QPaintEvent *event) override;
};

#endif // BASICSHAPESWIDGET_H
```

`basic_shapes_widget.cpp`:
```cpp
#include "basic_shapes_widget.h"
#include <QPainter>
#include <QPaintEvent>

BasicShapesWidget::BasicShapesWidget(QWidget *parent) : QWidget(parent) {
    setMinimumSize(400, 250);
    setWindowTitle("Basic Shapes");
}

void BasicShapesWidget::paintEvent(QPaintEvent *event) {
    Q_UNUSED(event);
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);

    // 1. 设置画笔 (用于轮廓)
    QPen pen(Qt::blue, 2, Qt::SolidLine, Qt::RoundCap, Qt::RoundJoin);
    painter.setPen(pen);

    // 2. 设置画刷 (用于填充)
    QBrush brush(QColor(150, 200, 255, 128)); // 半透明蓝色
    painter.setBrush(brush);

    // 3. 绘制图形
    painter.drawRect(10, 10, 100, 80); // 矩形
    painter.drawEllipse(130, 10, 100, 80); // 椭圆
    painter.drawRoundedRect(10, 110, 100, 80, 15, 15); // 圆角矩形
    painter.drawEllipse(QPoint(180, 150), 50, 50); // 圆形

    // 4. 只用画笔，不用画刷
    painter.setBrush(Qt::NoBrush);
    painter.setPen(Qt::red);
    painter.drawLine(250, 10, 350, 110);
}
```

## 示例2：绘制高级路径与形状

`QPainterPath` 允许你组合多个图元，创建复杂的形状，例如贝塞尔曲线、多边形等。

`advanced_shapes_widget.h`:
```cpp
#ifndef ADVANCEDSHAPESWIDGET_H
#define ADVANCEDSHAPESWIDGET_H

#include <QWidget>

class AdvancedShapesWidget : public QWidget {
    Q_OBJECT
public:
    explicit AdvancedShapesWidget(QWidget *parent = nullptr);

protected:
    void paintEvent(QPaintEvent *event) override;
};

#endif // ADVANCEDSHAPESWIDGET_H
```

`advanced_shapes_widget.cpp`:
```cpp
#include "advanced_shapes_widget.h"
#include <QPainter>
#include <QPainterPath>
#include <cmath> // For M_PI

AdvancedShapesWidget::AdvancedShapesWidget(QWidget *parent) : QWidget(parent) {
    setMinimumSize(400, 300);
    setWindowTitle("Advanced Shapes");
}

void AdvancedShapesWidget::paintEvent(QPaintEvent *event) {
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);
    painter.setPen(QPen(Qt::darkGreen, 2));

    // 1. 绘制多边形
    QPolygonF polygon;
    polygon << QPointF(10, 10) << QPointF(10, 90) << QPointF(110, 70) << QPointF(90, 20);
    painter.drawPolygon(polygon);

    // 2. 绘制贝塞尔曲线
    QPainterPath bezierPath;
    bezierPath.moveTo(150, 50);
    bezierPath.cubicTo(200, 10, 250, 100, 300, 60);
    painter.drawPath(bezierPath);

    // 3. 绘制一个复杂的路径（例如心形）
    QPainterPath heartPath;
    heartPath.moveTo(200, 150);
    heartPath.cubicTo(250, 120, 280, 180, 200, 250);
    heartPath.cubicTo(120, 180, 150, 120, 200, 150);
    painter.setBrush(Qt::red);
    painter.drawPath(heartPath);
}
```

## 示例3：渲染文本

`QPainter` 提供了强大的文本渲染功能。

`text_rendering_widget.h` / `.cpp` (结构同上):
```cpp
// In paintEvent of TextRenderingWidget
void TextRenderingWidget::paintEvent(QPaintEvent *event) {
    QPainter painter(this);
    painter.setRenderHint(QPainter::TextAntialiasing, true);

    // 1. 基础文本
    painter.setFont(QFont("Arial", 12));
    painter.setPen(Qt::black);
    painter.drawText(10, 20, "Hello, QPainter!");

    // 2. 带样式的文本
    painter.setFont(QFont("Times New Roman", 20, QFont::Bold, true));
    painter.setPen(Qt::darkBlue);
    painter.drawText(10, 60, "Styled Text");

    // 3. 旋转文本
    painter.save(); // 保存当前状态
    painter.translate(100, 150);
    painter.rotate(-45);
    painter.drawText(0, 0, "Rotated Text");
    painter.restore(); // 恢复之前状态

    // 4. 在矩形内换行
    QRectF textRect(200, 10, 180, 100);
    painter.drawRect(textRect); // 画出边界方便观察
    QString longText = "This is a long text that will wrap inside the specified rectangle.";
    painter.drawText(textRect, Qt::TextWordWrap, longText);
}
```

## 示例4：绘制与变换图像

`QPainter` 可以绘制 `QPixmap` 和 `QImage`，并对其进行实时变换。

`image_drawing_widget.h` / `.cpp` (结构同上):
```cpp
// In paintEvent of ImageDrawingWidget
void ImageDrawingWidget::paintEvent(QPaintEvent *event) {
    QPainter painter(this);
    painter.setRenderHint(QPainter::SmoothPixmapTransform, true);

    // 准备一张测试图片 (也可以从文件加载: QPixmap(":/images/logo.png"))
    QPixmap pixmap(100, 100);
    pixmap.fill(Qt::cyan);
    QPainter p(&pixmap);
    p.drawText(pixmap.rect(), Qt::AlignCenter, "Qt");
    p.end();

    // 1. 正常绘制
    painter.drawPixmap(10, 10, pixmap);

    // 2. 缩放绘制
    painter.drawPixmap(120, 10, 150, 150, pixmap);

    // 3. 旋转绘制
    painter.save();
    painter.translate(100, 200); // 移动坐标系
    painter.rotate(45); // 旋转
    painter.drawPixmap(-50, -50, 100, 100, pixmap); // 在新坐标系原点绘制
    painter.restore();

    // 4. 透明度绘制
    painter.setOpacity(0.5);
    painter.drawPixmap(200, 180, pixmap);
    painter.setOpacity(1.0); // 恢复不透明
}
```

## 示例5：应用渐变和特效

使用 `QGradient` 系列类可以创建漂亮的渐变效果。

`gradients_widget.h` / `.cpp` (结构同上):
```cpp
// In paintEvent of GradientsWidget
void GradientsWidget::paintEvent(QPaintEvent *event) {
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);
    painter.setPen(Qt::NoPen);

    // 1. 线性渐变
    QLinearGradient linearGrad(0, 0, 100, 100);
    linearGrad.setColorAt(0, Qt::red);
    linearGrad.setColorAt(1, Qt::yellow);
    painter.setBrush(linearGrad);
    painter.drawRect(10, 10, 100, 100);

    // 2. 径向渐变
    QRadialGradient radialGrad(180, 60, 50);
    radialGrad.setColorAt(0, Qt::white);
    radialGrad.setColorAt(1, Qt::blue);
    painter.setBrush(radialGrad);
    painter.drawEllipse(130, 10, 100, 100);

    // 3. 锥形渐变
    QConicalGradient conicalGrad(60, 170, 0);
    conicalGrad.setColorAt(0, Qt::cyan);
    conicalGrad.setColorAt(0.5, Qt::magenta);
    conicalGrad.setColorAt(1, Qt::cyan);
    painter.setBrush(conicalGrad);
    painter.drawEllipse(10, 120, 100, 100);
}
```

## 示例6：自定义控件 (圆形进度条)

这是将 `QPainter` 用于实践的最好例子：创建一个标准库中没有的、完全自定义的控件。

`circular_progress_bar.h`:
```cpp
#ifndef CIRCULARPROGRESSBAR_H
#define CIRCULARPROGRESSBAR_H

#include <QWidget>
#include <QColor>

class CircularProgressBar : public QWidget {
    Q_OBJECT
    Q_PROPERTY(int value READ value WRITE setValue)
public:
    explicit CircularProgressBar(QWidget *parent = nullptr);
    int value() const { return m_value; }

public slots:
    void setValue(int value);

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    int m_value = 0;
    QColor m_backgroundColor = QColor(220, 220, 220);
    QColor m_progressColor = QColor(30, 144, 255);
};

#endif // CIRCULARPROGRESSBAR_H
```

`circular_progress_bar.cpp`:
```cpp
#include "circular_progress_bar.h"
#include <QPainter>

CircularProgressBar::CircularProgressBar(QWidget *parent) : QWidget(parent) {
    setMinimumSize(100, 100);
}

void CircularProgressBar::setValue(int value) {
    if (m_value != value) {
        m_value = qBound(0, value, 100);
        update(); // 请求重绘
    }
}

void CircularProgressBar::paintEvent(QPaintEvent *event) {
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);

    QRectF rect = this->rect().adjusted(5, 5, -5, -5);
    int startAngle = 90 * 16; // 12点钟方向
    int spanAngle = -static_cast<int>((m_value / 100.0) * 360.0 * 16.0);

    // 绘制背景环
    painter.setPen(QPen(m_backgroundColor, 8, Qt::SolidLine, Qt::FlatCap));
    painter.drawArc(rect, 0, 360 * 16);

    // 绘制进度环
    painter.setPen(QPen(m_progressColor, 8, Qt::SolidLine, Qt::RoundCap));
    painter.drawArc(rect, startAngle, spanAngle);

    // 绘制中心文本
    painter.setPen(m_progressColor);
    painter.setFont(QFont("Arial", 16, QFont::Bold));
    painter.drawText(rect, Qt::AlignCenter, QString::number(m_value) + "%");
}
```

## 性能优化

- **双缓冲**: `QWidget` 默认开启双缓冲，一般无需手动处理。对于非 `QWidget` 的绘图表面（如 `QPixmap`），双缓冲是隐式的。
- **减少重绘区域**: 在 `paintEvent` 中，只重绘 `event->rect()` 或 `event->region()` 提供的“脏区域”，而不是整个控件。
- **缓存**: 对于复杂且不常变化的背景或元素，可以将其预先绘制到一个 `QPixmap` 缓存上，在 `paintEvent` 中直接绘制该 `QPixmap` 即可。
- **避免在 `paintEvent` 中进行耗时操作**: 不要在 `paintEvent` 中创建复杂的对象或执行计算。所有数据都应提前准备好。

## 常见问题

**Q1: 绘图有锯齿，不平滑?**
**A**: 开启抗锯齿。`painter.setRenderHint(QPainter::Antialiasing, true);`

**Q2: 控件缩放时，内容会闪烁?**
**A**: `QWidget` 默认的双缓冲能处理大部分情况。如果问题依然存在，确保没有在 `resizeEvent` 中调用 `update()`，而应让系统自动触发 `paintEvent`。

**Q3: 如何在高DPI屏幕上保证清晰度?**
**A**: 在 `main.cpp` 中启用高DPI支持：
```cpp
QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
```
Qt 会自动处理大部分DPI缩放。对于手动加载的 `QPixmap`，可能需要使用 `@2x` 后缀的资源或手动设置其 `devicePixelRatio`。
