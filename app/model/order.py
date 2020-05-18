import json
from flask import Flask, flash

class OrderItem():
    """ tracks the items of an order """

    def __init__(self, pizza_id, category_id, name, description, price, size, crust, quantity):
        ''' Constructor '''
        self.pizza_id = pizza_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.price = price
        self.size = size
        self.crust = crust
        self.quantity = quantity
    
class Order():
    """ maintains a list of Order objects """
    def __init__(self):
        self.load()

    def load(self):
        self.order = []
        order = []
        try:
            with open("app/data/order.json", "rt") as order_file:
                order_json_string = order_file.read()
                order_wrapped = json.loads(order_json_string)
                order = order_wrapped["order"]
        except:
            print("reading from order.json failed")

        for item in order:
            item_obj = OrderItem(item["pizza_id"], item["category_id"], item["name"], item["description"], item["price"], item["size"], item["crust"], item["quantity"])
            self.order.append(item_obj)
    
    def get_items(self):
        return self.order

    def get_item(self, pizza_id):
        for item in self.order:
            if item.pizza_id == pizza_id:
                return item
        return None

    def add_item(self, pizza_id, category_id, name, description, price, size, crust, quantity):
        item = self.get_item(pizza_id)
        if item:
            item.quantity += quantity
        else:
            item = OrderItem(pizza_id, category_id, name, description, price, size, crust, quantity)
            self.order.append(item)
        self.save()
    
    
    def update_item(self, pizza_id, quantity):
        pizza = self.get_item(pizza_id)
        
        if pizza:
            if quantity <= 0:
                self.order.remove(pizza)
            else:
                pizza.quantity = quantity
        else:
            flash("Pizza not found")
            
        self.save() 

    
    def place_order(self):
        ''' Right now, this just deletes all items from the order '''
        self.order = []
        
        self.save()

    
    def save(self):
        order = []
        for item in self.order:
            item_dict = {"pizza_id": item.pizza_id, "category_id": item.category_id, "name": item.name, "description": item.description, "price": item.price, "size": item.size, "crust": item.crust, "quantity": item.quantity }
            order.append(item_dict)
            
        try:
            with open("app/data/order.json", "wt") as order_file:
                order_file.write(json.dumps({"order": order}, indent=4))
        except:
            print("writing to file order.json failed")
            return False
        
        return True