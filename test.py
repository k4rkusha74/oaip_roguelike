from Character import Player, Enemy
from Item import Item, Weapon # name, rarity, place, x, y, || damage, size
from Storage import Chest

main_character = Player('Player', 15, 3, 0.2, 0, 0)
main_goblin = Enemy('Enemy', 5, 2, 0.1, 0, 0)
first_chest = Chest(4, 5)

Wood_Sword = Weapon('Деревянный Меч', 'unrare', None, None, None, 3, 1,)
Stone_Sword = Weapon('Каменный меч', 'rare', first_chest, None, None, 6, 1,)
Gold_Sword = Weapon('Золотой меч', 'epic', first_chest, None, None, 10, 1,)
Poison = Item('Зелье', 'unrare', first_chest, None, None)

first_chest.add(Stone_Sword)
first_chest.add(Gold_Sword)

Stone_Sword.pick_up(main_character)

Gold_Sword.equip(main_character)

print(f'''Здоровье гоблина - {main_goblin.current_health}
Здоровье персонажа - {main_character.current_health}
''')

main_character.attack(main_goblin)

print(f'''Здоровье гоблина - {main_goblin.current_health}
Здоровье персонажа - {main_character.current_health}
''')

for item in main_character.hand.get_items():
    print(item.name)