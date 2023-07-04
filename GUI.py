from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from webscraper import get_player_stats, scrape_all
from data_processor import DataProcessor

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
        self.comboBox_sort_column.setGeometry(QtCore.QRect(190, 60, 141, 31))
        self.comboBox_sort_column.setObjectName("comboBox_sort_column")
        
        self.lineEdit_player_names = QtWidgets.QLineEdit(self.json_tab)
        self.lineEdit_player_names.setGeometry(QtCore.QRect(40, 20, 211, 31))
        self.lineEdit_player_names.setObjectName("lineEdit_player_names")
        
        self.lineEdit_stat_columns = QtWidgets.QLineEdit(self.json_tab)
        self.lineEdit_stat_columns.setGeometry(QtCore.QRect(40, 50, 211, 31))
        self.lineEdit_stat_columns.setObjectName("lineEdit_stat_columns")
        
        self.textEdit = QtWidgets.QTextEdit(self.json_tab)
        self.textEdit.setGeometry(QtCore.QRect(40, 60, 711, 491))
        self.data_processor = DataProcessor(self.textEdit)

        # add widgets to the json tab
        self.pushButton_load = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_load.setGeometry(QtCore.QRect(350, 20, 89, 25))
        self.pushButton_load.setObjectName("pushButton_load")

        self.textEdit = QtWidgets.QTextEdit(self.json_tab)
        self.textEdit.setGeometry(QtCore.QRect(40, 60, 711, 491))

        self.pushButton_plot = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_plot.setGeometry(QtCore.QRect(450, 20, 89, 25))
        self.pushButton_plot.setObjectName("pushButton_plot")

        self.comboBox_sort = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_sort.setGeometry(QtCore.QRect(190, 20, 141, 31))
        self.comboBox_sort.addItems(["No Sort", "Ascending", "Descending"])
        self.comboBox_sort.setObjectName("comboBox_sort")
        
        self.label_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_filename.setGeometry(QtCore.QRect(600, 20, 180, 20))
        self.label_filename.setText("No file loaded.")

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

        # Connect button to function
        self.pushButton.clicked.connect(self.scrape_espn)
        self.pushButton_all.clicked.connect(self.scrape_all_data)
        self.pushButton_load.clicked.connect(self.load_json_file)
        self.comboBox_sort_column.currentIndexChanged.connect(self.sort_dataframe)
        self.pushButton_plot.clicked.connect(self.plot_stats)

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
        sortable_columns = self.data_processor.get_sortable_columns()
        self.comboBox_sort_column.clear() 
        self.comboBox_sort_column.addItems(["No Sort"] + sortable_columns)
        self.label_filename.setText(f"Loaded file: {self.data_processor.get_file_name()}")  # Display the loaded file's name

    def sort_dataframe(self):
        sort_by = self.comboBox_sort_column.currentText()
        sort_order = self.comboBox_sort.currentText()
        self.data_processor.sort_dataframe(sort_by, sort_order)

    def plot_stats(self):
        players = []
        stats = []

        while True:
            player, ok1 = QtWidgets.QInputDialog.getItem(None, "Input", "Select a player:", self.data_processor.get_player_names(), editable=False)
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


 