from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from UI.fuckthis import Ui_Form as RecipeWidgetUI

class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

class BaseRecipeWidget(QWidget, RecipeWidgetUI):
    def __init__(self, parent, recipe):
        QWidget.__init__(self, parent)
        self.recipe = recipe
        # self.vbox = QVBoxLayout(self)
        # self.label = QLabel()
        # self.label.setText('Go fuck yourself')
        # self.textBrowser = QTextBrowser()
        # self.vbox.addWidget(self.label)
        # self.vbox.addWidget(self.textBrowser)
        # self.setLayout(self.vbox)
        self.setupUi(self)


    def update(self):
        for ingredient in self.recipe.ingredients:
            self.listWidget.addItem(ingredient)

        self.label.setText(self.recipe.name)
        self.textBrowser.setText(self.recipe.instructions)
        self.updateGeometry()

class RecipeBank(QWidget):
    def __init__(self, parent, questions=[]):
        """
        Initializing the QuestionBank
        Args:
            parent: Parent Widget of the QuestionBank
            questions: list of Question objects
        """

        QWidget.__init__(self, parent)
        self.setMinimumWidth(250)
        self.setMinimumHeight(500)
        self.setObjectName("QuestionBank")

        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Storing Question objects
        self.questions = questions

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        #self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Initializing QScrollArea
        self.scroll.setMinimumWidth(250)
        self.scroll.setMinimumHeight(500)
        self.scroll.setAlignment(Qt.AlignLeft)
        self.setStyleSheet("""          
                            QWidget {
                                background:white;
                            }
                            QScrollBar:vertical {             
                                border: 1px solid white;
                                background:white;
                                width:8px;    
                                margin: 0px 0px 0px 0px;
								
                            }
                            QScrollBar::handle:vertical {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop: 0 rgb(192,192,192), stop: 0.5 rgb(192,192,192), stop:1 rgb(192,192,192));
                                min-height: 0px;
								border-radius: 5px;
                            }
                            QScrollBar::add-line:vertical {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(192,192,192),  stop:1 rgb(32, 47, 130));
                                height: 0px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::sub-line:vertical {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(192,192,192),  stop:1 rgb(32, 47, 130));
                                height: 0 px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }""")
        
        # Initializing widget to be set in QScrollArea
        self.widget = QWidget(self.scroll)
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        # Width needs to be smaller than QScrollArea to remove horizontal scroll bar
        self.widget.setMinimumWidth(self.scroll.frameGeometry().width()-20)
        # Initializing layout to hold questions

        self.layout = QVBoxLayout(self.widget)
        self.layout.setContentsMargins(10,10,30,10)
        self.layout.setSpacing(20)
        # Setting up the layout and widget
        self.widget.setLayout(self.layout)
        self.scroll.setWidget(self.widget)

        # Setting main widget
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.scroll)
        self.setLayout(self.mainLayout)

    def clearLayout(self):
        """
        Clears the questions from the widget
        """

        # Removing items has to be done in reversed order
        # as index of items shift if removing head first
        for layoutItem in [self.layout.itemAt(i) for i in reversed(range(self.layout.count()))]:
            self.layout.removeItem(layoutItem)
            if layoutItem.widget() != None:
                layoutItem.widget().setParent(None)

    def loadQuestions(self):
        """
        Loads the Questions stored into the widget to be displayed
        """

        self.clearLayout()

        # Initializing the questionWidgets
        self.questionWidgets = [BaseRecipeWidget(self.widget, question) for question in self.questions]
        for questionWidget in self.questionWidgets:
            self.layout.addWidget(questionWidget)

        # Updating size of widget
        self.update()

    def update(self):
        """
        Updates the widget shape if the questions in the layout change shape
        """
        
        # Checking all layout items
        for layoutItem in [self.layout.itemAt(i) for i in range(self.layout.count())]:
            if (layoutItem.widget() == None):
                self.layout.removeItem(layoutItem)
            else:
                if layoutItem.widget().isVisible():
                    if issubclass(type(layoutItem.widget()), BaseQuestionWidget):
                        layoutItem.widget().updateGeometry()

        self.updateGeometry()

    def getQuestions(self):
        return [self.layout.itemAt(i).widget().question for i in range(self.layout.count()) if issubclass(type(self.layout.itemAt(i).widget()), BaseQuestionWidget)]

    def updateQuestions(self, questions=None):
        """
        Updates the widget with new Questions
        Args:
            questions: list of new Questions
        """
        if questions != None:
            self.questions = questions
        self.clearLayout()
        self.loadQuestions()


if __name__ == "__main__":
    app = QApplication([])
    recipes = [
        Recipe("My Recipe", ["ingredient1", "ingredient2"], "Mix everything together"),
        Recipe("My Other Recipe", ["ingredient3", "ingredient4"], "Separate everything")
    ]

    window = RecipeBank(None, recipes)
    window.loadQuestions()
    window.show()

    app.exec_()
