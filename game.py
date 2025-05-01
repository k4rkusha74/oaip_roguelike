import draw_map
import curses
import Character
import Storage

def main(stdscr):
    curses.start_color()
    height, width = stdscr.getmaxyx()
    max_y, max_x = height - 1, width - 1 #запас
    curren_level = draw_map.View_characteristics("curren_level", 9, 0, 1)
    
    view_health = draw_map.View_characteristics("view_health", 24, 0, 100)
    view_event = draw_map.View_characteristics("view_event", 38, 0, " ")
    player = None
    flag_on_open_chest = False
    LIST_ROOMS = list() 
    LIST_CORRIDORS = list()
    LIST_DOORS = list()
    LIST_CHESTS = list()
    
    while True:
        
        if LIST_ROOMS == list():
        #расчет и отрисовка карты
            LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, LIST_SECTION, start_room, transition = draw_map.calculate_all_objects_in_map(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_DOORS, LIST_CHESTS)
        draw_map.draw_all_object_in_map(stdscr, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS, transition)

        #создание массива для передвижения по статическим объектам
        ARRAY_FOR_MOVEMENT = draw_map.creating_map_for_movement(max_y, max_x, LIST_ROOMS, LIST_CORRIDORS, LIST_CHESTS)
        
        #добавляем персонажа по соответствующим координатам
        player, flag_on_open_chest = Character.create_player(start_room, player, flag_on_open_chest)
        stdscr.addch(player.y, player.x, player.letter)
        
        #вывод характеристик
        draw_map.draw_characteristics(stdscr, curren_level, view_health, view_event)

        while True:
            flag_on_new_level = False
            
            #обработка передвижения врага
            #move_enemies(enemies, player, game_map)

            #обработка передвижения игрока
            player, open_chest, flag_on_new_level, flag_on_open_chest = Character.handle_player_movement(stdscr, player, ARRAY_FOR_MOVEMENT, LIST_DOORS, LIST_CHESTS, transition, flag_on_new_level, flag_on_open_chest)
            
            if flag_on_new_level == True:
                view_event.content = "Хотите перейти на следующий уровень? да-Y"
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
                else:
                    view_event.content = " "
                    draw_map.draw_characteristics(stdscr, curren_level, view_health, view_event)
                    
            if flag_on_open_chest == True:
                Storage.open_storges(stdscr, LIST_SECTION, open_chest)
                break

        
            stdscr.refresh()
        

if __name__ == "__main__":
    curses.wrapper(main)