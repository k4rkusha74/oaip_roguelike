from Storage import Chest, Inventory, Arming, ArmorStorage 
from Item import *
import random

class Character():
    def __init__(self, name, letter, max_health, strong, x, y):
        self.name = name # имя
        self.letter = letter # знак на экране 
        self.health = max_health # макс хп
        self.strong = strong # сила удара без оружия
        self.armor = ArmorStorage(3) # броня
        self.current_health = max_health # текущее хп
        self.hand = Arming(2) # вооружение (оружия в руках)
        self.x = x # х и у координаты соответственно
        self.y = y

    def move(self, side):
        match side:
            case 'right':
                self.x += 1
            case 'up':
                self.y += 1
            case 'left':
                self.x -= 1
            case 'down':
                self.y -= 1

    def attack(self, target):
        damage = max(self.hand.items[0].damage, self.hand.items[1].damage)
        target.take_damage(damage, True)
    
    def take_damage(self, damage, flag=False):
        self.current_health -= damage * (1 - (self.get_armor() if flag else 0))
        if self.current_health <= 0:
            self.current_health = 0

        if self.current_health == 0:
            self.death()

    def death(self):
        pass

    def get_current_state(self):
        state = (f"Имя: {self.name}\n"
        f"Здоровье: {self.current_health}/{self.health}\n"
        f"Броня: {self.armor}%\n"
        f"Атака: {self.strong}")
        return state

    def get_armor(self):
        full_block = 0
        for arm in self.armor.get_items():
            try:
                full_block += arm.get_block()
            except:
                continue
        return full_block

class Enemy(Character):
    def __init__(self, name, letter, max_health, strong, x, y):
        super().__init__(name, letter, max_health, strong, x, y)

    def death(self):
        pass

class Player(Character):
    def __init__(self, name, letter, max_health, strong, x, y):
        super().__init__(name, letter, max_health, strong, x, y)
        self.inventory = Inventory(20)#########

    def death(self):
        pass

class Transition:
    def __init__(self, letter, x, y):
        self.letter = letter
        self.x = x
        self.y = y

def create_player(start_room):
    x_start_player = start_room.start_point_x + start_room.width // 2
    y_start_player = start_room.start_point_y + start_room.height // 2
    player = Player("Бедолага", "•", 100, 0, x_start_player, y_start_player)

    return player  