import json

class Category():
    """ tracks a category """

    def __init__(self, category_id, category_name):
        ''' Constructor '''
        self.category_id = category_id
        self.category_name = category_name

class Categories():
    """ maintains a list of Category objects """
    def __init__(self):
        self.load()


    def load(self):
        self.categories = []
        categories = []
        try:
            with open("app/data/categories.json", "rt") as categories_file:
                categories_json_string = categories_file.read()
                categories_wrapped = json.loads(categories_json_string)
                categories = categories_wrapped["categories"]
        except:
            print("reading from categories.json failed")
        
        for category in categories:
            category_obj = Category(category["category_id"], category["category_name"])
            self.categories.append(category_obj)
    
    
    def get_categories(self):
        return self.categories
    
    
    def get_category(self, category_id):
        for category in self.categories:
            if category.category_id == category_id:
                return category
            
        return None