from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from data_processor import DataProcessor
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import webscraper
import penalties
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
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1000, 780))

        # Scraping tab
        self.scraping_tab = QtWidgets.QWidget()
        self.scraping_tab.setObjectName("scraping_tab")
        
        # add widgets to the scraping tab
        self.comboBox_start_year = QtWidgets.QComboBox(self.scraping_tab)
        self.comboBox_start_year.setGeometry(QtCore.QRect(300, 80, 100, 31))
        self.comboBox_start_year.addItems([str(year) for year in range(1970, 2023)])  
        self.comboBox_start_year.setObjectName("comboBox_start_year")
        self.comboBox_start_year.setCurrentText("2000") 

        self.comboBox_end_year = QtWidgets.QComboBox(self.scraping_tab)
        self.comboBox_end_year.setGeometry(QtCore.QRect(450, 80, 100, 31))
        self.comboBox_end_year.addItems([str(year) for year in range(1970, 2023)])
        self.comboBox_end_year.setObjectName("comboBox_end_year")
        self.comboBox_end_year.setCurrentText("2022") 

        self.label_years = QtWidgets.QLabel(self.scraping_tab)
        self.label_years.setGeometry(QtCore.QRect(300, 40, 300, 20))
        self.label_years.setObjectName("label_years")
        self.label_years.setText(QtCore.QCoreApplication.translate("MainWindow", "Years: (Start) to (End)"))

        self.checkBox_passing = QtWidgets.QCheckBox(self.scraping_tab)
        self.checkBox_passing.setGeometry(QtCore.QRect(50, 40, 200, 31))
        self.checkBox_passing.setText("Passing")
        self.checkBox_passing.setObjectName("checkBox_passing")

        self.checkBox_rushing = QtWidgets.QCheckBox(self.scraping_tab)
        self.checkBox_rushing.setGeometry(QtCore.QRect(50, 80, 200, 31))
        self.checkBox_rushing.setText("Rushing")
        self.checkBox_rushing.setObjectName("checkBox_rushing")

        self.checkBox_receiving = QtWidgets.QCheckBox(self.scraping_tab)
        self.checkBox_receiving.setGeometry(QtCore.QRect(50, 120, 200, 31))
        self.checkBox_receiving.setText("Receiving")
        self.checkBox_receiving.setObjectName("checkBox_receiving")
        
        self.checkBox_defense = QtWidgets.QCheckBox(self.scraping_tab)
        self.checkBox_defense.setGeometry(QtCore.QRect(50, 160, 200, 31))
        self.checkBox_defense.setText("Defense")
        self.checkBox_defense.setObjectName("checkBox_defense")
        
        self.checkBox_kicking = QtWidgets.QCheckBox(self.scraping_tab)
        self.checkBox_kicking.setGeometry(QtCore.QRect(50, 200, 200, 31))
        self.checkBox_kicking.setText("Kicking")
        self.checkBox_kicking.setObjectName("checkBox_kicking")

        self.pushButton_all = QtWidgets.QPushButton(self.scraping_tab)
        self.pushButton_all.setGeometry(QtCore.QRect(800, 80, 175, 30))
        self.pushButton_all.setObjectName("pushButton_all")
        
        self.pushButton_penalties = QtWidgets.QPushButton(self.scraping_tab)
        self.pushButton_penalties.setGeometry(QtCore.QRect(800, 120, 175, 30))
        self.pushButton_penalties.setObjectName("pushButton_penalties")

        # add scraping tab to the tab widget
        self.tabWidget.addTab(self.scraping_tab, "Scraping")

        # JSON Viewer
        self.json_tab = QtWidgets.QWidget()
        self.json_tab.setObjectName("json_tab")

        self.comboBox_sort_column = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_sort_column.setGeometry(QtCore.QRect(190, 100, 141, 31))
        self.comboBox_sort_column.setObjectName("comboBox_sort_column")
        
        self.tableWidget = QtWidgets.QTableWidget(self.json_tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 765, 690))

        # add widgets to the json tab
        self.comboBox_year = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_year.setGeometry(QtCore.QRect(10, 20, 75, 31))
        self.comboBox_year.setObjectName("comboBox_year")

        self.comboBox_sort_options = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_sort_options.setGeometry(QtCore.QRect(100, 20, 100, 31))
        self.comboBox_sort_options.setObjectName("comboBox_sort_options")
        self.comboBox_sort_options.setCurrentText("Yds")
        
        self.comboBox_sort_order = QtWidgets.QComboBox(self.json_tab)  
        self.comboBox_sort_order.setGeometry(QtCore.QRect(215, 20, 100, 31)) 
        self.comboBox_sort_order.addItems(["Descending", "Ascending"])
        self.comboBox_sort_order.setObjectName("comboBox_sort_order")
        
        self.label_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_filename.setGeometry(QtCore.QRect(600, 20, 180, 20))
        self.label_filename.setText("No file loaded.")
        
        self.pushButton_legend = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_legend.setGeometry(QtCore.QRect(350, 20, 200, 31))
        self.pushButton_legend.setObjectName("pushButton_legend")
        
        self.pushButton_load = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_load.setGeometry(QtCore.QRect(800, 60, 175, 30))
        self.pushButton_load.setObjectName("pushButton_load")

        self.pushButton_plot = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_plot.setGeometry(QtCore.QRect(800, 100, 175, 30))
        self.pushButton_plot.setObjectName("pushButton_plot")
        
        self.pushButton_distro = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_distro.setGeometry(QtCore.QRect(800, 140, 175, 30))
        self.pushButton_distro.setObjectName("pushButton_distro")
        
        self.pushButton_correlation = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_correlation.setGeometry(QtCore.QRect(800, 180, 175, 30)) 
        self.pushButton_correlation.setObjectName("pushButton_correlation")
        
        self.pushButton_display_stats = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_display_stats.setGeometry(QtCore.QRect(800, 220, 175, 30)) 
        self.pushButton_display_stats.setObjectName("pushButton_display_stats")

        # self.pushButton_handle_missing = QtWidgets.QPushButton(self.json_tab)
        # self.pushButton_handle_missing.setGeometry(QtCore.QRect(800, 140, 150, 30)) 
        # self.pushButton_handle_missing.setObjectName("pushButton_handle_missing")

        self.pushButton_detect_outliers = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_detect_outliers.setGeometry(QtCore.QRect(800, 260, 175, 30)) 
        self.pushButton_detect_outliers.setObjectName("pushButton_detect_outliers")

        # add json tab to the tab widget
        self.tabWidget.addTab(self.json_tab, "Data Viewer")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NFL Stats Analysis"))
        self.pushButton_all.setText(_translate("MainWindow", "Scrape Data"))
        self.pushButton_load.setText(_translate("MainWindow", "Load Data"))
        self.pushButton_plot.setText(_translate("MainWindow", "Plot Stats"))
        self.pushButton_distro.setText(_translate("MainWindow", "Distribution"))
        self.pushButton_legend.setText(_translate("MainWindow", "Show Legend"))
        self.pushButton_correlation.setText(_translate("MainWindow", "Correlation Analysis")) 
        self.pushButton_display_stats.setText(_translate("MainWindow", "Descriptive Stats")) 
        # self.pushButton_handle_missing.setText(_translate("MainWindow", "Handle Missing Data")) 
        self.pushButton_detect_outliers.setText(_translate("MainWindow", "Detect Outliers"))
        self.pushButton_penalties.setText(QtCore.QCoreApplication.translate("MainWindow", "Scrape Penalties"))


        # Connect button to function
        self.pushButton_all.clicked.connect(self.scrape_all)
        self.pushButton_load.clicked.connect(self.load_json_file)
        self.pushButton_plot.clicked.connect(self.plot_stats)
        self.pushButton_distro.clicked.connect(self.distribution)
        self.comboBox_year.currentIndexChanged.connect(self.update_table)
        self.comboBox_sort_column.currentIndexChanged.connect(self.sort_dataframe)
        self.comboBox_sort_order.currentIndexChanged.connect(self.sort_dataframe)
        self.pushButton_correlation.clicked.connect(self.correlation_analysis)
        self.pushButton_display_stats.clicked.connect(self.display_stats)
        # self.pushButton_handle_missing.clicked.connect(self.handle_missing_data)
        self.pushButton_detect_outliers.clicked.connect(self.detect_outliers)
        self.pushButton_legend.clicked.connect(self.show_legend)
        self.pushButton_penalties.clicked.connect(self.scrape_penalties)
        self.pushButton_load.clicked.connect(self.load_from_db)
        
    def load_from_db (self):
        self.data_processor.load_data_from_db()
        self.comboBox_year.clear()
        self.comboBox_year.addItems(sorted(self.data_processor.data_dict.keys(), key=int))

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

    def scrape_all(self):
        stat = []
        if self.checkBox_passing.isChecked():
            stat.append("passing")
        if self.checkBox_rushing.isChecked():
            stat.append("rushing")
        if self.checkBox_receiving.isChecked():
            stat.append("receiving")
        if self.checkBox_defense.isChecked():
            stat.append("defense")
        if self.checkBox_kicking.isChecked():
            stat.append("kicking")
        if not stat:
            QMessageBox.warning(self.centralwidget, "Warning", "No stat type selected.")
            return

        start_year = int(self.comboBox_start_year.currentText())
        end_year = int(self.comboBox_end_year.currentText())
        if start_year > end_year:
            QMessageBox.warning(self.centralwidget, "Warning", "Start year should be less than or equal to end year.")
            return

        for stat_type in stat:
            if stat_type == 'passing':
                max_players = 35
            elif stat_type == 'rushing':
                max_players = 50
            elif stat_type == 'receiving':
                max_players = 100
            elif stat_type == 'defense':
                max_players = 150
            elif stat_type == 'kicking':
                max_players = 35
            else:
                raise ValueError(f"Unknown stat type: {stat_type}")
            webscraper.scrape_all(stat_type, max_players, start_year, end_year)

        QMessageBox.information(self.centralwidget, "Success", f"Data for {', '.join(stat).capitalize()} for {start_year}-{end_year} scraped successfully.")
        
    def scrape_penalties(self):
        start_year = int(self.comboBox_start_year.currentText())
        end_year = int(self.comboBox_end_year.currentText())
        if start_year < 2006:
            QMessageBox.warning(self.centralwidget, "Warning", "Start year should not be less than 2006.")
            return
        if start_year > end_year:
            QMessageBox.warning(self.centralwidget, "Warning", "Start year should be less than or equal to end year.")
            return
        penalties.scrape_all(start_year, end_year)  # Call the penalties scraping function
        QMessageBox.information(self.centralwidget, "Success", f"Penalty data for {start_year}-{end_year} scraped successfully.")

    def sort_dataframe(self):
        year = self.comboBox_year.currentText()
        index = self.comboBox_sort_options.findText("Yds")
        if index >= 0:
            self.comboBox_sort_options.setCurrentIndex(index)
        sort_by = self.comboBox_sort_options.currentText()
        sort_order = self.comboBox_sort_order.currentText() 
        self.data_processor.sort_dataframe(year, sort_by, sort_order)
        self.update_table()
        
    def update_table(self):
        self.tableWidget.clearContents()
        year = self.comboBox_year.currentText()
        if year in self.data_processor.data_dict:
            data_df = self.data_processor.data_dict[year]
            self.tableWidget.setRowCount(len(data_df))
            self.tableWidget.setColumnCount(len(data_df.columns))
            self.tableWidget.setHorizontalHeaderLabels(data_df.columns)
            for i, (index, row) in enumerate(data_df.iterrows()):
                for j, cell in enumerate(row):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(cell)))
        else:
            print(f"No data for year {year}")

    def show_legend(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Legend")
        dialog.resize(400, 300)

        text_edit = QtWidgets.QTextEdit(dialog)
        text_edit.setGeometry(10, 10, 380, 280)
        text_edit.setReadOnly(True)

        # Display the legend
        text_edit.append("<b><u>Passing Stats:</u></b>")
        text_edit.append("<b>Player:</b> Player's name")
        text_edit.append("<b>Team:</b> Player's team")
        text_edit.append("<b>Gms:</b> Number of games")
        text_edit.append("<b>Att:</b> Number of attempts")
        text_edit.append("<b>Cmp:</b> Number of completions")
        text_edit.append("<b>Pct:</b> Completion percentage")
        text_edit.append("<b>Yds:</b> Total passing yards")
        text_edit.append("<b>YPA:</b> Yards per attempt")
        text_edit.append("<b>TD:</b> Number of touchdowns")
        text_edit.append("<b>TD%:</b> Touchdown percentage")
        text_edit.append("<b>Int:</b> Number of interceptions")
        text_edit.append("<b>Int%:</b> Interception percentage")
        text_edit.append("<b>Lg TD:</b> Longest Pass TD?")
        text_edit.append("<b>Lg:</b> Longest pass")
        text_edit.append("<b>Sack:</b> Number of sacks")
        text_edit.append("<b>Loss:</b> Yards lost due to sacks")
        text_edit.append("<b>Rate:</b> Quarterback rating")
        text_edit.append("<b>Score:</b> Calculated Player Score")
        text_edit.append("<b>TD:INT Ratio:</b> Ratio of TDs to INTs")
        text_edit.append("<b>ANY/A</b> Adjusted Net Yards per Pass Attempt")

        text_edit.append("\n<b><u>Rushing Stats:</u></b>")
        text_edit.append("<b>Player:</b> Player's name")
        text_edit.append("<b>Team:</b> Player's team")
        text_edit.append("<b>Gms:</b> Number of games")
        text_edit.append("<b>Att:</b> Number of attempts")
        text_edit.append("<b>Yds:</b> Total rushing yards")
        text_edit.append("<b>Avg:</b> Average yards per rush")
        text_edit.append("<b>YPG:</b> Rushing yards per game")
        text_edit.append("<b>Lg TD:</b> Longest rush a TD?")
        text_edit.append("<b>Lg:</b> Longest rush")
        text_edit.append("<b>TD:</b> Number of touchdowns")
        text_edit.append("<b>FD:</b> Number of first downs")
        text_edit.append("<b>Score:</b> Calculated Player Score")
        
        text_edit.append("\n<b><u>Rushing Efficiency Stats:</u></b>")
        text_edit.append("<b>Y/A:</b> Yards per attempt")
        text_edit.append("<b>TD/A:</b> Touchdowns per attempt")
        text_edit.append("<b>TD/G:</b> Touchdowns per game")

        text_edit.append("\n<b><u>Receiving Stats:</u></b>")
        text_edit.append("<b>Player:</b> Player's name")
        text_edit.append("<b>Team:</b> Player's team")
        text_edit.append("<b>Gms:</b> Number of games")
        text_edit.append("<b>Rec:</b> Number of receptions")
        text_edit.append("<b>Yds:</b> Total receiving yards")
        text_edit.append("<b>Avg:</b> Average yards per reception")
        text_edit.append("<b>YPG:</b> Receiving yards per game")
        text_edit.append("<b>Lg TD:</b> Longest touchdown reception")
        text_edit.append("<b>Lg:</b> Longest reception")
        text_edit.append("<b>TD:</b> Number of receiving touchdowns")
        text_edit.append("<b>FD:</b> Number of first downs from receptions")
        text_edit.append("<b>Tar:</b> Number of times targeted by the quarterback")
        text_edit.append("<b>YAC:</b> Yards after catch")
        text_edit.append("<b>Score:</b> Calculated Player Score")
        
        text_edit.append("\n<b><u>Receiving Efficiency Stats:</u></b>")
        text_edit.append("<b>Y/R:</b> Yards per reception")
        text_edit.append("<b>TD/R:</b> Touchdowns per reception")
        text_edit.append("<b>Y/Tgt:</b> Yards per target")
        text_edit.append("<b>Rec/Tgt:</b> Receptions per target")
        text_edit.append("<b>TD/G:</b> Touchdowns per game")

        dialog.exec_()

    def correlation_analysis(self):
        years = list(self.data_processor.data_dict.keys())
        years.append('All')
        year, ok = QtWidgets.QInputDialog.getItem(None, "Input", "Select a year:", years, editable=False)
        if ok:
            year = None if year == 'All' else year
            correlation_matrix = self.data_processor.correlation_analysis(year)
            if correlation_matrix is not None:
               
                dialog = QtWidgets.QDialog()
                dialog.setWindowTitle("Correlation Analysis")
                dialog.resize(1000, 700)  

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

    def detect_outliers(self):
        years = list(self.data_processor.data_dict.keys())
        years.append('All')
        year, ok = QtWidgets.QInputDialog.getItem(None, "Input", "Select a year:", years, editable=False)
        if ok:
            year = None if year == 'All' else year
            outliers_df = self.data_processor.detect_outliers(year)
            if outliers_df is not None and not outliers_df.empty:
                dialog = QtWidgets.QDialog()
                dialog.setWindowTitle("Outliers Analysis")
                dialog.resize(1000, 700)

                table = QtWidgets.QTableWidget()
                table.setColumnCount(len(outliers_df.columns))
                table.setRowCount(len(outliers_df.index))
                table.setHorizontalHeaderLabels(outliers_df.columns)
                table.setVerticalHeaderLabels(outliers_df.index.astype(str))

                for i in range(len(outliers_df.index)):
                    for j in range(len(outliers_df.columns)):
                        item = QtWidgets.QTableWidgetItem(str(outliers_df.iat[i, j]))
                        table.setItem(i, j, item)

                layout = QtWidgets.QVBoxLayout()
                layout.addWidget(table)
                dialog.setLayout(layout)

                explanation = "The table below shows the detected outliers for the selected year. An outlier is a data point that significantly differs from other observations. It could be due to variability in the data or experimental errors."
                label = QtWidgets.QLabel(explanation)
                layout.insertWidget(0, label)

                dialog.exec_()
            else:
                self.textEdit.setText("No outliers detected for the selected year.")
        else:
            self.textEdit.setText("No year selected.")

    def distribution(self):
        stat, ok = QtWidgets.QInputDialog.getItem(None, "Input", "Select a stat:", self.data_processor.get_columns(), editable=False)
        if not ok:
            return
        years = list(self.data_processor.data_dict.keys())
        years.append('All')
        year, ok = QtWidgets.QInputDialog.getItem(None, "Input", "Select a year:", years, editable=False)
        if not ok:
            return
        year = None if year == 'All' else year
        data = self.data_processor.distribution(stat, year)
        plot_window = QtWidgets.QDialog()
        plot_window.setWindowTitle(f"Distribution of {stat} in {'all years' if year is None else year}")
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(canvas)
        plot_window.setLayout(layout)
        ax.hist(data, bins='auto', alpha=0.7, rwidth=0.85, color='blue', edgecolor='black')
        ax.set_title(f'Distribution of {stat} in {"all years" if year is None else year}')
        ax.set_xlabel(stat)
        ax.set_ylabel('Frequency')

        plot_window.exec_()

    def plot_stats(self):
        player, ok1 = QInputDialog.getItem(None, "Input", "Select a player:", self.data_processor.get_player_names(), editable=False)
        if not ok1:
            return
        stat, ok2 = QInputDialog.getItem(None, "Input", "Select a stat:", self.data_processor.get_columns(), editable=False)
        if not ok2:
            return
        self.data_processor.plot_player_stat(player, stat)

