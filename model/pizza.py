import json

class Pizza():
    """ tracks a pizza """

    def __init__(self, pizza_id, category_id, name, description, price):
        ''' Constructor '''
        self.pizza_id = pizza_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.price = price

class Pizzas():
    """ maintains a list of Pizza objects """
    def __init__(self):
        self.max_id = 0
        self.pizzas = []
        self.load()

    def load(self):
        pizzas = []
        try:
            with open("data/pizzas.json", "rt") as pizzas_file:
                pizzas_json_string = pizzas_file.read()
                pizzas_wrapped = json.loads(pizzas_json_string)
                pizzas = pizzas_wrapped["pizzas"]
        except:
            print("reading from pizzas.json failed")
        
        for pizza in pizzas:
            pizza_obj = Pizza(pizza["pizza_id"], pizza["category_id"], pizza["name"], pizza["description"], pizza["price"])
            if pizza["pizza_id"] > self.max_id:
                self.max_id = pizza["pizza_id"]
            self.pizzas.append(pizza_obj)  

    
    def get_pizza(self, pizza_id):
        for pizza in self.pizzas:
            if pizza.pizza_id == pizza_id:
                return pizza
          
        return None


    def get_pizzas(self, category_id=None):
        if not category_id:
            return self.pizzas
           
        pizzas = []
        for pizza in self.pizzas:
            if pizza.category_id == category_id:
                pizzas.append(pizza)
          
        return pizzas
    
    
    def add_pizza(self, category_id, name, description, price):
        self.max_id = self.max_id + 1
        pizza = Pizza(self.max_id, category_id, name, description, price)
        self.pizzas.append(pizza)
        self.save()
    
    
    def delete_pizza(self, pizza_id):
        print("Delete pizza with id {}".format(pizza_id))
        pizza_to_delete = None
        for pizza in self.pizzas:
            if pizza.pizza_id == pizza_id:
                pizza_to_delete = pizza
        
        if pizza_to_delete:
            self.pizzas.remove(pizza_to_delete)
            self.save()
        
        
    def save(self):
        pizzas = []
        for pizza in self.pizzas:
            pizza_dict = {"pizza_id": pizza.pizza_id, "category_id": pizza.category_id, "name": pizza.name, "description": pizza.description, "price": pizza.price }
            pizzas.append(pizza_dict)
            
        try:
            with open("data/pizzas.json", "wt") as pizzas_file:
                pizzas_file.write(json.dumps({"pizzas": pizzas}))
        except:
            print("writing to file pizzas.json failed")
            return False
        
        return True 