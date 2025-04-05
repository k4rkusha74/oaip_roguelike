from Character import Character, Player, Enemy
from Weapons import Weapons
from Buttons import Buttons

main_character = Player('Player', 15, 3, 0.2, 0, 0)
main_goblin = Enemy('Enemy', 5, 2, 0.1, 0, 0)

Wood_Sword = Weapons(2, 'unrare', 1, 'Wood_Sword', 'hand', 0, 0)

button_pickup_weapon = Buttons(0, 0)
button_pickup_weapon.pick_up_weapon(Wood_Sword, main_character)

print('player hp -', main_character.current_health)
print('goblin hp -', main_goblin.current_health)

main_character.attack(main_goblin)

print('player hp -', main_character.current_health)
print('goblin hp -', main_goblin.current_health)