from model.order import Order
from model.pizza import Pizzas
from model.category import Categories

class Database:
    """ A database simulation """

    def __init__(self):
        self.pizzas = Pizzas()
        self.order = Order()
        self.categories = Categories()