from Character import Character, Player, Enemy
class Weapons():

    def __init__(self, damage, rarity, hand, name, place, x, y):
        self.damage = damage # урон
        self.rarity = rarity # редкость
        self.hand = hand # занимаемое количество рук (одноручное/двуручное)
        self.name = name # название оружия
        self.place = place # пололжение (в руке, сундуке?, магазине?, на полу, etc)
        self.x = x # положение х и у для подбора с пола
        self.y = y 
    
    def pick_up(self, character):
        if self.hand == 2:
            if character.current_hand == 0:
                character.first_hand = self.name
                character.second_hand = self.name
            else:
                return 'Слоты под оружие заняты'
        else:
            if character.current_hand == 2:
                return 'Слоты под оружие заняты'
            elif character.first_hand != None:
                character.first_hand = self.name
            else:
                character.second_weapon = self.name
        
        self.place = 'hand'
        self.x = character.x
        self.y = character.y
        return f'Экипировано оружие - {self.name}'
    
    def drop(self, character, hand):
        match hand:
            case 'first':
                character.first_hand = None

            case 'second':
                character.second_hand = None

            case 'all':
                character.first_hand = None
                character.second_hand = None
            
            case _:
                return 'Проверить параметр "hand" при использовании "drop"'
        
        self.place = 'floor'
        self.x = character.x
        self.y = character.y
        return f'Сброшено оружие - {self.name}'
        

        