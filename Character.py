from Storage import Chest, Inventory, Arming, ArmorStorage 
from Item import *
import curses
import random
from draw_other_elements import draw_info_grid, draw_characteristics
from working_with_sound import get_sound

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

def create_enemy(start_room):
    # чисто создать 2х врагов
    enemies = []
    for _ in range(2):  
        x = random.randint(start_room.start_point_x + 1, start_room.start_point_x + start_room.width - 1)
        y = random.randint(start_room.start_point_y + 1, start_room.start_point_y + start_room.height - 1)
        enemy_type = random.choice(["Слизень", "Гоблин", "Крыса"])
        enemies.append(Enemy(enemy_type, "e", 30 + random.randint(0, 20), 5 + random.randint(0, 10), x, y))

    return enemies

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

def was_door_or_transition(x, y, list_doors, transition, stdscr):
        for door in list_doors:
            if door.x == x and door.y == y:
                stdscr.addch(y,x,door.symbol)
                return True
        if x == transition.x and y == transition.y:
                stdscr.addch(y,x,"=", curses.color_pair(4))
                return True
        return False

def handle_player_movement(stdscr, player, array_for_movement, list_doors, list_chests, list_section, list_corpse, transition, curren_level, view_health, view_event, flag_on_new_level, flag_on_open_chest, flag_clicking_on_another_button):
    key = stdscr.getch()
    key = chr(key)
    x, y = player.x, player.y
    open_storage = None
    
    if key == 'w' or key == 'ц' or key == 'W' or key == 'Ц':#верх
        if array_for_movement[y - 1][x] == '1':
            if not was_door_or_transition(x, y, list_doors, transition, stdscr):
                stdscr.addch(y,x," ")
            stdscr.addch(y - 1,x,"☻", curses.color_pair(2) | curses.A_BOLD)
            player.y -= 1
    elif key == 's' or key == 'ы' or key == 'S' or key == 'Ы':#вниз
        if array_for_movement[y + 1][x] == '1':
            if not was_door_or_transition(x, y, list_doors, transition, stdscr):
                stdscr.addch(y,x," ")
            stdscr.addch(y + 1,x,"☻", curses.color_pair(2) | curses.A_BOLD)
            player.y += 1
    elif key == 'd' or key == 'в' or key == 'D' or key == 'В':#вправо
       if array_for_movement[y][x + 1] == '1':
            if not was_door_or_transition(x, y, list_doors, transition, stdscr):
                stdscr.addch(y,x," ")
            stdscr.addch(y,x + 1,"☻", curses.color_pair(2) | curses.A_BOLD)
            player.x += 1
    elif key == 'a' or key == 'ф' or key == 'A' or key == 'Ф':#влево
        if array_for_movement[y][x - 1] == '1':
            if not was_door_or_transition(x, y, list_doors, transition, stdscr):
                stdscr.addch(y,x," ")
            stdscr.addch(y,x - 1,"☻", curses.color_pair(2) | curses.A_BOLD)
            player.x -= 1
    elif key == 'e' or key == 'у' or key == 'E' or key == 'У':#открыть сундук и покапаться в трупе
        if (array_for_movement[y - 1][x] == '2' or array_for_movement[y + 1][x] == '2' or array_for_movement[y][x + 1] == '2' or array_for_movement[y][x - 1] == '2'):
            flag_on_open_chest = True
            get_sound("open_chest.wav")
            for chest in list_chests:
                if (((x+1 == chest.x or x-1 == chest.x) and y == chest.y) or ((y+1 == chest.y or y-1==chest.y) and x == chest.x)):
                    open_storage = chest
                    break
        elif (array_for_movement[y - 1][x] == '3' or array_for_movement[y + 1][x] == '3' or array_for_movement[y][x + 1] == '3' or array_for_movement[y][x - 1] == '3'):
            flag_on_open_chest = True
            get_sound("examine_corpse.wav")
            for corpse in list_corpse:
                if (((x+1 == corpse.x or x-1 == corpse.x) and y == corpse.y) or ((y+1 == corpse.y or y-1==corpse.y) and x == corpse.x)):
                    open_storage = corpse
                    break
    elif key == 'I' or key == 'i' or key == 'Ш' or key == 'ш':#вывод информации
        draw_info_grid(stdscr, list_section)
        view_event.content = " "
        draw_characteristics(stdscr, curren_level, view_health, view_event)
    else:
        flag_clicking_on_another_button = True

    
    if player.x == transition.x and player.y ==  transition.y:
        flag_on_new_level = True
        return player, open_storage, flag_on_new_level, flag_on_open_chest, flag_clicking_on_another_button

    return player, open_storage, flag_on_new_level, flag_on_open_chest, flag_clicking_on_another_button

def enemy_move_controller(array_for_movement, enemies, player, list_doors, transition, stdscr):
    list_move = ["up", "down", "left", "right"]
    vision_radius = 5
    for enemy in enemies:
        distance = abs(enemy.x - player.x) + abs(enemy.y - player.y)

        # Проверяем видимость игрока
        if distance < vision_radius:
            # Преследование игрока
            move_towards_player(enemy, player, array_for_movement, list_doors, transition, stdscr)
        else:
            # Случайное блуждание
            random_wander(enemy, list_move, array_for_movement, list_doors, transition, stdscr)

    return enemies


def move_towards_player(enemy, player, game_map, list_doors, transition, stdscr):
    
    dx = player.x - enemy.x
    dy = player.y - enemy.y
    
    # Определяем приоритет направления движения
    if abs(dx) > abs(dy):
        direction = "right" if dx > 0 else "left"
    else:
        direction = "down" if dy > 0 else "up"
    
    # Пробуем двигаться в выбранном направлении
    new_x, new_y = enemy.x, enemy.y
    if direction == "up":
        if game_map[new_y-1][new_x] == '1':
            new_y -= 1
    elif direction == "down":
        if game_map[new_y+1][new_x] == '1':
            new_y += 1
    elif direction == "left":
        if game_map[new_y][new_x-1] == '1':
            new_x -= 1
    elif direction == "right":
        if game_map[new_y][new_x+1] == '1':
            new_x += 1
        
    if not was_door_or_transition(new_x, new_y, list_doors, transition, stdscr):
        stdscr.addch(enemy.y, enemy.x, ' ')
        enemy.x, enemy.y = new_x, new_y


def random_wander(enemy, possible_moves, game_map, list_doors, transition, stdscr):
    from random import choice
    
    valid_moves = []
    for move in possible_moves:
        x, y = enemy.x, enemy.y
        if move == "up" and game_map[y-1][x] == '1':
            valid_moves.append((x, y-1))
        elif move == "down" and game_map[y+1][x] == '1':
            valid_moves.append((x, y+1))
        elif move == "left" and game_map[y][x-1] == '1':
            valid_moves.append((x-1, y))
        elif move == "right" and game_map[y][x+1] == '1':
            valid_moves.append((x+1, y))
            
    if valid_moves:
        new_x, new_y = choice(valid_moves)
        
        if not was_door_or_transition(new_x, new_y, list_doors, transition, stdscr):
            stdscr.addch(enemy.y, enemy.x, ' ')
            enemy.x, enemy.y = new_x, new_y