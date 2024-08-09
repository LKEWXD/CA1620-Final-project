from PyQt6.QtWidgets import *
from gui import *
import os
import time
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_error_msg.hide()
        self.votes_John = None
        self.votes_Jane = None
        self.vote_selection = None

        self.button_submit.clicked.connect(lambda : self.submit())

        if os.path.isfile('voter_ID_records.csv'): # checks if list of used IDs exists and if not it creates one
            read_ID = csv.reader(open('voter_ID_records.csv'))
            self.ID_list = list(read_ID)
        else:
            self.ID_list = []

        if os.path.isfile('vote_results.csv'):
            read_count = csv.reader(open('vote_results.csv'))

            try:
                self.vote_list = list(read_count)
                self.votes_John = int(self.vote_list[1][1])
                self.votes_Jane = int(self.vote_list[2][1])
            except IndexError:
                self.votes_John = 0
                self.votes_Jane = 0
        else:
            self.votes_John = 0
            self.votes_Jane = 0

    def submit(self):
        ID = self.entry_ID.text().strip()
        if ID.isnumeric() == False or len(ID) != 8:
            self.label_error_msg.setText('Invalid ID: ID consists of 8 numbers with no spaces or non-numeric characters')
            self.label_error_msg.show()
            return

        for index, stored_ID in enumerate(self.ID_list):
            if self.ID_list[index][0] == ID:
                self.label_error_msg.setText('Invalid ID: Cannot vote twice')
                self.label_error_msg.show()
                return

        print('pass ID check')

        if self.radioButton_Jane.isChecked():
            self.votes_Jane += 1
            self.vote_selection = 'Jane'
        elif self.radioButton_John.isChecked():
            self.votes_John += 1
            self.vote_selection = 'John'
        else:
            self.label_error_msg.setText('Invalid vote: User must select one candidate')
            self.label_error_msg.show()
            return

        vote_record = [ID, self.vote_selection]
        print(vote_record)
        self.ID_list.append(vote_record)


        with open('voter_ID_records.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.ID_list)

        with open('vote_results.csv', 'w', newline='', encoding='utf-8') as csv_file_votes:
            total = self.votes_Jane + self.votes_John
            vote_results_list = [["Vote Total",total], ["John",self.votes_John], ["Jane",self.votes_Jane]]
            writer = csv.writer(csv_file_votes)
            for item in vote_results_list:
                writer.writerow(item)

        self.label_error_msg.hide()
        self.entry_ID.clear()
        self.group_candidates.setExclusive(False)
        self.radioButton_John.setChecked(False)
        self.radioButton_Jane.setChecked(False)
        self.group_candidates.setExclusive(True)



