from recipeData import Recipe, RecipeFlags, guac

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from UI.RecipeWidgetClaire import Ui_Recipe as RecipeWidgetUI

class RecipeView(QWidget, RecipeWidgetUI):
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
        
        
        



if __name__ == "__main__":
    app = QApplication([])
    window = RecipeView(None, guac)
    window.show()
    app.exec()
