import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QListWidget,
)
from ui_design import Ui_MainWindow
import os, shutil
import sqlite3
from datetime import datetime


class SorterWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.setWindowTitle("File Sorter")

        self.directory = None

        self.select_button.clicked.connect(self.select_dir)
        self.sort_button.clicked.connect(self.start_sorting)

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

        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "history.db"
        )

        self.init_db()

        history_menu = self.menuBar().addMenu("History")

        history_action = history_menu.addAction("View history")
        history_action.triggered.connect(self.show_history)

        files_action = history_menu.addAction("View files")
        files_action.triggered.connect(self.show_files)

    def init_db(self):
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    old_path TEXT NOT NULL,
                    new_path TEXT NOT NULL,
                    moved_at TEXT NOT NULL
                )
            """
            )

    def save_history(self, filename, old_path, new_path):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO history (filename, old_path, new_path, moved_at) VALUES (?, ?, ?, ?)",
                (
                    filename,
                    old_path,
                    new_path,
                    datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                ),
            )

    def show_history(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Sorting history")
        dialog.resize(850, 450)

        layout = QVBoxLayout(dialog)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Filename", "Old path", "New path", "Date"])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        with sqlite3.connect(self.db_path) as conn:
            records = conn.execute(
                """
                SELECT filename, old_path, new_path, moved_at
                FROM history
                ORDER BY id DESC
            """
            ).fetchall()

        table.setRowCount(len(records))

        for row, record in enumerate(records):
            for column, value in enumerate(record):
                table.setItem(row, column, QTableWidgetItem(str(value)))

        layout.addWidget(table)
        dialog.exec()

    def show_files(self):
        if not self.directory:
            QMessageBox.warning(self, "Warning", "Select a directory first!")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Directory contents")
        dialog.resize(500, 400)

        layout = QVBoxLayout(dialog)
        file_list = QListWidget()

        try:
            files = os.listdir(self.directory)

            for filename in sorted(files):
                file_list.addItem(filename)

        except OSError as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        layout.addWidget(file_list)
        dialog.exec()

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
        # смотрит содержимое папки и для каждого файла делает его путь и отделяет расширение, пропускает папки внутри
        # и если расширение файла есть в словаре то выбирает название папки под него,
        # создает путь к папке соединяя исходный путь с названием папки, если ее еще нет то создает
        # собирает новый путь для файла и перемещает
        if not self.directory:
            QMessageBox.warning(self, "Warning", "Select a directory first!")
            return

        try:
            inside = os.listdir(self.directory)
        except OSError as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        sorted_count = 0
        error_count = 0

        # Названия папок согласно техническому заданию
        category_names = {
            "IMAGES": "Images",
            "DOCUMENTS": "Documents",
            "VIDEO": "Videos",
            "ARCHIVES": "Archives",
        }

        for filename in inside:
            old_path = os.path.join(self.directory, filename)

            if not os.path.isfile(old_path):
                continue

            try:
                extension = os.path.splitext(filename)[1].lower()

                category = self.CATEGORIES.get(extension, "Other")
                folder = category_names.get(category, category.title())

                folder_path = os.path.join(self.directory, folder)
                os.makedirs(folder_path, exist_ok=True)

                new_path = self.get_unique_path(folder_path, filename)

                # Перемещает файл
                shutil.move(old_path, new_path)

                # Сохраняет информацию в бд
                self.save_history(filename, old_path, new_path)

                sorted_count += 1

            except (OSError, sqlite3.Error) as e:
                print(f"Error with {filename}: {e}")
                error_count += 1

        QMessageBox.information(
            self,
            "Sorting completed",
            f"Successfully sorted: {sorted_count}\n" f"Errors: {error_count}",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SorterWindow()
    window.show()

    sys.exit(app.exec())
