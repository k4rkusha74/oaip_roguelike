from Item import WeaponNothing, ArmorNothing, GenerateItems
import draw_map

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
         # При создании сундука сразу генерируем предметы и добавляем их
        #self.generate_and_add_items()
    
    def generate_and_add_items(self):
        items = GenerateItems()  
        for item in items:
            self.add(item)

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

def open_storges(stdscr, list_section, open_chest):      
        stdscr.clear()
        start_section = list(filter(lambda x: x.ID == 1, list_section))
        end_section = list(filter(lambda x: x.ID == 6, list_section))
        start_x = start_section[0].start_point_x
        start_y = start_section[0].start_point_y
        end_x = end_section[0].end_point_x
        end_y = end_section[0].end_point_y

        draw_map.draw_rectangle(stdscr, start_x, start_y, end_x, end_y)

        key = stdscr.getch()
        key = chr(key)

        if key == 'ч' or key == 'x':
            stdscr.clear()
            return 0
        



    