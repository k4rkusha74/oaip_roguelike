from Weapons import Weapons

class Character():
    def __init__(self, name, max_health, strong, armor, x, y):
        self.name = name
        self.health = max_health
        self.strong = strong
        self.armor = armor
        self.current_health = max_health
        self.x = x
        self.y = y

    def attack(self, target):
        damage = max(self.first_hand.damage, self.second_hand.damage)
        if float(f'{((self.strong + damage) * (1 - target.armor)):.2f}') > target.current_health:
            target.current_health = 0
        else:
            target.current_health -= float(f'{((self.strong + damage) * (1 - target.armor)):.2f}')
            
        if target.current_health < 0:
            target.current_heath = 0
    
    def get_current_state(self):
        state = (f"Имя: {self.name}\n"
        f"Здоровье: {self.current_health}/{self.health}\n"
        f"Броня: {self.armor}%\n"
        f"Атака: {self.strong}")
        return state


class Enemy(Character):
    def __init__(self, name, max_health, strong, armor, x, y):
        super().__init__(name, max_health, strong, armor, x, y)


class Player(Character):
    def __init__(self, name, max_health, strong, armor, x, y):
        super().__init__(name, max_health, strong, armor, x, y)
        self.inventory = Inventory(32)
        self.first_hand = Weapons('Кулак', self.strong, None, None, None, None, None)
        self.second_hand = Weapons('Кулак', self.strong, None, None, None, None, None)
        self.current_hand = sum([1 if self.first_hand.name != 'Кулак' else 0,
                                 1 if self.second_hand.name != 'Кулак' else 0])
        

class Inventory():
    def __init__(self, size):
        self.items = []
        self.max_size = size
    
    def __str__(self):
        return str(self.items)

    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        self.items.remove(item)

    def get_items(self):
        return self.items
    
    