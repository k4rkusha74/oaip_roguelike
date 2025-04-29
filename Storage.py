<<<<<<< Updated upstream
from Item import Weapon, fist
=======
from Item import WeaponNothing, ArmorNothing, GenerateItems
>>>>>>> Stashed changes

class Storage():
    def __init__(self, x_amount, y_amount):
        self.x_amount = x_amount
        self.y_amount = y_amount
        self.amount = self.x_amount * self.y_amount
        self.items = [] * self.amount
        self.free_amount = self.amount - len(self.items)
        
    
    def __str__(self):
        return str(self.items)

    def add(self, item):
        self.items.append(item)
            
    def delete(self, item):
        self.items.remove(item)

    def get_items(self):
        return self.items


class Chest(Storage):
    def __init__(self, x_amount, y_amount):
        super().__init__(x_amount, y_amount)
<<<<<<< Updated upstream
=======
        self.x = x
        self.y = y
        self.generate_and_add_items()

    def generate_and_add_items(self):
        items = GenerateItems()  # Получаем список предметов
        for item in items:
            self.add(item)
>>>>>>> Stashed changes

class Inventory(Storage):
    def __init__(self, x_amount, y_amount):
        super().__init__(x_amount, y_amount)

class Arming(Storage):
    def __init__(self, x_amount, y_amount):
        super().__init__(x_amount, y_amount)
        self.items = [
            fist(),
            fist()
        ]


        
        



    