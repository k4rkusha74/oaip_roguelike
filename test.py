from Character import Player, Enemy
from Weapons import Weapons
from Buttons import Buttons
from Chest import Chest

main_character = Player('Player', 15, 3, 0.2, 0, 0)
main_goblin = Enemy('Enemy', 5, 2, 0.1, 0, 0)

Wood_Sword = Weapons('Деревянный Меч', 3, 1, 'unrare', 'hand', None, None)
Stone_Sword = Weapons('Каменный Меч', 6, 1, 'rare', 'chest', None, None)
Gold_Sword = Weapons('Золотой Меч', 10, 1, 'epic', 'chest', None, None)
Poison = 'Зелье'

button_pickup_weapon = Buttons(0, 0)
button_pickup_weapon.pick_up_weapon(Wood_Sword, main_character)

print('player hp -', main_character.current_health)
print('goblin hp -', main_goblin.current_health)

main_character.attack(main_goblin)

print('player hp -', main_character.current_health)
print('goblin hp -', main_goblin.current_health)

first_chest = Chest(4, 5)
first_chest.add(Stone_Sword)
first_chest.add(Poison)

print(first_chest.get_items())
print(main_character.inventory.get_items())

first_chest.take(main_character, Stone_Sword)
first_chest.take(main_character, Poison)

print(first_chest.get_items())
print(main_character.inventory.get_items())
print(main_character.first_hand)
print(main_character.second_hand)
