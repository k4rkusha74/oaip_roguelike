import draw_map
import curses
import Character

def main(stdscr):
    curses.start_color()
    height, width = stdscr.getmaxyx()
    max_y, max_x = height - 1, width - 1 #запас
    curren_level = draw_map.View_characteristics("curren_level", 9, 0, 1)
    view_health = draw_map.View_characteristics("view_health", 24, 0, 100)
    view_event = draw_map.View_characteristics("view_event", 38, 0, " ")
    player = None
    LIST_ROOMS = list() 
    LIST_CORRIDORS = list()
    LIST_DOORS = list()
    LIST_CHESTS = list()
    
    while True:
        
        #расчет и отрисовка карты
        LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, start_room, transition = draw_map.calculate_all_objects_in_map(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_DOORS, LIST_CHESTS)
        draw_map.draw_all_object_in_map(stdscr, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, transition)

        #создание массива для передвижения
        ARRAY_FOR_MOVEMENT = draw_map.creating_map_for_movement(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS)
        
        #добавляем персонажа
        player = Character.create_player(start_room, player)
        stdscr.addch(player.y, player.x, player.letter)
        
        #вывод характеристик
        draw_map.draw_characteristics(stdscr, curren_level, view_health, view_event)

        while True:
            flag_on_new_level = False
            #обработка передвижения врага
            #move_enemies(enemies, player, game_map)

            #обработка передвижения игрока
            player, flag_on_new_level = Character.handle_player_movement(stdscr, player, ARRAY_FOR_MOVEMENT, LIST_DOORS, transition, flag_on_new_level)
            
            if flag_on_new_level == True:
                view_event.content = "Хотите перейти на следующий уровень? да-Y, нет-N"
                draw_map.draw_characteristics(stdscr, curren_level, view_health, view_event)
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
                    view_event.content = " "
                    break

        
            stdscr.refresh()
        

if __name__ == "__main__":
    curses.wrapper(main)