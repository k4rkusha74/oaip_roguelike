import draw_map
import curses
import random
import Character

def main(stdscr):
    curses.start_color()
    height, width = stdscr.getmaxyx()
    max_y, max_x = height - 1, width - 1 #запас

    LIST_ROOMS = list() #сохранение карты
    LIST_CORRIDORS = list()
    LIST_DOORS = list()
    LIST_CHESTS = list()

    #расчет и отрисовка карты
    LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, start_room, transition = draw_map.calculate_all_objects_in_map(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_DOORS, LIST_CHESTS)
    draw_map.draw_all_object_in_map(stdscr, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, transition)

    #создание массива для передвижения
    ARRAY_FOR_MOVEMENT = draw_map.creating_map_for_movement(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS)
    
    #добавляем персонажа
    player = Character.create_player(start_room)
    stdscr.addch(player.y, player.x, player.letter)
    

    # key = stdscr.getch()
    # key = chr(key)
    
    # stdscr.addstr(0,0,key)
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)