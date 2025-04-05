class Weapons(): # __main__.Weapon

    def __init__(self, name, damage, size, rarity, place, x, y):
        self.name = name # название оружия
        self.damage = damage # урон
        self.size = size # занимаемое количество рук (одноручное/двуручное)
        self.rarity = rarity # редкость
        self.place = place # пололжение (в руке, на полу, сундуке?, магазине?, etc)
        self.x = x # положение х и у для подбора с пола
        self.y = y 
        self.hand = None # положение в руке: 1 - в первой руке, 2 - во второй, 0 - двуручное оружие
    
    def pick_up(self, character): # реальзовать невозможность брать одинаковые оружия
        if self.size == 2:
            if character.current_hand == 0:
                character.first_hand = self.name
                character.second_hand = self.name
            else:
                return 'Слоты под оружие заняты'
        else:
            if character.current_hand == 2:
                return 'Слоты под оружие заняты'
            elif character.first_hand.name != 'Кулак':
                character.first_hand = self.name
            else:
                character.second_weapon = self.name
        
        self.place = 'hand'
        self.x = None
        self.y = None
        return f'Экипировано оружие - {self.name}'
    
    def drop(self, character):
        match self.hand:
            case 1:
                character.first_hand = Weapons('Кулак', self.strong, None, None, None, None, None)

            case 2:
                character.second_hand = Weapons('Кулак', self.strong, None, None, None, None, None)

            case 0:
                character.first_hand = Weapons('Кулак', self.strong, None, None, None, None, None)
                character.second_hand = Weapons('Кулак', self.strong, None, None, None, None, None)
            
            case _:
                return 'Проверить параметр "hand" при использовании "drop"'
        
        self.place = 'floor'
        self.x = character.x
        self.y = character.y
        return f'Сброшено оружие - {self.name}'
        
    def replace(self, character): # self - оружие на замену, character - игрок ||| пока пока робит не как задуманно
        character.first_hand.drop(character)
        self.pick_up(character)
