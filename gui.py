import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate


class MyApp(QWidget):
    # ageRange = False
    censusStrings = [
    "Select pre-set date", 
    "Census 1841", 
    "Census 1851", 
    "Census 1861",
    "Census 1871",
    "Census 1881",
    "Census 1891",
    "Census 1901",
    "Census 1911",
    "Census 1921",
    ]

    def __init__(self):
        super().__init__()

        self.initUI()


    def ageChange(self):
        """Age text box listener."""
        self.resultsL.setText("")

    def run(self):
        """Returns results to the user."""
        try:
            date = self.dateedit.date()
            age = int(self.agetextbox.text())
            if age < 0:
                raise Exception()
            bornStart = date.addYears(-1 - age)
            bornStart = bornStart.addDays(1)
            bornEnd = date.addYears(- age)

            trueAge = True
            results = ""
            if self.dateCensusBox.currentIndex() == 1:
                results = "This is the 1841 census,"
                if age < 16 or age % 5 != 0:
                    results = results +  (" but the age of the person is exact \n " +  
                        "so we don't need to change the calculations.\n\n")
                else:
                    results = results +  (" and the age of the person is not \n " +  
                        "exact so we assume a 5 year age span.\n\n")
                    trueAge = False

            if trueAge:
                results = results + ("A person who was " + str(age) + 
                    " year(s) old on " + date.toString("dd MMM yyyy") + "\n" +
                    "was born between: " + bornStart.toString("dd MMM yyyy") +
                    " and " + bornEnd.toString("dd MMM yyyy") + ".")
            else: 
                bornStart = bornStart.addYears(-4)
                results = results + ("A person who was between " + str(age) + 
                    " and " + str(age + 4) + " year(s) old on " + date.toString("dd MMM yyyy") + "\n" +
                    "was born between: " + bornStart.toString("dd MMM yyyy") +
                    " and " + bornEnd.toString("dd MMM yyyy") + ".")
            now = date.currentDate()
            if now.day() == date.day() and now.month() == date.month():
                results = "It's their birthday today. Happy Birthday!\n\n" + results


            self.resultsL.setText(results)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Hi mum")
            msg.setInformativeText("There has been an error!")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()


    def presetDate(self, d, m, y):
        """Sets the gui date to the given value."""
        self.dateedit.setDate(QDate(y, m, d))


    def dateCensusBoxChange(self, i):
        """Census box listener."""
        self.resultsL.setText("")
        self.dateedit.blockSignals(True)
        if i == 1:
            self.presetDate(6, 6, 1841)
        elif i == 2:
            self.presetDate(30, 3, 1851)
        elif i == 3:
            self.presetDate(7, 4, 1861)
        elif i == 4:
            self.presetDate(2, 4, 1871)
        elif i == 5:
            self.presetDate(3, 4, 1881)
        elif i == 6:
            self.presetDate(5, 4, 1891)
        elif i == 7:
            self.presetDate(31, 3, 1901)
        elif i == 8:
            self.presetDate(2, 4, 1911)
        elif i == 9:
            self.presetDate(19, 6, 1921)
        self.dateedit.blockSignals(False)


    def dateeditChange(self):
        """Date listener."""
        self.resultsL.setText("")
        self.dateCensusBox.setCurrentIndex(0)


    def getAgeLayout(self):
        """Returns the age portion of the gui."""
        ageInputLayout = QHBoxLayout()
        self.ageL = QLabel('The person was', self.inputGroup)
        self.agetextbox = QLineEdit(self.inputGroup)
        self.agetextbox.setFixedWidth(50)
        ageInputLayout.addWidget(self.ageL)
        ageInputLayout.addWidget(self.agetextbox)
        ageInputLayout.addWidget(QLabel('years old', self.inputGroup))
        ageInputLayout.addStretch()
        ageLargerLayout = QVBoxLayout()
        ageLargerLayout.addLayout(ageInputLayout)
        return ageLargerLayout


    def getDateLayout(self):
        """Returns the date portion of the gui."""
        self.dateL = QLabel('on', self.inputGroup)
        self.dateedit = QDateEdit(self.inputGroup)
        self.dateedit.setDate(QDate.currentDate())
        self.dateedit.setCalendarPopup(True)
        self.dateedit.dateChanged.connect(self.dateeditChange)

        self.dateCensusBox = QComboBox()
        self.dateCensusBox.addItems(self.censusStrings)
        
        self.dateCensusBox.currentIndexChanged.connect(self.dateCensusBoxChange)
        dateGroupLayout = QHBoxLayout()
        dateGroupLayout.addWidget(self.dateL)
        dateGroupLayout.addWidget(self.dateedit)
        dateGroupLayout.addWidget(self.dateCensusBox)
        dateGroupLayout.addStretch()
        return dateGroupLayout

    def getRunLayout(self):
        """Returns the run portion of the gui."""
        runLayout = QHBoxLayout()
        self.runButton = QPushButton(self.inputGroup)
        self.runButton.setText("run")
        self.runButton.clicked.connect(self.run)
        runLayout.addStretch()
        runLayout.addWidget(self.runButton)
        runLayout.addStretch()
        return runLayout


    def createInputGroup(self):
        """Returns input section of the gui."""
        self.inputGroup = QGroupBox()
        ageLayout = self.getAgeLayout()
        dateLayout = self.getDateLayout()
        runLayout = self.getRunLayout()

        inputLayout = QVBoxLayout()
        inputLayout.addLayout(ageLayout)
        inputLayout.addLayout(dateLayout)
        inputLayout.addLayout(runLayout)
        inputLayout.addStretch()
        self.inputGroup.setLayout(inputLayout)
        return self.inputGroup


    def createResultsGroup(self):
        """Returns the results section of the gui."""
        self.resultsGroup = QGroupBox("Results")
        self.resultsL = QLabel('', self.resultsGroup)
        resultsLayout = QVBoxLayout()
        resultsLayout.addWidget(self.resultsL)
        resultsLayout.addStretch()
        self.resultsGroup.setLayout(resultsLayout)
        return self.resultsGroup


    def initUI(self):
        """Initialises the gui."""
        layout = QGridLayout()
        layout.addWidget(self.createInputGroup())
        layout.addWidget(self.createResultsGroup())
        self.setLayout(layout)

        self.setWindowTitle('Genealogy helper')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
