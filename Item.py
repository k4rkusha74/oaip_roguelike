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
        if storage.get_free_items() > 0:
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

    def __init__(self, name, rarity, place, x, y, damage, size):
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
        self.put(character.inventory)
        
def WeaponNothing():
    return Weapon('Кулак', None, None, None, None, 2, None)

class Armor(Item): # броня
    def __init__(self, name, rarity, place, x, y, position, block):
        super().__init__(name, rarity, place, x, y)
        self.position = position
        self.block = block

    def get_block(self):
        return self.block

    def equip(self, character): # начало экипировки брони
        match self.position:
            case 'head':
                self.__post_equip(character, 0)
            case 'body':
                self.__post_equip(character, 1)
            case 'leg':
                self.__post_equip(character, 2)
            case _:
                pass

    def __post_equip(self, character, pos): # продолжение экипировки брони
        if character.armor.items[pos] == ArmorNothing():
            if self.place != None:
                self.place.delete(self)
            self.x = None
            self.y = None
            self.place = character.armor
            character.armor.add(self)

    def unequip(self, character):
        self.put(character.inventory)


def ArmorNothing():
    return Armor('Одежда', None, None, None, None, None, 0)

class UseItem(Item): # расходники
    def __init__(self, name, rarity, place, x, y, effect):
        super().__init__(name, rarity, place, x, y)
        self.effect = effect
        self.counter = 1

    def pick_up(self, character): # подобрать в инвентарь
        if self in character.inventory.get_items():
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
    def use(self, character=None): # использовать расходник
        self.effect(character)
        self.minus_count()

    def plus_count(self): # добавить в стак + 1
        self.counter += 1

    def minus_count(self): # убрать из стака - 1
        self.counter -= 1
        if self.counter == 0:
            self.kill_item()

    def kill_item(self): # удалить item
        self.place.delete(self)
         