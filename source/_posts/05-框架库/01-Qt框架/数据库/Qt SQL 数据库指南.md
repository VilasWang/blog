---
tags:
  - Qt
  - QSqlDatabase
  - QSqlQuery
  - QSqlTableModel
  - 数据库
  - SQL
  - C++
title: Qt SQL 数据库指南
categories:
  - C++核心开发
  - Qt框架
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: 835264d4
date: 2025-12-04 13:13:22
---

# Qt SQL 数据库指南
## 目录
- [概述：Qt SQL 模块](#概述qt-sql-模块)
- [第一步：配置与连接数据库](#第一步配置与连接数据库)
- [第二步：使用 QSqlQuery 执行 SQL 命令](#第二步使用-qsqlquery-执行-sql-命令)
- [第三步：使用模型/视图显示数据](#第三步使用-模型视图显示数据)
- [第四步：使用事务](#第四步使用事务)
- [最佳实践与常见问题](#最佳实践与常见问题)

## 概述：Qt SQL 模块

Qt 的 `SQL` 模块提供了一套与平台和数据库无关的接口，用于访问 SQL 数据库。其核心是驱动程序架构，允许你使用相同的 Qt API 来操作多种不同的数据库，如 SQLite, MySQL, PostgreSQL 等。

### 核心类
- **`QSqlDatabase`**: 代表一个数据库连接。它负责管理连接本身。
- **`QSqlQuery`**: 用于执行 SQL 语句，并遍历查询结果。
- **`QSqlQueryModel`**: 一个只读的数据模型，用于将一个 SQL 查询的结果直接展示在视图（如 `QTableView`）中。
- **`QSqlTableModel`**: 一个可读写的数据模型，它代表一个单一的数据库表，并允许在视图中直接编辑数据。

## 第一步：配置与连接数据库

### 1. 项目配置 (`.pro` 文件)
确保你的项目文件包含了 `sql` 模块。

```qmake
QT += core gui sql
```

### 2. 检查驱动
在使用特定数据库前，应检查 Qt 是否有可用的驱动。

```cpp
#include <QSqlDatabase>
#include <QDebug>

qDebug() << "Available drivers:" << QSqlDatabase::drivers();
// 输出应包含 "QSQLITE", "QMYSQL", "QPSQL" 等
```
如果缺少驱动，你需要安装它（例如，在 Ubuntu 上 `sudo apt-get install libqt5sql5-mysql`）。

### 3. 建立连接 (SQLite 示例)
SQLite 是最简单的入门数据库，因为它是一个本地文件，无需服务器。

```cpp
#include <QSqlDatabase>
#include <QDebug>
#include <QSqlError>

bool createConnection() {
    // 1. 添加一个数据库连接，使用默认连接名
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");

    // 2. 设置数据库文件名
    db.setDatabaseName("mydatabase.db");

    // 3. 打开连接
    if (!db.open()) {
        qWarning() << "Connection failed:" << db.lastError().text();
        return false;
    }

    qDebug() << "Database connected successfully!";
    return true;
}
```
**提示**: `QSqlDatabase::addDatabase` 返回的是一个值，但它实际上创建了一个可被全局访问的静态实例。你可以通过 `QSqlDatabase::database()` 来随时获取这个连接的引用。

## 第二步：使用 QSqlQuery 执行 SQL 命令

`QSqlQuery` 是执行所有 SQL 操作的核心。

### 1. 执行简单查询 (DDL 和 DML)

```cpp
#include <QSqlQuery>

void setupDatabase() {
    QSqlQuery query; // 默认使用主连接

    // 创建表
    bool success = query.exec("CREATE TABLE IF NOT EXISTS contacts ("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "name TEXT NOT NULL, "
                            "phone TEXT)");
    if (!success) {
        qWarning() << "Create table failed:" << query.lastError();
    }

    // 插入数据
    query.exec("INSERT INTO contacts (name, phone) VALUES ('Alice', '+1-202-555-0173')");
}
```

### 2. 使用预处理查询 (防止 SQL 注入)

当你的查询需要包含来自用户输入等外部来源的数据时，**必须**使用预处理查询来防止 SQL 注入攻击。

```cpp
void addContact(const QString &name, const QString &phone) {
    QSqlQuery query;
    
    // 1. 准备一个带占位符的查询
    query.prepare("INSERT INTO contacts (name, phone) VALUES (:name, :phone)");
    
    // 2. 绑定值到占位符
    query.bindValue(":name", name);
    query.bindValue(":phone", phone);
    
    // 3. 执行查询
    if (!query.exec()) {
        qWarning() << "Add contact failed:" << query.lastError();
    }
}
```

### 3. 遍历查询结果

```cpp
void printAllContacts() {
    QSqlQuery query("SELECT id, name, phone FROM contacts");
    
    // query.next() 会将内部指针移动到下一条记录
    while (query.next()) {
        int id = query.value(0).toInt();
        QString name = query.value(1).toString();
        QString phone = query.value("phone").toString(); // 也可以按列名获取

        qDebug() << "ID:" << id << "Name:" << name << "Phone:" << phone;
    }
}
```

## 第三步：使用模型/视图显示数据

Qt 的 SQL 模块与模型/视图框架无缝集成，可以轻松地将数据库数据显示在 UI 上。

### 1. `QSqlQueryModel` (只读模型)
这个模型最适合用于显示复杂查询（如 `JOIN`）的结果。

```cpp
// 在 MainWindow 中
#include <QSqlQueryModel>

void MainWindow::setupQueryView() {
    auto *model = new QSqlQueryModel(this);
    model->setQuery("SELECT name, phone FROM contacts ORDER BY name");

    // 设置表头
    model->setHeaderData(0, Qt::Horizontal, tr("Name"));
    model->setHeaderData(1, Qt::Horizontal, tr("Phone Number"));

    ui->tableView->setModel(model);
}
```

### 2. `QSqlTableModel` (读写模型)
这个模型代表一个单一的数据库表，并支持直接在视图中进行编辑。

```cpp
// 在 MainWindow 中
#include <QSqlTableModel>

void MainWindow::setupTableView() {
    auto *model = new QSqlTableModel(this); // db 参数默认为主连接
    model->setTable("contacts");

    // 设置编辑策略：OnManualSubmit 表示所有修改都将缓存，直到手动提交
    model->setEditStrategy(QSqlTableModel::OnManualSubmit);

    // 从数据库加载数据
    model->select();

    // 设置表头
    model->setHeaderData(1, Qt::Horizontal, tr("Name"));
    model->setHeaderData(2, Qt::Horizontal, tr("Phone Number"));

    ui->tableView->setModel(model);
    ui->tableView->hideColumn(0); // 隐藏 ID 列

    // ... 在 UI 上添加 "Submit" 和 "Revert" 按钮
    connect(ui->submitButton, &QPushButton::clicked, model, &QSqlTableModel::submitAll);
    connect(ui->revertButton, &QPushButton::clicked, model, &QSqlTableModel::revertAll);
}
```

## 第四步：使用事务

当需要执行多个关联的 SQL 语句，并确保它们要么全部成功、要么全部失败时，应使用事务。

```cpp
void performTransaction() {
    QSqlDatabase db = QSqlDatabase::database(); // 获取默认连接

    // 1. 开始事务
    if (!db.transaction()) {
        qWarning() << "Failed to start transaction:" << db.lastError();
        return;
    }

    QSqlQuery query(db);
    query.prepare("UPDATE accounts SET balance = balance - 100 WHERE id = 1");
    bool success1 = query.exec();

    query.prepare("UPDATE accounts SET balance = balance + 100 WHERE id = 2");
    bool success2 = query.exec();

    // 2. 如果所有操作都成功，则提交事务
    if (success1 && success2) {
        if (db.commit()) {
            qDebug() << "Transaction successful!";
        } else {
            qWarning() << "Commit failed:" << db.lastError();
            db.rollback(); // 尝试回滚
        }
    } else {
        // 3. 如果有任何操作失败，则回滚事务
        qWarning() << "One of the queries failed, rolling back.";
        db.rollback();
    }
}
```

## 最佳实践与常见问题

- **防止 SQL 注入**: 永远不要手动拼接 SQL 查询字符串。始终使用 `QSqlQuery::prepare()` 和 `bindValue()` 来处理用户输入。
- **管理连接**: 对于多线程应用，每个线程都应该有自己独立的数据库连接。可以通过 `QSqlDatabase::addDatabase("QSQLITE", "connection_name")` 创建命名连接，并在需要时通过 `QSqlDatabase::database("connection_name")` 获取。
- **错误处理**: 每次数据库操作后，都应检查 `QSqlDatabase::lastError()` 或 `QSqlQuery::lastError()` 来确认操作是否成功。
- **模型 vs. 手动查询**: 优先使用 `QSqlQueryModel` 和 `QSqlTableModel` 来与 UI 交互，这比手动从查询结果中读取数据并填充 UI 要简单和高效得多。
