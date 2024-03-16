import os
import re
from ebooklib import epub

class MultiLevelBook:
    def __init__(self):
        self.volumes = []

    def add_volume(self, title):
        self.volumes.append({'title': title, 'chapters': []})

    def add_chapter_to_last_volume(self, title, content=None):
        if content is None:
            content = []
        if not self.volumes:
            self.add_volume('默认卷')
        self.volumes[-1]['chapters'].append({'title': title, 'content': content})

    def add_content_to_last_chapter(self, line):
        if self.volumes and self.volumes[-1]['chapters']:
            self.volumes[-1]['chapters'][-1]['content'].append(line)

class TextBookParser:
    CHAPTER_REGULARIZATION = r"^(第[零一二三四五六七八九十百千0-9]+章)[ ：]|(番外) |^(第[零一二三四五六七八九十百千0-9]+章)$"
    SUBSECTION_PATTERN = r"^第[一二三四五六七八九十百千0-9]+卷"

    @staticmethod
    def read(file_path):
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
    def save_chapters_as_html(multi_level_book, output_folder):
        for volume in multi_level_book.volumes:
            # 卷的章节
            vol_title = volume['title']
            vol_file_name = f"{vol_title}.html"
            vol_file_path = os.path.join(output_folder, vol_file_name)
            with open(vol_file_path, 'w', encoding='utf-8') as volume_file:
                volume_file.write(f'<html><head><title>{vol_title}</title></head><body>\n')
                volume_file.write(f'<h1>{vol_title}</h1>\n')
                volume_file.write('</body></html>')

            for chapter in volume['chapters']:
                # 章节的内容
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
    def __init__(self, txt_path, epub_path, book_title, author_name, output_folder='./html_chapters'):
        self.txt_path = txt_path
        self.epub_path = epub_path
        self.book_title = book_title
        self.author_name = author_name
        self.output_folder = output_folder

    def convert(self):
        os.makedirs(self.output_folder, exist_ok=True)

        parser = TextBookParser()
        book_structure = parser.read(self.txt_path)

        parser.save_chapters_as_html(book_structure, self.output_folder)

        book = epub.EpubBook()
        book.set_title(self.book_title)
        book.set_language('zh-cn')
        book.add_author(self.author_name)

        spine = []
        toc = []

        for volume in book_structure.volumes:
            # 添加卷标题作为章节
            vol_title = volume['title']
            vol_file_name = f"{vol_title}.html"
            vol_chapter = epub.EpubHtml(
                title=vol_title,
                file_name=vol_file_name,
                lang='zh-cn',
                content=f'<h1>{vol_title}</h1>'
            )
            book.add_item(vol_chapter)
            spine.append(vol_chapter)
            toc.append(epub.Section(vol_title, [vol_chapter]))

            for chapter in volume['chapters']:
                chap_title = chapter['title']
                file_name = f"{chap_title}.html"
                file_path = os.path.join(self.output_folder, file_name)
                with open(file_path, 'r', encoding="utf8") as f:
                    fcontent = f.read()

                chapter_item = epub.EpubHtml(
                    title=chap_title,
                    file_name=file_name,
                    lang='zh-cn',
                    content=fcontent
                )
                book.add_item(chapter_item)
                spine.append(chapter_item)
                toc.append(chapter_item)

        book.spine = ['nav'] + spine
        book.toc = toc

        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content='body { font-family: Times, Times New Roman, serif; }'
        )

        book.add_item(nav_css)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

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

