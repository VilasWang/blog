---
tags:
  - Qt
  - QAudioInput
  - 音频录制
  - WAV
  - 多媒体
  - C++
title: Qt 音频录制指南
categories:
  - C++核心开发
  - Qt框架
description: 专业技术完全指南，涵盖理论基础、实践操作、问题排查、性能优化等全方位内容，助力技能快速提升。
abbrlink: df73c2a8
date: 2025-12-04 13:13:22
---

# Qt 音频录制指南
## 目录
- [概述](#概述)
- [第一步：项目设置与UI设计](#第一步项目设置与ui设计)
- [第二步：实现录音逻辑](#第二步实现录音逻辑)
- [第三步：处理WAV文件头](#第三步处理wav文件头)
- [完整代码参考](#完整代码参考)
- [高级功能展望 (文字说明)](#高级功能展望-文字说明)
- [常见问题](#常见问题)

## 概述

本指南将以一个清晰、循序渐进的方式，介绍如何使用 Qt 的 `QAudioInput` 类来实现基础的音频录制功能，并将录制的原始音频数据保存为可播放的 `.wav` 文件。

### 核心组件
- **`QAudioDeviceInfo`**: 用于查询和选择可用的音频输入设备（如麦克风）。
- **`QAudioFormat`**: 用于定义录音的参数，如采样率、声道数、采样位深等。
- **`QAudioInput`**: 核心类，用于从指定的设备以指定的格式捕获音频数据。
- **`QFile`**: 一个继承自 `QIODevice` 的类，我们可以直接让 `QAudioInput` 将音频数据写入一个 `QFile` 对象。

## 第一步：项目设置与UI设计

### 1. 项目配置 (`.pro` 文件)
创建一个新的 Qt Widgets Application 项目，并确保 `.pro` 文件中包含了 `multimedia` 模块。

```qmake
QT += core gui multimedia

GREATER_THAN_QT_5 {
    QT += widgets
}

TARGET = AudioRecorderApp
TEMPLATE = app

SOURCES += main.cpp mainwindow.cpp
HEADERS += mainwindow.h
FORMS   += mainwindow.ui
```

### 2. UI 设计 (`mainwindow.ui`)
在 Qt Designer 中，设计一个简单的主窗口界面，包含以下控件：

- **`QComboBox` (deviceComboBox)**: 用于选择输入设备。
- **`QPushButton` (recordButton)**: 用于开始录音。
- **`QPushButton` (stopButton)**: 用于停止录音。
- **`QLabel` (statusLabel)**: 用于显示当前状态（如“正在录音...”、“已停止”）。

## 第二步：实现录音逻辑

我们将所有录音逻辑都封装在 `MainWindow` 类中，以保持示例的简洁性。

### 1. 添加成员变量
在 `mainwindow.h` 中，添加 `QAudioInput` 和 `QFile` 的指针。

```cpp
// mainwindow.h
#include <QAudioInput>
#include <QFile>

class MainWindow : public QMainWindow {
    // ...
private:
    Ui::MainWindow *ui;
    QAudioInput *m_audioInput = nullptr;
    QFile *m_outputFile = nullptr;
    QAudioDeviceInfo m_selectedDevice;
};
```

### 2. 初始化设备列表
在 `mainwindow.cpp` 的构造函数中，查找可用的音频输入设备并填充到 `QComboBox` 中。

```cpp
// mainwindow.cpp
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QAudioDeviceInfo>
#include <QMessageBox>
#include <QFileDialog>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);
    ui->stopButton->setEnabled(false);

    // 1. 填充设备列表
    const auto devices = QAudioDeviceInfo::availableDevices(QAudio::AudioInput);
    for (const QAudioDeviceInfo &deviceInfo : devices) {
        ui->deviceComboBox->addItem(deviceInfo.deviceName(), QVariant::fromValue(deviceInfo));
    }

    // 2. 连接信号槽
    connect(ui->recordButton, &QPushButton::clicked, this, &MainWindow::startRecording);
    connect(ui->stopButton, &QPushButton::clicked, this, &MainWindow::stopRecording);
}
```

### 3. 开始与停止录音

```cpp
// mainwindow.cpp

void MainWindow::startRecording() {
    // 1. 获取选中的设备
    int selectedIndex = ui->deviceComboBox->currentIndex();
    if (selectedIndex < 0) {
        QMessageBox::warning(this, "错误", "没有选择有效的音频输入设备。");
        return;
    }
    m_selectedDevice = ui->deviceComboBox->itemData(selectedIndex).value<QAudioDeviceInfo>();

    // 2. 设置音频格式 (例如: 44.1kHz, 16-bit, 立体声)
    QAudioFormat format;
    format.setSampleRate(44100);
    format.setChannelCount(2);
    format.setSampleSize(16);
    format.setSampleType(QAudioFormat::SignedInt);
    format.setByteOrder(QAudioFormat::LittleEndian);
    format.setCodec("audio/pcm");

    // 3. 检查设备是否支持此格式
    if (!m_selectedDevice.isFormatSupported(format)) {
        QMessageBox::warning(this, "错误", "所选设备不支持当前音频格式。");
        return;
    }

    // 4. 设置输出文件
    QString savePath = QFileDialog::getSaveFileName(this, "保存录音", "", "WAV 文件 (*.wav)");
    if (savePath.isEmpty()) return;

    m_outputFile = new QFile(savePath, this);
    if (!m_outputFile->open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        QMessageBox::warning(this, "错误", "无法打开输出文件。");
        return;
    }

    // 5. 创建并启动 QAudioInput
    m_audioInput = new QAudioInput(m_selectedDevice, format, this);
    m_audioInput->start(m_outputFile); // 直接将音频数据写入文件

    // 更新UI状态
    ui->recordButton->setEnabled(false);
    ui->stopButton->setEnabled(true);
    ui->statusLabel->setText("正在录音...");
}

void MainWindow::stopRecording() {
    if (!m_audioInput) return;

    // 1. 停止录音
    m_audioInput->stop();

    // 2. 清理资源
    m_outputFile->close();
    delete m_audioInput;
    m_audioInput = nullptr;

    // 更新UI状态
    ui->recordButton->setEnabled(true);
    ui->stopButton->setEnabled(false);
    ui->statusLabel->setText("录音已停止。");
}
```

## 第三步：处理WAV文件头

`QAudioInput` 录制的是纯净的 PCM 音频数据。为了让普通播放器能识别，我们需要在文件开头写入一个 WAV 格式的头部信息。由于录制前不知道文件总大小，我们采用“占位-回填”的方式。

### 1. 录制前写入占位文件头
修改 `startRecording` 函数，在 `m_audioInput->start(m_outputFile)` 之前加入写文件头的逻辑。

```cpp
// 在 startRecording() 中...
if (!m_outputFile->open(QIODevice::WriteOnly | QIODevice::Truncate)) { /*...*/ }

// 新增：写入一个44字节的占位WAV头
writeWavHeader(m_outputFile, format, 0);

m_audioInput = new QAudioInput(m_selectedDevice, format, this);
m_audioInput->start(m_outputFile);
// ...
```

### 2. 录制后更新文件头
修改 `stopRecording` 函数，在 `m_outputFile->close()` 之后，重新打开文件并更新文件头中的长度信息。

```cpp
// 在 stopRecording() 中...
m_audioInput->stop();

qint64 fileSize = m_outputFile->size();
m_outputFile->close();

// 新增：更新WAV头的长度信息
updateWavHeader(m_outputFile->fileName(), fileSize);

delete m_audioInput;
// ...
```

### 3. WAV 文件头辅助函数
将这些函数添加到 `mainwindow.cpp` 或一个单独的工具类中。

```cpp
// mainwindow.cpp
#include <QDataStream>

// 写一个占位的WAV头
void writeWavHeader(QFile *file, const QAudioFormat &format, qint64 dataSize) {
    QDataStream out(file);
    out.setByteOrder(QDataStream::LittleEndian);

    out.writeRawData("RIFF", 4);
    out << quint32(dataSize + 36);
    out.writeRawData("WAVE", 4);
    out.writeRawData("fmt ", 4);
    out << quint32(16);
    out << quint16(1); // PCM
    out << quint16(format.channelCount());
    out << quint32(format.sampleRate());
    out << quint32(format.sampleRate() * format.channelCount() * format.sampleSize() / 8); // byteRate
    out << quint16(format.channelCount() * format.sampleSize() / 8); // blockAlign
    out << quint16(format.sampleSize());
    out.writeRawData("data", 4);
    out << quint32(dataSize);
}

// 录制结束后更新WAV头的尺寸信息
void updateWavHeader(const QString &fileName, qint64 fileSize) {
    QFile file(fileName);
    if (!file.open(QIODevice::ReadWrite)) return;

    qint64 dataSize = fileSize - 44;
    QDataStream out(&file);
    out.setByteOrder(QDataStream::LittleEndian);

    file.seek(4);
    out << quint32(dataSize + 36);

    file.seek(40);
    out << quint32(dataSize);

    file.close();
}
```

## 完整代码参考

(为简洁起见，此处省略了完整的 `main.cpp` 和 `mainwindow.h` 文件，上文已包含所有核心逻辑。)

## 高级功能展望 (文字说明)

- **实时音频监控 (电平表)**: 不将 `QFile` 传递给 `start()`，而是调用 `QIODevice *device = m_audioInput->start()`。然后连接 `device` 的 `readyRead` 信号，从中实时读取音频数据块，计算其振幅（RMS或峰值），并更新 UI 上的 `QProgressBar`。
- **编码为 MP3**: `QAudioInput` 只产生原始的 PCM 数据。要录制为 MP3，你需要将实时读取的音频数据块传递给一个第三方的 MP3 编码库（如 LAME），然后将编码后的数据写入文件。
- **暂停与恢复**: `QAudioInput` 提供了 `suspend()` 和 `resume()` 方法，可以很方便地实现暂停和恢复功能。

## 常见问题

**Q1: 录制的 `.wav` 文件无法播放或播放速度不正常?**
**A**: 这几乎总是因为 WAV 文件头信息不正确。请仔细检查 `writeWavHeader` 和 `updateWavHeader` 函数中的计算，特别是 `dataSize` 和 `riffSize` 是否正确。

**Q2: 程序提示“默认音频输入设备不支持该格式”?**
**A**: 你的麦克风可能不支持你设置的 `QAudioFormat`（例如，不支持 48000Hz 采样率或立体声录制）。可以尝试一个更通用的格式，如 44100Hz 采样率、16位、单声道。

**Q3: 录音时有杂音或噪音?**
**A**: 这可能是硬件问题，也可能是缓冲区大小不合适。可以尝试通过 `m_audioInput->setBufferSize()` 设置一个更大的缓冲区。
