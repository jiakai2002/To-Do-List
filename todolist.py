import os
import random
from MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow
import sqlite3

# We inherit from the main class QtWidgets.QmainWindow
# We also import and inherit from Ui_MainWindow

# create data base table
conn = sqlite3.connect('mylist.db')
c = conn.cursor()
c.execute("CREATE TABLE if not exists todo_list(list_item text)")
conn.commit()
conn.close()


class MainWindow(QMainWindow, Ui_MainWindow):

    # initilize args as in library
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # setup clicked handlers
        self.add_pushbutton.clicked.connect(self.add_task)
        self.delete_pushbutton.clicked.connect(self.delete_task)
        self.clear_pushbutton.clicked.connect(self.clear_task)
        self.done_pushbutton_2.clicked.connect(self.done_task)
        self.save_actionSave.triggered.connect(self.save_file)

        # get music player widget object
        self.player = QMediaPlayer()

        # set up current_path to know if file is open
        self.current_path = None

        # retrieve save
        self.grab_database()

    # grab items from database and add to screen
    def grab_database(self):
        # grab data in records
        conn = sqlite3.connect('mylist.db')
        c = conn.cursor()
        c.execute("SELECT * FROM todo_list")
        records = c.fetchall()
        conn.commit()
        conn.close()

        # loop through records and add to screen
        for record in records:
            print(record)
            self.todolist_listWidget.addItem(str(record[0]))

    def save_file(self):
        conn = sqlite3.connect('mylist.db')
        c = conn.cursor()

        # delete old data in database
        c.execute('DELETE FROM todo_list;',)

        # add new data in database
        lw = self.todolist_listWidget
        items = []
        for x in range(lw.count()):
            items.append(lw.item(x))
        for item in items:
            c.execute("INSERT INTO todo_list VALUES (:item)",
                      {'item': item.text()},)
            print(item.text())
        conn.commit()
        conn.close()

    def play_audio(self):
        audio_file = random.choice(os.listdir(
            "C:\\Users\\ASUS\\Desktop\\KAI_PYTHON\\todo_list_app\\audio"))
        file_path = "C:\\Users\\ASUS\\Desktop\\KAI_PYTHON\\todo_list_app\\audio\\" + audio_file
        url = QUrl.fromLocalFile(file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    # add task to list

    def add_task(self):

        # grab task in the task box
        item = self.typetask_lineEdit.text()

        if item:
            # add task into the list
            self.todolist_listWidget.addItem(item)

        # clear the task box
            self.typetask_lineEdit.setText("")

        # update progress
        self.update_progress()

    # delete task from list
    def delete_task(self):

        # grab the selected task
        clicked = self.todolist_listWidget.currentRow()

        # delete selected task from todo list
        self.todolist_listWidget.takeItem(clicked)

        # update progress
        self.update_progress()

    # clear all tasks from list
    def clear_task(self):
        self.todolist_listWidget.clear()

        # update progress
        self.update_progress()

    # strike out selected task
    def done_task(self):

        # grab the selected task
        item = self.todolist_listWidget.currentItem()
        if item:
            # if selected task is done, undone it instead
            f = item.font()
            if f.strikeOut() == True:
                f.setStrikeOut(False)
                item.setFont(f)

            # strike out non-empty task
            else:
                f = item.font()
                f.setStrikeOut(True)
                item.setFont(f)

        # update progress
        self.update_progress()

    # track progress of tasks on progress bar
    def update_progress(self):

        # grab the total number of rows in the list
        total = self.todolist_listWidget.count()

        # if empty list, set value to 0
        if total == 0:
            value = 0

        # else count number of tasks done
        else:
            done = 0
            for i in range(total):
                item = self.todolist_listWidget.item(i)
                f = item.font()
                if f.strikeOut() == True:
                    done += 1

            # zero denominator case
            if done == 0:
                value = 0
            else:
                # calculate progress value
                value = round(done / total * 100, 2)
                if value == 100:
                    self.play_audio()

        # set the progress value accordingly
        self.progress_progressBar.setProperty("value", value)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationName("Kai's To Do List")

    window = MainWindow()
    window.show()
    app.exec_()
