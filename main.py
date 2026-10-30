import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from ui_design import Ui_MainWindow
import os, shutil


class SorterWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.setWindowTitle("File Sorter")

        self.directory = None

        self.select_button.clicked.connect(self.select_dir)
        self.sort_button.clicked.connect(self.start_sorting)
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.CATEGORIES = {
            # executables and scripts
            ".exe": "EXECUTABLES",
            ".msi": "EXECUTABLES",
            ".bat": "EXECUTABLES",
            ".cmd": "EXECUTABLES",
            ".sh": "EXECUTABLES",
            ".vbs": "EXECUTABLES",
            ".ps1": "EXECUTABLES",
            ".apk": "EXECUTABLES",
            ".app": "EXECUTABLES",
            ".gadget": "EXECUTABLES",

            # images
            ".png": "IMAGES",
            ".jpg": "IMAGES",
            ".jpeg": "IMAGES",
            ".gif": "IMAGES",
            ".bmp": "IMAGES",
            ".webp": "IMAGES",
            ".ico": "IMAGES",
            ".tiff": "IMAGES",
            ".tif": "IMAGES",
            ".heic": "IMAGES",
            ".svg": "IMAGES",
            ".psd": "IMAGES",
            ".ai": "IMAGES",
            ".raw": "IMAGES",

            # documents and text
            ".doc": "DOCUMENTS",
            ".docx": "DOCUMENTS",
            ".pdf": "DOCUMENTS",
            ".txt": "DOCUMENTS",
            ".rtf": "DOCUMENTS",
            ".odt": "DOCUMENTS",
            ".pages": "DOCUMENTS",
            ".tex": "DOCUMENTS",
            ".wpd": "DOCUMENTS",

            # tables
            ".xls": "SPREADSHEETS",
            ".xlsx": "SPREADSHEETS",
            ".xlsm": "SPREADSHEETS",
            ".csv": "SPREADSHEETS",
            ".ods": "SPREADSHEETS",

            # presentations
            ".ppt": "PRESENTATIONS",
            ".pptx": "PRESENTATIONS",
            ".pps": "PRESENTATIONS",
            ".key": "PRESENTATIONS",

            # audio
            ".mp3": "AUDIO",
            ".wav": "AUDIO",
            ".flac": "AUDIO",
            ".aac": "AUDIO",
            ".ogg": "AUDIO",
            ".m4a": "AUDIO",
            ".wma": "AUDIO",
            ".mid": "AUDIO",
            ".midi": "AUDIO",

            # video
            ".mp4": "VIDEO",
            ".mkv": "VIDEO",
            ".avi": "VIDEO",
            ".mov": "VIDEO",
            ".wmv": "VIDEO",
            ".flv": "VIDEO",
            ".webm": "VIDEO",
            ".m4v": "VIDEO",
            ".3gp": "VIDEO",
            ".mpeg": "VIDEO",
            ".mpg": "VIDEO",

            # archives
            ".zip": "ARCHIVES",
            ".rar": "ARCHIVES",
            ".7z": "ARCHIVES",
            ".tar": "ARCHIVES",
            ".gz": "ARCHIVES",
            ".bz2": "ARCHIVES",
            ".xz": "ARCHIVES",
            ".iso": "ARCHIVES",
            ".dmg": "ARCHIVES",

            # source code + programs
            ".py": "CODE",
            ".js": "CODE",
            ".html": "CODE",
            ".css": "CODE",
            ".cpp": "CODE",
            ".c": "CODE",
            ".cs": "CODE",
            ".java": "CODE",
            ".json": "CODE",
            ".xml": "CODE",
            ".php": "CODE",
            ".rb": "CODE",
            ".swift": "CODE",
            ".go": "CODE",
            ".ts": "CODE",

            # databases
            ".sql": "DATABASES",
            ".db": "DATABASES",
            ".sqlite": "DATABASES",
            ".mdb": "DATABASES",

            # ebooks
            ".epub": "BOOKS",
            ".fb2": "BOOKS",
            ".mobi": "BOOKS",
            ".djvu": "BOOKS",

            # fonts
            ".ttf": "FONTS",
            ".otf": "FONTS",
            ".woff": "FONTS",
            ".woff2": "FONTS",

            # 3d graphics
            ".obj": "3D_MODELS",
            ".fbx": "3D_MODELS",
            ".stl": "3D_MODELS",
            ".blend": "3D_MODELS",
            ".3ds": "3D_MODELS",

            # torrents and jars
            ".torrent": "TORRENTS",
            ".jar": "JARS",
        }

    def select_dir(self):
        # создает локальную переменную и если она есть то делает из нее глобальную
        directory = QFileDialog.getExistingDirectory(self, "Select directory")
        if directory:
            self.directory = directory
            self.selected_dir.setText(self.directory)

    def get_unique_path(self, folder_path, filename):
        # если файл уже есть то добавит к нему цифру в конец
        file_path = os.path.join(folder_path, filename)

        if not os.path.exists(file_path):
            return file_path

        name, extension = os.path.splitext(filename)
        counter = 1

        while True:
            new_name = f"{name}_{counter}{extension}"
            new_path = os.path.join(folder_path, new_name)

            if not os.path.exists(new_path):
                return new_path

            counter += 1

    def start_sorting(self):
        try:
            if not self.directory:
                self.selected_dir.setText("Select directory first")
                return

            sorted_count = 0
            inside = os.listdir(self.directory)
            # смотрит содержимое папки и для каждого файла делает его путь и отделяет расширение, пропускает папки внутри
            # и если расширение файла есть в словаре то выбирает название папки под него,
            # создает путь к папке соединяя исходный путь с названием папки, если ее еще нет то создает
            # собирает новый путь для файла и перемещяет
            for f in inside:
                file_path = os.path.join(self.directory, f)
                file_ext = os.path.splitext(f)[1].lower()

                if not os.path.isfile(file_path):
                    continue

                if file_ext in self.CATEGORIES:
                    folder = self.CATEGORIES[file_ext]
                else:
                    folder = "UNKNOWN"

                folder_path = os.path.join(self.directory, folder)
                os.makedirs(folder_path, exist_ok=True)

                destination = self.get_unique_path(folder_path, f)

                shutil.move(file_path, destination)
                sorted_count += 1
            self.selected_dir.setText(f"Succesfully sorted dir - {self.directory}, total sorted - {sorted_count}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SorterWindow()
    window.show()

    sys.exit(app.exec())
