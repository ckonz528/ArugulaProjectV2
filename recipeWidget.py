from recipeData import Recipe, RecipeFlags, guac
from quantities import Quantity

from typing import Tuple

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from UI.RecipeWidgetClaire import Ui_Recipe as RecipeViewUI
from UI.RecipeWidgetEditable import Ui_Recipe as RecipeEditUI
from UI.AddIngredientWidget import Ui_AddIngredientWidget as IngredientEditUI

class RecipeView(QWidget, RecipeViewUI):
    def __init__(self, parent: QWidget, recipe: Recipe):
        super(RecipeView, self).__init__(parent)
        self.setupUi(self)
        self.setRecipe(recipe)

    def setRecipe(self, recipe: Recipe):
        # store the recipe
        self.recipe = recipe
        # write data to widgets
        self.lblRecipeTitle.setText(recipe.title)
        self.lblCookTime.setText(str(recipe.cook))
        self.lblPrepTime.setText(str(recipe.prep))
        self.lblServings.setText(str(recipe.servings))
        self.txtDirections.setText(recipe.directions)
        # write ingredients list
        for ingredient, amount in recipe.ingredients.items():
            string = f'{ingredient}\t({str(amount)})'
            self.lstIngredients.addItem(string)
        # populate checkboxes
        self.chkDF.setChecked(bool(recipe.flags & RecipeFlags.DAIRYFREE))
        self.chkGF.setChecked(bool(recipe.flags & RecipeFlags.GLUTENFREE))
        self.chkVeg.setChecked(bool(recipe.flags & RecipeFlags.VEGETARIAN))
        self.chkVegan.setChecked(bool(recipe.flags & RecipeFlags.VEGAN))
        self.chkNoAlcohol.setChecked(bool(recipe.flags & RecipeFlags.NONALCOHOLIC))
        self.chkHealthy.setChecked(bool(recipe.flags & RecipeFlags.HEALTHY))
        

class IngredientEditor(QWidget, IngredientEditUI):
    def __init__(self, parent: QWidget, ingredient:Tuple[str, Quantity]=None):
        super(IngredientEditor, self).__init__(parent)
        self.setupUi(self)
        if ingredient is not None:
            self.setIngredient(ingredient)

    def setIngredient(self, ingredient: Tuple[str, Quantity]):
        name, quantity = ingredient
        amount, *unit = str(quantity).split()

        self.lineIngredientName.setText(name)
        self.dspnAmount.setValue(float(amount))
        if unit == []:
            self.comboUnits.setCurrentIndex(1)
        else:

            index = self.comboUnits.findText(unit[0])
            self.comboUnits.setCurrentIndex(index)

class RecipeEdit(QWidget, RecipeEditUI):
    def __init__(self, parent: QWidget, recipe: Recipe):
        super(RecipeEdit, self).__init__(parent)
        self.setupUi(self)
        # self.connectAll()
        self.setRecipe(recipe)

    def setRecipe(self, recipe: Recipe):
        # store the recipe
        self.recipe = recipe
        # write data to widgets
        self.lineRecipeName.setText(recipe.title)
        self.spnCookTime.setValue(recipe.cook)
        self.spnPrepTime.setValue(recipe.prep)
        self.spnServings.setValue(recipe.servings)
        self.txtEDirections.setText(recipe.directions)
        # write ingredients list
        self.vbox = QVBoxLayout()

        for ingredient, amount in recipe.ingredients.items():
            editor = IngredientEditor(self.scrollAreaWidgetContents, (ingredient, amount))
            self.vbox.addWidget(editor)

            # string = f'{ingredient}\t({str(amount)})'
            # self.lstIngredients.addItem(string)
        self.scrollAreaWidgetContents.setLayout(self.vbox)

        # populate checkboxes
        self.chkDF.setChecked(bool(recipe.flags & RecipeFlags.DAIRYFREE))
        self.chkGF.setChecked(bool(recipe.flags & RecipeFlags.GLUTENFREE))
        self.chkVeg.setChecked(bool(recipe.flags & RecipeFlags.VEGETARIAN))
        self.chkVegan.setChecked(bool(recipe.flags & RecipeFlags.VEGAN))
        self.chkNoAlcohol.setChecked(bool(recipe.flags & RecipeFlags.NONALCOHOLIC))
        self.chkHealthy.setChecked(bool(recipe.flags & RecipeFlags.HEALTHY))

    def getRecipe(self) -> Recipe:
        title = self.lineRecipeName.displayText()
        servings = self.spnServings.value()
        prep = self.spnPrepTime.value()
        cook = self.spnCookTime.value()
        directions = self.txtEDirections.toPlainText()
        ingredients = {}
        for i in range(self.vbox.count()):
            ingredient : IngredientEditor = self.vbox.itemAt(i)
            units = ingredient.comboUnits.currentText()
            amount = ingredient.dspnAmount.value()
            if units == 'count':
                quantity = Quantity.count(amount)
            else:
                quantity = Quantity.of(amount, units)

            name = ingredient.lineIngredientName.displayText()
            ingredients[name] = quantity
        flags = 0
        if self.chkDF.isChecked(): flags |= RecipeFlags.DAIRYFREE
        if self.chkGF.isChecked(): flags |= RecipeFlags.GLUTENFREE
        if self.chkHealthy.isChecked(): flags |= RecipeFlags.HEALTHY
        if self.chkNoAlcohol.isChecked(): flags |= RecipeFlags.NONALCOHOLIC
        if self.chkVeg.isChecked(): flags |= RecipeFlags.VEGETARIAN
        if self.chkVegan.isChecked(): flags |= RecipeFlags.VEGAN

        return Recipe(
            title=title,
            servings=servings,
            prep=prep,
            cook=cook,
            ingredients=ingredients,
            directions=directions,
            flags=flags
        )




class RecipeWidget(QStackedWidget):
    def __init__(self, parent: QWidget, recipe: Recipe):
        super(RecipeWidget, self).__init__(parent)
        self.viewer = RecipeView(parent, recipe)
        self.editor = RecipeEdit(parent, recipe)

        self.addWidget(self.viewer)
        self.addWidget(self.editor)
        self.setCurrentWidget(self.viewer)

        self.connectAll()

    def connectAll(self):
        self.viewer.btnOk.clicked.connect(self.close)
        self.viewer.btnEditRecipe.clicked.connect(self.switchToEditor)
        self.editor.btnCancel.clicked.connect(lambda: self.switchToViewer(False))
        self.editor.btnSave.clicked.connect(lambda: self.switchToViewer(True))

    def switchToEditor(self):
        self.editor.setRecipe(self.viewer.recipe)
        self.setCurrentWidget(self.editor)

    def switchToViewer(self, save: bool):
        # if save:
            # self.viewer.setRecipe(self.editor.getRecipe())
        self.setCurrentWidget(self.viewer)




if __name__ == "__main__":
    app = QApplication([])
    window = RecipeWidget(None, guac)
    window.show()
    app.exec()
