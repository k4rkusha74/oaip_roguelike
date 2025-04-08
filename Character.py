from Storage import Inventory, Arming

class Character():
    def __init__(self, name, max_health, strong, armor, x, y):
        self.name = name
        self.health = max_health
        self.strong = strong
        self.armor = armor
        self.current_health = max_health
        self.hand = Arming(2, 1)
        self.x = x
        self.y = y

    def attack(self, target):
        damage = max(self.hand.items[0].damage, self.hand.items[1].damage)
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
        self.inventory = Inventory(5, 4)