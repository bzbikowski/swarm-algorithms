import json
import os

from PySide2.QtCore import QUrl
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QPlainTextEdit

import lib.algorithms as alg


class Ui(QWidget):
    # todo make GUI more user friendly
    def __init__(self, parent):
        super(Ui, self).__init__()
        self.setParent(parent)
        self.mainLayout = None
        self.algorithmLayout = None
        self.webPageView = None
        self.algorithmTitle = None
        self.algorithmList = None
        self.chosenAlgorithm = None
        self.algorithmSplitLayout = None
        self.algorithmNext = None
        self.problemLayout = None
        self.parametersLayout = None
        self.mainHelpLayout = None
        self.parametersFullLayout = None
        self.finalButton = None

        self.setupUI()

    def setupUI(self):
        self.mainLayout = QHBoxLayout(self)
        self.algorithmLayout = QVBoxLayout()

        self.algorithmTitle = QLabel("Wybierz algorytm")
        self.algorithmLayout.addWidget(self.algorithmTitle)

        self.algorithmSplitLayout = QHBoxLayout()
        self.algorithmLayout.addLayout(self.algorithmSplitLayout)

        self.algorithmList = QListWidget()
        self.algorithmList.clicked.connect(self.chooseAlgorithm)
        self.algorithmSplitLayout.addWidget(self.algorithmList)
        self.makeAlgorithmList()

        self.algorithmNext = QPushButton("Dalej", self)
        self.algorithmNext.released.connect(self.goToNextLayout)
        self.algorithmSplitLayout.addWidget(self.algorithmNext)

        self.webPageView = QWebEngineView()
        # todo make default page
        self.webPageView.load(QUrl('http://google.com'))

        self.mainLayout.addLayout(self.algorithmLayout)
        self.mainLayout.addWidget(self.webPageView)

    def makeAlgorithmList(self):
        for file in os.listdir("./src/schema"):
            self.algorithmList.addItem(file[:-5])

    def chooseAlgorithm(self, index):
        # todo change web page
        print(index.row(), index.data())

    def goToNextLayout(self):
        self.chosenAlgorithm = self.algorithmList.currentItem().data(0)
        self.clearLayout(self.algorithmSplitLayout)
        self.algorithmSplitLayout.layout().deleteLater()
        self.clearLayout(self.algorithmLayout)
        self.algorithmLayout.layout().deleteLater()
        self.clearLayout(self.mainLayout)

        self.mainHelpLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.mainHelpLayout)

        self.parametersFullLayout = QHBoxLayout()
        self.mainHelpLayout.addLayout(self.parametersFullLayout)

        # todo make layout for choosing problem
        self.problemLayout = QVBoxLayout()
        self.parametersFullLayout.addLayout(self.problemLayout)

        self.test = QPlainTextEdit("Kappa")
        self.problemLayout.addWidget(self.test)

        self.parametersLayout = QVBoxLayout()
        self.parametersFullLayout.addLayout(self.parametersLayout)

        self.makeParametersLayout()

        self.finalButton = QPushButton("Next")
        self.finalButton.released.connect(self.startAlgorithm)
        self.mainHelpLayout.addWidget(self.finalButton)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def makeParametersLayout(self):
        data = None
        with open(f"src/schema/{self.chosenAlgorithm}.json", "r") as f:
            data = json.load(f)
            print(data['elements'][0])
        for element in data['elements']:
            layout = QHBoxLayout()
            label = QLabel(element['name'])
            text = None
            if element['type'] == 'plain_text':
                text = QPlainTextEdit()
            else:
                pass
            layout.addWidget(label)
            layout.addWidget(text)
            self.parametersLayout.addLayout(layout)

    @staticmethod
    def fun1(*args):
        return 50 - args[0] ** 2 - args[1] ** 2

    def startAlgorithm(self):
        # todo check correctness of data
        params = []
        for index in range(self.parametersLayout.count()):
            child = self.parametersLayout.itemAt(index)
            for x in range(child.count()):
                grandchild = child.itemAt(x).widget()
                if isinstance(grandchild, QPlainTextEdit):
                    params.append(float(grandchild.toPlainText()))
        print(params)
        # todo choose ideal algorithm
        algorithm = alg.BeesAlgorithm(self.fun1, 2, [(-5.00, 5.00)])
        algorithm.start_algorithm()