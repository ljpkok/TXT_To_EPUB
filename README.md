# TXT to EPUB Converter

## 项目简介

TXT to EPUB Converter 是一个用于将纯文本文件 (.txt) 转换为电子书格式 (.epub) 的工具。它支持多级目录（卷和章节）并能生成格式化的EPUB文件，适用于需要将长篇文本整理成电子书格式的用户。此外，该工具提供了一个图形用户界面（GUI），使非技术用户也能轻松进行转换。

## 功能特点

- 将TXT文档转换为EPUB格式
- 支持多级目录结构（卷和章节）
- 自动生成目录并在EPUB中嵌入
- 可自定义书名和作者信息
- 简易的图形用户界面（GUI）用于文件选择和转换控制

## 系统要求

- Python 3.6+
- ebooklib：用于EPUB文件的生成和处理
- PyQt5：用于图形用户界面

## 安装指南

确保你已安装Python 3.6或更高版本，并安装以下所需的Python库：

```bash
pip install ebooklib PyQt5
```

## 使用方法

### 命令行界面

1. 将TXT文件放在项目的某个目录下，例如`test_book`。
2. 在`main.py`文件中设置TXT文件路径、输出EPUB文件路径、书名和作者名。
3. 运行脚本：

   ```bash
   python main.py
   ```

### 图形用户界面

1. 运行`APP.py`启动GUI：

   ```bash
   python APP.py
   ```

2. 通过图形界面选择TXT文件，自动填充书名。
3. 可以修改书名和作者信息。
4. 点击“转换”按钮开始转换过程。

## 示例

假设你有一个名为`陈二狗的妖孽人生.txt`的文本文件，要转换成EPUB格式：

1. 将TXT文件放入`test_book`目录。
2. 使用GUI选择文件并设置书名及作者信息，或在`main.py`中设置并运行脚本。

## 未来目标

- 增强图形界面的功能，包括进度条和转换状态提示。
- 提供更多定制选项，如字体大小和样式设置。
- 优化代码结构和性能，减少转换时间。

## 许可协议

[MIT License](https://opensource.org/licenses/MIT)