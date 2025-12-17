---
title: Qt Model-View 架构指南
categories:
  - C++核心开发
  - Qt框架
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
tags:
  - Qt
  - C++
  - MVC
  - Model-View
  - Delegate
  - 架构设计
abbrlink: 4f2fc4b2
date: 2025-12-04 22:09:46
---

# Qt Model-View 架构指南
## 目录
- [概述：Model-View-Delegate 模式](#概述model-view-delegate-模式)
- [第一步：自定义数据模型 (Model)](#第一步自定义数据模型-model)
- [第二步：使用视图 (View) 展示数据](#第二步使用视图-view-展示数据)
- [第三步：自定义委托 (Delegate) 进行渲染](#第三步自定义委托-delegate-进行渲染)
- [第四步：使用代理模型 (Proxy Model) 实现排序与过滤](#第四步使用代理模型-proxy-model-实现排序与过滤)
- [第五步：组合应用](#第五步组合应用)
- [性能优化与最佳实践](#性能优化与最佳实践)

## 概述：Model-View-Delegate 模式

Qt 的 Model-View 架构是经典 MVC 模式的一种变体，它将 View（视图）和 Controller（控制器）的职责进一步划分：

- **Model (模型)**: 负责存储和管理数据。它不知道数据将如何被展示。这是数据的唯一真实来源。
- **View (视图)**: 负责以某种方式将模型中的数据展示给用户。它可以是列表 (`QListView`)、表格 (`QTableView`) 或树 (`QTreeView`)。
- **Delegate (委托)**: 负责控制数据项的渲染方式和编辑方式。它允许你高度自定义数据在视图中的外观和交互行为。

这种架构的核心优势在于**数据与表现的分离**，同一个数据模型可以被多个不同的视图以不同的方式展示，而无需复制数据。

## 第一步：自定义数据模型 (Model)

我们将创建一个联系人列表模型 `ContactModel`，它继承自 `QAbstractListModel`。

`contact_model.h`:
```cpp
#ifndef CONTACTMODEL_H
#define CONTACTMODEL_H

#include <QAbstractListModel>
#include <QStringList>
#include <QVector>

struct Contact {
    QString name;
    QString phone;
};

class ContactModel : public QAbstractListModel {
    Q_OBJECT

public:
    explicit ContactModel(QObject *parent = nullptr);

    // --- 必须重写的核心虚函数 ---
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // --- 用于 QML 或自定义 Delegate 的角色名称 ---
    QHash<int, QByteArray> roleNames() const override;

    // --- 自定义的数据操作方法 ---
    void addContact(const Contact &contact);
    void removeContact(int row);

private:
    QVector<Contact> m_contacts;
};

#endif // CONTACTMODEL_H
```

`contact_model.cpp`:
```cpp
#include "contact_model.h"

ContactModel::ContactModel(QObject *parent) : QAbstractListModel(parent) {
    // 添加一些初始数据
    addContact({"Alice", "+1-202-555-0173"});
    addContact({"Bob", "+44-20-7946-0958"});
}

int ContactModel::rowCount(const QModelIndex &parent) const {
    // 对于 List 模型，我们忽略 parent 参数
    if (parent.isValid()) return 0;
    return m_contacts.count();
}

QVariant ContactModel::data(const QModelIndex &index, int role) const {
    if (!index.isValid() || index.row() >= m_contacts.count()) {
        return QVariant();
    }

    const Contact &contact = m_contacts.at(index.row());

    // Qt::DisplayRole 是视图默认请求的文本角色
    if (role == Qt::DisplayRole) {
        return contact.name + " (" + contact.phone + ")";
    }
    // 也可以为其他角色提供数据，例如工具提示
    if (role == Qt::ToolTipRole) {
        return contact.name;
    }

    return QVariant();
}

void ContactModel::addContact(const Contact &contact) {
    // 在插入数据前，必须调用 beginInsertRows
    beginInsertRows(QModelIndex(), rowCount(), rowCount());
    m_contacts.append(contact);
    // 插入数据后，必须调用 endInsertRows，这会通知所有视图进行更新
    endInsertRows();
}

void ContactModel::removeContact(int row) {
    if (row < 0 || row >= m_contacts.count()) return;
    beginRemoveRows(QModelIndex(), row, row);
    m_contacts.removeAt(row);
    endRemoveRows();
}

// roleNames 的实现主要用于 QML 环境，此处省略
QHash<int, QByteArray> ContactModel::roleNames() const { return {}; }
```

## 第二步：使用视图 (View) 展示数据

现在，我们可以将这个模型设置到一个标准的 `QListView` 中。

`mainwindow.cpp`:
```cpp
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "contact_model.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);

    // 1. 创建模型实例
    auto *model = new ContactModel(this);

    // 2. 将模型设置到视图上
    ui->listView->setModel(model);
}
```
运行程序，你将看到一个简单的列表，显示了我们在模型中定义的联系人信息。这已经是一个可以工作的 Model-View 结构了。

## 第三步：自定义委托 (Delegate) 进行渲染

默认的视图只显示 `Qt::DisplayRole` 的文本。如果我们想创建一个更丰富的列表项（例如，左边是头像，右边是姓名和电话），就需要自定义委托。

`contact_delegate.h`:
```cpp
#ifndef CONTACTDELEGATE_H
#define CONTACTDELEGATE_H

#include <QStyledItemDelegate>

class ContactDelegate : public QStyledItemDelegate {
    Q_OBJECT
public:
    explicit ContactDelegate(QObject *parent = nullptr);

    // 重写 paint 来自定义绘制
    void paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const override;

    // 重写 sizeHint 来告诉视图每个项需要多大空间
    QSize sizeHint(const QStyleOptionViewItem &option, const QModelIndex &index) const override;
};

#endif // CONTACTDELEGATE_H
```

`contact_delegate.cpp`:
```cpp
#include "contact_delegate.h"
#include <QPainter>
#include "contact_model.h" // 需要访问模型中的数据

ContactDelegate::ContactDelegate(QObject *parent) : QStyledItemDelegate(parent) {}

void ContactDelegate::paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const {
    if (!index.isValid()) return;

    painter->save();

    // 绘制背景 (例如，选中时高亮)
    if (option.state & QStyle::State_Selected) {
        painter->fillRect(option.rect, option.palette.highlight());
    }

    // 获取数据 (这里我们假设模型返回一个 Contact 结构体)
    // 为了简化，我们直接从模型获取，更好的方式是通过角色
    Contact contact = index.data(Qt::UserRole).value<Contact>(); // 假设模型在 UserRole 中返回整个对象

    // 绘制布局
    QRect r = option.rect;
    QRect nameRect = r.adjusted(10, 10, -10, -20);
    QRect phoneRect = r.adjusted(10, 30, -10, 0);

    // 绘制文本
    painter->setPen(option.palette.windowText().color());
    painter->setFont(QFont("Arial", 10, QFont::Bold));
    painter->drawText(nameRect, Qt::AlignLeft, contact.name);

    painter->setPen(Qt::gray);
    painter->setFont(QFont("Arial", 9));
    painter->drawText(phoneRect, Qt::AlignLeft, contact.phone);

    painter->restore();
}

QSize ContactDelegate::sizeHint(const QStyleOptionViewItem &option, const QModelIndex &index) const {
    // 让每个列表项的高度为 60 像素
    return QSize(200, 60);
}
```

**应用委托**: 在 `MainWindow` 中，将委托设置给视图。
```cpp
// mainwindow.cpp
#include "contact_delegate.h"

MainWindow::MainWindow(QWidget *parent) /*...*/ {
    // ...
    ui->listView->setModel(model);

    // 设置自定义委托
    ui->listView->setItemDelegate(new ContactDelegate(this));
}
```

## 第四步：使用代理模型 (Proxy Model) 实现排序与过滤

如果你想在不修改原始数据模型的情况下，对视图中的数据进行排序或过滤，`QSortFilterProxyModel` 是最佳选择。

`mainwindow.cpp`:
```cpp
#include <QSortFilterProxyModel>
#include <QLineEdit>

MainWindow::MainWindow(QWidget *parent) /*...*/ {
    // ...
    auto *model = new ContactModel(this);

    // 1. 创建代理模型
    auto *proxyModel = new QSortFilterProxyModel(this);
    proxyModel->setSourceModel(model); // 设置源模型
    proxyModel->setFilterCaseSensitivity(Qt::CaseInsensitive); // 设置过滤时忽略大小写
    proxyModel->setFilterKeyColumn(0); // 按第一列（我们唯一的列）进行过滤

    // 2. 将代理模型设置到视图上
    ui->listView->setModel(proxyModel);

    // 3. 添加一个搜索框
    auto *filterLineEdit = new QLineEdit(this);
    // ... 将 filterLineEdit 添加到布局中 ...
    connect(filterLineEdit, &QLineEdit::textChanged, proxyModel, &QSortFilterProxyModel::setFilterFixedString);
}
```
现在，当你在搜索框中输入文本时，列表视图会自动过滤，只显示匹配的项，而原始的 `ContactModel` 中的数据完全不受影响。

## 第五步：组合应用

将以上所有部分组合起来，就可以构建一个功能强大的应用。例如，一个联系人管理器，左边是 `QListView` 显示联系人列表，右边是 `QDataWidgetMapper` 将选中项的数据映射到 `QLineEdit` 等编辑控件上。

## 性能优化与最佳实践

- **批量操作**: 当你要对模型进行大量修改（如添加或删除上百行）时，务必将操作包裹在 `begin...Rows()` 和 `end...Rows()` 或 `beginResetModel()` 和 `endResetModel()` 之间。这会将所有更新合并为一次，大大提高性能。
- **懒加载 (Lazy Loading)**: 对于极大的数据集（如数据库或大型日志文件），不要一次性将所有数据加载到模型中。可以在模型中重写 `canFetchMore()` 和 `fetchMore()` 方法，当视图滚动到末尾时，模型会按需加载下一批数据。
- **视图优化**: 如果你的列表项大小是固定的，在视图上设置 `view->setUniformItemSizes(true)` 可以显著提高滚动性能。
- **数据角色 (Roles)**: 充分利用 `data()` 函数的 `role` 参数。除了 `Qt::DisplayRole`，还可以为 `Qt::ToolTipRole` (工具提示), `Qt::FontRole` (字体), `Qt::ForegroundRole` (前景色) 等提供数据，让视图自动处理一些简单的样式，从而简化 Delegate。
- **避免在 Model 中持有 Qt 控件**: 模型应该只关心数据，不应包含任何与 UI 相关的对象。
