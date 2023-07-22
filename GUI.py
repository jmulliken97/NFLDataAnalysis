from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from data_processor import DataProcessor
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import webscraper
import os

class Ui_MainWindow(object):
    def __init__(self):
        self.textEdit = QtWidgets.QTextEdit()  
        self.data_processor = DataProcessor(self.textEdit)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1000, 600))

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

        # JSON Viewer
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
        
        # self.pushButton_compare = QtWidgets.QPushButton(self.json_tab)
        # self.pushButton_compare.setGeometry(QtCore.QRect(700, 20, 89, 25))
        # self.pushButton_compare.setObjectName("pushButton_compare")
        
        self.pushButton_correlation = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_correlation.setGeometry(QtCore.QRect(800, 60, 150, 30)) 
        self.pushButton_correlation.setObjectName("pushButton_correlation")
        
        self.comboBox_sort_order = QtWidgets.QComboBox(self.json_tab)  
        self.comboBox_sort_order.setGeometry(QtCore.QRect(240, 20, 100, 31)) 
        self.comboBox_sort_order.addItems(["Descending", "Ascending"])
        self.comboBox_sort_order.setObjectName("comboBox_sort_order")
        
        self.pushButton_display_stats = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_display_stats.setGeometry(QtCore.QRect(800, 100, 150, 30)) 
        self.pushButton_display_stats.setObjectName("pushButton_display_stats")

        # self.pushButton_handle_missing = QtWidgets.QPushButton(self.json_tab)
        # self.pushButton_handle_missing.setGeometry(QtCore.QRect(800, 140, 150, 30)) 
        # self.pushButton_handle_missing.setObjectName("pushButton_handle_missing")

        # self.pushButton_detect_outliers = QtWidgets.QPushButton(self.json_tab)
        # self.pushButton_detect_outliers.setGeometry(QtCore.QRect(800, 180, 150, 30)) 
        # self.pushButton_detect_outliers.setObjectName("pushButton_detect_outliers")

        self.textEdit_comparison = QtWidgets.QTextEdit(self.json_tab)
        self.textEdit_comparison.setGeometry(QtCore.QRect(40, 560, 711, 180))  
        self.textEdit_comparison.setReadOnly(True) 

        self.canvas.setParent(self.json_tab)
        self.canvas.setGeometry(800, 300, 400, 300)

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
        self.pushButton.setText(_translate("MainWindow", "Scrape Player"))
        self.pushButton_all.setText(_translate("MainWindow", "Scrape URL"))
        self.pushButton_load.setText(_translate("MainWindow", "Load JSON"))
        self.pushButton_plot.setText(_translate("MainWindow", "Plot Stats"))
        # self.pushButton_compare.setText(_translate("MainWindow", "Compare Players"))
        self.pushButton_legend.setText(_translate("MainWindow", "Show Legend"))
        self.pushButton_correlation.setText(_translate("MainWindow", "Correlation Analysis")) 
        self.pushButton_display_stats.setText(_translate("MainWindow", "Descriptive Stats")) 
        # self.pushButton_handle_missing.setText(_translate("MainWindow", "Handle Missing Data")) 
        # self.pushButton_detect_outliers.setText(_translate("MainWindow", "Detect Outliers")) 

        # Connect button to function
        self.pushButton.clicked.connect(self.get_player_stats)
        self.pushButton_all.clicked.connect(self.scrape_all)
        self.pushButton_load.clicked.connect(self.load_json_file)
        self.pushButton_plot.clicked.connect(self.plot_stats)
        self.pushButton_compare.clicked.connect(self.compare_stats)
        self.comboBox_year.currentIndexChanged.connect(self.update_table)
        self.comboBox_sort_column.currentIndexChanged.connect(self.sort_dataframe)
        self.comboBox_sort_order.currentIndexChanged.connect(self.sort_dataframe)
        self.pushButton_correlation.clicked.connect(self.correlation_analysis)
        self.pushButton_display_stats.clicked.connect(self.display_stats)
        # self.pushButton_handle_missing.clicked.connect(self.handle_missing_data)
        # self.pushButton_detect_outliers.clicked.connect(self.detect_outliers)
        self.pushButton_legend.clicked.connect(self.show_legend)

    def get_player_stats(self):
        url = self.lineEdit.text()
        player_name = self.lineEdit_player.text()
        stat_type = self.comboBox.currentText()
        player_stats = webscraper.get_player_stats(url, player_name, stat_type)
        self.textEdit_player_stats.setText(str(player_stats))

    def scrape_all(self):
        url = self.lineEdit.text()
        stat_type = self.comboBox.currentText()
        webscraper.scrape_all(url, stat_type)
        QMessageBox.information(self.centralwidget, "Success", f"All {stat_type.capitalize()} data scraped successfully.")

    def load_json_file(self):
        self.data_processor.load_json()
        self.comboBox_year.clear()
        self.comboBox_year.addItems(sorted(self.data_processor.data_dict.keys()))
        self.label_filename.setText(f"Loaded file: {os.path.basename(self.data_processor.get_file_name())}")

        year = self.comboBox_year.currentText()
        data_df = self.data_processor.data_dict[year]

        self.tableWidget.setRowCount(len(data_df))
        self.tableWidget.setColumnCount(len(data_df.columns))
        self.tableWidget.setHorizontalHeaderLabels(data_df.columns)
        for i, (index, row) in enumerate(data_df.iterrows()):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        self.comboBox_sort_column.clear()
        self.comboBox_sort_options.addItems(self.data_processor.get_columns())


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
        
    def correlation_analysis(self):
        year, ok = QtWidgets.QInputDialog.getItem(None, "Input", "Select a year:", list(self.data_processor.data_dict.keys()), editable=False)
        if ok:
            correlation_matrix = self.data_processor.correlation_analysis(year)
            if correlation_matrix is not None:
               
                dialog = QtWidgets.QDialog()
                dialog.setWindowTitle("Correlation Analysis")
                dialog.resize(1000, 600)  

                figure = Figure()
                canvas = FigureCanvas(figure)

                layout = QtWidgets.QVBoxLayout()
                layout.addWidget(canvas)
                dialog.setLayout(layout)

                ax = figure.add_subplot(111)
                sns.heatmap(correlation_matrix, ax=ax)
                canvas.draw()
                
                explanation = "A correlation close to 1 indicates a strong positive relationship, -1 indicates strong negative relationship, a near 0 indicates no relationship."
                label = QtWidgets.QLabel(explanation)
                layout.insertWidget(0, label)

                dialog.exec_()
            else:
                self.textEdit.setText("No data available for the selected year.")
        else:
            self.textEdit.setText("No year selected.")

    def display_stats(self):
        years = list(self.data_processor.data_dict.keys())
        years.append('All')
        year, ok = QInputDialog.getItem(None, "Input", "Select a year:", years, editable=False)
        if ok:
            year = None if year == 'All' else year
            stats = self.data_processor.descriptive_stats(year)
            if stats is not None:
                dialog = QDialog()
                dialog.setWindowTitle("Descriptive Statistics")
                table = QTableWidget()
                table.setRowCount(len(stats))
                table.setColumnCount(len(stats.columns))
                stats = stats.round(2)
                table.setHorizontalHeaderLabels(stats.columns)
                table.setVerticalHeaderLabels(stats.index.str.capitalize())
                for i in range(len(stats)):
                    for j in range(len(stats.columns)):
                        table.setItem(i, j, QTableWidgetItem(str(stats.iat[i, j])))
                layout = QVBoxLayout()
                layout.addWidget(table)
                dialog.setLayout(layout)
                dialog.exec_()
            else:
                self.textEdit.setText("No data available for the selected year.")

    # def handle_missing_data(self):
    #     year = self.comboBox_year.currentText()
    #     self.data_processor.handle_missing_data(year)
    #     self.textEdit.setText("Missing data has been handled.")

    # def detect_outliers(self):
    #     year = self.comboBox_year.currentText()
    #     stat = self.comboBox_stats.currentText()
    #     outliers = self.data_processor.detect_outliers(year, stat)
    #     if outliers is not None and not outliers.empty:
    #         self.textEdit.setText(outliers.to_string(index=False))
    #     else:
    #         self.textEdit.setText("No outliers detected for the selected year and stat.")
  
    # def compare_stats(self):
    #     players = []
    #     while True:
    #         year, ok0 = QInputDialog.getItem(None, "Input", "Select a year:", list(self.data_processor.data_dict.keys()), editable=False)
    #         if ok0:
    #             player, ok1 = QInputDialog.getItem(None, "Input", "Select a player:", self.data_processor.get_player_names(year), editable=False)
    #             if ok1:
    #                 players.append((year, player))
    #                 add_another = QMessageBox.question(None, 'Question', 'Would you like to add another player?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #                 if add_another == QMessageBox.No:
    #                     break
    #             else:
    #                 break
    #     stat, ok2 = QInputDialog.getItem(None, "Input", "Select a stat:", self.data_processor.get_columns(), editable=False)
    #     if ok2:
    #         comparison_results = self.data_processor.compare_stats([stat], players)
    #         self.textEdit_comparison.setText(comparison_results) 

    def plot_stats(self):
        player, ok1 = QInputDialog.getItem(None, "Input", "Select a player:", self.data_processor.get_player_names(), editable=False)
        if not ok1:
            return
        stat, ok2 = QInputDialog.getItem(None, "Input", "Select a stat:", self.data_processor.get_columns(), editable=False)
        if not ok2:
            return
        self.data_processor.plot_player_stat(player, stat)

