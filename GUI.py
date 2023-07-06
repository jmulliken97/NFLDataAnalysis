from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from webscraper import get_player_stats, scrape_all
from data_processor import DataProcessor
import os

class Ui_MainWindow(object):
    def __init__(self):
        self.textEdit = QtWidgets.QTextEdit()  
        self.data_processor = DataProcessor(self.textEdit)  
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))

        # Scraping tab
        self.scraping_tab = QtWidgets.QWidget()
        self.scraping_tab.setObjectName("scraping_tab")
        
        # add widgets to the scraping tab
        self.label = QtWidgets.QLabel(self.scraping_tab)
        self.label.setGeometry(QtCore.QRect(40, 40, 141, 31))
        self.label.setObjectName("label")
        
        self.lineEdit = QtWidgets.QLineEdit(self.scraping_tab)
        self.lineEdit.setGeometry(QtCore.QRect(190, 40, 551, 31))
        self.lineEdit.setObjectName("lineEdit")
        
        self.textEdit_player_stats = QtWidgets.QTextEdit(self.scraping_tab)
        self.textEdit_player_stats.setGeometry(QtCore.QRect(40, 230, 711, 300))
        self.textEdit_player_stats.setObjectName("textEdit_player_stats")
        
        self.label_player = QtWidgets.QLabel(self.scraping_tab)
        self.label_player.setGeometry(QtCore.QRect(40, 90, 141, 31))
        self.label_player.setObjectName("label_player")
        
        self.lineEdit_player = QtWidgets.QLineEdit(self.scraping_tab)
        self.lineEdit_player.setGeometry(QtCore.QRect(190, 90, 551, 31))
        self.lineEdit_player.setObjectName("lineEdit_player")

        self.comboBox = QtWidgets.QComboBox(self.scraping_tab)
        self.comboBox.setGeometry(QtCore.QRect(190, 140, 551, 31))
        self.comboBox.addItems(["passing", "rushing", "receiving"])
        self.comboBox.setObjectName("comboBox")

        self.pushButton = QtWidgets.QPushButton(self.scraping_tab)
        self.pushButton.setGeometry(QtCore.QRect(250, 190, 89, 25))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_all = QtWidgets.QPushButton(self.scraping_tab)
        self.pushButton_all.setGeometry(QtCore.QRect(450, 190, 89, 25))
        self.pushButton_all.setObjectName("pushButton_all")

        # add scraping tab to the tab widget
        self.tabWidget.addTab(self.scraping_tab, "Scraping")

        # JSON Viewer tab
        self.json_tab = QtWidgets.QWidget()
        self.json_tab.setObjectName("json_tab")

        self.comboBox_sort_column = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_sort_column.setGeometry(QtCore.QRect(190, 100, 141, 31))
        self.comboBox_sort_column.setObjectName("comboBox_sort_column")
        
        self.tableWidget = QtWidgets.QTableWidget(self.json_tab)
        self.tableWidget.setGeometry(QtCore.QRect(40, 60, 711, 491))

        # add widgets to the json tab
        self.pushButton_load = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_load.setGeometry(QtCore.QRect(500, 20, 89, 25))
        self.pushButton_load.setObjectName("pushButton_load")
        
        self.comboBox_year = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_year.setGeometry(QtCore.QRect(40, 20, 75, 31))
        self.comboBox_year.setObjectName("comboBox_year")

        self.comboBox_sort_options = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_sort_options.setGeometry(QtCore.QRect(130, 20, 100, 31))
        self.comboBox_sort_options.setObjectName("comboBox_sort_options")
        
        self.pushButton_legend = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_legend.setGeometry(QtCore.QRect(350, 20, 89, 25))
        self.pushButton_legend.setObjectName("pushButton_legend")

        self.pushButton_plot = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_plot.setGeometry(QtCore.QRect(600, 20, 89, 25))
        self.pushButton_plot.setObjectName("pushButton_plot")
        
        self.label_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_filename.setGeometry(QtCore.QRect(600, 20, 180, 20))
        self.label_filename.setText("No file loaded.")
        
        self.pushButton_compare = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_compare.setGeometry(QtCore.QRect(700, 20, 89, 25))
        self.pushButton_compare.setObjectName("pushButton_compare")
        
        self.comboBox_sort_order = QtWidgets.QComboBox(self.json_tab)  
        self.comboBox_sort_order.setGeometry(QtCore.QRect(240, 20, 100, 31)) 
        self.comboBox_sort_order.addItems(["Descending", "Ascending"])
        self.comboBox_sort_order.setObjectName("comboBox_sort_order")  
 

        # add json tab to the tab widget
        self.tabWidget.addTab(self.json_tab, "JSON Viewer")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NFL Stats Scraper"))
        self.label.setText(_translate("MainWindow", "Enter NFL URL:"))
        self.label_player.setText(_translate("MainWindow", "Enter Player Name:"))
        self.pushButton.setText(_translate("MainWindow", "Scrape"))
        self.pushButton_all.setText(_translate("MainWindow", "Scrape All"))
        self.pushButton_load.setText(_translate("MainWindow", "Load JSON"))
        self.pushButton_plot.setText(_translate("MainWindow", "Plot Stats"))
        self.pushButton_compare.setText(_translate("MainWindow", "Compare"))
        self.pushButton_legend.setText(_translate("MainWindow", "Legend"))

        # Connect button to function
        self.pushButton.clicked.connect(self.scrape_espn)
        self.pushButton_all.clicked.connect(self.scrape_all_data)
        self.pushButton_load.clicked.connect(self.load_json_file)
        self.comboBox_sort_column.currentIndexChanged.connect(self.sort_dataframe)
        self.pushButton_plot.clicked.connect(self.plot_stats)
        self.comboBox_year.currentIndexChanged.connect(self.update_table)
        self.pushButton_compare.clicked.connect(self.compare_stats)
        self.comboBox_sort_options.currentIndexChanged.connect(self.sort_dataframe)
        self.pushButton_legend.clicked.connect(self.show_legend)
        self.comboBox_sort_order.currentIndexChanged.connect(self.sort_dataframe)

    def scrape_espn(self):
        url = self.lineEdit.text()
        player_name = self.lineEdit_player.text()
        stat_type = self.comboBox.currentText()
        player_stats = get_player_stats(url, stat_type, player_name)
        print(player_stats)
        self.textEdit_player_stats.setText(str(player_stats))

    def scrape_all_data(self):
        url = self.lineEdit.text()
        stat_type = self.comboBox.currentText()
        scrape_all(url, stat_type)
        QMessageBox.information(self.centralwidget, "Success", f"{stat_type.capitalize()} data scraped successfully.")

    def load_json_file(self):
        self.data_processor.load_json()
        self.comboBox_year.clear()
        self.comboBox_year.addItems(sorted(self.data_processor.data_dict.keys()))
        self.label_filename.setText(f"Loaded file: {os.path.basename(self.data_processor.get_file_name())}")  # Display the loaded file's name

        year = self.comboBox_year.currentText()  # Get the selected year
        data_df = self.data_processor.data_dict[year]  # Get the DataFrame for the selected year

        # Fill the QTableWidget with the data from the DataFrame
        self.tableWidget.setRowCount(len(data_df))
        self.tableWidget.setColumnCount(len(data_df.columns))
        self.tableWidget.setHorizontalHeaderLabels(data_df.columns)
        for i, (index, row) in enumerate(data_df.iterrows()):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        self.comboBox_sort_column.clear()
        self.comboBox_sort_options.addItems([col for col in self.data_processor.get_sortable_columns(year) if col != "Player"])  # Exclude the "Player" column

    def sort_dataframe(self):
        year = self.comboBox_year.currentText()
        sort_by = self.comboBox_sort_options.currentText()
        sort_order = self.comboBox_sort_order.currentText() 
        self.data_processor.sort_dataframe(year, sort_by, sort_order)
        self.update_table()
        
    def update_table(self):
        year = self.comboBox_year.currentText()
        data_df = self.data_processor.data_dict[year]
        self.tableWidget.setRowCount(len(data_df))
        self.tableWidget.setColumnCount(len(data_df.columns))
        self.tableWidget.setHorizontalHeaderLabels(data_df.columns)
        for i, (index, row) in enumerate(data_df.iterrows()):
            for j, cell in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(cell)))
                
    def show_legend(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Legend")
        dialog.resize(400, 300)

        text_edit = QtWidgets.QTextEdit(dialog)
        text_edit.setGeometry(10, 10, 380, 280)
        text_edit.setReadOnly(True)

        # Display the legend
        text_edit.append("<b><u>Passing Stats:</u></b>")
        text_edit.append("<b>Pass Yds:</b> Total passing yards")
        text_edit.append("<b>Yds/Att:</b> Yards per attempt")
        text_edit.append("<b>Att:</b> Number of attempts")
        text_edit.append("<b>Cmp:</b> Number of completions")
        text_edit.append("<b>Cmp %:</b> Completion percentage")
        text_edit.append("<b>TD:</b> Number of touchdowns")
        text_edit.append("<b>INT:</b> Number of interceptions")
        text_edit.append("<b>Rate:</b> Quarterback rating")
        text_edit.append("<b>1st:</b> Number of first downs")
        text_edit.append("<b>1st%:</b> First down percentage")
        text_edit.append("<b>20+:</b> Number of 20+ yards passes")
        text_edit.append("<b>40+:</b> Number of 40+ yards passes")
        text_edit.append("<b>Lng:</b> Longest pass")
        text_edit.append("<b>Sck:</b> Number of sacks")
        text_edit.append("<b>SckY:</b> Yards lost due to sacks")
        text_edit.append("<b>TD:INT Ratio:</b> Ratio of touchdowns to interceptions")
        text_edit.append("<b>ANY/A:</b> Adjusted net yards per pass attempt")
        
        text_edit.append("\n<b><u>Rushing Stats:</u></b>")
        text_edit.append("<b>Rush Yds:</b> Total rushing yards")
        text_edit.append("<b>Att:</b> Number of attempts")
        text_edit.append("<b>TD:</b> Number of touchdowns")
        text_edit.append("<b>20+:</b> Number of 20+ yards rushes")
        text_edit.append("<b>40+:</b> Number of 40+ yards rushes")
        text_edit.append("<b>Lng:</b> Longest rush")
        text_edit.append("<b>Rush 1st:</b> Number of first downs")
        text_edit.append("<b>Rush 1st%:</b> First down percentage")
        text_edit.append("<b>Rush FUM:</b> Number of fumbles")
        
        text_edit.append("\n<b><u>Receiving Stats:</u></b>")
        text_edit.append("<b>Rec:</b> Number of receptions")
        text_edit.append("<b>Yds:</b> Total receiving yards")
        text_edit.append("<b>TD:</b> Number of receiving touchdowns")
        text_edit.append("<b>20+:</b> Number of 20+ yards receptions")
        text_edit.append("<b>40+:</b> Number of 40+ yards receptions")
        text_edit.append("<b>LNG:</b> Longest reception")
        text_edit.append("<b>Rec 1st:</b> Number of first downs from receptions")
        text_edit.append("<b>1st%:</b> Percentage of receptions for first downs")
        text_edit.append("<b>Rec FUM:</b> Number of fumbles during receptions")
        text_edit.append("<b>Rec YAC/R:</b> Average yards after catch per reception")
        text_edit.append("<b>Tgts:</b> Number of times targeted by the quarterback")

    

        dialog.exec_()
        
    def compare_stats(self):
        year = self.comboBox_year.currentText()
        stats = self.comboBox_sort_options.currentText()
        players = self.lineEdit_player.text().split(",")  # Assuming players are separated by commas
        comparison_results = self.data_processor.compare_stats(year, stats, players)
        self.textEdit_player_stats.setText(comparison_results)

        while True:
            player, ok1 = QtWidgets.QInputDialog.getItem(None, "Input", "Select a player:", self.data_processor.get_player_names(year), editable=False)
            if ok1:
                players.append(player)
                add_another = QtWidgets.QMessageBox.question(None, 'Question', 'Would you like to add another player?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if add_another == QtWidgets.QMessageBox.No:
                    break
            else:
                break

        player_scores = {}
        for player in players:
            player_data = self.data_processor.data_dict[year][self.data_processor.data_dict[year]['Player'] == player]
            if not player_data.empty:
                player_data_dict = player_data.to_dict(orient='records')[0]
                stats_type = self.data_processor.determine_stats_type(player_data_dict)
                if stats_type != "unknown":
                    player_scores[player] = self.data_processor.calculate_score(player_data_dict, stats_type)

        sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Player Comparison")
        dialog.resize(400, 300)

        text_edit = QtWidgets.QTextEdit(dialog)
        text_edit.setGeometry(10, 10, 380, 280)
        text_edit.setReadOnly(True)

        for player, score in sorted_players:
            text_edit.append(f"<b>{player}</b>: {score}")

        dialog.exec_()


    def plot_stats(self):
        year = self.comboBox_year.currentText()
        players = []
        stats = []

        while True:
            player, ok1 = QtWidgets.QInputDialog.getItem(None, "Input", "Select a player:", self.data_processor.get_player_names(year), editable=False)
            if ok1:
                players.append(player)
                add_another = QtWidgets.QMessageBox.question(None, 'Question', 'Would you like to add another player?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if add_another == QtWidgets.QMessageBox.No:
                    break
            else:
                break

        while True:
            stat, ok2 = QtWidgets.QInputDialog.getItem(None, "Input", "Select a stat:", self.data_processor.get_stat_columns(), editable=False)
            if ok2:
                stats.append(stat)
                add_another = QtWidgets.QMessageBox.question(None, 'Question', 'Would you like to add another stat?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if add_another == QtWidgets.QMessageBox.No:
                    break
            else:
                break

        self.data_processor.plot_stats(stats, players)


 