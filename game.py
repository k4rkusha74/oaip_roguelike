import draw_map
import draw_other_elements
import curses
import Character
import Storage
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
    max_y, max_x = height - 1, width - 1 #запас
    curren_level = draw_map.View_characteristics("curren_level", 9, 0, 1)
    view_health = draw_map.View_characteristics("view_health", 24, 0, 30)
    view_event = draw_map.View_characteristics("view_event", 38, 0, " ")
    player = None
    visible = None
    flag_on_open_chest = False
    flag_clicking_on_another_button = False
    LIST_ROOMS = list() 
    LIST_CORRIDORS = list()
    LIST_DOORS = list()
    LIST_CHESTS = list()
    
    while True:
        
        if LIST_ROOMS == list():
            
            #расчет карты
            LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, LIST_SECTION, start_room, transition = draw_map.calculate_all_objects_in_map(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_DOORS, LIST_CHESTS)

            #создание массива для передвижения по статическим объектам
            ARRAY_FOR_MOVEMENT = draw_map.creating_map_for_movement(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS)

        #добавляем персонажа по соответствующим координатам
        player, flag_on_open_chest = Character.create_player(start_room, player, flag_on_open_chest)
        
        #вывод характеристик
        draw_other_elements.draw_characteristics(stdscr, curren_level, view_health, view_event)

        while True:

            flag_on_new_level = False
            #получаем доступные для видимости элементы карты
            visible = draw_map.get_view_symbol(player.x, player.y, 4, max_x, max_y, visible)
             #отображаем карту с соответствующей видимостью
            draw_map.draw_all_object_in_map(stdscr, max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, transition, player, visible)

            #обработка передвижения врага
            #move_enemies(enemies, player, game_map)

            #обработка передвижения игрока
            player, open_chest, flag_on_new_level, flag_on_open_chest, flag_clicking_on_another_button = Character.handle_player_movement(stdscr, 
            player, ARRAY_FOR_MOVEMENT, LIST_DOORS, LIST_CHESTS, LIST_SECTION, transition, curren_level, view_health, view_event,
            flag_on_new_level, flag_on_open_chest, flag_clicking_on_another_button)

            if flag_clicking_on_another_button == True:
                view_event.content = "Для отображения списка команд нажмие - I"
                draw_other_elements.draw_characteristics(stdscr, curren_level, view_health, view_event)
                flag_clicking_on_another_button = False

            if flag_on_new_level == True:
                view_event.content = "Хотите перейти на следующий уровень? да-Y"
                draw_other_elements.draw_characteristics(stdscr, curren_level, view_health, view_event)
                key = stdscr.getch()
                key = chr(key)
                if key == 'y' or key == 'н':
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
                Storage.open_storges(stdscr, LIST_SECTION, open_chest)
                break

        
            stdscr.refresh()
        

if __name__ == "__main__":
    curses.wrapper(main)