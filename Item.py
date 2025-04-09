class Item():
    def __init__(self, name, rarity, place, x, y):
        self.name = name # название оружия
        self.rarity = rarity # редкость 
        self.place = place # владелец (игрок, сундук, моб, пол(place = None, существуют x, y))
        self.x = x # положение по x y соответственно
        self.y = y

    def pick_up(self, character): # положить в инвертарь
        self.place = character.inventory
        self.x = None
        self.y = None
        character.inventory.add(self)

    def put(self, storage): # переложить в хранилище
        self.place.delete(self)
        self.place = storage
        storage.add(self)

    def drop(self, character): # выкинуть на пол
        self.place = None
        character.inventory.remove(self)
        self.x = character.x
        self.y = character.y
    
    def replace(self, item): # self - предмет у игрока, item - предмет на замену || заменить один на другой
        self.place, item.place = item.palce, self.place
        item.place.remove(self)
        self.place.remove(item)
        self.place.add(self)
        item.place.add(item)


class Weapon(Item): # оружия

    def __init__(self, name, rarity, place, x, y, damage, size,):
        super().__init__(name, rarity, place, x, y)
        self.damage = damage
        self.size = size # занимаемое количество рук (одноручное/двуручное)
    
    def equip(self, character): # экипировать / положить в руку
        if self.place != None:
            self.place.delete(self)
            self.x = None
            self.y = None
        self.place = character.hand
        character.hand.add(self)
    
    def unequip(self, character): # разэкипировать, положить в инвентарь
        if character.inventory.free_amount > 0:
            self.place.items = [
            fist(),
            fist()
        ]
            character.inventory.add(self)
        
def fist():
    return Weapon('Кулак', None, None, None, None, 2, None)

class UseItem(Item): # расходники
    def __init__(self, name, rarity, place, x, y, effect, counter):
        super().__init__(name, rarity, place, x, y)
        self.effect = effect
        self.counter = counter

    def pick_up(self, character): # подобрать в инвентарь
        if self in character.inventory:
            character.inventory.self.plus_count()
        else:
            self.place = character.inventory
            self.x = None
            self.y = None
            character.inventory.add(self)

    def drop(self, character): # выкинуть на пол
        self.minus_count()
        self.place = None
        character.inventory.remove(self)
        self.x = character.x
        self.y = character.y

    def put(self, storage): # переложить в хранилище
        self.minus_count()
        self.pick_up(storage)

    # может не работать -> -> ->
    def use(self): # использовать расходник
        self.effect
        self.minus_count()

    def plus_count(self): # добавить в стак + 1
        self.counter += 1

    def minus_count(self): # убрать из стака - 1
        self.counter -= 1
        if self.counter == 0:
            self.kill_item()

    def kill_item(self): # удалить item
        self.place.delete(self)
         