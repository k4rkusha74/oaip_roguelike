import curses
from curses import ascii
import random
from sys import setrecursionlimit
setrecursionlimit(1_000_000)


class Cube:
    def __init__(self, height, width, start_point_x, start_point_y):
        
        self.height = height
        self.width = width
        self.start_point_x = start_point_x
        self.start_point_y = start_point_y

class Door:
    def __init__(self, x, y, orientation, symbol):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.symbol = symbol
    def symbol_door(self):
        if self.orientation == "horizontal":
            self.symbol = "|"
        else:
            self.symbol = "-"

        return self.symbol

class Corridor:
    def __init__(self, bend_x, bend_y):
        self.bend_x = bend_x
        self.bend_y = bend_y
        self.doors = []

    def add_door(self, door):
        self.doors.append((door))
        
class Room(Cube):
    def __init__(self, height, width, start_point_x, start_point_y):
        super().__init__(height, width, start_point_x, start_point_y)
        self.doors = []
    
    def add_door(self, door):
        self.doors.append((door))

    def key_func(obj):
            if isinstance(obj, Room):
                return obj.start_point_x
            
#рисуем рамку игры и камнаты
def draw_rectangle(stdscr, start_x, start_y, end_x, end_y, index_cube):#
    
    if index_cube == 1:
        vertical_line = "║"
        horizontal_line = "═"
        LU_corner = "╔"
        LD_corner = "╚"
        RU_corner = "╗"
        RD_corner = "╝"
    elif index_cube == 2:
        vertical_line = curses.ACS_VLINE
        horizontal_line = curses.ACS_HLINE
        LU_corner = curses.ACS_ULCORNER
        LD_corner = curses.ACS_LLCORNER
        RU_corner = curses.ACS_URCORNER
        RD_corner = curses.ACS_LRCORNER

    #углы
    try:
        stdscr.addch(start_y, start_x, LU_corner)
        stdscr.addch(start_y, end_x, RU_corner)
        stdscr.addch(end_y, start_x, LD_corner)
        stdscr.addch(end_y, end_x, RD_corner)
    except:
        pass
        
    #горизонтальные линии
    for x in range(1, end_x - start_x):
        try:
            stdscr.addch(start_y, start_x + x, horizontal_line)
            stdscr.addch(end_y, start_x + x, horizontal_line)
        except:
            continue
        
    #вертикальные линии 
    for y in range(1,  end_y - start_y):
        try:
            stdscr.addch(start_y + y, start_x, vertical_line)
            stdscr.addch(start_y + y, end_x, vertical_line)
        except:
            continue

#рисуем коридоры и двери
def draw_corridor(stdscr, corridor):
    
    if corridor.doors[0].y < corridor.doors[1].y:
        sign = 1
    else:
        sign = -1

    x = corridor.doors[0].x
    y = corridor.doors[0].y

    while x != corridor.doors[1].x:
        stdscr.addch(corridor.doors[0].y, x, "-")
        x += 1

    while y != corridor.doors[1].y:
        stdscr.addch(y, corridor.doors[1].x, "|")
        y += sign

    for door in corridor.doors: #рисуем двери
        symbol = door.symbol_door()
        stdscr.addch(door.y, door.x, symbol)
    

    


    
def calculate_rooms(stdscr, max_y, max_x, list_rooms): 
    h = random.randint(int(max_y / 6), int(max_y / 4))
    w = random.randint(int(max_x / 6), int(max_x / 4))
    
    min_size = 3
    padding = 3
    max_attempts = 100 
    
    for _ in range(max_attempts):
        
        start_point_x = random.randint(min_size, max_x - w - min_size)
        start_point_y = random.randint(min_size, max_y - h - min_size)
        end_point_x = start_point_x + w
        end_point_y = start_point_y + h
        
        flag = False
        for room in list_rooms:
            if not (end_point_x + padding < room.start_point_x  or 
                    start_point_x > room.start_point_x + room.width + padding or
                    end_point_y + padding < room.start_point_y or
                    start_point_y > room.start_point_y + room.height + padding):
                flag = True
                break
        
        if not flag:
            room = Room(h, w, start_point_x, start_point_y)
            list_rooms.append(room)
            
            return 1
    
    return -1

#добавление двери к комнате
def add_door_in_room(y, x, list_rooms, orientation):
    for room in list_rooms:
        if (x == room.start_point_x and (room.start_point_y < y < room.start_point_y + room.height) or
        x == room.start_point_x + room.width and (room.start_point_y < y < room.start_point_y + room.height) or
        y == room.start_point_y and (room.start_point_x < x < room.start_point_x + room.width) or
        y == room.start_point_y + room.height and (room.start_point_x < x < room.start_point_x + room.width)):
            door = Door(x, y, orientation, " ")
            room.add_door(door)
            return door
    return None
            
