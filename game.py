import draw_map
import draw_other_elements
import curses
import Character
import Storage
import random
from Character import Enemy
from Battle_window_main import BattleWindow
from Storage import Corpse  
from working_with_sound import get_sound

def init_colors():
    curses.start_color()
    # Основные цвета (текст, фон)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)      # Красный - враги
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Зеленый - игрок
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Желтый - сундуки
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Синий - переходы
    curses.init_pair(8, 8, curses.COLOR_BLACK)                    # Серый (память)


def main(stdscr):
    init_colors()
    height, width = stdscr.getmaxyx()
    max_y, max_x = height - 1, width - 1
    
    curren_level = draw_other_elements.View_characteristics("curren_level", 9, 0, 1)
    view_health = draw_other_elements.View_characteristics("view_health", 24, 0, None)
    view_event = draw_other_elements.View_characteristics("view_event", 38, 0, " ")
    player = None
    visible = None
    flag_on_open_chest = False
    flag_clicking_on_another_button = False
    LIST_ROOMS = list() 
    LIST_CORRIDORS = list()
    LIST_DOORS = list()
    LIST_CHESTS = list()
    LIST_CORPSE = list()
    enemies = []

    while True:
        if LIST_ROOMS == list():
            
            #расчет карты
            LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, LIST_SECTION, start_room, transition = draw_map.calculate_all_objects_in_map(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_DOORS, LIST_CHESTS)

            #создание массива для передвижения по статическим объектам
            ARRAY_FOR_MOVEMENT = draw_map.creating_map_for_movement(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS)
            
            # чисто создать 3х врагов
            enemies = []
            for _ in range(3):  
                x = random.randint(start_room.start_point_x + 1, start_room.start_point_x + start_room.width - 1)
                y = random.randint(start_room.start_point_y + 1, start_room.start_point_y + start_room.height - 1)
                enemy_type = random.choice(["Слизень", "Гоблин", "Крыса"])
                enemies.append(Enemy(enemy_type, "e", 30 + random.randint(0, 20), 5 + random.randint(0, 10), x, y))

        player, flag_on_open_chest = Character.create_player(start_room, player, flag_on_open_chest)

        view_health.content = player.current_health
        draw_other_elements.draw_characteristics(stdscr, curren_level, view_health, view_event)

        while True:
            flag_on_new_level = False
            #получаем доступные для видимости элементы карты
            visible = draw_map.get_view_symbol(player.x, player.y, 4, max_x, max_y, visible)
            #отображаем карту с соответствующей видимостью
            draw_map.draw_all_object_in_map(stdscr, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, LIST_CORPSE, transition, player, visible)

            #рассчитываем передвижение врага по карте
            #enemies = Character.enemy_move_controller(ARRAY_FOR_MOVEMENT, enemies, player)

            # рисование врага на карте 
            for enemy in enemies:
                if (enemy.x, enemy.y) in visible:
                    stdscr.addch(enemy.y, enemy.x, enemy.letter, curses.color_pair(1))

            player, open_storage, flag_on_new_level, flag_on_open_chest, flag_clicking_on_another_button = Character.handle_player_movement(
                stdscr, player, ARRAY_FOR_MOVEMENT, LIST_DOORS, LIST_CHESTS, LIST_SECTION, LIST_CORPSE, transition, curren_level, view_health, view_event, flag_on_new_level, flag_on_open_chest, flag_clicking_on_another_button)

            if flag_clicking_on_another_button == True:
                view_event.content = "Для отображения списка команд нажмие - I"
                draw_other_elements.draw_characteristics(stdscr, curren_level, view_health, view_event)
                flag_clicking_on_another_button = False
                
            if flag_on_new_level == True:
                view_event.content = "Хотите перейти на следующий уровень? да-Y"
                draw_other_elements.draw_characteristics(stdscr, curren_level, view_health, view_event)
                key = stdscr.getch()
                key = chr(key)
                if key == 'y' or key == 'н' or key == 'Y' or key == 'Н':
                    curren_level.content += 1
                    stdscr.clear()
                    stdscr.refresh()
                    LIST_ROOMS = list() 
                    LIST_CORRIDORS = list()
                    LIST_DOORS = list()
                    LIST_CHESTS = list()
                    visible = None
                    view_event.content = " "
                    get_sound("open_transition.wav")
                    break
                else:
                    view_event.content = " "
                    draw_other_elements.draw_characteristics(stdscr, curren_level, view_health, view_event)
                    
            if flag_on_open_chest == True:
                Storage.open_storges(stdscr, LIST_SECTION, LIST_CHESTS, open_storage)
                break

            # Проверка
            for enemy in enemies[:]:
                if abs(player.x - enemy.x) <= 1 and abs(player.y - enemy.y) <= 1:
                    battle = BattleWindow(stdscr, player, enemy)
                    while battle.in_battle:
                        battle.draw()
                        key = stdscr.getch()
                        battle.handle_input(key)
                        if player.current_health <= 0:
                            return  # GG
                    
                    # замена врага трупом при победе
                    if enemy.current_health <= 0:
                        stdscr.clear()
                        enemies.remove(enemy)
                        corpse = Corpse(5, enemy.x, enemy.y)
                        LIST_CORPSE.append(corpse)
                        ARRAY_FOR_MOVEMENT[enemy.y][enemy.x] = "3"
                        break
                
                        
                

            stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
