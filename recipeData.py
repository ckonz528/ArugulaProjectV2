from enum import Flag, auto
from typing import NamedTuple, Dict
from quantities import Quantity

class RecipeFlags(Flag):
    NONE = 0
    GLUTENFREE = auto()
    DAIRYFREE = auto()
    VEGETARIAN = auto()
    VEGAN = auto()
    NONALCOHOLIC = auto()
    HEALTHY = auto()

class Recipe(NamedTuple):
    title: str
    servings: str
    prep: int
    cook: int
    ingredients: Dict[str, Quantity]
    directions: str
    flags: RecipeFlags

guac = Recipe(
    title='Guacamole',
    ingredients={
        'avocado': Quantity.count(4),
        'roma tomato': Quantity.count(2),
        'onion': Quantity.count(0.5),
        'lime': Quantity.count(2),
        'jalapeño': Quantity.count(1),
        'cilantro': Quantity.count(0.5),
        'salt': Quantity.of(2, 'tsp')
    },
    directions='Combine ingredients in a bowl. Chill before serving.',
    servings=8,
    prep=20,
    cook=0,
    flags=RecipeFlags.GLUTENFREE | RecipeFlags.DAIRYFREE | RecipeFlags.VEGAN | RecipeFlags.NONALCOHOLIC | RecipeFlags.VEGETARIAN
)