#точка в углу комнаты
def needs_redraw(y1, x2, list_rooms):
    for room in list_rooms:
        if (((y1 == room.start_point_y or 
            y1 == room.start_point_y + room.height) and x2 > room.start_point_x) or 
            x2 == room.start_point_x or 
            x2 == room.start_point_x + room.width):
            return True
    return False

#точка в комнате
def point_in_room(x, y, list_rooms):
    flag = False
    for room in list_rooms:
            if (room.start_point_x < x < room.start_point_x + room.width and
                room.start_point_y < y < room.start_point_y + room.height):
                flag = True
    return flag

#перегенирация карты
def handle_redraw(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Перегенерация карты...")
    stdscr.refresh()
    curses.napms(500)  
    curses.endwin()
    main(stdscr)

#высчитываем коридор и двери к нему
def calculate_corridor_and_door(stdscr, room1, room2, list_rooms, list_corridor):
    list_doors = list()
    # Центры комнат
    x1 = room1.start_point_x + room1.width // 2
    y1 = room1.start_point_y + room1.height // 2
    x2 = room2.start_point_x + room2.width // 2
    y2 = room2.start_point_y + room2.height // 2
    
    is_corner = needs_redraw(y1, x2, list_rooms) #заходит ли коридор в угол комнты
    if is_corner == True:
        handle_redraw(stdscr)
        return None
    
    # Горизонтальная часть
    if x2 > x1:
        step_x = 1
    else:
        step_x = -1
    for x in range(x1, x2 + step_x, step_x):
        orientation = "horizontal"
        flag = point_in_room(x, y1, list_rooms)
        if flag == False:
            door = add_door_in_room(y1, x, list_rooms, orientation)
            if door != None:#если мы находимся на периметре комнаты
                list_doors.append(door)

    # Вертикальная часть
    if y2 > y1:
        step_y = 1 
    else:
        step_y = -1
    for y in range(y1, y2 + step_y, step_y):
        orientation = "vertical"
        flag = point_in_room(x2, y, list_rooms)
        if flag == False:
            door = add_door_in_room(y, x2, list_rooms, orientation)
            if door != None:#если мы находимся на периметре комнаты
                list_doors.append(door)

    for i in range(0, len(list_doors) - 1, 2):
        corridor = Corridor(x2, y1)
        corridor.add_door(list_doors[i])
        corridor.add_door(list_doors[i+1])
        list_corridor.append(corridor)
        
#высчитываем все объекты на карте
def calculate_all_objects_in_map(stdscr, max_y, max_x, list_rooms, list_corridor):
    count_room = random.randint(4,6)
    #высчитываем комнаты
    for _ in range(count_room):            
        answear = calculate_rooms(stdscr, max_y, max_x, list_rooms)
        if answear == -1:
            break

    if len(list_rooms) <= 2:
        handle_redraw(stdscr)
        return None
    
    #сортируем комнаты по X координате
    list_rooms = sorted(list_rooms, key=lambda room: room.start_point_x)

    #вычисляем коридоры и двери
    for i in range(len(list_rooms) - 1):
        flag = False
        if list_rooms[i+1].doors:
            flag = True
        if flag == False:
            calculate_corridor_and_door(stdscr, list_rooms[i], list_rooms[i+1], list_rooms, list_corridor)

#рисуем все объекты на карте
def draw_map(stdscr, max_y, max_x, list_rooms, list_corridor):
    curses.curs_set(0)#скрываем курсор
    draw_rectangle(stdscr, 0, 0, max_x, max_y, 1)#рисуем окно

    for room in list_rooms: #рисуем комнаты
        draw_rectangle(stdscr, room.start_point_x, room.start_point_y, room.start_point_x + room.width, room.start_point_y + room.height, 1)
    
    for corridor in list_corridor:#рисуем коридоры
        draw_corridor(stdscr, corridor)

def main(stdscr):
    height, width = stdscr.getmaxyx()
    max_y, max_x = height - 1, width - 1 #запас
    list_rooms = list()
    list_corridor = list()
    

    calculate_all_objects_in_map(stdscr, max_y, max_x, list_rooms, list_corridor)
    draw_map(stdscr, max_y, max_x, list_rooms, list_corridor)
    
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)