from Storage import Chest, Inventory, Arming, ArmorStorage 
from Item import *
import curses

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

def create_player(start_room, player, flag_on_open_chest):
    
    x_start_player = start_room.start_point_x + start_room.width // 2
    y_start_player = start_room.start_point_y + start_room.height // 2
    if player == None:
        player = Player("Бедолага", "☻", 100, 0, x_start_player, y_start_player)
    else:
        if flag_on_open_chest:
            flag_on_open_chest = False
            return player, flag_on_open_chest
        else:
            player.x = x_start_player
            player.y = y_start_player

    return player, flag_on_open_chest

def handle_player_movement(stdscr, player, array_for_movement, list_doors, list_chests, transition, flag_on_new_level, flag_on_open_chest):

    def was_door_or_transition(x, y, list_doors, transition):
        for door in list_doors:
            if door.x == x and door.y == y:
                stdscr.addch(y,x,door.symbol)
                return True
        if x == transition.x and y == transition.y:
                stdscr.addch(y,x,"=", curses.color_pair(4))
                return True
        return False
    
    key = stdscr.getch()
    key = chr(key)
    x, y = player.x, player.y
    open_chest = None
    
    if key == 'w' or key == 'ц':#верх
        if array_for_movement[y - 1][x] == '1':
            if not was_door_or_transition(x, y, list_doors, transition):
                stdscr.addch(y,x," ")
            stdscr.addch(y - 1,x,"☻", curses.color_pair(2) | curses.A_BOLD)
            player.y -= 1
    elif key == 's' or key == 'ы':#вниз
        if array_for_movement[y + 1][x] == '1':
            if not was_door_or_transition(x, y, list_doors, transition):
                stdscr.addch(y,x," ")
            stdscr.addch(y + 1,x,"☻", curses.color_pair(2) | curses.A_BOLD)
            player.y += 1
    elif key == 'd' or key == 'в':#вправо
       if array_for_movement[y][x + 1] == '1':
            if not was_door_or_transition(x, y, list_doors, transition):
                stdscr.addch(y,x," ")
            stdscr.addch(y,x + 1,"☻", curses.color_pair(2) | curses.A_BOLD)
            player.x += 1
    elif key == 'a' or key == 'ф':#влево
        if array_for_movement[y][x - 1] == '1':
            if not was_door_or_transition(x, y, list_doors, transition):
                stdscr.addch(y,x," ")
            stdscr.addch(y,x - 1,"☻", curses.color_pair(2) | curses.A_BOLD)
            player.x -= 1
    elif key == 'e' or key == 'у':#открыть сундук
        if (array_for_movement[y - 1][x] == '2' or array_for_movement[y + 1][x] == '2' or array_for_movement[y][x + 1] == '2' or array_for_movement[y][x - 1] == '2'):
            flag_on_open_chest = True
            for chest in list_chests:
                if (((x+1 == chest.x or x-1 == chest.x) and y == chest.y) or ((y+1 == chest.y or y-1==chest.y) and x == chest.x)):
                    open_chest = chest
                    break

    elif key == 'f' or key == 'а':#начать бой
        #запуск окна боя
        pass
    else:
        pass
    
    if player.x == transition.x and player.y ==  transition.y:
        flag_on_new_level = True
        return player, open_chest, flag_on_new_level, flag_on_open_chest

    return player, open_chest, flag_on_new_level, flag_on_open_chest
