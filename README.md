# TXT to EPUB Converter

## 项目简介

TXT to EPUB Converter 是一个用于将纯文本文件 (.txt) 转换为电子书格式 (.epub) 的工具。它支持多级目录（卷和章节）并能生成格式化的EPUB文件，适用于需要将长篇文本整理成电子书格式的用户。

## 功能特点

- 将TXT文档转换为EPUB格式
- 支持多级目录结构（卷和章节）
- 自动生成目录并在EPUB中嵌入
- 可自定义书名和作者信息

## 系统要求

- Python 3.6+
- ebooklib：用于EPUB文件的生成和处理
- 需要额外的Python库支持，如`re`和`os`

## 安装指南

确保你已安装Python 3.6或更高版本。使用以下命令安装所需的Python库：

```bash
pip install ebooklib
```

## 使用方法

1. 将TXT文件放在项目的某个目录下，例如`test_book`。
2. 在`main`函数中设置TXT文件路径、输出EPUB文件路径、书名和作者名。
3. 运行脚本：

   ```bash
   python main.py
   ```

## 示例

假设你有一个名为`陈二狗的妖孽人生.txt`的文本文件，要转换成EPUB格式：

1. 将TXT文件放入`test_book`目录。
2. 修改`main`函数中的相关参数：

   ```python
   if __name__ == '__main__':
       book_name = '陈二狗的妖孽人生'
       txt_path = f'./test_book/{book_name}.txt'
       epub_path = f'./out/{book_name}.epub'
       book_title = '陈二狗的妖孽人生'
       author_name = '作者名'
       converter = TxtToEpubConverter(txt_path, epub_path, book_title, author_name)
       converter.convert()
   ```

3. 运行脚本生成EPUB文件。

## 许可协议

[MIT License](https://opensource.org/licenses/MIT)