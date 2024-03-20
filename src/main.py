import os
import re
import shutil

from ebooklib import epub
from typing import NoReturn
from PIL import Image, ImageDraw, ImageFont


class MultiLevelBook:
    """
    MultiLevelBook 用于存储和管理一个多级目录的书籍结构，包括卷和章节。
    """

    def __init__(self) -> None:
        """
        初始化 MultiLevelBook 实例，创建空的卷列表。
        """
        self.volumes: list[dict[str, any]] = []

    def add_volume(self, title: str) -> None:
        """
        添加一个新卷到书籍中。

        :param title: 新卷的标题，类型为字符串。
        """
        self.volumes.append({'title': title, 'chapters': []})

    def add_chapter_to_last_volume(self, title: str, content: list[str] = None) -> None:
        """
        在最后一个卷中添加一个新章节。

        :param title: 新章节的标题，类型为字符串。
        :param content: 新章节的内容列表，类型为字符串列表，如果没有提供，默认为空列表。
        """
        if content is None:
            content = []
        if not self.volumes:
            self.add_volume('默认卷')
        self.volumes[-1]['chapters'].append({'title': title, 'content': content})

    def add_content_to_last_chapter(self, line: str) -> None:
        """
        向最后一个章节添加内容。

        :param line: 要添加到最后一个章节的内容行，类型为字符串。
        """
        if self.volumes and self.volumes[-1]['chapters']:
            self.volumes[-1]['chapters'][-1]['content'].append(line)


class TextBookParser:
    CHAPTER_REGULARIZATION = r"^(第[零一二三四五六七八九十百千0-9]+章)[ ：]|(番外) |^(第[零一二三四五六七八九十百千0-9]+章)$"
    SUBSECTION_PATTERN = r"^第[一二三四五六七八九十百千0-9]+卷"

    @staticmethod
    def read(file_path: str) -> MultiLevelBook:
        """
        读取文本文件并解析成一个多级书籍结构。

        :param file_path: TXT文件的路径。
        :return: MultiLevelBook对象，包含解析后的卷和章节信息。
        """
        multi_level_book = MultiLevelBook()
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if re.match(TextBookParser.SUBSECTION_PATTERN, line):
                    multi_level_book.add_volume(line)
                elif re.match(TextBookParser.CHAPTER_REGULARIZATION, line):
                    multi_level_book.add_chapter_to_last_volume(line)
                elif line:
                    multi_level_book.add_content_to_last_chapter(line)

        return multi_level_book

    @staticmethod
    def save_chapters_as_html(multi_level_book, output_folder: str) -> NoReturn:
        """
        将书籍的每个章节保存为HTML文件，使用编号来命名文件。

        :param multi_level_book: 包含卷和章节信息的MultiLevelBook对象。
        :param output_folder: HTML文件保存的目录。
        """
        for volume_index, volume in enumerate(multi_level_book.volumes, start=1):
            for chapter_index, chapter in enumerate(volume['chapters'], start=1):
                # 使用编号来命名文件，格式为"001_001.html"代表第一卷第一章
                file_name = f"{volume_index:03}_{chapter_index:03}.html"
                file_path = os.path.join(output_folder, file_name)

                with open(file_path, 'w', encoding='utf-8') as chapter_file:
                    chapter_file.write(f'<html><head><title>{chapter["title"]}</title></head><body>\n')
                    chapter_file.write(f'<h1>{chapter["title"]}</h1>\n')
                    for line in chapter['content']:
                        chapter_file.write(f'<p>{line}</p>\n')
                    chapter_file.write('</body></html>')


