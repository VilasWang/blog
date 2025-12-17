---
title: Qt 国际化指南
categories:
  - C++核心开发
  - Qt框架
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
tags:
  - Qt
  - C++
  - 国际化
  - i18n
  - 本地化
  - QTranslator
  - lupdate
abbrlink: 6d91761d
date: 2025-12-04 22:09:42
---

# Qt 国际化指南
## 目录
- [概述：Qt 的 i18n 工作流程](#概述qt-的-i18n-工作流程)
- [第一步：在代码中标记待翻译文本](#第一步在代码中标记待翻译文本)
- [第二步：配置项目 (.pro) 文件](#第二步配置项目-pro-文件)
- [第三步：使用工具生成和翻译](#第三步使用工具生成和翻译)
- [第四步：在应用程序中加载翻译](#第四步在应用程序中加载翻译)
- [第五步：实现动态语言切换](#第五步实现动态语言切换)
- [处理数字、日期和货币的本地化](#处理数字日期和货币的本地化)

## 概述：Qt 的 i18n 工作流程

国际化 (i18n) 是指让你的应用程序能够适应不同语言和地区的过程。Qt 提供了一套强大而直接的工具链来完成这项工作，其核心流程如下：

1.  **包裹 (Wrap)**: 在你的 C++ 源代码中，将所有需要被翻译的用户界面字符串用 `tr()` 函数包裹起来。
2.  **更新 (Update)**: 使用 Qt 的命令行工具 `lupdate` 扫描你的项目文件，它会找到所有被 `tr()` 包裹的字符串，并生成或更新 `.ts` (Translation Source) 格式的翻译源文件。
3.  **翻译 (Translate)**: 使用 Qt 提供的图形化工具 `Qt Linguist` 打开 `.ts` 文件，然后由翻译人员逐条填写目标语言的译文。
4.  **发布 (Release)**: 使用 Qt 的命令行工具 `lrelease` 将翻译完成的 `.ts` 文件编译成紧凑的二进制 `.qm` (Qt Message) 文件。你的应用程序在运行时实际加载的是这个 `.qm` 文件。
5.  **加载 (Load)**: 在你的应用程序中，创建一个 `QTranslator` 对象，加载对应的 `.qm` 文件，并将其安装到应用程序实例中。

## 第一步：在代码中标记待翻译文本

这是国际化的基础。为了让 `lupdate` 工具能识别出哪些文本需要翻译，你必须将它们用 `tr()` 函数包裹起来。`tr()` 是 `QObject` 的一个成员函数。

```cpp
// mywidget.cpp
#include <QPushButton>
#include <QLabel>

MyWidget::MyWidget(QWidget *parent) : QWidget(parent) {
    // 正确的做法：使用 tr()
    auto *label = new QLabel(tr("Username:"), this);
    auto *button = new QPushButton(tr("Submit"), this);

    // 错误的做法：使用裸字符串
    // auto *label = new QLabel("Username:", this); // 这个字符串不会被翻译
}
```

### 处理复数
当文本需要根据数量变化时（例如“1个文件” vs “多个文件”），可以使用 `tr()` 的第三个参数。

```cpp
int fileCount = getFileCount();
QString text = tr("%n file(s) found.", "", fileCount);
// 当 fileCount 为 1 时，翻译工具会让你翻译 "%n file found."
// 当 fileCount 不为 1 时，会让你翻译 "%n files found."
```

## 第二步：配置项目 (.pro) 文件

在你的 `.pro` 项目文件中，使用 `TRANSLATIONS` 变量来声明你计划支持的语言以及对应的 `.ts` 文件。

```qmake
# Qt 国际化指南
SOURCES += main.cpp \
           mainwindow.cpp

HEADERS += mainwindow.h

FORMS += mainwindow.ui

# Qt 国际化指南
TRANSLATIONS = \
    translations/my_app_de.ts \
    translations/my_app_fr.ts \
    translations/my_app_zh_CN.ts
```

## 第三步：使用工具生成和翻译

### 1. `lupdate` - 生成/更新 .ts 文件
打开一个 Qt 命令行工具（例如 Qt Creator 中的命令行，或手动配置好环境的终端），进入你的项目根目录，然后运行：

```bash
# Qt 国际化指南
lupdate my_app.pro
```

执行后，`translations/` 目录下就会生成 `my_app_de.ts`, `my_app_fr.ts` 等文件。

### 2. `Qt Linguist` - 进行翻译
`Qt Linguist` 是一个图形化的翻译工具。

1.  打开 `Qt Linguist`。
2.  文件 -> 打开... -> 选择一个 `.ts` 文件（例如 `my_app_zh_CN.ts`）。
3.  在左侧的“上下文”列表中选择一项，然后在右侧的“翻译”区域填入中文译文。
4.  完成后，点击工具栏上的“完成”复选框。
5.  保存文件。

### 3. `lrelease` - 发布 .qm 文件
翻译完成后，使用 `lrelease` 工具将 `.ts` 文件编译成应用程序最终使用的 `.qm` 文件。

```bash
lrelease my_app.pro
```
执行后，每个 `.ts` 文件旁边都会生成一个同名的 `.qm` 文件。

**提示**: 将 `.qm` 文件添加到你的项目的资源文件 (`.qrc`) 中是最佳实践，这样它们会被编译进最终的可执行文件中。

## 第四步：在应用程序中加载翻译

在 `main.cpp` 中，根据当前的系统语言环境，加载对应的 `.qm` 文件。

```cpp
// main.cpp
#include <QApplication>
#include <QTranslator>
#include <QLocale>
#include <QLibraryInfo>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QTranslator translator;
    // 获取系统当前的语言环境
    QLocale currentLocale = QLocale::system();

    // 加载我们自己的翻译文件
    // 注意：路径 ":/translations" 是指在 qrc 资源文件中的路径
    if (translator.load(currentLocale, "my_app", "_", ":/translations")) {
        app.installTranslator(&translator);
    }

    // (可选) 加载 Qt 自身的标准翻译（例如 "OK", "Cancel" 按钮的翻译）
    QTranslator qtBaseTranslator;
    if (qtBaseTranslator.load("qtbase_" + currentLocale.name(), 
                              QLibraryInfo::location(QLibraryInfo::TranslationsPath))) {
        app.installTranslator(&qtBaseTranslator);
    }

    MainWindow w;
    w.show();

    return app.exec();
}
```

## 第五步：实现动态语言切换

要让用户在程序运行时切换语言，你需要：
1.  一个加载新翻译文件的机制。
2.  一个让所有窗口和控件刷新其文本的机制。

Qt 通过 `QEvent::LanguageChange` 事件来优雅地处理第二点。

```cpp
// 在你的主窗口或设置对话框中

// 成员变量
QTranslator m_translator;

void switchLanguage(const QString& langCode) { // e.g., "zh_CN"
    // 1. 移除旧的翻译器
    qApp->removeTranslator(&m_translator);

    // 2. 加载新的 .qm 文件
    if (m_translator.load(":/translations/my_app_" + langCode)) {
        // 3. 安装新的翻译器
        qApp->installTranslator(&m_translator);
    }
}

// 在需要更新界面的 QWidget 子类中，重写 changeEvent
void MyWidget::changeEvent(QEvent *event) {
    if (event->type() == QEvent::LanguageChange) {
        // 当语言改变时，这个事件会被发送到所有顶级窗口
        // 在这里重新翻译所有 UI 文本
        ui->retranslateUi(this); // 如果使用 .ui 文件
        // 或者手动调用 tr()
        // ui->myButton->setText(tr("Submit"));
    }
    QWidget::changeEvent(event);
}
```
当你安装一个新的翻译器后，Qt 会自动向所有窗口发送 `LanguageChange` 事件，触发 `changeEvent`，从而刷新整个 UI。

## 处理数字、日期和货币的本地化

翻译文本只是国际化的一部分。不同地区对数字、日期和货币的格式要求也不同。`QLocale` 是处理这些问题的关键。

```cpp
#include <QLocale>
#include <QDate>

// 假设当前 locale 是 "de_DE" (德国)
QLocale german(QLocale::German, QLocale::Germany);

double number = 12345.67;
QDate date(2025, 9, 21);

// 使用德国的格式
debug() << german.toString(number, 'f', 2); // 输出: "12.345,67"
debug() << german.toString(date, QLocale::LongFormat); // 输出: "Sonntag, 21. September 2025"

// 使用美国的格式
QLocale american(QLocale::English, QLocale::UnitedStates);
debug() << american.toString(number, 'f', 2); // 输出: "12,345.67"
debug() << american.toString(date, QLocale::LongFormat); // 输出: "Sunday, September 21, 2025"
```
