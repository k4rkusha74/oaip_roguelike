from Character import Player, Enemy
from Item import Item, Weapon # name, rarity, place, x, y, || damage, size,
from Buttons import Buttons
from Storage import Chest

main_character = Player('Player', 15, 3, 0.2, 0, 0)
main_goblin = Enemy('Enemy', 5, 2, 0.1, 0, 0)
first_chest = Chest(4, 5)

Wood_Sword = Weapon('Деревянный Меч', 'unrare', main_character.hand, None, None, 3, 1,)
Stone_Sword = Weapon('Каменный меч', 'rare', first_chest, None, None, 6, 1,)
Gold_Sword = Weapon('Золотой меч', 'epic', first_chest, None, None, 10, 1,)
Poison = Item('Зелье', 'unrare', first_chest, None, None)

button_pickup_weapon = Buttons(0, 0)
button_pickup_weapon.pick_up_weapon(Wood_Sword, main_character)

print('player hp -', main_character.current_health)
print('goblin hp -', main_goblin.current_health)

main_character.attack(main_goblin)

print('player hp -', main_character.current_health)
print('goblin hp -', main_goblin.current_health)

first_chest.add(Stone_Sword)
first_chest.add(Poison)

print(first_chest.get_items())
print(main_character.inventory.get_items())

# first_chest.take(main_character, Stone_Sword)
# first_chest.take(main_character, Poison)
# =>
Stone_Sword.pick_up(main_character)
Poison.pick_up(main_character)

print(first_chest.get_items())
print(main_character.inventory.get_items())

# print(main_character.first_hand)
# print(main_character.second_hand)
# =>
print(main_character.hand)