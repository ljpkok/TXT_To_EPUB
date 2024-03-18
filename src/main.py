import os
import re
from ebooklib import epub
from typing import NoReturn

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
    def save_chapters_as_html(multi_level_book: MultiLevelBook, output_folder: str) -> NoReturn:
        """
        将书籍的每个章节保存为HTML文件。

        :param multi_level_book: 包含卷和章节信息的MultiLevelBook对象。
        :param output_folder: HTML文件保存的目录。
        """
        for volume in multi_level_book.volumes:
            vol_title = volume['title']
            vol_file_name = f"{vol_title}.html"
            vol_file_path = os.path.join(output_folder, vol_file_name)
            with open(vol_file_path, 'w', encoding='utf-8') as volume_file:
                volume_file.write(f'<html><head><title>{vol_title}</title></head><body>\n')
                volume_file.write(f'<h1>{vol_title}</h1>\n')
                volume_file.write('</body></html>')

            for chapter in volume['chapters']:
                chap_title = chapter['title']
                file_name = f"{chap_title}.html"
                file_path = os.path.join(output_folder, file_name)
                with open(file_path, 'w', encoding='utf-8') as chapter_file:
                    chapter_file.write(f'<html><head><title>{chap_title}</title></head><body>\n')
                    chapter_file.write(f'<h1>{chap_title}</h1>\n')
                    for line in chapter['content']:
                        chapter_file.write(f'<p>{line}</p>\n')
                    chapter_file.write('</body></html>')


class TxtToEpubConverter:
    def __init__(self, txt_path: str, epub_path: str, book_title: str, author_name: str,
                 output_folder: str = './html_chapters'):
        """
        初始化转换器实例。

        :param txt_path: TXT文件的路径。
        :param epub_path: 输出的EPUB文件路径。
        :param book_title: 电子书标题。
        :param author_name: 作者名。
        :param output_folder: 存放HTML章节文件的目录，默认为'./html_chapters'。
        """
        self.txt_path = txt_path
        self.epub_path = epub_path
        self.book_title = book_title
        self.author_name = author_name
        self.output_folder = output_folder

    def convert(self) -> NoReturn:
        """
        执行TXT到EPUB的转换过程。
        """
        # 确保输出目录存在
        os.makedirs(self.output_folder, exist_ok=True)

        # 解析TXT文件并构建书籍结构
        parser = TextBookParser()
        book_structure = parser.read(self.txt_path)

        # 将章节内容保存为HTML文件
        parser.save_chapters_as_html(book_structure, self.output_folder)

        # 创建EPUB书籍并设置元数据
        book = epub.EpubBook()
        book.set_title(self.book_title)
        book.set_language('zh-cn')
        book.add_author(self.author_name)

        # 准备EPUB书籍的目录结构
        spine = []
        toc = []

        # 遍历书籍结构，添加卷和章节到EPUB
        for volume in book_structure.volumes:
            vol_title = volume['title']
            vol_file_name = f"{vol_title}.html"
            vol_chapter = epub.EpubHtml(title=vol_title, file_name=vol_file_name, lang='zh-cn',
                                        content=f'<h1>{vol_title}</h1>')

            book.add_item(vol_chapter)
            spine.append(vol_chapter)
            toc.append(epub.Section(vol_title, [vol_chapter]))

            for chapter in volume['chapters']:
                chap_title = chapter['title']
                file_name = f"{chap_title}.html"
                file_path = os.path.join(self.output_folder, file_name)

                with open(file_path, 'r', encoding="utf8") as f:
                    fcontent = f.read()

                chapter_item = epub.EpubHtml(title=chap_title, file_name=file_name, lang='zh-cn', content=fcontent)

                book.add_item(chapter_item)
                spine.append(chapter_item)
                toc.append(chapter_item)

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


if __name__ == '__main__':
    book_name = '陈二狗的妖孽人生'
    txt_path = f'../test_book/{book_name}.txt'
    epub_path = f'../out/{book_name}.epub'

    # 设置书名和作者
    book_title = '陈二狗的妖孽人生'
    author_name = '骁骑校'

    converter = TxtToEpubConverter(txt_path, epub_path, book_title, author_name)
    converter.convert()

