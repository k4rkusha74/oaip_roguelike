from Weapons import Weapons

class Chest():
    def __init__(self, x_amount, y_amount):
        self.x_amount = x_amount
        self.y_amount = y_amount
        self.amount = self.x_amount * self.y_amount
        self.free_amount = x_amount * y_amount
        self.items = [] * self.amount

    def add(self, item):
        self.items.append(item)

    def put(self, character, item):
        if self.free_amount != 0:
            if item in character.invertory:
                character.invertory.remove_item
                self.items.append(item)
            elif item == character.first_hand:
                character.first_hand == Weapons('Кулак', self.strong, None, None, None, None, None)
                self.items.append(item)
            elif item == character.character.second_hand:
                character.second_hand == Weapons('Кулак', self.strong, None, None, None, None, None)
                self.items.append(item)
        else:
            return 'Отсутствуют свободные ячейки'

    def take(self, character, item):
        print(type(item))
        if type(item) == Weapons:
            self.items.remove(item)
            item.pick_up(character)
        else:
            if len(character.inventory.get_items()) < character.inventory.max_size:
                self.items.remove(item)
                character.inventory.add_item(item)
            else:
                return 'Отсутствуют свобоные ячейки'

    def get_items(self):
        return self.items