from PyQt6.QtWidgets import *
from gui import *
import os
import csv


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        '''
        Creates Logic object and initializes self variables
        '''
        super().__init__()
        self.setupUi(self)
        self.label_error_msg.hide()
        self.votes_John = None
        self.votes_Jane = None
        self.vote_selection = None
        self.button_submit.clicked.connect(lambda: self.submit())
        self.read_records()

    def read_records(self) -> None:
        '''
        reads voter_ID_records.csv & vote_results.csv and adjusts counts of votes
        '''
        if os.path.isfile('voter_ID_records.csv'):  # checks if list of used IDs exists and if not it creates one
            read_ID = csv.reader(open('voter_ID_records.csv'))
            self.ID_list = list(read_ID)
        else:
            self.ID_list = []

        if os.path.isfile('vote_results.csv'):  # checks if counts of votes exists and initializes variables
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

    def submit(self) -> None:
        '''
        checks and error handles input of entry box and radio buttons. If the input is valid, information will be stored in two csv files.
        :return: -1 if entry values are invalid
        '''

        ID = self.entry_ID.text().strip()

        if ID.isnumeric() == False or len(ID) != 8:  # checks if len == 8 and is only numbers
            self.label_error_msg.setText(
                'Invalid ID: ID consists of 8 numbers with no spaces or non-numeric characters')
            self.label_error_msg.show()
            return -1

        for index, stored_ID in enumerate(self.ID_list):  # checks if ID has already been used
            if self.ID_list[index][0] == ID:
                self.label_error_msg.setText('Invalid ID: Cannot vote twice')
                self.label_error_msg.show()
                return -1

        if self.radioButton_Jane.isChecked():  # candidate selection and error handling
            self.votes_Jane += 1
            self.vote_selection = 'Jane'
        elif self.radioButton_John.isChecked():
            self.votes_John += 1
            self.vote_selection = 'John'
        else:
            self.label_error_msg.setText('Invalid vote: User must select one candidate')
            self.label_error_msg.show()
            return -1

        vote_data = [ID, self.vote_selection]  # adds voter ID and choice to output
        self.ID_list.append(vote_data)

        with open('voter_ID_records.csv', 'w', newline='', encoding='utf-8') as csv_file:  # saves output to csv file
            writer = csv.writer(csv_file)
            writer.writerows(self.ID_list)

        with open('vote_results.csv', 'w', newline='',
                  encoding='utf-8') as csv_file_votes:  # saves vote counts to a csv file
            total = self.votes_Jane + self.votes_John
            vote_results_list = [["Vote Total", total], ["John", self.votes_John], ["Jane", self.votes_Jane]]
            writer = csv.writer(csv_file_votes)
            for item in vote_results_list:
                writer.writerow(item)

        self.label_error_msg.hide()  # resets all items in menu
        self.entry_ID.clear()
        self.group_candidates.setExclusive(False)
        self.radioButton_John.setChecked(False)
        self.radioButton_Jane.setChecked(False)
        self.group_candidates.setExclusive(True)
