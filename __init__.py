from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from typing import Sequence, Union

class OsceDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Enumeration tool")
        self.layout = QVBoxLayout()

        label1 = QLabel("Enter lines below, each line goes into {{c1::line}} in a note")
        self.noteseditor = QPlainTextEdit()
        self.layout.addWidget(label1)
        self.layout.addWidget(self.noteseditor)

        label2 = QLabel("Enter name of deck below")
        self.deck_taker = QLineEdit()
        self.layout.addWidget(label2)
        self.layout.addWidget(self.deck_taker)

        label3 = QLabel("Enter name of note type below")
        self.notetype_taker = QLineEdit()
        self.layout.addWidget(label3)
        self.layout.addWidget(self.notetype_taker)

        label4 = QLabel("Enter title below")
        self.tag_taker = QLineEdit()
        self.layout.addWidget(label4)
        self.layout.addWidget(self.tag_taker)

        label5 = QLabel("Press button below to make notes")
        self.button = QPushButton("Create notes")
        self.button.clicked.connect(self.makeNotes)
        self.layout.addWidget(label5)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def makeNotes(self):
        notetype_name: str = self.notetype_taker.text()
        model_to_use: Union[None, NoteType] = mw.col.models.byName(notetype_name)
        if model_to_use is None:
            outstring = "Unable to find the specified note type.\nPlease enter the name of a note type that exists.\nNo cards are being made."
            showInfo(outstring)
            return False

        title: str = self.tag_taker.text()

        deck_name: str = self.deck_taker.text()
        did = mw.col.decks.id(deck_name)
        mw.col.decks.select(did)
        deck = mw.col.decks.get(did)

        notes_content: Sequence[str] = make_osce_notes(self.noteseditor.toPlainText())

        model_to_use['did'] = did
        mw.col.models.save(model_to_use)

        deck['mid'] = model_to_use['id']
        mw.col.decks.save(deck)

        for content in notes_content:
            new_note: Note = mw.col.newNote()
            new_note.fields[0] = title + "<br>" + content
            mw.col.addNote(new_note)
        showInfo("Cards created successfully.")

osce_dialog = OsceDialog()

def showoscedialog() -> None:
    osce_dialog.show()

def make_osce_notes(a: str) -> Sequence[str]:
    string_list: Sequence[str] = a.split('\n')
    out_list = []
    for line in string_list:
        important_line = line
        index_of_line = string_list.index(line)
        if index_of_line == 0:
            out_list.append(f"{1}: {{{{c1::{important_line}}}}}")
        if index_of_line > 0:
            not_important_lines = string_list[:index_of_line]
            outstring = ""
            i = 1
            for notimportline in not_important_lines:
                outstring += f"{i}: {notimportline}<br>"
                i += 1
            outstring += f"{i}: {{{{c1::{important_line}}}}}"
            out_list.append(outstring)

    return out_list

action = QAction()
action.setText("Enumeration tool")
mw.form.menuTools.addAction(action)
action.triggered.connect(showoscedialog)
