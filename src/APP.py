import os
import sys
from main import TxtToEpubConverter
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt


class TxtToEpubGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('TXT 转 EPUB 转换器')
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        # 信息标签
        self.infoLabel = QLabel('点击“浏览”选择TXT文件。')
        self.infoLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.infoLabel)

        # 浏览按钮
        self.browseButton = QPushButton('浏览')
        self.browseButton.clicked.connect(self.browseFile)
        layout.addWidget(self.browseButton)

        # 书名输入框
        self.fileNameEdit = QLineEdit()
        self.fileNameEdit.setPlaceholderText('书本名称')
        layout.addWidget(self.fileNameEdit)

        # 作者名输入框
        self.authorNameEdit = QLineEdit()
        self.authorNameEdit.setPlaceholderText('作者名称')
        layout.addWidget(self.authorNameEdit)

        # 转换按钮
        self.convertButton = QPushButton('转换')
        self.convertButton.clicked.connect(self.convert)
        layout.addWidget(self.convertButton)

        self.setLayout(layout)

    def browseFile(self):
        # 打开文件选择对话框
        filePath, _ = QFileDialog.getOpenFileName(self, '选择一个TXT文件', '', '文本文件 (*.txt)')
        if filePath:
            self.setFilePath(filePath)

    def setFilePath(self, filePath):
        # 设置文件路径并更新UI
        self.filePath = filePath
        self.infoLabel.setText(f'选中的文件: {os.path.basename(filePath)}')
        self.fileNameEdit.setText(os.path.splitext(os.path.basename(filePath))[0])

    def convert(self):
        # 从UI获取书名和作者名，执行转换
        bookTitle = self.fileNameEdit.text()
        authorName = self.authorNameEdit.text()
        output_path = f'../out/{bookTitle}.epub'
        converter = TxtToEpubConverter(self.filePath, output_path, bookTitle, authorName)
        converter.convert()

        # 显示转换完成消息
        self.infoLabel.setText('转换完成！')


def main():
    app = QApplication(sys.argv)
    gui = TxtToEpubGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
