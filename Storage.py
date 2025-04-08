from Item import Weapon, fist

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
        self.remove(item)

    def get_items(self):
        return self.items


class Chest(Storage):
    def __init__(self, x_amount, y_amount):
        super().__init__(x_amount, y_amount)

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


        
        



    