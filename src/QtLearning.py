import sys

from pathlib import Path

from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QTreeView, QTextEdit, QSplitter, QSizePolicy, QMenuBar, QMenu

# TODO: Split this out into its own module for handling the FS operations in an abstract manner. We need to relocate
#       all of this code up to the class.
NYTEWORKS_DIR = QStandardPaths.locate(QStandardPaths.AppDataLocation, 'NyteWoks', QStandardPaths.LocateDirectory)
if not NYTEWORKS_DIR:
    # We don't already have a directory in the roaming area
    NYTEWORKS_DIR = QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)
    if not NYTEWORKS_DIR:
        # There are no suitable areas on the system to write our data to. Throw an error and let the user decide where
        # to store the data if possible.
        # TODO: Implement some sort of handling for this unfortunate situation...
        print('Unable to find a suitable location for data on your system.', file=sys.stderr)
        sys.exit(1)
    else:
        NYTEWORKS_DIR = Path(NYTEWORKS_DIR[0] + '/Nyteworks')
else:
    NYTEWORKS_DIR = Path(NYTEWORKS_DIR)

# We have the parent directory, let's get the binder list
LIFEFLOW_DIR = NYTEWORKS_DIR / 'LifeFlow'
BINDERS_DIR = LIFEFLOW_DIR / 'Binders'

# Ensure that the binder directory exists
BINDERS_DIR.mkdir(parents=True, exist_ok=True)

# Some business logic that is currently necessary...
# TODO: Find a more elegant way to handle the Inbox folder
INBOX_DIR = BINDERS_DIR / 'Inbox'
Path(INBOX_DIR).mkdir(parents=True, exist_ok=True)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('LifeFlow - Notes for the Real World')
        self._create_ui()

    def _create_ui(self):
        self._setup_menu_bar()
        self._create_note_tree_view()
        self.text_area = QTextEdit()
        self.setCentralWidget(self.note_tree_view)

        self.note_tree_view.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.text_area.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.note_tree_view.clicked.connect(self.selected_note_changed)

        self.splitter = QSplitter()
        self.splitter.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.splitter.addWidget(self.note_tree_view)
        self.splitter.addWidget(self.text_area)

        self.splitter.setSizes([self.note_tree_view.sizeHint().width(), 1000])

        self.setCentralWidget(self.splitter)

    def _setup_menu_bar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction('Open')
        fileMenu.addAction('New')
        fileMenu.addAction('Save')
        fileMenu.addAction('Save As...')

        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction('Undo')
        editMenu.addAction('Redo')
        editMenu.addSeparator()
        editMenu.addAction('Cut')
        editMenu.addAction('Copy')
        editMenu.addAction('Paste')

    def _create_note_tree_view(self):
        self.note_tree_view = QTreeView()
        self.note_tree_view.setHeaderHidden(True)
        self.note_tree_view.setModel(self._create_note_model())

    def _create_note_model(self):
        self.note_tree_model = QStandardItemModel()
        root = self.note_tree_model.invisibleRootItem()

        # TODO: Investigate what else pathlib might be able to do for us better here.
        # TODO: Right now the note hierarchy is hard-coded. We need a more generic recursion code and need to consider
        #       how the database will be implemented so that other views fit in the hierarchy.
        binders = [binder for binder in BINDERS_DIR.iterdir() if binder.is_dir()]
        for binder in binders:
            binder_name = binder.parts[-1]
            binder_item = QStandardItem(binder_name)
            binder_item.setData(False, 1)
            notebooks = [notebook for notebook in binder.iterdir() if notebook.is_dir()]
            for notebook in notebooks:
                notebook_name = notebook.parts[-1]
                notebook_item = QStandardItem(notebook_name)
                notebook_item.setData(False, 1)
                notes = [note for note in notebook.iterdir() if note.is_file()]
                for note in notes:
                    note_name = note.parts[-1]
                    note_item = QStandardItem(note_name)
                    note_item.is_note = True
                    note_item.setData(True, 1)
                    notebook_item.appendRow(note_item)
                binder_item.appendRow(notebook_item)
            root.appendRow(binder_item)

        return self.note_tree_model

    def selected_note_changed(self, index):
        item = index.model().itemFromIndex(index)
        if item.data(1):
            notebook = item.parent().text()
            binder = item.parent().parent().text()
            note = BINDERS_DIR / binder / notebook / item.text()
            print('I should get:', note)
            note_text = None
            with open(note, 'r') as note_file:
                note_text = note_file.readlines()
            self.text_area.setText(''.join(note_text))



def main():
    app = QApplication()

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