class TxtToEpubConverter:
    def __init__(self, txt_path: str, epub_path: str, book_title: str, author_name: str, cover_image: str = None,
                 output_folder: str = './html_chapters', progress_callback=None):
        """
        初始化转换器实例。

        :param txt_path: TXT文件的路径。
        :param epub_path: 输出的EPUB文件路径。
        :param book_title: 电子书标题。
        :param author_name: 作者名。
        :param cover_image: 封面图片文件的路径。
        :param output_folder: 存放HTML章节文件的目录，默认为'./html_chapters'。
        """
        self.txt_path = txt_path
        self.epub_path = epub_path
        self.book_title = book_title
        self.author_name = author_name
        self.cover_image = cover_image
        self.output_folder = output_folder
        self.progress_callback = progress_callback

    def generate_cover(self) -> str:
        width, height = 600, 800
        background_color = 'white'
        font_color = 'black'

        image = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Directly draw the text without calculating its size
        text_x = width / 2  # You might need to adjust this manually to center the text
        text_y = height / 2  # Same here
        draw.text((text_x, text_y), self.book_title, fill=font_color, font=font, anchor="mm")

        cover_path = os.path.join(self.output_folder, 'cover.jpg')
        image.save(cover_path)

        return cover_path

    def convert(self):
        os.makedirs(self.output_folder, exist_ok=True)

        # Parse the TXT file and build the book structure
        parser = TextBookParser()
        book_structure = parser.read(self.txt_path)

        # Progress update: after parsing (e.g., 10% completed)
        if self.progress_callback:
            self.progress_callback(10)

        # Save chapters as HTML files
        parser.save_chapters_as_html(book_structure, self.output_folder)

        # Progress update: after saving HTML files (e.g., 40% completed)
        if self.progress_callback:
            self.progress_callback(40)

        # Create EPUB book and set metadata
        book = epub.EpubBook()
        book.set_title(self.book_title)
        book.set_language('zh-cn')
        book.add_author(self.author_name)

        # Add cover image
        if self.cover_image and os.path.isfile(self.cover_image):
            cover_path = self.cover_image
        else:
            cover_path = self.generate_cover()

        book.set_cover(os.path.basename(cover_path), open(cover_path, 'rb').read())

        # Progress update: after setting cover (e.g., 50% completed)
        if self.progress_callback:
            self.progress_callback(50)

        # Prepare EPUB book structure
        spine = []
        toc = []

        total_chapters = sum(len(volume['chapters']) for volume in book_structure.volumes)
        chapters_processed = 0

        # 遍历书籍结构，添加卷和章节到EPUB
        for volume_index, volume in enumerate(book_structure.volumes, start=1):
            # 使用编号命名卷的HTML文件
            vol_file_name = f"{volume_index:03}.html"

            # 创建卷的HTML内容
            vol_title = volume['title']
            vol_content = f'<html><head><title>{vol_title}</title></head><body>\n<h1>{vol_title}</h1>\n</body></html>'

            # 创建EpubHtml对象代表卷
            vol_chapter = epub.EpubHtml(title=vol_title, file_name=vol_file_name, lang='zh-cn', content=vol_content)
            book.add_item(vol_chapter)
            spine.append(vol_chapter)
            toc.append(epub.Section(vol_title, [vol_chapter]))

            for chapter_index, chapter in enumerate(volume['chapters'], start=1):
                # 使用编号构建章节的HTML文件名
                chap_file_name = f"{volume_index:03}_{chapter_index:03}.html"
                chap_file_path = os.path.join(self.output_folder, chap_file_name)

                # 读取章节内容
                with open(chap_file_path, 'r', encoding="utf8") as f:
                    fcontent = f.read()

                # 创建EpubHtml对象代表章节
                chap_title = chapter['title']
                chapter_item = epub.EpubHtml(title=chap_title, file_name=chap_file_name, lang='zh-cn', content=fcontent)

                book.add_item(chapter_item)
                spine.append(chapter_item)
                toc.append(epub.Link(chap_file_name, chap_title, chap_title))

                chapters_processed += 1
                # Progress update: dynamically calculated based on chapters processed
                if self.progress_callback:
                    progress = 50 + (
                                chapters_processed / total_chapters * 50)  # Assuming the rest 50% is for chapter processing
                    self.progress_callback(progress)

        # 设置EPUB书籍的导航和样式
        book.spine = ['nav'] + spine
        book.toc = toc

        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css",
                                content='body { font-family: Times, Times New Roman, serif; }')
        book.add_item(nav_css)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # 写入EPUB文件
        epub.write_epub(self.epub_path, book, {})

        # Progress update: conversion completed (100%)
        if self.progress_callback:
            self.progress_callback(100)

        # 清理临时HTML文件
        self.cleanup()

    def cleanup(self) -> NoReturn:
        """
        清理输出目录中的所有文件。
        """
        # 检查目录是否存在
        if os.path.isdir(self.output_folder):
            # 遍历目录中的所有文件，并删除它们
            for filename in os.listdir(self.output_folder):
                file_path = os.path.join(self.output_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

        print("Cleanup completed, temporary files removed.")


if __name__ == '__main__':
    book_name = '我不是戏神'
    txt_path = f'../test_book/{book_name}.txt'
    epub_path = f'../out/{book_name}.epub'
    cover_image = f'../test_book/{book_name}.jpg'
    # 设置书名和作者
    book_title = '我不是戏神'
    author_name = '三九音域'

    converter = TxtToEpubConverter(txt_path, epub_path, book_title, author_name, cover_image)
    converter.convert()
