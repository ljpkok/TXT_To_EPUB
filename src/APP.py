import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QGridLayout
from main import TxtToEpubConverter

class TxtToEpubGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.filePath = None
        self.coverImagePath = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TXT to EPUB Converter')
        self.setGeometry(100, 100, 400, 300)

        mainLayout = QVBoxLayout()
        formLayout = QGridLayout()

        self.infoLabel = QLabel('选择一个TXT文件并转换为EPUB。')
        mainLayout.addWidget(self.infoLabel)

        self.browseButton = QPushButton('选择TXT文件')
        self.browseButton.clicked.connect(self.browseFile)
        mainLayout.addWidget(self.browseButton)

        formLayout.addWidget(QLabel('书本名称：'), 0, 0)
        self.fileNameEdit = QLineEdit()
        self.fileNameEdit.setPlaceholderText('书本名称')
        formLayout.addWidget(self.fileNameEdit, 0, 1)

        formLayout.addWidget(QLabel('作者名称：'), 1, 0)
        self.authorNameEdit = QLineEdit()
        self.authorNameEdit.setPlaceholderText('作者名称')
        formLayout.addWidget(self.authorNameEdit, 1, 1)

        self.coverButton = QPushButton('选择封面图像')
        self.coverButton.clicked.connect(self.browseCoverImage)
        mainLayout.addWidget(self.coverButton)

        self.coverLabel = QLabel('未选择封面图像')
        mainLayout.addWidget(self.coverLabel)

        self.convertButton = QPushButton('转换为EPUB')
        self.convertButton.clicked.connect(self.convert)
        mainLayout.addWidget(self.convertButton)

        # 将表单布局添加到主布局
        mainLayout.addLayout(formLayout)

        self.setLayout(mainLayout)

    def browseFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, '选择TXT文件', '', 'Text files (*.txt)')
        if filePath:
            self.filePath = filePath
            self.infoLabel.setText(f'选择的文件: {os.path.basename(filePath)}')
            self.fileNameEdit.setText(os.path.splitext(os.path.basename(filePath))[0])

    def browseCoverImage(self):
        coverImagePath, _ = QFileDialog.getOpenFileName(self, '选择封面图像', '', 'Image files (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp)')
        if coverImagePath:
            self.coverImagePath = coverImagePath
            self.coverLabel.setText(f'选择的封面图像: {os.path.basename(coverImagePath)}')

    def convert(self):
        bookTitle = self.fileNameEdit.text()
        authorName = self.authorNameEdit.text()
        if self.filePath:
            output_path = os.path.join('..', 'out', f'{bookTitle}.epub')
            converter = TxtToEpubConverter(self.filePath, output_path, bookTitle, authorName, self.coverImagePath)
            converter.convert()
            self.infoLabel.setText('转换完成！')
        else:
            self.infoLabel.setText('请确保已选择TXT文件。')

def main():
    app = QApplication(sys.argv)
    gui = TxtToEpubGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
