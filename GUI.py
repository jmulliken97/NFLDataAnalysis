from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from data_processor import DataProcessor
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import webscraper
import penalties
from data_loader import DataLoader
from roster import load_roster
import pandas as pd
import openpyxl

bucket_name = "statsbucketpython"

class Ui_MainWindow(object):
    def __init__(self):
        self.data_loader = DataLoader(bucket_name)
        self.preloaded_data = self.data_loader.get_data()
        self.textEdit = QtWidgets.QTextEdit()  
        self.data_processor = DataProcessor(bucket_name)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.rosters_data = load_roster()

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
        self.label = QtWidgets.QLabel(self.scraping_tab)
        self.label.setGeometry(QtCore.QRect(40, 40, 141, 31))
        self.label.setObjectName("label")
        
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
        
        self.checkBox_team_def = QtWidgets.QCheckBox(self.scraping_tab)
        self.checkBox_team_def.setGeometry(QtCore.QRect(50, 240, 200, 31))
        self.checkBox_team_def.setText("Team Defense")
        self.checkBox_team_def.setObjectName("checkBox_team_def")

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
        
        self.tableWidget = QtWidgets.QTableWidget(self.json_tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 765, 690))

        # add widgets to the json tab
        self.comboBox_year = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_year.setGeometry(QtCore.QRect(10, 20, 75, 31))
        self.comboBox_year.setObjectName("comboBox_year")
        
        self.comboBox_selector = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_selector.setGeometry(QtCore.QRect(95, 20, 100, 31))
        self.comboBox_selector.addItems(['Passing', 'Rushing', 'Receiving', 'Defense', 'Kicking'])
        self.comboBox_selector.setObjectName("comboBox_selector")
        self.comboBox_selector.setCurrentIndex(0)
        
        self.comboBox_sort = QtWidgets.QComboBox(self.json_tab)
        self.comboBox_sort.setGeometry(QtCore.QRect(205, 20, 75, 31))
        self.comboBox_sort.setObjectName("comboBox_sort")
        
        self.pushButton_legend = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_legend.setGeometry(QtCore.QRect(600, 20, 200, 31))
        self.pushButton_legend.setObjectName("pushButton_legend")

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

        self.pushButton_detect_outliers = QtWidgets.QPushButton(self.json_tab)
        self.pushButton_detect_outliers.setGeometry(QtCore.QRect(800, 260, 175, 30)) 
        self.pushButton_detect_outliers.setObjectName("pushButton_detect_outliers")

        # add json tab to the tab widget
        self.tabWidget.addTab(self.json_tab, "Data Viewer")
        
        # Prediction Tab
        self.predict_tab = QtWidgets.QWidget()
        self.predict_tab.setObjectName("predict_tab")
        
        # add predict tab to the tab widget
        self.tabWidget.addTab(self.predict_tab, "Predictions")
        
        # Roster Tab
        self.roster_tab = QtWidgets.QWidget()
        self.roster_tab.setObjectName("roster_tab")
        
        # Add widgets to the roster tab
        self.comboBox_team = QtWidgets.QComboBox(self.roster_tab)
        self.comboBox_team.setGeometry(QtCore.QRect(10, 20, 100, 31))
        self.comboBox_team.setObjectName("comboBox_team")
        self.comboBox_team.addItems(list(self.rosters_data.keys()))

        self.tableWidget_roster = QtWidgets.QTableWidget(self.roster_tab)
        self.tableWidget_roster.setGeometry(QtCore.QRect(10, 60, 965, 690))
        self.tableWidget_roster.setColumnCount(3) 
        self.tableWidget_roster.setHorizontalHeaderLabels(["Number", "Name", "Position"])

        # add roster tab to the tab widget
        self.tabWidget.addTab(self.roster_tab, "Roster")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.load_data_from_s3()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NFL Stats Analysis"))
        self.pushButton_all.setText(_translate("MainWindow", "Scrape Data"))
        self.pushButton_plot.setText(_translate("MainWindow", "Plot Stats"))
        self.pushButton_distro.setText(_translate("MainWindow", "Distribution"))
        self.pushButton_legend.setText(_translate("MainWindow", "Show Legend"))
        self.pushButton_correlation.setText(_translate("MainWindow", "Correlation Analysis")) 
        self.pushButton_display_stats.setText(_translate("MainWindow", "Descriptive Stats")) 
        self.pushButton_detect_outliers.setText(_translate("MainWindow", "Detect Outliers"))
        self.pushButton_penalties.setText(QtCore.QCoreApplication.translate("MainWindow", "Scrape Penalties"))


        # Connect button to function
        self.pushButton_all.clicked.connect(self.scrape_all)
        self.pushButton_plot.clicked.connect(self.plot_stats)
        self.pushButton_distro.clicked.connect(self.distribution)
        self.pushButton_correlation.clicked.connect(self.correlation_analysis)
        self.pushButton_display_stats.clicked.connect(self.display_stats)
        self.pushButton_detect_outliers.clicked.connect(self.detect_outliers)
        self.pushButton_legend.clicked.connect(self.show_legend)
        self.pushButton_penalties.clicked.connect(self.scrape_penalties)
        self.comboBox_sort.currentIndexChanged.connect(self.update_table)
        self.comboBox_selector.currentTextChanged.connect(self.load_data_from_s3)
        self.comboBox_year.currentIndexChanged.connect(self.year_changed)
        self.comboBox_team.currentIndexChanged.connect(self.update_roster_table)


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
        if self.checkBox_team_def.isChecked():
            stat.append("team-defense")
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
                max_players = 960
            elif stat_type == 'kicking':
                max_players = 35
            elif stat_type == 'team-defense':
                max_players = 32
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
        penalties.scrape_all(start_year, end_year) 
        QMessageBox.information(self.centralwidget, "Success", f"Penalty data for {start_year}-{end_year} scraped successfully.")

    def load_data_from_s3(self):
        stat_type = self.comboBox_selector.currentText()
        self.data_processor.load_and_process_data(self.preloaded_data, stat_type)
        self.comboBox_year.clear()
        self.comboBox_year.addItems(sorted(self.data_processor.data_dict.keys(), key=int))
        if "2022" in self.data_processor.data_dict:
            self.comboBox_year.setCurrentText("2022")
            
        year = self.comboBox_year.currentText()
        data_df = self.data_processor.data_dict[year]
        self.comboBox_sort.clear()

        sort_columns = [col for col in data_df.columns if col not in ["Player", "Team", "Year"]]
        self.comboBox_sort.addItems(sort_columns)
        
        if 'Yds' in data_df.columns:
            index_of_yds = self.comboBox_sort.findText('Yds')
            self.comboBox_sort.setCurrentIndex(index_of_yds)
        else:
            index_of_pts = self.comboBox_sort.findText('Pts')
            if index_of_pts != -1:
                self.comboBox_sort.setCurrentIndex(index_of_pts)
        if stat_type == "Kicking":
            index_of_pts = self.comboBox_sort.findText('Pts')
            if index_of_pts != -1:
                self.comboBox_sort.setCurrentIndex(index_of_pts)

        self.update_table()
        self.tableWidget.setRowCount(len(data_df))
        
        display_columns = [col for col in data_df.columns if col != "Year"]
        self.tableWidget.setColumnCount(len(display_columns))
        self.tableWidget.setHorizontalHeaderLabels(display_columns)
        for i, (index, row) in enumerate(data_df[display_columns].iterrows()):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

    def update_table(self):
        self.tableWidget.clearContents()
        year = self.comboBox_year.currentText()
        
        if year in self.data_processor.data_dict:
            data_df = self.data_processor.data_dict[year]
            sort_column = self.comboBox_sort.currentText()
            
            # Sorting the dataframe by the selected column (if necessary)
            if sort_column in data_df.columns:
                data_df = data_df.sort_values(by=sort_column, ascending=False)
                
            display_columns = [col for col in data_df.columns if col != "Year"]
            self.tableWidget.setRowCount(len(data_df))
            self.tableWidget.setColumnCount(len(display_columns))
            self.tableWidget.setHorizontalHeaderLabels(display_columns)
            
            for i, (index, row) in enumerate(data_df[display_columns].iterrows()):
                for j, value in enumerate(row):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

    def year_changed(self):
        selected_stat_type = self.comboBox_selector.currentText()
        year = self.comboBox_year.currentText()
        
        if year in self.data_processor.data_dict:
            data_df = self.data_processor.data_dict[year]
            
            # Update the sort combo box
            self.comboBox_sort.clear()
            sort_columns = [col for col in data_df.columns if col not in ["Player", "Team", "Year"]]
            self.comboBox_sort.addItems(sort_columns)
            if 'Yds' in data_df.columns:
                self.comboBox_sort.setCurrentText('Yds')
            elif 'Pts' in data_df.columns:
                self.comboBox_sort.setCurrentText('Pts')
            
            # Update the table
            self.update_table()
            
    def export_to_excel(self, data, filename):
        # Convert the data to DataFrame if it's not already a DataFrame
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)

        # Save to Excel
        filepath = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", f"{filename}.xlsx", "Excel Files (*.xlsx)")[0]
        if filepath:
            data.to_excel(filepath, engine='openpyxl')

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
                
                export_btn = QtWidgets.QPushButton("Export to Excel")
                export_btn.clicked.connect(lambda: self.export_to_excel(correlation_matrix, "correlation_analysis"))
                layout.addWidget(export_btn)

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
                
                export_btn = QtWidgets.QPushButton("Export to Excel")
                export_btn.clicked.connect(lambda: self.export_to_excel(stats, "descriptive_stats"))
                layout.addWidget(export_btn)

                dialog.exec_()
            else:
                self.textEdit.setText("No data available for the selected year.")

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
                
                export_btn = QtWidgets.QPushButton("Export to Excel")
                export_btn.clicked.connect(lambda: self.export_to_excel(outliers_df, "outliers_analysis"))
                layout.addWidget(export_btn)

                dialog.exec_()
            else:
                self.textEdit.setText("No outliers detected for the selected year.")
        else:
            self.textEdit.setText("No year selected.")

    def distribution(self):
        stats_columns = self.data_processor.get_columns()
        stats_columns.append("All")
        stat, ok = QtWidgets.QInputDialog.getItem(None, "Input", "Select a stat:", stats_columns, editable=False)
        if not ok:
            return
        years = list(self.data_processor.data_dict.keys())
        years.append('All')
        year, ok = QtWidgets.QInputDialog.getItem(None, "Input", "Select a year:", years, editable=False)
        if not ok:
            return
        year = None if year == 'All' else year
        data_dict = {}
        if stat == "All":
            for each_stat in stats_columns:
                if each_stat not in ["Player", "Team", "Year", "All"]:
                    data_dict[each_stat] = self.data_processor.distribution(each_stat, year)
        else:
            data_dict[stat] = self.data_processor.distribution(stat, year)

        plot_data = data_dict[stat] if stat != "All" else list(data_dict.values())[0]
        plot_window = QtWidgets.QDialog()
        plot_window.setWindowTitle(f"Distribution of {stat} in {'all years' if year is None else year}")
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(canvas)
        plot_window.setLayout(layout)
        ax.hist(plot_data, bins='auto', alpha=0.7, rwidth=0.85, color='blue', edgecolor='black')
        ax.set_title(f'Distribution of {stat} in {"all years" if year is None else year}')
        ax.set_xlabel(stat)
        ax.set_ylabel('Frequency')
        
        export_btn = QtWidgets.QPushButton("Export to Excel")
        export_btn.clicked.connect(lambda: self.export_to_excel(data_dict, "distribution_data"))
        layout.addWidget(export_btn)

        plot_window.exec_()

    def plot_stats(self):
        player, ok1 = QInputDialog.getItem(None, "Input", "Select a player:", self.data_processor.get_player_names(), editable=False)
        if not ok1:
            return
        stat, ok2 = QInputDialog.getItem(None, "Input", "Select a stat:", self.data_processor.get_columns(), editable=False)
        if not ok2:
            return
        fig = self.data_processor.plot_player_stat(player, stat)
        if fig:
            plot_window = QtWidgets.QDialog()
            plot_window.setWindowTitle(f"{player}'s {stat} Stats Over the Years")
            canvas = FigureCanvas(fig)
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(canvas)
            plot_window.setLayout(layout)
            plot_window.exec_()

    def update_roster_table(self):
        team_selected = self.comboBox_team.currentText()
        roster = self.rosters_data.get(team_selected, [])

        self.tableWidget_roster.setRowCount(len(roster))
        for i, player in enumerate(roster):
            self.tableWidget_roster.setItem(i, 0, QTableWidgetItem(player["Number"]))
            self.tableWidget_roster.setItem(i, 1, QTableWidgetItem(player["Name"]))
            self.tableWidget_roster.setItem(i, 2, QTableWidgetItem(player["Position"]))

