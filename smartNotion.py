from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
 QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, 
 QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout)

import json

# notes = {
#     'моя первая заметка' : {
#         'text' : 'оаоаоаоаоао',
#         'tags' : ['вау', 'важное']
#     },
#     'моя вторая заметка' : {
#         'text' : 'ничего себе!!!!',
#         'tags' : ['вау', 'смешное']
#     }
# }

# with open('notes_data.json', 'w', encoding='utf-8') as file:
#     json.dump(notes, file)

app = QApplication([])
notes =[]
#Интерфейс
notes_win = QWidget()
notes_win.setWindowTitle('Самые умные заметки!!!!')
notes_win.resize(900,600)

list_notes = QListWidget()
list_notes_label = QLabel('Списочек заметочек:')

button_note_create = QPushButton('Создать заметочку')
button_note_del = QPushButton('Удалить заметочку')
button_note_save = QPushButton('Сохранить заметочку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег....')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Списочек тегов')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    # field_text.setText(notes[key]['text'])
    # list_tags.clear()
    # list_tags.addItems(notes[key]['tags'])
    for note in notes:
        if key == note[0]:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'добавить заметочку', 'название заметочки:')
    if ok and note_name != '':
        # notes[note_name] = {'text': '', 'tags' : []}
        # list_notes.addItem(note_name)
        # list_tags.addItems(notes[note_name]['tags'])
        # print(notes)
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note_name)
        list_tags.addItems(note[2])
        with open(str(len(notes)-1)+'.txt','w') as file:
            file.write(note[0]+'\n'+'\n'+'\n')
       

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        # notes[key]['text'] = field_text.toPlainText()
        # with open('notes_data.json', 'w', encoding='utf-8') as file:
        #     json.dump(notes, file, sort_keys= True)
        index = 0
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index)+'.txt', 'w') as file:
                    file.write(note[0]+'\n')
                    file.write(note[1]+'\n')
                    for tag in note[2]:
                        file.write(tag+' ')
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print('заметка не выбрана')

def del_note():
    # ok = QMessageBox(ok, 'удаляем?')
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys= True)
        print(notes)
    else:
        print('заметка не выбрана')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['tags']:
            notes[key]['tags'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys= True)
        print(notes)
    else:
        print('заметка для тега не выбрана')

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['tags'])
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys= True)
        print(notes)
    else:
        print('тег не выбран')
    
def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать по тегу' and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['tags']:
                notes_filtered[note] = notes[note]
        button_tag_search.setText('сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == 'сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать по тегу')
    else:
        print('что-то идет не так')
        pass
        

list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

notes_win.show()

# with open('notes_data.json', 'r', encoding = 'utf-8') as file:
#     notes = json.load(file)
# list_notes.addItems(notes)
name = 0
note = []
while True:
    filename = str(name)+'.txt'
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.replace('\n','')
                note.append(line)
            tags = note[2].split(' ')
            note[2] = tags

            notes.append(note)
            note = []
            name += 1
    except IOError:
        break
for note in notes:
    list_notes.addItem(note[0])

app.exec_()