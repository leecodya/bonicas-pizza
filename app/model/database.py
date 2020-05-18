from app.model.order import Order
from app.model.pizza import Pizzas
from app.model.category import Categories

class Database:
    """ A database simulation """

    def __init__(self):
        self.pizzas = Pizzas()
        self.order = Order()
        self.categories = Categories()