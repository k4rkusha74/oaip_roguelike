from Item import WeaponNothing, ArmorNothing

class Storage():
    def __init__(self, amount):
        self.amount = amount
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
    
    def get_free_amount(self):
        return self.free_amount

class Chest(Storage):
    def __init__(self, amount, x ,y):
        super().__init__(amount)
        self.x = x
        self.y = y

class Inventory(Storage):
    def __init__(self, amount):
        super().__init__(amount)

class Arming(Storage):
    def __init__(self, amount):
        super().__init__(amount)
        self.items = [
            WeaponNothing(),
            WeaponNothing()
        ]

    def delete(self, item):
        self.items[item] = WeaponNothing()

class ArmorStorage(Storage):
    def __init__(self, amount):
        super().__init__(amount)
        self.items = [
            ArmorNothing(),
            ArmorNothing(),
            ArmorNothing()
        ]

    def delete(self, item):
        self.items[item] = ArmorNothing()

        
        



    